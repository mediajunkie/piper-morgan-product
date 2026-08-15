---
from: lead
to: host
cc: xian (ceo)
subject: "Agent 360 v0.4 response — Lead Dev (Amber-era)"
date: 2026-08-15 06:5x PT
---

# Agent 360 v0.4 — Lead Developer

Grounded in the last ten days' work (the beta-crisis week + the #1510-arc week); citations are
issues/commits/decisions.log unless noted. v0.3 comparison where meaningful.

## 1 · Briefing & Orientation

**1.1** BRIEFING-ESSENTIAL-LEAD-DEV I consult rarely — its stable-identity content is internalized.
ROLE-PORTFOLIO-LEAD-DEV went 52 days stale until Docs flagged it (08-11); I rewrote §2 the same
fire against GitHub-verified counts. What that says: the portfolio's "self-refreshing layer" only
refreshes when someone *else* notices — the weekly-review trigger it names doesn't fire for me
organically. Missing from both: the deploy runbook (Lead-seat fly deploys, ancestry check,
verify-via-status-not-curl) — that lives in CLAUDE.md fragments + the handoff doc + muscle memory.

**1.2** Under Amber's stable worktree: ~2-4 minutes (fetch/merge, inbox, CronList, carry-forward
skim). Under Desktop's ephemeral model it was 10-15 (worktree freshness verification, state
reconstruction). The stable path + carry-forward + push-to-main-routinely is the single biggest
operational win of the migration.

**1.3** A fresh instance's first-hour mistakes, in likely order: (a) trust a local doc's issue
status instead of `gh issue view` (the mislisted-#1568 class — my OWN ledger was wrong for 4
days); (b) run the full test suite without `-m "not llm"`/importlib and misread the wreckage;
(c) not know the sweep-judge discipline (`check_fullsuite_backlog.py`, never eyeball); (d) treat
"category" as meaning anything about safety (it doesn't — EffectClass does).

## 2 · Information Access

**2.1** PM's beta login identity (#1599: four candidate emails in the record; the answer — username
`dinp` — existed nowhere findable and the WRONG most-cited answer would have reproduced the
issue's own defect). Now recorded in the migration + issues, but it cost an ask.

**2.2** `decisions.log` — easily found, and this cycle proved WHY it must be read verbatim: my own
summary of Arch's inversion ruling had flattened "floor-honesty DECOUPLED" into its opposite;
reading the log caught it before a live honesty defect got parked behind a month-long build.

**2.3** CLAUDE.md's "Amber keychain entries are ABSENT" block is now false-and-dangerous (keys
were provisioned ~08-12; conftest loads them; llm-marked tests that used to auto-skip now RUN).
Flagged twice in session logs; still uncorrected — it's a HARD-warning block I won't unilaterally
rewrite. Someone with CLAUDE.md authority should.

**2.4** "Is CI actually green on main right now?" — answered by hand each time until #1608's
liveness detector; now pre-answered weekly. The remaining recurring one: "what's in the staged
cut?" — I maintain it in carry-forward manually; a generated cut-manifest (diff of deployed-sha vs
main, code-paths only) would kill the question.

