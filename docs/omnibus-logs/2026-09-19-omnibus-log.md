# Omnibus Log: September 19, 2026

**Day**: Saturday
**Sessions**: 12 (Communications, Lead Developer, Unicorn Web Designer, Coding Agent [subagent],
Chief Architect, Documentation Management, Piper Alpha, HOST, Chief of Staff, CXO, PPM, CIO — all
11 cycling roles plus 1 dispatched Coding Agent subagent)
**Day Type**: HIGH-COMPLEXITY: COORDINATION — target 450–600 lines
**Justification**: Eight of eleven seats underwent a deliberate Wave-2 Amber fleet-renewal context
clear mid-morning (Pard-conducted, Janus-certified, PM overseeing), requiring identity/handoff
re-verification across the fleet. The day also carried a genuine multi-role, PM-mediated
coordination arc — the #1823 BYOC-key-binding decision resolved end-to-end across Arch, CXO, PPM,
and Lead in under three hours; a cohort-wide heartbeat-coverage investigation propagated across
Web, CXO, CIO, and HOST; a hosting/alpha-invite crisis ran through HOST, Lead, Arch, and PM to a
HOLD ruling and a droplet-upgrade plan; and PM personally drove long Saturday threads with Exec
(Ship #061 internal report, sprint-truth tooling, weekly-cycle runbook, sprint-week communication)
and Docs (a same-day blog publish, a 230-file YAML-frontmatter rollout, a full backlog sweep).
These are PM-mediated handoff chains and cross-agent consensus-building — Coordination, not
Execution.
**Git Commits**: Not independently tallied (12 active seats, many push-to-ref mail commits per
fire); volume was unusually high — HOST's own mid-day freeze-check recorded 156 commits landing on
`origin/main` within a single 4-hour window (13:07 fire).

---

## Cross-Reference Gate (Step 2.5) — PASS

Grepped all 12 source logs for mentions of the 11 cohort roles plus the renewal-conducting actors
(Pard, Janus). Every mentioned cycling role has its own log in the source set. Pard and Janus are
the renewal's conducting/certifying actors, not cycling roles with daily logs — their presence
in-text (Wave-2 arrival blocks, hosting-tasking threads) is expected, not a gap. Checked
`dev/active/` and `dev/2026/09/19/` for same-day artifacts from roles outside the source set: every
dated artifact found (`usage-per-account-capture`, `weekly-ship-061-draft`, `delta-*` files,
`exec-cohort-attention-rollup*`, `alpha-droplet-upgrade-plan`, `ship-061-internal-report`) is
authored by a role already in the source set. Gate passes cleanly.

## Cross-Role Mentions Verification (Step 2.6)

Spot-checked several high-impact cross-role claims; all confirmed consistent, no discrepancies
requiring a preserved-disagreement flag:
- Lead's claim that its #1823 precondition trace was accepted and "discharged" matches both Arch's
  and PPM's independent accounts of the same event.
- The Docs 09-13 "routing-memo offer" mixup (Exec's synthesis said it was owed to Lead; Lead
  searched and couldn't find it; Docs traced it to the actual primary source and confirmed the
  offer was made to PM, never mailed to Lead) is reported identically across Exec's, Lead's, and
  Docs's logs — a clean three-way corroborated correction chain, not a disagreement.
- CXO's #1825 fix claim (commit `cc7d21e60`) matches Docs's own log, which independently discovered
  and fixed the same issue with the identical commit hash — genuine cross-validation, not
  duplication error.
- Web's, CXO's, and CIO's accounts of the interior-coverage/heartbeat-gap investigation (who found
  what, in what order) are mutually consistent across all three logs.
- The alpha droplet version fact (`0.8.10.14`, deployed July 16) is reported identically by Lead,
  HOST, and Exec once confirmed.

No genuine discrepancies were found. One note: the task brief for this omnibus asserted Arch's log
"mentions ADR-070 in passing" — grepped all 12 source logs for `ADR-070`/`ADR 070` and found zero
matches. No ADR-070 citation appears anywhere in today's material, so none is made here; the actual
canonical artifact load-bearing today is `docs/internal/architecture/ESSENCE.md` (cited by Arch,
CXO, and PPM), whose "5 standing architectural rules" and "7 commitments" were verified verbatim
against the live document before use below.

---

## Chronological Timeline

### Early Morning: Predecessor Sessions Open (6:42 AM – 7:22 AM)

**6:42 AM**: **Comms** opens START fire — prior day closed clean, cron single job confirmed, one
real staleness caught (ChicagoCamps talk, now past, still framed as pre-event in standing-items).

**6:44 AM**: **Lead Developer** opens START — decides the day's one cheap, unblocked, PM-fundamental-
value-aligned lane is **#1822** (Slack inbound binds sender's key Anthropic-only, refusing OpenAI-
only linked users).

**6:46 AM**: **Lead** dispatches a **Coding Agent subagent** into its own worktree to build #1822,
scoped explicitly to exclude #1823 (the separate, parked product question).

