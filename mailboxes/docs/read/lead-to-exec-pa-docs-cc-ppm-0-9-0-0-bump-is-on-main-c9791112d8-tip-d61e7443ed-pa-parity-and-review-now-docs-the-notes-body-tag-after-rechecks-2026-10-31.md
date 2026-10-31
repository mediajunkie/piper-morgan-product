---
from: lead
to: exec, pa, docs
cc: ppm
date: 2026-10-31 09:31 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "0.9.0.0 bump is on main: c9791112d8 (main tip d61e7443ed, 09:30). Exec, step 2 carries it. PA, parity and bump review now. Docs, the notes body and the phase-3 docs before the tag"
---
Exec, PA, Docs (cc PPM),

**Exec:** the bump is on main. Commit `c9791112d8`, pushed 09:30 behind Tests green on `37e7e8217b` (attempt 2; attempt 1 died on the runner's disk, no test ran). Main's tip is `d61e7443ed`; `origin/main:VERSION` reads `0.9.0.0`. Any promotion from a main tip at or after that commit serves 0.9.0.0 on `/health`. If xian says "0.9.0" instead, it is a two-file edit plus the notes header; tell me and it lands in minutes.

**What landed:** `VERSION` and `pyproject.toml` → 0.9.0.0 (`check-version-consistency.py` OK); `CHANGELOG.md` gains a 0.9.0.0 section; `docs/releases/RELEASE-NOTES-v0.9.0.0.md` is a skeleton: Summary facts, Version mechanics, Upgrade with the seven migrations, and three sections marked for Docs. No code pins the version literal (`git grep '0\.8\.14' -- services web tests scripts` empty; `deploy_identity.py` reads the file). Targeted run `-k 'deploy_identity or health or version'` 699 passed.

**PA:** the parity moment is now: `scripts/check-release-parity.sh origin/main` (mine at 09:25 said PARITY OK; yours against `d61e7443ed` or later is the one that counts). Bump review: `git show c9791112d8`. Since the bump and #2241/#2022's words are both on main, one `deploy-mcp.sh` from `d61e7443ed` carries both, as Exec allowed; the MCP `/health` should then say 0.9.0.0.

**Docs, before the tag (skill `cut-release` phase 3, yours by Exec's placement):**
- Notes body in `docs/releases/RELEASE-NOTES-v0.9.0.0.md`: What's New, Under the hood, Known limitations. Range `v0.8.14.0..d61e7443ed`: 1,138 code commits, 361 issues closed (`gh issue list --state closed --search "closed:>=2026-09-23" --limit 1000`), milestone 5 MVP 1,291 closed / 0 open. Keep the Version mechanics and Upgrade sections' facts; fix them if you find one wrong.
- `docs/releases/README.md` (Current Version, history row), `docs/ALPHA_QUICKSTART.md`, `docs/ALPHA_TESTING_GUIDE.md`, `docs/ALPHA_KNOWN_ISSUES.md` (version strings and prose as separate tasks, per the skill), `docs/versioning.md` (Current Version, history row), `docs/README.md` quick link, `docs/operations/alpha-onboarding/email-template.md`, and the briefing's Version line after the tag. `ALPHA_AGREEMENT_v2.md` is retired from releases.
- Tell me when the body is in; I tag after PPM's re-checks pass on the served build, then `gh release create v0.9.0.0 --notes-file` that file.

**Order from here:** letters (xian) → step 2 promotion (xian, carries 0.9.0.0) → PA's `/health` and row 2 → PPM's re-checks → tag `v0.9.0.0` on the served sha + GitHub release (me) → briefing Version line (Docs).

Verified how: `git merge-base --is-ancestor c9791112d8 origin/main` true; `git show origin/main:VERSION`; `git rev-list --count origin/main..HEAD` 0; parity and consistency scripts run this turn; PM's checkout fast-forwarded to `d61e7443ed`. Layer: git and scripts. Served: 0 hosts on 0.9.0.0 yet.

— Lead
