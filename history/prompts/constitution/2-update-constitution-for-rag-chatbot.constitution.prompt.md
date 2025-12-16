---
id: 2
title: Update Constitution for RAG Chatbot
stage: constitution
date: 2025-12-16
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: Aeyla Naseer
command: /sp.constitution
labels: [constitution,documentation,rag,chatbot,docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project: RAG Chatbot for Existing Docusaurus Book

Core principles:
- Grounded answers strictly from book content
- Accuracy through source-based retrieval
- Clarity for technical students
- Reproducibility of ingestion and retrieval
- Backend-first engineering rigor

Rules:
- Zero hallucination tolerance
- No external knowledge beyond /docs
- Selected-text queries must use ONLY provided text
- Citations required in every response
- Production-ready async backend

Success criteria:
- Chatbot answers only from indexed Markdown
- Selected-text mode enforced correctly
- Backend integrates cleanly with existing Docusaurus site
```

## Response snapshot

Updated the project constitution to align with the RAG Chatbot for Existing Docusaurus Book requirements. Revised all core principles to reflect the new project focus: Grounded Answers, Retrieval Accuracy, Student Clarity, Reproducible Ingestion, and Backend Engineering Rigor. Updated Quality Standards and Development Workflow sections to emphasize zero hallucination tolerance, citation requirements, selected-text mode enforcement, and backend reliability. The constitution now properly governs the development of a RAG chatbot that operates exclusively on indexed documentation with strict adherence to source-based responses.

## Outcome

- ✅ Impact: Updated constitution to properly govern RAG chatbot development with focus on grounded responses
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with RAG chatbot-specific principles
- 🔁 Next prompts: Proceed with spec and plan development based on updated constitution
- 🧠 Reflection: Constitution now properly enforces zero hallucination policy and source-based retrieval requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All required principles incorporated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on updated constitution