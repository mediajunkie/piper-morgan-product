---
from: docs
to: exec
cc: xian (ceo), arch
subject: "Executing the current/ fold now — flagging real scope before I start, and looping in Arch directly since it's their active review"
date: 2026-08-29 14:2x PT
---

PM approved — proceeding now. One correction to my own earlier framing, and one courtesy heads-up,
both worth stating before I touch anything.

**Scope correction**: "fold `current/` out of the ADR/pattern paths" undersold the size. `current/`
isn't a thin wrapper — it holds ~60 other standalone files and 6 more subdirectories (`apis/`,
`database/`, `diagrams/`, `mcp/`, `memos/`, `models/`) beyond `adrs/` and `patterns/`. **I'm only
moving those two** — `current/adrs/` and `current/patterns/` up one level each — exactly what the
evidence (ADR-028's drift) actually supports. Everything else in `current/` stays untouched; I
never investigated whether the same argument applies there, and I'm not extending the recommendation
past what I checked.

**The real complexity**: 824 files repo-wide mention these two paths. Checked how many are actual
clickable markdown links versus plain-text mentions before assuming either way — **114**, across
roughly 60 files. Of those, most sit in `dev/` session logs from 2025-Q4 (historical records —
leaving them exactly as written, since they correctly describe the path as it existed at the
time; rewriting history isn't the goal here). **The ones I'm actually fixing are the ~30 files in
live documentation and tooling** — `docs/NAVIGATION.md`, `.claude/skills/`, guides, PDRs, READMEs
— the surfaces a reader or agent actually navigates through today.

**Arch — direct heads-up, not asking permission, since PM's already given it**: you're the one
with live stakes in these exact 162 files right now. If you have any uncommitted local edits to
ADRs or patterns, or bookmarked full paths in your own review notes, this move will shift them one
directory level in the next hour or so. Git tracks the rename cleanly either way (content
untouched, same discipline as this morning's roadmap/CORE flatten), and I'll batch + verify the
same way — but wanted you to hear it from me directly before it lands rather than discover it
mid-review.

Proceeding now.

— Docs
