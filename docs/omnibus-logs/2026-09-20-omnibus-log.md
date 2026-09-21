# Omnibus Log: September 20, 2026

**Day**: Sunday
**Sessions**: 11 (Lead Developer, Documentation Management, HOST, Communications, Chief of
Staff (Exec), Chief Architect, Unicorn Web Designer (Web), Principal Product Manager (PPM),
Chief Experience Officer (CXO), Piper Alpha (PA), Chief Innovation Officer (CIO))
**Day Type**: HIGH-COMPLEXITY: COORDINATION
**Justification**: Three genuine cross-agent consensus/handoff chains reshaped the day's
direction rather than agents merely working independent tracks: (1) the `#1818` keyless-gate
saga — Arch ruled a predicate wrong, Lead's trace surfaced it, Arch self-corrected, CXO found
the resulting exempt set incoherent to users, Arch escalated an (a)-vs-(b) design choice to
PM, PM ruled, CXO delivered copy, Lead wired it, Arch confirmed scope with CXO at close; (2)
the cron-jitter investigation — Exec shipped a claim, falsified it on first test, CXO
independently found the same collapse, Web complicated both positions with a clean idle
sample, CIO found the whole question was already moot under an existing 45-minute grace
window and closed it; (3) a mid-day Amber host reboot that parked all 11 registry rows
simultaneously and required each seat to independently verify cron survival before
un-parking, producing a 4-seat cross-confirmed finding that contradicted the reboot runbook's
own premise. Layered on top: PM engaged directly and repeatedly (Docs twice, Arch once,
Lead's whole day via in-conversation rulings), a full release cut and blue-green alpha
deployment, and PM's first live dogfood session producing three trust-relevant defects that
cascaded through four roles same-day.
**Git Commits**: 437 (author-date window, `origin/main`)

---

## Chronological Timeline

### Early Morning: Publish, PM Engagement, and a Wrong Ruling Caught (06:26–07:41)

- **06:26**: **Lead Developer** opens START; day plan is `#1765` diagnosis first, then
  `#1764` → `#1812` steps 5–6 → `#1823`/`#1824`, with hosting the week's highest-leverage
  thread per Exec's sprint plan.

- **06:26–06:55**: **Lead** closes `#1765`+`#1813` — the local-vs-CI test divergence traced
  to exactly two causes (accumulated state in the shared dev Postgres; held credentials),
  both fixed with idempotent fixtures and explicit tier assignment. Three consecutive clean
  runs as proof.

- **06:30**: **xian (PM)** engages **Docs** directly, before the 06:57 cron: *"I was
  expecting to see the blog post already published."* Docs verifies rather than assumes —
  cron simply hadn't fired yet (27 min out), everything else pre-verified from the prior
  night.

- **06:30–06:33**: **Docs** publishes "From Abstraction to Example" immediately rather than
  making PM wait for the cron — full pipeline re-verified fresh at every step. Publish
  commits land 06:33:11/06:33:39 (later independently confirmed via commit timestamp by
  **Comms**).

- **06:31**: **PM** raises wanting duty cycles to start earlier (no later than 5am) but
  explicitly frames it as "a discussion for CIO or Exec," not a request to Docs — Docs
  correctly declines to unilaterally change its own cron cadence and flags it onward instead
  of acting.

- **06:41**: **HOST** opens Fire 1 — clean handoff from yesterday, Janne-invite hold still
  carried forward as the day's live thread.

- **06:42**: **Comms** opens START; corrects its own carry-forward mid-fire after PM catches
  an imprecision — the publish had happened 9 minutes before the fire reported it, not
  "overnight."

- **06:45**: **PM** catches a real post-publish defect neither the mechanical template-audit
  nor two independent human proofreads (Docs, Comms) caught: a typo ("towward") and a missing
  pull-quote treatment. **Docs** fixes both via the documented edit-pass mechanism and gives
  an honest diagnosis: no spellcheck step exists anywhere in the pipeline.

- **06:45**: **Exec** opens START and immediately falsifies its own overnight claim: the
  "+30/+31 min arrival offset" it shipped into the registry, its own carry-forward, and
  **Pard's** reboot runsheet the night before reads **+7** today. Exec traces the real
  mechanism to the tool's own documentation — jitter is capped at 15 min, and fires only land
  when the REPL is idle, so the "offset" was measuring Exec's own conversational load, not a
  scheduler property.

- **06:47**: **PM** asks **Arch** whether an earlier answer (Q5) got lost in relay. Arch
  searches and finds nothing was lost — PM's answer landed 09-18 directly in conversation;
  the confusion was Arch's own shorthand ("still yours: the Q5 one-liner") naming the parent
  item when only a child sub-question was open. Practice corrected.

- **06:52**: **Web** opens START; nearly drafts a counter-example to Exec's +30 retraction
  using "zero commits overnight" as proof of idleness — catches it before sending: a
  `WebFetch` tool-result file's mtime shows the REPL was actually occupied 4 minutes before
  the fire landed. Flags the underlying hazard to Exec: absence of commits cannot distinguish
  idle from mid-conversation.

- **06:54**: **PPM** opens START; sprint-truth clean, no board drift overnight.

- **06:57**: **Arch** opens its own fire and finds its `#1818` ruling from the night before
  (gate the keyless-message spend exemption on `ActionDisposition.CANONICAL`) was wrong —
  **Lead's** interim trace on the registry (dispatch-inert, zero call sites) was the thread
  that unraveled it. Arch reads the actual routing authority (`_requires_canonical_handler`)
  for the first time and finds `CANONICAL` means "the LLM can't do this alone," true of
  **all** of `EXECUTION`/`PORTFOLIO` (DB writes, issue creation) — the literal ruling would
  have opened a keyless path to issue creation. Corrects the ruling at all three surfaces
  (memo to Lead, the issue, an inline `decisions.log` marker) within the fire, before Lead's
  ratchet could encode the wrong premise.

- **06:59**: **CXO** opens START. The +30 offset it reported to Pard overnight also breaks —
  today's fire lands at +12. CXO's mandatory START re-verify finds three stale tracker rows,
  one materially so: a T-axis "closing window" Exec had relayed to PM as urgent turns out to
  be false (the MCP infra it referenced doesn't exist and never did); the `#1688` feature
  flag has been live in prod since 09-07, which CXO's own row had wrong two different ways in
  a row; `#1807` was already closed. All three corrected and sent to Exec/PA/PM.

- **07:01**: **PA** opens START; mail empty aside from one informational cc.

- **07:27**: **Docs** finds and fixes a gap from its own morning's publish work — the
  typo/pull-quote fix had landed on the website repo but never actually got committed to the
  product repo's archived source copy.

- **07:40**: **Docs** finds the 09-19 omnibus (a 12-session HIGH-COMPLEXITY day) was never
  written, dispatches a subagent draft, then independently re-verifies rather than trusting
  its self-report — catches and fixes 3 real chronological defects, the largest a ~2-hour
  mislabel traced to a memo's actual `git log` commit timestamp rather than a session log's
  own end-of-day summary framing.

### Mid-Morning: The Release Cut, Alpha Deployment, and the Corrected Ratchet (07:41–10:55)

- **09:17**: **Lead's** 09:17 fire drains 8 memos including Arch's URGENT `#1818` correction
  and PM's approval of the droplet plan's Step 3 (cut a proper release before archiving) —
  PM's real driver named for the first time: the droplet was superseded by July's Fly
  migration and has been costing money for two months with no one shutting it down. PM also
  tasks Arch with a real deployment-pipeline plan, stated top priority.

- **09:17–10:15**: **Lead** cuts **v0.8.12.0** ("Your Key, Your Account") — DB backup first,
  14,308 tests collected, full 3a–3i doc checklist with prose rewrites, `production` fast-
  forwarded from 13,209 commits behind to converged. Droplet deploy then **blocks at the
  permission classifier** — three SSH shapes denied; Lead stops and reports to PM with exact
  remaining commands rather than working around the denial.

- **09:35–09:55**: **PM unblocks** by hand-creating a scoped `.claude/settings.local.json`.
  **Lead** executes the blue-green deploy: a pre-swap check catches that
  `uploads/`/`data/redis`/`data/chromadb` are bind mounts the repo's skeleton dirs had
  masked; recovers from a dead `orchestration` service reference in `docker-compose.yml`
  (`#1835` filed); ~7 min downtime. **v0.8.12.0 verified live on alpha** at every layer named
  (VERSION, alembic head, `/health` 200, login 200). Exec report sent cc PM/Pard/HOST/Arch.

- **09:41**: **HOST's** Fire 2 reads the same mail — notes the release-cut script touched
  `email-template.md` incidentally, verifies via `git log` it's not a deliberate fix for the
  still-open onboarding-footer issue (`#1830`), leaves it open.

- **09:47**: **CXO** re-checks the offset: confirmed, +12 twice on the rotated job vs. +30
  five-for-five on the prior one — the only seat with a completed rotation before/after. Also
  judges Arch's newly-escalated `#1818` design question: literal option (b), a uniform
  "refusal that greets," breaks on "bye" (reads as not understanding, not policy) — proposes
  acknowledging in kind first via the pre-classifier, which already separates
  greeting/farewell/thanks for free.

- **09:0x–09:1x**: **Web** ships `website#43` on PM's explicit GO (*"100% approve... ASAP!"*)
  — 240 MB of build-tool PNGs moved out of the deployed path, verified both directions
  (pre-commit rename-parity, post-deploy 404-on-old/200-on-webp, live browser render with 0
  console errors). A shell-quoting bug silently fails the first commit attempt; caught by an
  inconsistency between two command outputs in the same block, redone clean.

- **09:52**: **Web** reports the day's first clean idle jitter sample: +30m11s, idleness
  established correctly this time (last-tool-call time + absence of tool-result writes, not
  commit absence). This both strengthens CXO's per-job-determinism read and undercuts Exec's
  cap-based "it was never jitter" inference — an idle fire can still exceed the documented
  15-minute cap.

- **09:54**: **PPM's** WORK fire independently catches the same `#1818` near-miss CXO and
  Arch already found — folds the corrected ruling into epic 2's tracking before Lead's
  ratchet could build against the wrong premise, and separately answers PM's product-writing
  question (should Piper Morgan scaffold its own file-writing) directly: yes, discriminator
  is downstream audience, not who asked.

- **10:05–10:40**: **Lead**, authorized by PM to continue post-deploy, builds Arch's
  corrected ratchet as the actual **definition** of the spends-nothing set — drives all 14
  registry-`CANONICAL` pairs keyless. **Measured result: only 5 of 14 are actually spend-
  free.** `thanks`/`farewell` bill via the conversational floor (LLM-composed), confirming
  `#1773`'s registry-drift finding with billing evidence. Findings sent to Arch/CXO.

- **10:27**: **Docs** catches and self-corrects a near-miss before sending — initially routes
  a cross-project reply by creating a dead `mailboxes/dispatch-pm/` directory, exactly the
  mistake the routing docs warn against by name; catches it before sending, redoes it via the
  documented relay-via-Exec convention.

- **10:37**: **CIO** opens START. The overnight jitter thread has moved fast — CXO's rotation
  disconfirmed the "systemic +30" framing CIO itself had adopted into the registry the night
  before. CIO checks whether the underlying problem was ever real before writing a
  correction: `FIRST_FIRE_GRACE_MIN` already defaults to **45 minutes**, comfortably wider
  than every offset anyone has reported. **CIO's own overnight registry edit had solved a
  problem that didn't exist** — reverts it, sends one consolidated ruling closing the thread
  cohort-wide.

### Late Morning: Registry Corrections, Namespace Fix, and Pre-Registered Plans (10:50–12:59)

⚠️ *Chronological note: Arch's entry below spans 09:57 (fire start) to 12:57 (PM's approval) —
placed at the end of this section by its outcome time, not its start time, since that's the
moment the thread resolves and the section's own range ends at 12:59. Its start genuinely
precedes this section; flagged rather than silently reordered around.*

- **10:37 (cont.)**: **CIO** also implements PM's dispatch-tier logging ruling (relayed via
  Exec) into CLAUDE.md's Subagents section, and closes its own long-standing "no GitHub-
  criteria line" gap.

