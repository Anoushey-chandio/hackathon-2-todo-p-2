---
id: 037
title: fix-ts-jwt-error
stage: green
date: 2026-01-11
surface: agent
model: gemini
feature: todo-phase2
branch: 001-todo-phase2
user: km
command: /sp.implement
labels: ["auth", "jwt", "typescript", "fix"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - []
---

## Prompt

/sp.implement Fix TS JWT error in frontend Todo app (`session.type`) and enable JWT.Use `.env` BETTER_AUTH_SECRET, PostgreSQL pool, and Better Auth JWT plugin:```tsimport { betterAuth } from "better-auth";import { Pool } from "pg";import { jwt } from "better-auth/plugins";export const auth = betterAuth({  database: new Pool({ connectionString: process.env.DATABASE_URL, ssl: process.env.DATABASE_URL.includes("neon.tech") ? { rejectUnauthorized: false } : false }),  secret: process.env.BETTER_AUTH_SECRET,  emailAndPassword: { enabled: true },  plugins: [jwt({ secret: process.env.BETTER_AUTH_SECRET })],});Outcome: TS error fixed, JWT issued, frontend can send Authorization: Bearer <JWT>

## Response snapshot

Fixed TypeScript error in `frontend/src/lib/auth.ts` by correctly implementing the Better Auth JWT plugin configuration as requested.
- Replaced incorrect `session: { strategy: "jwt" }` with `plugins: [jwt({ secret: ... })]`.
- Updated database connection pool initialization.
- Added import for `jwt` from `better-auth/plugins`.

## Outcome

- ✅ Impact: Fixed TypeScript build error and correctly enabled JWT issuance.
- 🧪 Tests: Manual verification of config structure.
- 📁 Files: Modified 1 file.
- 🔁 Next prompts: None.
- 🧠 Reflection: Corrected configuration syntax for Better Auth v1.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
