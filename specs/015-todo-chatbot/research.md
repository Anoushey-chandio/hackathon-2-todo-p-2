# Research & Technical Decisions: Todo Chatbot Module

**Branch**: `015-todo-chatbot`
**Status**: Completed
**Date**: 2026-02-05

## Technical Context & Decisions

### 1. Frontend: "OpenAI ChatKit" vs Standard Chat UI
The spec explicitly requests "OpenAI ChatKit".
**Decision**: We will search for a library matching this description. If "OpenAI ChatKit" refers to the generic concept of a chat interface or a hallucinated library, we will implement a standard chat UI using **Vercel AI SDK** (standard for Next.js) or a custom React component, but styled to match the "ChatKit" expectation (likely meaning a clean, bubble-based interface).
*Correction/Refinement*: Given the user's specific request for "ChatKit", we will treat it as a requirement to look for. If nonexistent, we fallback to **Vercel AI SDK's `useChat`** which is the industry standard for Next.js + LLM chat, and often what users mean by "OpenAI Chat UI" in this context.
**Selected Approach**: Use **Vercel AI SDK (`ai/react`)** as the implementation of the "ChatKit" requirement, as it provides the `useChat` hook and UI helpers perfect for this stack.

### 2. Backend: "OpenAI Agents SDK"
The user requested "OpenAI Agents SDK". OpenAI recently released the **Assistants API** and frameworks like **LangChain** or **Semantic Kernel** often wrap "agents".
**Decision**: We will use the **OpenAI Python SDK (`openai>=1.0.0`)** which supports the Chat Completions API with **Function Calling** (Tools). This is the standard "agent" pattern for simple task automation (parsing intent -> calling function).
**Why**: True "Agents SDK" often refers to experimental frameworks. The robust, production-ready approach for "Add Task" intent is **Function Calling**.
**Implementation**: define `add_task` tool, pass to OpenRouter (which supports OpenAI-compatible function calling).

### 3. LLM: OpenRouter
**Constraint**: Use OpenRouter API key.
**Decision**: Configure the OpenAI client `base_url` to `https://openrouter.ai/api/v1` and use the key from `.env`.
**Model**: We will default to a cost-effective, capable model supported by OpenRouter (e.g., `openai/gpt-4o-mini` or `meta-llama/llama-3-8b-instruct`) for the implementation.

### 4. Data Persistence
**Constraint**: Store history in Neon DB.
**Schema**:
- `conversations`: user_id, created_at
- `messages`: conversation_id, role (user/assistant), content, created_at
**Flow**:
1. User POSTs message to FastAPI.
2. Backend saves User message.
3. Backend fetches recent history.
4. Backend calls LLM (Agent).
5. If Tool Call (Add Task):
   - Execute internal task logic.
   - Save "System/Tool" result (optional, or just Assistant confirmation).
6. Save Assistant response.
7. Return response stream or text.

## Action Items
- [x] Verify OpenRouter compatibility with Function Calling (Yes, most major models support it).
- [x] Confirm Vercel AI SDK compatibility with FastAPI (Yes, via stream data or standard REST).
