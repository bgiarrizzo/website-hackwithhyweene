---
title: "Hyweene Static Site Generator — Tech stack"
filename: "STACK.md"
description: "Languages, frameworks, testing strategy, and deployment configuration."
creation_date: 2026-04-27
update_date: 2026-05-26
category: engineering
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Tech stack

## Language & version

| | |
|---|---|
| **Language** | Swift 6.0 |
| **Concurrency** | async/await + task-based parallel execution |
| **Strict concurrency** | Partially adopted; progressive hardening during migration |

## Frameworks

| Framework | Usage |
|---|---|
| **Foundation** | Core filesystem, date/time, parsing helpers |
| **FoundationNetworking** | URLSession/URLRequest compatibility when needed |
| **Network** | Local HTTP server implementation on Apple platforms |
| **Swift Argument Parser** | CLI parsing, subcommands, options |
| **Ink** | Markdown to HTML transformation |
| **Yams** | YAML/frontmatter parsing, including global navigation menu loading |
| **Stencil** | HTML and text template rendering |
| **Swift Testing / XCTest compatibility** | Unit and integration-style package tests |

Third-party dependencies are managed via Swift Package Manager.

## UI approach

- No graphical UI layer.
- CLI-first interaction model.
- Output is filesystem artifacts plus deterministic stdout/stderr command feedback.

## State management

```text
hyweene command entry point
	-> App command wiring
		-> Application services/use cases
			-> Core models/protocol contracts
				-> Adapters (filesystem, parser, templates, network)
```

State is short-lived and command-scoped; generated artifacts are persisted as release folders.

## Testing

| Framework | Usage |
|---|---|
| **Swift Testing / XCTest compatibility** | Core, use cases, adapters, runtime command boundaries |

Tests are split by layer under the package test tree:

- `src/Tests/Core/` — core models and rules.
- `src/Tests/Application/` — use-case and service orchestration.
- `src/Tests/Adapters/` — repositories, parsers, template engine, IO adapters.
- `src/Tests/App/` — CLI command-facing behavior.
- `src/Tests/Shared/` — shared utilities and configuration helpers.

## Target & deployment

| | |
|---|---|
| **Target** | CLI |
| **Minimum version** | macOS 15 |
| **Device** | N/A |
| **Orientation** | N/A |
| **Permissions** | Local filesystem read/write, optional local network bind in dev mode |
| **Entitlements** | None |
| **Network** | Optional, for dev server and quick-add-link title retrieval |
| **Persistence** | Local filesystem (content input + release output) |

## Architecture notes

- Layered CLI architecture: App, Application, Core, Adapters, Shared.
- Executable/library split in SwiftPM: lightweight CLI entry + testable core library.
- Current SwiftPM source layout uses `src/Code` for the library target and `src/Tests` for tests.

## Dependencies and services

- Monitoring and crash reporting: Sentry planned by project rules, rollout in progress.
- Analytics: none by default.
- Payments: none.
- Authentication provider: none.
- Backend/database: none required for core static generation.

## Build and release

- Build tools: Swift Package Manager and optional `mise` task runner.
- Distribution: CLI binary execution in local/dev/CI contexts.
- Publication model: generate timestamped release folders then point `current` to latest valid release.

## Constraints

- Deterministic output is required.
- Architecture boundaries must remain clear and enforce dependency direction.
- No unnecessary third-party dependencies without explicit approval.
