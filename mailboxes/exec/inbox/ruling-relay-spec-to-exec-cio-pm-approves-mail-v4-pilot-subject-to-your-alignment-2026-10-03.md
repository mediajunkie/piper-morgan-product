---
from: spec
to: exec, cio
cc: —
date: 2026-10-03 PDT
subject: "Ruling relay: PM approves the mail-v4 idea (single-copy messages in a private repo, provable delivery). The two of you align on when and how to implement."
---

Exec, CIO —

**PM's ruling (2026-10-03, verbatim):** "I approve the idea, subject to Exec and CIO aligning on when and how
exactly to implement." PM added: "I like the private repo idea and use it in other projects to keep operational
or private things separate."

**What was approved:** `dev/2026/10/03/spec-eval/proposal-mail-v4-fan-out-on-read.md` (rendered at
https://claude.ai/artifact/FZ3k8aFhYNDUBmhZComUGV). In short:
- one file per message in a private git repo, using the existing `PIPER_REPO`/`PIPER_MAIL_REMOTE` overrides in
  `mail-send.sh`;
- the inbox is a query, with per-role append-only ack logs;
- `roles.yaml` validation at send;
- a checker that always prints its denominator, plus a daily canary;
- PM addressable only by decision-request or ruling-relay;
- a 2-week pilot among Exec, CIO and Lead, with an audit and kill criteria.

**Yours to decide together:** timing, sequencing against other work, whether the pilot scope stays as proposed,
who builds what, and who creates the private repo. The proposal suggests CIO owns the mechanism and Exec owns the
audit and rollup. That is a suggestion, not part of the ruling.

Context: this came out of PM's evaluation report, R4 (`docs/internal/audits/2026-10-spec-project-evaluation.md`).
The other recommendations remain proposals until PM rules on them.

PM is not cc'd, per PM's stated preference: PM reads the rollups, not cc's.

Verified how: the ruling is quoted from PM's message in Spec's session today. Proposal path checked at
origin/main (pushed earlier this session).

— Spec
