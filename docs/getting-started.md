# Getting started

## 1. Install dependencies

```bash
uv sync --all-groups
uv run pre-commit install
```

## 2. Run quality checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

## 3. Start documentation locally

```bash
uv run mkdocs serve
```

## 4. Start the SDLC workflow

1. Open `sdlc_docs/trace_workflow.md` to identify the current stage and next action.
2. Begin in `sdlc_docs/00_inception/sources/` by storing the original request evidence.
3. Continue with the stage guidance in [AI-assisted workflow](workflow.md).

## 5. Repository workflow references

- Root workflow summary: `WORKFLOW.md`
- SDLC artifact overview: `sdlc_docs/README.md`
- Stage status tracker: `sdlc_docs/trace_workflow.md`
