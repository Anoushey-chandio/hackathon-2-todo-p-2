from typing import Optional, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.database import get_db
from src.models.user import User
from src.models.chat import Conversation, Message
from src.models.task import Task
from src.api.deps import get_current_user
from src.core.llm import client, MODEL_NAME
import uuid
import json
import re
from pydantic import BaseModel

router = APIRouter()


# =========================
# Schemas
# =========================
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[uuid.UUID] = None


class ChatMessageResponse(BaseModel):
    response: str
    conversation_id: uuid.UUID
    action_taken: Optional[str] = None


# =========================
# Helpers
# =========================
async def get_user_tasks(db: AsyncSession, user_id: uuid.UUID):
    result = await db.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.asc())
    )
    return result.scalars().all()


# =========================
# Main Chat Endpoint
# =========================
@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # 1️⃣ Conversation setup
    conv_id = request.conversation_id
    if not conv_id:
        conv = Conversation(user_id=current_user.id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conv_id = conv.id

    # 2️⃣ Save user message
    db.add(
        Message(
            conversation_id=conv_id,
            role="user",
            content=request.message,
        )
    )
    await db.commit()

    user_input = request.message.lower().strip()
    action_taken = None

    # =========================
    # 🔍 VIEW TASK
    # =========================
    if re.match(r"(view|show) task \d+", user_input):
        task_number = int(re.findall(r"\d+", user_input)[0])
        tasks = await get_user_tasks(db, current_user.id)

        if 0 < task_number <= len(tasks):
            task = tasks[task_number - 1]
            assistant_content = (
                f"📌 Task {task_number}\n"
                f"Title: {task.title}\n"
                f"Status: {task.status}"
            )
        else:
            assistant_content = "❌ Task number not found."

    # =========================
    # ✅ COMPLETE TASK
    # =========================
    elif re.match(r"(complete|done|finish) task \d+", user_input):
        task_number = int(re.findall(r"\d+", user_input)[0])
        tasks = await get_user_tasks(db, current_user.id)

        if 0 < task_number <= len(tasks):
            task = tasks[task_number - 1]
            task.status = "completed"
            db.add(task)
            await db.commit()

            action_taken = "task_completed"
            assistant_content = f"✅ Task '{task.title}' marked as completed."
        else:
            assistant_content = "❌ Task number not found."

    # =========================
    # ➕ ADD TASK (LLM)
    # =========================
    else:
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a task manager. "
                            "If user wants to add a task, respond ONLY in JSON:\n"
                            '{"action":"add_task","title":"...","description":"..."}'
                        ),
                    },
                    {"role": "user", "content": request.message},
                ],
            )

            content = response.choices[0].message.content

            # Try JSON parse
            try:
                parsed = json.loads(content)
                if parsed.get("action") == "add_task":
                    task = Task(
                        title=parsed.get("title"),
                        description=parsed.get("description", ""),
                        user_id=current_user.id,
                    )
                    db.add(task)
                    await db.commit()
                    action_taken = "task_added"

                    tasks = await get_user_tasks(db, current_user.id)
                    task_list = "\n".join(
                        [f"{i+1}. {t.title}" for i, t in enumerate(tasks)]
                    )

                    assistant_content = (
                        f"✅ Task '{task.title}' has been added.\n\n"
                        f"📋 Current Tasks:\n{task_list}\n\n"
                        "Would you like to add another task, view a task, "
                        "or mark a task as completed?"
                    )
                else:
                    assistant_content = content
            except json.JSONDecodeError:
                assistant_content = content

        except Exception as e:
            print("LLM Error:", e)
            assistant_content = "⚠️ AI is not responding right now."

    # 3️⃣ Save assistant message
    db.add(
        Message(
            conversation_id=conv_id,
            role="assistant",
            content=assistant_content,
        )
    )
    await db.commit()

    return ChatMessageResponse(
        response=assistant_content,
        conversation_id=conv_id,
        action_taken=action_taken,
    )
