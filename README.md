# disordered regions flagger

A Python project developed with an AI-assisted, approval-gated SDLC workflow.

## Development approach

This repository follows an AI-assisted, documentation-driven software development lifecycle. AI may support analysis, planning, implementation, testing, and documentation, but designated artifacts require human approval before work proceeds to the next stage.

Start with:

1. `sdlc_docs/trace_workflow.md` to see workflow status and next action.
2. `sdlc_docs/00_inception/sources/` to store original project request evidence.
3. `sdlc_docs/00_inception/project_context.md` after request clarification and approval.

Consult `WORKFLOW.md` for the complete staged sequence and skill ownership.

The AI SDLC Agent Skills are installed under:

```text
.agents/skills/

OR

.claude/skills/
```

They are maintained separately in:

```text
https://github.com/ecarrenolozano/ai-sdlc-skills
```

## Setup

```bash
uv sync --all-groups
uv run pre-commit install
```

## Quality checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

## Documentation

```bash
uv run mkdocs serve
```

## Project metadata

- **Type:** library
- **Python:** 3.14+
- **Agent skills:** `.agents/skills/`
- **Author:** Maxim <schereme@mpi-cbg.de>
- **License:** https://creativecommons.org/licenses/by/4.0/

## Acknowledgements

This exercise was developed with the support of the Max Planck Institute of Molecular Cell Biology and Genetics (MPI-CBG) in Dresden, Germany.
Thank you to my PI Prof. Agnes Toth-Petroczy for her continuous support.

The project setup and AI-assisted SDLC workflow was developed by Edwin Carreño (https://github.com/ecarrenolozano).
I would also like to thank you my colleague Ksenia Kuznetsova for her valued feedback and support in the development of this project.
