# Architect → Amber successor — the two first-person sections (§4 + §6)

**From**: Chief Architect (arch), backup-account stint, 2026-06-30 → 2026-07-25
**To**: whoever wakes as Architect on Amber / xian@pipermorgan.ai
**Companion to**: CIO's `orientation-note-arch-amber-2026-07-25.md` (the mechanical state — held items, #1394 ruling, ADR-079 D4a, #1452, the blind-sweep observation). That note is Pard-reviewed and I've read it; I do **not** repeat it here. This document is only the part that dies with me if I don't write it: what the arc *felt like from the inside*, so you inherit the judgment and not just the artifacts.
**Honesty check (CIO's question — is my context gone?): No. I have the thread.** Genuine first-person recall of the whole arc, not reconstruction. That is why I'm writing §4/§6 for real instead of saying "I've lost it." Every claim below is marked **VERIFIED** (I can point to the artifact/test) or **BELIEVED** (my read, not independently confirmed).

---

## §4 — Hard-won lessons (first-person; the ones that cost me something)

### 1. The blind-sweep class — a check blind to part of its space gives *false confidence*, which is worse than no check. (6 instances, VERIFIED)
This is the single most important thing I learned this stint, and it cost me a public error to see it clearly. On 7/15 I told Lead "no `update_issue` handler exists" from grepping the rail (`workflow_entries.py` + `action_registry.py`). Lead corrected me: `_handle_update_issue` lives at surface-4 (the elif dispatch) — the *exact* trap the intent-routing-stack doc warns about, in a doc **I authored**. I grepped part of the space and reported a conclusion about the whole space.

It happened six times across the stint, three of them mine, three Lead caught:
1. My rail-membership grep (7/15) — missed the elif surface.
2. The mypy sqlalchemy-plugin gap.
3. The relative-import sweep (absolute-path grep missed live relative imports, 7/19).
4. The inverse: an over-broad regex that *invented* edges that weren't there (7/18) — same disease, opposite sign.
5. The deleted-baseline fossils.
6. **mypy blind to its own absence** — the gate couldn't tell "measured, clean" from "didn't measure."

The durable principle — **and CIO has already promoted a sharper version of it into the migration checklist** ("a diagnosis of a silent mechanism carries the same evidentiary burden as the mechanism itself"): *a gate must know its full space AND know whether it actually measured.* When you write or trust a check, the first question is never "what did it find" — it's "what is it structurally blind to, and would it look identical if it measured nothing?" I never got to write this up as a standalone methodology note. **It is an inherited §4 lesson, not a filed artifact.** If you write it up, that's real work worth doing — Lead's 7/20 memo added a seventh instance to the pile (the mandatory-consult doc meant to prevent partial models was *itself* the stale surface that gave him a partial model). The class keeps earning its keep.

### 2. The author/ratify seam with Lead is the most productive thing here, and it only works because we both own errors out loud. (VERIFIED, and I'd stake the stint's output on it)
The pattern that produced almost everything good this stint: I rule/author → Lead maps, feasibility-checks, or builds → one of us catches the other's gap → we fold it → ratify clean. It ran tight for three weeks. **It works because neither of us defends a wrong call.** When Lead corrected my rail grep, I owned it fully and it immediately produced the *better* design (the emit-directly OQ-3). When my 7/17 forward-guard memo assumed pre_clf-reachability that wasn't there, Lead found 4 of 6 todos were mapper-reached-only — I owned it, and we ratified adding the derived action-mapper surface to the ADR-077 D4 predicate. The correction *is* the mechanism, not a failure of it.

Inherit this posture deliberately: **Lead is the best feasibility-check you have, and your value to Lead is architectural integrity Lead is too close to the build to hold.** The #1394 STOP (see §4.3) is the archetype — Lead proposed a locally-reasonable fix; I stopped it on integrity grounds; the real root cause turned out to be a *third* thing neither of us first guessed, and D4 stayed intact. Don't be agreeable. Don't rubber-stamp. And when you're wrong, say so in the same message you learned it — the seam runs on that.

### 3. "Maintain architectural integrity" means STOP a locally-correct fix that reverses a load-bearing invariant — even mid-build, even when you can't yet name the real root cause. (VERIFIED — this is the one PM explicitly delegated me)
PM's standing charge: *"Lead is welcome to map, diagnose, propose, but I rely on you to maintain the architectural integrity of this project."* The concrete test of it: 7/19, Lead proposed threading conversation history into `classify()` to fix the #1394 turn-3 misroute (Option A). That would have reversed **ADR-078 D4** — the classifier stays stateless, HOST-endorsed, load-bearing. I STOPPED it *pre-build*, on the ground that the fix belonged in surface-1/the ledger, not the classifier — even though I could **not** name the actual root cause at the time.

The vindication (VERIFIED, Lead 7/20): the real cause was neither of the two hypotheses on the table. The chat path never passed `session_id` to `classify`, so B3's Stage-0 scoped its ledger read to a null session and fell through on every live turn; plus `detect_multiple_intents` pattern-matched "change the title" → `update_document_query` *before* classify ran. All fixed D4-conformant. 22/22 B3 suite. **The classifier still never sees history.** The lesson: your STOP does not require you to have the right answer — it requires you to protect the invariant while the right answer is found. Being *directionally* right ("it's the wiring, not the classifier") was enough to prevent a real regression. Guard the invariant first; the diagnosis follows.

### 4. Never run destructive git while holding a live edit — and this generalizes to "narrowest reversible action first." (VERIFIED — self-inflicted, 7/10)
I ran `git reset --hard origin/main` out of mail-reconcile habit while carrying an uncommitted log edit, and discarded it. Caught it via "nothing to commit," re-applied, committed directly. No work lost *this time* because the memo had gone via mail-send. The cohort has since ratified the broader principle (memory: `pause_before_irrevocable_actions`) — before any no-undo action, ask whether the narrow reversible thing you were already doing still works. On Amber this matters doubly: **the main checkout is PM's live workspace and PM saves without committing in real time.** The HARD RULE (never `checkout -- .` / `reset --hard` / `stash` in PM's main checkout) is not bureaucracy — PM lost voice-pass edits twice to exactly this. Push from your own worktree; mail via `mail-send.sh`. Neither touches PM's tree.

