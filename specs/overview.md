# Todo App – Phase 2 Overview

This project is a simple web-based Todo application with user authentication.

## Core Features
- User Sign Up (email & password)
- User Login
- Authentication using FastAPI & JWT
- All data stored in PostgreSQL database (Neon)
- add, update,view, delete tasks
- Mark tasks as complete/incomplete
- Each user can access only their own tasks

## Access Rules
- Tasks page must NOT open without login
- Unauthorized users are redirected to login page

## UI Requirements
- Welcome page after login with text:
  "The easiest way to manage your tasks"
- Use soft illustration-style images related to productivity & todo tasks
- Theme colors:
  - White
  - Black
  - Light Purple
  - Light Sky Blue (Cyan)
- Same theme across login, signup, and task pages
- Fully responsive for mobile, tablet, and desktop

## Technical Notes
- Backend: FastAPI (RESTful API)
- Authentication: JWT
- Database: PostgreSQL (Neon)
- Frontend: Simple HTML, CSS, JavaScript