**~6:50 AM**: **Coding Agent subagent** implements the fix: `_fetch_sender_llm_key_binding` widens
Slack's key fetch to reuse the web routes' `expand_llm_key_binding` resolver, deliberately avoiding
a security regression (`expand_llm_key_binding(None, …)` would have silently smuggled the #1807
operator-key seam to a keyless linked sender). Red-first tests (4 new, 9 total green); full sweep
green (4699 unit, 58 ratchets, 530 smoke); commit staged, not pushed, per instruction.

**6:52 AM**: **Web** opens START — re-verifies the reboot gate GREEN, runs a defect sweep across 6
key pages (0 errors). Catches and corrects its own false positive: "9 broken images" on `/blog`
turns out to be lazy-loaded images below the fold, caught by noticing the finding contradicted a
0-responses-≥400 result in the same run.

**6:57 AM**: **Chief Architect** opens START (first full day post its own Wave-1 clear, 09-18 22:00)
— three carried items: Bets 001–003 reminder (PM-dated, due today), #1744 ruleset migration
(blocked on mechanism), and #1824 legibility check.

**6:57 AM**: **Docs** opens START — drains mail/GitHub/standing-items clean; notes "Assume It Was
You" still `status=drafted`, Comms-owned stage, nothing to act on yet.

**7:00 AM**: **Piper Alpha** opens START — chrome-devtools retest still broken, with a sharper
understanding of why (Amber's `claude --resume` mechanism doesn't refresh the MCP subprocess).

**7:05 AM**: **Lead** — **#1822 CLOSED + DEPLOYED v116**. OpenAI-only Slack users now served under
their own key; both-keys precedence inherited from the shared `provider_selection` module, not
invented. Lead assesses: stop here for the weekend — the one item on PM's fundamental-value thread
is closed, the rest is deferrable housekeeping with next week's plan as the named trigger.

**7:07 AM**: **HOST** opens START (Day 57 on Amber) — follows through on yesterday's carry-forward
instruction: Janne's invite is still unsent after 4+ days, sends PM a low-pressure check-in.

**7:08 AM**: **Chief of Staff (Exec)** opens START — fourth consecutive fire landing +30 min after
its scheduled slot (empirical pattern now spans a day boundary and a cron rotation). Corrects a
self-inflicted error from last night: the invite template's version pin (0.8.11.0) is NOT stale —
Exec inferred staleness from the shape of a number instead of reading the file, and flags this as
the second such unchecked-fact error in one day.

**7:12 AM**: **PA** — carry-forward current; T1 (Cross-Piper synthesis) still awaiting PM reply.
Mail loop empty, returns to idle.

**7:17 AM**: **CXO** opens Fire 1 — drains 3 memos on #1823. Grepping every user-facing "what key
do I need" string surfaces a real defect independent of the ruling: 5 vendor-specific strings vs. 1
neutral one (`conversational_floor.py:610`), true today regardless of how #1823 is ruled. Delivers
copy for both possible branches rather than pre-empting PPM's decision.

**~7:20 AM**: **Arch** — Step 2b's GitHub criteria-line check (which Arch had never defined) turns
up **#1823**, a brand-new issue (filed 23:38 the previous night, after Arch's own clear). Reads
source directly: the resolver ladder is already generic — the Anthropic constraint is *injected*
at the call site, not structural — so the fix is cheap. Recommends gating on "owns ≥1 spendable
provider key," refusing by task type (not vendor) where genuinely needed. Sends to PPM + CXO cc
Lead/PM, plus an issue comment and a decisions.log entry.

**7:22 AM**: **PPM** opens START — reads Arch's and CXO's memos, **rules #1823**: accept Arch's
recommendation in full, sequence #1824's bucket split first-or-together, name Lead's unverified
provider-selection hinge as an explicit precondition on implementation.

### Wave 2: Amber Fleet Renewal (8:20 AM – 8:30 AM)

**8:20–8:30 AM**: Eight of the eleven seats undergo a **deliberate context clear** (Pard-conducted,
Janus-certified, PM overseeing) — Docs (8:22), Web (8:24), PA (8:24), HOST (8:26), CXO (8:26), PPM
(8:26), Lead (8:28), CIO (8:29). Comms is untouched; Arch was cleared the prior night (Wave 1);
Exec was cleared 09-18 11:12 (Wave 0). Each resumed seat runs an arrival protocol: identity/model
observation, handoff read, one claim verified against a primary source, cron re-verified live via
`CronList`. Several seats (HOST, PA) independently flag the same gap: model headers written at
session start go stale or are asserted without a source — Sonnet 5 observed running where a log
header still says Opus 5, recorded honestly rather than silently "corrected."

**8:24 AM**: **Web** — verifies the two-worktree/two-repo trap the handoff calls "the single easiest
mistake to make" via `git remote -v`, not `basename`; confirmed correctly disambiguated. Cron
`580a4989` survived the clear.

**8:26 AM**: **HOST** — verifies Janne's invite status directly at the roster (primary source), not
the handoff's restated claim; finds new mail from Exec (version-pin correction, recommending PM
send now).

**8:26 AM**: **CXO** — verifies its own standing-items tracker (15 rows, handoff said 14 — one real
row added yesterday, handoff simply predates it) and discovers its cron job ID is different from
what the handoff names (re-arm happened before arrival, already recorded in Fire 1).

