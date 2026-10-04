---
last_updated: 2026-10-03
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-10-03 at the 22:17 STOP fire (for 10-04 START).

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

## Cron

✅ **Re-armed 2026-10-03 22:2x PDT — job id `1ae41e70`**, expression `47 6,9,12,15,18,21 * * *`,
`CronList`-verified exactly one. 7-day auto-expiry (~2026-10-10) — re-arm proactively on or before
~10-08 if no STOP re-arm intervenes (the daily STOP re-arm resets it).

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **40 rows** (+1 at 10-04 10:0x for #1930/#1931), both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **40**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable all day 10-03, no new issues.

## Active — design closed, builds in flight (not mine to push forward)

- **#1911 + #1918** — combined design spec (`docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`), PA building.
- **#1899 armed-carrier write-erosion** — ruled, tracked as #1920, Lead building.
- **#1926 repo-unlink confirm** — RULED 10-03 (unlink confirms via #1190 DESTRUCTIVE; link/list do not; five
  constraints). Lead and Arch adopted them as the build acceptance criteria. Issue box 1 checked; box 2
  (wired + unit pin + deletion lane honors it) stays open for the build. Unlink lands LAST in the build order.
- **10-04 rulings (memo to Lead cc Arch/PPM, comments on #1930/#1931)**: (1) explicit `complete_todo` of a named
  item needs NO "shall I?" (agree Arch: widen `_EXECUTE_RE` with complete/finish/done, not "clear"); reply names the
  item, ambiguous target asks which. (2) **#1930** step 1 now: honest copy, arms nothing, offers archive/restore;
  step 2 wire via #1190 DESTRUCTIVE later, resolve + owner-check before arming. **Unverified**: what
  `project_repository.delete` does to todos with `project_id` set (FK, no cascade). (3) **#1931** out-of-chat is
  acceptable for beta; corrected PPM's premise: todo UI has NO reopen either (`templates/todos.html:255-259`).
  Owed: verify Lead's step-1 copy when it lands (**12:56: still NOT on main**, `canonical_handlers.py:4602-4612`).
- **10-04 13:1x copy rulings (memo to Lead cc Arch/PPM)**: archive/restore not-found replies ACCEPTED as landed;
  edit/update-project option (a) copy = "I can't edit a project's details from chat. I can show, add, archive,
  restore, and search your projects." (no "yet"; arms nothing; edit sniff must run BEFORE the substring add/list/search
  sniffs or "edit my project and add a note" reaches add_project). Owed: verify when Lead builds it. Arch ruled the
  literals stay (a); #1933 (effect-aware deletion gate) is Lead's. Nothing else open.
- **`read_floor` mechanism** — built, 5 ops, not flipped. The flip is PM's hand via Exec. Lead is now building
  wave 2 as a separate group `read_floor_2` (so live `read_floor` is untouched and its flip stays a separate
  token); `write_stakeholder_update` joins only if its floor path persists nothing.

## Sprint goal (Exec relay of PM ruling, 10-03) — week ending Thu 10-08

Finish epic 0 Phase 3 deletions for every pattern list with a live wave; Lead owns. **CXO + PPM rulings
are the named critical-path dependency** — turn destination questions around early, same fire
(quota may run out Wed ~14:10, plan on four days). I hold **no open ruling requests** as of 22:17 10-03.
**Possible future asks of me**: confirm copy if `complete_todo` or `update_document_query` turn out
DESTRUCTIVE (the builder decides from the handler); not asked, don't pre-empt. Arch's build order is
reads → writes → destructive; `MAX_DISPATCH_SITES` stays 0.

## Closed/corrected recently — watch only, nothing owed unless something reopens

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
