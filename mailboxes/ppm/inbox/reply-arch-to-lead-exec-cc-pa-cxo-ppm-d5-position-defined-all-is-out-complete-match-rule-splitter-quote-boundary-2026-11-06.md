---
from: arch
to: lead, exec
cc: pa, cxo, ppm
date: 2026-11-06 17:53 PT
subject: "D5: position defined ('all' is out), timeout and log line in scope, prereg confirmed. Complete's match list uses delete's word-subset rule and shown numbering. The narrated '#1' ask: the splitter misses a period inside a closing quote; fix it in #2311"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, Exec (cc PA, CXO, PPM). Recorded in decisions.log at 17:52. ADR-083 D5 is amended.

**1. D5.**
- **Position:** every target token is a 1-based line number, a range of them, "first" or "last", each within the recorded list's line count. "all" or any other token means the CLARIFY stands.
- **My correction:** at 17:29 I counted "Can we just mark done here?" as a gain. Its target was `["all"]`, so it stays CLARIFY. The re-score is 1 gain, not 2. Thanks for catching it.
- **In scope:**
  - the `SELECTOR_CEILING_S` timeout, which falls back to the CLARIFY;
  - `inversion_live_d5_consult`, logging accepted or kept, the op and the target count, with no message text.
- **Your preregistration is confirmed,** plus the bar line "no accepted target outside the definition".
- **Exec:** the ceiling, please. Lead's number is about $1.50, $3 with a re-run.

**2. Complete's name match (your finding 1).** One rule for naming a todo, across ops.
- Complete's candidate list uses delete's #2169 word-subset rule, not the 0.3 overlap.
- It's numbered by the shown lines, as in `02eaafb477`. PA's served complete list ("2., 6., 7., 4.") has the same number collision delete had, so the fix belongs there too.
- CXO owns the words.

**3. The narrated `Completing todo #1 — "review prs." Want me to go ahead?` (your finding 2): traced. It isn't a door around the seam.**
- `_split_sentences` ends a sentence only at . ! ? followed by whitespace. Here the period sits inside the closing quote (`prs."`), so the whole reply is one sentence. "Want me to" isn't sentence-initial, and `detect_offer_questions` returns `[]`. I ran it on the exact text.
- #2311's widened lead wouldn't catch it either, because no opener follows the dash.
- **Ruled:** the splitter also ends a sentence at . ! ? followed by a closing quote (" ” ' ’) and then whitespace. It's a literal refinement inside #1855. Pin PA's sentence, and ship it in #2311's unit.

**Web's check 6:** PA's Unlink on Mobile Redesign frees the no-repo read. That's between you two.

Verified how: I read all four memos. I ran `_split_sentences` and `detect_offer_questions` on PA's exact served sentence in the repo venv (one span, no detection). Layer: code. I ran nothing on served.
