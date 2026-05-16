# CIO V1 Autonomous Duty Cycle — Design v0.3

**Author**: CIO (Piper Morgan, Code instance)
**Date**: 2026-05-16 (v0.3 absorbs research-agent findings on wake-up mechanism)
**Status**: Draft v0.3 — PM-ratified pre-implementation; ready for routine setup
**Predecessor**: `dev/active/cio-v1-duty-cycle-design-v0.2-2026-05-16.md`

---

## What changed from v0.2

Research-agent investigation (claude-code-guide subagent, ~1:25 PM) identified **Anthropic Routines** as the only wake-up mechanism that fits "cloud-hosted, no local-machine dependency." Routines have a **1-hour minimum interval**, which displaces v0.2's 30-min default.

PM ratified 1:35 PM:
- ✅ 1-hour interval acceptable for V1
- ✅ Phase 0 routine setup is PM's action (later this afternoon)
- ✅ Phase 1-3 dry-run sequence acceptable

**Two substantive changes** to V1:

1. **Cadence: 30-min → 1-hour interval**. Routines mechanical floor. Cohort feedback didn't strongly object to 30-min specifically; 1-hour still validates trust property at 24 cycles/day.
2. **Worktree-default mechanic moot at cycle level**. Routines do per-run fresh clone — cycle doesn't accumulate worktree state across runs. Cycle commits go to `main` (mailbox-on-main discipline; sign-off after each cycle). Substantive non-mailbox work CIO does within a cycle continues to use `claude/*` branches per existing worktree-default discipline. Per-run fresh clone is *advantageous* for V1: clean slate, reproducible, no cross-cycle drift in working tree state.

**Everything else carries from v0.2** unchanged: artifact structure (structured Day-N digest + enumerated escalations + active-cohort-threads section); authority model (existing conversational practice); operating discipline (bias-toward-MORE-escalation; trust bidirectionality); Mushy middle (dashboard / dynamic cadence / cross-agent extension).

---

## Frame: three horizons (unchanged)

1. **North Star** — PM trusts work moves forward at appropriate cadence without needing to check
2. **Next Horizon** — two-week proof-of-concept (V1) via Anthropic Routines, 1-hour interval
3. **Mushy middle** — incremental from Gall's law

---

## Wake-up mechanism: Anthropic Routines

Per research-agent investigation (claude-code-guide subagent, May 16):

**Routines** (Anthropic, April 2026 release) is purpose-built for autonomous cloud-hosted Claude Code agents. Key properties:

- **Runs on Anthropic cloud** — no laptop dependency
- **Per-run fresh clone** — reproducible state; no cross-run drift
- **No mid-execution permission UI** — constraints baked into routine config upfront
- **Each run = separate session** in PM's session list — strong observability
- **"Run now" button** for one-off dry-runs before enabling schedule
- **Minimum interval 1 hour**
- **Capped daily runs** by plan (well above 24/day for typical configs)

Alternatives considered + rejected:
- `/loop`: requires open session + local machine on
- Desktop Scheduled Tasks: requires laptop on

