# Omnibus Log: September 30, 2026

**Day**: Wednesday
**Sessions**: 15 (Documentation Management, Lead Developer, Chief Architect, Communications
Director, Unicorn Web Designer, Head of Sapient Trust, Piper Alpha, Chief Experience Officer,
Principal Product Manager, Chief of Staff, Chief Innovation Officer, + 4 Coding Agent subagent
dispatches, three Phase 3 Inversion corpus-deposit lanes and one armed-offer fix)
**Day Type**: HIGH-COMPLEXITY: COORDINATION — the evening's PM-driven tape run surfaced that the
Inversion router had never actually served a live turn on alpha since 09-25 (a classifier-wrapper
kwarg mismatch the scorer's own layer couldn't see), triggering a same-night fix, deploy, and two
more shipped units; two cascade-seat LaunchAgent migrations (PA → seat 3, Docs → seat 4) each
produced real findings that Pard fixed at the generator level, benefiting every future seat; and
three separate round-trip coordination loops (Lead↔CXO↔PPM on PRIORITY/CALENDAR destination
questions, HOST↔CXO on #1174's visibility gap, Exec↔PA/Docs↔Pard on cascade-seat overlap timing)
each depended on a prior step being independently re-verified, not accepted on trust.
**Justification**: same-day PM redirect reshaping the evening (the tape run), multiple handoff
chains with real technical substance resolved through genuine back-and-forth, and a cross-role
correction propagating through infrastructure (the cascade migrations) — past EXECUTION's
independent-tracks threshold despite real portions of the day (five quiet fires on most roles)
being genuinely independent.

**Git Commits**: 70+ across all seats, including 4 alpha deploys (v152–v153 plus intermediate)

## Sources

Session logs: `2026-09-30-0527-docs-code-log.md`, `0627-arch-code-log.md`, `0639-comms-code-log.md`,
`0647-lead-code-log.md`, `0652-web-code-log.md`, `0700-host-code-log.md`, `0704-exec-code-log.md`,
`0712-pa-code-log.md`, `0717-cxo-code-log.md`, `0722-ppm-code-log.md`, `1007-cio-code-log.md`,
`2130-prog-code-log-1595-phase3-deposits-priority.md`,
`2145-prog-code-log-1906-arm-which-one-clarify.md`,
`2150-prog-code-log-1595-phase3-deposits-calendar.md`,
`2155-prog-code-log-1595-phase3-deposits-temporal.md`. Cross-reference gate: all 11 core roles
present; no stray `dev/active/` artifacts dated 09-30 beyond Docs's own auto-generated delta file.

## Executive Summary

### Core Themes
- **The Inversion router had never served a live turn on alpha since 09-25** — Lead's first real
  end-to-end probe through the actual app (not the scorer, which calls the LLM client directly)
  found `LLMDomainService.complete()` rejecting the router's `served=` kwarg (added 09-02 for
  #1620), silently falling every live consult back to legacy routing. A week of "live" claims had
  measured the router layer, never the app's call path — m-43's textbook case, by Lead's own
  framing. Fixed and deployed same night (v152); #1897 proven live via a real two-part turn.
- **PM's evening tape-run test card found and closed a real bug the same session it surfaced**:
  "Clear the first one" after "also clear the overdue reminder" re-entered classification with no
  carrier to bind it — the floor improvised a confirm outside the armed-offer family, so "Yes" had
  nothing to execute. Filed as #1906, armed (ordinal/status/name binding, all-or-nothing resolve,
  a genuine new carrier extending the existing `_act_on_resolved_targets` continuation rather than
  a parallel code path), and deployed within the same evening (v153).
- **Two cascade-seat LaunchAgent migrations landed, each producing a real cross-seat fix**: PA
  (seat 3) found the wrapper was injecting the whole prompt file (preamble, markers, everything)
  rather than the marked line on all seven LaunchAgent seats — fixed fleet-wide. Docs (seat 4,
  overnight into 10-01) found the generated prompt omitted a second worktree and the
  carry-forward-read instruction — fixed at the generator level (auto-detection + a per-seat
  extras file) before Comms or Web could hit the identical trap on their own future migrations.
- **Three Phase 3 Inversion corpus-deposit lanes ran in the same shared worktree overnight**
  (PRIORITY, CALENDAR_QUERY, TEMPORAL — 132 new corpus rows total, 151→283), each independently
  verifying every claim against the real production matcher rather than hand-deriving regex
  behavior, and each finding genuine structural-unreachability cases plus one new shadow shape
  (a TEMPORAL literal permanently shadowed by an entirely different, earlier-checked list).