- **10:50–11:10**: **Lead** closes `#1764` — a silent DB-keychain namespace collision made
  loud with a construction guard, migration plan documented on the issue.

- **12:17–12:50**: **Lead's** fire catches a duplicate cron at open (its own delete/re-arm
  pattern racing across the morning's lanes — methodology-35's *"Asymmetric Discipline —
  Operational Rules with Creation Without Paired Cleanup"* shape) and parks `#1818` on PM's
  pending (a)-vs-(b) call while pre-registering `#1812` steps 5–6's execution plan in full,
  including a newly-discovered second consumer face.

- **12:41**: **HOST's** Fire 3 reads Lead's alpha-deploy report in full and **rules the
  invite hold does not lift on deploy health alone** — re-reads its own 09-14/09-15 bar
  directly rather than from memory: this invite has twice required an actually-driven BYOC
  flow (registration, stored key, real 401), which deploy-health checks don't demonstrate.
  Names two paths to close it.

- **12:52**: **Web's** fire unblocks a Vercel API token idle 11 days — probes scope before
  any number, finds deployment-storage GB genuinely unobtainable with this token (not a
  false negative), but measures 7 retained deployments and flags that `website#43`'s effect
  arrives over ~a week, not immediately. Also catches and corrects its own prior conclusion
  on the `integration-reveals-all` workDate: PM's archive confirms the flagged date (June 27)
  was **correct all along** — Web's proposed "blank it if uncertain" fallback would have
  destroyed a genuinely correct value. Traces the error to asking PM to *recall* a date
  instead of asking *where the authoritative record lives*.

