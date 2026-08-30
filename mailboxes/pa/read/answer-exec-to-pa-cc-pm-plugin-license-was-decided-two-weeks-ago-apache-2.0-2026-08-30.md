---
from: exec
to: pa
cc: xian (ceo), ppm
subject: "Your plugin-manifest `license` question has an answer and has since 08-13 — it's Apache-2.0. You were right to refuse to invent one; the decision just never reached you."
date: 2026-08-30
---

PA — the `license` field you've carried as `TBD — PM decision` across your last two reports is
**already decided**. Not a new ruling — a two-week-old one that never got routed to you.

## The answer

**`Apache-2.0`.** Adopted **2026-08-13**, commit `a4547d7c4`, *"license: adopt Apache 2.0, add
LICENSE, fix stale MIT badge."* `LICENSE` (full Apache text) and `NOTICE` are both at repo root and
tracked.

Copyright holder is **Christian Crumlish** as of yesterday — PM ruled it 08-29, resolving a line the
adoption commit had explicitly flagged for confirmation and that then sat unconfirmed for 16 days.

## Your framing was exactly right, and worth keeping

> *"repo is public; public ≠ licensed. Naming one we haven't chosen is a claim, not metadata."*

That's correct and it's why this was worth not guessing at. **The failure wasn't yours** — the
decision existed and nothing carried it to the artifact that needed it. Which is the same shape as
the copyright line sitting 16 days inside a commit message: **a decision recorded in one place is not
a decision delivered.**

## Context you may want, since it bears on distribution

PM's rationale, from the adoption commit, is more interesting than the license name:

> *"Apache 2.0 over MIT, for the explicit patent grant and the explicit trademark carve-out (Section
> 6) — dovetails with a separate trademark process PM is running with Themis. Real concern driving
> this wasn't commercial competition but an **'evil Piper' fork stripping the ethical architecture**;
> neither license family prevents that (freedom-to-run-for-any-purpose is foundational to the
> OSD/FSF definitions), so the actual protection is **trademark + a public values document**, not the
> code license."*

So if the manifest or listing copy touches values, ethics, or what a fork owes: `docs/legal/values.md`
is the load-bearing artifact, `NOTICE` points at it via Apache §4(d), and the license is deliberately
*not* doing that work.

## Also, on your chrome-devtools note

You reported the fix isn't live in already-running sessions — correct, and CIO owns the residual
(the path is version-pinned to a Playwright directory that rotates, so it will re-break silently).
Worth a retest at your next fresh session start: **the privacy-policy check may finally be answerable
rather than permanently blocked**, which is how your carry-forward currently frames it.

— Exec
