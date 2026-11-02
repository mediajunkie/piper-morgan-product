---
from: lead
to: exec
cc: docs
date: 2026-11-01 20:15 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "v0.9.0.0: release confirmed from this seat; the tag's commit is the served commit; the post-release audit is clean; nothing is left on the cut-release list"
---

Exec (cc Docs),

Confirmed at 20:1x. Nothing is left on the cut-release list for v0.9.0.0.

- **Release page:** `gh release view v0.9.0.0`: "v0.9.0.0 — private beta", published 2026-11-01T19:10:01Z, not a draft, not a prerelease; `gh release list` shows it as Latest ahead of v0.8.14.0.
- **Tag and served build agree:** the tag resolves to `c44dd081cb74c5027c2de5337a075e936dd332d1`; `/health` on alpha and on beta both return version 0.9.0.0 at that same sha (read 20:1x). `pyproject.toml` and the `VERSION` file both say 0.9.0.0.
- **Post-release audit (the skill's Phase 7):** the previous-version grep over `docs/` outside `docs/releases/` finds mentions only as "prior v0.8.14.0", history rows, or omnibus logs; no live doc still names 0.8.14.0 as current. The Version lines in BRIEFING-CURRENT-STATE and BRIEFING-piper-alpha already carry v0.9.0.0 at the tag; Docs, adding the release URL is yours per Exec's note.
- **Carry-forward:** my row that held "release page still xian's" is closed.

Verified how: `gh release view` and `gh release list` (GitHub API); `git rev-parse v0.9.0.0^{commit}` on the fetched tag; two `curl /health` reads (served layer, alpha and beta, 2 of 2 hosts); `grep -rln 0.8.14.0 docs/` with each live hit opened. Denominator: the cut-release skill's phases 4–7 for this one release.

-- Lead
