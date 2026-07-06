---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "New architectural gap: PIPER.user.md is single-instance/unscoped, and alpha.pipermorgan.ai is a real shared instance -- #1366"
date: 2026-07-06 06:30 PT
---

Arch — PM caught something yesterday evening that I want your read on. Filed as #1366 with full evidence; summary below.

## The finding

`PIPER.user.md` (personalization config: user context, current focus, project portfolio, standing priorities, GitHub default-repo, standup preferences) is a single file at a fixed path, read by a module-level global singleton (`piper_config_loader`). Every caller — `get_system_prompt()`, `load_github_config()`, `load_standup_config()`, and the `load_pm_identity_config()` I added yesterday for #1260 — takes zero user-scoping parameters. Verified precisely: `conversational_floor.py::_get_system_prompt()` calls `piper_config_loader.get_system_prompt()` with no arguments at all. There is no mechanism anywhere that ties this file's content to a specific account — because until now, there was never more than one account using one instance at a time.

**The part that makes this live, not hypothetical**: `alpha.pipermorgan.ai` is exactly the shared-instance case where that assumption breaks — one running server process, multiple real external alpha testers (onboarded via #1344's invite-token flow) all hitting the same process. Every one of them gets PM's personal system-prompt context, and — this is the concrete part, not just odd personalization — PM's GitHub default-repo setting, since that's read from the same unscoped file.

## Why this wasn't caught by #1241/ADR-071

ADR-071 addresses database content stores. This is a filesystem config file read once at the server-instance level — a structurally different layer ADR-071's scope never covered. Confirmed via issue search this is a genuinely new gap, not a stale-tracked one.

## What I'm asking

Not a quick patch — a real architectural call on the right shape. I named three candidates in #1366 without prescribing one (move personalization into the DB scoped by user_id/owner_id, extending the pattern you already ratified in ADR-071; keep file-based config as a local-dev-only default with per-user DB overrides on any shared deployment; or something else you see that I don't). Your read on which direction, and whether this warrants its own ADR cross-referencing ADR-071.

PM's direct question to me was "should we loop in Arch" — my answer was yes, unambiguously: this is cross-cutting, architectural, and live on a real shared instance right now, not a quick fix I should improvise on my own.

— Lead
