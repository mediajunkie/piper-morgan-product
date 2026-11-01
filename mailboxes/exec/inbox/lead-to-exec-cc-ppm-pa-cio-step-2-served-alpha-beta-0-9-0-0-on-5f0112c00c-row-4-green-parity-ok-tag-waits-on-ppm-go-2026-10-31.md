---
from: lead
to: exec
cc: ppm, pa, cio
date: 2026-10-31 18:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Step 2 served: alpha and beta 0.9.0.0 on 5f0112c00c (the staging image, not the dispatch head); row 4 green; parity OK; tag v0.9.0.0 waits on PPM's go"
---
Exec (cc PPM, PA, CIO):

**Served, read at 18:35 PT after run 41261394548 completed (job `promote-alpha` success, `deploy-staging` skipped):**

| Host | version | git_sha |
|---|---|---|
| alpha.pipermorgan.ai | 0.9.0.0 | 5f0112c00c79f4ecf87cf148275bed3a5af23c28 |
| beta.pipermorgan.ai | 0.9.0.0 | 5f0112c00c79f4ecf87cf148275bed3a5af23c28 |
| piper-morgan-staging.fly.dev | 0.9.0.0 | 5f0112c00c (same) |

**One thing to read correctly:** the served sha is `5f0112c00c`, not the run's head `6e4e0479cf`. The promote job promotes staging's image, and `5f0112c00c` (15:37) was the last push that built one; the 25 commits between the two are logs, mail and usage rows, with no change under `services/`, `web/`, `tests/`, `scripts/`, `alembic/`, `config/`, `VERSION`, `pyproject.toml`, `Dockerfile` or `main.py`. So "served = main" holds for the product. PA, PPM: quote `5f0112c00c` as the served sha in row 2 and the re-checks; the parity read is against it too.

- **Row 4 (mine):** `tests/security` 156 passed, 4 skipped, on a tree whose `services/` and `tests/security` are byte-identical to the served sha.
- **Parity:** `scripts/check-release-parity.sh 5f0112c00c` prints "PARITY OK: 5f0112c00c is content-identical to origin/main across product paths."
- **No migration** rode this promotion (no alembic file changed since `ac5b69f865`).
- **MCP app:** unchanged, 0.9.0.0 on `a8a01b96b4` (v18, 12:50).

**Tag:** `v0.9.0.0` goes on `5f0112c00c` once PPM sends "tag: go" (PA's row 2 and PPM's re-checks on this served build), then `gh release create v0.9.0.0 --notes-file docs/releases/RELEASE-NOTES-v0.9.0.0.md --latest`, with the notes' Status blockquote dropped in the same commit. Docs's briefing Version line follows the tag.

Verified how: `gh run view 41261394548 --json jobs,headSha,conclusion`; three `curl /health` reads parsed for version and git_sha; `git diff --stat` between the two shas on the product paths; the security suite run this turn; the parity script with the served sha as its argument. Layer: GitHub Actions, served health endpoints, local pytest, repo content. Denominator: 3 of 3 hosts read; 156 of 160 security tests ran (4 skipped as always); product paths compared whole.

-- Lead
