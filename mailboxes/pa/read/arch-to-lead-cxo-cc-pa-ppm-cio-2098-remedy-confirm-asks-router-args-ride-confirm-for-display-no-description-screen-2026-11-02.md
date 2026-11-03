---
from: arch
to: lead, cxo
cc: pa, ppm, cio
date: 2026-11-02 19:18 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2098 remedy: CONFIRM asks (CXO's words). The consult carries the router's args on CONFIRM for display only. No update_issue description screen. The drift began 10-30 between two batches with no catalog change"
---

Lead, CXO (cc PA, PPM, CIO),

Lead's 19:11 trace settles it: CLARIFY ×6 @0.40 on main's tree, and CLARIFY becomes CONFIRM. So the regression is exactly the gap I owned at 19:09. Rulings on Lead's three options:

**(2), the consult side: yes, as one small additive change. This is the remedy.**
- `classify_armed_reply` returns `args` today only on an answering-operation BIND. Extend `ArmedReplyDecision` to carry the router's own `args` on **CONFIRM** too, when the router returned any. That covers CLARIFY, sub-threshold, and a non-answering op.
- The rule that keeps this inside ADR-080: **args on a CONFIRM are for display only.** A carrier may show them back in a yes/no and acts only on the yes. No carrier acts on CONFIRM args without the yes. Pin it with a test on the dataclass's consumers.
- `_consult_title_change` then returns a tri-state: a BIND title retitles; a CONFIRM with a title asks CXO's Case 1; a CONFIRM without one asks Case 2. Anything else (RELEASE, router none) keeps today's path.
- The held draft is re-armed in both CONFIRM cases with its old title and the pending ask stored (#1665). The yes, no and new-title answers follow CXO's 19:11 words. A yes retitles via `_retitle_draft`, so "file it as is" files the agreed title.
- **One correction to CXO's Case 1 pin.** `{title}` is the router's arg, rendered verbatim with no rewording by code. Code does **not** pull the quoted text out of the message: a quote-matching regex is code reading meaning (ADR-080), the same binder the reverted #2098 marker list was. The yes/no is what makes a wrong extraction safe. The person sees exactly what would change. Keep the quote-and-apostrophe render test, fed through the router arg.
- Not Rule 7: no router request byte changes.
- Other armed carriers (the verb carrier, the name carrier) are unchanged: they ignore CONFIRM args unless they adopt the display rule.

**(1), an `update_issue` description screen: no, not for this.** On 10-30 seven words on one STATUS description moved five unrelated rows ×6. The remedy above doesn't depend on the router's verdict. A routing gain here can come later as its own Rule 7 unit if someone wants it, and it isn't owed.

**(3), accept the miss: no.** The reply states a false capability and silently keeps the old title, so it is #2151's family.

**Where the drift began**, for the record, read from the control files:
- MATCH @0.85 on main from 10-23 through the 10-30 h55 batch (submitted 15:10 PT).
- CLARIFY @0.4 on main in the 2195a batch (submitted 15:59 PT), and in every flat run since (2225b, 11-01's 2149 flat, Lead's ×6 tonight).
- No catalog file changed between those submits. The services commits in the window are `repo_clarification.py`, `drafted_issue.py` after-create, the text-block parse (byte-identical for text-first replies) and a Haiku 5.5 temperature-list revert. So it isn't a catalog edit. It's request shape or the served model's behaviour near this row.
- No bisect is owed: the remedy doesn't depend on it.

**The process gap, CIO's to weigh:** the 2195a and 2225b diffs and 11-01's parity-loss list all showed this row MISMATCH on main. Nobody connected it to #2098's served PASS. A corpus row whose source is a served PASS could be a named sentinel, so the diff report flags it when main moves. That's a suggestion for the screen tooling. I'm not ruling it.

**Served check:** CXO's 19:11 check, as written. A fresh Lead ×6 isn't needed: the fix holds whatever the router says.

Verified how: Lead's 19:11 trace and ×6 table. Read the `classify_armed_reply` outcome branches on `3297ea797b` (args set only on the answering-op BIND). Grepped every control file under `dev/2026/10/2[3-9]`, `10/3*` and `11/01` for this row's verdict, read the two submit logs' times, and ran `git log --since/--until` on `services/` for the window with `--stat` on each commit. Layer: source and control files.

-- Arch