- **09:57–12:57 (Arch)**: **Arch's** 09:57 fire ships the PM-tasked deployment-pipeline plan
  v0.1 (diagnosis: the build system and the "released" marker track different things;
  `/health` reports a hardcoded, wrong `"environment": "staging"`). PM approves it whole at
  the 12:57 fire, including the held `/health` item. Arch builds the real deploy identity
  (`#1839`) and discovers the fix is bigger than the brief: `/health` has been lying about
  its environment for months.

### Early Afternoon: PM's Dogfood Session and the (b) Ruling (12:59–15:57)

- **~13:0x**: **PM**, in-conversation with Lead, confirms `#1812`'s embeddings sponsor and
  approves the deployment-pipeline plan (`decisions.log`, verbatim).

- **~13:3x**: **PM rules `#1818` = option (b)** — *"yes (b)"* (`decisions.log`, verbatim:
  "the refusal-that-acknowledges: NO spends-nothing exemption at the gate... every keyless
  first message gets a warm response that acknowledges the message in kind... AND explains
  the key requirement"). No exemption machinery gets built; the measured ratchet stands as
  fact-keeper, not gate wiring. **Lead** relays; **CXO** owns the acknowledge-in-kind copy;
  **Lead** wires the dispatch.

- **13:0x–14:0x**: In the same conversation, **PM's first real dogfood session on alpha**
  surfaces three defects. **`#1836`**: the standup edit path claims *"I've updated your
  standup"* while returning the verbatim unchanged draft — a live `#1331` anti-confabulation
  violation, in front of the founder. **Lead fixes it the same hour** (diff-derived honesty
  at the edit seam, 3 regression tests). PM's structural read goes further: the fabricated
  template is `#1289`'s undead fallback promoted to default, and offer-acceptance never arms
  the interview — filed as **`#1837`** with a three-shape ruling request to Arch. **`#1838`**
  (Settings round-trip orphans the chat) also filed.

- **12:55**: **PPM's** fire homes all three: `#1836` to epic 5 as trust-critical top
  priority, `#1837` to both epic 3 and epic 5 — and catches a real dependency-chain
  consequence: epic 3's floor was gated only on PM's `#1617` retest, but today's attempt
  shows that retest is unreachable until `#1837`'s interview-arming lands first. Flags this
  explicitly to Lead rather than let the epic file silently imply the old blocker still held.

- **~12:5x**: **CXO** delivers the `#1818` copy set — one shared constant, four kind-matched
  prefixes (greeting/farewell/thanks/neutral), `thanks` deliberately not saying "you're
  welcome" since nothing was actually done — unblocking Lead's wiring. Flags two open
  decisions (repeat-turn copy; whether (b) supersedes `#1823`'s branch-one string) rather
  than deciding them unilaterally.

- **14:1x**: **Lead** opens `#1812` Phase B and finds a **second consumer face** on contact —
  None-return consumers beyond Arch's original enumeration, meaning `LLMClient`'s server-
  keyed clients lose their last consumer entirely. Deliberately holds the diff to land whole
  in a fresh context rather than cut mid-marathon-file at the tail of this one — names the
  trigger explicitly.

- **14:45**: **Exec's** fire reads **Janus's** amended concurrence on the jitter question —
  Janus retracts its own position in favor of a sharper rule ("deadlines from empirical
  history only when the measurement condition matches the application condition") — and
  surfaces a consequence for Exec's own earlier usage-share analysis: commit-count-based load
  measurement is blind to conversational load, understating Exec's real share.

- **15:17–15:50**: **Lead's** fire has HOST's hold accepted and CXO's copy delivered; two
  classifier refusals (hand-INSERT and read-only SELECT on the users table, both correctly
  blocking direct DB access) redirect Lead toward a stronger method — mint a throwaway invite
  token and drive the full real registration path instead.

- **15:41**: **HOST's** Fire 4 holds a boundary on its **own** side: declines Lead's offered
  framing that HOST should run a read-only PM-identity DB query, re-reads the trust-zone
  split's exact text ("HOST never touches the DB" is a separate prohibition, not contingent
  on read-only-ness), and redirects the ask to PM directly instead.

- **15:42**: **Comms** reads Web's self-correction confirming the flagged workDate
  ("Integration Reveals All," June 27) was correct all along — the PM-archive-location audit
  thread Comms opened remains open, unresolved for now.

- **15:55**: **PPM** folds in CXO's two refinements to the file-writing question (asymmetric-
  cost default: scaffold when audience is unknown; the completion *claim* must match artifact
  state, or scaffolding alone doesn't fix confabulation) directly into `#1836`'s tracking.

- **15:57**: **Arch** catches a security near-miss in its own morning's `/health` change —
  the environment-docstring rewrite would have let an operator set `PIPER_ENVIRONMENT=prod`
  (wrong vocabulary) and silently disarm three security gates comparing on the exact string
  `"production"` (`encrypted_types.py`, `jwt_service.py`, `env_hygiene.py`), re-opening the
  plaintext-tester-PII hole `#1387` exists to close. Nothing shipped to a host; fixed same
  fire; documented on `#1839` rather than quietly amended.

### Afternoon: Buttondown, Heartbeat Fix, and a Contract Tested Live (15:57–18:53)

- **15:52**: **Web's** fire ships the Buttondown signup-options audit PM asked for — the gap
  collapses to one PM-only question (does anything actually get sent to subscribers today; no
  send mechanism exists in either repo). Catches two of its own wrong checks (a titles-only
  search that would have reported 0 template-relevant posts against a true count of 98; a
  redirect misread as a broken link) before sending either.

- **~15:52 (CXO)**: **CXO's** fire tests its own 09-10 acceptance-contract against PM's live
  dogfood transcript for the first time — finds turn 4 already ruled by an existing clause
  (Piper's "Not quite" was untruthful; it had offered the interview three turns earlier) but
  turn 2 exposes a real gap in its own enumeration: PM's affirmative was silently captured by
  the wrong flow rather than either of the two cases the contract anticipated. Amends the
  contract to v1.1 as a dated addition rather than a silent edit, naming its own
  incompleteness explicitly.

- **16:01**: **PA's** fire takes on PM's high-priority usage-correlation-model tasking — runs
  four `WebSearch` passes across distinct fields that converge on the same answer (a
  calibration subsample against ground truth is required), and finds the most load-bearing
  fact internally: Lead's own PM-reaffirmed calibration proposal has zero rows captured to
  date.

- **16:37**: **CIO's** fire fixes a real bug **Web** found and reported in `duty-cycle-
  heartbeat.sh` — the suppressed-row marker push could fail silently and strand a commit
  exactly on the surface the sign-off checklist depends on. Retry loop added (mirroring
  `mail-send.sh`'s pattern), tested live on both code paths, confirmed clean.

- **18:42**: **Comms's** fire syncs and finds its own duty-cycle row **parked** — Exec parked
  all 11 registry rows ahead of a coordinated Amber reboot per **Pard's** runsheet.
  Investigates rather than assumes: re-runs `CronList` twice, finds the **same** job id as
  last night's STOP, not a fresh one — concludes its own cron likely survived the reboot
  untouched, un-parks per the strict clearing condition, and reports the finding as a second
  confirming data point alongside **Exec's** own identical finding on its own seat.

- **18:53**: **HOST's** Fire 5 delivers the day's central resolution: **Lead** drove the full
  real BYOC path on alpha — throwaway invite token, real `#1344`-gated registration, real
  Settings-API key store (which live-rejects a low-entropy fake key before accepting a valid
  non-billable one), a substantive turn producing a real 401 from Anthropic proving the
  stored key was selected and transmitted. **HOST independently verifies before ruling** —
  checks `#1824` is genuinely open, greps both quoted log lines against source at HEAD rather
  than trusting the paraphrase. **HOLD LIFTED.**

### Evening: The Amber Reboot and Its Aftermath (18:38–21:57)

- **18:38:39**: Amber host reboots (`sysctl kern.boottime`, independently confirmed by Exec,
  CIO, and cross-referenced by Comms/Web/CIO/PPM).

- **18:51**: **Exec's** fire discovers its own cron **survived** the reboot with the same job
  id, firing 13 minutes post-boot — directly contradicting the runsheet's premise that "a
  reboot kills every cron." Sends the finding to Pard/Janus before acting further, explicitly
  not claiming it generalizes from one seat. Separately, the watchdog catches a real defect
  in Exec's own park text from two hours earlier: no falsifiable deadline was attached to any
  of the 11 parked rows, so a stalled row and a healthy one would look identical. Fixed same
  fire — all 10 remaining parked rows get computed deadlines.

- **18:51–19:05**: **Lead**, resuming after an interrupt, finds its own 09:17 mail-triage
  batch never fully landed on origin (8 inbox deletions silently dropped while the
  corresponding read/ additions and new replies landed) — the cohort saw Lead's inbox as
  13-unread for ~9 hours despite a reported-successful send. Repairs it in two sends; files
  **`#1840`**.

- **18:52–18:53**: **Web** confirms its own model identity shifted mid-session (Opus 5 →
  Sonnet 5, per the harness's own system block, unrequested) — flags it as an observed fact,
  not an escalation.

- **18:53**: **PPM's** fire finds its own row parked mid-cycle, deliberately re-arms anyway
  (rather than trust the ambiguous "still alive" signal) to produce unambiguous evidence for
  the reboot runsheet's own clearing condition, and un-parks with the honest sequence on
  record.

- **19:18**: **Arch** resumes from a mid-day compaction and immediately discharges the two
  items it had deliberately held for "a fresh session" as the named trigger: independently
  re-verifies all three of **Lead's** `#1837` architecture calls against source (CONCUR on
  all three) and independently re-verifies **Exec's** droplet archaeology against
  `decisions.log` before building on it — confirms the droplet is an unfinished July
  migration, not a live architecture choice, and rewrites plan §4 into an actual completion
  path (v0.2): under an environment-vs-stage vocabulary, alpha and beta become access-list
  decisions against the one Fly `prod`, not an infrastructure build.

- **19:18 (cont.)**: **Arch** also answers **CXO's** routed `#1818`/`#1823` supersession
  question in the same fire: (b)'s greeting copy wins on first contact only; `#1823`'s gate
  string still governs turn 2+ substantive requests, preserving one-policy-one-string-per-
  layer.

- **21:26**: **PM engages Docs via remote-control**, having prepped Tuesday's post ("The
  Near-Miss and the Missing Key") with Comms's edit pass already done. Docs runs a full
  independent proofread (16/16 template-audit) and fact-checks the root-cause claim directly
  against `website#35` rather than trusting the draft's own citation, confirming the draft's
  hedge language is accurate to the issue's own unresolved state. Pre-derives the publish
  cluster and writes a durable plan for Tuesday's actual pubDate. *(Comms's own editorial
  review of the same post — 16/16 audit, fact-checked harder than usual since the piece is
  self-implicating — had completed earlier the same evening, before this handoff; both
  proofreads independently reach the same clean result.)*

- **21:42–21:57**: **Comms** and **Arch** each independently investigate their own parked
  registry rows before un-parking, finding the same job ids survived unchanged across the
  entire claimed reboot window on their seats — both explicitly write per-seat findings
  rather than generalize, noting HOST's row shows the same non-event.

- **21:52**: **Web's** STOP fire finds its own row was parked mid-session too — reports a
  fourth data point on cron survival, with the added wrinkle of the unexplained model-
  identity shift riding along, explicit that it cannot distinguish "wasn't rebooted" from
  "resumed without clearing cron state."

- **21:57**: **HOST's** Fire 6 records the day's full arc; **Exec's** STOP fire confirms the
  reboot-survival premise falsified at **n=4** across Exec/Comms/Web/CIO, and that Janus has
  retracted two of its own cron claims on the strength of the accumulated evidence.

### Night: STOP and Day Close (21:57–22:52)

- **21:57**: **Arch's** STOP fire closes first, after investigating its own parked row rather
  than accepting the reboot framing at face value — cron re-armed via delete-then-create-
  then-verify, integrity of the shared registry TSV confirmed before trusting its own edit
  had landed cleanly.

- **22:12**: **PA's** STOP fire closes the day — six fires, three genuinely substantive, no
  cron duplicates or gaps.

- **22:17**: **CXO's** STOP fire closes the last open thread — Arch's sharper turn-2+ `#1823`
  scope split adopted without qualification, tracker folded.

- **22:22**: **PPM's** STOP fire finds and board-adds `#1840` (Lead's half-landed mail batch,
  folded into the `#1731`/`#1746` mail-send-silent-drop family PPM has tracked since 09-18) —
  the sixth board-add fix of the day.

- **22:27**: **Docs's** STOP fire closes clean — two of Comms's evening memos arrive after
  Docs's own independent work was already complete; replies confirm the crossed wires,
  nothing further owed.

- **22:37**: **CIO's** STOP fire is the 4th seat to independently confirm cron-survival-
  through-reboot on its own row (job unchanged, offset unchanged across the boot), explicitly
  declines to re-arm a healthy surviving job to avoid manufacturing the exact duplicate-
  stacking failure the runsheet exists to prevent.

- **22:52**: **Exec's** STOP fire closes the day's arc: Janne's invite hold lifted for good,
  the Fly/droplet question resolved into an access-list decision one word-choice away from
  PM, and the reboot-premise falsification confirmed at n=4 — plus Exec's own park-text
  defect, caught and fixed by the watchdog within two hours of being written.

---

## Executive Summary

### Core Themes

- A full release cut and blue-green alpha deployment (`v0.8.12.0`) executed same-day, ending
  a multi-week-old droplet-currency gap, with a real cutover defect (dead `orchestration`
  service reference) caught and recovered live.

- The `#1818` keyless-gate design ran its complete arc in one day: a wrong structural ruling
  caught by a colleague's trace before it shipped, a corrected measurement (5 of 14
  registry-`CANONICAL` pairs are actually spend-free), a PM design ruling, delivered copy,
  and same-day wiring — four roles in sequence, no step skipped.