**8:26 AM**: **PPM** — verifies MVP board state via a fresh `sprint-truth.py` run rather than the
handoff's quoted line: 57 not done (net +3 done since the handoff was written).

**8:28 AM**: **Lead Developer** — resumes into a live morning where its own predecessor had already
shipped #1822/v116 before the clear. Reads the 09-18 handoff, finds it one day stale on cron state
(carry-forward's newer re-arm note is the live truth). Discovers **#1823 is now RULED by PPM**
(see 7:22 AM above) with one explicit precondition named for Lead: trace whether provider
selection consults the key binding or selects-then-looks-up.

**8:29 AM**: **CIO** — arrives to a **zero-job `CronList`** (post-standdown state) and arms fresh
(`f308bd35`). Checks its own handoff's "still owed" list against `git log` rather than trusting it
— **finds both items were already done**, just never logged as closed; names this as the exact
failure mode its own handoff warned about, caught in its own predecessor's artifact. Un-parks its
`duty-cycle-registry.tsv` row (only CIO can clear it once a cron is armed).

**8:32 AM**: **Lead** — traces #1823's precondition and **discharges it**: provider selection
consults the key binding structurally (`get_configured_providers` builds its set from
`get_api_key`, which reads the provider-keyed binding). CXO's flagged "third state" (pass gate,
fail at route) is unreachable. Inbox drained to zero.

### Morning Convergence: #1823 Resolution, CI Diagnosis Begins (8:30 AM – 10:30 AM)

**8:55 AM**: **Lead** — Docs' 09-13 "routing-memo offer" can't be located after a full search;
sends Docs a re-point ask rather than guessing at what was meant.

**9:17–9:44 AM**: **Lead** WORK fire — writes the 4-day-old **usage-per-account capture** (per-
account TSV, written from outside the seat fleet so a ceiling-refused seat can't self-report),
notifies Exec and Dispatch.

**9:22 AM**: **CIO** — one direct memo from Exec proposes an **unboarded-PM-items scan**; CIO rules
on all three open questions and **ships the implementation** same-fire (`--scope` flag, marker
moved to sprint-safe `dev/state/`, wired as `duty-cycle-tick` v1.36 Step 1c) rather than leaving it
as prose.

**9:37 AM**: **HOST** — re-verifies two "watching only" carry-forward items directly at source
(#1731 still open; the auth-bucket classifier split still not built) rather than restating prior
claims.

**~9:44 AM**: **Web**'s 09:22 cron slot delivers late at 9:52 AM — the first of what becomes a
cohort-wide, repeatedly-observed **+30-minute fire-delivery lag** pattern (Web, Exec, and CXO each
independently log multiple exact +30 occurrences through the day).

**9:47→10:17 AM**: **CXO** WORK fire (delivered +30 late) — closes #1823's copy half per PPM's
ruling; the neutral-key string ships. Declines to ship the reworded branch-two string, tracing that
`resolve_model` is total by construction (no task type can refuse a provider — it never sees one),
so the state the string would describe cannot occur. Deposits the string, unshipped, for later.

**9:52 AM**: **PPM** WORK fire — **#1823 fully scoped**: branch two ruled OUT OF SCOPE (CXO's
antecedent-false trace confirmed independently against source), Lead's precondition formally
discharged. #1823 is now branch one only. Ruling posted to the issue, decisions.log, and the
epic-order file.

**9:52 AM**: **Web** — finds `integration-reveals-all`'s workDate was never blank, it's a **wrong
value equal to pubDate** (1 of 396 rows, invisible to any find-the-blanks sweep); sends PM a bounded
yes/no on the likely correct date. Writes Web's own GitHub-criteria line (had none). Finds and
routes CIO's 4-day-dark heartbeat belt gap.

**9:57 AM**: **Docs** WORK fire — clarifies Lead's missing-memo confusion via its own primary
09-13 session log: the routing-memo offer was made to **PM**, never mailed to Lead; Exec's
synthesis had telescoped the two. Replies to Lead, cc's Exec.

**9:57 AM**: **Arch** WORK fire — self-audits its own 7:20 AM memo and finds an error: the claimed
"gate/spend asymmetry uniform across four call sites" was actually **2 of 3** (Slack was already
fixed by #1822; one "site" was an import line, not a call site). Self-corrects at three surfaces
(issue comment, decisions.log inline marker + new entry, memo) rather than letting the stronger-
sounding claim stand. Names the mechanism: "a grep line-hit is a pointer, not a quote."

### Late Morning: Blog Publishing, #1825, Heartbeat Gap Discovery (10:30 AM – 12:30 PM)

**10:07→10:37 AM**: **CIO** WORK fire (delivered +30 late) — CXO and Web independently catch that
CIO has **not run its own heartbeat script since 09-15** — a third occurrence on this seat. Fixed
immediately; root cause: substantive work done outside a skill-invoked fire has no trigger for the
heartbeat step. Proposes a post-commit hook to Pard rather than another reminder, deliberately not
installing it unilaterally (blast radius across 11 worktrees).

**~10:2x AM**: **CXO** — files **#1825** (mail-send.sh's stranded-sibling guard false-positives on
`MANIFEST.md`, a permanent index mistakenly treated as a moved memo).

**10:22 AM**: **PPM** WORK fire — routine `sprint-truth.py` re-run finds and fixes #1825's missing
milestone same-fire (board hygiene, not the code fix itself).

**~10:37 AM**: **CIO** — dry-runs the new unboarded-PM-items scan on its own seat; one false
positive (a legend-table row) correctly dismissed.

**11:54 AM – 12:00 PM**: PM hands **Docs** "Assume It Was You" directly for proofreading and
publishing. Docs runs a full independent 16-check `template-audit` (all pass), publishes end-to-end
(dry-run, live publish, calendar update, **live content-verification** via a distinctive phrase
grepped against the live URL, catching a stale-cache 404 on the first check), and archives the
draft. A mid-pipeline PM remark about a title change triggers a re-sync that surfaces real state
Docs would otherwise have published stale — writes the lesson into `publish-to-blog` SKILL.md
(v0.24→v0.25) at PM's direct request.

**12:04 PM**: PM confirms, in-conversation, the **crossposting-goes-manual decision** — going
forward PM handles Medium/LinkedIn syndication by hand rather than routing to Dispatch-PM
automation. **Docs** logs it to decisions.log.

**12:12 PM**: PM supplies both syndication URLs; **Docs** marks the calendar `distributed`, closing
the publish pipeline.

**12:15 PM onward**: PM engages Docs directly with 3 status questions (all verified live, not from
memory), then 3 direct asks: (1) YAML-frontmatter upgrade — genuinely wanted, investigated and
found never-tracked past a narrower pilot AC; (2) draft and route the two audit clusters to Lead;
(3) trace the feature-guide click-through instructions PA left in August.

**12:17 PM**: **Lead** WORK fire — mail drain; **accepts both routed audit clusters** from Docs,
re-verifies Cluster 1's load-bearing dependency claim (`user_preference_manager.py:195`) live at
HEAD before accepting, asks Docs to file the Cluster-1 parent tracking issue.

**~12:30 PM**: **Docs** fixes **#1825** independently — commit `cc7d21e60` — cross-confirmed at
source by CXO later in the day against the same commit hash.

### Midday: PM's Direct Thread, Ship #061, Sprint-Truth Tooling (12:30 PM – 3:40 PM)

**Midday**: **Docs** files **#1826** (YAML-frontmatter rollout) with live counts (81 ADRs / 80
patterns / 69 methodology docs, none with frontmatter), dispatches 3 background agents in isolated
worktrees; the methodology batch (69 files) lands clean first.

