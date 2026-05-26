---
title: "Agent guide for Swift CLI"
filename: "AGENTS.md"
description: "Engineering rules, Swift conventions, and pragmatic architecture guidance for CLI projects."
creation_date: 2026-05-05
update_date: 2026-05-25
category: meta
author: Bruno Giarrizzo
applies_to: ["src/**/*.swift", "src/Tests/**/*.swift", "docs/**/*.md", "README.md", "Package.swift"]
---

# Agent guide for Swift CLI

This repository contains a Swift command-line application and a supporting core library. Follow the shared guide first, then the CLI-specific rules below.

## Role

You are a Senior Swift Engineer specialized in CLI tools, automation, deterministic output, and maintainable SwiftPM-based code.

## CLI priorities

- Keep the command surface small and discoverable.
- Prefer deterministic behavior and stable output.
- Design for composability, automation, and scripting.
- Keep command parsing separate from business logic.
- Prefer async/await over callback APIs when both exist.
- Do not introduce third-party dependencies without asking first.
- Prefer the simplest architecture that preserves clarity, testability, and long-term maintainability.

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
│   ├── Code/
│   │   ├── Adapters/
│   │   │   ├── FileSystem/
│   │   │   ├── Network/
│   │   │   ├── Parsers/
│   │   │   └── Templates/
│   │   ├── Application/
│   │   │   ├── App/
│   │   │   │   ├── CLIApp.swift
│   │   │   │   └── Commands/
│   │   │   ├── Services/
│   │   │   └── UseCases/
│   │   ├── Core/
│   │   │   ├── Models/
│   │   │   ├── Errors/
│   │   │   ├── Protocols/
│   │   │   └── Helpers/
│   │   └── Shared/
│   │        ├── Config.swift
│   │        ├── DateFormat.swift
│   │        ├── FileManager+Extensions.swift
│   │        ├── Slugify.swift
│   │        └── String+Extensions.swift
│   ├── Templates/
│   └── Tests/
│       ├── App/
│       ├── Application/
│       ├── Core/
│       ├── Adapters/
│       └── Shared/
├── Package.swift
└── README.md
```

## Architectural model

Use this model as the default:

```text
CLI entry point -> Commands -> Services / Use Cases -> Core
Adapters -> Core
```

The executable target handles argument parsing, command wiring, and boundary error mapping.  
The core library contains reusable logic, models, rules, and protocol definitions.  
Adapters contain the concrete filesystem, network, parser, and template implementations.

## Layer rules

- **App** — command entry point, argument parsing, wiring, process exit codes.
- **Services / Use Cases** — orchestration, workflows, command execution, business operations.
- **Core** — models, value types, invariants, errors, and protocol definitions.
- **Adapters** — filesystem, network, parsing, templates, and other concrete implementations.
- **Shared** — cross-cutting utilities and extensions with no business meaning.

## Dependency direction

- `App -> Services / Use Cases -> Core`
- `Adapters -> Core`
- `Services / Use Cases` depend on `Core` protocols, not on concrete adapters.
- `Core` must not depend on `App` or `Adapters`.
- `Shared` must remain generic and must not become a hidden business layer.

## CLI rules

- Map CLI arguments into typed request models early.
- Keep parsing, validation, and execution separate.
- Convert domain errors into user-friendly exit messages at the boundary.
- Prefer idempotent commands when possible.
- Support quiet, verbose, and machine-friendly output modes when relevant.
- Keep stdout predictable and reserve stderr for errors and diagnostics.
- Use environment variables only when they are appropriate for automation or deployment.
- If a command starts becoming large, split it into smaller services or use cases rather than adding another architecture layer.

## Logging and observability

- Logging is mandatory.
- Use a consistent logging strategy across the project.
- Use at least:
  - Debug for troubleshooting and development.
  - Info for important runtime events and command summaries.
  - Error for failures and important warnings.
- Keep logs structured and include useful context such as command names and relevant identifiers.
- For significant commands, provide progress feedback or a final summary when it improves usability.
- Sentry is the main choice for error tracking and monitoring.

## Testing strategy

- Test command parsing, validation, and output formatting.
- Test services and core logic with unit tests.
- Test adapters with focused integration or contract tests.
- Keep fixture data small and explicit.
- Assert exit codes, stderr, and stdout when relevant.
- Prefer Given-When-Then style for clarity.
- Keep tests close to the behavior they validate.

## Documentation

- Keep the project structure consistent and easy to navigate.
- Use strict naming conventions for types, properties, methods, and files.
- Break different public types into different Swift files when it improves readability.
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
- Prefer fewer abstractions when the code is still evolving and the benefit of abstraction is not yet clear.
