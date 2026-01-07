# Feature Specification: Phase II Todo App with Auth

**Feature Branch**: `001-todo-phase2`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Implement Phase II Todo App with Auth (Next.js, FastAPI, Better Auth, JWT, CRUD, Themed UI)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure User Onboarding & Access (Priority: P1)

Users must be able to create an account and log in securely to access their private task list. This is the foundation for the entire application.

**Why this priority**: Essential for identifying users and isolating their data. Without auth, the multi-user requirement cannot be met.

**Independent Test**: Can be tested by signing up a new user, verifying successful login, and confirming the JWT token is issued.

**Acceptance Scenarios**:

1. **Given** a visitor on the Signup page, **When** they enter a valid email and password, **Then** a new account is created, and they are redirected to the Login page.
2. **Given** a registered user on the Login page, **When** they enter correct credentials, **Then** they receive a JWT, are redirected to the Welcome page, and the "The easiest way to manage your tasks" text is visible.
3. **Given** an unauthenticated visitor, **When** they attempt to access `/tasks`, **Then** they are redirected to the Login page.

---

### User Story 2 - Task Management (CRUD) (Priority: P1)

Authenticated users need to manage their daily tasks. This includes adding new tasks, viewing their list, updating details, marking as complete, and deleting unwanted tasks.

**Why this priority**: Core value proposition of the application.

**Independent Test**: Can be tested by a logged-in user performing all CRUD operations and verifying the list state updates accordingly.

**Acceptance Scenarios**:

1. **Given** a logged-in user on the Tasks page, **When** they submit a new task title and description, **Then** the task appears in their list immediately.
2. **Given** a task in the list, **When** the user clicks "Edit" and changes the title, **Then** the task list reflects the updated title.
3. **Given** an incomplete task, **When** the user marks it as "Complete", **Then** the task status updates visually and persists.
4. **Given** a task, **When** the user deletes it, **Then** it is removed from the list permanently.
5. **Given** two different users, **When** User A views their tasks, **Then** they see ONLY their own tasks and NOT User B's tasks.

---

### User Story 3 - Themed & Responsive Experience (Priority: P2)

Users should experience a visually consistent, cartoon-themed interface that works seamlessly across devices.

**Why this priority**: Ensures the app meets the specific aesthetic and usability requirements defined for Phase II.

**Independent Test**: Can be tested by resizing the browser window to mobile/tablet widths and verifying layout adjustments and theme color compliance.

**Acceptance Scenarios**:

1. **Given** any page (Login, Signup, Tasks), **When** viewed on a mobile device, **Then** the layout adjusts to fit the screen without horizontal scrolling.
2. **Given** the Welcome page, **When** loaded, **Then** it displays the required cartoon-style illustration and theme colors (White, Black, Light Purple, Light Cyan).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use Better Auth with JWT for user authentication.
- **FR-002**: System MUST protect the `/tasks` route and all `/api/{user_id}/tasks` endpoints; only the owner of the `user_id` can access them.
- **FR-003**: System MUST expose a REST API `GET /api/{user_id}/tasks` to retrieve the authenticated user's tasks.
- **FR-004**: System MUST expose a REST API `POST /api/{user_id}/tasks` to create a new task.
- **FR-005**: System MUST expose a REST API `GET /api/{user_id}/tasks/{id}` to retrieve a specific task.
- **FR-006**: System MUST expose a REST API `PUT /api/{user_id}/tasks/{id}` to update a task's full details.
- **FR-007**: System MUST expose a REST API `DELETE /api/{user_id}/tasks/{id}` to remove a task.
- **FR-008**: System MUST expose a REST API `PATCH /api/{user_id}/tasks/{id}/complete` to toggle task completion status.
- **FR-009**: System MUST persist data using the `DATABASE_URL` defined in `.env`.
- **FR-010**: Frontend MUST include Signup, Login, Welcome, and Tasks pages.
- **FR-011**: UI MUST use the specific color palette: White, Black, Light Purple, Light Cyan/Sky Blue.

### Key Entities

- **User**: Represents a registered account.
  - Attributes: ID (unique), Email (unique), Password (hashed), CreatedAt.
- **Task**: Represents a todo item.
  - Attributes: ID (unique), UserID (foreign key), Title, Description, IsCompleted (boolean), CreatedAt, UpdatedAt.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can complete the Signup flow and land on the Login page in under 2 minutes.
- **SC-002**: System responds to Task creation requests within 500ms (p95).
- **SC-003**: 100% of unauthorized access attempts to user data are rejected (e.g., return 401/403).
- **SC-004**: Application layout passes visual inspection for "broken" elements on Mobile (375px), Tablet (768px), and Desktop (1024px+) viewports.
- **SC-005**: User data persistence is verified by retrieving the same data after a system restart or session refresh.

### Edge Cases

- **EC-001**: User tries to access `/tasks` with an expired JWT token -> Should redirect to Login.
- **EC-002**: User tries to access `/api/{other_user_id}/tasks` -> Should return 403 Forbidden.
- **EC-003**: User tries to create a task with an empty title -> Should show validation error.
- **EC-004**: Database connection is lost -> Frontend should display a friendly "Service Unavailable" message.