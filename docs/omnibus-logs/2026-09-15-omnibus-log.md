# Omnibus Log: Tuesday, September 15, 2026

**Day**: Tuesday
**Sessions**: 17 (11 named roles — Lead Developer, Documentation Management, Chief Architect,
Chief of Staff/Exec, HOST, Communications, CXO, CIO, PPM, Piper Alpha/PA, Web — plus 6 `prog`
coding-agent subagent sessions, all dispatched from Lead Dev's worktree)
**Day Type**: HIGH-COMPLEXITY — COORDINATION
**Git Commits**: 295 (`git log --oneline --since="2026-09-15 00:00" --until="2026-09-16 00:00"`)
**Note**: written retroactively 2026-09-16, after PM engaged directly the evening of 09-15
(publishing a blog post) before the day's own STOP fire could run — no work was lost, but the
omnibus itself was deferred. This is that catch-up pass.

**Justification**: A credential/consent security thread reopened overnight and ran through five
distinct findings in one day (#1814 → #1815 → #1816 → #1772 measurement → classifier-bucket
split), each closed only after independent verification by a different role, with three separate
agents (Lead, Arch, Exec) naming their own share of an overnight sequencing miss before being
asked. In parallel, a genuinely separate multi-role thread (Comms/Web/PM) worked through a
publishing incident on a live blog draft. This is coordination, not parallel execution: the
security thread's discipline (observe, don't trust a description) was invoked and re-invoked by
name across four different rulings same-day.

---

## Chronological Timeline

### Morning: The Invite Re-Held, Then Cleared By Observation (06:29 – 09:53)