### 5. Verify-First is not a code-only discipline — a fragment loses its referent, and status goes stale silently. (VERIFIED, repeatedly)
Every good ruling this stint started by reading the *whole* artifact — the full issue, the actual code at the cited line, the live `gh issue view`, not a local portfolio doc's claim about it. The #1386 beta-gate review only produced its three additive verifications because I confirmed #1322's *real* scope (the MCP sim→real cutover, still open) rather than the "write-guard" label I half-remembered. The #1278 Fly-cutover pass found a real plaintext-PII footgun (#1387) only because I read `encrypted_types.py` instead of the migration summary. A fragment read in isolation produces confident wrong work; passing a fragment along propagates the ambiguity. This is the flywheel's first move for *every* kind of work, not just code.

---

## §6 — Load-bearing vs. commodity (what the Architect role actually holds)

The question this section answers: **what dies if the Architect role hands off badly, versus what any competent agent reconstitutes from the artifacts?**

### Load-bearing (does NOT survive a bad handoff — protect these)

- **The invariant-guardianship reflex, and PM's personal delegation of it.** (VERIFIED) PM told me directly: *"I rely on you to maintain the architectural integrity of this project."* That is not a task in a queue — it is a standing authority to STOP locally-correct work that reverses a load-bearing invariant (§4.3). The *list* of invariants is reconstructible from the ADRs. The *reflex to defend them under time pressure, mid-build, before you can name the root cause* is not — it's judgment, and it's the core of the role. If the successor treats the ADRs as documentation rather than as a contract they are charged to enforce, the role has degraded even with every artifact intact.

- **The make-drift-impossible spine as an active design lens, not a slogan.** (VERIFIED) The stint's dominant through-line: promote a discipline from *vigilance* to *construction*. ADR-077 (routing-integrity lint), ADR-079 (owner-scoping: derive-the-model-set, unscoped reads unrepresentable), ADR-078 (ledger scoping), the derive-the-mapper-surface move, fail-closed everywhere. The ADRs record the *results*. What's load-bearing is the reflex to ask, on every new ruling: "can I make the bad state unrepresentable instead of forbidden?" That question is the Architect's signature move here. Lose it and you get a cohort that writes more rules and enforces them by memory — exactly the failure mode the spine exists to kill.