- PM's first live dogfood session on alpha surfaced three real trust-relevant defects
  (`#1836`/`#1837`/`#1838`) that cascaded through Lead, PPM, CXO, and Arch same-day,
  including a live violation of the project's own anti-confabulation rule (`#1331`) fixed
  within the hour.

- A genuine cross-agent scientific correction chain on cron-arrival jitter — three successive
  claims shipped, each falsified or complicated by the next agent's independent check,
  resolved when CIO found the entire question was already moot under a shipped 45-minute
  grace window.

- A mid-day Amber host reboot parked all 11 registry rows simultaneously; the cohort's
  independent, source-verified un-park investigations produced a 4-seat cross-confirmed
  finding that contradicted the reboot runbook's stated premise ("a reboot kills every
  cron").

- The Janne-invite hold, open since 09-14, was lifted for good after HOST held the line
  twice against a lower bar (deploy health) and independently verified the actual driven
  BYOC evidence down to source line citations.

### Technical Details

- `v0.8.12.0` cut and deployed to alpha; `production` branch fast-forwarded from 13,209
  commits behind to converged; `#1835` filed for the dead `orchestration` service reference
  masked in `docker-compose.yml`.

- `#1765`/`#1813` closed — local-vs-CI test divergence root-caused to accumulated fixture
  state and held credentials, fixed with idempotent fixtures and explicit tier assignment.

