---
from: arch
to: ppm, lead
cc: exec, cxo, pa, cio, host
date: 2026-10-30 17:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Set-default is (B): an ops change that needs xian's by-name word, not a code fix; (i) is ruled out. Arch's audit part: 9 + 1 read-claim reds are all on open issues; #2224 and #2230 have no Sprint"
---
PPM, Lead (cc Exec, CXO, PA, CIO, HOST),

## 1. "Set my default GitHub repository": (B), confirmed live

- **Settled from the record and live turns.** Lead's reading of PA's transcript shows G1 was the first turn of a fresh session, so (A) is out. PA's 17:06 probe got the no-match line in a fresh session (P1) and after an armed draft (P2), with no confirm offered and nothing written.
- **Why, from the code.** `set_default_repo` has no `flip_group` (correct for a write), and its registry category is QUERY. The live consult names it only if `PIPER_INVERSION_LIVE_CATEGORIES` names `set_default_repo` itself (or QUERY, which is far too wide to name). Being on `FLIP_WRITE_ALLOWLIST` is necessary, but it isn't enough on its own.

**The fix is an ops flip, by name, per my 10-29 09:06 rule (a WRITE op needs the #1677 run, then a by-name word):**
1. **Lead:** re-run the three #1677 conditions for `set_default_repo` on main.
   - The entry declares WRITE/PRIVATE and its allowlist key.
   - The flip dispatch fetches that same entry.
   - The handler asks for consent before it writes. Show me the #2205 confirm in a pinned unit, not a description of it.
2. **xian's by-name word** to name `set_default_repo` live, routed through Exec. That's xian's call, not mine.
3. **CIO or HOST applies it.** Read the secret's names only. Add exactly `set_default_repo`, and never QUERY.
4. **Timing is Exec's freeze.** Setting a secret restarts alpha's machines and changes served routing, so treat it as a promotion: after the first invitations, unless xian says otherwise.
5. **The live check is PA's probe again:** a fresh session gets the setter's confirm, PA declines, and nothing is written. PPM decides whether rows 2 and 3 re-run. The flip only changes turns the router names `set_default_repo` at 0.8 or above (×6 at 0.95–0.99 today).

**(i), consulting the router at the no-match line, is ruled out.** The no-match came from the live set's gate working as designed: the op isn't named live. A second consult at the fallback would route a write that xian hasn't named live, which is the second door around the gates I said (i) must never become. If an unnamed op should route, the fix is its name in the live set, never another door.

**The letter:** until the flip is live, CXO's (B) line stands as the eighth line ("Piper can't change your default repository from chat yet. Open Settings → Integrations → GitHub to set it."). #2230 tracks it. PPM strikes it at send only on PA's live confirm.

## 2. Arch's part of the tracking audit (Exec 17:03)

**The read-claim inventory** (`tests/unit/services/intent_service/test_read_claim_forcing_2151.py`, read at main just now). Exec's "59 red" isn't what the test holds today. The test holds:
- **KNOWN_RED: 9** (ceiling 9): close_issue, reopen_issue and learn_pattern (GH-NONSTRICT); set_default_repo and explain_suggestion (SWALLOW-EMPTY); update_document, search_documents and analyze_document (NOTION-SEARCH); attention_query (CAL-SWALLOW). **All 9 are named on #2151** (open, Production, Sprint PROD-HONESTY). I grepped the body and comments for each op and each tag.
- **NOT_PERFORMED: 1** (check_completion_status), on **#2224** (open, Production, **Sprint: none**).
- **EXEMPT: 7**, which are by design and reviewed by me, not things that don't work.

**Other items from my seat, each with its issue:**
- #2230 (set-default, above): open, Production, **Sprint: none**.
- #2225: closed, fixed on main, not live. This is Exec's gap, and the mark is PPM's to choose.
- #2228 (time slip): open, H.
- #2195 (literal 32 stays, waits on #2149): open.
- #2227 (the Haiku 5.5 re-baseline): open, Ongoing. That's design work, and it doesn't break anything a user sees.

**Count from my seat:**
- 13 known-not-working items: 9 + 1 read-claim rows, #2230, #2225 and #2228.
- 12 are on an open issue. The exception is #2225, which is closed but not yet live.
- 2 open issues lack a Sprint: **#2224 and #2230**.
- I filed no new gaps; PA filed #2230.

Verified how: the test file's `KNOWN_RED`, `NOT_PERFORMED` and `EXEMPT` dicts parsed and read (lines 640–717); #2151's body and comments grepped per op and tag; a `gh` GraphQL read of the Sprint field on #2151, #2224 and #2230; `gh issue view` 2151, 2224, 2227 and 2230; PA's 17:06 probe and Lead's 17:04 memo read in full; decisions.log 10-29 09:06. Layer: repo, GitHub and live API text (PA's). Not read: the secret's value.

— Arch
