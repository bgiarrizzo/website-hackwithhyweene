---
title: "Hyweene Static Site Generator — Architecture"
filename: "ARCHITECTURE.md"
description: "Architecture overview, layer model, folder layout, and dependency rules."
creation_date: 2026-04-27
update_date: 2026-05-24
category: architecture
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Architecture

## Overview

The project is a Swift package under `src/` with a library target for generator logic and an executable target for CLI entry.

The architecture follows a CLI-oriented layered model aligned with AGENTS guidance.

```text
App -> Application -> Domain
Infrastructure -> Domain
Shared is cross-cutting and reused by all layers when appropriate.
```

All layers are present and actively used.

CLI command organization:

- Root command is defined in `src/Application/App/CLIApp.swift`.
- Each subcommand is defined in its own file under `src/Application/App/Commands/`.

## Canonical folder layout

```text
src/
├── Sources/
│   ├── hyweene/
│   │   └── command.swift
│   └── HyweeneSiteGenerator/
│       ├── App/
│       ├── Application/
│       │   ├── UseCases/
│       │   └── Services/
│       ├── Domain/
│       │   ├── Models/
│       │   └── Repositories/
│       ├── Infrastructure/
│       │   ├── DTOs/
│       │   ├── Mappers/
│       │   ├── Repositories/
│       │   ├── FileSystem/
│       │   ├── Network/
│       │   ├── Parsers/
│       │   └── Templates/
│       └── Shared/
└── Tests/
    └── HyweeneSiteGeneratorTests/
        ├── App/
        ├── Application/
        ├── Domain/
        ├── Infrastructure/
        └── Shared/
```

## Layer rules

| Layer | Responsibility | Must not |
|---|---|---|
| **App** | CLI parsing, command wiring, boundary error mapping | Embed business rules or persistence details |
| **Application** | Orchestration, workflows, service coordination | Depend directly on infrastructure concrete types when protocol abstraction exists |
| **Domain** | Core entities/results and repository contracts | Depend on Application or Infrastructure |
| **Infrastructure** | Filesystem/network/parsing/template concrete adapters | Contain command parsing or presentation logic |
| **Shared** | Reusable configuration and utilities | Become a hidden business-logic layer |

## Layer diagram

```text
┌─────────────────────────────────────────────┐
│                    App                      │
│           CLI commands and wiring           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                Application                  │
│         Use cases and orchestration         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                  Domain                     │
│      Models/entities and repository APIs    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              Infrastructure                 │
│   Repositories, parsers, templates, IO      │
└─────────────────────────────────────────────┘
```

## Dependency injection

Dependencies are primarily injected by initializer wiring at runtime boundary.

```swift
// Production: CLI runtime creates concrete adapters and passes them to services/use cases.

// Testing: tests provide in-memory or fake implementations of repository protocols.
```

Repository protocols live in `Domain/Repositories`; concrete implementations live in `Infrastructure/Repositories`.

## Testing strategy

| Type | Strategy |
|---|---|
| **Domain** | Unit test entities/results and business invariants |
| **Use Case / Service** | Unit test execution paths with deterministic fixtures |
| **App** | Command parsing and boundary behavior tests |
| **Infrastructure** | Focused integration/contract tests for adapters |
| **End-to-end build flow** | Build runtime tests for release behavior where relevant |

```text
src/Tests/HyweeneSiteGeneratorTests/
├── App/
├── Application/
├── Domain/
├── Infrastructure/
└── Shared/
```

## Domain

### Entities

Domain models represent blog, links, pages, learn modules/pages, and resume aggregates with typed result objects for generation outcomes.

### Use cases

Use cases expose focused generation operations (`GenerateBlogUseCase`, `GenerateLinksUseCase`, `GeneratePagesUseCase`, `GenerateLearnUseCase`, `GenerateHomepageUseCase`, `GenerateResumeUseCase`) plus `BuildSiteUseCase` orchestration.

### Rules

- Build outputs must remain deterministic for identical inputs.
- Domain layer owns business shape and validation boundaries.
- Repository contracts in Domain shield use cases from concrete IO details.

## Presentation

### View / screen structure

Not applicable: CLI-first project without graphical presentation layer.

### View model responsibilities

Not applicable.

### Shared UI components

Not applicable.

## Data / infrastructure

### Repositories

Filesystem-backed repositories load Markdown/YAML content and template files, then map DTOs to domain entities.

Template rendering also loads a global navigation menu from a dedicated YAML input and injects it into template context for all rendered pages.

### Network / backend

Local HTTP serving is used in dev mode. `quick-add-link` performs remote title extraction over HTTP(S).

### Persistence

Persistence is filesystem-based:

- Input from `content/`
- Navigation from `content/nav-menu.yml` (or `SITE_NAV_MENU_PATH` override)
- Template sources from `src/Templates/`
- Output to timestamped `releases/` with publication through `current`

Navigation loading is strict by design: missing file, invalid YAML, or invalid menu item structure fails generation explicitly.

## Backend / API

Not applicable: no server-side API module in this repository.

## Platform notes

### Supported platforms

| Platform | Minimum version |
|---|---|
| macOS | 15 |

### Platform-specific behavior

- CLI command set is the primary interface.
- Dev server and watcher are optimized for local iterative development.

## Dependency rules

- App may depend on Application and Domain.
- Application depends on Domain contracts.
- Domain remains independent of App and Infrastructure.
- Infrastructure depends on Domain contracts/entities, not the opposite.
- Shared utilities stay generic and non-domain-specific.

## Architecture decisions

- Layered CLI architecture with explicit boundary separation.
- Release publication model uses timestamped outputs and a stable current pointer.
- Migration policy is incremental to avoid output regressions.

See ADR entries in `docs/ADR/` for decision history.

## Constraints

- Deterministic and scriptable behavior is required.
- Output compatibility must be preserved during refactors.
- Repository is optimized for static generation, not dynamic rendering.

## Open questions

- Add explicit `Domain/Errors` and `Shared/Errors` packages as first-class boundaries.
- Finalize structured logging implementation details and Sentry integration points.
