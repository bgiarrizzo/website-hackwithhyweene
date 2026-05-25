---
title: "Hyweene Static Site Generator — Setup guide"
filename: "SETUP.md"
description: "Installation, configuration, and run guide from a fresh clone."
creation_date: 2026-04-27
update_date: 2026-05-26
category: engineering
author: Bruno Giarrizzo
status: active
---

# Hyweene Static Site Generator — Setup guide

> Get from a fresh clone to a running CLI in under 10 minutes.

---

## Table of contents

1. [Requirements](#1-requirements)
2. [Quick start](#2-quick-start)
3. [Project details](#3-project-details)
4. [Running from the command line](#4-running-from-the-command-line)
5. [Running tests](#5-running-tests)
6. [Environment & secrets](#6-environment--secrets)
7. [CI parity tips](#7-ci-parity-tips)
8. [Troubleshooting](#8-troubleshooting)
9. [Project conventions](#9-project-conventions)
10. [To be confirmed](#10-to-be-confirmed)

---

## 1. Requirements

| Tool | Minimum version | Notes |
|---|---|---|
| macOS | 15 | Primary development platform configured in SwiftPM |
| Swift | 6.0 | Required by `Package.swift` |
| mise | latest stable | Optional but recommended for repeatable tasks |

If `mise` is not installed, project commands can still be run directly with `swift`.

---

## 2. Quick start

```bash
# 1. Clone
git clone https://github.com/bgiarrizzo/website-hyweene.git
cd website-hyweene

# 2. Install optional task tooling
mise run install

# 3. Build
swift build
```

To run with task aliases from repository root:

```bash
mise run build
mise run dev
```

---

## 3. Project details

| Setting | Value |
|---|---|
| Project root | `website-hyweene/` |
| Swift package file | `Package.swift` |
| Main executable target | `hyweene` |
| Main library target | `HyweeneSiteGenerator` |
| Test target | `HyweeneSiteGeneratorTests` |
| Deployment target | macOS 15 |
| Swift version | 6.0 |
| Code signing style | Not applicable (CLI package) |

### Build configurations

| Configuration | Usage |
|---|---|
| `debug` | Local development and iterative testing |
| `release` | Optimized local/CI build |

---

## 4. Running from the command line

### Build only

```bash
swift build
```

### Build for release

```bash
swift build -c release
```

### Run CLI locally

```bash
./.build/debug/hyweene build
./.build/debug/hyweene dev --host 0.0.0.0 --port 1234
./.build/debug/hyweene quick-add-link https://example.com --comment "Great read"
./.build/debug/hyweene check-dead-links --path ../current
```

### Run with SwiftPM

```bash
swift run hyweene build
swift run hyweene dev
```

---

## 5. Running tests

### From the command line

```bash
swift test
```

### What is tested

| Target | Framework | Coverage |
|---|---|---|
| `HyweeneSiteGeneratorTests` | Swift Testing / XCTest compatibility | Domain models, use cases, repositories, parsers, runtime command boundaries |

---

## 6. Environment & secrets

### How configuration works

Configuration is environment-variable driven with defaults defined in code.

### Required secrets

- None for standard local generation.

### Security notes

- Do not commit private tokens or credentials.
- Keep local overrides outside committed files.

---

## 7. CI parity tips

- Run commands from repository root via `mise` or from `src/` via `swift` consistently.
- Run commands from repository root consistently (where `Package.swift` is located).
- Use `swift build -c release` in CI for production-like compilation.
- Keep `swift test` mandatory on pull requests.

---

## 8. Troubleshooting

- If build fails after dependency updates, run `swift package resolve`.
- If generated output looks stale, run a fresh `hyweene build` and verify `current/` target content.
- If dev mode does not reload, confirm changes happen under `content/` or `src/Templates/`.
- If you see `Template named ... does not exist` with `generator/Templates`, update `SITE_TEMPLATE_PATH` or unset it to use `src/Templates`.

---

## 9. Project conventions

- Keep CLI output deterministic.
- Use layered boundaries described in `docs/ARCHITECTURE.md`.
- Add or update documentation in `docs/` for every behavior change.

---

## 10. To be confirmed

- Exact CI baseline image/toolchain pinning strategy.
- Structured logging rollout details and Sentry integration bootstrap sequence.
