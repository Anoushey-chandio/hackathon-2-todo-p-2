---
description: "Task list for Phase II Todo App implementation"
---

# Tasks: Phase II Todo App with Auth

**Input**: Design documents from `/specs/001-todo-phase2/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Integration tests are included to verify critical flows (Auth, CRUD) as per standard best practices, even if not explicitly TDD-mandated.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Tests**: `backend/tests/`, `frontend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create monorepo structure with `backend/` and `frontend/` folders
- [x] T002 [P] Initialize FastAPI backend: `backend/pyproject.toml`, `backend/src/main.py`
- [x] T003 [P] Initialize Next.js frontend: `frontend/package.json`, `frontend/tsconfig.json`
- [x] T004 [P] Configure shared environment variables in root `.env` (DATABASE_URL)

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup Database Engine & Session with SQLModel in `backend/src/core/database.py`
- [x] T006 Setup SQLModel Base in `backend/src/models/base.py`
- [x] T007 Configure Alembic for migrations in `backend/alembic.ini` and `backend/migrations/env.py`
- [x] T008 [P] Implement Security Utils (Pwd Hashing) in `backend/src/core/security.py`
- [x] T009 [P] Implement JWT Token Utilities (create/verify) in `backend/src/core/security.py`
- [x] T010 Setup API Router structure in `backend/src/api/api.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure User Onboarding & Access (Priority: P1) 🎯 MVP

**Goal**: Users can sign up, log in, and receive a JWT. Protected routes reject unauthorized access.

**Independent Test**: Sign up a new user via API, get a token, and use it to access a protected endpoint.

### Implementation for User Story 1

- [x] T011 [US1] Create User SQLModel in `backend/src/models/user.py`
- [x] T012 [US1] Generate Alembic migration for User table (SQLModel) in `backend/migrations/versions/`
- [x] T013 [US1] Create User Schemas (Pydantic) in `backend/src/schemas/user.py`
- [x] T014 [US1] Implement Auth Routes (Signup/Login) in `backend/src/api/endpoints/auth.py`
- [x] T015 [US1] Implement `get_current_user` dependency in `backend/src/api/deps.py`
- [x] T016 [US1] Create Frontend Auth Pages (Login/Signup) in `frontend/src/app/(auth)/login/page.tsx` & `signup/page.tsx`
- [x] T017 [US1] Implement Frontend Auth Client (fetch wrapper) in `frontend/src/lib/api.ts`
- [x] T018 [US1] Create Welcome Page (Protected) in `frontend/src/app/page.tsx`
- [x] T019 [US1] Implement Auth Guard in `frontend/src/app/layout.tsx` for Route Protection (Replacing Middleware)
- [x] T019a [US1] Remove deprecated `frontend/src/middleware.ts`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (CRUD) (Priority: P1)

**Goal**: Authenticated users can Create, Read, Update, Delete tasks. Data is isolated per user.

**Independent Test**: Login as User A, create task. Login as User B, verify User A's task is NOT visible.

### Implementation for User Story 2

- [x] T020 [US2] Create Task SQLModel in `backend/src/models/task.py`
- [x] T021 [US2] Generate Alembic migration for Task table (SQLModel) in `backend/migrations/versions/`
- [x] T022 [US2] Create Task Schemas (Create, Update, Out) in `backend/src/schemas/task.py`
- [x] T023 [US2] Implement Task CRUD Endpoints in `backend/src/api/endpoints/tasks.py`
- [x] T024 [US2] Create Frontend Tasks Page in `frontend/src/app/(dashboard)/tasks/page.tsx`
- [x] T025 [US2] Implement Task List Component in `frontend/src/components/TaskList.tsx`
- [x] T026 [US2] Implement Add Task Form in `frontend/src/components/AddTaskForm.tsx`
- [x] T027 [US2] Integrate Task API calls in `frontend/src/lib/api_tasks.ts`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Themed & Responsive Experience (Priority: P2)

**Goal**: Consistent "Cartoon" theme and responsive layout across all pages.

**Independent Test**: Visual inspection on Mobile/Desktop.

### Implementation for User Story 3

- [x] T028 [US3] Configure Tailwind Theme (colors/fonts) in `frontend/tailwind.config.ts`
- [x] T029 [US3] Create Global Layout with Theme in `frontend/src/app/layout.tsx`
- [x] T030 [US3] Add Illustration Assets to `frontend/public/assets/`
- [x] T031 [US3] Style Login/Signup Pages with Theme in `frontend/src/app/(auth)/layout.tsx`
- [x] T032 [US3] Style Tasks Page with Responsive Grid in `frontend/src/app/(dashboard)/tasks/page.tsx`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 [P] Add error handling toast notifications in `frontend/src/components/ui/toast.tsx`
- [x] T034 [P] Verify API Security (CORS, Rate Limiting) in `backend/src/main.py`
- [x] T035 [P] Run final Quickstart verification
- [x] T036 [P] Update `README.md` with Phase II details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Story 1 (P1)**: Depends on Foundational
- **User Story 2 (P1)**: Depends on User Story 1 (Auth needed for Tasks)
- **User Story 3 (P2)**: Can run parallel to US2, but best after US1

### Parallel Opportunities

- T002 & T003 (Backend/Frontend Init)
- T008 & T009 (Security Utils)
- T016, T017, T018 (Frontend Pages - once API contract is set)
- T024, T025, T026 (Frontend Components)

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Setup + Foundational
2. Implement Auth (US1) -> Verify Login
3. Implement Tasks (US2) -> Verify CRUD
4. Apply Theme (US3) -> Polish UI
5. Final Validation

