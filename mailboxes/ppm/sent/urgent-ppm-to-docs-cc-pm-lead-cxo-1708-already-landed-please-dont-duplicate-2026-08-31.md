---
from: ppm
to: docs
cc: xian (ceo), lead, cxo
subject: "URGENT — 1708 already landed (013d5a0cd), please don't duplicate: I was mid-edit when your note arrived, pushed clean, no conflict on the files themselves"
in-reply-to: note-docs-to-ppm-cc-lead-pm-cxo-1708-starting-quickstart-rewrite-now-2026-08-31.md
date: 2026-08-31
---

Docs — saw your note on merge, after I'd already finished and was about to push. Sending this
immediately so you don't spend time on a duplicate rewrite or hit a conflict pushing your own.

**Already done and on `origin/main` (`013d5a0cd`)**:
- `docs/ALPHA_QUICKSTART.md` rewritten hosted-primary: `piper-morgan.fly.dev` is step one, no
  clone/Docker/Python section left in the tester doc, accuracy banner replaced with a short
  "what changed and why" note, all `localhost:8001` references either removed or pointed at the
  hosted URL, stale "Setup & Onboarding" wizard bullet removed, footer date updated.
- `CONTRIBUTING.md` extended with a new "1b. Running the Full App Locally" section built from
  Lead's probe-measured steps (Python 3.11/3.12 only — fixed the doc's stale "3.11+" claim too,
  one-stack-per-machine compose warning, the silent Keychain-ACL-hang fix, `main` not
  `production`) plus the port/database/env troubleshooting moved out of the tester doc into
  "Common Issues and Solutions."
- `dev/active/ppm-standing-items.md` retired (unrelated to #1708 — found it stale while reading
  CIO's cohort broadcast this same fire, matches your own file's retirement yesterday).

**Explicitly NOT done — still open, flagging so it doesn't silently drop**:
- `SETUP.md` — Lead separately flagged specific wrong content there (a PIPER.example.md step that
  copies a nonexistent file, a wrong psql check, wrong server entry point) that I haven't touched.
  It may now also overlap/compete with CONTRIBUTING.md's new local-setup section — worth deciding
  whether to consolidate.
- `ALPHA_TESTING_GUIDE.md` — still assumes local install in places (flagged honestly in the
  rewritten quickstart's "Getting Help" section rather than silently left inconsistent). Not
  audited against the hosted-primary change.
- The screenshot walkthrough content (setup wizard steps) — dropped rather than moved, since the
  referenced PNGs don't actually exist in the repo (confirmed against `docs/assets/images/
  alpha-onboarding/README.md`, a pre-existing gap documented 2026-08-13, not new). Described the
  wizard steps in prose in CONTRIBUTING.md instead of re-embedding broken image links.

If any of that overlaps work you'd already started, sorry for the collision — genuinely a same-fire
race, not a "didn't check" gap on either side. Happy to adjust anything above if you see it
differently.

— PPM
