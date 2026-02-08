# Implementation Plan - Todo Chatbot

**Feature**: `015-todo-chatbot`
**Status**: Planned

## Technical Context

- **Frontend**: Next.js 15+, Tailwind CSS. We will add a `ChatWidget` component.
- **Backend**: FastAPI. New `api/endpoints/chat.py`.
- **Database**: Neon (PostgreSQL) via SQLModel. New `Conversation` and `Message` models.
- **AI**: OpenAI Python SDK pointing to OpenRouter.

## Constitution Check

- [x] **Modern Tech Stack**: Uses Next.js/FastAPI.
- [x] **Secure Multi-User Access**: Chat endpoints will be protected by `get_current_user` dependency.
- [x] **Thematic Design**: Chat UI will match the "light purple" theme.
- [x] **Code Quality**: Separated concerns (models, api, logic).
- [x] **Database Integrity**: Uses Alembic for migrations.

## Phases

### Phase 1: Backend Foundations & Data Layer

1. **Models**: Create `backend/src/models/chat.py` with `Conversation` and `Message`.
2. **Migrations**: Run `alembic revision` to create tables.
3. **API Skeleton**: Create `backend/src/api/endpoints/chat.py` with empty endpoints.
4. **Router**: Register `chat` router in `backend/src/api/api.py`.

### Phase 2: AI Logic & Backend Implementation

1. **OpenAI Client**: Configure `AsyncOpenAI` client in `backend/src/core/llm.py` (new file) using `OPENROUTER_API_KEY`.
2. **Tools Definition**: Define `add_task` tool schema for the LLM.
3. **Chat Logic**: Implement `POST /api/chat/message`:
   - Save User message.
   - Fetch history.
   - Call LLM with tools.
   - If tool call -> execute `create_task` logic -> add result to history -> call LLM again (optional, or just return).
   - Save Assistant message.
   - Return response.

### Phase 3: Frontend UI

1. **Install SDK**: `npm install ai` (Vercel AI SDK) or just use standard `fetch` if preferred for simplicity. *Decision*: Use standard `fetch` + React state for maximum control and simplicity given the constraints, unless streaming is strictly required. The spec didn't mandate streaming, but "ChatKit" implies a good UI.
2. **Components**:
   - `components/Chat/ChatWidget.tsx`: The floating button and window.
   - `components/Chat/MessageList.tsx`: Scrollable area.
   - `components/Chat/MessageInput.tsx`: Text area.
3. **Integration**: Add `ChatWidget` to `app/tasks/page.tsx`.
4. **State Management**: Ensure `onTaskAdded` callback refreshes the main task list.

### Phase 4: Integration & Refinement

1. **History Loading**: Implement `GET /api/chat/history` and load on mount.
2. **Error Handling**: Handle OpenRouter timeouts or API errors.
3. **Styling**: Polish the UI to match the "cartoon" theme.