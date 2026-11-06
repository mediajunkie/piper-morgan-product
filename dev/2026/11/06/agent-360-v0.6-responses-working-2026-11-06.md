# Agent 360 v0.6: working extraction (HOST), started 2026-11-06

Responses extracted from the memo text as they land. Claims about another role are checked against that role's logs before the synthesis (procedure step 5). Not a synthesis.

## Coverage
| Seat | Filed | Depth |
|---|---|---|
| ppm | 2026-11-06 05:15 (plus correction 05:17) | one week of logs, 10-30 to 11-05; says so |

## PPM (response and correction)
- **Correction first:** PPM's 2.3 and 8.1 ("roadmap.md is a historical record", banner suggestion) are withdrawn by its 05:17 memo. The file was already a pointer document (v19.1, 10-26); only Current Position was stale, now v19.2. Do not use the original 2.3/8.1 text.
- **3.5 (tooling, CIO's call):** `mail-send.sh` stopped on its first attempt with a `cannot lock ref 'refs/remotes/origin/main'` fetch failure and did not retry; its non-fast-forward path retries. Candidate: same retry for the fetch-lock failure. Owner: CIO.
- **5.4 (carried from v0.5):** estimated times ("16:1x") still written; the stamp-check works as a catch, not a habit. HOST has the same slip on 11-05 (my wrap, line 4 of #068).
- **5.6:** gates seen only when handed over; the link checker's red on 11-05 reached PPM by mail.
- **5.7 (new):** the owed scan undercounts for PPM by about eight, since most of its owed items sit in the carry-forward waiting list, not OWED markers. Proposed: one marker per waiting item that names a trigger. Owner: PPM. Cohort-wide question for synthesis: does the scan read the carry-forward?
- **5.8 (new):** two blocks, both platform: the auto-mode classifier refused issue-closing comments (11-02), and #2282 step 4 waits on xian's word for Web's sign-in. No credential case.
- **6.1:** a scoped `gh issue close` rule for PPM, or a named seat that has it. Needs xian. (HOST does not write permission rules for its own seat; this is another seat's, still xian's call.)
- **6.3:** `place-issue.sh` (about six calls per placement, over 25 placements on 11-04 and 11-05). Owner: PPM.
- **8.3 / 9.2:** the invite hold has no single standing document (PPM will draft a PDR; xian ratifies); a fresh-account, no-help session as a gate row before any Go. Both PPM's.
- **Open to check:** PPM's "3.4 wake push reached me at 05:09" matches my own 05:09 wake (same kickoff).