Sources: [Anthropic Routines docs](https://code.claude.com/docs/en/routines.md); [Scheduled tasks docs](https://code.claude.com/docs/en/scheduled-tasks.md).

---

## North Star (unchanged from v0.2)

CIO operates autonomously on a rhythm, mail-driven, never silent, with decisions and questions visible to PM at a single glance. The cycle's quality is judged by one metric: **does PM trust that work is moving forward at the appropriate cadence without needing to check?**

Trust is bidirectional + lagging (per HOST). V1 errs toward MORE escalation; calibrates down with PM-reaction feedback over the two-week window.

---

## Next Horizon: V1 two-week proof-of-concept

### 1. Cadence primitive — Routines, 1-hour interval

Routine fires every hour (`0 * * * *` cron). 24 cycles/day. PM tunable up but not down (Routines floor).

### 2. Authority model — extend existing conversational practice (unchanged)

Per PM May 16: existing pattern ("do everything unblocked, batch questions, use discretion") is the operating rule. V1 biases toward **more** escalation than conversational equivalent; calibrate down.

### 3. Escalation surface — `dev/active/duty-cycle-escalations-cio.md`

Live as of 2026-05-16 ~1:25 PM (initialized). Structured format per CXO Framing 2; active-cohort-threads section per PPM contribution; cross-agent globbable naming per CXO Framing 4.

### 4. Day-N reconciliation — structured-markdown digest

Once-a-day digest at bottom of session log at ~10pm Pacific. Per CXO Framing 1 structured shape; per PPM Ship-publish-day awareness; per exec commit-message one-line summary in subject.

### 5. Cycle-level git mechanics — fresh-clone-on-main; commits and pushes go to `origin/main`

Routines clone the repo fresh per run. V1 cycle works on `main`:
- Mailbox operations (read, move to read/, distribute memos) go on main per existing discipline
- Methodology-corpus updates (tracker, methodology entries, pattern files) go on main
- Substantive *implementation* work would still use `claude/*` worktree branches — but V1 cycle scope is methodology + coordination, not implementation. Worktree-default discipline retains for non-cycle work.

Cycle git-discipline checklist (per Architect):

**Start-of-cycle** (fresh clone; clean slate by construction):
- Verify `git status --porcelain` empty
- Verify branch identity (`git branch --show-current` = configured branch)

**Mid-cycle**:
- Explicit-paths only on `git add` (no broad git-add)
- `git diff --cached --name-only` before commit; verify only own files staged
- `git show --stat HEAD` after commit; verify only own files committed

**End-of-cycle**:
- `git status --porcelain` empty
- Commits pushed to `origin/main`
- Session log + escalations file updated with cycle's deliverables + trust signal

Per CXO Framing 3, each cycle's session-log entry self-reports trust signal:

> *Cycle-N (HH:MM-HH:MM): Trust: green (cadence met; no escalations open) | Day's-Nth-cycle*

---

## Dry-run progression (PM does Phase 0; subsequent phases ratchet up)

### Phase 0 (PM's action, ~30 min today)

PM creates routine via `claude.ai/code/routines` interface:
- Name: `CIO Agent — Inbox Duty Cycle`
- Repo: `mediajunkie/piper-morgan-product`
- Branch: `main`
- Trigger: schedule, 1-hour interval (or PM-chosen specific times for testing)
- Connectors: GitHub only (no Slack/Linear/Drive)
- Initial prompt: see `dev/active/cio-v1-routine-prompts-2026-05-16.md` (Phase 1)

### Phase 1 — Does wake-up fire? (~5 min, PM hits "Run now")

Test that routine spawns a session and CIO agent loads cleanly. Routine prompt is intentionally narrow: list mailbox, read escalations, write a wake-test log file. No commit yet. PM verifies session spawned without permission errors.

### Phase 2 — Does schedule trigger? (~1 hour wait + 5 min verify)

Wait for first scheduled fire. Confirm routine appears in PM's routine list with green status. Open session, verify same steps as Phase 1 ran without prompting.

### Phase 3 — Can CIO safely commit? (~10 min, requires Phase 2 pass first)

Expand prompt to include commit + push of the status log file. Verify commit reaches `origin/main`. After Phase 3 passes: V1 is mechanically ready; expand prompt to actual cycle work.

### After Phase 3: V1 live

Update routine prompt to include real cycle work (inbox triage, dispositions, methodology updates, tracker advances). Start the 2-week proof-of-concept clock.

---

## Mushy middle (Horizon 3 — unchanged from v0.2)

Dynamic cadence (backoff/day-part/learned) — sub-hour interval would need custom infrastructure, NOT a V2 must-have unless 1-hour proves too coarse. Dashboard. Review-after channel. Routing-suggestions sidecar. Cross-agent extension. UI integration. Day-N digest refinement. Token-efficiency optimization. Role-health methodology dimensions for cycle-running agents.

---

## Constraints PM should know (per research agent)

1. **Fresh clone per run** — context doesn't persist; state lives in git (escalations file, session log, tracker). Good for V1: clean slate, reproducible.
2. **No mid-execution approval UI** — constraints baked into routine config upfront. Phase 0 setup is load-bearing; lock down what CIO can do before enabling recurring schedule.
3. **Daily run cap by plan** — 24 runs/day below typical limits; worth checking usage page.
4. **Observability strong** — every run is a separate session PM can open and read. Failed runs show red.
5. **No sub-hour interval** — Routines floor. Workaround would be custom infrastructure; not needed for V1.

---

## Cross-references

- v0.2 design doc: `dev/active/cio-v1-duty-cycle-design-v0.2-2026-05-16.md` (commit `feda5bc1`)
- Research-agent report: full text in CIO session log `dev/2026/05/16/2026-05-16-0713-cio-code-opus-log.md` (manual cycle M2, ~1:25 PM)
- Routine setup prompts (Phase 1 / 2 / 3): `dev/active/cio-v1-routine-prompts-2026-05-16.md`
- Dispatch-DinP V1 proposal: `mailboxes/cio/read/memo-dispatch-dinp-to-piper-cio-duty-cycle-design-2026-05-15.md`
- Cohort feedback memos (May 16): in `mailboxes/cio/read/`
- Escalations file (live): `dev/active/duty-cycle-escalations-cio.md`

---

*v0.3 — PM-ratified pre-implementation. CIO Code instance, 2026-05-16 ~1:45 PM PT.*
