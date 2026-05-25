---
title: "Hyweene Static Site Generator — Application overview"
filename: "APP.md"
description: "Product scope, user-facing behavior, and operational rules for the hyweene CLI static site generator."
creation_date: 2026-04-27
update_date: 2026-05-26
category: product
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Application overview

## Product

### What is Hyweene Static Site Generator?

Hyweene Static Site Generator is a CLI-first Swift application that generates hyweene.fr from Markdown and YAML content using Stencil templates.

It is designed for deterministic automation workflows with timestamped releases.

### Primary goal

> Generate a complete static website safely and repeatedly, while always keeping a valid published version available.

### Scope

- Generate all major sections: blog, links, pages, learning, resume.
- Publish output into timestamped releases with a stable current target.
- Support local development mode with watch and local serving.
- Provide automation-oriented helper commands for content maintenance and dead-link checking.
- Out of scope: CMS UI, multi-user authoring, runtime database-backed rendering.

### User roles

- Site owner
- Content editor (CLI-based)
- Maintainer/CI operator

## Experience

### Core flow

1. User updates content and templates.
2. User runs build or dev command.
3. Generator produces section outputs and shared artifacts.
4. Release is published and current site pointer is updated.

### Key screens or entry points

- `hyweene build`
- `hyweene dev --host <host> --port <port>`
- `hyweene quick-add-link <url> [--comment <text>]`
- `hyweene check-dead-links [--path <dir>]`

### Rules and behavior

- Output generation is section-based and deterministic.
- Releases are written to timestamped directories under `releases/`.
- Publication updates `current` atomically when possible.
- In dev mode, failed rebuilds do not replace the last valid served release.

## Accounts

### Account model

- No accounts
- No authentication flow
- Local CLI usage only

### Sign in and sign up

- Not applicable for this project.

### User data

- Repository content files (Markdown/YAML)
- Generated static files under release directories
- Optional environment-driven configuration

### Account lifecycle

- Not applicable for this project.

## Monetization

### Business model

- Internal/personal tooling
- No billing or subscription model

### Access rules

- Full feature set available locally and in CI.

### Purchases

- Not applicable.

### Billing notes

- Not applicable.

## Data and privacy

| Topic | Details |
|---|---|
| Data collected | Site source content in repository files and generated static output artifacts. |
| Data usage | Build static pages, feeds, and sitemaps. |
| Storage | Local filesystem in repository and release folders. |
| Sharing | No automatic third-party sharing by default. |
| Tracking | No analytics/tracking built into generator runtime by default. |
| Permissions | Filesystem read/write and optional local network bind in dev mode. |
| Purpose strings / disclosures | Not applicable for CLI context. |

## Security

### Security model

- Local CLI tooling, optionally executed in CI.
- Trust boundary is the local machine/CI runner and repository content.

### Sensitive data

- Environment variables may include deployment-related values.
- Secrets are not required for core generation flow and must not be committed.

### Transport and storage

- Local file storage for generated output.
- Optional outbound HTTP(S) fetch in `quick-add-link` for page title extraction.

### Threat considerations

- Validate and sanitize parsed content metadata.
- Keep deterministic build rules to reduce unexpected output drift.
- Treat remote HTML as untrusted input.

## Platform support

### Supported platforms

| Platform | Minimum version |
|---|---|
| macOS | 15 |

### Platform-specific behavior

- CLI-focused workflow only.
- Dev server defaults to host `0.0.0.0` and port `8000`.

## Technical design

### Architecture

- CLI-first layered architecture.
- Current layered structure: App, Application, Core, Adapters, Shared under `src/Code/`.
- Pragmatic architecture keeps parsing, orchestration, and IO separated while preserving deterministic output compatibility.

### Core dependencies

- Swift Argument Parser
- Ink
- Yams
- Stencil

### API and backend

- No dedicated backend service.
- Optional HTTP(S) reads for `quick-add-link`.

### Persistence

- Filesystem-based content ingestion and static output generation.
- Timestamp-based release versioning strategy.

## Operations

### Logging and analytics

- Runtime currently focused on deterministic command output.
- Structured logging strategy is mandatory per project rules and should be expanded consistently.

### Error handling

- Command failures keep non-destructive behavior for active release serving in dev mode.
- Errors are surfaced at CLI boundary.

### Testing

- Unit tests on core entities/results and use-case logic.
- Repository and parsing tests for adapter behavior.
- Command/runtime tests for CLI boundaries.

## Constraints

- Deterministic output and stable publication behavior are non-negotiable.
- Architecture changes must preserve compatibility of generated site artifacts.
