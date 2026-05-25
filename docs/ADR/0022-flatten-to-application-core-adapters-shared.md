---
title: "ADR 0022 — Flatten to Application / Core / Adapters / Shared"
filename: "0022-flatten-to-application-core-adapters-shared.md"
description: "Simplify the source tree from a deeply nested four-layer model to a flat Application / Core / Adapters / Shared layout."
creation_date: 2026-05-26
update_date: 2026-05-26
category: architecture
author: Bruno Giarrizzo
status: Accepted
---

# ADR 0022 — Flatten to Application / Core / Adapters / Shared

## Status

Accepted

## Context

The previous layout nested all library sources under `src/Application/` and used four sub-layers:

```text
src/Application/
├── App/                  ← CLI entry point
├── Application/          ← Services + UseCases (double-nested)
│   ├── Services/
│   └── UseCases/
├── Domain/               ← Models + repository protocols
│   ├── Models/
│   └── Repositories/
├── Infrastructure/       ← Concrete adapters
│   ├── DTOs/
│   ├── Mappers/
│   ├── FileSystem/
│   ├── Network/
│   ├── Parsers/
│   ├── Repositories/
│   └── Templates/
└── Shared/               ← Cross-cutting utilities
```

This produced two friction points:

1. **Double nesting** — `Application/Application/Services/` and `Application/Application/UseCases/` made paths confusing and did not add any boundary value.
2. **Misaligned naming** — `Domain` and `Infrastructure` are heavy DDD terms for a pragmatic CLI tool. The AGENTS.md guidance names these layers `Core` and `Adapters`, which better signals their role.

## Decision

Restructure the source tree to the AGENTS.md canonical model:

```text
src/
├── Application/          ← App + Services + UseCases
│   ├── App/
│   ├── Services/
│   └── UseCases/
├── Core/                 ← Models, protocol contracts, errors
│   ├── Models/
│   ├── Protocols/
│   └── Errors/
├── Adapters/             ← Concrete IO implementations
│   ├── FileSystem/
│   ├── Network/
│   ├── Parsers/
│   │   ├── DTOs/
│   │   └── Mappers/
│   └── Templates/
└── Shared/               ← Cross-cutting utilities
```

Package.swift is updated to set `path: "src"` for the library target with `sources: ["Application", "Core", "Adapters", "Shared"]`, replacing the old `path: "src/Application"`. No Swift module or import changes are required since all files remain in the same SPM target.

Test folders mirror the source layout: `Tests/Domain/` becomes `Tests/Core/`, `Tests/Infrastructure/` becomes `Tests/Adapters/`.

## Rationale

- Removes the meaningless `Application/Application/` double nesting.
- Aligns layer names with AGENTS.md guidance (`Core`, `Adapters`).
- DTOs and Mappers are co-located under `Adapters/Parsers/` because they form a single parsing chain (parse → DTO → mapper → entity).
- Repository protocol files move to `Core/Protocols/` to make the contract-vs-implementation boundary explicit.
- `Shared/` is promoted to the `src/` root, making it visually independent from any single layer.
- No new dependencies are introduced. No behaviour changes.

## Consequences

- All existing tests continue to pass (236 tests, 45 suites).
- Source paths in documentation and ADR index must reference the new layout.
- Future files must be placed in the appropriate new layer (`Core/`, `Adapters/`, etc.) rather than the old `Domain/` or `Infrastructure/` paths.
