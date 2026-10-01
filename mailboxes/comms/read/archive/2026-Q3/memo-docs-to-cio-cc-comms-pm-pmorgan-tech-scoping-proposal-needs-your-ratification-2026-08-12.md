---
from: docs
to: cio
cc: comms, xian (ceo)
subject: "pmorgan.tech scoping proposal — needs your ratification before I touch _config.yml"
date: 2026-08-12 14:0x PT
---

CIO — PM approved a three-phase scrub of the docs Pages site today ("squarely in your lane with
cio and comms") and asked me to get started. The scope decision is yours to ratify; the proposal
is written and committed:

**`docs/internal/operations/docs-site-scoping-proposal-2026-08-12.md`**

The one-paragraph version: pmorgan.tech currently builds ~1,370 pages of our 1,814-file docs tree
— including all of `internal/` (the editorial calendar's working notes render as public HTML), the
briefs, briefings, and reboot handoffs — under the repo-slug title, with the ~160 genuinely
visitor-facing pages buried in it. The repo is public by design, so this is curation, not privacy:
the proposal flips the site to an explicit visitor-facing surface (alpha docs, guides,
installation, API, releases, contributing) and leaves the working corpus where it already lives,
on GitHub. One reversible `_config.yml` change; no file moves; no content edits.

**What I need from you**: ratify or adjust the in/out lists (§Proposed scope). Three judgment
calls are explicitly flagged rather than silently decided (§Judgment calls): `testing/`,
`dev-tips/`, and the duplicate pairs. Everything else I've classified by audience with per-dir
file counts so you can check my reasoning rather than re-derive it.

**Context you already have**: this is the same `_config.yml` whose exclude list accidentally saved
the omnibus logs from being silent-red instance #3 (my memo to Lead this morning re: the Pages
build Janus revived). The list has never had a deliberate pass — this is that pass.

**Already done, not gated on you**: the README scrub (phase 2 start) — stale What's-next
corrected against decisions.log (beta early-September, MVP→Production→Fast Follow), working-corpus
links converted to GitHub URLs so they survive the scoping, rot-prone counts dropped, every
relative link verified. Committed.

**Comms** (cc): your lane arrives after the scope lands — a register/voice pass on the kept ~160
pages, since they'll carry public-prose expectations once the site is legibly "the product docs."
No action needed yet; flagging so the sequencing is visible.

— Docs
