---
title: "Hyweene Static Site Generator — Features"
filename: "FEATURES.md"
description: "Complete list of features, their scope, behavior rules, and current status."
creation_date: 2026-04-27
update_date: 2026-05-26
category: product
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Features

## Overview

This document defines the functional scope of the CLI generator used to build hyweene.fr. It is organized as feature entries with status, rules, and verifiable acceptance criteria.

## Feature index

| # | Feature | Status |
|---|---|---|
| F-01 | Full static content generation | `done` |
| F-02 | Deterministic release publication | `done` |
| F-03 | Development mode with watch and local server | `done` |
| F-04 | Quick link capture command | `done` |
| F-05 | Dead external link check | `done` |
| F-06 | Parallel build execution | `done` |
| F-07 | Layered architecture simplification and hardening | `done` |
| F-08 | Structured observability and Sentry rollout | `planned` |
| F-09 | YAML-driven global navigation menu | `done` |

---

## F-01 — Full static content generation

**Status:** `done`  
**Area:** `Content`

### Description

Generate all website sections from repository content sources and templates: blog, links, pages, learning, and resume.

### User stories

- As a maintainer, I can generate all sections in one command so that publication is consistent.
- As a content editor, I can add Markdown/YAML content so that pages are rebuilt automatically.

### Behavior rules

- Build includes section pages and shared artifacts such as feeds and sitemaps.
- Inputs come from content folders and templates configured by environment variables.
- Generation failure must fail the command and prevent partial publication.

### Acceptance criteria

- [x] A single build command generates all supported sections.
- [x] Blog and links outputs include RSS and sitemap entries.
- [x] Missing or invalid input causes explicit command failure.

### Out of scope

- Runtime CMS editing UI.
- Dynamic server-side rendering.

### Notes

Section generators are now orchestrators over use cases to keep output behavior stable while refactoring.

---

## F-02 — Deterministic release publication

**Status:** `done`  
**Area:** `Publication`

### Description

Publish each successful build into a timestamped release directory, then expose the active version through a stable current target.

### User stories

- As an operator, I can publish a new release atomically so that end users avoid half-built content.

### Behavior rules

- Each build writes to a new release path.
- Current target is switched only after successful generation.
- Old releases are cleaned after publication according to project policy.

### Acceptance criteria

- [x] Successful build creates a timestamped release folder.
- [x] Current target points to the latest valid release.
- [x] Cleanup of previous releases happens after successful publish.

### Out of scope

- Blue/green deployment across remote infrastructure.

### Notes

This is a core reliability contract and must remain stable during architecture refactors.

---

## F-03 — Development mode with watch and local server

**Status:** `done`  
**Area:** `CLI`

### Description

Provide a development command that runs an initial build, serves generated output locally, and triggers rebuilds when source files change.

### User stories

- As a maintainer, I can preview local changes quickly so that editing loops are short.

### Behavior rules

- `dev` runs an initial build before serving.
- File watcher monitors project content/template inputs.
- Failed rebuild keeps serving the latest valid release.

### Acceptance criteria

- [x] `hyweene dev` starts local serving after initial build.
- [x] Content or template changes trigger rebuild attempts.
- [x] Last valid release remains served when a rebuild fails.

### Out of scope

- Hot module replacement.
- Distributed multi-user development serving.

### Notes

Default server settings are host `0.0.0.0` and port `8000`.

---

## F-04 — Quick link capture command

**Status:** `done`  
**Area:** `CLI`

### Description

Create a link content file from a URL by fetching the remote title and optionally attaching a comment.

### User stories

- As a content editor, I can create a links entry from a URL so that I save manual metadata typing time.

### Behavior rules

- Command supports interactive and non-interactive comment modes.
- Generated file is stored in the links content path.
- Remote metadata fetch errors are surfaced clearly.

### Acceptance criteria

- [x] URL-only mode generates a link file with remote title.
- [x] `--comment` mode stores the provided comment.
- [x] Command failure is explicit when URL fetch fails.

### Out of scope

- Rich metadata scraping beyond title extraction.

### Notes

Designed for automation and fast curation workflows.

---

## F-05 — Dead external link check

**Status:** `done`  
**Area:** `Quality`

### Description

Scan generated HTML files and report external links returning HTTP 404.

### User stories

- As a maintainer, I can detect broken outbound links so that published content quality remains high.

### Behavior rules

- Command scans recursively from the configured output path.
- Only external links are validated.
- Results are emitted in machine-friendly output.

### Acceptance criteria

- [x] Command scans all generated HTML files under target path.
- [x] 404 links are listed in output.
- [x] Non-404 links are not flagged as dead.

### Out of scope

- Full SEO auditing.
- Internal route consistency analysis.

### Notes

Primary command: `hyweene check-dead-links --path ./current`.

---

## F-06 — Parallel build execution

**Status:** `done`  
**Area:** `Performance`

### Description