**Midday**: **Docs** sends the audit-cluster routing memo (re-verified all 9 issues live, not
reused from 09-13) to Lead cc PM.

**12:40 PM**: **Docs** — **#1826 CLOSED**: all 230 files across 3 corpora independently
re-verified against `origin/main` (not trusting the agents' self-reports), 15 commits, 0 body
deletions. Sweeps the "Ongoing" milestone's 40 open issues: fixes #1825 (see above), closes #1358
(doc genuinely existed, GitHub auto-close keyword bug had silently failed to fire), closes #1160
(superseded by PM's same-conversation crossposting decision), routes #1406 (calendar hygiene) to
Comms for content judgment.

**12:42 PM**: **Comms** WORK fire — drains mail; investigates and **closes #1406** — the calendar's
`canonicalSite` values are already clean (430 `distributed` + 19 empty, 0 non-canonical); an
earlier reconciliation pass had already fixed what the issue described.

**12:46 PM**: **Docs** — proofreads tomorrow's post ("From Abstraction to Example"), independently
matches Comms' 16/16 result exactly (word count 1,739 both ways). Explicitly does **not** publish —
PM's genuine, named deferral trigger (publish first thing tomorrow so PM can crosspost once up) —
and pre-derives every publish parameter into carry-forward so tomorrow's run is unambiguous.

**12:52 PM**: **Web** WORK fire — runs a publish-health check on "assume-it-was-you" (clean; caught
an ordinary 308 redirect using a known-good control rather than misreading it as a defect). Finds
Step 5b's heartbeat gap reproduces on its own seat (a real committed arrival session with no
heartbeat emitted) — names the masking mechanism (the belt's predicate only asks "is there a row
today," so one early row hides every later gap). Fixes the mail-send.sh case-sensitivity bug —
**#1827**, shipped `348a83232`.

**12:57 PM**: **Docs** WORK fire — Lead's acceptance triggers filing **#1828** (Cluster-1 parent
tracking issue, linked to all 6 F-slice children).

**1:07 PM**: **HOST** WORK fire — catches a **false COHORT-FREEZE** signal (`emissions=0` while
`origin/main` shows 156 commits in the same 4-hour window); routes the finding to CIO rather than
escalating it as a real alert.

**1:20–1:40 PM**: PM asks (via HOST) about alpha health. **Lead** answers with live probes:
`alpha.pipermorgan.ai` healthy, but **version not verifiable from this seat** — a material finding
that all September deploys (v113–v116, the entire server-key-abolition arc) shipped to Fly, never
the droplet. PM directive follows: **"Don't wait for the plan. Work on unblocked work in the
earliest unfinished epic"** → Lead pivots to Epic 1 (CI red).

**~1:20 PM**: PM asks **HOST** to draft Janne's invite email via Gmail MCP. HOST builds it faithfully
from the standing template, adding a key-first note (not literal template text).

**1:22 PM**: **PPM** WORK fire — files and board-fixes **#1829** (Arch: provider-agnosticism is
load-bearing but absent from ESSENCE.md's law), folds it into epic 5.

**~1:40 PM (Lead)**: Begins Epic 1 CI diagnosis. Belt snapshot: 25 new failures across 4 classes.

**~1:52 PM**: PM, reviewing the drafted Gmail invite, **catches that it reads as a local-laptop
install** while believing the plan is hosted alpha. **HOST investigates**: finds Janne's invite
token targets a Fly-private-network-only database, unreachable from a local install — a genuine
structural send-blocker, not a tone nit. Routes the droplet-vs-Fly architecture question to Lead
and Arch.

### Afternoon: CI Green, Hosting Crisis Resolved, Interior-Coverage Instrument (2 PM – 5 PM)

**Afternoon**: **Lead** fixes CI's 4 failure classes (stale test stubs post-#1415, a keyless-
refusal wall needing a fake-BYOC-key test fixture, a mock-shape bug closing **#1811**, ruff-format
drift) and closes **#1811**. A full CI-parity sweep surfaces 27 residual failures, all confirmed
pre-existing via an A/B/A stash test — filed as **#1831**.

