---
id: 001
title: Establish Phase II Constitution
stage: constitution
date: 2026-01-06
surface: agent
model: gemini
feature: none
branch: main
user: km
command: /sp.constitution
labels: ["setup", "governance", "phase-ii"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests: []
---

## Prompt

/sp.constitution  You are building a Phase II Full-Stack Todo Web App.
MANDATORY:- Read .spec-kit/config.yaml- Read specs/overview.mdRules:- Frontend: Next.js 16+, App Router, TypeScript, Tailwind, fully responsive.- Backend: FastAPI + Neon PostgreSQL. 
- Auth: Better Auth with JWT (multi-user).- RESTful APIs (GET, POST, PUT, DELETE, PATCH).- Login/signup required before tasks.- Theme: white, black, light purple, light cyan/sky blue.- Use cartoon-style illustrations matching todo theme.- Clean, readable, reusable code.- DATABASE_URL already exists in .env → use as-is, no placeholders.- Phase II only (do not mention Phase I).Follow Spec-Kit folder structure strictly.

## Response snapshot

Updated constitution to v1.0.0 reflecting Phase II requirements (Next.js 16+, FastAPI, Better Auth, Thematic Design).

## Outcome

- ✅ Impact: Constitution established.
- 🧪 Tests: N/A
- 📁 Files: 1 file updated.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Initial setup complete.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