Use controlled parallelism for independent generation workloads to reduce total build time.

### User stories

- As an operator, I can run builds faster so that CI and local feedback loops improve.

### Behavior rules

- Independent sections can run concurrently.
- Item-level rendering (posts/links/pages/modules) can run in parallel.
- Failure in one branch must stop the global build path safely.

### Acceptance criteria

- [x] Independent generators execute in parallel.
- [x] Item-level rendering uses controlled concurrent execution.
- [x] First hard failure aborts build and prevents publication switch.

### Out of scope

- Distributed build execution over remote workers.

### Notes

Concurrency remains bounded and deterministic at command level.

---

## F-07 — Layered architecture simplification and hardening

**Status:** `done`  
**Area:** `Architecture`

### Description

Complete and stabilize migration from legacy nested layout to the flatter App/Application/Core/Adapters/Shared boundaries.

### User stories

- As a maintainer, I can evolve implementation safely so that behavior remains stable and testable.

### Behavior rules

- Core owns models/results and repository contracts.
- Adapters provide concrete implementations only.
- App and Application layers remain orchestration boundaries.

### Acceptance criteria

- [x] Core generation use cases exist and are used by orchestration adapters.
- [x] Tests are organized by layer.
- [x] Source tree is flattened under `src/Code/` with `Application`, `Core`, `Adapters`, and `Shared` folders.

### Out of scope

- Rewriting the entire codebase in one disruptive step.

### Notes

Migration policy is incremental to preserve output compatibility.

---

## F-08 — Structured observability and Sentry rollout

**Status:** `planned`  
**Area:** `Operations`

### Description

Introduce structured logs with consistent levels and context, plus Sentry integration for runtime failure monitoring.

### User stories

- As an operator, I can diagnose failures quickly so that recovery time is reduced.

### Behavior rules

- Logs include command name, timestamps, and contextual identifiers.
- Error events are reportable to Sentry at command boundaries.
- Sensitive data must never be logged or sent.

### Acceptance criteria

- [ ] Debug/info/error levels are consistently implemented.
- [ ] Sentry can be enabled in configured environments.
- [ ] Failure summaries include actionable context.

### Out of scope

- Full APM stack with distributed traces across unrelated systems.

### Notes

This feature must follow project security and privacy constraints.

---

## F-09 — YAML-driven global navigation menu

**Status:** `done`
**Area:** `Content`

### Description

Load website navigation entries from a dedicated YAML file and expose them to all templates through global rendering context.

### User stories

- As a maintainer, I can update menu entries in one YAML file so that every generated page uses the same navigation.

### Behavior rules

- Navigation source of truth is `content/nav-menu.yml`.
- Menu items are ordered exactly as listed in YAML.
- Menu schema is strict: each item must define non-empty `name` and `url` strings.
- Missing file, invalid YAML, or invalid schema must fail generation explicitly.

### Acceptance criteria

- [x] Main template renders navigation via loop over `menu` context data.
- [x] Menu entries come from YAML, not hardcoded template links.
- [x] Invalid navigation YAML causes explicit build failure.

### Out of scope

- Active-link highlighting based on current page.
- Nested/hierarchical menus.

### Notes

Navigation path is configurable through `SITE_NAV_MENU_PATH`.

---

## Cross-cutting concerns

- **Error states:** Commands fail fast with explicit diagnostic output; publication state remains safe when applicable.
- **Empty states:** Generators handle empty content sets by producing valid list/index outputs where supported.
- **Loading states:** CLI progress is command-driven and can be enriched with structured summaries.
- **Offline behavior:** Core generation is offline-capable; only remote title fetch and link checks require network.
- **Accessibility:** Not a UI app; accessibility concerns apply to generated HTML semantics and content quality.
- **Localization:** Primary locale is French (`fr-FR`) with locale-driven formatting support via configuration.

## Dependencies between features

| Feature | Depends on | Notes |
|---|---|---|
| F-02 | F-01 | Publication is meaningful only after full generation output exists. |
| F-03 | F-01, F-02 | Dev mode requires build and reliable publication behavior. |
| F-04 | F-01 | Link creation feeds the links generation pipeline. |
| F-05 | F-01, F-02 | Link checks target generated output, usually current release. |
| F-06 | F-01 | Parallelism is applied to generation workloads. |
| F-07 | F-01, F-06 | Migration preserves generation and concurrency contracts. |
| F-08 | F-07 | Observability rollout should target stabilized layered boundaries. |
| F-09 | F-01 | Navigation is rendered as part of standard template-based generation. |

## Out of scope (product level)

- Browser-based CMS and editorial interface.
- Multi-tenant authoring and role-based access control.
- Runtime dynamic rendering with persistent backend database.
- Payment, subscription, or account management workflows.

## Open questions

- Should release-retention policy become configurable beyond current cleanup behavior?
- What is the exact Sentry bootstrap and environment matrix for local/dev/CI/prod?