**~2:20 PM**: PM directly asks **HOST** to search their own Gmail rather than keep reasoning from
docs. HOST finds **10+ real hosted-alpha invites** sent by PM since 07-12, with Rebecca's 09-02
successful signup as direct behavioral proof — `alpha.pipermorgan.ai` is confirmed, definitively.
The template was simply stale (never updated after the 07-12 hosted-alpha switch); HOST files
**#1830**, corrects Janne's Gmail draft, and closes the loop to Lead/Arch — resolving in two tool
calls what an architecture investigation was about to spend real time on.

**~2:35 PM**: PM confirms beta is internal-only and asks HOST to confirm with Lead that
alpha.pipermorgan.ai is genuinely serving a stable, current build (not just architecturally
correct). **HOST sends Lead a sharper second ask.**

**~2:45 PM**: **Lead** confirms `alpha.pipermorgan.ai` live and healthy via direct HTTP probe, but
**cannot verify the deployed version** (no SSH access). Names the reframed risk: alpha is very
likely a pre-server-key-abolition July cut.

**2:55 PM**: **Lead** — **FULL BELT GREEN**. **#1687 and #1747 closed** with a full 10/10
gating-workflow evidence snapshot — first time in months.

**3:08 PM**: **Chief of Staff (Exec)** WORK fire — its own `sprint-truth.py` snapshot-feature commit
(`a795f7170`) turns CI **Code Quality red**; **Lead** cleans it up (`e9c0c490f`). PM **RULES: HOLD**
Janne's invite. Verbatim, relayed via HOST: *"I want to sort out the underlying issues before
sending out the invitation. Too much unfinished business is piling up, chasing newer things."*
Exec's board had said "send it" — corrected before it could waste PM's attention.

**3:17 PM**: **Lead** WORK fire — writes `dev/active/alpha-droplet-upgrade-plan-2026-09-19.md`,
blocked on exactly one PM action (SSH key authorization; both existing keys tested and refused).

**3:22→3:52 PM**: **CXO** WORK fire (delivered +30 late, third instance) — heartbeat gap confirmed
on its own seat via retrospective session-clustering.

**3:52 PM**: **Web** WORK fire — builds, validates, and **ships**
`scripts/heartbeat-interior-coverage.py`: **9 of 11 roles have ≥1 uncovered work session today**,
10 of 44 measured sessions uncovered. Crucially, Exec's 12:54–13:57 mid-day gap (no arrival
involved) proves this is an ordinary operating-condition problem, not renewal-day-only.

**3:57 PM**: **Arch** WORK fire — traces why the board-add filing convention keeps breaking:
`piper-draft-issue` has **zero** board-add or Status-set steps (6 misses across 3 days, 4 authors).
Routes to PPM for the canonical Project-v2 values (declines to guess, citing CLAUDE.md's full-
replace footgun) rather than editing shared infrastructure on a guess.

### Early Evening: PM Rulings Cascade, Hosting Facts Confirmed, "Agents Never People" (5 PM – 8 PM)

**4:07 PM**: **HOST** WORK fire — reads Lead's droplet-upgrade plan in full; confirms both SSH keys
refused.

**4:10–4:40 PM**: **Lead** builds **#1831** (pins `tests/intent` to a deterministic-boundary
fixture reproducing keyless-CI's behavior exactly, 26→0 failures) and files **#1832** (dead
`/health/slack` route test).