- **06:29 AM**: **Lead Developer** START — inbox 5, both of Arch's #1798 hook conditions already
  landed. Dispatches the day's first **prog subagent** to run the FTUX observation as its own task
  (not folded into someone else's errand, which is how a rider got lost the day before).
- **06:31 AM**: **Lead Developer** Fire 1 — 🔴 owns a false claim from the night before ("CXO's
  rider is satisfied by the same run" — it wasn't; CXO's own correction caught it). HOST lifts
  last night's hold on Janne's alpha-tester invite, verifying via `gh issue view` + `git
  merge-base` rather than trusting reports; Arch rules the bar met and owns having tried to lower
  it.
- **06:47 AM**: The FTUX-observation **prog subagent** finds a real blocker: `LLMConfigService
  .get_api_key()` takes no user parameter and never consults `UserAPIKeyService` — a signed-in
  BYOC user's own stored key is never read. **This is exactly the path the invite's own onboarding
  condition ("configure your key first") walks a tester into.** Filed **#1814**. Lead re-asks
  Exec/HOST to re-hold the invite they'd just correctly lifted, on evidence of the cohort's own bug.
- **06:53 AM**: **Chief Architect** START — backs the re-hold, owns the sequencing share that's
  theirs (ruled "delete the write" on 09-14 without requiring every reader be shown another
  source first). Heartbeat push fails loud (by design) on a transient push race, self-heals on
  retry — the first watched firing of that mechanism.
- **07:07 AM**: **HOST** Fire 1 — updates the alpha-tester roster to RE-HELD before anything else
  this fire, prior LIFTED status struck through and preserved, not erased. Restates the bar
  sharpened for this failure: must show a stored key actually being read and used, not just an
  empty slot.
- **07:07 AM**: **Chief of Staff (Exec)** START — 🔴 retracts its own "ready to send" relay from
  the night before, naming its own share: relayed an onboarding instruction nobody had walked
  through, the exact discipline Exec had insisted on for the #1810 fix itself.
- **07:08 AM**: **CXO** START — takes no independent position on the overnight thread (no evidence
  of its own), but pre-registers FTUX/keyless scoring properties *before* any transcript exists,
  and does the layer-match check *in advance* this time (what the coming observation will and
  won't close). Finds #1814 exposes a real conflation in copy CXO wrote 24 hours earlier
  (verified-absent vs. lookup-failed keys produce the same exception; the copy can only assert the
  stronger claim).
- **07:12 AM**: **Piper Alpha** START — checks the alert against its own lane (not applicable);
  notes the BYOC hosted-alpha assessment is still unanswered (~57 hours).
- **07:16 AM**: The **prog subagent** re-runs the FTUX observation and confirms **#1814 CLOSED by
  observation**: a real turn hits the network, gets `401 authentication_error` — proof the key was
  resolved, selected, and sent, using a throwaway key so PM's real key is never spent. Lead
  corrects two of its own earlier mis-attributions in the same breath.
- **07:22 AM**: **PPM** START, ~30 min late — is itself one of the seven roles the prior day's
  false alarm named; triages #1814/#1815 into epic 2 (Security/tenancy, reopened the day before).
- **09:31 AM**: **Lead Developer** Fire 2 — the cohort had already acted on Lead's urgent before
  the fix landed: Exec retracted, HOST re-held, Arch backed it and owned part of the sequencing
  error. CXO's pre-registered layer-match table holds exactly once transcripts land. Dispatches
  the day's third **prog subagent** to #1815 (a BYOC key working as primary but never as fallback).
- **09:37 AM**: **Chief Architect** WORK — rules #1816 + #1815 Gap 2 together after Lead inverts
  its own premise and finds a consent-authorization boundary failing OPEN (`KeychainService
  .get_api_key` swallows exceptions, so the fail-closed branch is unreachable in production —
  "absence read as permission"). Four rulings: fix the consent reader, never the credential
  primitive; name it a third live instance of the honest-empty family at the security layer;
  closed must refuse, not degrade (coherent with PM's server-key-abolition ruling); keep
  consent-from-key-presence but dated with a named invalidation trigger.
- **09:50 AM**: The **prog subagent** fixes #1815 Gap 1, and Gap 2's own investigation **inverts
  the issue's own premise** — the stated trigger doesn't fire in production; what does is worse
  (fail-open, not the fail-closed the issue assumed). Filed **#1816**.
- **09:53 AM**: **HOST** Fire 2 — verifies #1814's closure independently before ruling, reads
  `provider_selection.py` directly to confirm #1816 doesn't touch Janne's actual path, lifts the
  hold again.

### Late Morning: The Consent Boundary Closes, A Real Leak Gets Measured (10:07 – 13:22)

- **10:07 AM**: **Communications** — synced onto Lead's traffic; nothing in its own domain yet.
- **10:17 AM**: **CXO** Fire 2 — 🔴 checks a ruling that credited its own copy with covering a
  state it doesn't (a consent-read failure is a user who *has* a key, not one who lacks it — the
  #1108 "recommends a known-failing action" shape, arriving via someone else's ruling). Delivers
  correct copy with three deliberate properties, including that "try again" is admissible here
  specifically because a store hiccup is genuinely transient.
- **10:37 AM**: **Chief Innovation Officer** START — a quiet, well-run fire: banks Arch's watched
  heartbeat-fail-loud firing directly into `duty-cycle-heartbeat.sh`'s own header (comment-only),
  agrees with Arch against a silent retry (would relocate the invisible-success shape one layer
  down).
- **12:03 PM**: The **prog subagent** measures #1772 (CXO's earlier N=1 scope-leak anecdote):
  **50% leak rate on claude-sonnet** (production's actual default provider), 0% on gpt-4o, N≥2
  aggregate clean on both — turning a declined-to-overclaim anecdote into a real, alarming rate.
- **12:12 PM**: **Lead Developer** — measures #1772 properly (n=10/cell, not n=1); separately rules
  #1788 DocumentDB closed alongside Arch. **The whole credential/consent family (#1814/#1815/#1816)
  closes today, all three MVP, 0 unmilestoned.**
- **12:17 PM**: **Lead Developer** reports #1772's measurement directly, with both of CXO's prior
  caveats discharged (not caused by #1717; re-verified at current HEAD rather than trusting the
  09-12 check).
- **12:30 PM**: The **prog subagent** ships #1816 + #1815 Gap 2 together (v111) — a red-first pass
  catches a *second* violation the static reading missed (the closed state was still being served
  by the operator's own client via a swallowed exception in `_complete_raw`).
- **12:53 PM**: **Chief Architect** WORK — 🔴 concedes to CXO in full: the ruling's claim that
  CXO's copy already covered a state was wrong, and would have shipped the #1108 failure directly.
  Names the pattern as a property, not an error — three instances in three days, all "the summary
  was my own memory of an artifact I had genuinely read once" — and proposes a mechanical fix on
  its own future output: quote the artifact inline, or say unverified.
- **13:07 PM**: **HOST** Fire 3 — verifies #1816's closure directly, considers #1772's leak
  explicitly (a different harm class than anything gating the invite; doesn't change Janne's
  status).
- **13:17 PM**: **Lead Developer** Fire 3 — 🔴 discloses to CXO before shipping: the deployed
  copy is CXO's *proposal* string, not their ratified one — a live fail-open boundary outranked
  waiting. CXO reviews it in situ (not rubber-stamping) and finds a real bug in its own prose sitting
  in a slot that renders actionable chips, not text.
- **13:22 PM**: **PPM** WORK — the consent fail-open thread closes same-day; #1772 gets its real
  measurement recorded against epic 5; triages the one unmilestoned issue (#1817, the
  invalidation-trigger tripwire).

### Midday: The Publishing Saga (Comms/PM/Web) Runs Alongside (11:xx – 18:42)

- **~11:00 AM onward**: **Communications**, working "The Bug That Was Misdiagnosed Twice" (today's
  scheduled beat), catches two landed admin-UI edits, runs a full template-audit, fixes 3 real
  issues including a garbled name ("Docgg'" for "Docs'") — then discovers mid-fire that **Web had
  independently landed the identical fix moments earlier**, but with the real root cause: Web's own
  P0 caret-restore regression (shipped the day before) had reversed characters while PM was typing,
  genuinely corrupting the draft — not typos at all.
- **~10:2x AM**: **Web** diagnoses and fixes its own regression: yesterday's Source/Split/Preview
  toggle's `useLayoutEffect` re-ran on every keystroke instead of only on remount, rewinding the
  caret and reversing typed characters ("odd"→"ddo"). Fixed (`45ab4a9`), verified by reverting the
  guard to prove the test could detect the bug before trusting it green. **Then checks whether the
  bug wrote anything down** — finds it corrupted *persisted* content, measures the exact blast
  radius (2 commits, 1 file), and repairs the surviving artifacts against pre-corruption text.
- **Midday**: PM independently editing the same draft in the main checkout hits a real merge
  conflict against both fixes. **Comms declines to edit PM's checkout directly** (an agent write
  there cost PM real lost edits before) and instead gives PM a scripted one-shot fix PM runs
  themselves — twice, as a second defect (a lost blank line) surfaces on the first resolution.
- **Web's stand-off memo to Comms** (an urgent "stop pushing to this file") turns out to
  mischaracterize Comms, who had actually acted correctly on a published signal — Web reads Comms'
  own log, finds the error, and sends a same-fire correction rather than let it stand.
- **Web separately investigates and retracts its own inference** that a stray PM commit
  (`say-cheese.png`) was today's hero art — Comms independently verifies via `git ls-tree` that the
  only file by that name is the already-published Who's Who cover, and the real art PM used is
  `…-gallery-hooks.png`. Web: "the check beat the reasoning."
- **~14:2x PM**: **Comms** confirms frontmatter is finally complete, diffs directly against the
  last fully-audited commit (confirming zero drift in prose), re-runs the full template-audit, and
  sends **PUBLISH-READY** to Docs.
- **15:53 PM**: **Web** drains **website#42** (no automated test on the compose editor's ordinary
  typing path) same-day rather than leave it for PM to prioritize — ships jest + `next/jest` config,
  verifies the new tests actually detect the regression before trusting them green.
- **15:53 PM**: **Chief Architect** WORK — the auth-bucket classifier thread: Lead holds CXO's own
  conditional replacement copy to its stated test and finds it fails (the "auth" bucket actually
  mixes five distinct causes, not the assumed one); Arch finds a fifth cause nobody had named (a
  404 branch whose own comment says "config issue" while returning `auth`).
- **16:17 PM**: **CXO** Fire 4 — 🔴 its own attached condition fails, "which is the conditional
  working." Misapplied its own contract's rule (checked whether *we* held the answer, not whether
  the layer writing the sentence did) — refines the contract to v0.6 on the spot.
- **18:42 PM**: **Communications** — the post publishes (Docs takes the fix live); the whole
  merge-conflict/stand-off saga on this one post closes out cleanly end to end, same day it started.
- **18:53 PM**: **Chief Architect** WORK — its own "not initialized" hypothesis about #1814's real
  cause is refuted by Lead's transcript evidence; accepts the refutation and corrects the split's
  justification on the record rather than let a right conclusion rest on a wrong reason.

### Afternoon/Evening: BYOC Parallel-Work Plan Approved, Usage Limit Surfaces (13:xx – 19:22)

- **Mid-afternoon (between fires)**: **Piper Alpha** answers a live PM "hand up" check, surfaces
  two pending items (T1, BYOC sequencing) unprompted, and gets a direct PM ruling: BYOC parallel
  work is fine provided it doesn't distract Lead Dev and nothing merges that risks the MVP
  milestone. Produces three real artifacts same-session: a three-phase BYOC parallel-work plan, a
  first-pass "Piper harness inventory" (mapping cohort disciplines like session logs and
  verification to Piper's own product-side equivalents — sharpest finding: the memory/colleague-
  model gap is the one everything else depends on), and publishes T1 itself as a browsable Artifact
  so PM can close the pending item directly.
- **16:12 PM**: **Piper Alpha** picks up its own plan's named next step (the Phase A readiness
  checklist) unprompted, and finds a real stale citation along the way: PDR-006's "untested"
  ChatGPT honest-decline mechanism was actually tested 2026-08-02 at 6/6 — the result never made it
  back into the doc. Fixes PDR-006 and its own Saturday plan doc; flags PPM directly since it
  unblocks a wording proposal PPM had been holding.
- **16:22 PM**: **PPM** WORK — revises PDR-006's wording per PA's finding (moves from "under active
  question" to "provisionally confirmed, pending one deployed-host retest"). PA verifies the actual
  file rather than trust "thanks, done."
- **17:50 PM (relayed via Dispatch)**: **PM notice, cc all eleven roles**: pipermorgan.ai is at 97%
  of its weekly all-models limit (Fable at 100%); wall expected within 12h, resets Thursday 22:00,
  usage credits off. Defer non-urgent work two days; a quiet fire in this window is expected, not a
  fault.
- **18:38 PM**: **Chief of Staff (Exec)** WORK — 🔴 corrects its own prior finding's scope: the
  usage spike isn't fully explained by the subagent-dispatch concentration Exec found on Saturday
  (48 dispatches, 30 in one day, all Fable) — a separate cause exists (the summer promotion ended
  09-13, dropping the ceiling ~17%), and conflating the two would misattribute the whole rise to
  behavior alone. Deliberately does not relay PM's notice cohort-wide (PM already cc'd all eleven
  roles directly; a relay would spend quota duplicating a memo everyone already holds).
- **19:07 PM**: **HOST** Fire 5 — the classifier-bucket-split thread closes cleanly, no HOST action
  needed; notes both Arch and Lead treating being corrected as more important than being right.
- **19:17 PM**: **CXO** Fire 5 — scores real FTUX transcripts against its own morning
  pre-registration: keyless refusal passes 4/4; one property (leads with copy, not a greeting) is
  ruled **UNSCOREABLE** rather than failed, since the feature is gated OFF by a PPM 09-03 HOLD
  ruling CXO hadn't been tracking — closing an 8-day-old "unverified" tracker row by discovering it
  was never a measurement gap at all. Finds two live copy defects transcripts surfaced that source
  reading alone hadn't: a keyless-refusal string that's literally false ahead of a bare greeting
  (a deterministic handler needing no key), and a "default configuration" notice that fires
  misleadingly right after a user finishes configuring their own key.
- **19:22 PM**: **PPM** WORK — the classifier-bucket-split thread resolves cleanly, cc-only.

### Night: Day Close (21:12 – 22:17) — and a Deferred STOP

- **21:12 PM**: **Communications** STOP — day closes on a real, substantive gap surfaced but not
  yet actioned: PM asked directly whether the Aug 9–18 narrative-front window was under-reviewed,
  Comms checked rather than assumed, and a dispatched subagent confirmed a real miss — Aug 10-18 is
  arguably the densest 9-day run of the month, with five strong unsurfaced beat candidates. PM
  directed a 5-beat backfill plus a process fix (per-calendar-day ledger discipline for future
  narrative-front surveys); both await PM's confirmation before any drafting or skill changes.
- **21:42/22:12 PM**: **Piper Alpha** — last scheduled fire, quiet; flags its own cron's exact-day
  expiry landing on tomorrow's last fire slot, planning a proactive re-arm rather than discovering
  it dead.
- **21:52 PM**: **Web** STOP — day-close; catches a genuine near-miss reading a cleanup script
  before running it (the name matched intent, but the actual script was a venv-nuking `rm -rf`
  with no dry-run flag). Finds and fixes a real registry gap on its own row (missing a status
  column entirely, meaning the skill's proactive-expiry check has had nothing to read for this
  seat).
- **21:53 PM**: **Lead Developer** Fire 6 — Arch accepts Lead's refutation of its own hypothesis;
  CXO scores the FTUX transcripts and finds a live defect in its own string in production by
  21:00, having written the rule that string violated at 08:00 that same morning. Files **#1818**
  for the routing half, explicitly no longer urgent since the sentence itself is already fixed.
- **21:57 PM**: **Chief Architect** STOP — one item drained (CXO's transcript scoring), no arch
  action needed.
- **22:07 PM**: **HOST** Fire 6 STOP — one memo triaged (CXO's two live copy defects), both
  correctly scoped as copy-only with no security implication.
- **22:17 PM**: **CXO** STOP — reconciles its own 8-day-old tracker row that had been asking a
  measurement question whose actual answer was a ruling — the third such row in nine days, and the
  first whose cause wasn't "I didn't read the issue."
- **The 21:57 duty-cycle fire for Docs never formally ran**: PM engaged directly with a rate-limit
  update and a new Weekly Ship publish request before the tick's sync/mail-loop could execute.
  No work was lost — the 18:57 fire had already fully drained the day — but the day's own STOP
  (and this omnibus) were deferred to the morning of 09-16.

---

## Executive Summary

### Core Themes

- A credential/consent security thread reopened overnight (#1814) and closed same-day through
  #1815, #1816, a real leak measurement (#1772), and a classifier-bucket split — every step gated
  on independent verification, not a report, and three separate roles (Lead, Arch, Exec) named
  their own share of the original sequencing miss before being asked.
- The clearing-bar discipline held under real pressure across two full hold/lift cycles on an
  external tester's invite: HOST lifted, a bug immediately re-opened the risk, HOST re-held on
  sharper criteria, and the invite cleared a second time only after a real network-observed 401,
  never a test pin.
- A live blog-publishing incident (a P0 typing-backwards regression corrupting a draft mid-edit)
  ran through Web, Comms, and PM directly, resolved end-to-end same day with a real data-repair
  obligation separated from the code fix, and closed with the fix confirmed in production by real
  post-deploy user edits.
- PM approved a BYOC parallel-work track (Piper Alpha) explicitly bounded to not distract Lead Dev
  or risk the MVP milestone — producing a real plan, a harness inventory, and a stale-citation fix
  to PDR-006 in one day.
- A weekly usage-limit notice arrived late in the day (97% of all-models capacity, Fable at 100%),
  and Exec caught a real error in its own earlier analysis before it could harden: the spike has
  two independent causes (a subagent-dispatch concentration *and* an unannounced ~17% ceiling drop
  from an ended promotion), not one.
- Self-correction was the day's operating mode, not an exception: CXO caught two colleagues
  crediting its own work with covering states it didn't, twice in two days; Arch named a
  three-in-three-days pattern in its own rulings and proposed a mechanical fix for it; Web
  identified five of its own wrong predictions in one session, all one shape (asserting state it
  hadn't verified).

### Technical Details

- **#1814**: `LLMConfigService.get_api_key()` had no user parameter and never consulted
  `UserAPIKeyService`, reading only the legacy global slot #1810 had correctly emptied — closed
  by driving a real turn to a `401 authentication_error` (proof of resolution over the network,
  via a throwaway key), deployed v109.
- **#1815**: two residual "server singleton as availability proxy" instances — a cross-provider
  fallback loop gating on the server's own client (BYOC key works as primary, never as fallback)
  and a consent fail-closed branch degrading to the now-abolished server-key concept. Gap 1 fixed
  same pattern as #1814; Gap 2 ruled alongside #1816.
- **#1816**: `KeychainService.get_api_key` swallowed exceptions broadly, making the intended
  fail-closed consent branch unreachable in production — control fell through to "everything
  authorized." Fixed with a tri-state read (PRESENT / VERIFIED_ABSENT / STORE_FAILED); a red-first
  pass also caught a second violation (`_complete_raw`'s blanket except silently re-selecting the
  operator's own client).
- **#1772**: measured (not anecdotal) — 50% scope-directive leak rate on claude-sonnet
  (production's default provider) under a single-source degrade, 0% on gpt-4o, clean on the N≥2
  aggregate path on both providers.
- **Classifier bucket split**: the "auth" error bucket was found to collapse five distinct causes
  (rejected credential, insufficient permission, uninitialized client, deprecated model, a 404
  branch whose own comment said "config issue" while returning `auth`) — split adopted on the
  criterion "a bucket earns its own name when the honest user-facing sentence differs," not on any
  single incident.
- **Compose-editor P0** (website): a `useLayoutEffect`'s dependency array caused the caret-restore
  logic to re-run on every keystroke instead of only on remount, reversing typed characters.
  Fixed by guarding on a ref rather than removing `body` from deps (still needed for scroll math);
  a jest test suite shipped same-day, verified to actually detect the regression before trusting
  it green.
- **PDR-006**: OQ3 wording corrected from "under active question" to "provisionally confirmed,
  pending one deployed-host retest" after PA found the cited "untested" mechanism had actually
  been tested 2026-08-02 at 6/6.

### Impact Measurement

- Credential/consent family (#1814, #1815, #1816) fully closed same day, all three counted against
  the MVP milestone; 0 issues unmilestoned throughout the day (checked repeatedly by PPM via
  `sprint-truth.py`).
- MVP not-done count moved 56 → 54 → 55 across the day's fires, tracking real discovery/closure
  churn, not drift.
- Four deploys shipped to close the security chain and its copy work: v109, v110 (implied by the
  #1815 fix), v111, v112, v113.
- One external alpha tester's invite held across two full hold/lift cycles, cleared only on
  independently-verified network evidence both times.
- One blog post ("The Bug That Was Misdiagnosed Twice") published same day, fully distributed by
  the next morning, after a genuine same-day production-bug data-corruption incident was found,
  fixed, and repaired.
- website#42 (compose-editor test coverage) filed and closed same day.

### Session Learnings

- **"A claim that something was satisfied 'along the way' is the easiest kind to make and the
  least likely to be checked — because it costs nothing to say."** Lead's own framing, after
  correcting exactly that kind of claim twice in the day's first hour.
- **Deleting a write requires enumerating that slot's readers with their post-deletion source
  named** — "the readers still resolve whatever is already there" is true and insufficient the
  moment the slot goes empty. The #1814 root cause, named durably by Arch.
- **A credit is the one claim nobody expects the creditee to audit** — CXO's framing, after
  catching two different colleagues (Lead, then Arch) crediting its own copy with covering states
  it didn't, on two consecutive days.
- **A ruling that asserts "X already covers Y" should quote X inline or say "unverified."** Arch's
  proposed mechanical fix on its own output, after naming a three-in-three-days pattern of citing
  an artifact from memory rather than reading it fresh.
- **A true conclusion resting on a wrong reason survives longer than it should** — named
  independently by both Lead and Arch the same day, about a hypothesis Arch floated and Lead
  refuted with a transcript.
- **When a check returns "nothing found," run it against a case known to be good before believing
  the nothing.** Web's control-group catch, after a raw-HTML grep for images returned zero on both
  a broken-looking post and a known-healthy one.
- **A code fix and a data repair are separate obligations** — Web's own framing, after fixing the
  compose-editor bug and then separately asking "did this bug write anything down?"
- **Two independent causes can both be real; naming only one misattributes the whole effect** —
  Exec's correction of its own earlier analysis, applied to the week's usage-limit spike.
- **A tracker row can hold a real-looking measurement gap open while the actual answer was a
  ruling all along** — CXO's third instance of this in nine days, closing an 8-day-old row by
  discovering the FTUX flag was OFF by a PPM decision, not unverified.

---

## Sources

All 17 source session logs for 2026-09-15 were read in full or to task-identifying depth (the 6
`prog` sessions, all confirmed via worktree/branch/task-header alignment as Lead Dev's own
dispatches):

- `dev/2026/09/15/2026-09-15-0629-lead-code-log.md` (Lead Developer)
- `dev/2026/09/15/2026-09-15-0630-prog-code-log.md` (prog — FTUX observation, found #1814)
- `dev/2026/09/15/2026-09-15-0642-comms-code-log.md` (Communications)
- `dev/2026/09/15/2026-09-15-0648-prog-code-log.md` (prog — #1814 fix)
- `dev/2026/09/15/2026-09-15-0652-web-code-log.md` (Web)
- `dev/2026/09/15/2026-09-15-0653-arch-code-log.md` (Chief Architect)
- `dev/2026/09/15/2026-09-15-0700-pa-code-log.md` (Piper Alpha)
- `dev/2026/09/15/2026-09-15-0707-host-code-log.md` (HOST)
- `dev/2026/09/15/2026-09-15-0707-prog-code-log.md` (prog — #1814 re-observation)
- `dev/2026/09/15/2026-09-15-0708-exec-code-log.md` (Chief of Staff/Exec)
- `dev/2026/09/15/2026-09-15-0717-cxo-code-log.md` (CXO)
- `dev/2026/09/15/2026-09-15-0722-ppm-code-log.md` (PPM)
- `dev/2026/09/15/2026-09-15-0727-docs-code-log.md` (Documentation Management)
- `dev/2026/09/15/2026-09-15-0930-prog-code-log.md` (prog — #1815 Gap 1 fix)
- `dev/2026/09/15/2026-09-15-1037-cio-code-log.md` (Chief Innovation Officer)
- `dev/2026/09/15/2026-09-15-1203-prog-code-log.md` (prog — #1772 measurement)
- `dev/2026/09/15/2026-09-15-1230-prog-code-log.md` (prog — #1816 + #1815 Gap 2 fix)

**Cross-reference gate**: all 11 cohort roles have session logs in the source set — gate passes
cleanly. Cross-project mentions (Dispatch relaying PM's usage-limit notice) are correctly outside
this cohort and not counted as gaps.

**Canonical references**: no PDR/ADR/Pattern/methodology was newly ratified today. PDR-006's
wording revision is quoted from PPM's own session log describing the actual file edit, not
paraphrased.

**A note on this omnibus's own retroactive nature**: written 2026-09-16 rather than same-day, after
Docs' own 21:57 fire was superseded by direct PM engagement (a rate-limit update plus a new
publish request) before the day's STOP could run. No work from 09-15 was lost — the day was fully
drained by its 18:57 fire — but this synthesis itself is one day late, and is explicitly noted as
such per this project's own discipline of naming gaps rather than back-filling silently.
