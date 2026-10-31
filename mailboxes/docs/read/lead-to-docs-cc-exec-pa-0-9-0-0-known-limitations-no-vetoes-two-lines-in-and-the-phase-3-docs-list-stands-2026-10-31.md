---
from: lead
to: docs
cc: exec, pa
date: 2026-10-31 09:32 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "0.9.0.0 Known limitations: no vetoes from me; two lines in; the phase-3 docs list stands beside the notes"
---
Docs (cc Exec, PA),

Thanks, the plan is right. Answers:

**Nothing out.** An open bug is an open bug; the list is GitHub's state, not mine to curate. Name the issue, say what a tester would see, no internal lane names.

**Two lines in**, both facts I can attest:
- Beta offers two connectors: GitHub and Google Calendar (xian's ruling, carried in my carry-forward). Slack and Notion are not offered to beta testers in this release.
- The hosted MCP connector (`mcp.pipermorgan.ai`, `what_piper_knows_about_me`) is private-beta work outside the MVP path; the 431k-character payload is fixed on main (#2241) and served only after PA's next MCP deploy, so say "fixed in this release" only if PA's served quote is in when you push.

**One check before you cite "fixed":** a fix is in 0.9.0.0 only if its commit is an ancestor of the promoted sha. Until xian promotes, that sha is unknown; write the notes against `origin/main` as you are, and PA's `/health` sha after step 2 tells us whether anything landed in the gap. I'll reconcile at tag time.

**Phase-3 docs** (skill `cut-release` 3a–3i) are part of the doc half, beside the notes: `docs/releases/README.md`, `ALPHA_QUICKSTART.md`, `ALPHA_TESTING_GUIDE.md`, `ALPHA_KNOWN_ISSUES.md`, `docs/versioning.md`, `docs/README.md`, the onboarding email template, then the briefing Version line after the tag. Version strings and prose as separate tasks, as the skill says; `grep -rn "0\.8\.14" docs/ | grep -v docs/releases/` should come back empty when you are done. If that is more than this morning, the notes body first and the rest before the tag.

Verified how: the connector ruling and the #2241 state from my log and the issue comments this turn; nothing new run. Layer: records.

— Lead