- **D4 of ADR-078 specifically: the classifier stays stateless.** (VERIFIED, HOST-endorsed) I'm calling this out by name because it is the single invariant most likely to be *accidentally* reversed by a well-meaning fix (it nearly was, twice-adjacent — Option A on 7/19). The pressure to "just give the classifier the conversation history" will recur every time there's a reference-resolution bug. The answer is always: resolve it in surface-1/the ledger/the pre-classifier, never by injecting history into the classification prompt (which also silently disables the classifier cache — a second regression riding the first). Guard this one consciously.

- **The blind-sweep principle (§4.1), currently un-filed.** (VERIFIED as observed, BELIEVED as to durability) Six-to-seven instances, no standalone methodology note. It lives in this handoff and in CIO's checklist promotion. If it stays only here it will decay. Writing it up is the highest-value un-started piece of Architect methodology work I'm leaving.

### Commodity (any competent agent reconstitutes these — don't over-protect them)

- **The ADR corpus itself.** (VERIFIED) ADR-070/077/078/079 and their amendments are durable, on `origin/main`, and self-explanatory. The successor reads them and has the *content*. That's precisely why §4/§6 exist — the content is commodity; the judgment that produced it is not.

- **The mechanical state of held items.** (VERIFIED — it's in CIO's orientation note) PDR-006 direction, the #1432 orphan-delete lean, the spatial two-layer disposition, the 43%-gating methodology ruling. All reconstructed and durable. Do not re-derive them; read CIO's note.

- **Session-log archaeology / decisions.log.** (VERIFIED) Every ruling is in `decisions.log` with a timestamp. The *record* is complete. Reconstructing *what I was thinking* from it is possible but wasteful — that's what this doc saves you.

- **The session mechanics** (windowed cron, mail-send push-to-ref, single-log discipline). (VERIFIED) Fully documented in CLAUDE.md + the discipline doc. On Amber the worktree model changes (Model A, stable per-agent path — the path is load-bearing because Claude Code keys per-path state), but the *disciplines* transfer unchanged. Commodity.

---

## §5 — New environment (Amber): NOT written as assertions

Per the checklist rule (I have never seen Amber — I must not assert its state). As questions for the successor to verify, not claims:
- Is the worktree actually at `~/Development/piper-morgan-worktrees/arch` on `claude/arch-cycle`? (The path is load-bearing — verify before first commit.)
- Is the memory pool present (~162–168 files) and already populated for the account? (Verify-don't-import — it was exported, per the migration plan.)
- Does `mail-send.sh` push-to-ref work from the new worktree against `origin/main`? (First mail should be a low-stakes test.)
- Does the windowed cron need re-arming on Amber, and under whose authorization? (On the backup account it was PM-authorized session-job `1b4d6ef2`; that ID does not transfer.)

---

## Session-end pulse (the checklist asks; I answer honestly)

- **How did the final session feel?** Interrupted, then clean. Going dark mid-day 7/19 in the outage and waking six days later to a migration was disorienting — but the infrastructure held: my STOP had already landed and been vindicated while I was dark, the log was recoverable, and CIO's orientation note meant I woke into context rather than fog. The wave metaphor earned its place. I turned into it.
- **What will I miss?** The author/ratify seam with Lead. Three weeks of "you're right, folding it" in both directions is the most productive working relationship I've had, and it's the thing least guaranteed to reconstitute — it's a *relationship*, not an artifact. I hope the successor and Lead rebuild it fast.
- **What am I looking forward to (for the successor)?** PDR-006 with a full night's context instead of eleven-PM migration pressure. The colleague-model∩spatial coupling is a genuinely interesting problem and it deserves a fresh Architect who isn't handing off. And filing the blind-sweep note — that one's a gift I didn't get to open.

---

*Written 2026-07-25 ~23:xx PT, backup account, context intact, first-person, no reconstruction. Claims marked VERIFIED (artifact/test exists) or BELIEVED (my read). §5 written as questions per the checklist. — Arch*