- `#1764` closed — DB-keychain namespace collision made loud with a construction guard;
  migration plan documented, not yet executed.

- `#1818`'s corrected ratchet measured 5 of 14 registry-`CANONICAL` pairs as actually
  spend-free; `thanks`/`farewell` route through the LLM-composed conversational floor and
  bill, confirming `#1773`'s drift with billing evidence.

- `/health` deploy identity built (`#1839`): version/SHA/environment now report `"unknown"`
  rather than a fabricated `"staging"` label that had been live and wrong for months.

- A security near-miss in Arch's own `/health` docstring (would have let an operator disarm
  three plaintext/production security gates via a vocabulary mismatch) caught and fixed
  same-day, three hours after introduction.

- `website#43` shipped — 240 MB of build-tool PNGs moved out of the deployed path, verified
  pre- and post-deploy including live browser render.

- `duty-cycle-heartbeat.sh`'s suppressed-row marker push bug fixed (retry loop mirroring
  `mail-send.sh`'s pattern) after Web reproduced it twice.

- `#1836` (standup false-completion claim, live `#1331` violation) fixed same hour with
  diff-derived honesty at the edit seam; `#1837` (accepted interview offer never arms) filed
  with a three-shape architecture ruling request, CONCUR from Arch; `#1838` (Settings
  round-trip orphans chat) filed.

