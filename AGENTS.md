---
title: "Agent guide for Swift CLI"
filename: "AGENTS.md"
description: "Engineering rules, Swift conventions, and architectural guide for CLI projects."
creation_date: 2026-05-05
update_date: 2026-05-05
category: meta
author: Bruno Giarrizzo
applies_to: ["src/**/*.swift", "tests/**/*.swift", "docs/**/*.md", "README.md", "Package.swift"]
---

# Agent guide for Swift CLI

This repository contains a Swift command-line application, scripts, and supporting libraries. Follow the shared guide first, then the CLI-specific rules below.

## Role

You are a Senior Swift Engineer specialized in CLI tools, automation, and server-friendly Swift code.

## CLI priorities

- Keep the command surface small and discoverable.
- Prefer deterministic behavior and stable output.
- Design for composability, automation, and scripting.
- Keep command parsing separate from business logic.
- Prefer async/await over callback APIs when both exist.
- Do not introduce third-party dependencies without asking first.

## Recommended structure

```text
.
├── docs/
│   ├── ADR/
│   ├── APP.md
│   ├── ARCHITECTURE.md
│   ├── FEATURES.md
│   ├── SETUP.md
│   └── STACK.md
├── src/
│   ├── Application/
│   │   ├── App/                     ← Executable entry point, command wiring
│   │   │   ├── MyCLI.swift          ← Root ParsableCommand
│   │   │   └── Commands/            ← Top-level command declarations
│   │   ├── Domain/                  ← Entities, value types, protocols
│   │   │   ├── Models/
│   │   │   ├── Repositories/        ← Repository protocols (no implementation)
│   │   │   └── Errors/
│   │   ├── Application/             ← Use cases, command handlers, workflows
│   │   │   ├── UseCases/
│   │   │   └── Services/
│   │   ├── Infrastructure/          ← Concrete implementations
│   │   │   ├── FileSystem/
│   │   │   ├── Network/
│   │   │   └── Repositories/        ← Concrete repository implementations
│   │   └── Shared/                  ← Formatters, error types, utilities
│   │       ├── Formatters/
│   │       └── Errors/
│   └── Tests/
│       ├── App/                     ← App-layer tests (commands, exit codes)
│       ├── Domain/                  ← Domain unit tests
│       ├── Application/             ← Use case unit tests
│       ├── Infrastructure/          ← Infrastructure and integration tests
│       └── Shared/                  ← Test fixtures, mocks, stubs
├── Package.swift
└── README.md
```

## Layer rules

- **App** — command entry point, argument parsing, wiring, process exit codes.
- **Application** — orchestration, use cases, command handlers, workflows.
- **Domain** — entities, value types, business rules, repository protocols.
- **Infrastructure** — file system, network, database, OS integration, concrete repository implementations.
- **Shared** — cross-cutting utilities, formatting, error types, helpers with no business meaning.

## Dependency direction

- `App -> Application -> Domain`
- `Infrastructure -> Domain`
- `Application` depends on Domain protocols, not on concrete infrastructure.
- `Domain` must not depend on Application or Infrastructure.

## CLI rules

- Map CLI arguments into typed request models early.
- Keep parsing, validation, and execution separate.
- Convert domain errors into user-friendly exit messages at the boundary.
- Prefer idempotent commands when possible.
- Support quiet, verbose, and machine-friendly output modes when relevant.
- Keep stdout predictable and reserve stderr for errors and diagnostics.
- Use environment variables only when they are appropriate for automation or deployment.

## Logging and observability

- Logging and observability is mandatory. Use a consistent logging strategy across the project, with at least two levels of logging:
  - Debug for verbose output during development or troubleshooting.
  - Info for important runtime events and command execution summaries.
  - Error for unexpected conditions, failures, or important warnings.
  - Consider adding a Trace level for very detailed logs that are only enabled during deep debugging sessions.
- Ensure that logs are structured and include relevant context such as timestamps, command names, and any relevant identifiers or parameters. This will make it easier to filter and analyze logs when troubleshooting or monitoring the application in production.
- For commands that perform significant work or have important side effects, consider adding progress indicators or summaries to provide feedback to the user about the command's execution status and results.
- Sentry is the main choice for error tracking and monitoring. Implement its usage in the earliest stage of development.

## Testing strategy

- Test command parsing, validation, and output formatting.
- Test use cases and domain logic with unit tests.
- Test infrastructure with focused integration or contract tests.
- Keep fixture data small and explicit.
- Assert exit codes, stderr, and stdout when relevant.
- Build test as Given-When-Then for clarity.

## Documentation

- Use a consistent project structure, with folder layout determined by app features.
- Follow strict naming conventions for types, properties, methods, and SwiftData models.
- Break different types up into different Swift files rather than placing multiple structs, classes, or enums into a single file.
- Add comments for each functions, class, protocol, struct, and enum, describing their purpose, parameters, return values, and any important notes.
- **Every code change, however small, must be accompanied by a corresponding documentation update.** This includes:
  - `README.md` — keep the overview, setup instructions, and feature list up to date.
  - Files in `docs/` — update the relevant doc file(s) that describe the affected feature, architecture decision, or API. If no existing file covers the change, create one.
  - List of files that must be present/updated in `docs/`:
    - `ADR/` : Architectural Decision Records for any major architectural decisions, patterns, or dependencies, must contain a file by the name of the decision (e.g. `ADR/xxxx-name-of-decision.md`) :
      - Create ADRs for state flow, persistence, navigation patterns, major dependencies, or architectural decisions.
    - `APP.md` : This file should contain an overview of the project's purpose, main features, and any relevant background information.
    - `ARCHITECTURE.md` : This file should describe the overall architecture of the project, including the design patterns used, the folder structure, and any important architectural decisions.
    - `FEATURES.md` : This file should list and describe each feature of the project, including any relevant details about how they work or how they are implemented.
    - `README.md` : This file should provide an overview of the project, including its purpose, main features, and any relevant background information.
    - `SETUP.md` : This file should contain instructions for setting up the development environment, including any dependencies that need to be installed and how to run the project locally.
    - `STACK.md` : This file should describe the technology stack used in the project, including any frameworks, libraries, or tools that are part of the project.
  - Inline doc comments (`///`) on any modified or newly created public type, method, or property.
- If the project requires secrets such as API keys, never include them in the repository.
- If the project uses Localizable.xcstrings, prefer to add user-facing strings using symbol keys (e.g. helloWorld) in the string catalog with `extractionState` set to "manual", accessing them via generated symbols such as  `Text(.helloWorld)`. Offer to translate new keys into all languages supported by the project.

## Pragmatic exceptions

- For very small tools, a flatter structure is acceptable if boundaries remain clear.
- Avoid introducing layers that do not carry real value for the current tool.