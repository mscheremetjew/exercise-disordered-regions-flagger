# AI-Assisted SDLC Workflow

The repository uses the following staged workflow and skill ownership:

1. Project request clarification (`a-clarify-project-request`).
2. Project context formation (`b-form-project-context`).
3. Product requirements management (`c-manage-product-requirements`).
4. Product architecture design (`d-design-product-architecture`).
5. Repository requirements synchronization (`e-sync-repository-requirements`).
6. Technical foundation establishment (`f-establish-technical-foundation`).
7. Repository work implementation (`g-implement-repository-work`).
8. User story completion validation (`i-validate-user-story-completion`).
9. Implementation pull request creation (`h-create-implementation-pull-request`).
10. Release and deployment preparation (`j-prepare-release-deployment`).

Use `sdlc_docs/trace_workflow.md` as the canonical workflow status file. The orchestrator skill `sdlc-orchestrate-workflow` validates and routes execution based on this trace.

Core SDLC artifacts:

- `sdlc_docs/00_inception/`
- `sdlc_docs/01_requirements/`
- `sdlc_docs/02_architecture/`
- `sdlc_docs/03_implementation/`
- `sdlc_docs/trace_workflow.md`

## Approval rule

Do not treat AI-generated documentation, plans, code, tests, or validation results as approved by default. A human reviewer must record a decision in each required approval gate.
