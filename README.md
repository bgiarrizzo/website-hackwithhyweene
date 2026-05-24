# Hyweene Static Site Generator

Swift static site generator for hyweene.fr.

This repository follows the engineering directives in `AGENTS.md`. The file is normative and code/docs are aligned to it.

## CLI Commands

The `hyweene` binary exposes four explicit commands:

CLI parsing is handled by `swift-argument-parser` (typed subcommands and options).

```bash
hyweene build
hyweene dev
hyweene dev --host 0.0.0.0 --port 1234
hyweene quick-add-link https://example.com
hyweene quick-add-link https://example.com --comment "Great read"
hyweene check-dead-links --path ./current
```

Behavior:
- `build`: generates the site once, updates the `current` symlink, and cleans old releases.
- `dev`: runs an initial build, starts a local HTTP server, and automatically rebuilds when files change.
- `dev` defaults: host `0.0.0.0`, port `8000`.
- `quick-add-link`: fetches a page title from a URL and automatically creates a Markdown file in `content/text/links`.
    - interactive mode: prompts for a comment
    - non-interactive mode: `--comment "..."`
- `check-dead-links`: scans generated HTML files and lists external links returning 404 (JSON output).

## Features

- Parsing Markdown + frontmatter YAML
- Navigation menu loaded from YAML (`content/nav-menu.yml`)
- Templates Stencil
- Generation of blog, links, pages, resume, and learning sections
- RSS + sitemaps
- Parallel build:
    - independent generators in parallel
    - blog posts in parallel
    - links in parallel
    - learning modules/pages in parallel
    - static pages in parallel
- Development mode with file watching + local server

## Usage via mise

```bash
mise run install
mise run build
mise run dev
mise run test
```

## Direct Usage

```bash
swift build

# One-time build
./.build/debug/hyweene build

# Dev mode
./.build/debug/hyweene dev --host 0.0.0.0 --port 1234

# Quick-add a link
./.build/debug/hyweene quick-add-link https://example.com
./.build/debug/hyweene quick-add-link https://example.com --comment "Great read"

# Check dead links
./.build/debug/hyweene check-dead-links --path ./current
```

## Architecture Direction

- Runtime entry points remain in CLI commands.
- Business logic is being migrated toward Domain Use Cases and repository boundaries.
- Data access and rendering adapters remain isolated from Domain rules.
- Migration is incremental to keep generated output behavior stable.

Current migration status:
- `BlogGenerator` delegates to `GenerateBlogUseCase` (Domain + Data adapters).
- `LinksGenerator` delegates to `GenerateLinksUseCase` (Domain + Data adapters).
- `PagesGenerator` delegates to `GeneratePagesUseCase` (Domain + Data adapters).
- `LearnGenerator` delegates to `GenerateLearnUseCase` (Domain + Data adapters).
- `HomepageGenerator` delegates to `GenerateHomepageUseCase` and consumes Domain entities directly.
- `ResumeGenerator` delegates to `GenerateResumeUseCase` (Domain aggregate + Data repository).

## Tests

```bash
swift test
```

## Environment Variables

All configuration values can be overridden via environment variables. Unset variables fall back to their default values.

### URL Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `SITE_SCHEME` | Site protocol | `String` | `https` |
| `SITE_SHORT_URL` | Short site URL | `String` | `hyweene.fr` |
| `SITE_LONG_URL` | Full site URL | `String` | `www.hyweene.fr` |
| `SITE_BASE_URL` | Full base URL with scheme | `String` | `https://www.hyweene.fr` |

### Path Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `SITE_RELEASES_PATH` | Directory where versioned releases are stored | `String` | `releases` |
| `SITE_CURRENT_RELEASE_PATH` | Symlink (or copy) pointing to the active release | `String` | `current` |
| `SITE_CONTENT_PATH` | Content root directory | `String` | `content` |
| `SITE_NAV_MENU_PATH` | Navigation menu YAML file path | `String` | `content/nav-menu.yml` |
| `SITE_MEDIA_PATH` | Media assets directory | `String` | `content/media` |
| `SITE_STATIC_PATH` | Static files directory (CSS, JS, images) | `String` | `content/static` |
| `SITE_TEMPLATE_PATH` | Stencil templates directory | `String` | `src/Templates` |
| `SITE_TEXT_CONTENT_PATH` | Text content root directory | `String` | `content/text` |
| `SITE_BLOG_PATH` | Blog posts directory | `String` | `content/text/blog` |
| `SITE_LINKS_PATH` | Links directory | `String` | `content/text/links` |
| `SITE_PAGES_PATH` | Static pages directory | `String` | `content/text/pages` |
| `SITE_RESUME_PATH` | Resume data directory | `String` | `content/text/resume` |
| `SITE_LEARN_PATH` | Learning modules directory | `String` | `content/text/learn` |

### Author Information

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `SITE_AUTHOR_NAME` | Author short name | `String` | `Bruno Giarrizzo` |
| `SITE_AUTHOR_FULL` | Author full display name | `String` | `Bruno 'Hyweene' Giarrizzo` |
| `SITE_GITHUB_LINK` | Author GitHub profile URL | `String` | `https://github.com/bgiarrizzo/` |
| `SITE_LINKEDIN_LINK` | Author LinkedIn profile URL | `String` | `https://www.linkedin.com/in/bruno-giarrizzo/` |

### Site Metadata

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `SITE_DESCRIPTION` | Site meta description | `String` | `Linuxien, Developpeur Python, Swift et DevOps` |
| `SITE_KEYWORDS` | SEO keywords (comma-separated list) | `[String]` | `Bruno,Giarrizzo,Hyweene,...` |
| `SITE_LANGUAGE` | HTML `lang` attribute value | `String` | `fr-FR` |
| `SITE_LOCALE` | System locale for date/number formatting | `String` | `fr_FR.UTF-8` |

## Navigation Menu Configuration

The main navigation menu is loaded from YAML and injected globally in templates.

- Default file: `content/nav-menu.yml`
- Override path: `SITE_NAV_MENU_PATH`
- Schema:

```yaml
menu:
    - name: /blog
        url: /blog/
    - name: /about
        url: /about/
```

The menu loader is strict: missing file, invalid YAML, or invalid/missing `name` or `url`
fields fail the build explicitly.

## Compatibility

- Swift 6+
- macOS 15+

## Troubleshooting

- If template rendering fails with a path like `generator/Templates`, verify `SITE_TEMPLATE_PATH`.
- The runtime now falls back to `src/Templates` when `SITE_TEMPLATE_PATH` points to a missing legacy path.