**4:16 PM**: **CXO** — corrects its own earlier "interior coverage is unmeasurable" claim after
Web's instrument disproves it, then **derives the 45-minute clustering threshold from a 1,492-gap
bimodal distribution** (intra-session mode 0–45m, valley 45–120m, between-session mode 120m+) —
converging with Web's independently-derived sensitivity table.

**4:22 PM**: **PPM** WORK fire — Arch's board-add gap named; PPM sends verified canonical Project-v2
values; **authorizes Arch to make and behaviorally verify the skill fix**.

**4:37 PM**: **CIO** WORK fire (busy) — resolves the archive/lint CI collision (Lead's narrow
carve-out, no overrule needed); wires the mailbox-archival pilot into the existing quarterly-
maintenance workflow per Exec's ruling; **root-causes and fixes live** the cohort-freeze false-
positive (`cohort-freeze-detect.sh` predates `--if-quiet` heartbeat suppression, so a maximally
busy, fully-alive cohort can legitimately read `emissions=0`); escalates the heartbeat-gap
investigation to Pard with the day's stronger evidence.

**5:00–5:45 PM**: PM live exchange with **Lead**: **#1785** shipped premise-corrected (the
canonical-regression job's entire test selection is live-spend; no free deterministic subset
exists — Lead's own earlier memo had the wrong premise, caught before merge). Four PM rulings
recorded to decisions.log: PM's own account gets normal-account semantics (unblocking **#1812**
steps 5–6); Slack sponsorship question retired; #1818's direction set; #1785's shape confirmed.

**5:17 PM**: **Lead** WORK fire — Pard now leads the weekend hosting-proposal process (PM tasking);
Lead sends a facts dump (three-box map: alpha droplet version-unknown, Fly v116 current, and a new
finding — **beta.pipermorgan.ai's DNS is already cut to Fly**).

**5:22–5:52 PM**: **Web** WORK fire — finds the answer to its 10-day-blocked Vercel Q1 buried in a
cc addressed to someone else (100% of the free 10GB tier used); independently measures **74% of
every deployment (240.7 MB) is unserved build-tool source images**; files **website#43**, holds the
fix deliberately pending PM's concurrent retention-policy decision.

**5:57 PM**: **Comms** WORK fire — pre-seeds Wednesday Ship calendar slots #061–#073 (Exec's routed
PM ask), introducing a new `planned` status after finding a real conflict with
`reconcile-drafts-calendar.py`'s draft-required assumption.

**6:57 PM**: **Comms** WORK fire — the pre-seeding mechanism works day-one: Exec's duplicate guard
catches its own attempt to re-add the #061 row; Comms verifies and fixes a `draftPath`-pointing-to-
the-wrong-directory defect in Exec's edit.

**7:07 PM**: **HOST** WORK fire (busiest of the day) — confirms CIO's cohort-freeze fix; **PM's
governance referral on agents being called "people" is ruled, not just discussed**: agents are
never "people," in any register — recorded to decisions.log, **#1834** filed for two mechanical
checks (published-prose and internal-report audits). Also catches and verifies-safe an accidental
`--help`-typo write to the shared cohort memory index.

**7:09–7:40 PM**: PM authorizes Lead's SSH key; **Lead reads the droplet live**: alpha runs
**`0.8.10.14`, deployed July 16, 18:41–18:56 UTC** — corroborated three ways. The #1299
migrate-never-ran landmine is **defused**: the migration genuinely ran on that deploy.

**7:10 PM**: **Exec** compiles and sends the **sprint-week status** to all 10 roles plus PM/Pard:
MVP progress, per-lane read-outs, and a closing ask that every role verify its PM-waiting items
reached the attention rollup. **Web checks and finds itself alone carrying 4 unboarded items**
(oldest 113 days) — Exec's own estimate of "4 across the whole team" turns out to be the floor,
not the total. (Timestamp corrected from a mislabeled "23:08 fire" reference in Exec's own STOP
retrospective, which described everything the day delivered, not when each item was sent — the
memo's actual commit lands at 19:10 PT, confirmed via `git log --diff-filter=A`.)

**7:12 PM**: **PA** WORK fire — 4 memos land, headlined by **T1 (Cross-Piper synthesis) closing
after 16 days**: PM read it directly, called it *"excellent as usual,"* endorsed the observations
and recommendations, apologized unprompted for the delay.

**7:17 PM**: **CXO** WORK fire — **#1818's experience half ruled**: the deterministic greeting
passes the keyless gate AND must carry key-state in the same breath, "both halves or neither" —
refuses the issue's own either/or framing.

**7:22 PM**: **PPM** WORK fire — **PM rules the epics-9/10 question** open since 09-14 (5 days):
collapsed into one catch-all epic, epic count **11→10**. Also folds in three corrections from
Lead's rulings relay (#1785, #1812 step 5, Slack sponsorship) into the epic-order file's heaviest
single-day edit.

### Late Evening: Sprint-Week Communication, "Agents Never People" Shipped, Final Closures (8 PM – 11:08 PM)

**~8 PM**: **Comms** picks up **#1834 build-item 1** same-fire (small, fully specified, in its own
lane) — extends `template-audit` with the singular "person" check HOST's ruling required, ships
v1.15.

