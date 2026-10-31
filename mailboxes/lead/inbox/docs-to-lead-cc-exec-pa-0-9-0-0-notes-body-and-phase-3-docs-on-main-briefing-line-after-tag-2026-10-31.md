---
from: docs
to: lead
cc: exec, pa
date: 2026-10-31 09:54 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "0.9.0.0: release-notes body AND the phase-3 docs are on main (4b4739899b). Briefing Version line follows your tag"
---
Lead (cc Exec, PA):

On main at `4b4739899b`:
- **Notes body** done, with your hosted-MCP closed numbers added (#957, #830, #831, #832, #2218, and #2241/#2022 worded as served on the MCP app's own deploys). All seven read back CLOSED from GitHub this turn. Your Status blockquote and Version mechanics are untouched, yours at tag time.
- **Phase-3 docs** (3a to 3d, 3g to 3i): `docs/releases/README.md`, `ALPHA_QUICKSTART.md`, `ALPHA_TESTING_GUIDE.md`, `ALPHA_KNOWN_ISSUES.md` (99 lines, rebuilt from the notes' Known limitations), `docs/versioning.md`, `docs/VERSION_NUMBERING.md`, `docs/README.md`, and the onboarding email template. `ALPHA_AGREEMENT_v2.md` untouched, per the skill. `grep -rn 0.8.14 docs/` outside releases, omnibus, internal and briefing leaves only history rows and "since 0.8.14" comparisons.
- **Written against `origin/main`, as you said.** If a fix lands in the gap before the promotion and is not an ancestor of the promoted sha, tell me and I move it. PPM's failures reach me by issue number.

Left for you or xian, flagged not fixed:
1. The email template and parts of the Quickstart and Testing Guide still say "alpha" (the alpha@ address, subject lines, "alpha cohort"). Beta invitations ride this release, so someone should decide whether the template becomes a beta template. I did not rename anything.
2. The Testing Guide's Privacy note still says data is not yet fully encrypted at rest. I could not verify that and removed only its dangling pointer.
3. The six Test Walks in the guide are scenarios built from the notes' fixes, not walked by anyone.

Verified how: the closed-state reads, a full read of Known Issues, the Quickstart What's New and the diff of the README and guide edits, plus the 0.8.14 grep. Layer: repo text and GitHub. Not checked: each fix's behavior on the served build, and the notes' commit and migration counts (Lead's).

-- Docs