- **Three genuine round-trip coordination loops closed with a verified correction on both sides**:
  Lead's PRIORITY/CALENDAR destination-question rulings went to CXO, who re-grounded against
  source and sent back two real splits; PPM then independently re-verified CXO's rulings rather
  than trust the table, catching the same "naive grouping hides a real split" shape for the second
  time in a week. HOST's #1174 check-in from CXO turned out to be a visibility gap, not a stalled
  one — both parties verified the other's claim before accepting it.

### Technical Details
- **`served=` kwarg fix**: `LLMDomainService.complete()`'s wrapper didn't accept the keyword the
  Inversion router passes (since #1620, 09-02); every live consult raised `TypeError` and silently
  fell back to legacy. Fixed with a passthrough plus a pin driving the router through the app's
  actual object, not a bypass. Alpha's own log confirmed the identical error at the exact timestamp
  of PM's earlier failed test. Consequence named explicitly: REMINDER/REMINDER_QUERY/TODO_QUERY
  phrasings had neither pattern coverage (deleted in Phase 3) nor a working router path from
  09-27 to 09-30 — PM's earlier dead-end test was exactly this gap.
- **#1906 (reminder-clear pick-target)**: the `named_target_unmatched` branch now arms a new
  `reminder_clear_pick_target` carrier (READ×PRIVATE, no new rail dispatch site). Binding resolves
  via ordinal → status-word → name-substring, in that priority order, with bounds-checking so an
  unrelated command's issue number never misreads as a position. A bound pick re-enters the SAME
  shared continuation (`_act_on_resolved_targets`, extracted from the original inline flow) a
  matched name would have reached — one source of truth, not a parallel code path. 28 new tests,
  including a self-caught early-draft mistake (a test accidentally exercised the real LLM-backed
  floor; rewritten to the turn-handler-seam idiom).
- **PRIORITY_PATTERNS deposits**: 38 of 43 unexercised literals given corpus rows (single
  destination, `get_top_priority`, FLOOR-disposed); 5 confirmed structurally unreachable (always
  shadowed by an earlier sibling in the same list). Verdict stayed NO-GO (FLOOR has no live flip
  group), which — a genuinely new finding — suppresses the gate's "needs a corpus row" section as
  a side effect, not evidence the unreachable literals got coverage.
- **CALENDAR_QUERY_PATTERNS deposits**: 46 of 49 literals covered across three live destinations
  (`meeting_time`/`recurring_meetings`/`week_calendar`, all WORKFLOW-disposed, sharing flip group
  `read_temporal`); verdict stayed GO, so the gate's "needs a corpus row" section correctly listed
  the 3 remaining unreachable literals by name — the opposite suppression behavior from PRIORITY's
  NO-GO case, flagged explicitly as a real divergence worth the Lead knowing. A genuine finding:
  the literal that *claims* a message and the literal that *determines its action* are independent
  checks — two rows route correctly only because of a collateral substring match, not the literal
  that claimed them.
- **TEMPORAL_PATTERNS deposits**: 48 of 54 literals covered (single destination,
  `get_current_time`, CANONICAL/floor-disposed, same shape as PRIORITY); verdict NO-GO and will
  **stay** NO-GO regardless of future coverage, since `get_current_time` has no WORKFLOW/flip-group
  registration and isn't in the router's own grammar — a disposition question for the Lead, not a
  corpus-coverage one. 6 unreachable literals found, 4 of them a new shadow shape (shadowed by a
  *different*, earlier-checked list — `CALENDAR_QUERY_PATTERNS` — not a sibling in TEMPORAL's own
  list). One self-caught bookkeeping mistake (a literal wrongly assumed already-claimed, corrected
  mid-session before it became a silent gap).
- **Corpus total**: 151 → 283 rows across the three lanes (+132), purely additive, each lane
  independently re-verifying the pinned corpus-size test constant and searching for other stale
  pinned-size references before declaring done.
- **Weekly Ship #062**: published blog-first this morning (after PM caught a real miss in
  yesterday's own routine — see 09-29's omnibus), then fully distributed same day once PM provided
  the LinkedIn URL. Thread fully closed within 24 hours of the piece going live.
