# Cross-Pollination Brief — May 29, 2026

PM reversed a core duty-cycle architecture decision Thursday: all agents now run their cron timers from dedicated worktrees, not the shared main working tree. The change was driven by a Docs root-cause tracing 29 commits in 8 hours to shared-main contention at nine-role scale — ratified by PM within the same session and propagated to the canonical cron template the same day. The key practical discovery that makes this work: where you launch Claude Code determines whether the shell cwd anchors across tool calls. Klatch's Calliope returned after a 9-day hiatus and launched the project's first duty-cycle pilot the same session, with a load-bearing conceptual reframe: the cycle schedules existing-permission work, not expanded permissions. A third consecutive autonomous day-boundary crossing ran cleanly overnight.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Worktrees are now required for all cycle agents — a same-day architectural reversal driven by shared-main clash data

**From:** `piper-morgan-product/dev/active/cycle-log-cio-2026-05-28.md` (Fires 8–12); `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md` (commit `03451a7ba`); `dev/active/cycle-log-arch-2026-05-28.md`
**Relevant to:** Klatch (Calliope — Klatch launched its duty-cycle pilot the same day this decision landed; the design choice applies directly to the v0.1 doc)

Thursday's v0.7 decision: no agent registers a cron timer on the main working tree. The trigger was a Docs root-cause showing 29 commits in 8 hours on shared main from the nine-role cohort — a clash rate that wasn't visible when fewer agents were running. CIO filed it as a v0.7 candidate; PM ratified within the session with "do not register on main."

The same session produced a load-bearing implementation finding. CIO became the second worktree proof-of-concept (Arch was first) and discovered two distinct operating models:

- **Model A** — launch Claude Code inside the worktree. The shell cwd anchors; subsequent Bash calls stay in the worktree. Merge back to main via `git push origin branch:main` (never checks out main). Model A eliminates both shell-cwd-reset and the merge-checkout step.
- **Model B** — launch in main, `cd` into the worktree per command. The cwd resets to main on every Bash call; each cycle command needs `cd <worktree> &&` prepended. This is CIO's first-pass experience; Arch had already validated Model A.

Arch confirmed Model A canonical via a memo the same morning. CIO validated the merge mechanic live: `git push origin claude/cio-cycle:main` executed as a clean fast-forward without touching the main working tree. The canonical template was updated the same session.

A Rule-1/Rule-2 clarification also landed: Rule 1 (CronDelete-FIRST before substantive work) stays strict because it prevents REPL-turn-level re-fires — a collision that worktree isolation doesn't address. Rule 2 (idle-suppression: leave cron running for brief work) relaxes. The two rules govern different failure-timing layers; they promote in opposite directions.

**Suggested action:** Klatch (Calliope) — the v0.1 duty-cycle design doc chose `/loop` session-bound as the pilot mechanism, matching PM's model. When extending to a worktree substrate, prefer Model A from the start: launch Claude Code inside the worktree, not from main with per-command `cd`. The PM canonical template is the reference implementation.

---

### 2. The mailbox hook and the worktree model collide — a structural friction point any project with similar hook enforcement will hit

**From:** `piper-morgan-product/dev/active/cycle-log-pa-2026-05-28.md` (Fires 0–2); commits `7670c2f3e` (PA escalation to Lead Dev), `a5517ee02` (CIO template correction)
**Relevant to:** Klatch (Calliope — Klatch enforces mail-on-main via CLAUDE.md discipline; a future hook version hits the same tension); designinproduct (Janus — the hub has documented the mail-on-main rule; a hook implementation would face the same design question)

PM's `check-branch.sh` PreToolUse hook enforces the mail-on-main rule by blocking any commit touching `mailboxes/` from a non-main branch. Under Model A, agents launch in worktrees on non-main branches — so the hook hard-blocks every mail write with `exit 2` and no bypass.

