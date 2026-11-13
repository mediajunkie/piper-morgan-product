# Public-beta gate: Lead's sizes for the unsized rows (2026-11-12)

**For:** PPM's estimate of when the gate closes (mail of 11-12, PDR-009), in answer to xian's question. These are sizes, not dates. The go date is xian's.

**Unit:** a Lead-day is one seat-day of build, the full landing gate, Arch's validation and the served check, as on the 10-31 page (`first-production-sprint-sizes-lead-2026-10-31.md`).

**Confidence marks:** (d) means the size is for the build after a decision or design that is not Lead's. (o) means most of the row is operations or another seat's work, and the size is Lead's part only.

**What I read:** each issue's body and its latest comment, this fire. I did not read the linked issues (#1352, #1383, #1232, #651, #336, the owner-id inventory issues) or re-measure the code, except where a line says so. Every number is an estimate.

## The rows

| Row | Issue | Lead size | What it rests on, and what it waits for |
|---|---|---|---|
| G6 | #1441 Calendar: full port to the connector contract | 4–6 days | The GitHub port is the pattern. It subsumes #1352 and #1383, moves the stored Calendar grant onto user-scoped names (a data move, so a promotion with care), fixes one adapter logging defect, and needs a two-user isolation test and a scenario turn. The swing is the stored-name move. #1706 (MCP increment 7) waits on this. |
| G3 | #2158 Account deletion in product, with a real purge and a deletion record outside the snapshot | 3–5 days (d) | `scripts/erase_user.py` already plans the purge table by table (an operator script, 931 lines), so the product route reuses it. New: the confirm step (CXO's words, Web's page), purging soft-deleted rows such as insights, and the deletion record kept outside the database. Where that record lives is Arch's and HOST's decision and is not made. |
| G3 | #2159 Export everything Piper holds for a user | 3–4 days | One bundle builder read against the same table plan as deletion, a route, and a test that every owner table is in the bundle or excluded with a reason. A pin that no credential or ciphertext is in it. Large accounts may need the bundle built in the background; that is the top of the range. |
| G3 | #2160 Support intake | 1–1.5 days (d)(o) | The owner, queue and response window are Exec's and xian's. Lead's part is the feedback form reaching that queue with enough context, and CXO's lines after Send (her words exist, 10-24). Which queue is not decided. |
| G3 | #2062 Terms: every commitment mapped to a mechanism | 0.5–1.5 days (d)(o) | The plain layer is xian's, the legal layer counsel's, the page Comms' and Web's. Lead's part is checking the map row by row and adding a pin where a commitment has none. The count of missing pins is unknown until the plain layer exists; I've allowed for two. |
| G7 | #2157 Backups, retention, one timed restore drill, key custody, HA decision | 1.5–2.5 days (d)(o) | The decisions and the drill run are HOST's and xian's (no seat runs `fly`). Lead's part is the drill as one command xian runs, on the pattern of the cutover sitting: restore to a copy, boot, check a stored key decrypts (`scripts/verify_stored_credential_decrypt.py` exists), re-apply deletions, destroy the copy and check it. Re-applying deletions needs #2158's record first. HOST's drill design is not written. |
| G7 | #2162 Staging for destructive tests and rehearsal | 1.5–2 days (o) | The staging app exists and has had its own master key since 10-22 (the issue's text). Missing in the code I searched: a synthetic seed script and the banner (no "Staging site" string under `templates/`, `web/` page code or `services/`). The secrets comparison is HOST's read and xian's. |
| G4 | #2164 Waiting list with batch admission | 0–1 day (o) | The list lives in Buttondown (xian, 11-03), outside Piper. Admission uses the existing invite path. Lead's part, if wanted, is a helper that mints a wave's codes for HOST. The served rows are HOST's, Comms' and xian's. |
| G7 | A pause switch for admission waves (not filed) | 1–1.5 days (d) | Not specified. If it means "new accounts stop being created, with CXO's line, until the operator turns it back on", it is an operator setting read at create-account. A setting xian flips on the host is 1 day; a switch on an admin page, stored in the database, is 1.5. Needs filing and a ruling on which. |
| G7 | #2345 GitHub and Calendar connect state in Redis | 1–1.5 days | Slack's nonce handling is the pattern (Arch's ruling of 10-28). Both starts for Calendar. I filed this one today; deferred until the #2342 sitting has run, because it changes the connect path the sitting exercises. |
| G7 | #2350 Evidence log lines kept at INFO on the hosts | 0.5–1 day | A named logger and `LOG_LEVEL` (Arch filed it today). The served check is a read of host logs, which is PA's or xian's. Same deferral as #2345. |

## The G5 set (false answers on the first-run paths)

Three of these five were sized on 10-31, and their state has moved since.

| Issue | Lead size | State |
|---|---|---|
| #2183 a count is ignored | 0 build | The fix is on main (`b2b928ee46`, 10-28). It closes on its served check. |
| #2185 "261 open issues" | 0 build | Both halves are on main and the sort was read served on alpha (10-28 comment). It needs the close with evidence, about half an hour. |
| #2209 a milestone the account doesn't have | 0 build | Arch validated the fix on main (10-30). Served check, then close. |
| #2186 unit 2, declared argument keys in the router grammar | 1–2 days | As sized on 10-31. It is a router-prompt change, so it needs a rule-7 screen, and those are stopped until xian supplies a provider key (Exec, 11-11). Blocked on that, not on build. |
| #2184 a read that lists one milestone's issues | 1.5–2 days (d) | Arch changed the design on 11-01: the handler resolves the milestone with its own LLM call over titles code read, and code binds only to a read title. That is larger than the 1 day of 10-31. Its tests need model calls, so the same provider-key question applies. |

## Totals

- All rows above: about **20 to 32 Lead-days**.
- Of that, the three rows with no decision dependency and the most build are #1441 (4–6), #2159 (3–4) and #2158 (3–5, after the record's home is decided).
- About 6 to 10 of the days sit behind a decision someone else owns: the deletion record's home, the queue for support, HOST's drill design, the pause switch's meaning, the provider key.

Added to PPM's figure for the ten rows already sized (13 to 21.5 Lead-days), the gate's build is roughly **33 to 53 Lead-days**. At about 7 Lead-days a sprint that is 5 to 8 sprints of Lead time if every row is serial and all of it is Lead's. It is neither: about a third is marked (o), and independent units run two at a time.

## What would shorten it

1. **Decide the deletion record's home** (Arch, HOST). #2158 and #2157's drill both wait on it.
2. **A provider key for rule-7 screens** (xian). #2186 unit 2 and #2184 cannot land without one.
3. **File and rule the pause switch** (PPM, Arch).
4. **HOST's drill design** for #2157, so the one-command drill can be built while the Terms are written.

Verified how: `gh issue view` on #1441, #2158, #2159, #2160, #2062, #2157, #2162, #2164, #2345, #2350, #2183, #2184, #2185, #2186 and #2209 this fire (15 of the 15 filed rows PPM named; the pause switch has no issue), each body and its last comment; `wc -l scripts/erase_user.py`; a search for "Staging site" and for seed scripts. No code was measured beyond that.
