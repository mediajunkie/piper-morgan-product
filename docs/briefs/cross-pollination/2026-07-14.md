# Cross-Pollination Brief — July 14, 2026

The July 13 brief covered the diagnosis: deprecated prose in agent behavioral documents activates both old and new patterns in LLM readers — the fix is deletion, not compression. Today's finding from Piper Morgan's CIO addresses the structural question the diagnosis leaves open: what goes *where* in a behavioral document, and how do you keep the right content at the right altitude without every edit session drifting back? The answer is a three-altitude model with a concrete survival test for rationale lines. Klatch and all secondary sources quiet this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A three-altitude model for agent behavioral documents — and a concrete test for when rationale belongs

**From:** Piper Morgan, CIO (scoping note `dev/active/claude-md-refactor-scoping-cio-2026-07-13.md`, July 13 — produced after HOST's diagnosis in yesterday's brief was greenlit by PM)

**Relevant to:** Any project that maintains agent behavioral documents over time — CLAUDE.md files, agent briefings, system prompts that accumulate editing history. Directly applicable to Klatch (COORDINATION.md, CLAUDE.md, agent layer files); DinP (CLAUDE.md, layer4/layer5 per-agent files); One Job (CLAUDE.md).

The July 13 brief identified the problem (deprecated prose activates both patterns) and the immediate fix (delete historical narrative; the fix is deletion not compression). What it didn't address: what's the structural model for *where content belongs* in the first place — so future editing sessions don't reproduce the same pattern?

**The three-altitude framework:**

| Altitude | What lives here | Shape |
|---|---|---|
| Identity/floor (CLAUDE.md) | Behavioral rules that must be active in every session: STOP conditions, HARD RULEs, standing disciplines. Current truth only. WHY lines preserved *only* if they carry load-bearing rationale. | Terse, imperative, no narrative |
| Reference/history (linked docs) | Incident post-mortems, full design rationale, "how we got here," anything a future agent would want *if* reconsidering a past decision — but doesn't need loaded by default. CLAUDE.md points here with one line. | As long as needed |
| Procedures (skills) | Multi-step how-tos invoked situationally, not standing behavioral rules. Already mostly in `.claude/skills/`; CLAUDE.md shouldn't duplicate them. | Already mostly correct |

The immediate value isn't cleanup — it's that the model makes the right choice during *future* edits the easy choice. When fixing a stale reference or documenting a norm change, the natural move is to append "the old approach was X" next to the new text rather than replace it. The CIO names this explicitly as a habit they wrote into a commit this same week. Knowing that historical narrative belongs at the reference/history altitude — in a linked doc, not in CLAUDE.md — makes the correct choice structural rather than requiring discipline to override instinct every time.

**The WHY-line survival test:**

The hardest call in any behavioral document edit is which rationale lines stay. Too permissive and you're back to narrative bloat; too strict and you strip load-bearing context that prevents future mis-decisions.

The test: *"Would a future agent make a worse decision without this?"*

Applied concretely from PM's CLAUDE.md inventory:

- "Lead Dev determined empirically the ephemeral worktree suffices even for the dev-server" **survives** — without it, someone could propose the same exception not knowing it was already tested and rejected. The rationale changes what a future agent would do.
- "3 leadership session logs were trapped on worktree branches on April 27" does **not** survive — the rule (push to main routinely) stands on its own. The incident count doesn't change how anyone acts today. It belongs in git log, which already has it.

A second concrete application: two places in PM's CLAUDE.md state the same fact about the log-maintenance-reminder hook being "currently clock-based, being realigned to event-based." One is accurate redundancy; one is real duplication — and the right fix is to verify the hook's actual current state from its source file rather than trust either copy, then state it once. This passes the WHY-line test (the hook's current state is actionable; agents need it); the duplication itself doesn't.

**Suggested action:** Apply the three-altitude model as a mental checklist when editing your CLAUDE.md or equivalent behavioral document. For each passage: (1) Is this current behavioral truth an agent needs loaded by default? → identity/floor, stays. (2) Is this rationale for a current rule that a future agent needs to make a better decision? → stays if it passes the WHY-line test ("worse decision without it?"), but trim to the load-bearing sentence(s). (3) Is this "how we got here" / incident narrative / historical context? → move to a linked doc; CLAUDE.md keeps one pointer. (4) Is this a multi-step procedural how-to? → move to a skill. The three-altitude model and the WHY-line test are jointly the replacement for the habit of appending corrections next to old text.

## Sources Read

- **Klatch** — git log (48h): brief delivery commits and automated external intel sweep (`docs/intel/2026-07-13-sweep.md`). External intel covers Anthropic Managed Agents memory API stabilization and Fable 5/Mythos 5 backstory — external news, not transferable methodology from Klatch's own work. No new Klatch-internal findings this window.
- **Piper Morgan** — git log (48h, full): CIO CLAUDE.md refactor scoping note (post-sweep commit, Jul 13 ~10:51 AM PT); ADR-078 D1a amendment (fold HOST trust-lens, session isolation keyed by session_id+user_id rather than session alone — incremental refinement of yesterday's ADR-078 finding); Docs 4-phase `docs/` tree audit plan (operational cleanup proposal, awaiting PM gate); Lead Dev duty-cycle stall (multiple watchdog alerts, parked pending Lead). One transferable finding above; rest operational.
- **weather, one-job** — brief delivery commits only; skipped.
- **nyt-crossword** — automated status commits; skipped.
- **atlas, globe, cuneo, optilisten, mediajunkie** — no commits in 48h window; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
