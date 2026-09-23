# Architecture

This directory contains the product architecture baseline: architecture narrative, canonical Structurizr DSL model, per-container documentation, and Architecture Decision Records.

**Primary skill:** `d-design-product-architecture`

## Contents

- `architecture.md`: authoritative architecture narrative.
- `containers/`: one documentation folder per internal C4 container.
- `diagrams/workspace.dsl`: canonical C4 model.
- `diagrams/docker-compose.yml`: local Structurizr viewer.
- `diagrams/images/`: optional exported SVG or PNG diagrams.
- `adr/`: accepted and historical Architecture Decision Records.

The baseline always includes System Context and Container views. Component, Dynamic, and Deployment views are included only when they materially improve the architecture description.

## How To View This Architecture

These commands apply after `d-design-product-architecture` creates `diagrams/workspace.dsl` and `diagrams/docker-compose.yml`.

From the repository root, run:

```bash
docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml up
```

Then open `http://localhost:8080`.

Stop the local viewer with:

```bash
docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml down
```

Do not commit Structurizr runtime files from `diagrams/.structurizr/`. The directory must be excluded by `diagrams/.gitignore`.

Do not skip required approval gates.
