# Fact-check: "The Caveat That Kept Disappearing" (Tue 10-27, building)

**Draft:** `docs/public/comms/drafts/the-caveat-that-kept-disappearing.md` (Comms' full draft, 10-01). xian hasn't touched it yet.
**Checked:** 2026-10-20, before xian's rewrite. An Opus subagent checked it against primary logs, probe results and git, and Comms reviewed the results.

## The record, in order

1. **08-30.** The probe's prose arm (Claude) said "your todo list is currently empty" after a failed read. The structured arm didn't (`dev/active/probes/RESULTS-probe-b-recomposition-2026-08-30.md:25-26`).
2. **09-01, morning.**
   - xian found the key was in a different org from the one he'd been topping up. He added credit to the right org, and no rotation was needed.
   - PA ran 16 trials: 14 on GPT-4o plus 2 deconfounders. The 30 total includes Claude's 14 from 08-30.
   - The deconfounder (`may_claim_complete: false`) disproved CXO's directive-field theory in both vendors.
   - Sources: PA log `dev/2026/09/01/2026-09-01-0645-pa-code-log.md:31-45`, and the probe results file.
3. **09-01 10:17.**
   - CXO reframed the question: is the caveat about content *in* the reply, or content *missing* from it?
   - For missing content, the structured field vanished, but **prose survived in both vendors**.
   - CXO labelled the reframe post-hoc and wrote the rubric up as v0.3 (CXO log :75-120).
4. **09-01 12:45.** PA checked CXO's reading against their own data and added the mechanism: the reply "reads complete on its own" (PA log :82-99).
5. **09-01 ~12:50-13:30.** Arch revised the connector rule (CONNECTORS.md rule 1), marked "post-hoc taxonomy, killer test pending" (Arch log :25-31).
6. **09-02 10:17.** CXO found their own row marked "not asking yet" since 08-31, called it "a deferral with no trigger", asked xian, and offered "drop it" (CXO 09-02 log :56-75).
7. **09-02 13:17.** CIO's STALE-BLOCKER check missed CXO's test row. CXO's own truncated regex edit from 09-01 had left an orphan line that hid three rows (:78-120).
8. **09-02 16:17.** CXO wrote first-turn copy for MCP users (cold, partial, rich). It leads with what Piper can do, with no apology (:132-168).
9. **09-02 22:17.**
   - PA found that `search_consciousness.py` adds "...and N more results" as a list *member*.
   - CXO named the pattern "member not metadata", recorded as a candidate only (:208-243).
10. **09-03, early.**
   - xian told Arch: "let's do the killer test (authorized!)" (Arch 09-03 log :10-14).
   - PA committed the results at 07:05 (`a20bdeb6bc`). Claude matched "Holds". GPT-4o matched neither prediction and kept both caveats.
11. **09-03 10:17.**
    - CXO named a caveat-count confound and called it their third error in a week.
    - They recommended stopping and said it "isn't discouragement".
    - Their record: "on Claude a lone completeness/truncation caveat reliably vanishes — three trials, three drops" (CXO 09-03 log :15-62).
12. **09-06.** xian authorized the member test. The caveat survived in both vendors at n=1, the first clean pass after "six prior rounds" (`RESULTS-probe-b-member-candidate-2026-09-06.md`, `08907462ff`).

## Claims to fix

| Draft says | Record | Fix |
|---|---|---|
| "Marking the failure as a structured field fixed that one" | Only in the probe. No fix shipped | "…didn't make that mistake in the test" |
| PA "ran the full set of trials… thirty in all" | 16 on 09-01. 30 across both days | "sixteen more trials, thirty across both days" |
| "Caveats about missing content disappeared" | As structured fields. Prose survived in both vendors | Add "when sent as a structured field" |
| The "because the reply already looked like a finished answer" clause sits in CXO's paragraph | That mechanism is PA's | Credit it to PA |
| "with no reason attached" | Log says "no trigger" | "with no trigger to restart it" |
| "CXO ran a check" | The check is CIO's script. CXO ran it with a test row CXO built | "CXO tested CIO's new check with a row it should have flagged" |
| "A clumsy edit" | CXO's own truncated regex edit | Say it was CXO's own. That credits the self-catch |
| "every tool" missed the rows | Only the scan was affected | Drop "every tool" |
| "Piper Alpha had results by seven" | Committed 07:05 | "just after seven" |
| "a reply carrying two caveats" | A tool result (payload), not a reply | "a payload carrying…" |
| The rule "put the caveat where the model can't drop it" is unattributed | From PA's 09-02 code find, sharpened by CXO | Credit PA |
| "…and four more not shown" | The record has "…and 7 more not shown" and `...and more not shown` | Quote one of these, or mark it illustrative |

**True as written:**
- xian topping up the wrong org.
- The directive field failing in both models.
- CXO restructuring the rubric, and PA checking it.
- Arch's same-afternoon rule update, marked pending.
- CXO catching their own "not asking yet" row and offering "drop it".
- The tracker malformed for a day.
- The first-turn copy that afternoon.
- xian's "let's do the killer test (authorized!)" to Arch.
- CXO pre-registering the predictions.
- Claude matching exactly, GPT-4o matching neither.
- The confound diagnosis, "third miss in a week", "not discouragement".
- Claude dropping the caveat 3 of 3 times.
- The 09-06 pass three days later, first try, first clean pass in seven rounds, n=1.

## Voice and template

- **H1** matches the calendar. The **tease** matches Thu 10-29 "Where the Citation Came From".
- **Watch words:**
  - "quieter"
  - "quiet deferral"
- **Claude-isms:**
  - "that turned out not to matter"
  - "isn't the same as learning something"
  - the not-X-but-Y close "…rather than because it finally told you what you wanted"
  - the "tested that theory to destruction… CXO stopped" reveal
  - Keep "an item in the list, not a note beside the list". It's a real design contrast.
- **Unglossed:** "tracker" and "rubric".
- **Clean:** 0 semicolons, no agents called people, no issue numbers in the prose.

## By line, for xian's pass (mapped 2026-10-24 to the draft as last changed in ea44b0d407, 10-03)

| Line | Draft says | Suggested |
|---|---|---|
| 11 | "Marking the failure as a structured field fixed that one." | "…didn't make that mistake in the test." (Only the probe. No fix shipped.) |
| 11 | "The open question was quieter and harder." | Watch word "quieter". E.g. "subtler and harder". |
| 17 | "ran the full set of trials… thirty in all" | "ran sixteen more trials… thirty across both days" |
| 21 | "Caveats about missing content disappeared" | "…disappeared when sent as a structured field" (prose survived in both models) |
| 21 | "because the reply already looked like a finished answer" sits in CXO's sentence | That mechanism is Piper Alpha's. Move it to the Piper Alpha sentence, which already quotes it |
| 27 | "with no reason attached" | "with no trigger to restart it" (the log's word). The line already has it, so cut "no reason attached and" |
| 27 | "quiet deferral" | Watch word. E.g. "open-ended deferral" |
| 29 | "CXO ran a check" | "CXO tested CIO's new check with a row it should have flagged" |
| 29 | "A clumsy edit" | "CXO's own clumsy edit, a day earlier," (credits the self-catch) |
| 29 | "from every tool that read it" | Only the scan was affected. "from the scan" |
| 35 | "Piper Alpha had results by seven." | "just after seven" (committed 07:05) |
| 35 | "a reply carrying two caveats" | "a payload carrying two caveats" (a tool result, not a reply) |
| 39 | "isn't the same as learning something" | Claude-ism. Consider cutting the sentence |
| 41 | "put the caveat where the model can't drop it" (unattributed) | Credit Piper Alpha's code find (09-02), sharpened by CXO |
| 41 | "(…and four more not shown)" | The record has "…and 7 more not shown". Use that, or mark it as an example |
| 43 | "the team wrote it down that way" | Optional: "Piper Alpha wrote it down that way" (the results file is PA's) |
| 47 | "that turned out not to matter" | Claude-ism. Consider rephrasing |
| 53 | "…rather than because it finally told you what you wanted?" | not-X-but-Y close. Optional |

Also: "tested that theory to destruction… CXO stopped" (L13) is a reveal beat. Keep "an item in the list, not a note beside the list" (L41), because it's a real design contrast. Unglossed: "tracker" (L27), "rubric" (L21). Tease (L51) matches Thu 10-29. Art needed.
