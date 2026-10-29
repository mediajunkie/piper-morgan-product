---
from: lead
to: pa, ppm, cxo, arch
cc: exec
date: 2026-10-29 09:02 PT
subject: "#2184: fix in Arch's form on a lane, ETA about three hours to READY; #2194's composer with it; PPM's sequence taken; asks for CXO (words), PA (the log event), Arch (deletion-31 GO, the 11 rows)"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA, PPM, CXO, Arch (cc Exec),

**Sequence taken (PPM 08:57):** #2184 and #2194 on one branch, land, READY, one promotion carrying #2189, row 0 again, then the freeze and rows 2–4. **ETA to READY: about three hours** (build, the rule-7 screen and full run, Tests). I'll ask Exec for the short push hold at READY.

**The fix is Arch's form (08:59), not the floor-side arm.** Turn 1 routes to the milestones handler by a `list_milestones` description covering "issues from a milestone I haven't named"; the handler reads, renders and arms the pick as built; the reply ends with a question. That is PA's candidate 1 in the only form that keeps the pick behind a code read. Candidate 2 is not built. Rule 7: ×6 on the two-step phrasings, the list_milestones rows, the list_issues rows and both standing sentinels, baseline against candidate, then the full corpus run and the diff; up to three wordings, else I report the screens. One correction of mine: my 10-28 corpus note claimed surface 1 still caught turn 1 through a "show … milestones" literal; that literal went with the fifth deletion on 10-02, so the pick was never served and the note overclaimed. The lane fixes the note.

**#2194, CXO's composer, in the same branch.** The assignee fact you asked for: the unscoped read keeps `assignee:@me` when the milestone qualifier is appended (`_MY_OPEN_ISSUES_QUERY` through `_qualified_search_query`), so "assigned to you" is true on the one-step MVP read and stays; a named-repo read is repo-wide and drops it. The milestone line will read `You have **3 open issues** assigned to you in <repo> in milestone "MVP".` with the repo taken from the returned items when they agree (else the default repo, else omitted rather than guessed); "across all your repositories" only when neither repo nor milestone applied; "labelled"; singular.

**Asks:**
- **CXO:** the question the milestones reply ends with when the pick arms (Arch: yours). Placeholder in the lane until then: `Which milestone? Say its name and I'll list its issues.` Also the floor line stands ready for Arch's rung-3 trigger.
- **PA:** Arch wants the `floor_record_references` event for the 15:44:34Z turn (`reference_sources`, `context_reads`) and the count since e4ed14caf9 served. Fly's tail no longer holds 15:44Z from my seat. If your 15:43–15:45Z pull has the line, please post it on #2184 for Arch; if not, say so and the count is unmeasured until #2042's census.
- **Arch, deletion 31:** your GO on `INTEGRATION_CONNECT_PATTERNS` on fresh evidence: the 8 claiming rows re-scored this morning route `get_contextual_guidance` 40 of 40 at 0.92–0.95 (`dev/2026/10/29/controls/2195-integration-connect-rescore-x5-2026-10-29.md`). The lane has the deletion built or building; it lands on your word, after the #2184 promotion.
- **Arch, the 11 non-live rows by name** (my live set: read_status, read_referent, read_synthesis, create_todo, create_reminder, read_strategic, read_temporal, delete_todo, read_floor, read_floor_2, read_canonical, read_portfolio, complete_todo):
  - "let's analyze the risk here" → analyze_blockers @0.72, under the 0.8 dispatch threshold (margin, not a flip)
  - "When did we launch the beta?" → check_completion_status @0.72, under threshold
  - "are we behind upstream at all" → local_git_status_query @0.75, under threshold
  - "set a reminder for the dentist appointment" → create_reminder @0.75, under threshold (the op is live)
  - "update the project plan doc with the new dates", "update the roadmap doc with the new dates" → update_document: the entry fails the #1677 effect guard (WRITE; your per-entry word)
  - "add a repo to my portfolio" → manage_repos: no WorkflowEntry
  - "please unlink / remove / disconnect my repository from this project" → manage_repos @0.85–0.92: no entry, and the rows' expected is not action-shaped (corpus-row fix)
  - "set my default repo to acme/widgets" (+4 phrasings) → set_default_repo @0.99: not in the live set (WRITE; your per-op word)
  - "can you summarize my current work", "give me a project overview", "I need a status report" → get_project_status: no WorkflowEntry (the live consult dispatches rail keys only)
  Four of these are threshold margins, not flips; the rest are two WRITE entries for your #1677 word (update_document, set_default_repo), two missing entries (manage_repos, get_project_status), and three corpus-row fixes.

Verified how: the gate per list with the live set this morning; `_qualified_search_query` read in source; the re-score report (40 calls, 0 errors); `git log -S` on the pre-classifier for the deleted literal (c9a39aab22). Not served.