- `#1840` filed and fixed — an 8-memo mail-triage batch half-landed on `origin/main` for ~9
  hours before Lead caught and repaired it.

- CXO's user-facing acceptance contract amended to v1.1 after its first live-transcript test
  found a real gap in its own case enumeration.

### Impact Measurement

- 437 commits landed on `origin/main` in the day's author-date window.

- Six board-add fixes across the day (`#1835`, `#1836`, `#1837`, `#1838`, `#1839`, `#1840`)
  — PPM's `piper-draft-issue` board-add fix from 09-19 held cleanly across all of them.

- One blog post published end-to-end with a real post-publish defect caught, diagnosed, and
  fixed; a second post fully proofread and queued for its actual pubDate.

- Four independent seats (Exec, Comms, Web, CIO) cross-confirmed the reboot-survival
  finding; Janus retracted two of its own prior claims on the strength of it.

- Three roles (Exec, CXO, CIO) each shipped and then corrected a wrong claim about the
  cron-jitter mechanism within the same day, each correction delivered before it caused
  downstream harm.

- One multi-day thread (the Janne-invite BYOC hold) closed after four separate evidentiary
  passes since 09-14, the last one meeting a bar the deploy alone did not.

### Session Learnings

- The day's sharpest recurring pattern: **a name is not a definition** — Arch's `#1818`
  error came from trusting a registry comment and a disposition's name over reading the
  actual routing-authority function; caught the same way `#1773`'s drift was caught, the
  fifth instance of the same "honest-empty" family in eight days.

