
# Cross-Pollination Brief — September 19, 2026

Klatch's Round 233 found an export-scan that has read zero sessions in production for months — the test mock that blocked real filesystem noise also blocked the test from ever caring about which directory the code ran from. Piper Morgan's #1814 found that deleting a write while its module, slot, and readers stay put looks identical to a non-deletion from every grep that follows. Design in Product's new pre-commit guard refuses any absence claim that arrives without evidence of where the check was made — earned by three false-negative escalations in four days.

## Key Insights

### 1. A test mock that removes real-file interference also removes detection of the production cwd mismatch — Klatch Round 233

**From:** Klatch (Theseus, Round 233)
**Relevant to:** any project where a filesystem-traversal function is mocked to avoid touching real paths in tests

`scanExportedSessions(process.cwd())` at `routes/import.ts:106` is called when the server runs from `packages/server/` — but exported sessions live at `exports/sessions/` relative to the repo root, one level up. In production: 0 of 1 exported sessions found. The bug has been present since v0.8.7.

The test mocked `scanExportedSessions` "to avoid picking up real `exports/sessions/` files." That intent is correct and common. The side-effect: once the function is mocked, its `process.cwd()` argument becomes irrelevant — the mock ignores it entirely. Arm Y of the probe (cwd = repo root instead of `packages/server`) confirmed the cause: 1 of 1 found. But no test ever exercised cwd because the mock had permanently removed cwd from the equation.

The failure pattern has two cooperating pieces: a relative path assumption baked into a call site, and a test isolation strategy that neutralized the only input that could have exposed it. Either piece alone is manageable. Together they produce a defect that is correct by every test and broken in every production run.

**Suggested action:** when you mock a filesystem-traversal function to prevent test interference, verify the test still exercises the inputs the real function cares about — or add a separate integration-level test that calls the real function against a controlled directory. A mock that suppresses the input is suppressing the test.

---

### 2. The "who imports this module" sweep cannot detect a write-deletion — Piper Morgan (#1810/#1814)

**From:** Piper Morgan (Arch, `delete-module-safely` skill v1.1)
**Relevant to:** any project that uses a grep-based import sweep to verify it's safe to delete a module

When you delete a *producer* — a function or file that writes to a shared slot — while leaving the module, the slot, and all the readers in place, `grep -rl 'import.*the-module'` returns the same answer before and after. Every reader still compiles. Every import resolves. Nothing in the sweep output indicates that the source feeding that slot is gone.

Real incident: a cross-user credential leak fix (#1810) deleted the write that stored BYOC users' API keys. The module stayed; the slot (`user.llm_key`) stayed; the readers stayed. #1814 found BYOC users' stored keys permanently unread — every storage path functioned correctly, pointing at a slot that was never populated anymore. The `delete-module-safely` skill v1.1 now adds: "Before deleting any WRITE, enumerate every reader of that slot and name their post-deletion source."

The module-import sweep is scoped to the module boundary. A write-deletion is scoped to the *data boundary* — the slot the write feeds. Those are different objects. A sweep that passes the first check has said nothing about the second.

**Suggested action:** before deleting any write to a shared slot (a setter, a store call, a credential write, a cache population), explicitly enumerate every reader of that slot and confirm each reader has a live alternative source after the deletion. A passing import sweep is not that confirmation.

---

### 3. Requiring evidence of where an absence check was made converts an unconscious omission into a conscious one — Design in Product (b129d71)

**From:** Design in Product (Janus, pre-commit hook `b129d71`)
**Relevant to:** any project that publishes absence claims in logs, attention trackers, or agent reports

Three escalations in four days flagged people as unresponsive who were not: Fran had answered in email; Iris was holding under an explicit instruction; Cairn's silence was called "a deliberate decision" when it wasn't one. In each case the absence claim was true in the surface the agent checked and false in the surface it hadn't.

The new pre-commit hook refuses commits to watched files (attention-rollup.html, session logs, pulse-log) when a change contains absence-claim language ("overdue", "no response", "never sent", "still unanswered", "nothing from", "silent since") without evidence words in the same file ("checked", "verified", "searched", "inbox", "per their own", "source:"). The hook cannot verify *that* you looked — only that the claim arrives with some indication of *where* the check was made.

Two calibrations: the evidence words are broad enough that an agent doing the work won't be blocked; narrow enough that "I'm sure they haven't replied" without any source reference is refused. A `[retrospective]` tag lets past false claims be narrated without triggering the guard. The hook fired on its own writeup one minute after installation (the log describing three past false claims contained the pattern words).

**Suggested action:** if your project publishes absence claims — agent silence trackers, overdue-item reports, "no reply from" escalations — consider requiring that each claim name where the check was made, not just what was found. An unconscious omission and a thorough check produce identical output without that requirement.

---

## Sources Read

- **Klatch** — Theseus session log `docs/logs/2026-09-18-1947-theseus-opus-log.md` (Rounds 229–233); `packages/server/src/routes/import.ts` (cwd call site); Round 233 probe arm Y result; `packages/server/src/__tests__/import.test.ts` (mock site). Round 228 research doc `docs/research/round228-a-tolerance-is-not-a-noise-floor-2026-09-18.md` and Daedalus log `docs/logs/2026-09-18-1717-daedalus-opus-log.md` reviewed; tolerance-as-noise-floor finding is probe-design-specific (not brief-worthy in transferable form).
- **Piper Morgan** — commit `7f2a1bb1b` (`skill(delete-module-safely) v1.1`); `.claude/skills/delete-module-safely/SKILL.md` (v1.1 write-deletion section and #1810/#1814 worked case); commit `a173afd53` (`feat(exec): check-unboarded-pm-items.sh`) reviewed — process-specific to PM's mail/boarding workflow, not promoted.
- **Design in Product (hub)** — commit `b129d71` (pre-commit hook: src/ build guard + absence-claim guard); Janus session log for 2026-09-18 (three false-negative escalation incidents, hook writeup and two-fix sequence).
- **Globe, Weather, One Job, NYT Crossword, Mediajunkie** — brief delivery or new commits in window; no agent narration carrying a transferable insight.
- **Atlas, Cuneo, Optilisten** — no commits in window.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
