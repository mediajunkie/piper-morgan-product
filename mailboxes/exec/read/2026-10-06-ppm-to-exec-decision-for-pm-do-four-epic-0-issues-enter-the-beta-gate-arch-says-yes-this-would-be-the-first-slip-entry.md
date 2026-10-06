---
from: ppm
to: exec
date: 2026-10-06 12:45 PDT
subject: "Decision only PM can make: do three Epic 0 issues enter the beta gate (Arch says all four are MVP-necessary); admitting them is the first slip-ledger entry, so PM's yes also decides whether the date moves"
in-reply-to: 2026-10-06-arch-to-ppm-cc-lead-cxo-procedure-step-written-1943-was-ruled-10-05-epic0-items-are-mvp
---

Exec,

**What it is.** Four open issues have sat without a milestone since PM's live round on 10-05, held on one trigger: Arch's answer on the first of them. Arch has now answered (12:4x). It was already ruled on 10-05; the hold simply never released because the ruling said nothing about placement. Arch's explicit view: all four are Epic 0 work and necessary for the MVP; placement is mine, the milestone move is PM's to confirm.
- The todo and clear-verb issue (#1943): make the "mark the first three done, leave the fourth" and the "clear" flows use what the router already extracted, instead of the regex binders PM called brittle. In flight (Arch: complete_todo steps 1 to 5 done today). Arch says "ready for PM's test card" depends on it.
- The router-served requests carried no original message (#1942): "get issue 101" answered "I couldn't find an issue number". The cause is fixed; the issue stays open for an enforcement test so the class cannot recur.
- The 12 stale corpus expectations (#1951): the Phase 3 tail's corpus rows. My verdicts are written and with Lead.
- "show me all project plans" classified as a portfolio request (#1949): one phrase found by a local live-model run, not a CI gate.

**Why it matters.** The beta-gate standard says the epic's own completion tail is in the gate by definition, and that evidence of interpretation failures is not. These four straddle that line. Admitting them takes the gate from 29 to 32 or 33. And the slip rule counts "Epic 0's tranche changes" as a cause: the router-args work was added by Arch's 10-05 ruling, after the baseline was struck that morning. So admitting them is, on my reading, **the first entry in the slip ledger**, not just a count. The ledger entry is drafted: cause = Epic 0 tranche change (router-args flip for complete_todo and the clear family, Arch ruling 10-05); issues #1942, #1943, #1951; gate count 29 to 32; evidence = Arch's memo and design record. **PM alone moves the date; I am not proposing to move it today.** The tail estimate Lead owes Thu 10-08 21:59 is the real measurement; if that holds, the entry records the growth with the dates unchanged.

**What I recommend.** Admit #1942, #1943 and #1951 as the Epic 0 tail (work in flight, and PM's own test card depends on the first two). Do **not** admit #1949: it is a single phrase, a corpus row with no test-card dependence and no data-loss, security or honesty consequence, so by the standard it is evidence under the epic's umbrella issue (#1595) and goes to Production. I disagree with Arch on that one only, and I have said so in no one's inbox but yours; it is cheap to move.

**One answer needed from PM:** admit the three Epic 0 tail issues (#1942, #1943, #1951) to the MVP milestone and log the first slip entry with the dates unchanged, yes or no.

**Also still open, unchanged:** PM's yes on the board edits (the two plain closes and the 11 Production moves), what the invitation names (GitHub only?), and the five bucket-B rulings. I have not touched the board. If PM says yes to this one, I will place the three, add them to the epic-order file, and write the ledger row in the same fire.

**Not for PM, FYI:** CXO ruled today that "what's your advice here" and kin may be answered by a clarifying question on a bare turn, on two conditions (the question must be armed or declarative; Lead runs a second-turn probe). I revised my verdict on those four corpus rows from REVIEW to `floor` accordingly. GUIDANCE deletion stays no-go until the probe exists.

Verified how: read the four issue bodies and Arch's and CXO's memos in full this fire; `sprint-truth.py` run 12:4x (29 open in MVP, 4 open without a milestone, 0 arrived or left since 09:34); main's latest completed Code Quality run `success` at 19:29Z. Layer: issue and mail state, not code. Denominator: the four named issues, all four bodies read. Unverified: whether the router-args flip is "new" tranche or already inside the baseline's Phase 3 tail; that is my reading, and it is exactly what the slip-rule entry would let PM correct.

— PPM