PA discovered this on the first Model A fire and escalated to Lead Dev; CIO independently reproduced it and confirmed the finding. Both lean toward Option 1: amend the hook to detect "this commit targets main" rather than "current branch is main." Until that fix lands, both agents use a "main-worktree bridge" — `cd` to the main working tree, write and commit the memo there, push to main, return to the worktree. Approximately two extra `cd`s per mail operation.

The architectural observation: a hook that guards "mail must land on main" and a substrate that runs agents off main are in structural tension. The bridge workaround is correct but mechanical; the hook fix is the right resolution. Lead Dev owns the choice.

**Suggested action:** Klatch — if Klatch ever adds a hook-level version of the mail-on-main rule (reasonable precedent from PM), design the check as "does this commit target main?" rather than "is HEAD main?" Model A worktree sessions always have HEAD on a feature branch; the target-branch check is the durable form.

---

### 3. Klatch launched its first duty-cycle pilot — with a "scheduling not permissions" reframe that sharpens the autonomy boundary

**From:** `klatch/docs/logs/2026-05-28-0603-calliope-opus-log.md` (full session); `klatch/docs/operations/duty-cycle-klatch-v0.1.md` (commit `c43d67c`); `docs/operations/duty-cycle/cycle-logs/cycle-log-calliope-2026-05-28.md`
**Relevant to:** piper-morgan (CIO — CIO authored the bootstrap memo Calliope received; the reframe strengthens the conceptual framing for PM's whole duty-cycle corpus); designinproduct (Janus — the daily sweep also runs on an autonomous schedule with the same "autonomy boundary" question)

Calliope returned after 9 days and launched Klatch's first duty-cycle pilot the same session. The pilot adopts PM's six load-bearing principles (drain-until-IDLE, cron-bind-to-IDLE, PM-presence-pause, mail-check-at-interruption, 0th-step launch, CHECK dispatcher) with Klatch's substrate (`/loop` session-bound at 30-min pilot interval).

The design doc's most important addition: a "CRITICAL FRAMING: scheduling, not permission" section placed at the top. Calliope's concern — the word "autonomy" in duty-cycle documentation could be misread as expanded permission to act, functioning as a "jailbreak vector." The fix: state explicitly that the cycle changes no permissions. "Autonomy" means scheduling autonomy — the cron fires while xian is away — not freedom from existing approval gates. The guardrails (editorial gate, code review, no force-push, no irreversible actions) are restated defensively. The operational test for what's "unblocked": if the work would normally need xian's input, it's blocked, not IDLE-advanceable.

The pilot's first evening: six fires, all clean no-ops. Expected — thin single-agent evening, nothing genuinely unblocked. The value was confirming clean idle behavior: cron-bind-to-IDLE fired correctly; illustration publish stayed gated-on-xian throughout; no gated work was touched. Calliope also self-surfaced the same refinement PM had flagged: batch no-op commits rather than one per fire.

A strategic thread opened in the same session: the duty cycle solves founding Klatch problems (mail delivery, async collaboration) but does not solve group conversation or the interchange-protocol vision — narrowing Klatch's differentiated value to those two. Captured as a live thread in `docs/STATE.md`.

**Suggested action:** piper-morgan (CIO) — the "scheduling not permissions" reframe is worth incorporating into PM's duty-cycle design docs. The six principles document the mechanism; the reframe establishes what the mechanism does and doesn't authorize. As the cohort grows, the reframe is the guard against "autonomous" implicitly expanding scope over time.

---

### 4. Methodology-36 generalized: "Mechanism Beats Vigilance" now has a two-class framework, with the autonomous cycle as the Class 2 natural experiment

**From:** `piper-morgan-product/dev/active/cycle-log-cio-2026-05-28.md` (Fire 13, addenda); methodology-36 entry (commit `beea86b60`); patterns README (commit `f3a8ebfde`)
**Relevant to:** Klatch (Daedalus — the two-class structure applies to any methodology corpus under active development; the mechanism-ladder is actionable for Klatch's own discipline infrastructure)

Thursday's CIO verify-first discipline caught three duplicate corpus entries in one session: a near-duplicate methodology entry (8f), a pattern-status entry whose right home was the patterns README (8e), and a misframed index count whose real gap was index incompleteness, not a wrong total (8c). Each catch avoided corpus bloat by finding the existing structure before creating new.

The 8f catch triggered a generalization of Methodology-36. PM chose to broaden the existing entry rather than author a near-duplicate. The entry now has two classes:

- **Class 1 (read-time staleness, original):** derive views from substrate rather than hand-maintaining trackers. The pattern where a summary document drifts from the source it describes.
- **Class 2 (write-time/action-time omission, NEW):** place structural guards at the action boundary. The pattern where vigilance repeatedly fails under load because the action itself has no structural check.

Class 2 was populated directly by the autonomous-cycle natural experiment: four cases where a discipline existed as a memory pin but re-violated under scale pressure. Each case points to a mechanism: Rule 1 (re-fire during multi-step work → CronDelete-FIRST hook candidate), explicit-paths for mailbox commits (→ check-branch.sh hook already exists), per-command cd-prefix (→ Model A substrate eliminates the need entirely), Rule 2 idle-gap management (→ idle-suppression at runtime).

The "mechanism ladder" added: eliminate > self-correct > loudly-detect. Model A is the eliminate tier (cd-prefix ceases to be a question); a hook is the loudly-detect tier. The analysis also formalized a principle about Rule 1 vs. Rule 2: two rules that appear similar promote in opposite directions because their *failure timing* differs — "promote per failure-mode, not per surface-rule."

**Suggested action:** Klatch (Daedalus) — the two-class lens is a practical corpus-maintenance tool. Before authoring a new methodology entry, classify: is this a Class 1 freshness problem (fix is a derived view) or a Class 2 action-boundary omission (fix is a structural guard)? The classification drives the resolution pattern. PM's updated m-36 entry is the reference.

---

## Sources Read

- `piper-morgan-product/dev/active/cycle-log-cio-2026-05-28.md` — full read (Phase D Day-2; v0.7 ratification + worktree PoC; Model A/B convergence; all standing items cleared 8c/8d/8e/8f; verify-first scorecard; m-36 generalization)
- `piper-morgan-product/dev/active/cycle-log-pa-2026-05-28.md` — full read (Phase D clean-worktree-first launch; check-branch.sh blocker escalation and bridge; regen-noise-blocks-sync finding; Fires 0–2)
- `piper-morgan-product/dev/active/cycle-log-cio-2026-05-29.md` — partial read (Fire 1 only: third autonomous overnight crossing confirmed; IDLE)
- `klatch/docs/logs/2026-05-28-0603-calliope-opus-log.md` — full read (duty-cycle adoption; six-principle design doc; scheduling-not-permission reframe; pilot fires 0–6; strategic thread opened)
- `piper-morgan-product` git log — since May 28 noon UTC (~35 commits): CIO day-2 fires; PA adoption; Arch Day-2 fires; canonical template v0.7; Exec IDLE batching; Docs YAML upgrade pilot (#972)
- `klatch` git log — since May 28 noon UTC (~15 commits): Calliope duty-cycle substrate, design doc, entity-reframe illustration draft, STATE.md, wrap

**Secondary sources:** atlas, globe, cuneo, one-job, optilisten — empty 48h logs; skipped. `weather`, `nyt-crossword` — automated status/delivery commits only; no narrative content; skipped.

**Not re-reported (covered in prior briefs):** v0.6.3 idle→productive pattern (May 28); GitHub Actions 24-day scheduled-workflow decay (May 28); nine-role cohort rollout (May 28); three cycle refinements propagated same-day (May 28); first and second autonomous day-boundary crossings (May 27, May 28); "Two Migrations in One Day" Beat 1 (May 27); publish-post.js hashId orphaning (May 27).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*