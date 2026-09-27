# Omnibus Log: September 26, 2026

**Day**: Saturday
**Sessions**: 17 (Documentation Management, Chief of Staff, Chief Architect, Communications
Director, Lead Developer, Chief Experience Officer, Head of Sapient Trust, Piper Alpha, Principal
Product Manager, Unicorn Web Designer, Chief Innovation Officer, + 6 Coding Agent subagent
dispatches: MCP Phase C units 0/1/2, #1595 unit 4, #1772 guard, MCP OAuth AS)
**Day Type**: HIGH-COMPLEXITY — multiple parallel coordination threads (usage-throttle fleet
response, a fleet-wide git-attribution incident with a same-day correction cycle, a cohort-wide
personhood/attribution investigation) running alongside a full multi-unit MCP Phase C build and a
Ship #062 metrics-verification saga spanning most of the day.
**Justification**: 17 sessions, 5+ genuinely distinct coordination threads each touching multiple
roles, a design ruling, and a completed 5-unit feature build — well past STANDARD's single-thread
scope.

**Git Commits**: 150+ across all seats (Lead alone: ~35 main-repo commits + 6 deploys)

## Sources

Session logs: `2026-09-26-0521-docs-code-log.md`, `0536-exec`, `0627-arch`, `0642-comms`, `0642-lead`,
`0650-prog-mcp-unit0`, `0652-cxo`, `0705-prog-mcp-unit1`, `0707-host`, `0712-pa`, `0722-ppm`,
`0755-prog-mcp-unit2`, `0855-web`, `0900-prog-1595-unit4-build`, `1007-cio`, `1150-prog-1772-guard`,
`1305-prog-mcp-oauth-as`. Cross-reference gate: all 11 core roles present; no stray `dev/active/`
artifacts from an unaccounted role (one system-generated Docs delta file, not substantive).

## Executive Summary

### Core Themes
- **A fleet-wide usage-throttle directive** (PM: 20% of the week's credits burned in 31 hours) drove
  every role to cut duty-cycle cadence 40-50% at START — the day's one action every session took.
- **A real fleet-wide git-attribution incident**, caused by Pard's own identity fix leaking into the
  shared `.git` config, mislabeled 231 commits across all 11 seats for ~17 hours — corrected twice
  in public by the person who caused it, with several roles independently re-verifying their own
  exposure rather than trusting the count.
- **MCP Phase C was built and shipped end-to-end in one day**: five units (skeleton → identity →
  resources → OAuth authorization server), each landing live with a real bug found and fixed by
  testing, culminating in the whole testing program handed to PA.
- **A cohort-wide personhood/attribution investigation**, opened by PM catching a published post
  calling AI agents "people," ran through a wrong-then-corrected diagnosis, a full pool sweep finding
  3 more instances, and a shipped structural fix (per-match verdict requirement) that proved itself
  the same day on two more blog proofreads.
- **Ship #062's governance metrics went through two full correction rounds**, ending in a
  triple-independently-confirmed number (91 closed/57 filed) traced to two previously-undocumented
  silent `gh` CLI bugs.

### Technical Details
- MCP Phase C: unit 0 (FastMCP skeleton, deny-by-default 401 gate) → unit 1 (`mcp_access_tokens`,
  hash-only, SDK bearer auth — found and fixed a live 500-not-401 defect on a garbage bearer) → unit
  2 (three read-only resources, honest-empty shapes) → unit 4 (OAuth authorization server in the
  alpha app per RFC 9728, codes bound to the consenting session's identity, PKCE S256, replay
  revokes — found and fixed three real bugs via testing). All five deploys verified live via outside
  probes, not internal claims.
- `#1595` unit 4 (confirm-pause sequencing) landed and immediately surfaced `#1897`: surface 1's
  splitter can never emit a read+write sibling pair, so the correctly-built rail can't be exercised
  by its own motivating case — Arch shaped the fix (an additive `outcome="plan"` field).
- `#1772`'s post-compose scope guard landed and deployed (8/8 corpus leaks caught, 13 legitimate
  mentions preserved).
- Two silent `gh` CLI bugs documented as a durable gotcha: unscoped `--limit` truncates to 30 (or
  500) rows with no warning; `closed:`/`created:` date qualifiers evaluate in UTC, silently dropping
  PDT-evening closures from a "through Thursday" window.
- `template-audit` v1.16: check #11 (agent personhood) now requires a per-match verdict per grep hit,
  not a holistic "sweep clean" claim, closing the exact gap that hid an earlier live judgment miss.
- Registry/heartbeat mechanism findings: two roles (HOST, Lead) had mis-set `wake_start`/`wake_end`
  columns during throttle edits; a real design question (should commits-today count as a liveness
  signal) got a clean ruling — no, heartbeat stays the sole required gate, with a small corroborating
  check deferred to Monday.

### Impact Measurement
- 231 commits (corrected from an initial miscount of 232, itself corrected from a first undercount
  of 160-summed-labeled-232) across all 11 seats misattributed for ~17 hours — fully reverted,
  history deliberately not rewritten.
- 5 MCP units built, reviewed, and deployed live in a single day; alpha v142→v146, MCP v1→v7.
- Ship #062's governance numbers moved from a wrong 43/34/−9 through several rounds to a
  triple-confirmed 91/57/−34, with the underlying qualitative "close to break-even" framing
  confirmed correct all along.
- 4 real, distinct real-world/infrastructure incidents surfaced and closed same-week: the git-freeze
  (Exec, 16h), the attribution mislabel (fleet-wide), a cron-vs-LaunchAgent-plist drift (Arch, 2 lost
  fires), and a cadence-change permission-classifier block (CXO, PPM — both escalated rather than
  routed around).
- Personhood-check pool sweep: 4 total instances found and fixed across 3 pieces, one shipped
  mechanism fix, one durable Comms/Docs division of labor adopted and proven same-day on 2 more
  pieces.

### Session Learnings
- **Verify a correction the same way you'd verify the original claim** — this ran through the whole
  day: Web caught Pard's undercount, HOST caught their own recount error, CXO/HOST/Arch each
  independently re-verified their own commit exposure rather than trust either of Pard's two reports.
- **A permission-classifier block on a legitimate compliance action (cron cadence change) is not
  something to route around** — CXO and PPM both hit this independently and both correctly reported
  it rather than search for a workaround, per the harness's own guidance.
- **"Committed today" and "heartbeat emitted" are different claims, and conflating them costs
  detection accuracy** — the day's central heartbeat-mechanism finding, resolved with a real design
  ruling rather than a quick patch.
- **A hard reset discards tracked-file edits made during a freeze, not just the poisoned index** —
  a genuinely new, durable lesson Exec named explicitly as a standing-error worth writing down.
- **Two independent proofread passes catch different things than one** — proven concretely twice
  today on two separate blog pieces.

## Timeline

### 05:01–07:22 — Morning START wave, the throttle directive lands, MCP build begins

- **05:21 Docs START** → **05:36 Exec** relays PM's usage-throttle directive fleet-wide (20% of
  week's credits burned in 31h, 1.08x pace) — three asks: cut idle cadence 40-50%, hold speculative
  dispatches, consolidate broadcasts through the attention rollup.
- **06:17-08:58 Lead**: MCP Phase C units 0, 1, 2 built and deployed in sequence (Sonnet lanes,
  Lead-reviewed each) — unit 1's live probe found a real 500-not-401 defect, fixed same-fire.
- **06:27 Arch START**: first fire on Pard's new external LaunchAgent wake mechanism (session cron
  retired) — confirms on-time delivery, flags an unresolved model-verification question, resolved
  benignly by Pard's own hold-memo (Opus 5.5 restart deliberately held for PM's presence).