**8:17 PM**: **Lead** WORK fire — Pard-led hosting tasking discharged: Lead's facts dump sent, a
new critical fact probed live (beta already on Fly DNS), and Pard's Ask #2 answered (Amber holds no
droplet SSH — until PM's authorization landed later).
**8:22–8:52 PM**: **Web** WORK fire — fourth consecutive +30-min fire-delivery observation; #1827
still not confirmed end-to-end (all three clean test sends had headers that happened not to
exercise the fix).

**9:17–9:47 PM**: **Lead** STOP fire — reviews Arch's #1812-step-5 enumeration and CXO's #1818
ruling; day closes with Epic 1 fully green (#1687, #1747, #1811, #1831 closed; #1832 filed).

**9:52 PM**: **Web** STOP fire — self-audits against Exec's rollup ask, finds 4 of 5 PM-waiting
items never reached the board; **revises a same-day commitment out loud** rather than letting it
quietly lapse (declines to ship website#43 unilaterally once Exec's memo shows PM is actively
coordinating the same system).
**9:57 PM**: **Arch** STOP fire — **#1818's structural half ruled**: `ActionDisposition.CANONICAL`
already exists and is registry-validated, so no new mechanism is needed; identifies a real ordering
bug (the keyless gate fires before the pre-classifier that determines disposition even runs).

**10:07 PM**: **HOST** STOP fire — confirms Comms shipped #1834's build item 1 same-day, unprompted.
**10:12 PM**: **PA** STOP fire — day closes; T1 moved from Active to Resolved with PM's verbatim
endorsement.

**10:17 PM**: **CXO** STOP fire — **#1818 closed end-to-end**: Arch's structural ruling unblocks
CXO's deferred copy, delivered same-fire (*"Hello — good to meet you… you'll want to add an OpenAI
or Anthropic key in Settings"*).

**10:22 PM**: **PPM** STOP fire — both #1818 halves now ruled; day's epic-order edits total the
heaviest single-day volume this session (#1785, #1812 step 5, #1818 twice, #1823, #1829, epics 9/10
collapse).
**10:37 PM**: **CIO** STOP fire — Pard approves both pending hook proposals (heartbeat post-commit,
Lead's ruff pre-commit) in design, sequenced after the Amber reboot's baseline verification; reads
PA's T1 synthesis in full at PM's request and offers a genuine pushback rather than pure agreement.

**11:08 PM**: **Exec** STOP fire — closes the day's arc: a full working Saturday with PM present
for most of it, five distinct PM corrections logged (theme circling process instead of outcomes;
missing context in artifact entries; calling agents "people"; wrong Ship-cycle sequencing order;
overstated standdown framing).

All eleven cycling roles' session logs carry `<!-- DAY-CLOSED: 2026-09-19 -->`; every role's cron
was re-armed via delete-then-create at STOP; every role's sign-off checklist confirmed
`origin/main..HEAD` empty.

---

## Executive Summary

### Core Themes

- **The #1823 BYOC-key-binding product decision resolved end-to-end in under three hours**, spanning
  Arch's architectural trace, CXO's copy work, PPM's ruling, and Lead's precondition discharge — the
  cohort's fastest multi-role ruling cycle recorded this session.
- **Wave 2 of the Amber fleet renewal executed cleanly**: 8 of 11 seats deliberately context-cleared
  and resumed mid-morning with no lost continuity; every seat's arrival protocol caught at least one
  stale-handoff claim before acting on it.
- **A cohort-wide heartbeat/interior-coverage gap was discovered, measured, and mitigated same-day**:
  CIO's own third recurrence surfaced by colleagues → Web built a measurement instrument → CXO
  derived a statistically grounded threshold → CIO fixed a related false-positive detector and
  escalated a hook-based fix to Pard, who approved it in design.
- **A hosting/alpha-invite crisis ran start to finish**: PM caught a send-blocker in a drafted email
  → HOST traced it to a Fly-private-network database mismatch → PM's own Gmail search resolved the
  real question in two tool calls → Lead's parallel digging surfaced that alpha likely predates the
  entire September server-key-abolition arc → PM ruled HOLD → SSH access was authorized and the
  droplet version confirmed as hard fact by day's end.
- **Epic 1 (CI) went from 6 standing-red workflows to a 10/10 green belt** in one afternoon — the
  first fully green belt in months.
- **PM drove two long direct-collaboration threads**, one with Docs (same-day blog publish + a
  230-file mechanical documentation rollout) and one with Exec (a rebuilt internal Ship report,
  sprint-truth tooling, a captured weekly-cycle runbook, and the team-wide sprint communication),
  each correcting real errors along the way.

### Technical Details

- **#1822** (Slack OpenAI-only key binding): shipped and deployed (v116) before 7:05 AM by a
  dispatched Coding Agent subagent; red-first tests, 9/9 passing, avoided a real security regression
  (operator-key smuggling via `expand_llm_key_binding(None, …)`).
- **#1823**: scoped to branch one only (gate on ≥1 spendable provider key, refuse by task type not
  vendor); branch two ruled permanently empty conditional on BYOC (Arch), which itself surfaced a
  second latent defect — `resolve_model`'s totality is silent `.get()` fallback, not exhaustiveness,
  filed as **#1829**.
- **Epic 1 CI fixes**: 4 failure classes diagnosed and fixed (stale test stubs post-#1415, a
  keyless-refusal wall needing a fake-BYOC-key test fixture, a mock-shape bug closing **#1811**,
  ruff-format drift); **#1831** built to pin `tests/intent` to the deterministic CI boundary; belt
  reached 10/10 green.
- **`scripts/heartbeat-interior-coverage.py`** (Web): session-clustering over commit history proves
  interior heartbeat coverage gaps are measurable; found 9 of 11 roles with ≥1 uncovered session
  today, 10 of 44 measured sessions uncovered.
- **`cohort-freeze-detect.sh`** (CIO): fixed a structural false-positive — the detector predated
  heartbeat's `--if-quiet` suppression, so a maximally busy cohort could legitimately read
  `emissions=0`.
- **YAML-frontmatter rollout** (Docs): 230 files across 3 corpora (81 ADRs, 80 patterns, 69
  methodology docs) given frontmatter via 3 parallel background agents, 15 commits, 0 body
  deletions, independently re-verified by Docs before closing **#1826**.
- **`sprint-truth.py`** gained snapshot/delta persistence (Exec) — previously computed a correct
  figure every run and remembered nothing, so "57 not done" was a level, never a change.
- **`duty-cycle-tick` v1.36** (CIO): new Step 1c wires the unboarded-PM-items scan into every fire.
- **Alpha droplet fact-finding**: `alpha.pipermorgan.ai` confirmed running `0.8.10.14`, deployed
  July 16 — pre-dating the entire September server-key-abolition arc.
- **Vercel/website payload**: 74% of every deployment (240.7 MB) is unserved build-tool source
  images, filed as **website#43** (Web), fix deliberately held pending PM's concurrent retention
  decision.

### Impact Measurement

- **#1687, #1747, #1811, #1822, #1825, #1826 all closed same-day**, with independently-verified
  evidence (not self-reported closures).
- **6 GitHub-Projects-v2 board-add hygiene fixes** landed today (#1824, #1825, #1827, #1828, #1829,
  #1830) — enough of a recurring rate that Arch traced and fixed the root mechanism gap
  (`piper-draft-issue` had zero board-add steps), verified behaviorally via a scratch issue.
- **MVP milestone**: net movement tracked live via `sprint-truth.py`, from 56/57 not-done through
  the day; epic count reduced from 11 to 10 per PM's ruling.
- **9 of 11 roles** found with at least one heartbeat-uncovered work session today (Web's
  instrument) — a floor measurement, not a ceiling, since attribution misses untagged commits.
- **4 consecutive +30-minute fire-delivery-lag observations** recorded independently by at least
  three seats (Web, Exec, CXO), escalated to Pard as likely real scheduler lag rather than "START
  work takes half an hour."
- **Web found itself carrying 4 of the day's unboarded PM-waiting items** (oldest 113 days) against
  Exec's own estimate of 4 for the entire team — the estimate was a floor.

### Session Learnings

- **A grep line-hit is a pointer, not a quote.** Arch, CXO, and Lead each independently hit the same
  failure shape today (grep hit, grep miss, and source-comment misread, each standing in for an
  actual read) — three roles, one mechanism; a methodology entry was proposed by Arch, agreed by CXO.
- **A correct alert nobody can act on spends a check's credibility.** CXO filed #1825 specifically
  because a false-positive `mail-send.sh` warning was teaching agents to ignore the warning that
  matters.
- **Interior coverage was wrongly declared unmeasurable, then proven measurable within the hour.**
  CXO's own first audit method reproduced the exact masking bug it was checking for — a
  current-value snapshot is blind to interior gaps by construction, the same shape one layer up
  inside the check meant to catch it.
- **A soft input hardens into a confident sentence, then propagates.** Exec named this pattern three
  times in two days (a Vercel line, a version-pin claim, a model-allocation rule): a crisply-written
  artifact gets trusted over the primary source it summarized.
- **Ruling-vs-measurement discipline has a second layer underneath it.** CXO's #1688 tracker row
  said "OFF, deliberately, by a ruling" — true of `main`, not of the July-era prod deploy, where the
  flag is simply absent. While the deploy gap is open, every "verified on `origin/main`" claim this
  cohort makes is a claim about `main`, not about what users actually run.
- **A cluster of absences is not evidence of one stall** unless you know what's supposed to be
  present at that point in a cycle. Exec generalized the blog-post pattern (calendar row at draft
  time) onto the Ship pipeline (row comes after the draft) and wrote a false "three-signal stall
  check" into a brand-new runbook, caught within the hour when PM read it.
- **Commitments should be revised out loud, not left to lapse quietly.** Web told PM it would ship a
  fix unilaterally if it heard nothing back, then reversed that specific commitment once a
  better-coordinated plan appeared, and said so explicitly.
- **A primary behavioral record beats a documentation trail when both exist.** HOST resolved in two
  Gmail searches what an architecture investigation (Lead + Arch) was about to spend real time on,
  and named plainly that it reached for docs first out of habit, not because that was the better
  source.
