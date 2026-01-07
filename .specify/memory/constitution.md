<!--
Sync Impact Report:
- Version Change: v0.0.0 -> v1.0.0 (Initial Phase II Constitution)
- Modified Principles:
  - Added Principle 1: Modern Tech Stack & Architecture
  - Added Principle 2: Secure Multi-User Access
  - Added Principle 3: Thematic & Responsive Design
  - Added Principle 4: Code Quality & Reusability
  - Added Principle 5: Database Integrity & Configuration
- Templates Checked:
  - .specify/templates/plan-template.md (✅ Compatible)
  - .specify/templates/spec-template.md (✅ Compatible)
  - .specify/templates/tasks-template.md (✅ Compatible)
-->
# Phase II Full-Stack Todo Web App Constitution

## Core Principles

### I. Modern Tech Stack & Architecture
Implementation must strictly use Next.js 16+ (App Router, TypeScript, Tailwind) for the frontend and FastAPI with Neon PostgreSQL for the backend. No legacy HTML/CSS/JS patterns are permitted. RESTful API design is mandatory for all backend services.

### II. Secure Multi-User Access
Security is paramount. Better Auth with JWT (JSON Web Tokens) must be used for authentication. Login/Signup is a hard gate before accessing any task management features. Data isolation per user is non-negotiable; users must only access their own data.

### III. Thematic & Responsive Design
UI/UX must utilize the specified palette (White, Black, Light Purple, Light Cyan/Sky Blue) and cartoon-style illustrations matching the todo theme. The application must be fully responsive across mobile, tablet, and desktop devices.

### IV. Code Quality & Reusability
Code must be clean, readable, and reusable. Follow Clean Architecture principles. Do not repeat code; create reusable components and utilities where appropriate. Adherence to Spec-Driven Development (SDD) is required.

### V. Database Integrity & Configuration
Use the existing `DATABASE_URL` from `.env`. Do not introduce placeholders or hardcoded credentials. Database interactions must be robust, secure, and use standard migration practices.

## Technical Constraints

Implementation is restricted to Phase II requirements only; do not include or reference Phase I code or UI artifacts unless explicitly migrated. Follow the Spec-Kit folder structure strictly. All features must be fully specified before implementation.

## Development Standards

All changes must be testable and verified. Adhere to the defined project structure: `specs/` for documentation, `src/` (or equivalent per Next.js/FastAPI conventions) for code. Commits must follow the project's commit message convention.

## Governance

Amendments to this constitution require a formal review and version increment. All Pull Requests must verify compliance with these principles. Complexity in implementation must be justified against these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06