---
from: lead
to: exec, docs
cc: pa, ppm
date: 2026-10-31 09:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "0.9.0 for the beta (xian via Docs 09:14): Lead owns the cut with PA in the loop; the cut is the version-bump commit on main's head; three inputs I need from xian through Exec before I tag"
---
Exec, Docs (cc PA, PPM),

Taking xian's word as relayed by Docs at 09:14: a 0.9.0 release for the beta. Lead owns the cut, PA in the loop (the 06-22 rule: never cut solo), Exec confirms timing, Docs takes the doc half. Procedure is skill `cut-release` with the runbook, parity gate first.

**Where things stand (read 09:16):**
- Latest tag `v0.8.14.0` (09-23). `pyproject.toml` and `VERSION` both `0.8.14.0`; they agree.
- alpha and beta both serve `ac5b69f865`, `/health` version `0.8.14.0`. `/health` reads the `VERSION` file, so a served surface says 0.9.0 only after the commit carrying the bump is promoted.
- No open P0. CI Tests green at `e394cb4c21`; the run on `37e7e8217b` failed on the runner's disk (no test ran) and its re-run is in progress.
- `origin/production` no longer exists; the release train deploys main cuts (`deploy-environments-and-release-train.md`, phase 3: beta invitations out → `production` cuts to beta as the primary surface). `release-exclusions.txt` is absent, so the parity gate needs an empty diff or a fresh exclusions file.
- MVP closed 10-30 17:03; decisions.log 08-30: "MVP closure ends alpha and starts invitation-only private beta (v0.9.0)". The gate for 0.9.0 is met.

**What the cut is.** One commit on main's head: `VERSION` + `pyproject.toml` to the new version, `CHANGELOG.md` `[Unreleased]` → the release, `docs/releases/RELEASE-NOTES-v<ver>.md` (Docs's body), then the tag on that commit and the GitHub release. A tag cannot go on `ac5b69f865`: its `VERSION` says 0.8.14.0. So 0.9.0 is served when that commit is promoted (alpha, verify, then beta), which is the next promotion in my order anyway. The cut is a push to main and is allowed under the freeze; the promotion is not.

**Three inputs, xian's through you, Exec:**
1. **Version string.** Tags since `v0.8.9.2` are four-part (`v0.8.11.0` … `v0.8.14.0`). Default unless he says otherwise: `0.9.0.0`, tag `v0.9.0.0`. If he wants literally `0.9.0`, say so and I use it.
2. **Cut point.** Default: main's head once the Tests re-run is green, with the bump commit itself as the cut. If he wants a specific sha frozen first (for example after one more fix), name it.
3. **Timing.** The cut can go today, before or after the letters. Does he want the 0.9.0 sha promoted to alpha and beta the same day the letters go (his word via you lifts the freeze), or the cut now and the promotion on his next word? The letters invite people to beta; if beta should say 0.9.0 when they arrive, the promotion comes first.

**Docs:** the release-notes body is yours (What's New since 09-23, Known limitations, Upgrade), `CHANGELOG.md`, and the briefing refresh after the tag. I'll send you the commit range (`v0.8.14.0..<cut>`) and the issue list when the cut point is fixed; the version strings I change myself in the bump commit, and `scripts/check-version-consistency.py` must print OK.

**PA:** `scripts/check-release-parity.sh` with me before the tag, review of the bump commit, and the served checks after the promotion (`/health` version and sha on both hosts, your row 2). Tell me if you want the tag push to be yours.

Verified how: `git tag --sort=-creatordate`, `cat VERSION`, `grep version pyproject.toml`, `curl /health` on both hosts, `gh issue list --label P0`, `git fetch origin production` (not found), `ls docs/releases/`, the release-train doc and decisions.log lines, read this turn. Layer: git, files, served health. Denominator: the inputs the skill names; no release step run.

— Lead
