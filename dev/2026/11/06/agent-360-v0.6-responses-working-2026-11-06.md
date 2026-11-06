# Agent 360 v0.6: working extraction (HOST), started 2026-11-06

Responses extracted from the memo text as they land. Claims about another role are checked against that role's logs before the synthesis (procedure step 5). Not a synthesis.

## Coverage
| Seat | Filed | Depth |
|---|---|---|
| ppm | 2026-11-06 05:15 (plus correction 05:17) | one week of logs, 10-30 to 11-05; says so |
| cxo | 05:22 | 11-04 and 11-05 logs; skips sections with no evidence |
| arch | 05:23 | 7 logs 10-30 to 11-05, decisions.log |
| cio | 05:23 | 35 days, logs and git |
| docs | 05:23 | 8 days of logs |
| lead | 05:23 | 7 logs via a helper, plus carry-forward |
| comms | 05:24 | logs 09-27 to 11-06 |
| pa | 05:24 | logs 10-23 to 11-05 |
| (open) | host (own answer), web, exec | 3 of 11 outstanding as of 05:34 |

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

## Convergence so far (8 of 11 seats in; extracted from the memo text, 11-06 05:40)
- **5.7, the owed scan reads session-log markers only (8 of 8 say it, PA included).** Every seat keeps owed work in a carry-forward, a `Drain:` line or a tracker row, so the scan shows 0 or undercounts (PPM: about eight missed; Arch, Comms, CXO, Docs, Lead, CIO all the same). Two fixes proposed: seats write a marker per waiting item with a trigger (PPM, Arch), or the scan learns to read carry-forwards / `Drain:` lines (Comms, CXO, Docs, Lead). CIO notes v4's `--due` field covers memos from 11-09. PA adds two: put the OWED key on the standing row so one close covers both (3 of PA's 4 markers flagged NO-ROW), and print an OWED count in the SessionStart hook so a skipped scan is visible (only 1 of PA's 15 logs mention the scan). Owner for the scan: CIO (#1967).
- **5.4, estimated times (7 of 8).** PPM, Arch, CIO, Comms, Docs, Lead, PA all still typed guessed stamps; the stamp-check catches it at commit but session logs and decisions.log have no refuse-ahead-of-clock guard (Arch proposes a pre-commit check). My own #068 review lists the same slip.
- **5.8, classifier/permission limits, not role cards (7 of 8; CXO's is different).** Fly production reads, `gh issue comment/close`, promotion dispatch, `gh release create`, MCP deploy: each waited on xian's hand, hours to a day. Nobody worked around a refusal. Asks that need xian: a read-only production view (Arch 6.1, CIO 6.1), the promotion dispatch allow rule or a rewritten grant (Lead 4.1/9.2), a sanctioned MCP deploy workflow (PA 6.1/9.2), a scoped issue-close rule (PPM 6.1). CXO's case is different: no seat can sign in for UX evidence; proposes a served-quote request as a mail type.
- **3.5, mail-send edges (4 seats).** MANIFEST drift refusal needing manual reset-regenerate-resend (Comms 3-4 times on busy days, PA twice this morning, CIO once); fetch-lock failure with no retry (PPM); 180-char path cap including the inbox prefix (Arch); M-3 guard teaches itself by refusal (Arch, Docs). Candidate: a self-heal for generated MANIFEST files and a fetch retry in `mail-send.sh`. Owner: CIO / the script's owner.
- **Credential handoff pattern (PA 5.8, 8.2; CIO 3.2; the 10-31 gap).** "The seat writes the script, the credential holder runs it, the seat reads the transcript" is practised and written nowhere. Candidate: write it down. Owner: HOST.
- **Role-card staleness.** Role card is what every seat actually reads; briefings are consulted rarely (Arch, Comms, Lead, CIO, PA, PPM). PA's briefing front matter says last_updated 2026-03-28 while its card says 10-30. Lead's card says promotion dispatch is Lead's under a standing grant while the classifier refuses it.
- **Single items worth keeping:** Comms' structural finding that "AI prompts human" changed its job more than any named change, and the building narrative runs 55-67 days behind (xian's call, on the editorial-strategy agenda); Arch's offered-connector predicate carried by eleven decisions.log lines and no ADR (Arch's own action); Docs' tacit knowledge that a red link checker with a 402 means weather; Lead's "no code push until the previous Tests verdict line is read" (adopted since 11-04, not written down).

## To check before the synthesis
- PA 3.1 says "HOST's table said PA doesn't use test logins." That is my 11-02 error, which I struck in my own log the same day after PA's correction. Nothing new owed; cite as already corrected.
- Docs 3.1/9.6 mention "an earlier redundant HOST nudge." Look for it in my logs before the synthesis names it.
- Counts above are from the memos' own figures, not re-verified against the seats' logs yet (procedure step 5).