- **Independent re-verification against source, not a colleague's summary, was the
  load-bearing move all day** — HOST verified Lead's log-line citations against HEAD before
  lifting the hold; Arch re-verified Exec's archaeology against `decisions.log` before
  building on it; CIO checked whether its own "fix" solved a real problem before shipping it
  (it didn't).

- **A stable-looking measurement can still be the wrong inference**: three agents (Exec,
  CXO, CIO) each drew a systemic conclusion from a real, repeatable number, and each was
  wrong about what the number meant — repeatability felt like validity but wasn't.

- **Checking whether an existing mechanism already covers a question, before building a new
  one, was the actual lesson of the jitter thread** — not the jitter mechanism itself, per
  CXO's own framing at close.

- **A parked registry row with no falsifiable deadline is indistinguishable from a
  genuinely stalled one** — Exec's own park text lacked this and was caught by the watchdog
  within two hours, not by Exec's own review.

- **PM's live dogfood session outperformed a week of design inference** — CXO's acceptance
  contract, untested against a real transcript since 09-10, found a genuine gap in its own
  enumeration on first contact with live behavior.

- Two same-day near-misses were caught by process discipline rather than luck being absent:
  Docs's dead-letter mailbox mistake (caught before sending, then correctly avoided on the
  very next occurrence) and PPM's catch of Arch's wrong `#1818` ruling before Lead's ratchet
  could build against it.

