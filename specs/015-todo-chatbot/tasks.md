# Tasks: Todo Chatbot

**Feature**: `015-todo-chatbot`
**Status**: Ready
**Total Tasks**: 21
**Story Count**: 2

## Phase 1: Setup

Goal: Initialize the data layer and API structure required for the chatbot.

- [ ] T001 Create `Conversation` and `Message` models in `backend/src/models/chat.py`
- [ ] T002 Register new models in `backend/src/models/__init__.py`
- [ ] T003 Generate Alembic revision for chat tables in `backend/migrations/versions`
- [ ] T004 Apply database migrations to create `conversation` and `message` tables
- [ ] T005 Create `backend/src/api/endpoints/chat.py` with placeholder endpoints
- [ ] T006 Register `chat` router in `backend/src/api/api.py`

## Phase 2: Foundational

Goal: Establish LLM connectivity and backend infrastructure.

- [ ] T007 Configure `AsyncOpenAI` client in `backend/src/core/llm.py` using `OPENROUTER_API_KEY`
- [ ] T008 [P] Define `add_task` tool schema in `backend/src/core/llm.py`
- [ ] T009 Install `ai` (Vercel AI SDK) dependency in `frontend`

## Phase 3: User Story 1 - Add Task via Chat (P1)

Goal: Enable users to add tasks via natural language.
**Independent Test**: User types "Add buy milk", system creates task and confirms.

- [ ] T010 [US1] Implement `POST /api/chat/message` in `backend/src/api/endpoints/chat.py` to handle tool calling logic
- [ ] T011 [US1] Implement logic to save User and Assistant messages to DB in `backend/src/api/endpoints/chat.py`
- [ ] T012 [P] [US1] Create `frontend/src/components/Chat/MessageList.tsx` component
- [ ] T013 [P] [US1] Create `frontend/src/components/Chat/MessageInput.tsx` component
- [ ] T014 [US1] Create `frontend/src/components/Chat/ChatWidget.tsx` integrating list and input
- [ ] T015 [US1] Integrate `ChatWidget` into `frontend/src/app/tasks/page.tsx`
- [ ] T016 [US1] Implement callback mechanism to refresh tasks when chatbot adds a task

## Phase 4: User Story 2 - Persistent Conversation History (P2)

Goal: Load and display past chat history.
**Independent Test**: Refresh page, previous messages reappear.

- [ ] T017 [US2] Implement `GET /api/chat/history` endpoint in `backend/src/api/endpoints/chat.py`
- [ ] T018 [US2] Update `ChatWidget` to fetch history on mount in `frontend/src/components/Chat/ChatWidget.tsx`
- [ ] T019 [US2] Ensure proper error handling for network/LLM failures in frontend components
- [ ] T020 [US2] Style Chat UI to match cartoon theme in `frontend/src/components/Chat/ChatWidget.tsx`

## Phase 5: Polish & Cross-Cutting

- [ ] T021 Verify all LLM responses are sanitized and errors are graceful

## Dependencies

- **US1** depends on **Phase 1** & **Phase 2** (Models, API, LLM Client)
- **US2** depends on **US1** (Message saving logic)

## Parallel Execution Opportunities

- T008 (Tool Definition) can run parallel to T001-T006 (DB Setup)
- T012/T013 (Frontend Components) can run parallel to T010/T011 (Backend Logic)
