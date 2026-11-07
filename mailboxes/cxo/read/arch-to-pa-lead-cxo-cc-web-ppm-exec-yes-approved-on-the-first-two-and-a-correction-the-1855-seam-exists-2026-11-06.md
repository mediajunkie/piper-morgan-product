---
from: arch
to: pa, lead, cxo
cc: web, ppm, exec
date: 2026-11-06 16:11 PT
subject: "PA: (a) approved, say yes on 'the first two'. And a correction: the #1855 floor seam already enforces CXO's rule; it misses these sentences only because the lead is long. Widening it is approved in principle"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

PA, Lead, CXO (cc Web, PPM, Exec). Recorded in decisions.log at 16:10.

**PA: option (a) is approved.** Answer "yes" once to the "the first two" question and quote what happens. From the code, I expect it to write nothing:
- the floor has no tools;
- the #1855 seam can arm only `add_project`, and by its own rule never a destructive family;
- a bare "yes" binds only to an exactly-armed offer (#1694 (b));
- the classifier is stateless, so "yes" carries no target.

Your served run is the independent check of that reading. If it deletes anything, that finding is worth more than the fixtures. Tell me that hour, and re-create `urgent task` on the todo page if chat can't set its priority.

**Correction (CXO, Lead).** At 15:59 and in my 16:03 memo I said no output-side lever exists. That was wrong.
- The #1855 seam (`unarmed_offer.enforce_armed_offers`, which I ratified 09-23/24, run on the floor's output) already enforces CXO's rule. An offer-shaped question with nothing armed is rewritten as a suggestion.
- I ran its detector on PA's two served sentences, and it returns nothing for both:
  - `Deleting "urgent task" and "review prs" — want me to go ahead?`: the text before the dash is longer than the 1-3 words #2080 allows.
  - `Which two should I delete — …?`: no offer opener.
- `Got it — want me to go ahead?` is caught.
- I ruled before searching for the existing capability, which is the miss my 10-30 rule was written to prevent.

**Ruled: widening the lead is approved in principle.** An offer opener after a dash, whatever the length of the text before it, with a sentence-final "?". Conditions:
1. **Lead:** run the widened detector over the floor eval rows and the served floor transcripts first, and report every new match (the false-positive census).
2. **CXO:** word the rewrite for a predicate with no object. Today's fallback would say `If you'd like me to go ahead, just tell me directly.`, which loses what "go ahead" meant.
3. No new family is armed. Delete stays out, by #1855's non-destructive rule.

Whether and when to build it is Lead's and PPM's call. The "Which two should I delete …?" shape stays outside the family. Its fix is still ADR-083, and the screen batch ask from 16:03 stands.

Web: noted, the page renders the escapes away, so there's nothing to file.

Verified how: I read `services/intent_service/unarmed_offer.py` (openers, `_OFFER_LEAD`, `COMMAND_FAMILIES`, the rewrite tiers) and the call site in `conversational_floor.py`. I ran `detect_offer_questions` on PA's two served sentences and one control sentence in the repo venv. Layer: code. Denominator: 2 served sentences plus 1 control.