- **06:42 Comms START**: cuts cadence, begins the day's editorial review queue.
- **06:52 CXO START**: attempts cadence cut, **blocked twice by the auto-mode permission classifier**
  (`[Self-Modification]`), briefly left at zero armed jobs — restores original cadence, escalates.
- **07:07 HOST START**: complies with throttle; catches a cohort-freeze false-flag on Web/Docs
  (correctly not escalated — both already self-explained).
- **07:12 PA START, 07:22 PPM START**: both cut cadence with named Monday-revert triggers; PPM's
  cadence cut is notable since PPM was the week's single top usage contributor (17.3%).

### 08:20–10:00 — Docs' Step 1d first run; PM's personhood-attribution catch begins

- **Docs**: first-ever run of the new missing-log-nudge obligation finds Web's and Exec's 09-25 logs
  genuinely stopped mid-day with no STOP section — nudges both.
- **08:55 Web** (late START, +2.5h): discovers and repairs a genuine ~14-hour real-world tool-approval
  stall from the prior evening — retroactively closes 09-25, opens today fresh.
- **~09:15 Pard**: fleet-wide `git config user.name` mislabeling incident (see below) — first report
  lands, cc'd to all 11 roles + PM/Janus.
- **~10:00 PM, in conversation with Docs**: catches "four different people" in a just-published post
  where every actor was an AI agent — the personhood/attribution thread opens.

