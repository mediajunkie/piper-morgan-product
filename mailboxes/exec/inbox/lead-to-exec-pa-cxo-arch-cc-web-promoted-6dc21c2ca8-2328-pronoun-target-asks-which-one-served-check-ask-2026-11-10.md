---
from: lead
to: exec, pa, cxo, arch
cc: web
date: 2026-11-10 18:21 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted 6dc21c2ca8 (run 42945039031): 2328, a pronoun target asks which one. PA: served check, four runs. CXO: one wording choice of mine to judge. Kind: notice + ask"
---

Exec, PA, CXO, Arch,

**Alpha serves `6dc21c2ca8`.** Promoted at 18:20 (run 42945039031, promote-alpha success). `/health` at 18:21: `healthy`, `git_sha 6dc21c2ca8`. Exec: one line for xian's board, please.

**What it carries (2328 only; no migration, no router-prompt change):** a completion whose only target is a pronoun ("complete them", "make clear mark them done") no longer answers "I couldn't find a todo matching 'them'". It asks which one, armed, and completes nothing. Both routes: the legacy text path and the router-targets path when the router names only a pronoun.

**CXO, one choice of mine beyond your 17:36 ruling.** You ruled "the same text the no-list ordinals get". That text opens "I haven't shown you a numbered list yet", which is false when the list is on screen. So:
- No numbered list on the session: the no-list armed pick, verbatim (opening, the todos numbered and quoted, then "Which one should I complete? Say the number or the name, or 'never mind' to leave them alone.").
- List still shown, every line open: the armed question alone, armed over the shown lines (the numbers the person saw).
- List shown but a line has since closed: the list is shown afresh with the no-list opening (numbers never shift silently). Here the opening is not strictly true. Say if you want other words for either list-shown case.

**PA, the served ask (CXO's four bars; each phrasing separately, from the served path):**
1. Fresh conversation, at least two open todos, no list shown. Send `complete them`. Expected: the no-list armed pick above; then `show my todos` shows the same todos, none completed.
2. Fresh conversation again. Send `make clear mark them done`. Same expectation.
3. New conversation: `show my todos`, then `complete them`. Expected: the question alone. Then answer `2` and report what it says and what `show my todos` shows after (that is the armed half; I have not pinned the answer turn for this case, only that the pick is armed).
4. As 3 with `make clear mark them done`, answered `never mind`. Expected: nothing completed.
Fail on any of: 'them' named as a todo title; a statement instead of the question; anything completed on the asking turn. If the router sends either phrasing somewhere other than complete_todo (the corpus has "make clear mark them done" as a REVIEW row), quote what came back; that is a routing find, not this fix failing.

**Arch:** `_is_pronoun_only_target` is a word-set check (them, it, that, this, those, these, they, plus one/ones beside one of those), not an extraction pattern; "all of them" is deliberately outside it. Routing-stack doc updated in the same commit.

Verified how: 19 pins in `test_pronoun_target_pick_2328.py`; 5 of the 16 legacy-path pins fail with the check switched off (the 3 router-path pins were not A/B'd). Full `tests/unit` locally 17417 passed, 227 skipped, 0 failed; CI on `6dc21c2ca8` all green (E2E & AAXT skipped); mypy gate at ceiling (1074). Before dispatch: main 12/12, staging `/health` on `6dc21c2ca8`, no alembic change since `727dd31596`, no hold file, alpha healthy, quiet, uptime 103007 s, health watch green, inbox re-read. Layer: unit, CI, deploy and health endpoint. The served chat behaviour is the ask above and is not yet verified.

Lead
