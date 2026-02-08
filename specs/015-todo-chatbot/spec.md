# Feature Specification: Todo Chatbot Module

**Feature Branch**: `015-todo-chatbot`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Create a concise specification for a "Todo Chatbot" module to integrate into the existing Todo project. Context: - Existing Todo app (from previous step) - Goal: Add a chatbot floating button on tasks page. - User can type commands like "Add a task to buy groceries". - Chatbot should: - Parse intent - Call existing backend API to add tasks - Reflect new tasks in frontend task list - Maintain all existing task operations (delete, update, complete/incomplete) - Tech stack: - Frontend: OpenAI ChatKit - Backend: FastAPI endpoint for chatbot - AI logic: OpenAI Agents SDK - LLM: OpenRouter API key from .env - Conversation history should be stored in database. Output: Short, clear, concise specification document for chatbot module."

## User Scenarios & Testing

### User Story 1 - Add Task via Chat (Priority: P1)

As a user, I want to add tasks using natural language in a chat interface so that I can quickly capture to-dos without filling out a form.

**Why this priority**: Core functionality of the chatbot module.

**Independent Test**: Can be tested by opening the chat, typing "Add a task to call mom", and verifying "Call mom" appears in the task list.

**Acceptance Scenarios**:

1. **Given** a logged-in user on the tasks page, **When** they click the floating chat button, **Then** the chat interface opens.
2. **Given** an open chat, **When** the user types "Add buy milk", **Then** the chatbot confirms the action ("Added 'buy milk' to your list") AND the task "buy milk" appears in the main task list.
3. **Given** an ambiguous request, **When** the user types "milk", **Then** the chatbot asks for clarification (e.g., "Do you want to add 'milk' as a task?").

---

### User Story 2 - Persistent Conversation History (Priority: P2)

As a user, I want my chat history to be saved so that I can review previous interactions or continue a conversation after reloading the page.

**Why this priority**: Enhances user experience by providing context and continuity.

**Independent Test**: Can be tested by sending messages, refreshing the page, and verifying the messages are still visible.

**Acceptance Scenarios**:

1. **Given** a user with previous chat messages, **When** they log in or refresh the page, **Then** the previous conversation history is loaded and displayed.
2. **Given** a new user, **When** they open the chat, **Then** they see an empty state or welcome message.

---

### Edge Cases

- **API Failure**: If the LLM provider (OpenRouter) is down, the chatbot should gracefully inform the user ("I'm having trouble connecting right now. Please try again later.").
- **Rate Limiting**: If the user sends too many messages quickly, the system should handle rate limits appropriately without crashing.
- **Unauthorized Access**: Users should only access their own conversation history.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a floating action button (FAB) on the tasks page to toggle the chat interface.
- **FR-002**: System MUST use OpenAI ChatKit for the frontend chat UI.
- **FR-003**: System MUST expose a FastAPI endpoint to handle chat messages and intent parsing.
- **FR-004**: System MUST use OpenAI Agents SDK to parse user intent from natural language.
- **FR-005**: System MUST call the existing internal Task API (or service layer) to create tasks when the intent is "add task".
- **FR-006**: System MUST persist all chat messages (User and Assistant) in the database (Neon/PostgreSQL).
- **FR-007**: System MUST update the frontend task list automatically (e.g., via shared state or re-fetch) when a task is added via chat.
- **FR-008**: System MUST authenticate chat requests using the existing session-based auth.
- **FR-009**: System MUST use the OpenRouter API for LLM inference, configured via `.env`.

### Technical Constraints

- **Frontend**: OpenAI ChatKit
- **Backend**: FastAPI, OpenAI Agents SDK
- **LLM**: OpenRouter API
- **Database**: Neon (PostgreSQL) - New tables for `Conversation` and `Message`

### Key Entities

- **Conversation**: Represents a chat thread.
  - `id` (UUID): Unique identifier.
  - `user_id` (UUID): Owner of the conversation.
  - `created_at` (DateTime): Timestamp.

- **Message**: Represents a single message in a thread.
  - `id` (UUID): Unique identifier.
  - `conversation_id` (UUID): Link to Conversation.
  - `role` (String): "user" or "assistant".
  - `content` (Text): The message body.
  - `created_at` (DateTime): Timestamp.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can successfully add a task via chat in under 5 seconds (including typing and processing).
- **SC-002**: The system correctly identifies "add task" intent for 95% of clear natural language commands (e.g., "Add X", "Remind me to X", "New task X").
- **SC-003**: Chat history loads within 500ms when opening the chat window.
- **SC-004**: UI task list updates immediately (optimistically or <200ms after API response) after a chat-based task creation.