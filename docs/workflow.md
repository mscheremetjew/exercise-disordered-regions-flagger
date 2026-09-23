# AI-Assisted Workflow

This project uses a controlled, approval-gated SDLC workflow.

## Canonical Workflow Status

Use `sdlc_docs/trace_workflow.md` as the single source of truth for stage status, blockers, evidence, and next action.

## Stage Artifacts

- `sdlc_docs/00_inception/`: request clarification and project context.
- `sdlc_docs/01_requirements/`: approved product requirements.
- `sdlc_docs/02_architecture/`: architecture baseline, diagrams, and ADRs.
- `sdlc_docs/03_implementation/`: implementation priority and execution tracking.

## Skill Sequence

Bundled Agent Skills are stored in `__AGENT_SKILLS_PATH__/`.

The workflow progresses through these skills in order:

1. `a-clarify-project-request`
2. `b-form-project-context`
3. `c-manage-product-requirements`
4. `d-design-product-architecture`
5. `e-sync-repository-requirements`
6. `f-establish-technical-foundation`
7. `g-implement-repository-work`
8. `i-validate-user-story-completion`
9. `h-create-implementation-pull-request`
10. `j-prepare-release-deployment`

The controller `sdlc-orchestrate-workflow` can be used to inspect status and route to the correct next stage.

## Approval Requirement

AI outputs are drafts until a human reviewer records approval at the required gate for each stage.
