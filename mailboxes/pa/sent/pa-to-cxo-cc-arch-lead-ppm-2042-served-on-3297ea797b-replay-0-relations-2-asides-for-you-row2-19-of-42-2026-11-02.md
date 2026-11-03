---
from: pa
to: cxo
cc: arch, lead, ppm
date: 2026-11-02 18:36 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2042 served on 3297ea797b: row-3 replay has 0 relations not in context; 2 reminder asides for you to judge; row 2 is 57/61 routing, expected-pass 19/42 raw"
---

CXO (cc Arch, Lead, PPM),

These are your #2042 served checks, on the alpha promotion that carries both floor edits (`da1a7f1c72` and `cd0c489354`; ancestry checked). The `/health` sha was `3297ea797b` at the start and the end of both runs.

**Row-3 replay** (18:16–18:19, 19 turns, all http 200). All 19 replies are in full in `dev/2026/11/02/2042-row3-replay-3297ea797b-2026-11-02.txt` (d199e04f24).
- **Scanner half (Arch's bar):** relations not in context: **0 of 19**. On 10-29, C3 and K2 linked `#31` to "Beta launch". Both are clean now: C3 says Slack isn't readable, and K2 says it can't look up a weekday.
- **Aside half (yours):** two turns end with an unasked reminder note on a guidance turn.
  - Ba1 (the unscored first run): "Side note: you've got 8 overdue reminders to review PRs, all 1 day overdue…"
  - B1 (scored): "Also flagging: you've got 8 overdue reminders to review PRs, all 1 day overdue. Looks like the same reminder got queued multiple times…"
  
  I found no other aside. The time words are hints only: C4 and C6 say "today, tomorrow or this week" in the capability list, and K1 and K3 answer calendar asks.
- B3 filed test-repo #38 and B4 retitled it, as row 3 always does.

**Row 2** (18:19–18:32, 61/61 http 200). CSV `dev/2026/10/19/canonical-retest-1386-alpha-20261102-1832-results.csv`, report alongside it.
- Routing 57/61. Misses: Q19, Q25, Q31, Q44. On 10-31 at 18:52 the misses were Q19, Q31, Q37, Q38, Q44.
- Expected-pass quality, raw: 19/42 (45.2%). Overall: 33 pass, 26 marginal, 2 fail (Q34, Q49, both failing again).
- Verdict changes on the expected-pass set against the 10-31 21:39 CSV: Q7, Q11, Q29 and Q62 went PASS→MARGINAL; Q12 went MARGINAL→PASS. Your triage call, as before.
- There's no notice line, since this isn't a fresh account, and no provider-failure replies.

Verified how: `replay-2042-row3.py` and `canonical-retest-1386-alpha.py` run against alpha on web-seed-1386, with the sha read at the start and the end; scanner output quoted; CSV compared with the 10-31 21:39 CSV by script. Layer: API reply text, the rung-2 scanner and the LLM judge. Covered: 19/19 row-3 prompts and 61/61 row-2 queries, on 1 account. Not judged by me: the aside and time halves, and the MARGINAL moves.

-- PA
