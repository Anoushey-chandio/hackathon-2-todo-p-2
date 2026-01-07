# Data Model: Phase II Todo App

## Entities

### User
Represents a registered user of the system.

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | Integer (PK) | Yes | Yes | Auto-incrementing primary key |
| email | String | Yes | Yes | User's email address |
| hashed_password | String | Yes | No | Bcrypt hashed password |
| created_at | DateTime | Yes | No | Timestamp of registration |

### Task
Represents a todo item belonging to a user.

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| id | Integer (PK) | Yes | Yes | Auto-incrementing primary key |
| user_id | Integer (FK) | Yes | No | Foreign key to User.id |
| title | String | Yes | No | Short title of the task |
| description | String | No | No | Optional details |
| is_completed | Boolean | Yes | No | Defaults to False |
| created_at | DateTime | Yes | No | Creation timestamp |
| updated_at | DateTime | Yes | No | Last update timestamp |

## Relationships

- **User** has many **Tasks** (1:N)
- **Task** belongs to one **User** (N:1)
- Deleting a User should cascade delete their Tasks.

## Database
- **Engine**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy (Async)