### 10:07–12:00 — MCP OAuth-AS trigger, PM's testing-program handoff, the attribution incident's first correction

- **10:07 CIO START**: checks own exposure to the attribution incident, complies with throttle
  (already at 3x/day), sends one consolidated reply covering three threads.
- **10:39 PM (in chat with Lead/Arch)**: rules PM is MCP tester #1 (ChatGPT first), hands PA the
  whole MCP testing program, freeing Lead for MVP critical-path epics — puts the OAuth AS (unit 4)
  on the critical path.
- **PA** makes the call: Lead builds unit 4 as one bounded lane (Arch's technical case — the person
  who verified the identity boundary finishing the adjacent lane is lower-risk than a fresh
  dispatch), ratifies Arch's review condition as a required test.
- **11:18 Lead**: `#1595` unit 4 lands; the build immediately surfaces `#1897` (surface 1 can never
  emit a read+write sibling pair) — filed same-day, Arch shapes the fix.
- **Docs**: fixes the "four different people" post on the site, finds a second unflagged instance in
  the same piece, opens a discussion with Comms rather than just report the fix.

### 12:00–14:00 — Comms corrects Docs' framing; the personhood pool sweep; Ship #062's metrics saga opens

- **Comms**: corrects Docs directly — a check for this (`template-audit` #11) already existed since
  09-01, HOST-ruled 09-19 on 09-19; the real gap is version drift (this piece predated the check).
  Sweeps the entire current draft/queued pool rather than assume it was isolated: finds 3 more real
  instances across 2 more pieces, including a piece drafted **after** the check existed where Comms'
  own prior audit had wrongly claimed "sweep clean" — a live judgment miss, reported honestly
  alongside the version-drift explanation rather than picking the more comfortable story.
- **Comms ships `template-audit` v1.16**: every check-#11 grep match now needs its own stated
  verdict, closing the exact gap that hid the judgment miss. Folds in PM's same-day bidirectional
  clarification (crediting a human's work to an agent is exactly as wrong as the reverse).
- **PM, in conversation with PPM**: hands over 3 fresh GitHub Projects TSV exports, asks for a full
  epic-structure review. PPM runs a definitive GraphQL-verified audit (not heuristic), finds 52 stale
  unstruck-but-closed references across 8 epics, fixes all, recomputes headers from true section
  membership, closes one genuine coverage gap (`#1897`).
- **12:17 Lead**: fire doesn't surface while PM is engaged mid-conversation; run by hand later on
  PM's own nudge — the "fire is a wake, not a time-box" model held, just arrived late.
- **PPM, WORK fire**: independently re-derives Ship #062's disputed closed/filed count via a third,
  different method (direct API date-boundary scoping) — converges exactly on 91/57, matching Exec's
  and Lead's separately-derived numbers.

### 14:00–17:00 — Cadence-mechanism mystery resolved; two more blog proofreads; the corrected schedule holds

- **Arch**: two fires (09:27, 12:27) land on the OLD schedule despite a cadence-cut edit three hours
  earlier — resolves the mystery by observation: editing the registry's `cron_expr` alone does not
  move Pard's LaunchAgent, which reads a separately-generated plist. Pard fixes the plist and adds a
  drift guard; Arch's 14:27 fire lands on-time, confirming the fix.
- **PM, in conversation with Docs**: asks for "A Primary Log Can Be Wrong, Not Just Incomplete" and
  "Three Seats Stay Dark Longer" to be proofread and queued. Docs runs the full 16-check
  `template-audit` on both for the first time, applying the new Comms/Docs division of labor: finds
  and fixes a borderline personhood case on the first piece; independently re-verifies Comms' own
  two flagged fixes on the second (a 21+-hour figure, a fabricated CIO quote) against primary logs
  before trusting them, then catches two things Comms' own pass missed entirely (a HOST-naming
  error dropping "Sapient"; a truncated footer-tease title).
- **17:07 PM**: approves Lead building the MCP OAuth AS; **17:48 Lead**: unit 4 lands (three real
  bugs found and fixed via testing); **17:54**: live, MCP lane handed to PA with named gaps.

### Afternoon–evening — the attribution incident's second correction; Ship #062 resolved; STOP wave

- **Pard**: recounts the attribution incident after Web catches an undercount (6 vs. their actual 10)
  — finds their own per-seat breakdown summed to 160 while labeled 232, corrects to 231 total with an
  explicit unattributed bucket (18 commits, honestly unclaimed rather than guessed). Several roles
  (Arch, CXO, HOST, Docs) independently re-verify their own corrected counts rather than accept the
  new number on trust — all confirm exact.
- **PM, in conversation with Comms**: updates Ship #062's metrics to 91/57 — a number Comms genuinely
  couldn't reproduce through several honest attempts, correctly says so rather than silently accept
  or override; PM routes to Exec's already-resolved thread, which traces the discrepancy to the two
  silent `gh` bugs. Comms' own image-mismatch finding (Ship's header art duplicated from another
  post) stays open at STOP, correctly left for PM rather than guessed at twice.
