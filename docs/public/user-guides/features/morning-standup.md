# Morning Standup - User Guide

> **Note on `PM-NNN` references** (added 2026-08-13): IDs like PM-011/PM-124/PM-126 are the project's 2025-era internal ticket numbers, predating the move to GitHub Issues as the sole tracker. They're kept as historical references; where a GitHub mapping is known it's shown inline (e.g. PM-126 = GitHub #132). They are not links and have no current lookup surface.

**Last Updated**: October 31, 2026 (rewritten against the current code, issue #1779)

## Overview

Piper Morgan can generate a daily standup in three ways:

- **In chat or on the `/standup` page** (the hosted app): the standup is derived from your live data (conversations, documents, work items, calendar). If a source cannot be read, the standup says so instead of showing an empty day.
- **From the command line** (`cli/commands/standup.py`): a developer tool for a self-hosted install.
- **Through the REST API** (`/api/v1/standup`): for scripts and integrations.

This guide covers the command line and the REST API. The hosted app's standup needs no setup beyond connecting your sources in Settings.

## Command line

### Usage

```bash
# Generate a standup in the terminal
python cli/commands/standup.py

# Also print Slack-ready markdown
python cli/commands/standup.py --format slack

# Post to Slack, create GitHub issues from action items, update a Notion database
python cli/commands/standup.py --slack --github --notion
```

### Options

| Flag | Meaning |
|------|---------|
| `--format cli` | Terminal output (default) |
| `--format slack` | Terminal output plus a Slack-ready block |
| `--slack` | Post the standup to Slack |
| `--github` | Create GitHub issues from action items |
| `--notion` | Update a Notion database with the standup |

There is no `--with-issues` or `--without-issues` flag. Earlier versions of this guide described one. It was removed when the command moved to `StandupWorkflowSkill`. Issue-based standups now come from the REST API's `issues` and `trifecta` modes (below).

### What it prints

- **Yesterday's Accomplishments**, or "No specific accomplishments found".
- **Today's Priorities**.
- **Blockers**, or "No blockers identified". (The underlying data calls this slot Watch.)
- **Posted to**, listing each system you asked it to post to.
- A line with the generation time in milliseconds. The command aims for under 2 seconds.

If generation fails, the command prints the error and exits with status 1.

## REST API

`POST /api/v1/standup/generate` takes a JSON body:

```json
{ "mode": "trifecta", "format": "slack" }
```

- **mode**: `standard`, `issues` (GitHub issues), `documents`, `calendar`, or `trifecta` (all sources combined). Default `standard`.
- **format**: `json` (default), `slack`, `markdown`, or `text`.

Other routes under `/api/v1/standup`:

- `GET /today`: the on-demand standup derived from your live data, the same one the `/standup` page shows. It scopes to the signed-in user.
- `GET /modes` and `GET /formats`: the options above.
- `GET /health`: service health.

Authentication is on by default. Interactive API documentation is served at `/docs` on a running server.

## Troubleshooting

**The standup is empty or says a source could not be read.** That is the app reporting a failed read, not an empty day. Check the connection in Settings, Integrations, and use its Test button.

**The command line fails.** It prints the error and exits with status 1. Read the error first.

## Related

- [Integration Guide](integration-guide.md)
- Architecture: [Canonical Queries Architecture](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/canonical-queries-architecture.md)
- Development history: [Morning Standup MVP Guide](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/development/tools/MORNING_STANDUP_MVP_GUIDE.md)
