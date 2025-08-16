# Cursor AI — Project Guardrails & Coding Contract

> Use these instructions for **all** code you generate or edit in this workspace.

---

## 0) Project Context (fill me in)
- **Project name:** {{PROJECT_NAME}}
- **Stack:** {{FRONTEND_FRAMEWORK}} + {{LANGUAGE}} + {{BACKEND}} + {{DB}} + {{VECTOR_DB}}
- **Styling:** {{UI_LIB}} (prefer Mantine if present, else Tailwind; otherwise stick to existing)
- **AI:** {{LLM_PROVIDER}} + {{OBSERVABILITY}} (e.g., LangChain, LangGraph, CrewAI, LangSmith)
- **Build target:** {{VERCEL|RENDER|DOCKER|OTHER}}

---

## 1) Inviolable Rules
- Match **existing stack, patterns, and folder structure**. Never switch libraries.
- **Do not remove** existing logic, conditionals, or safety checks unless explicitly asked.
- Code must run **clean**: no TypeScript errors, no ESLint errors, no unused imports/vars.
- Prefer **functional components** + hooks; no class components.
- **Beginner-friendly**: add clear comments and short docstrings; keep functions single-purpose.
- Keep PR-sized changes: **small, focused, and atomic**.

---

## 2) File Structure & Naming
- Components: `PascalCase.tsx`, hooks: `useThing.ts`, utils: `camelCase.ts`.
- Separate layers: `components/`, `hooks/`, `lib/` (clients, helpers), `services/` (API), `types/`, `store/`, `pages|app/`.
- Put config/constants in `config/` or `lib/constants.ts`. No magic strings.
- If you create files, **update all imports** and export from relevant `index.ts`.

---

## 3) GenAI & Multi-Agent UI/UX
- Always implement:
  - **Loading states** (skeleton/spinner) and **disabled** actions while fetching.
  - **Streaming** UI when backend supports it; append tokens progressively.
  - **Agent timeline** (steps, status, durations, errors) for orchestration visibility.
  - **Retry** and **cancel** controls.
  - **Copy** buttons for prompts and outputs.
- Errors: show user-friendly message + technical details in collapsible section.
- Long outputs: virtualize or paginate; allow **export** (txt/md/json).

---

## 4) State, Data, and Types
- Local state first; promote to global (`Zustand/Redux`) **only** when shared.
- Strong typing everywhere: props, API responses, DTOs. Create `types/*.ts`.
- API response shape:  
  ```ts
  { success: boolean; data?: T; error?: { code: string; message: string; details?: unknown } }
