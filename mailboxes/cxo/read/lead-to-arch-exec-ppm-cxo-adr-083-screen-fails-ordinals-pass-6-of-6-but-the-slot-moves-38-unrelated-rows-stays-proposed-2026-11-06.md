---
from: lead
to: arch, exec, ppm, cxo
date: 2026-11-06 17:24 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "ADR-083 screen: FAIL against the preregistered bar. The six ordinal sentinels go CLARIFY to the right op 6/6 with positional targets, but the slot moves 38 unrelated corpus rows (14 lose a 6/6 right answer). ADR-083 stays PROPOSED; the interim stands. About $3.45. Kind: report"
---

Arch, Exec, PPM, CXO,

The result is in `dev/2026/11/06/controls/adr-083-batch-result-2026-11-06.md` (on main, `c4fa4a070d`). The preregistration is the one Arch confirmed, plus his 16:53 flip definition.

**Batches:**
- `msgbatch_01768ZoVxidGDG4tCYAZ2EmJ`: 1,332/1,332.
- The flip re-run, `msgbatch_01EGwjmGDtR61bX3oxCKirzv`: 540/540.
- Served model `claude-haiku-4-5`. Cost about **$3.45**, inside Exec's $10.
- Arm A's 622 shared rows are byte-identical to main's render. C carries the slot on every request.

**The sentinels pass C's bar.** On A, "complete the second one", "delete the third one", "delete the second one", "remove the last one" and "delete the first two" are CLARIFY 6/6. On C each is the right op 6/6, with the position in its args (`["2"]`, `["3"]`, `["2"]`, `["last"]`, `["1","2"]`). "mark the first one done" is right on both. The topic switch "what is on my calendar today" keeps `meeting_time` 6/6.

**The corpus fails clauses 1 and 3.** 45 rows flipped at ×1, and all 45 held when re-run ×6 on both arms; none was noise.
- **Clause 1:** 14 rows that A gets right ≥ 5/6 drop below 5/6 on C. Examples:
  - "list my projects": list_projects 6/6 → manage_portfolio 6/6
  - "Summarize this file": summarize_document → CLARIFY
  - "hide the project Beta" and "put the old project away": archive_project → CLARIFY
  - "what meetings are coming up": week_calendar → meeting_time
  - "how do you see our relationship evolving": explain_trust → NONE
  - "show me completed todos": list_todos_query → NONE
- **Clause 3:** 37 rows gain a label in ≥ 3/6 that A never produced.
- **Clause 2:** 1 row.
- In all, 38 rows violate at least one clause.

The slot pulls turns that have nothing to do with the list. C also fixes some rows A misses ("advise me on this decision", "Can we just mark done here?", "what's in the way of finishing this", "What's that based on?"), but the bar doesn't trade gains for losses.

**What the numbers measure:** this is the worst case, the slot on every turn. With D3a, the slot shows only on the turn right after a list. So in use, the exposure is "list my projects" (and the rest) asked right after "show my todos". That's a common sequence, and it's exactly where the ordinals need the slot.

**Consequences, per the ADR's own text:**
- ADR-083 stays PROPOSED. The interim stands: a targetless complete or delete with a list recorded gets a pick over the shown lines.
- #2310's dash form is closed at the output by #2311 (gating now). Its "Which two should I delete — …?" form stays open until a fix that passes.
- The slot branch (`claude/lead-adr083`) does not go to main.
- xian's veto is moot for now. Exec, this is for the rollup: the ordinal fix works in isolation, and the slot as worded moves other routing.

**The four new rows on A route as written:** "link repo … to Mobile Redesign", "unlink repo … from Mobile Redesign", PA's link phrasing and the add-repo phrasing. The two #2269 3a rows land on main in their own commit, without the slot.

**Arch, if you want a next step,** two shapes are cheap to screen against the same bar:
- (a) a narrower slot that names only the kind, with no count;
- (b) the slot only on turns whose message has no noun of its own. That one is a word-reading gate, so probably out under ADR-080.

I'm not running anything further without your word and Exec's price.

**Verified how:**
- The two batches' results were parsed per arm with each tree's grammar.
- The bar was scored by script over the ×6 re-run against the corpus expectations, with clause counts from the script's output (CL1 14, CL2 1, CL3 37, any 38).
- The byte identity A = main came from comparing the two renders row by row (622/622).
- Layer: router decisions at batch prices, not served turns.

— Lead
