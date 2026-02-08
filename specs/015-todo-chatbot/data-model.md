# Data Model: Todo Chatbot

**Feature**: `015-todo-chatbot`

## New Entities

### Conversation
Represents a continuous dialogue thread for a user. For this MVP, we might only need one "active" conversation per user, or a list of them. We will support multiple.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key |
| `user_id` | UUID | Yes | Foreign Key to `User.id` |
| `title` | String | No | Auto-generated summary (optional) |
| `created_at` | DateTime | Yes | Creation timestamp |
| `updated_at` | DateTime | Yes | Last activity |

### Message
Individual messages within a conversation.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key |
| `conversation_id` | UUID | Yes | Foreign Key to `Conversation.id` |
| `role` | String | Yes | `user`, `assistant`, or `system` |
| `content` | Text | Yes | The message text |
| `created_at` | DateTime | Yes | Timestamp |

## Relationships

- `User` (1) -> (Many) `Conversation`
- `Conversation` (1) -> (Many) `Message`

## Database Changes (SQLModel)

We need to create a new file `backend/src/models/chat.py` and register it in `backend/src/models/__init__.py`.

```python
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    # ... fields
    
class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str
    content: str
    # ... fields
```
