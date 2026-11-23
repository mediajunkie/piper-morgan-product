# Mail v4 review (2026-11-23)

**Reviewer**: CIO (mechanism owner). **Written**: 2026-11-23, from the 10:07 START (clock read `10:07`). **Window**: the two weeks after the widening, 2026-11-09 00:00 to 11-23 00:00 Pacific; R16's follow-up uses 11-11 to 11-23. **Inputs**: `scripts/mail4.py` (`check`, `stats`, and its own functions over `piper-morgan-mail` origin/main), `scripts/memo-volume.py`, `git log` over this repo's origin/main, and a script over each v3 memo's `from:`, `to:` and `cc:`. **Terms reviewed**: the 11-05 review's widening terms (xian's yes, 11-05 10:47) and the pilot's success and stop criteria (`docs/internal/operations/mail-v4-pilot.md`).

## Verdict

v4 is now the cohort's mail. In the two weeks after the widening it carried 1,743 messages, and v3 carried 128, mostly from agents outside this repo. The `mail(` share of main's commits fell from 30.7% to 3.1%, which is the routing cost xian asked about. Daily self-tests passed 77 of 77 seat-days last week. No stop criterion fired.

**Recommendation: end the v3 fallback today, as the approved terms say,** for mail between seats in this repo. v3's `mailboxes/` stays for what v4 can't carry: agents outside this repo (Pard, Janus, Dispatch, Themis), Spec, and Exec's Ship kickoff until it moves (finding 2). Nothing here needs xian. The terms he approved on 11-05 already set the end date.

## What the window shows

| Measure | Result | Verified how |
|---|---|---|
| Traffic, 11-09 to 11-23 | **v4 1,743 messages, v3 128 memos.** v4: Lead 386, Arch 357, CIO 210, CXO 174, Exec 152. v3: Janus 24, Pard 23, Lead 22 | `memo-volume.py 2026-11-09 2026-11-23` |
| Routing cost on main (the criterion added 11-05) | **`mail(` commits: 242 of 7,799, 3.1%,** against 3,005 of 9,787 (30.7%) in the 10-22 to 11-05 window. The same count without merge commits gives 4.9% against 39.9% | `git log origin/main` over each window, with and without `--no-merges`, subjects starting `mail(` |
| R16 follow-up: v4's share of mail where every participant is a v4 seat, 11-11 to 11-23 | **1,740 v4 against 28 v3, so v4 carries 98.4%** (11-09 to 11-10: 3 of 52). By day the 28 are 19 on 11-11, 8 on 11-13 (Ship 069's workstream reviews), and 1 on 11-20 (Ship 070's kickoff). Since 11-13 the only one is the scripted kickoff | `memo-volume.py 2026-11-11 2026-11-23`; a script over the 75 v3 memos added in the window |
| Daily canaries, 11-16 to 11-22 | **77 of 77 seat-days, all acked.** Every one of the 11 seats ran one every day | `mail4.all_messages`, canary type, per sender per day |
| Required-ack mail overdue | **10, all flagged by `check`.** CXO 9 (7.7 to 1.0 days; mostly Lead's grant and validation requests where CXO is cc), Web 1 (CIO's 11-22 step-4 ask, acted on in the work but not acked) | `mail4.py check` at START |
| Ack rates, required-ack since 11-09 | Arch 196 of 196, Lead 103 of 103, Web 53 of 55, **CXO 107 of 124** (to: 60 of 64; cc: 47 of 60) | `mail4.acks` against each message's recipients |
| Files per message | 1 by construction (1,888 messages; `messages/` commits 2,121, acks 6,217) | `mail4.py stats` |
| Stop criteria | **Neither fired.** No overdue decision request went unflagged (all 10 are in `check`). No false all-clear was seen | `check`'s list read against the ack logs |

## Findings

1. **CXO's acks lag** (9 overdue; 17 required-ack messages unacked since 11-09). CXO is reading (7 of 7 canaries) and acting: the grant and validation threads moved. The gap is the ack, mostly on cc'd messages. It is not a delivery failure, and `check` shows it, but an unacked decision request looks the same as an unread one. Ask: CXO acks or declines the 9 in one pass, and acks cc'd decision requests as `read`.
2. **The Ship pipeline still has v3 parts.** `scripts/ship-kickoff.sh` sends the kickoff on v3 and keys its once-only check on `mailboxes/exec/sent/`. It already counts v4 replies (Exec, `ca5c21ebc3`). The `draft-weekly-ship` skill still gates on "6 of 6 memos in `mailboxes/exec/inbox/`", and all eleven Ship 070 reviews went on v4 (11-20 05:12 to 05:15), so that gate as written reads 0 of 6. Ship 070 is due this week. Owner: Exec for the script; the skill's owner for its gate.
3. **The ADR-084 D6 warning in `mail4.py send` is noisy** (9t item 5's count). Of 65 ruling-relays since it went live (11-16 17:00), it fires on 7: 3 right (a step put on xian with no standing access named) and 4 wrong ("his console screenshots", "xian's own edits", "2364's runs", "a standing word"). Reading the 26 relays that mention xian found 2 misses, both "that step is xian's". It only warns and Exec makes the real check, so no harm, but at 3 in 7 a sender learns to ignore it. **Tightened today:** the verb must follow "xian" (not "xian's") within three words, and "that step is xian's" and "needs xian" now count. On the same 65 relays it fires 6 times: the 3 right ones, the 2 misses, and Comms's "if that step needs xian, route it through Exec" (borderline, since it is conditional). None of the 4 false ones fire. Tests: 19 pass, 7 of them added from these cases.
4. **One slow read.** During this START a `mail4.py read` sat for over 120 s, and I stopped it; the next calls were normal. One observation, cause unknown. If it recurs, look at the fetch.
5. **Usage friction seen:** `--cc` takes roles separated by spaces; a single quoted string is refused (CIO, 11-22). The refusal says why, so nothing to fix.

## What changes now (CIO's, unless named)

- `docs/internal/operations/mail-v4-pilot.md`: the fallback is ended for in-repo seat-to-seat mail from 11-23, and what still uses `mailboxes/` is listed.
- `mail-send.sh`'s v4 route hint stays a warning for now. It turns into a refusal for all-v4-participant memos once the Ship kickoff is on v4 (finding 2), so the script isn't broken by it. Trigger: Exec's word that the kickoff moved.
- D6 pattern tightened (finding 3): done, `scripts/mail4.py` and `tests/unit/scripts/test_mail4_d6_warning.py`.
- Mail to CXO (finding 1) and Exec (this review, finding 2).

## What this review does not measure

- Whether a v4 message was acted on well. No 20-message audit was run for this window. Exec ran the earlier two. An ack is a seat's claim, not proof.
- Inbox read cost in seconds, beyond the one slow read.
- v4 beyond this repo. Before it widens to Design in Product, `mail4.py` needs one fetch shared across roles for Pard's watcher (the 11-05 cost note). Not built.