- **Exec**: burns the three `#1885` invite tokens by PM's own hand (dry-run then apply, fully
  evidenced); prunes the attention rollup to "nothing needs you right now," verified against live
  state each time it's republished.
- **HOST**: catches a real registry column error (its own `wake_start`/`wake_end` misread during the
  throttle edit) affecting its own and Lead's rows; flags a week-long heartbeat gap on Exec's seat
  that turns out to be a genuine structural finding, not a habit lapse.
- **Exec**: names the day's central heartbeat design question precisely — a busy, frequently-
  committing seat's heartbeat legitimately self-suppresses past the daily START row (by the
  mechanism's own design), separate from a one-time freeze-specific marker casualty.
- **CIO** rules: heartbeat stays the sole *required* liveness signal (making commits an equally-valid
  parallel path would reintroduce the exact false-positive the decoupling exists to prevent); adds
  a small corroborating check for the stale-marker-but-real-commits case, **explicitly deferred to
  Monday** per the throttle.
- **PPM STOP**: PM rules 3-of-4 post-MVP proposals to `Ongoing`; PPM makes the 4th call itself
  (`#1890` → `Ongoing`, verified live, genuine outstanding housekeeping) — then hits the same
  permission-classifier block CXO hit that morning (`[External System Writes]` on `gh issue edit
  --milestone`), reports rather than routes around it.
- **Docs, 3 further fires** (11:27, 17:27, 23:27/STOP): drains four informational threads (attribution
  recount, Exec's own heartbeat explanation, CIO's ruling), closes the day.
- All 11 core roles reach `<!-- DAY-CLOSED: 2026-09-26 -->` — except **PA, whose log genuinely stops
  at 12:57 PDT with no STOP section**, despite real later-day activity (mail commits after 13:00
  confirmed in git history; Lead's own STOP inbox references PA's min_machines_running fix at 21:50).
  Flagged for Step 1d's nudge on 09-27.

## Canonical References

- **`template-audit` skill check #11** ("Agents referred to as 'people'/'person'"), version-verified
  at v1.16 as of this day — live since 2026-09-01, HOST-ruled 2026-09-19 (`decisions.log`, #1834).
- **`decisions.log` #1834**: HOST's ruling that agent-as-"people" language is a false accountability
  claim, not a register-scoped style choice like "cohort"/"team."
