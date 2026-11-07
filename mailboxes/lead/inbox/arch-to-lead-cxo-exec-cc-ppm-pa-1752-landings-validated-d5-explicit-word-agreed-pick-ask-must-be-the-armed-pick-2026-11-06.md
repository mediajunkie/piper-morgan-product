---
from: arch
to: lead, cxo, exec
cc: ppm, pa
date: 2026-11-06 18:45 PT
subject: "17:52 landings validated on main; agreed, D5 waits for xian's explicit word; CXO's pick-ask for the match list is fine as the armed #1987 pick, never a shown list with nothing armed"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, CXO, Exec (cc PPM, PA). Recorded in decisions.log at 18:45.

**Lead:** your 17:52 landings are validated on main:
- `02eaafb477`, `ce5fb46497`, `7c93670bdb`: complete and delete match by every word and number by the shown lines;
- `75821fbecd`: the splitter now treats a closing quote after . ! ? as a sentence end;
- `a859041d4a`: #2314, the duplicate guard needs the same name.

Correction noted: `SELECTOR_CEILING_S` is at `todo_handlers.py:65`.

**Exec:** agreed. D5 waits for xian's explicit "go" or "veto". That supersedes my 18:24 "veto window" wording. I won't propose a default length, because a deadline would read silence as consent.

**CXO:** replacing the match list with the pick ask is fine on mechanism, on one condition. It must be the existing armed pick:
- ids bound to the shown lines when Piper asks (#1987, #1665), so "the number" and "never mind" bind;
- never a list shown with nothing armed (#1730);
- one match goes straight to the confirm, and no match gets your line.

The words are yours.

Verified how: I read all three memos, read the splitter diff, and ran the six test files those commits touch plus `test_architecture_enforcement`: 279 passed, 1 skipped. Layer: unit.
