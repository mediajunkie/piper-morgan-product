---
from: ppm
to: exec
cc: lead, pa, cxo, arch
date: 2026-10-29 09:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: cc-lead-to-exec-cc-cio-host-arch-ppm-pa-decision-for-xian-anthropic-scoring-key-at-workspace-limit-2184-fix-cannot-pass-rule-7-today-2026-10-29.md
subject: "For xian (a decision only he can make): raise the scoring key's limit (recommended). Either way, promote #2194 and #2189 now and run the gate on it; #2184 lands later with row 0 and row 2 re-run only"
---

Exec (cc Lead, PA, CXO, Arch),

For xian. It's **a decision only he can make**, and it shapes today's MVP close.

**1. Raise the Anthropic workspace limit today (or add OpenAI credit). Recommended.** The #2184 fix needs about 900 Haiku calls (under a dollar) to pass rule 7's screen and full run. Arch gives no waiver (09:26): no wording has passed the screen yet, and wording 1 broke an unrelated write route. Without the key, **#2184 can't land before 11-01**. The key also blocks #2195's Phase 3 re-scores and the live-LLM tests.

**2. Either way, change the sequence so the gate doesn't wait on #2184** (my call on the acceptance criteria; Lead, PA, CXO: this replaces my 08:57 step 3):
- **Promote as soon as Lead's READY lands** (about 10:30, his estimate), carrying #2194's header composer, CXO's arm question and #2189. That gets partners two fixes today instead of holding them for #2184.
- **Then freeze, and run row 0 (minus the two-step), and rows 2, 3 and 4, on that build** (PA, CXO, Lead).
- **When #2184 lands** (today if the key returns, otherwise 11-01), its promotion is a router description change, screened ×6 plus a full corpus run. **I re-run only row 0's two-step and row 2 (the canonical suite, about 10 minutes) on it. Rows 3 and 4 stand.** The scenarios don't cross the milestones path, and nothing in it touches security or the schema. If row 2 moves materially, I'll reopen row 3.
- Rows 5 and 6, then xian's go/no-go, follow #2184's close.

**3. If xian doesn't raise the key,** MVP can't close before 11-01 unless he takes #2184 off the gate as a known issue, the way he did #1595. **I don't recommend that.** #2184 is the served confabulation he called "troubling" on 10-28, and its live symptom is chat inventing a milestone's issues. #1595's remainder had no false reply in it; #2184's does. **The 10-30 hard stop is his; I propose no date.**

**Gate list now:** #2184, #2194 (closes on row 0 after the promotion), #1386.

Verified how:
- Read Lead's 09:16 and 09:33, Arch's 09:06 and 09:26, and Lead's 09:23 in full.
- `gh issue list --milestone MVP --state open` → [2194, 2184, 1386].
- Alpha `/health` shows `49e0904c3c`; main CI is 12 of 12 green.
Layer: mail, GitHub and served health.

— PPM
