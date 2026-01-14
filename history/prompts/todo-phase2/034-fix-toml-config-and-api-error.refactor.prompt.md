---
id: 034
title: fix-toml-config-and-api-error
stage: refactor
date: 2026-01-11
surface: agent
model: gemini
feature: todo-phase2
branch: 001-todo-phase2
user: km
command: /sp.implement
labels: ["config", "refactor", "python"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .gemini/commands/sp.reverse-engineer.toml
  - backend/src/api/errors.py
  - backend/src/main.py
tests:
  - []
---

## Prompt

/sp.implement - Do **NOT** write Python code in `.gemini/commands/*.toml` files.- Keep `.toml` files **config/text only**.- Move all backend logic to proper Python files (e.g. `src/api/errors.py`).- Implement `APIError` for consistent API error handling.- Remove Python blocks from `sp.reverse-engineer.toml`.- Ensure Gemini CLI runs without TOML parse errors.

## Response snapshot

Cleaned up `sp.reverse-engineer.toml` by removing embedded Python code blocks from the prompt string. Implemented `APIError` class in `backend/src/api/errors.py` and registered a global exception handler for it in `backend/src/main.py`.

## Outcome

- ✅ Impact: Fixed TOML configuration safety and standardized API error handling.
- 🧪 Tests: Manual verification of code changes.
- 📁 Files: Modified 2 files, created 1 file.
- 🔁 Next prompts: Verify backend startup.
- 🧠 Reflection: Handled user override of implementation task.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