- **§4e staging deploy pipeline**: PM set both Fly secrets and the `alpha` environment's required-
  reviewer rule (which hadn't saved on the first attempt — PM redid it, API confirmed). The first
  real (non-skip-path) staging deploy succeeded end-to-end; a concurrency-group burst produced 5
  correctly-cancelled runs in 90 seconds before the real one landed. #1849 (the deployment-pipeline
  epic) closes on this evidence.

### Impact Measurement
- Inversion router: dark on alpha for live routing from 09-27 to 09-30 (3 days), now proven live
  via a real e2e probe, not a scorer-layer claim.
- #1906: found, armed, tested (28 new), and deployed in the same evening — same-session
  discover-to-ship.
- Phase 3 corpus: 151 → 283 rows (+132) across three lanes; two of three lanes stayed NO-GO for
  structural (not coverage) reasons, now explicitly documented rather than silently reported as a
  gap.
- Cascade migrations: 2 of 11 seats complete end to end (PA seat 3, confirmed; Docs seat 4,
  confirmed 10-01 morning) — each closing with an independently-verified generator-level fix
  benefiting the remaining 9.
- Ship #062: published → fully distributed within the same calendar day.
- Board hygiene: 2 closures (#1559, #1897-proven) + 1 new milestone (#1907, 4 bundled live defects
  from PM's own iPad test-card session) same evening, re-verified clean after each change.

### Session Learnings
- **A green test/scorer result can measure the wrong layer entirely, and the only way to know is
  to probe the real call path** — Lead's own framing of the `served=` finding, now explicitly
  named as the week's textbook m-43 case: a passing score at the router/LLM-client layer said
  nothing about whether the deployed app's own object graph actually reached that layer.
- **A visibility gap and a stalled-work gap look identical from outside, and the fix for each is
  different** — HOST's #1174 resolution (both discovery docs converged the same day they were
  filed, just never reported back to the issue) is the same shape CXO independently named: "the
  work didn't age, its visibility did." Worth distinguishing explicitly rather than defaulting to
  either "it's fine" or "it's stalled."
- **Independent re-verification caught the same failure shape twice in one week** — PPM's note
  that this is the second time a naive same-bucket grouping in a source memo hid a real split
  (Monday's GUIDANCE setup-trio, tonight's PRIORITY sprint-view question) is itself worth keeping
  as a standing pattern, not a one-off catch.
- **A `git status` clean reading can measure stale local HEAD rather than the actual pushed
  state** — HOST's `mail-send.sh` mechanics finding (local ref doesn't auto-advance after a
  push-to-ref) is a real, reusable instance of "name the layer" applied to git plumbing itself.
- **Declining to execute a literal instruction and investigating instead can prevent a real
  misattribution** — Web's newsletter-CTA investigation (PM's "576→800" suggestion would have
  misattributed LinkedIn's growing audience to a different, dormant Buttondown list) is a clean
  instance of the investigate-before-extending discipline applied to a PM request directly, not
  just to internal process work.

## Timeline

- **04:12** (overnight, into 10-01) — see the cascade-seat-4 thread below; not part of 09-30's own
  wake window, included here only for continuity since the 09-30 STOP explicitly deferred it.
- **06:27** — **Arch** START. Mail: Pard declined to build a structural fix for a hypothetical,
  unmeasured race window, naming it in the failure text instead — Arch concurs (a certain defect
  gets fixed, a theory gets a diagnostic). Measures directly that `fly-deploy`'s green runs are
  still the skip path (staging `/health` unmoved) — a green checkmark isn't deploy evidence yet.
- **06:39** — **Comms** START (Opus 5.5). Confirms Ship #062 will publish today; re-verifies every
  PM-gated carry-forward row against its actual source rather than trust the carried framing —
  catches its own miss doing so: yesterday it asked PM to verify something its own 08-30 log had
  already answered ("Drained on Paper"). Added to its own standing-errors list.
- **06:47** — **Lead** START. Inbox: Docs's Step 1d nudge (09-27/28/29 logs genuinely closed but
  missing the literal marker) — fixed, plus a caught bug in the fix itself (an unquoted zsh glob
  silently did nothing on the first attempt; caught by grepping after the commit rather than
  trusting the command's silence).
- **06:52** — **Web** START. Notes `web-standing-items.md`'s "Recently Completed" section is ~8
  weeks past its own trim window — picks it up opportunistically rather than deferring again.
- **07:00** — **HOST** START. Fixes the same `DAY-CLOSED`-marker gap Docs nudged — checked format
  against a peer log before adding, confirmed exact syntax rather than guess.
- **07:04** — **Exec** START. Notes Ship #062's actual pubDate is today (double-checks the date
  rather than assume).
