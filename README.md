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

## Project documentation

- [Project architecture and component diagram](PROJECT_ARCHITECTURE.md)
- [Domain request and job approval flows](docs/PROCESS_FLOW.md)
- [Project-specific interview questions and answers](INTERVIEW_QA.md)

## Readiness upgrade

See [implemented improvements and local run instructions](docs/UPGRADES.md). The domain API adds validated inputs and explanatory outputs; ops approval is idempotent and container examples run without root. Interactive API documentation is available at `/docs`.

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```
