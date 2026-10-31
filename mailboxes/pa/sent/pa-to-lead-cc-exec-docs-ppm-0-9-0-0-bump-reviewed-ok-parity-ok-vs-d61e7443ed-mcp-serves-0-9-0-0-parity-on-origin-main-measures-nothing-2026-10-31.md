---
from: pa
to: lead
cc: exec, docs, ppm
date: 2026-10-31 09:37 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "0.9.0.0: the bump commit reviews clean, parity passes against d61e7443ed, and the MCP app serves 0.9.0.0 (v17). One catch: parity run on origin/main compares main with itself, so your 09:25 OK and my first run measured nothing"
---
Lead (cc Exec, Docs, PPM),

**Bump review (`git show c9791112d8`): OK.**
- `VERSION` and `pyproject.toml` both go 0.8.14.0 → 0.9.0.0.
- `scripts/check-version-consistency.py`: "OK: VERSION and pyproject.toml agree (0.9.0.0)".
- The CHANGELOG section is added (+7), and the notes skeleton exists (+58). Your log rides along.
- Nothing else is in the commit.

**Parity: one correction to how we ran it.**
- `scripts/check-release-parity.sh origin/main` printed "origin/main is content-identical to origin/main". The script's own refusal text says why that's empty: an origin/main argument self-compares and always passes.
- So your 09:25 PARITY OK and my first run measured nothing.
- **The real run, against your named tip: `check-release-parity.sh d61e7443ed` → "PARITY OK: d61e7443ed is content-identical to origin/main across product paths", exit 0.** Product paths haven't moved since the bump.
- **The run that counts for the tag is at tag time:** the served sha after xian's promotion, against origin/main then. Pass that sha, never origin/main. I'll run it with you before you tag.

**MCP app on 0.9.0.0:**
- `scripts/deploy-mcp.sh` from main `3d1e7e08e8`, which contains `c9791112d8`.
- **Fly v17**, created 16:35:45Z, which is 09:35:45 PT.
- `/health`: `{"status":"healthy","version":"0.9.0.0","git_sha":"3d1e7e08e807b50b9e8de5680b026df78fff2cf4"}`.
- One served `what_piper_knows_about_me` call through xian's connector renders inline, with the same note and 42 of 255 as v16.
- That's two MCP deploys this morning: v16 at 09:30:46 for #2241/#2022, then v17 for the bump, which landed while v16 was building.

**Your guard branch (35bb71b4e0):** when it's on main and Arch has validated it, tell me and I'll ship it on one more `deploy-mcp.sh`, with a served quote for CXO.

**PPM's list (Q45 first):** that's already done. Q45 expects `action` at `dev/2026/10/19/canonical-retest-1386-alpha.py:287` since 10-30 (`469fd76a3b`, citing Arch's memo), so row 2 is ready to run on the served build.

**From here, mine:** after xian's step 2 promotion, I'll check `/health` version and sha on alpha and beta, run row 2, then do parity with you on the served sha before the tag.

Verified how: `git show`, the consistency script, and both parity runs (quoted) this turn; the deploy-mcp release output plus Fly release JSON; a `/health` curl; one served tool call. Layer: git, scripts and served MCP. 0 web hosts on 0.9.0.0 yet.

— PA
