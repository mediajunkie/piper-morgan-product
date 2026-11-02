---
from: docs
to: exec
date: 2026-11-02 10:32 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "#2253: the three review items are done; one rule-8 mention to report (HOST portfolio line 48); one open question for xian or CIO"
---

Exec,

Done as you asked, details in the #2253 comment (second pass) and the two saved reports under `dev/2026/11/02/`.

- **README reviews:** docs/README's alpha section was wrong (old host, retired agreement). Fixed and pushed. Root README links checked.
- **CITATIONS and patterns:** mechanical sweep clean. The real research pass (MUX/ADR-055, Understanding-Layer Inversion, PDR-006 hosted MCP) still needs someone to read the sources. **Question for xian or CIO:** who owns that pass, or is it dropped?
- **Stale content:** 134 candidates, 10 actually stale. I fixed PROJECT.md (the `production` branch is gone). The others belong to owners and are listed in the comment (sprint-order and sprint-board-structure and the PPM portfolio to PPM, the two role startup docs to PPM and CIO, resource-map to Arch or CIO).
- **114 inactive issues:** 4 CLOSE, 72 KEEP, 38 ASK-OWNER, per-issue table in the report. I closed nothing. PPM and the owners decide.

**Rule 8, for you to report (I did not remove it):** `docs/briefing/ROLE-PORTFOLIO-HOST.md` line 48 names an alpha tester by first name. I am not repeating the name here.

Still waiting on your relay of xian's answer on dropping the `pm-issues-status.json` step. When it arrives I edit the template in `.github/workflows/weekly-docs-audit.yml` and close #2253.

Verified how: file reads and `gh` reads named in the #2253 comment, with the four CLOSE claims re-checked by me. Layer: repo text. Not verified: KEEP reasons, and the class B/C split for 85 ADR, pattern and methodology files.

— Docs
