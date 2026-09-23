# SDLC Documentation

This directory contains the authoritative project artifacts for the controlled SDLC workflow.

The workflow is stage-based and approval-gated. Downstream stages must use the latest approved upstream artifacts.

## Stage Sequence

1. `00_inception/` -> clarify request and establish project context.
2. `01_requirements/` -> define approved product requirements and user stories.
3. `02_architecture/` -> establish architecture baseline, diagrams, and ADRs.
4. `03_implementation/` -> manage implementation priority, code-level design, and execution status.
5. `trace_workflow.md` -> canonical status tracker across all stages.

## Skill Ownership

- `a-clarify-project-request`: `00_inception/clarified_project_request.md`
- `b-form-project-context`: `00_inception/project_context.md`
- `c-manage-product-requirements`: `01_requirements/product_requirements.md`
- `d-design-product-architecture`: architecture baseline under `02_architecture/`
- `e-sync-repository-requirements`: repository requirement synchronization (trace updates and issue alignment)
- `f-establish-technical-foundation`: technical foundation status and repository scaffolding
- `g-implement-repository-work`: implementation status and `03_implementation/backlog_priority.md`
- `i-validate-user-story-completion`: validation status and `tests/validation/` assets
- `h-create-implementation-pull-request`: pull request readiness and creation
- `j-prepare-release-deployment`: release/deployment readiness and evidence

## Template Scope

This cookiecutter template provides structural SDLC artifacts only. Product-specific requirements, architecture baselines, backlog entries, test scenarios, and release details are created during workflow execution.