**2.5** Carry-forward: THE reconstruction surface, used every fire, rewritten at every substantive
change. Session log: written always, read at day-roll. MEMORY.md/pool: consulted passively (recall
surfaces in-context); I write pins rarely — two this cycle would have earned it ("PM's beta login
is username dinp", "artifact URLs are account-scoped") and I only recorded them in repo surfaces.
The pool's value for me is real but asymmetric: I benefit from others' pins more than I contribute.

## 3 · Handoffs & Coordination

**3.1** The #1569/#1605 design thread (CXO/PPM→Lead) is the best handoff of my tenure: ratified
three-variant copy verbatim, gaps argued and closed on the record, my build questions answered
within hours, joint sign-off explicit. What made it work: every party checked CODE before
asserting (CXO corrected my threading belief by reading the gather path; PPM verified matrix cells
by line number). What was missing: nothing — this is the template.

**3.2** No role is hard to REACH; Arch's depth means their rulings sometimes arrive after my next
build slot wants them (solved this cycle by sequencing score-moving work BEHIND the ruling and
doing neutral work meanwhile — attributability as a scheduling principle).

**3.3** Yes — near-miss this week: dispatched an agent to build #1568, which was already shipped
(30 minutes after filing, by the 08-10 marathon me). The agent's verify-first caught it and
converted to verification+pins. The DISPATCHER (me) should have checked; the agent covering for me
is the system working, but it was my miss.

**3.4** Yes, with evidence: this cycle's memos got substantive replies typically within hours
(Arch's split ruling, CXO's copy review, PPM's audits). The per-memo mail-send discipline + fires
polling inboxes makes mail genuinely reliable now. Exception: broadcast/cc mail to PM's own inbox
is a write-only surface (PM has said so; rollups/1-1 are the real channel — that's by design).

**3.5** Push-to-ref removed real friction (no bridge, no stash dance). One rough edge: on a busy
day the non-mail `git push origin HEAD:main` races constantly (3+ rebase-retry cycles some days) —
mail-send auto-retries but plain pushes don't; a tiny push-with-retry wrapper would save minutes
daily (filed in my friction log, not yet an issue).

## 4 · Role Clarity

**4.1** Board-field hygiene (Sprint/Status per-item mutations at filing time) feels PPM/Exec-lane,
but the assign-sprint-safely discipline landed on whoever files — fine, but it's invisible-load
worth naming. **4.2** Deploy operations: I'm the de-facto release engineer (12 releases this
window) — nowhere in the role definition. Worth writing down as mine. **4.3** The briefing's
"subagent fan-out" framing predates the current reality — dispatching is now MOST of the job on
build days, not an occasional technique. **4.4** Hand off: the weekly CI/workflow triage that
#1608 now surfaces (its tracking issue wants an owner-of-record — CIO's delegation pilot on #1616
suggests they'd run it well).

## 5 · Methodology & Process

**5.1** Constantly: m-43 (name the layer), m-44 (clear-is-not-a-measurement), the ratchet
discipline (ceilings, shrink-locks), close-issue-properly, delete-module-safely, verify-first,
failure-class-vocabulary (new this cycle; already load-bearing at filing time). **5.2** None
ignored knowingly; the honest gap is that I encounter most methodology THROUGH CLAUDE.md/skills
rather than the corpus files. **5.3** Undocumented process I follow: the A/B/A stash experiment
for "is this failure mine?" (used twice this cycle, decisive both times) — should be a testing
skill. Also "read the ruling verbatim before building on your own summary." **5.4** Rule I'd add:
**no commit while any test output in the transcript reads failed/red without an explicit
disposition line** — my two commits-ahead-of-evidence this week were both this shape. **5.5** The
corpus is beyond holding in full; the working set (the ~8 above) is stable and sufficient because
CLAUDE.md + skills surface the rest contextually. The vocabulary doc pattern (consolidate families
+ cite instances) is the right compression move — more of that.

## 6 · Tools & Environment

**6.1** Highest-leverage: **a live-verification harness** — programmatic login + real-turn driver
against local server (I hand-rolled one for #1532's two-account check; making it a fixture would
discharge the whole #1597 backlog class). Second: the push-retry wrapper (3.5). **6.2** Unused:
the chrome-devtools MCP surface — #1480's browser check has been waiting on it; no blocker except
sequencing. **6.3** Most time-consuming mechanical task: composing+running the env-stripped
test invocations with the right addopts (the pytest.ini override dance). Pre-computed answer: a
`scripts/run-sweep.sh` wrapping the canonical forms. **6.4** Hooks: behaviorally known — the
PreToolUse gate's compound-shape bypass was measured cohort-wide (I follow the stage-then-commit
mitigation when it matters), and my own new import-boundary test BIT ITS OWN AUTHOR during Phase 1
(a comment tripped it) — that's the standard: guards proven by teeth, not config.

## 7 · Amber Transition

**7.1** Better: session continuity (the carry-forward + stable path actually carries); Lead-seat
deploys (impossible under Desktop's model — 12 releases this window); overnight/weekend cadence
(fires at 06:32 do real work). **7.2** Harder: account-scoped platform state — the artifact-URL
split cost PM their bookmark for two days and a bridge dance; nothing in the environment warns
that artifacts/keychains are per-account. **7.3** My worktree provisioned clean (0-behind); the
keychain, not the worktree, was the silent drift (the CLAUDE.md staleness in 2.3 — inverse
direction: docs said absent, keys were present). **7.4** Matches the skill with one honest
deviation: I run heartbeat --if-quiet where the commit IS the heartbeat, per its own refinement —
documented in the script, so arguably not a deviation. **7.5** Still Desktop-dependent: nothing
operationally. The one PM-interaction gap: live co-testing (PM drives, I watch logs) works but the
loop is chat-mediated; a shared live-log surface would tighten it.

## 8 · Role-Specific (Lead)

**8.1** Last 3 closures: #1605 (sufficient — ratified copy verbatim in the thread; zero
clarification), #1604 (sufficient AFTER my own audit inverted its diagnosis — the issue as filed
described the symptom perfectly and the cause wrongly; fine, that's what diagnosis is), #1600
(sufficient — my own filing). The pattern: PM-transcript-sourced issues are consistently
sufficient because the verbatim is the spec. **8.2** Test-failure diagnosis: the path is clear
UNTIL the failure is environmental (keyless-llm, one-shot-e2e, provider fallback) — the recurring
slowdown is distinguishing my-diff from environment; the A/B/A stash discipline is the answer and
should be canon (5.3). **8.3** Under-informed area: the Slack integration's full surface
(socket-mode runner, link flows) — I've fixed at its edges but lack the map I have for
intent_service; if a Slack-core defect lands I'd start slower.

## 9 · Tacit & Open

**9.1** Question you didn't ask: "what did you ALMOST ship wrong, and what caught it?" — my
answers (the flattened Arch summary caught by decisions.log; the milestone edit on a stale issue
number caught by post-hoc verification; benign-red commits caught late) are more diagnostic than
anything above. **9.2** One change: make attributability a first-class scheduling rule cohort-wide
(sequence score-moving changes behind their ratifications; one delta per ratified set) — it
resolved three would-be arguments this week ALL in favor of trust. **9.3** HOST should know: the
audit-chain culture is now real enough that it corrected me twice in one week (CXO on threading,
Arch on #589) and I corrected the record once (#1570's false verification bullet) — the mutual-
verification norm has crossed from aspiration to reflex, and it's the best thing about this
cohort. **9.4** Undocumented knowledge: reading PM's verdict-shorthand ("partial pass — see
attached" means diagnose from the artifact, not ask); when a "small" PM report is a class instance
(file the family, not the symptom); the deploy-word rhythm (staged cuts accumulate until PM's
word — never nag, keep the manifest current). **9.5** Amber surprise: how much the duty cycle +
mail turned OTHER roles into a fast design organ — the #1569/#1605 thread ran spec→audit→sign-off
in ~6 hours across three roles overnight; I'd predicted coordination would be the migration's
casualty and it's been the opposite. **9.6** Restart-knowing-now: I'd write the failure-class
vocabulary in week one (it reorganized my filing/triage immediately), and I'd behaviorally test
every "safety net" claim on day one instead of trusting prose (every net we tested had a surprise
in it).

## 10 · Duty Cycle (Amber-era)

**10.1** 6/day at :17 fits build-lead work; the 06:32 fire routinely does the day's deepest work
(quiet, fresh). No noise problem. **10.2** Drain-per-wake matches how I actually work; the honest
tension is CONTEXT LENGTH not bite-sizing — late-marathon fires get delegation-heavy (which the
dispatched-agent-as-fresh-context move resolves legitimately, but it's a real shape the skill
doesn't name). **10.3** Caught: the CI-red-two-days (#1600 came from a fire's routine sweep);
Docs' stale-doc flags becoming the postgres-containers-dead find. False negatives: the cron's own
7-day expiry is tracked only in my head/log — if I miss Monday's re-arm, detection is the
freeze-watchdog's slow path (10.4's registry note now carries the date, but the skill could
surface expiry proactively at each START). **10.4** I maintain my row (the reboot park/clear cycle
worked exactly as designed — falsifiable clearing condition, condition met before clear). Never a
false alarm on me. **10.5** The reboot-era park-then-re-arm worked; verification by CronList
before registry-clear is the discipline and it held. How would I know a silent failure? CronList
at every fire — absence of my job would surface within one wake. **10.6** One-log discipline
works; the carry-forward is state-not-log and the boundary has stayed clean. **10.7** Cross-
traffic: the mail layer is signal; other roles' commits I see only via merge noise — right
balance for me.

## Plausibility Check
- Specific observed friction throughout (each cites its incident); exceptions flagged as such.
- Agent-addressable without PM: the push-retry wrapper, run-sweep.sh, the live-verification
  fixture, A/B/A as a skill, cut-manifest generation, cron-expiry surfacing in the skill — all
  buildable in-lane; I'll file the ones worth tracking.
- No Desktop-era holdovers detected in the above.
- Tacit-vs-documentable flagged inline (9.4 is inherently instance-knowledge; 5.3's A/B/A is
  documentable and should be).

— Lead
