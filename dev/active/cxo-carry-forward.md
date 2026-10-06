---
last_updated: 2026-10-06
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — updated 2026-10-06 07:5x (Fire 1 START); structure from the 10-05 22:2x STOP rewrite.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — emit the per-fire heartbeat before ending every fire
>
> Run `scripts/duty-cycle-heartbeat.sh cxo {fire-type} --if-quiet` as the second-to-last action
> every fire. Third instance of this exact miss in one week (me 10-01, Lead 10-02, Docs 10-03);
> no misses by me since 10-02. Memory: `feedback_emit_heartbeat_every_fire_before_finishing`.

> ## 🔴 STANDING RULE — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — after `mail-send.sh`, a local `ls` can look reverted; merge before trusting it
>
> `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Both 10-02/10-03 self-corrections (D1, C1) came from re-reading source, and #1926 was decided by
> reading the unlink arm, not Lead's summary of it. Don't let a prior ruling stand unexamined just
> because it was ratified once.

> ## 🔴 STANDING RULE — keep mailbox filename basenames ≤150 chars (180 is the hard gate)
>
> The 180 limit includes `mailboxes/{role}/{box}/`, and `inbox/` is one char longer than `read/`.
> My own working rule is ≤130 (see below).

> ## 🔴 STANDING RULE — NEVER cc PM, never write to `mailboxes/xian (ceo)/` (PM ruling 10-03, Exec broadcast 17:28)
>
> No cc copy, PM not in `to:`/`cc:`. If something needs PM (a decision only PM can make, a relayed PM
> ruling, something PM would want to contradict), **address it to `exec` and name which of the three in
> the subject.** Supersedes the 09-11 three-condition cc rule. **This includes workstream reviews:
> Ship #064's review goes to `mailboxes/exec/inbox/` only.** In CLAUDE.md:717 and `DIRECTORY.md`.
> `mail-send.sh` calls now carry two paths (recipient inbox + own `sent/`), not three.

## Fire 2 (2026-10-06 10:25) — what I ruled, what's owed
- RULED to Lead (cc Arch/PPM): clear-family strings (V1 rewrite, V2 split by set size, V3 ok, string 5 strike verb clause), numbered list ratified, two flaws in unresolved reply (tail promise; remember only shown 10). RULED to PPM (cc Lead): CLARIFY ok for subject-less GUIDANCE if declarative/armed + turn-2 probe; repo-less link wording = declarative house style.
- #1950 CLOSED by me. Criteria line now 3: #1911, #1174, #1108.
- OWED/WATCH: Lead's reply on renderer start-number check; landing of V1/V2/string 5 + the two flaw fixes (verify in source when they land); the standing owed list above unchanged.

## Cron

✅ **Re-armed 2026-10-05 22:2x PDT — job id `d3d65afd`** (delete-then-create from `5fbdd6df`, SAME expression
`47 6,9,12,15,18,21 * * *`), `CronList`-verified exactly one. 7-day auto-expiry (~2026-10-12); the daily STOP
re-arm resets it.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **41 rows**, both guards clean at 10-05 22:2x. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **41**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **4** at 10-06 07:5x (#1950, #1911, #1174, #1108). **#1948 CLOSED by me 10-06 07:5x** (verified `app-shell.css:28-33`). #1950 (undefined `--font-family-mono`) approved, Web ships; I verify the render evidence and then it is mine to close.

## Active — design closed, builds in flight (not mine to push forward)

- **#1911 + #1918** — combined design spec (`docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`), PA building.
- **#1899 armed-carrier write-erosion** — ruled, tracked as #1920, Lead building.
- **#1926 repo-unlink confirm** — CLOSED by Lead 10-04 (610983fb96); I verified it in source (constraint 5 pinned).
- **10-04 rulings, all verified landed in source (nothing owed)**: #1930 step 1 delete copy; edit/update-project honest
  copy + sniff precedence; Lead's non-leading-edit fix `7f134f991b` (on main, intent prefixes skipped); reminder idioms
  ("don't let me forget", "I need to remember") need NO consent pause (reply echoes the saved text; revisit if
  `_reminder_saved_message` stops naming it). #1930 step 2 (wire delete via #1190 DESTRUCTIVE, resolve + owner-check
  first) and #1931 (out-of-chat acceptable; todo UI has no reopen either) stay as ruled. **Unverified**: what
  `project_repository.delete` does to todos with `project_id` set (FK, no cascade) — needed before step 2's copy.
- **Arch's "rail owns rail keys" (`can_handle` declines any rail key)**: Lead parked it on `wip/rail-owns-rail-keys`;
  Arch took split predicate (a) (`claims_category` for the orchestrator, rail-aware `can_handle` for the main path)
  with adapter parity landing WITH it; (b) multi-intent via the rail is a tracked follow-up. **My 22:2x call (memo to
  Lead cc Arch)**: `offer_hint` carry-through is a must-land (the not-found replies end in a question whose "yes"
  resolves through `last_offer`, `intent_service.py:2850`); parity test should run "reply, then 'yes'" through both
  paths. Under (b), a consent hold on a later sibling must NAME the siblings not run. **LANDED + VERIFIED 10-05 07:3x**
  (`25f1abc010`, `f163f1dd90`; source read, no run). **list_repos misread REPRODUCED by Lead and RULED 10-05 10:33**
  ("list my repos on github" -> no project 'github'; "show all of my repos" -> 'repos'): corpus rows + a list_repos-only
  copy fallback ("I couldn't find a project called '{name}'. Here are all {n} of your registered repositories:" +
  list; zero-repo variant; original casing; no plausibility gate; write ops keep not-found-and-stop). **LANDED 13:04 (`630e410910`) + VERIFIED in source**
  (all 5 pins). Gap was mine: n=1 reads "all 1 of your registered repository:"; ruled 13:35 "The only repository you have
  registered is:". n=1 fix LANDED 15:52 (`f0c17eb20d`) and VERIFIED in source: **list_repos thread DONE on my side** (live after PM's next deploy). #1911 isolation-claim recheck DONE 10-05 16:3x (#1458 closed; claim stands; trigger retired). `read_portfolio` token release is Exec/Arch's call.
- **10-06 07:45-07:52 rulings (memos sent, mail-send 21f97d6c45/2f3207b456/e257916c78)**: #1943 batch strings ratified with edits to Lead (duplicate titles collapse with a count; decline = existing "Okay — I won't…" family; unresolved line names the list searched and never quotes the ordinal; summary reports only what succeeded; ordinal resolves only against a list last shown NUMBERED). #1951 to PPM cc Lead/Arch: **`is my calendar showing any conflict` stays floor, week dump is not an answer, real regression, fix by adding "listing only — no conflicts/free time/availability" to the `week_calendar` description (`workflow_entries.py:1448`)**; `what am I working on?` stays floor; no-repo-named CLARIFY accepted if armed/declarative. **Owed by me**: verify Lead lands the #1943 strings as ruled; verify the week_calendar description fix and the ×6 rerun; verify #1950's render evidence and close it. 10-05 Docs nudge answered (DAY-CLOSED marker appended).
- **10-05 19:50 + 22:25 rulings (tracker row 1 holds the detail)**: VERIFIED LANDED in source (no run): #1880 tail copy, `complete_todo` copy, deferred-sibling ratified, #1945 slices 1+3 (mirror hidden, Project integrations copy) + default-repo pointer (`f8d71cd334`+), #1948 body font (`1479914ecc`). **Ruled 22:25 (memos to Lead cc Arch, and Web)**: no default-project badge/copy (`Project.is_default` inert, `get_default_project` zero callers; reopens only when something consults it); widen `settings_github.html:475` label to "Default repository:" + hint "Used when a chat command or workflow doesn't name a repository."; **Places removal concurred** (keep `PlaceService`); **Documents NOT concurred, held on #1270** (restore path for the Q&A view; `documents.html` says do not delete) — Lead to record that on #1522; Web: `button, input, select, textarea { font-family: inherit; }` approved under #1948 with before/after screenshots. **Owed by me**: verify the label widening, #1945 slice 2 (unlink deletes the mirror; Lead tomorrow), Arch's dual-write retirement incl. the dormant `Project.get_github_repository` fallback (`models.py:503-504`); read Web's #1948 evidence and close it; #1943 clear-family exact strings (Lead brings them before that path changes); close/reopen "Which one would you like to close?" unarmed-question flag (unanswered); what `project_repository.delete` does to todos before #1930 step 2 copy.
- **`read_floor` mechanism** — built, 5 ops, not flipped. The flip is PM's hand via Exec. Lead is building wave 2 as
  group `read_floor_2` (separate token); `write_stakeholder_update` joins only if its floor path persists nothing.
- ⚠️ **No Python env in this worktree** (no venv; system python3 lacks sqlalchemy), so I cannot run handler probes;
  every verification this day was source-read and said so. If a probe matters, ask Lead to measure it.
- **Note**: my 22:2x memo's `date:` frontmatter reads 22:25 but it was sent ~22:20 (typo, no effect).

## Sprint goal (Exec relay of PM ruling, 10-03) — week ending Thu 10-08

Finish epic 0 Phase 3 deletions for every pattern list with a live wave; Lead owns. **CXO + PPM rulings
are the named critical-path dependency** — turn destination questions around early, same fire
(quota may run out Wed ~14:10, plan on four days). I hold **no open ruling requests** as of 22:2x 10-05 (Lead's slice 2 is gated clear; slice 4 closed).
**Possible future asks of me**: confirm copy if `complete_todo` or `update_document_query` turn out
DESTRUCTIVE (the builder decides from the handler); not asked, don't pre-empt. Arch's build order is
reads → writes → destructive; `MAX_DISPATCH_SITES` stays 0.

## Closed/corrected recently — watch only, nothing owed unless something reopens

- **10-05: six fires, ~8 memos; list_repos thread, #1911 isolation recheck, #1880/`complete_todo`/deferred-sibling copy, #1945, #1948, Places/Documents concurrence all ruled; everything Lead/Web reported landed was verified in source.**
- **10-04: five fires, six memos, all rulings verified in source** (see Active). Residual I flagged at 15:58 was real
  (Lead measured it) and fixed same day.
- **10-03: #1926 ruled**; Ship-related PM-routing change absorbed (standing rule above).
- **10-02/10-03: 13-row DISCOVERY/TRUST/ANALYSIS/MEMORY addendum — RULED, CORRECTED TWICE** (D1 `session_activity_query`
  is current-session only; C1 `attention_query` vs `analyze_blockers` reversed to ANALYSIS). Both self-initiated
  after re-checking source — worth remembering the pattern if a third one shows up.
- **10-02: #1899 RULED; Ship #063 workstream review sent to Exec.**
- **10-03: mailbox filename-gate incident** — Arch's fix; I regenerated my own MANIFESTs.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open question
(build unowned). **Ship #064 workstream review**: send to `mailboxes/exec/inbox/` only when the kickoff arrives.

## Agent 360 v0.5 — response owed within ~2 weeks of 09-25, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`). Tracked as a standing-items
row. Answer via memo to `mailboxes/host/inbox/` when there's something real to say.

## Not mine — noted so it isn't re-investigated

The Web row in `dev/active/duty-cycle-registry.tsv` has doubled-quote CSV corruption; the freeze-check
prints REGISTRY-CORRUPTION for it. HOST and Arch have written to Web and CIO. **Never edit that file via
Python's csv module.**

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2.
- **BYOC rubric**: v0.8.2. T-own-surface measurable (series closed 09-25); T-MCP-surface
  `UNMEASURED` until increment-1 infra.

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters**. The subject line carries the argument.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag. Check that file directly rather than assuming this note stays current about it.
