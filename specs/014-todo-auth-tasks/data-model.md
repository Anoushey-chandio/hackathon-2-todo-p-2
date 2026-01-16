# Data Model: Full-Stack Todo App

## Entities

### User

Represents a registered user of the application.

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | UUID | Yes | Yes | Primary Key |
| email | String | Yes | Yes | User's email address (login credential) |
| password_hash | String | Yes | No | Bcrypt hashed password |
| created_at | DateTime | Yes | No | Timestamp of registration |
| updated_at | DateTime | Yes | No | Timestamp of last profile update |

**Relationships**:
- One-to-Many with **Task** (User has many Tasks)

### Task

Represents a single to-do item.

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | UUID | Yes | Yes | Primary Key |
| title | String | Yes | No | Short summary of the task |
| description | String | No | No | Detailed information |
| is_complete | Boolean | Yes | No | Completion status (default: false) |
| owner_id | UUID | Yes | No | Foreign Key to User.id |
| created_at | DateTime | Yes | No | Timestamp of creation |
| updated_at | DateTime | Yes | No | Timestamp of last update |

**Relationships**:
- Many-to-One with **User** (Task belongs to one User)