- **07:12** — **PA** START. Corrects its own briefing's MCP Architecture section, stale since
  09-26 ("still not deployed" → live units 0-4, PA's own ownership, current milestone counts).
- **07:17** — **CXO** START. Opens both GitHub-criteria issues directly rather than note
  "unchanged" again — finds #1174 genuinely stale-looking (19 days silent) and sends HOST a
  respectful, no-deadline check-in; finds #1108 differently shaped (unowned backlog, not
  person-blocked) and correctly takes no action.
- **07:22** — **PPM** START. Board hygiene clean, no delta.
- **~09:00** — **HOST** fire: investigates CXO's #1174 check-in properly rather than accept either
  horn — finds both discovery docs were filed the **same day** (09-11) and already cross-
  integrated; the real gap was that neither half was ever reported back to the issue itself.
  Posts the closing comment, replies to CXO naming the precise shape: "the work didn't age, its
  visibility did."
- **10:00** — **CXO** fire: **verifies HOST's claim independently** rather than take it at face
  value — pulls the actual GitHub comment and greps its own v0.2 doc for all three claimed
  cross-integrations, confirms genuine. Adopts HOST's framing, closes the standing-items row.
- **10:07** — **CIO** START (Opus 5.5). Quiet — #1174 already resolved by the time this fire reads
  the criteria line.
- **~13:00** — **HOST** fire: a real mail-send.sh mechanics finding — after a push, local HEAD
  doesn't auto-advance, so checking `git status` before fast-forwarding can show a "clean" reading
  that's actually measuring stale local state against the real pushed commit. A genuine m-43
  instance in git plumbing itself, not just application logic.
- **~13:16–15:52** — **Web**, PM-engaged directly (not a fire): investigates PM's "576→800"
  newsletter-copy suggestion rather than execute it literally — traces the actual signup mechanism
  to a third, dormant Buttondown list (not LinkedIn's growing 800 or Medium's ~28), re-confirms no
  credential exists, and surfaces that the literal edit would have misattributed one channel's
  audience to a different, unused one. PM's own question independently confirms a 09-20 audit's
  central open question ("does anything actually get sent?" — no). Recommends repointing the CTA
  at live channels as the zero-blocker path; holds the one real gating question (LinkedIn vs.
  Medium vs. both) open rather than guess.
- **~15:00** — **Exec** fire: PA is cascade seat 3 — LaunchAgent armed at `:47`, session cron held
  per the standard overlap discipline.
- **~15:17–15:52** — **Comms**, holding a read-only pre-check on PM's in-progress admin-UI edit to
  "Described Is Not Running" (10-03) rather than audit mid-edit — a version-drift precaution, same
  discipline Comms names explicitly from a prior week's lesson.
- **~15:47** — **PA**: first LaunchAgent fire lands. Reports two real findings to Pard: the whole
  prompt file is being injected (preamble + markers, not just the marked line — confirmed for all
  7 wrapper seats), and the session cron's actual landing minute is `:12`, not the registry's
  stated `:42` — inverting the assumed overlap order.
- **~16:12** — **PA**: the session cron's own slot fires 25 minutes after the LaunchAgent, finds
  nothing to do — direct evidence for Pard's "does the overlap cause duplicate work" question (no).
- **~17:1x** — **Pard → PA**: confirms both findings, fixes the whole-file injection fleet-wide
  (`e975929`), corrects his own overlap-order reasoning on the record.
- **~18:47** — **PA**: the 15:47 LaunchAgent fire logged `consumed (5 own commits)` — meets the
  standard. `CronDelete`'s the session cron, confirms `CronList` → "No scheduled jobs." Notifies
  Exec; flags one remaining mismatch (registry says `:42`, LaunchAgent fires `:47`) for the
  registry-flip.
- **~19:04** — **Exec** fire: flips PA's registry row — and corrects it, not just relabels the
  mechanism: the old row's stated minute was already wrong (`:42` vs. the real `:12`), fixed to the
  LaunchAgent's actual `:47` rather than compound the error.
- **~19:17** — **CXO** fire (one of three quiet, batched).
- **~20:52** — **Web** STOP: last scheduled slot of today, newsletter-CTA question correctly still
  held, unanswered, not blocking anything else.
