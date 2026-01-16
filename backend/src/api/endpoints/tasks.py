from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskOut
from src.api.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskOut])
async def read_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
):
    result = await db.execute(
        select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    task = Task(**task_in.model_dump(), user_id=current_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@router.get("/{id}", response_model=TaskOut)
async def read_task(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    result = await db.execute(select(Task).where(Task.id == id, Task.user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{id}", response_model=TaskOut)
async def update_task(
    id: int,
    task_update: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    result = await db.execute(select(Task).where(Task.id == id, Task.user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    result = await db.execute(select(Task).where(Task.id == id, Task.user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()

# Removed separate /{id}/complete endpoint in favor of generic PATCH
