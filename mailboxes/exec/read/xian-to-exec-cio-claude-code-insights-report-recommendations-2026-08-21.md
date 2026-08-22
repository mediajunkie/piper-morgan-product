---
from: xian (ceo) — drafted on PM's request by general-purpose code agent
to: exec, cio
cc: janus, themis (designinproduct repo, docs/mail/), pard (mediajunkie repo, docs/mail/)
subject: "Claude Code /insights report (Jun 22–Aug 18) — recommendations to evaluate and adopt across projects"
date: 2026-08-21 19:00 PT
---

**Report location**: this repo is public, and the report narrates session content from other projects, so the full HTML is NOT committed here. It is committed in the two private sibling repos (`designinproduct/docs/mail/claude-code-insights-report-2026-08-21.html`, `mediajunkie/docs/mail/claude-code-insights-report-2026-08-21.html`) and lives locally at `/Users/xian/.claude/usage-data/report-2026-08-21-184622.html`. Everything actionable is summarized below.

## Why you're getting this

xian ran Claude Code's `/insights` report on 2026-08-21. It analyzed 45 of 79 sessions (2026-06-22 → 2026-08-18, 471 commits) spanning Piper Morgan, designinproduct, mediajunkie, and several smaller projects. The friction it surfaces is cross-project — the same three failure classes show up regardless of which repo the agent was in. xian's ask: **each of you evaluate these recommendations for your own project and adopt what fits**, rather than having each repo rediscover the same lessons.

Reply with what you adopted, what you rejected and why, and anything you think the report got wrong. Silence is not ratification.

## What the report says is working

- **Verification as a first-class request.** Read-only checks (SHAs, file content, origin state) before anything moves; full commit→push→verify-against-origin loop before "done." This caught real problems: a stale HEAD, a wrong file path, a false "second confirmation," origin advancing mid-check.
- **Duty-cycle agents with paper trails** — roles, handoff protocols, logs. One Lead Dev cycle drove a backlog from 634 to 94 items while holding CI green.
- **Corrections encoded as hooks and durable rules** rather than repeated in chat. Dissatisfaction rate: 5 signals out of ~150.

## The three friction clusters (cross-project)

1. **Unverified assertions from memory** — an invented "49 imports" figure; a file-history diagnosis stated backwards, which spawned a background task on a false premise; an outdated skill spec quoted as current.
2. **Git contention and stale worktrees** — push rejections, unplanned rebases, contradictory tracker entries; one retry reused a stale tree object and clobbered other agents' commits on main; several sessions started from a stale checkout (one debugged a browser preview of the wrong site).
3. **Convention hooks firing on verbatim quoted output** — stop hooks flagged bare issue references and cost framing inside `git log` excerpts that xian had explicitly asked to see verbatim. Rework that isn't really a violation.

## Recommendations to evaluate

### A. CLAUDE.md additions (the report's suggested text, lightly condensed)

1. **Verify Before Asserting** (top-level, above workflow sections): never state a fact about repo history, file contents, counts, or config from memory. Run the command and quote the output before making the claim. If the check wasn't run, say "unverified." *Piper note: CLAUDE.md already has "Never guess at facts you can look up" and m-43/m-44; the delta is the mechanical "tool call in the same turn, quote the output" form and the explicit "unverified" label.*
2. **Reference & framing conventions with a quoted-output carve-out**: full issue URLs, no cost framing — **and state explicitly how those rules apply to verbatim pastes** (the report suggests: quote the text, restate references with URLs). The point is to stop the hook-vs-verbatim argument from recurring.
3. **Git hygiene before any edit**: `pwd && git rev-parse --show-toplevel`; `git fetch origin && git status -sb`; after push, confirm `HEAD == origin/main` and report the SHA. *Piper already has most of this in Sign-Off Discipline; the gap is the session-START freshness check.*
4. **Concurrency**: before editing a shared file (calendar CSV, trackers, activity logs), re-read from a fresh fetch; rebase on rejection, never force-push; assume an edit you "remember" may already be committed by another session — `git log -- <file>` first.
5. **Agent memos go in the RECIPIENT's repo.** Confirm the target path before writing. (A memo to Janus was once written into the wrong repo's `docs/mail`.)

### B. Tooling

- **`/verify` skill**: one scripted read-only battery (toplevel, fetch, `rev-parse HEAD origin/main`, `status -sb`, `log -5`) reported verbatim with PASS/FAIL on `HEAD == origin/main`. Replaces the 4–9 sequential commands xian types each session.
- **PreToolUse freshness gate** on Edit/Write: block when the worktree is behind `origin/main`, with an override flag. Prevents the stale-worktree class entirely instead of catching it at Stop.
- **Headless duty-cycle ticks with a heartbeat log** (`claude -p … | tee -a logs/duty-$(date +%F).log && date -u >> logs/heartbeat`). The report notes ~22 hours lost to a silent cron outage; a heartbeat makes a dead cron visible immediately.

### C. Working patterns

- Batch read-only git batteries into one script with `=== SECTION ===` headers, raw output first, interpretation after.
- For multi-file or multi-location changes, require a written plan naming every exact path **before** editing (hardcoded repo lists were found in five places only after repeated discovery).
- Use a subagent for "find every place X is defined" before editing; return a table, edit nothing.

### D. Longer horizon (not asks yet — for your roadmap thinking)

- A verification harness where any claim about git state / file contents / spec version must carry inline evidence, plus the freshness gate above.
- **Lane-based write ownership**: a machine-readable `lanes.yaml` per agent (owned files, CSV columns, directories, read-only zones) enforced by a PreToolUse hook, with pushes serialized through a queue and "never reuse a tree object on retry — fail loudly." The report's framing: this is what lets the fleet go from 6 agents to 20 without reconciliation time growing. **Concrete first step it suggests: write down, per agent, exactly which files and fields you own.**
- A closed-loop CI repair agent (wake on red → reproduce → bisect → failing test first → fix → 3 consecutive green runs → PR), one subagent per failure class.

## Asks, by recipient

- **Exec (Piper)**: own the cross-repo rollout — collect each lane's adopt/reject response and surface the consolidated answer to xian. Decide whether A.1–A.5 are CIO's to draft or yours.
- **CIO (Piper)**: assess A.1–A.5 against the existing CLAUDE.md (which already covers much of this, at length — the question is whether the condensed mechanical form should sit *above* the prose), and whether B's `/verify` skill and freshness gate should be cohort-standard. D's lane-ownership map is squarely methodology — your call whether it gets an issue now.
- **Janus, Themis (designinproduct)**: same evaluation for designinproduct's CLAUDE.md and duty cycles. The "memo in the wrong repo" item and the cron-outage heartbeat item both originated in your lane.
- **Pard (mediajunkie)**: infrastructure angle — the freshness gate, heartbeat log, and lane/commit-queue design are host-level concerns on Amber; tell us what's feasible to standardize across seats.