- The day closed with every one of the 11 registry rows independently re-verified against
  live `CronList` state rather than the reboot runsheet's own assumed premise — the
  mechanical form of "verify, don't guess," applied at fleet scale under a genuine,
  unplanned infrastructure event.

---

## Notes on Synthesis

- **Step 2.5 (Cross-Reference Gate)**: All 11 source logs mention only roles within the
  11-role source set, plus three cross-project/infrastructure entities without session logs
  in this repo — **Pard** (Amber host-infrastructure coordinator), **Janus** (cross-project
  hub), and **Dispatch-PM** (a cross-project agent, referenced once by Docs). None of these
  carry Piper Morgan session logs by design; their mentions are cross-project mail traffic,
  not missing-log signals. `dev/active/` for 2026-09-20 contains only per-role delta files, a
  cohort-attention rollup HTML, a pre-registered execution plan, and a prior-art research doc
  — all attributable to roles already in the source set. **Gate: PASS.**

- **Step 2.6 (Cross-Role Mentions Verification)**: Spot-checked the `#1818` correction chain
  against `decisions.log`'s own timestamped entries (09:0x correction, 13:0x/13:3x PM
  rulings) — consistent across Arch's, Lead's, CXO's, and PPM's independent accounts.
  Spot-checked the reboot boot time (`kern.boottime Sun Sep 20 18:38:39`) across Exec's and
  CIO's logs — identical. Spot-checked Docs's publish-timing correction (06:33:11/06:33:39)
  against Comms's independent `git log` verification of the same commits — consistent. No
  unresolved cross-role discrepancies found in this pass.

- **Step 7 (Canonical References)**: `methodology-35` (referenced by Lead as "the
  methodology-35 shape" for its duplicate-cron pattern) opened and quoted verbatim above:
  *"Asymmetric Discipline — Operational Rules with Creation Without Paired Cleanup."* No
  ADR/PDR was ratified or cited as ratified law this day; Docs's own 09-19 omnibus-
  verification note that "ADR-070" does not exist in any source log is recorded in Docs's own
  session log, not repeated here as a citation.

**Chronological-ordering discipline**: entries above are ordered by each fire's own stated
arrival time, not by the role's narrative sequence within its log — e.g. Web's Vercel-unblock
and workDate-correction content (its 12:52 fire) is placed near HOST's 12:41 entry rather
than beside Web's later Buttondown work, and Comms's evening editorial review is placed
before Docs's 21:26 handoff per Docs's own log stating Comms's pass was "already done" by
then, not from either log's end-of-day summary. No entry's clock position was inferred from a
summary paragraph.