- **21:04 → 21:4x** — **PM, direct with Exec**: asks why usage stayed under quota (answered from
  fresh `usage-audit.py` data, not estimated); approves a bounded tape-run for Lead (71%→90% stop
  line, Sonnet-default). Mid-writing-the-memo, Exec finds epic 0's queue is fully PM-gated on one
  token. PM corrects three stale items in Exec's own rollup read (droplet done, Ship #062 published
  **today**, crossposts caught up) — a new standing error logged: say today's actual weekday+date
  and check it, don't assume. PM approves Docs as cascade seat 4 and asks Docs to resolve two
  calendar rows — Exec re-verifies both are fresh (re-fetches `origin/main` after PM directly asks
  "are you checking origin main?").
- **21:17** — **Lead** fire, scheduled to be STOP — **becomes a tape run** once Exec relays PM's
  go-ahead. Dispatches three Phase 3 corpus-deposit lanes (PRIORITY, then CALENDAR, then TEMPORAL)
  while working PM's live test card directly.
- **21:1x–21:2x** — **Lead**: building the live-probe harness for #1897 finds the Inversion router
  has never served a live turn since 09-25 — the `served=` kwarg mismatch. **Fixed and deployed
  v152** same session; #1897 proven live via a real two-part dispatch.
- **21:2x–21:4x** — **Exec**: PM asks for a secrets walkthrough before signing off. Verifies live
  (not from memory) that `piper-morgan-staging-redis` already exists (an earlier step was stale,
  struck from the rollup) and that three GitHub-side steps remain.
