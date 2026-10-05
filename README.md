# SQL Data Analyst Agent

Level: 8 — Beginner Agentic AI

Skills: Python, tool order, read-only SQL

Runs profile then aggregate on posted rows. Goals that say delete or drop are refused.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.
