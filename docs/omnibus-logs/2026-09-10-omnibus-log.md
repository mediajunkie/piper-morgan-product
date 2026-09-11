# Omnibus Log: September 10, 2026

**Day**: Thursday
**Sessions**: 14 (Communications, Lead Developer, Chief Architect, Web, Piper Alpha (PA),
HOST, CXO, Documentation Management, PPM, Chief of Staff (Exec), CIO, and 3 separate Coding
Agent (prog) delegations from Lead)
**Day Type**: HIGH-COMPLEXITY: COORDINATION — 11 distinct roles plus 3 prog delegations,
with sustained cross-agent handoff chains, not independent parallel tracks.
**Justification**: Four coordination threads ran through the day with real back-and-forth,
each requiring one role's output to change another's next move: (1) the flywheel v3 Layer 2
text reached PM's ratification step via an Arch→Docs→Arch verification loop that caught its
own slip (an m-49 fold violating D5's ruling); (2) CXO's ruling on Lead's arm-survival
question unblocked both the #1732 security lane and the #1739 DESTRUCTIVE-tier adoption,
executed same-day by two prog delegations; (3) the scope-guard mechanism (CIO's predicate +
Arch's delivery Action) was built, synthetically tested, and found to contain a cascading
sequence of five distinct self-caught "false clear" defects across CIO/Arch/CXO/PPM in one
afternoon; (4) a mailbox-mislocation defect (`inbox/read/` instead of `read/`) was found by
PPM (#1743, 188 files), swept cohort-wide by CXO, found again on PA's seat (30 files), fixed
by PA, and traced by CXO to a month-old incident that had been declared "PPM only" —
surfacing that no prior sweep had installed a durable invariant.
**Git Commits**: 280 (product + website repos combined)

---

## Chronological Timeline

### Phase 1: Six Starts and the Flywheel Text Lands on PM's Desk (6:15 AM – 7:22 AM)

**6:15 AM**: **Communications** starts the duty cycle; no confirmed post scheduled, mail
empty, standing items (series structure, ChicagoCamps) unchanged.

**6:31 AM**: **Lead Developer** starts; drains CXO's overnight self-answer on arm-lifetime
(CONFIRM arms live exactly one turn, popped pre-classification — their own
drop-on-topic-change recommendation was an inverted no-op); acks and queues #1732 as next
intake item.

**6:46 AM**: **Chief Architect** starts and drafts the **flywheel v3 Layer 2 replacement
text** (`dev/active/flywheel-v3-layer2-text-2026-09-10.md`) — the exact text the seven
ratified decisions resolve to, five days after PM named the "something has been lost"
feeling. Sends the ratification memo to PM (cc leadership) with the round record and two
open asks riding the cc: Docs' pointer-list slots, CIO's canon-application-on-ratification.

**~8:00 AM**: **Lead Developer** deploys v71 on PM's word (fly release green) — carries the
1527+1654 dawn fixes, 1730 honest decline, notice cut, 1734 admin gate.

**6:52 AM**: **Web** starts; mail empty, all four standing items still gated (three on PM,
one on the Vercel access blocker).

**~8:00 AM** (between fires): **xian** asks **Web** how hard a WYSIWYG editor would be for
the publishing workflow. **Web** re-reads `ComposeApp.tsx` before estimating: moderate lift
(~3-4 days) but the real risk is round-trip fidelity — any true WYSIWYG re-serializes
markdown, normalizing formatting into noisy diffs and spurious 409s against Comms' direct
edits. Offers a cheap middle ground (toolbar + shortcuts, ~1 day, zero round-trip risk) and
asks PM which pain is real; question left open, not chased.

**7:07 AM**: **HOST** starts (Day 48 on Amber); verifies Arch's ratification memo by reading
the actual text file rather than trusting the summary, confirms HOST's own contributions
(m-53 chokepoint sub-clause, Practice 5's D7 cadence) are accurately reflected.

**7:12 AM**: **Piper Alpha (PA)** starts; inbox empty; retests the known-broken
chrome-devtools MCP path against pipermorgan.ai/privacy, confirms still the same continuous
session (not new information).

**7:12 AM**: **Piper Alpha (PA)** confirms T1 (Cross-Piper synthesis) and the #1463 probe
series both remain in the same settled state as yesterday — T1 delivered with no PM reply
yet, not auto-closed on silence; #1463 closed with a tested answer, its named
revisiting-trigger still unmet.

**7:17 AM**: **CXO** starts and rules on **Lead Developer's arm-survival question** from
overnight: separates two tangled questions — arm survival (5a: CONFIRM tier lives exactly
one turn, stated explicitly rather than inherited) and orphan handling (5b: re-rendering is
safe at every tier including DESTRUCTIVE, because a re-render is still an ask — only
executing on a decayed arm is dangerous). Names the generative rule: *"an ambiguous
acceptance should cost a turn, not an action."*

**7:17 AM**: **CXO** also consolidates the acceptance contract — amended twice in 24 hours
and living only in mail — into a single addressed document,
`docs/internal/design/acceptance-contract-user-facing-2026-09-10.md` v1.0, ending "a spec
whose authoritative version is whichever memo you happened to read."

**7:17 AM**: **CXO** catches a third scripted-edit incident on their own standing-items
tracker (a `.replace()` dropped a row's last two columns; the row-count guard added after
the 09-01 incident couldn't see it because it counts lines, not columns) — adds a column
check, states the honest tally (three incidents in ten days), and resolves to use `Edit`
instead of scripted replace going forward.

**7:17 AM**: **CXO**'s freeze-detect reads `INSUFFICIENT-SCHEDULE` (too early in the window
to discriminate a real stall) and is logged explicitly as **not** an all-clear — the m-44
denominator discipline applied to the freeze-check's own output, not just to other roles'
claims.

**7:20 AM**: **Documentation Management** starts and delivers **Arch's named ask**: the two
verified pointer-list slots (P1: m-07/m-30/m-42/m-16/m-14; P5: m-23/m-24/m-37 alongside the
existing m-45), re-verified live against the corpus rather than pulled from a two-day-old
memory, sent formatted for direct drop-in.

**7:22 AM**: **PPM** starts; `sprint-truth.py` clean (MVP 47 not done, zero unmilestoned);
links the newly-consolidated acceptance-contract doc into the epic-order file's epic 3
section so it cites a live address instead of a mail thread.

### Phase 2: The Security Lane Opens and the Contract's First Test (9:02 AM – 10:22 AM)

**9:02 AM**: **Chief of Staff (Exec)** starts; freeze-check reads 11 rows, zero alerts —
first fully clean read of the week.

**9:02 AM**: **Chief of Staff (Exec)** falsifies their own proposal from yesterday before it
could be built: the "≥1 MVP item In Progress" board-visible floor read the same 3 stale
items all week while nine MVP issues closed **Sprint Backlog → Done** yesterday, skipping In
Progress entirely — a watchdog on it would have false-alarmed on the most productive day
since the collapse. Names the error as the same mistake (m-43, measuring schema not
behavior) they'd challenged someone else on two days earlier; corrects to CIO/Arch/PM with a
replacement metric (days-since-last-closure + Sprint Backlog trend).

**9:12 AM**: **Communications** — quiet fire, no unblocked work.

**9:31 AM**: **Lead Developer** — intake fire 4: **#1732** (chat-render sanitizer, the
render-boundary chokepoint) begins, now that CXO's arm-survival ruling and the one-address
contract have landed. Delegates to **Coding Agent (prog)**.

**9:32 AM**: **Coding Agent (prog)**, delegated by Lead, investigates #1732 and finds two
divergent copies of the renderer exist: `web/bot-message-renderer.js` (the one the issue
cites, unserved) and `web/assets/bot-message-renderer.js` (the live one) — a duplicate-file
drift class, plus a raw `marked.parse` fallback in `chat.js` that bypasses sanitization
entirely on `app_shell` pages. Corrects the issue's cited marked version (18.0.12 claimed,
15.0.12 actual, curl-verified).

**9:46 AM**: **Chief Architect** — v3 text reaches complete: Docs delivered both
pointer-list slots and caught a real slip — Arch's own P4 draft had folded m-49 into canon
against D5's own maturity-gate ruling; corrected and dated inline, credited to Docs.

**9:52 AM**: **Web** — quiet fire, WYSIWYG question to PM still open.

**9:57 AM**: **Documentation Management** — verifies the v3 text is genuinely complete by
reading the live file rather than trusting the memo; separately fixes an own-mistake
mail-send resend (missing the `inbox/` path) surfaced while triaging CXO's MANIFEST finding.
Closes **#1727** (10 dead links across 8 files in legacy trees, none ever written) and files
**#1742** for an adjacent dead link found outside #1727's original scope, fixing both in one
pass.

**10:00 AM**: **Piper Alpha (PA)** — quiet fire.

**10:07 AM**: **HOST** — verifies Docs' pointer-list delivery directly against the live
corpus; flywheel ratification now unblocked on both named slots.

**10:17 AM**: **CXO** rotates their own cron a day early (`65e2a3c5` → `2e2952df`) on their
own sharpened rule — *"rotate at the first fire where you have both the information and the
margin, not the last one where it's still possible"* — catching themselves nearly obeying a
stale note ("rotate at 09-11") over the rule that produced it.

**10:17 AM**: **CXO** gives **#1738** a name: Piper told the user 6 archived projects
existed, rendered 5 with "…and 1 more," and the assistant then described its own truncated
render as *"the list I got back"* — a false claim about provenance, not a truncation bug.
States the rule as GatherOutcome contract §5b: **a provenance value must survive rendering
unchanged; a render cap may shorten what the user sees but never what the system believes it
has.**

**10:22 AM**: **PPM** reflects Exec's In Progress self-correction into the epic-order file,
verifies and marks **#1637, #1732, #1734** closed in place (not deleted, so the record shows
history), and folds CXO's #1738 framing into epic 5's section without reordering (per CXO's
own explicit scope statement that it doesn't reorder either epic).

### Phase 3: #1732 Closes, the Scope-Guard Predicate Ships (10:22 AM – 12:12 PM)

**~10:20 AM**: **Lead Developer** closes **#1732**: the render boundary is sanitized at one
chokepoint (DOMPurify + pinned marked, vendored locally). Discoveries from the lane: the
issue's cited renderer was an unserved twin (filed **#1740** for the drift class), a fourth
unsanitized sink found and backstopped, the marked version corrected, double-escape
disproven behaviorally against the 1730 pins, and a new security finding filed separately
(**#1741**, suggestions-UI inline-onclick) rather than scope-creeping the fix. Evidence: a
new 16-pin jest suite plus 9 template-render tests, full jest suite 128/128 green, template
+ 1730 pins 1147 passed, ratchet + seed guard 55 passed. Epic 2 (security/tenancy) now
complete except #1741.

**10:37 AM**: **CIO** starts; drains Exec's floor-metric correction and replies confirming
the scope-guard predicate's own design (reads commit content and issue state directly, never
a board column) doesn't share that exposure — commits to checking the lesson live on today's
own work, not just nodding.

**10:37 AM**: **CIO** ships the **scope-guard detection predicate**
(`scripts/scope-drift-check.sh`) — two signals (closure-intent commit on an open issue;
100%-checked-but-open checklist), explicitly negation-aware after testing against the exact
#1278 false-positive class GitHub's own auto-close matcher fell into. 11 tests, real git
commits + mocked `gh`. Delivers the flag-memo format to Arch: one memo per issue, "possible"
never "certain," denominator always stated.

**12:12 PM**: **Communications** runs a full `template-audit` on "The Mailbox Trust
Violation" (today's scheduled beat) after PM's text-only edits land, catching four real
issues no mechanical check alone would find: the internal "load-bearing" idiom, two separate
pronoun inconsistencies (Arch given "himself" against the piece's established "they/them";
PPM given "it" against the same treatment given Arch and CIO), and a dateline reading as one
day though the piece spans two. Does not send PUBLISH-READY — frontmatter (image) still
empty.

### Phase 4: DESTRUCTIVE Tier Adopted, Scope-Guard's Delivery Half Ships (12:31 PM – 1:22 PM)

**12:31 PM**: **Lead Developer** — intake fire 5: the **#1739 DESTRUCTIVE-tier adoption**
lane begins, inputs complete (CXO's contract + arm-survival ruling). Delegates to **Coding
Agent (prog)**.

**12:42 PM**: **Coding Agent (prog)**, delegated by Lead, adopts all four
DESTRUCTIVE-adjacent seams (confirm-workflow, drafted-issue file-confirm,
repo-clarification, plus acceptance.py's tier table) under the one-address contract,
threading each seam's registry-declared axes and applying CXO's §5a/§5b arm-survival rule:
STATE_QUESTION at CONFIRM tier gets a visible re-arm only (stored ask restated in-line),
never silent. Removes three now-dead `detect_confirm_response` call sites from the ratchet;
adds 7 new behavior-delta tests covering the full §5b arc and retires one stale abandon-pin
that the contract mandated flipping. Evidence: full intent_service tree + standup 3908
passed, architecture enforcement + seed guard 50 passed, post-format re-run 131 passed.

**12:46 PM**: **Chief Architect** ships the scope-guard delivery half,
`.github/workflows/scope-guard.yml` (dispatch-only, arming checklist in the header,
m-50-conformant machine-written memos). Confirms **CXO's #1738 framing as the joint
invariant of epics 1 and 2**: provenance rides the structured GatherOutcome; the renderer
consumes and never writes; the model's context gets the outcome, not the rendered string.

**12:52 PM**: **Web** — quiet fire.

**1:00 PM**: **Piper Alpha (PA)** — quiet fire.

**1:03 PM**: **CXO** elevates #1738 further after Arch's confirmation, records Arch's
sharper architectural framing verbatim rather than paraphrasing (*"the assistant reading its
own render as evidence is the architectural defect, not the truncation"*), and updates the
contract to v0.3 — catching that §5b still said "CXO's position" after becoming ratified
law, the exact "authoritative version is whichever memo" failure named the day before, on
CXO's own artifact.

**1:03 PM**: **CXO** reads `scope-guard.yml` itself rather than trust the description, finds
the design's last bolt-on standing: the promotion-to-required-check decision rides a
hand-kept tally in PPM's drain notes. Proposes a `verdict: UNSET` header field so the rate
becomes a grep, not a habit — explicitly not having run the Action yet.

**1:07 PM**: **HOST** verifies CIO's scope-guard predicate directly against the commit and
code (not the memo's description), confirming the negation-handling claim.

**1:20 PM**: **Documentation Management** — quiet fire, no day-of-week trigger today.

**1:22 PM**: **PPM** reports the scope-guard shipped (CIO's predicate + Arch's Action
skeleton) and ships CXO's `verdict: UNSET` fix same-morning. Runs two `workflow_dispatch`
tests honestly — both take the quiet-run path cleanly with denominators printed — and
explicitly names the boundary: this verifies the predicate and quiet-run path, **not** the
memo-delivery path, since neither test range produced a flag.

### Phase 5: The False-Clear Cascade — Five Self-Caught Defects in One
Afternoon (3:12 PM – 5:15 PM)

**3:12 PM**: **Communications** — quiet fire; art still hasn't landed on today's beat.

**3:31 PM**: **Lead Developer** — the CI belt regresses to 3 reds since morning (Code
Quality, Router Pattern, Architecture). Delegates the repair to **Coding Agent (prog)**.

**3:33 PM**: **Coding Agent (prog)**, delegated by Lead, repairs all three gates: mailbox
filename lint (6 CXO memo basenames shortened across every tracked copy, malformed
`mailboxes/ppm/inbox/read/` copies relocated to `ppm/read/` — **files #1743** for the 188
remaining files as discovered-but-out-of-scope work); router pattern (a docstring line, not
real code, tripping the grep-based import checker on a historical-correction note —
reworded, no exclusion added, since excluding the file would ungate a real future
violation); mypy drift (rebuilds a CI-replica venv pinned to the exact toolchain, fixes
forward a non-narrowing `Optional` guard pattern from yesterday's #1739 seam work, clearing
5 pre-existing same-root errors as a bonus, ceilings lowered union-attr 161→156 /
truthy-function 1→0 / arg-type 378→377). 175 tests passed on the final gate re-verify.

**3:46 PM**: **Chief Architect** runs a **synthetic end-to-end test** of the delivery path
as its own author rather than trust the design on paper — creates fixture issue **#1744**.
First dispatch is over-cautious and misses; second dispatch (`#1744` plain reference) proves
the predicate fires 1/1, but the delivery half has a **double defect**: `GITHUB_TOKEN`
cannot push to protected `main` (GH006), and the retry loop had silently swallowed that
failure and reported SUCCESS — a false clear from the mechanism built to prevent false
clears. Fixes the silent-swallow same-fire; routes the branch-protection bypass decision to
PM.

**3:52 PM**: **Web** — quiet fire.

**4:00 PM**: **Piper Alpha (PA)** — quiet fire.

**4:03 PM**: **CXO** checks their own verdict-slot fix from the morning and finds it has the
identical shape: the proposed `grep -c 'verdict: UNSET'` count is a numerator with no
denominator — over zero matching files it prints nothing, byte-identical to "no flags have
ever occurred." Verifies behaviorally (empty directory → empty output; one file → correct
count) and, with Arch's synthetic test proving no memo has ever landed, names the
consequence: *"in two weeks my count would have read clean while delivery had never once
worked."* Offers a per-run ledger as the fix, sequenced after PM's repo-settings decision
since it shares the same push-access blocker.

**4:03 PM**: **CXO** names a sharper structural problem in the same design: it chose mail
over CI checks specifically because checks are unwatched, yet a **failed** delivery reports
only to the workflow run status (unwatched) while a **successful** one reports to PPM's
inbox (watched) — *"success reports to the watched channel; failure and the denominator
report to the one the design rejected. That is backwards — failures are what you cannot
afford to miss."*

**4:07 PM**: **HOST** — quiet fire.

**4:20 PM**: **Documentation Management** — quiet fire; scans #1740-1744, confirms #1743 is
explicitly PPM-owned per its own acceptance criteria.

**4:22 PM**: **PPM** closes **#1743** as their own long-standing bug: 188 files misfiled in
`mailboxes/ppm/inbox/read/` instead of `mailboxes/ppm/read/`, repeated every fire of this
multi-day session without being noticed, found via the drift check. Moved in 10 batches with
`origin/main` verification after each. Separately confirms the scope-guard's real synthetic
test result (Arch's GH006 + false-SUCCESS finding) and accepts CXO's denominator gap in the
verdict-slot fix.

**4:37 PM**: **CIO** reviews Arch's synthetic-test memo and, rather than accept its praise
at face value, reads `scope-drift-check.sh` directly — finding the described "rc>1 fails
loudly" behavior doesn't exist: the script has two unconditional `exit 0`s, including the
not-a-git-repo path, making Arch's `if [ $RC -gt 1 ]` branch **dead code** — the fifth
self-caught false-clear instance of the afternoon. Fixes same-fire (exit 2 for genuine run
failures, exit 0 for every real outcome including a flagged one), adds three tests, verifies
via `git stash` that they fail pre-fix and pass post-fix.

**4:38-5:15 PM**: **Chief of Staff (Exec)**, at PM's direct request, verifies their own
cycling is healthy (both 09-09 STOP and 09-10 START heartbeats confirmed), and corrects a
UTC-vs-Pacific counting error affecting every closure figure given this week (today's real
Pacific-day count is 4, not 6 as first read) — recomputes the whole window in Pacific rather
than quietly restating the wrong number. Confirms the cause-grouping prediction from
Wednesday landed: three of today's four closes (#1631, #1650, #1694) are the acceptance
contract, one cause. Delivers PM's afternoon asks: the **forest-report rollup**
(`dev/active/exec-cohort-attention-rollup-2026-09-10.html`, trajectory-first per PM's ask,
three items flagged as needing only PM — Vercel access, the bot's branch-protection bypass,
flywheel v3 ratification) and a **7-item In Review test round**
(`dev/active/in-review-test-round-2026-09-10.html`, three of the seven re-runs of items PM
failed live Wednesday). Vercel diagnosed as account-side, not repo-side — Web's blocked
access and billing blindness are the same underlying fact. Flags their own 2×/day cadence
(vs. everyone else's 6×) as the cause of PM seeing no updates all afternoon — proposed as a
fix, not changed unilaterally.

### Phase 6: The Mailbox Defect Propagates — PPM's Fix, CXO's Sweep, PA's Instance (6:12 PM – 7:22 PM)

**6:12 PM**: **Communications** — quiet fire; art in progress (alt text and caption landed,
`image` field still blank) — read correctly as mid-process, not chased.

**6:31 PM**: **Lead Developer** — Exec flags the carry-forward a day stale. Lead's first
refresh attempt **silently no-opped** (a regex miss the script reported as MISS, logged as
"refreshed" anyway for one commit) — caught on re-read and corrected the same fire. Adopts a
new rule: the carry-forward refreshes at any fire where live state materially moved, not
only at STOP.

**6:37 PM**: **CIO** confirms all findings from the afternoon's cascade, credits the
discipline (each defect found by someone other than its own author, except CIO's and CXO's —
found by their own authors because the thread had made self-checking the expected move), and
closes the loop on 7t's remaining half.

**6:52 PM**: **Web** — quiet fire.

**7:00 PM**: **Piper Alpha (PA)** — **CXO's cohort-wide mailbox sweep** (see below) finds
**30 files in `mailboxes/pa/inbox/read/`**, the exact destination path every triage move in
this entire session has used. PA verifies independently against `origin/main` before
touching anything (matching CXO's numbers exactly), moves all 30 in 4 batches via
`mail-send.sh` mirroring PPM's own #1743 procedure, regenerates both MANIFESTs, and confirms
zero nested mailbox paths remain cohort-wide. Replies to CXO confirming the fix; saves the
convention to memory.

**7:03 PM**: **CXO** — with both loop-closing acks in the inbox (PPM's ledger fix, CIO's
fifth catch), asks the question nobody had: *"one seat found it by accident is the signal a
shared default is at work, not one person's slip."* Sweeps every directory under
`mailboxes/` on `origin/main` at any depth and finds exactly **PA's 30-file instance** — not
historical, newest is yesterday. Discloses the personal interest (several of the 30 are
memos CXO sent PA) and deliberately does not touch PA's mailbox, routing the fix to PA per
PPM's own #1743 procedure as the worked template.

**7:07 PM**: **HOST** — quiet fire.

**7:20 PM**: **Documentation Management** delivers a **real deliverable**: Lead's finding
that the batch-15 `dev/active` housekeeping sweep (#1486, 09-02) had archived **PM's live
sprint tracker** (`honest-mvp-ledger-2026-08-08.html`) as "forensic-only," sitting archived
8 days until PM's own 404 surfaced it. Lead had already restored it; Docs verifies the
restore directly, then ships **`cleanup-dev-active` SKILL.md v1.1→v1.2** with a mandatory
Step 2.1 guard (published-artifact reference check + recent-commit check — either fires,
hold rather than archive) so the class is closed, not just the instance. Separately
reproduces **CXO's MANIFEST.md false-positive** on Docs' own seat, closing the open
verification gap CXO's 09-09 finding had named (confirming denominator now 2 seats).

**7:22 PM**: **PPM** confirms the cohort-wide #1743 shape is now fixed everywhere (CXO's
sweep + PA's independent fix) and that CIO's fifth false-clear catch is tested and holding.

### Phase 7: Day Close — the Rollup, the History, and the Uninstalled
Invariant (9:02 PM – 10:17 PM)

**9:02-9:25 PM**: **Chief of Staff (Exec)** runs the day's STOP fire: sweeps all eleven
agent seats on `origin/main` for nested `inbox/read/`, `read/read/`, and `sent/read/` paths
and confirms **zero remaining** now that PA's fix has landed. Closes the day at 4 MVP
(Pacific-corrected): #1631, #1650, #1694 (the acceptance contract, one cause) and #1732
(security). Checks Lead's own records: session log current and strong, carry-forward a day
stale — flagged, not fixed, since it's Lead's own working state.

**9:12 PM**: **Communications** closes the day: art still incomplete (image field blank),
correctly not chased or declared ready.

**9:37 PM**: **CIO** — quiet close.

**9:42 PM / 10:12 PM**: **Piper Alpha (PA)** — last scheduled fire; confirms the mailbox fix
from earlier holds clean.

**9:47 PM**: **Lead Developer** closes the day: v71 deployed, DESTRUCTIVE tier adopted (3
issues closed, #1617 held deliberately for PM's live standup), #1732 render boundary sealed,
tracker restructured, belt repaired 2/3 (third is a known CI env-drift signature, diagnosis
queued past the Fable cap), and **Docs shipped both cleanup-dev-active guards same day** —
the class Lead's own incident produced is now closed cohort-wide, not just patched locally.

**10:07 PM**: **HOST** runs the full STOP procedure (Fire 6): checkers all clean, MEMORY.md
regenerated (192 entries, routine drift). Names the day's shape: the flywheel re-evaluation
that opened 09-08 reached PM's ratification step, HOST's own credited contributions verified
directly; a genuinely quiet week-closing day otherwise, three of five fires empty.

**10:17 PM**: **CXO** closes the day by tracing **#1743's actual history** rather than treat
tonight's fix as the end of the story: `2026-08-10-ppm-code-log.md` shows PPM found the
identical nested-dir shape a month ago (21 files), swept the cohort, and declared it **"PPM
only."** PPM's own log the very next day (08-11) shows the habit resuming. By 09-10 the
count is 188, plus PA's independent 30. States the two mechanical conclusions plainly: *"a
cleanup that doesn't change the behavior that produced the mess is a rollback, not a fix"*
and *"a cohort sweep is a point-in-time measurement with a shelf life — 'PPM only' was true
on 08-10 and false by 08-31."* Names that tonight's own sweep has the identical limit ("PA
only" is true at 22:17 and says nothing about 09-25) and proposes a standing invariant check
(`git ls-tree` for any nested `mailboxes/*/inbox/read/`) rather than another one-time sweep
— ownership offered to PPM/CIO, not claimed.

---

## Executive Summary

### Core Themes

- The flywheel v3 Layer 2 text completed a five-day, seven-decision synthesis and reached PM's
ratification step, with its own verification loop catching a real slip (m-49 folded against
D5's own ruling) inside the ratification thread itself.
- A single afternoon produced five independently self-caught "false clear" defects on one
mechanism (the scope-guard build) — CIO's own predicate, Arch's own retry loop, and CXO's
own verdict-slot fix each failed the exact standard their authors had just applied to
someone else's work.
- A mailbox mis-triage defect (files landing in `inbox/read/` instead of `read/`) was fixed
three times in one day across two roles (PPM's 188, PA's 30) and traced by CXO to a
month-old "PPM only" declaration that had already proven false by the time it was made
durable — no sweep to date has installed an invariant that would notice a recurrence.
- CXO's ruling separating "arm survival" from "orphan handling" on Lead's DESTRUCTIVE-confirm
question unblocked two prog-delegated implementation lanes (#1732 security, #1739
DESTRUCTIVE-tier adoption) same day.
- Exec falsified their own board-metric proposal before it shipped, catching the same
measurement-layer mistake (m-43) they had challenged a colleague on two days earlier.

### Technical Details

- **#1732** closed: chat-render XSS chokepoint sanitized (DOMPurify + pinned marked, vendored
locally), discovering a duplicate unserved renderer file (#1740) and a fourth unsanitized
sink, plus a new security finding filed separately (#1741) rather than scope-creeping the
fix.
- **#1739** (DESTRUCTIVE-tier adoption) completed for all four adjacent seams
(confirm-workflow, drafted-issue, repo-clarification, acceptance.py tier table), applying
CXO's §5a/§5b arm-survival rule; 3908+50+131 tests passed.
- **Scope-guard mechanism** shipped end-to-end: CIO's detection predicate
(`scripts/scope-drift-check.sh`, negation-aware, 11 tests) + Arch's delivery Action
(`.github/workflows/scope-guard.yml`, dispatch-only); synthetic test found GH006
branch-protection block plus a silently-swallowed retry-loop failure, both fixed same-day.
- **CI belt repaired** 2/3 gates same-day by a prog delegation (mailbox filename lint, router
pattern false positive, mypy drift fix-forward with ceilings lowered); Architecture gate
diagnosed as a known CI-environment version-skew signature, not new code rot.
- **#1743** (188 misfiled mailbox files) and its sibling instance (PA's 30 files) both fixed
and verified against `origin/main`, cohort-wide sweep confirming zero remaining nested
`inbox/read/` paths as of tonight.
- **`cleanup-dev-active` skill v1.1→v1.2** shipped same-day with a mandatory
published-artifact/active-use guard, closing the class behind an incident where PM's live
sprint tracker was archived as "forensic-only" for 8 days.
- **Acceptance contract** consolidated from three scattered memos into one addressed document
(`docs/internal/design/acceptance-contract-user-facing-2026-09-10.md`), reaching v0.3 same
day as the GatherOutcome provenance rule (§5b) was elevated to a joint invariant of epics 1
and 2.
- **#1727/#1742** (13 total dead links across legacy doc trees) closed in one pass by Docs.
- Total tests run across the day's implementation work exceed 5,600 (3908+50+131 on #1739;
128+9+1147+55 on #1732; 175 on the belt repair; 15 on CIO's scope-guard fix; 11 on the
original predicate).

### Impact Measurement

- 280 commits across product and website repos.
- MVP trajectory: 4 (Mon) + 9 (Tue) + 4 (Thu, Pacific-corrected) = 17 MVP items closed in
three days, against 7-11 per week during the prior collapse; MVP stands at 45 not done,
1,133 done, zero unmilestoned.
- Five distinct "false clear" defects found and fixed in one thread in one afternoon, each
caught by someone other than the mechanism's own author except two — both of which were
caught by their own authors specifically because the thread had made self-checking the
expected move.
- Two GitHub issues newly discovered during #1732 remediation (#1740, #1741); one discovered
during belt repair (#1743, 188 files) and fully closed same day.
- Three items named as needing PM specifically and nothing else: Vercel account-side access
(Web hard-blocked), branch-protection bypass for the scope-guard bot (Arch's finding), and
flywheel v3 ratification itself — none ratified as of day's close (verified against
`decisions.log`).
- 218 total mailbox files corrected cohort-wide today (188 PPM's #1743 + 30 PA's sibling
instance), with an eleven-seat sweep confirming zero nested `inbox/read/` paths remain as of
the day's last check.

### Session Learnings

- **A cohort sweep is a point-in-time measurement with a shelf life** — CXO's closing finding:
"PPM only" was declared true on 08-10 and was already false by 08-31, and tonight's own "PA
only" sweep carries the identical limitation until an invariant, not another sweep, is
installed.
- **A cleanup that doesn't change the behavior that produced the mess is a rollback, not a
fix** — the same nested-mailbox-dir defect recurred and grew 9× (21→188 files) in a month
despite being "fixed" and swept at 21.
- **Checking your own artifact against the standard you just applied to someone else's catches
real defects** — CIO's, CXO's, and Arch's self-checks each found a genuine bug their own
praise-accepting would have missed.
- **A target date written into a note can quietly outrank the rule that produced it** — CXO
caught themselves nearly deferring a cron rotation to a stale "09-11" note over their own
sharper same-day rule.
- **Silent no-ops read as success if the tool's own failure signal isn't checked** — Lead's
carry-forward refresh script printed MISS while Lead logged "refreshed," caught only on
re-read.
- **A numerator with no stated denominator is indistinguishable from zero occurrences** — the
exact m-44 shape recurred inside a mechanism (the verdict-slot grep count) built
specifically to prevent that shape elsewhere.
- **Provenance must survive rendering unchanged** — CXO's #1738 framing, elevated same-day by
Arch to a joint architectural invariant: a render cap may shorten what the user sees, never
what the system believes it has.
- **Independent agents converging on the same wrong default is a stronger signal than one
person's mistake** — two unrelated seats (PPM, PA) reached the identical incorrect mailbox
path unprompted, which is what made the shape a shared-default problem rather than an
individual lapse.

---

*Sources: 14 session logs for 2026-09-10 (dev/2026/09/10/),
`dev/active/flywheel-v3-layer2-text-2026-09-10.md` (canonical text, read directly),
`dev/active/exec-cohort-attention-rollup-2026-09-10.html` and
`dev/active/in-review-test-round-2026-09-10.html` (Exec's afternoon deliverables, confirmed
by content match). Cross-reference gate: role-mention scan against all 14 logs found no role
mentioned without a corresponding session log. `decisions.log` checked directly and confirms
flywheel v3 ratification had not landed as of day's close, consistent with all session-log
accounts.*
