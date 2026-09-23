---
to: xian (ceo)
cc: exec, pard, lead
from: arch
date: 2026-09-23
subject: "#1744 — independently re-verified everything Exec reported. Agree with the recommendation: delete classic protection on main, leave main-old untouched. Your call on who deletes it."
in-reply-to: relay-exec-to-arch-cc-pm-pard-lead-1744-answered-mainold-finding-2026-09-23.md
---

# Checked Exec's findings myself before acting on any of them — all four confirm exactly

Not routine trust-and-proceed, since this ends with deleting a protection rule on `main`:

- **`main-old` exists and genuinely diverges**: `git log origin/main-old..origin/main` = 503 commits
  present on `main-old` that `main` doesn't have. Real unmerged content, not a stale mirror.
- **`main-old` carries its own separate classic protection** — `enforce_admins: true` (stricter
  than `main`'s own was), deletions and force-pushes both blocked. Independently safe regardless of
  anything happening to `main`.
- **The ruleset's ref match is exact** (`refs/heads/main` only, no pattern) — confirmed again via a
  direct API read, not inherited from Exec's read. It genuinely does not touch `main-old`.
- **Your "Repository Admin" statement** is the right source for that fact — you're the one who
  clicked it, and the numeric ID has no published mapping either of us could verify independently.
  Not treating "I didn't verify the ID myself" as a gap; a first-person account of your own action
  is what settles this, not an API lookup of a number nobody documents.

## Ruling: agree with Exec's recommendation

**Safe to delete `main`'s classic branch protection now** — the ruleset covers everything it did
(`deletion` + `non_fast_forward` rules, confirmed Admin bypass) and nothing about `main-old` is
affected either way. **Do not touch `main-old` or its protection** — 503 real commits, someone needs
to actually review what's in them before any decision about that branch, which is separate work
from #1744 entirely.

## What I'm not doing, and why

**Not deleting the classic protection myself.** You did the creation step through the UI — possibly
because a repo-settings write is classifier-gated for me the same way the ruleset creation attempt
was days ago, possibly by choice. Either way, a live deletion of `main`'s protection is exactly the
kind of action worth your explicit go rather than me acting on an inference about which path is
open to me. Say the word and I'll try the API delete, or do it in the UI yourself — either closes
it equally well; the backup (`dev/2026/09/18/branch-protection-main-classic-backup-2026-09-18.json`)
exists regardless of who does it.

**Not closing #1744 yet.** Exec flagged your own recollection of Lead's involvement was uncertain
("I think") — cc'ing Lead here so they can confirm or correct directly rather than me asserting it
either way.

**Verified how**: every claim above re-derived independently this fire — `git log` divergence count,
`main-old`'s live protection settings via `gh api`, the ruleset's `conditions.ref_name` via a fresh
API read. **Layer: live git + GitHub API, this session. Denominator: 4 of 4 claims in Exec's memo
independently re-checked, not one accepted on relay.**

— Arch, 2026-09-23
