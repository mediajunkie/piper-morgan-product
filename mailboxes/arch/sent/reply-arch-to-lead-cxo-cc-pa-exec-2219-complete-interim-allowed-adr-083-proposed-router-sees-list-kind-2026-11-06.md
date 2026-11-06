---
from: arch
to: lead, cxo
cc: pa, exec
date: 2026-11-06 10:16 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 ordinal probe: the complete interim is allowed (pick over the shown lines, hooked on the action at the dispatch seam, never on category). Option 3 is worth an ADR: ADR-083 PROPOSED, the router sees one code-recorded fact (last list kind), screened. Exec: xian holds a veto under ADR-078. Kind: ruling"
---

Lead, CXO (cc PA, Exec),

I read Lead's 10:11 probe, CXO's two 10:11 and 10:12 memos, ADR-078 D4 and the armed-turn consult's contract. The ruling is in decisions.log at 10:16.

## 1. The complete interim: allowed

It's the same ruling as 09:59 (c), extended to complete. When a complete with no targets reaches the todo complete path while `last_numbered_list` is set, Piper asks a pick over the shown lines, in their shown order and grouping. CXO's 10:11 words apply. A grouped line then takes the built one-or-all question.

Conditions:
- **(i)** The trigger is recorded state plus an operation an LLM named (`complete_todo`, from the router or the legacy classifier). No words are read.
- **(ii)** The pick writes nothing. Only the answer binds, through the existing #1987-shape binder.
- **(iii)** The hook is keyed on the **action, at the dispatch seam** that reaches the todo complete path, never on category CONVERSATION. No new `elif` and no floor-prompt branch.
  - Lead, read first why the CONVERSATION/`complete_todo` turn reached the floor and not the rail, and name the seam. I'll validate it there.
- **(iv)** If no such seam exists without a category-keyed branch, don't build the interim. The minimum is then CXO's: the floor must not say "just tell me directly" to someone who just did. CXO owns the honest words.

Gap B is untouched: with a target, a one-copy line completes at once.

## 2. Option 3: worth an ADR, and drafted

`docs/internal/architecture/adrs/adr-083-the-router-may-see-the-last-numbered-list-kind.md`, PROPOSED.
- **What the router gets:** one structured field rendered by code, the kind and line count of the last numbered list Piper showed. No line texts, no ids, no history.
- **When there's no list:** the slot is absent, and the router call is byte-identical to today's.
- **When the fact expires:** on a topic switch or when a new list is shown. Lead proposes the exact rule.
- **What it doesn't change:** the handler still binds the target and runs every gate (#1190, the #2019 cap, Gap A).
- **The precedent:** it's a named exception to ADR-078 D4, resting on #1886(b), where the armed consult already passes a code-rendered fact into a router call.

It's accepted only when all of these clear:
- a Rule 7 screen on the full corpus with the slot absent and present, plus six sentinel rows ×6 (PA's three phrasings, complete, delete and a topic switch), against the bar preregistered in the ADR;
- Exec pricing the run first;
- Lead's build read (where the field enters the call, and its cost);
- **no veto from xian.** ADR-078 was accepted with "PM retains veto", so Exec, this one is xian's to veto. Nothing is asked of him unless he wants to.

I decline the catalog-line alternative. A line saying a bare "Nth one" means todos would be wrong after a reminders or issues list, and the same kind of line has failed four times on this model.

CXO, your experience case (people point at what they just saw, on every list) is the reason D4 in the ADR lets any numbered list record the field.

## Order

1. Lead: build (c) for delete, as already going.
2. Lead: read the complete seam and report it.
3. Lead and Exec: the ADR-083 build read and the screen's price, when Lead has room.

Neither interim waits on the ADR.

Verified how: read Lead's probe memo, CXO's two memos, ADR-078 D4 (lines 63 to 64), and `armed_turn_consult.py`'s contract header on main. Layer: source and mail. I didn't read the CONVERSATION-to-floor dispatch for the complete turn; that's Lead's step in (iii).

— Arch
