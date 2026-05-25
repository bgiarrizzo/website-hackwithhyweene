---
title: "Hyweene Static Site Generator — Architecture"
filename: "ARCHITECTURE.md"
description: "Architecture overview, layer model, folder layout, and dependency rules."
creation_date: 2026-04-27
update_date: 2026-05-26
category: architecture
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Architecture

## Overview

The project is a Swift package rooted at `Package.swift`, with library sources under `src/Code/`, templates under `src/Templates/`, and tests under `src/Tests/`.

The architecture follows a CLI-oriented layered model aligned with AGENTS guidance.

```text
App -> Application -> Core
Adapters -> Core
Shared is cross-cutting and reused by all layers when appropriate.
```

All layers are present and actively used.

CLI command organization:

- Root command is defined in `src/Code/Application/App/CLIApp.swift`.
- Each subcommand is defined in its own file under `src/Code/Application/App/Commands/`.

## Canonical folder layout

```text
src/
├── Code/
│   ├── Application/
│   │   ├── App/
│   │   │   ├── CLIApp.swift
│   │   │   ├── command.swift          ← executable entry point
│   │   │   └── Commands/
│   │   ├── Services/
│   │   └── UseCases/
│   ├── Core/
│   │   ├── Models/
│   │   ├── Protocols/
│   │   └── Errors/
│   ├── Adapters/
│   │   ├── FileSystem/
│   │   ├── Network/
│   │   ├── Parsers/
│   │   │   ├── DTOs/
│   │   │   └── Mappers/
│   │   └── Templates/
│   └── Shared/
├── Templates/
└── Tests/
    ├── App/
    ├── Application/
    │   ├── Services/
    │   └── UseCases/
    ├── Core/
    │   └── Models/
    ├── Adapters/
    │   ├── FileSystem/
    │   ├── Parsers/
    │   │   ├── DTOs/
    │   │   └── Mappers/
    │   └── Templates/
    └── Shared/
```

## Layer rules

| Layer | Responsibility | Must not |
|---|---|---|
| **App** | CLI parsing, command wiring, boundary error mapping | Embed business rules or persistence details |
| **Application** | Orchestration, workflows, service coordination | Depend directly on adapter concrete types when protocol abstraction exists |
| **Core** | Domain entities/results and repository protocol contracts | Depend on Application or Adapters |
| **Adapters** | Filesystem/network/parsing/template concrete implementations | Contain command parsing or presentation logic |
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
│         Services / Use cases / Orchestration│
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                   Core                      │
│      Models, Protocols, Errors              │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                 Adapters                    │
│   FileSystem, Network, Parsers, Templates   │
└─────────────────────────────────────────────┘

Shared: cross-cutting utilities (all layers may use)
```

## Dependency injection

Dependencies are primarily injected by initializer wiring at runtime boundary.

```swift
// Production: CLI runtime creates concrete adapters and passes them to services/use cases.

// Testing: tests provide in-memory or fake implementations of repository protocols.
// For concurrent use cases, mutable test doubles must protect shared state (for example with NSLock).
```

Repository protocols live in `src/Code/Core/Protocols`; concrete implementations live in `src/Code/Adapters/FileSystem` and `src/Code/Adapters/Templates`.

## Testing strategy

| Type | Strategy |
|---|---|
| **Core** | Unit test entities/results and business invariants |
| **Use Case / Service** | Unit test execution paths with deterministic fixtures |
| **App** | Command parsing and boundary behavior tests |
| **Adapters** | Focused integration/contract tests for concrete implementations |
| **End-to-end build flow** | Build runtime tests for release behavior where relevant |

```text
src/Tests/
├── App/
├── Application/
│   ├── Services/
│   └── UseCases/
├── Core/
│   └── Models/
├── Adapters/
│   ├── FileSystem/
│   ├── Parsers/
│   │   ├── DTOs/
│   │   └── Mappers/
│   └── Templates/
└── Shared/
```

## Core

### Models

Core models represent blog posts, links, static pages, learn modules/pages, and resume aggregates with typed result objects for generation outcomes.

### Protocols

Repository protocols define the contracts for content loading (`ContentRepository`, `LearnContentRepository`, `LinkContentRepository`, `PageContentRepository`, `ResumeContentRepository`), file writing (`FileRepository`), and template rendering (`TemplateRepository`).

### Use cases

Use cases expose focused generation operations (`GenerateBlogUseCase`, `GenerateLinksUseCase`, `GeneratePagesUseCase`, `GenerateLearnUseCase`, `GenerateHomepageUseCase`, `GenerateResumeUseCase`) plus `BuildSiteUseCase` orchestration. They live in `Application/UseCases/`.

### Rules

- Build outputs must remain deterministic for identical inputs.
- Core owns business shape and validation boundaries.
- Repository contracts in Core/Protocols shield use cases from concrete IO details.

## Presentation

### View / screen structure

Not applicable: CLI-first project without graphical presentation layer.

### View model responsibilities

Not applicable.

### Shared UI components

Not applicable.

## Data / infrastructure

### Repositories

Filesystem-backed repositories (`Adapters/FileSystem/`) load Markdown/YAML content, then parse via DTOs and Mappers (`Adapters/Parsers/`) to produce Core entities. The template adapter (`Adapters/Templates/`) renders Stencil templates.

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

- App may depend on Application and Core.
- Application depends on Core contracts.
- Core remains independent of App and Adapters.
- Adapters depend on Core contracts/entities, not the opposite.
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

- Add explicit error-type organization under `src/Code/Core/Errors` and shared cross-cutting error helpers where needed.
- Finalize structured logging implementation details and Sentry integration points.