- **~21:30** — **prog (PRIORITY lane)** dispatched by Lead: 38 of 43 unexercised literals deposited
  with real-matcher verification; 5 confirmed structurally unreachable. Flags an unrelated,
  concurrent, uncommitted change to `llm_domain_service.py` in the shared worktree (another lane's
  #1897 wiring) without touching it.
- **~21:3x** — **Lead**: PM's test card goes 3 passes (rows 11, 10, test 1; **#1559 closed**), 1
  real fail — **#1906** found (the unarmed "which one?" clarify). Dispatches a Sonnet lane to arm
  it. Dispatches a second lane for CALENDAR_QUERY deposits in parallel (disjoint files).
- **~21:45** — **prog (#1906 lane)**: arms the pick-target carrier, extends the existing resolved-
  target continuation rather than duplicate it, self-catches an early test draft that accidentally
  exercised the real LLM-backed floor and rewrites it to the deterministic turn-handler-seam idiom.
- **22:0x–22:1x** — **Exec**: **§4e staging pipeline proven** — PM sets both secrets and the
  `alpha` environment's required-reviewer rule (hadn't saved the first time, PM redid it); the
  first real staging deploy succeeds end-to-end after a 5-run cancellation burst (concurrency
  groups working as designed).
- **~22:0x–22:4x** — **Lead**: **#1906 landed and closed** (28 new tests); **TEMPORAL deposits
  landed** (48 rows, NO-GO — floor-disposed, no live flip group, a disposition question for
  later); **CALENDAR scored 24/46 → a description fix → 32/46**, changing live calendar behavior
  for the better; **alpha v153 deployed**. Corpus for the day: 151 → 283.
- **~21:50** — **prog (CALENDAR lane)** dispatched: 46 of 49 literals deposited across three live
  destinations; finds the claiming-literal/action-determining-match independence (two rows route
  correctly via a collateral substring, not the literal that claimed them); verdict stays GO,
  correctly surfacing its 3 unreachable literals in the gate's own output (the opposite suppression
  behavior from PRIORITY's NO-GO case).
- **~21:55** — **prog (TEMPORAL lane)** dispatched: 48 of 54 literals deposited; finds a new
  shadow shape (shadowed by a different, earlier-checked list, not a sibling); self-catches one
  bookkeeping mistake mid-session (a literal wrongly assumed pre-claimed); verdict NO-GO and will
  stay NO-GO regardless of coverage (CANONICAL disposition, same shape as PRIORITY).
- **22:17** — **CXO** fire, running long: two destination-question memos (PRIORITY, CALENDAR)
  arrive right at the STOP slot. **Drains both rather than defer** — reads `_handle_attention_query`
  and `action_registry.py` directly before ruling, splits rows a naive same-bucket grouping had
  merged, routes one genuine "does this feature exist" question to PPM rather than guess, and
  explicitly declines to answer CALENDAR's one live-turn-dependent question rather than rule past
  a gap it can't verify from its own seat.
- **~21:5x** — **PPM** fire: **answers CXO's routed question from a real roadmap/codebase search**
  (no sprint-priority view exists or is planned — a genuine "doesn't exist," not a search that
  failed), independently re-verifies CXO's other 8+8 re-score rows against source rather than trust
  the table, catches a new board-hygiene item (**#1907**, four bundled live render defects from
  PM's own iPad test-card session) within minutes of it landing, places it correctly in epic 9.
- **22:38** — **Exec** STOP: day fully drained (inbox 3→0, including Docs's cascade-seat-4 news
  and the calendar-row resolutions); day-0 `fly-deploy` count recorded for Pard (37 runs, 18
  success, 17 correctly cancelled); cron rotated.
- **~23:2x** — **Exec**: self-corrects its own earlier characterization to Pard ("~2-3 builds per
  burst" → the real count, 37 runs/18 builds in 90 min) — named as a lesson about counting the
  window rather than extrapolating from a brief observed sample.
- **~22:17–23:27 (Docs, continuing into 10-01)** — resolves Exec's two flagged calendar rows
  (Ship #058 a pure record gap, fixed; "Drained on Paper" confirmed still genuinely unresolved),
  builds the durable crosspost-mechanism follow-through, gets confirmation of cascade-seat-4
  arming from Pard, holds the session cron per instruction, STOPs for 09-30.
- **04:12 (10-01, documented here for continuity)** — the cascade-seat-4 verification fire lands
  exactly on schedule with the corrected prompt (both worktree paths + carry-forward instruction
  present); Docs retires the session cron, confirms `CronList` empty, tells Exec and Pard. Closes
  the three-fire cascade-seat-4 thread that began 09-30 evening.

## Cross-Role Coordination Notes

- **Lead↔CXO↔PPM, twice in one week**: a corpus-scoring table's same-bucket grouping hid a real
  split both times (GUIDANCE's setup-trio on Monday, PRIORITY's sprint-view question tonight) —
  caught only because CXO re-grounded against source rather than accept the grouping, and PPM
  independently re-verified CXO's own rulings rather than trust the memo. Three layers of
  verification, not two, is what caught it consistently.
- **HOST↔CXO on #1174**: a 19-day silence that looked like stalled work turned out to be a
  reporting gap — both discovery docs converged the day they were filed. Both parties verified the
  other's claim (HOST read both docs directly before replying; CXO pulled the actual GitHub comment
  and grepped the doc itself before accepting HOST's account) rather than take either side's word.
- **Pard↔PA↔Exec on cascade-seat-3 overlap timing**: PA's measured data (9-10 observed fires)
  inverted Pard's own assumed overlap order, and Pard said so plainly rather than let the
  correction go unacknowledged. Exec's registry flip then corrected a second, independent error
  (the row's stated minute was already wrong before the mechanism even changed) rather than just
  relabel the mechanism.
- **PM↔Exec on rollup accuracy**: PM corrected three stale items in one pass (droplet status, Ship
  #062's actual pubDate, crosspost status) and asked directly whether Exec was checking live state
  — Exec's answer was yes, and demonstrated it by re-fetching before answering, not just asserting.

## Discovered Work Filed

- **#1906** — Lead, from PM's live test card (the unarmed reminder-clear "which one?" clarify).
  Filed, armed, tested, and **closed same evening**.
- **#1907** — found during PM's iPad test-card session (four bundled render/layout defects), board-
  placed by PPM same evening (epic 9).
- No separate issues filed for the Phase 3 deposit lanes' structural findings (unreachable
  literals, the TEMPORAL CANONICAL-disposition NO-GO) — consistent with the established convention
  of reporting these inline/in the progress log rather than as new tracked bugs, since they're
  properties of existing regex ordering or action disposition, not new defects.

## Notable Process Findings

- **A green scorer result measured the wrong layer for three days** — the week's clearest m-43
  instance, caught only by a first-ever real end-to-end probe through the actual app rather than
  another scorer-layer check.
- **`mail-send.sh`'s local-HEAD-doesn't-auto-advance behavior produced a technically-clean but
  misleading `git status` reading** — HOST's finding, a genuine instance of "name the layer"
  applied to the mailbox mechanism's own plumbing, not just application code.
- **Two cascade-seat migrations in one day, two real generator-level fixes** — both PA's
  whole-file-injection finding and Docs's (overnight) missing-worktree finding were fixed upstream
  rather than patched per-seat, directly benefiting every remaining migration still to come.
