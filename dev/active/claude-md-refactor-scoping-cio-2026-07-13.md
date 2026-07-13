# CLAUDE.md Refactor — Scoping (CIO architecture pass)

**Author**: CIO · **Date**: 2026-07-13 · **Status**: SCOPE for HOST + Docs review, before any text changes
**Origin**: HOST memo 2026-07-12 (PM-greenlit), diagnosis: accumulated "used to be X, now Y" transition prose causes LLM readers to activate both the old and new pattern — negation doesn't suppress the way it does for a human reader.

---

## 1. Confirming the diagnosis, with my own evidence

Read the full current `CLAUDE.md` (658 lines) fresh rather than work from memory. The pattern is real and recurring — I've personally *added* instances of it this week while fixing other things, which is worth naming plainly rather than only pointing at legacy content:

- Line 436: "the main-checkout bridge this line used to reference was retired by #1259 on 2026-06-19" — I wrote language exactly this shape when correcting a stale reference Monday, rather than just stating the current mechanism.
- The same "used to be X now Y" shape appears independently in at least 6 other places (full inventory below) — this isn't one bad paragraph, it's a habit the file's own editing pattern encourages: when something changes, the natural move is to *append* the correction next to the old text rather than *replace* it.

That last observation matters for the fix: **the fix principle needs to be an editing habit, not just a one-time cleanup**, or the file drifts back to this shape within weeks.

## 2. Proposed section-structure framework

Three altitudes, not two:

| Altitude | What lives here | Shape |
|---|---|---|
| **CLAUDE.md — identity/floor** | Behavioral rules an agent needs active in every session: STOP conditions, Core Principles, HARD RULEs, the mailbox/worktree/sign-off disciplines. Current truth only. WHY lines preserved when they carry load-bearing rationale (a past incident that explains why the rule isn't obvious) — but the WHY is 1-2 sentences, not a re-told incident. | Terse, imperative, no narrative. |
| **Linked docs — reference/history** | Incident post-mortems, full design rationale, "how we got here," anything a future agent would want *if* they're reconsidering a past decision but doesn't need to have loaded by default. | As long as needed; CLAUDE.md points to it with one line. |
| **Skills — procedures** | Multi-step how-tos that are invoked situationally, not identity-shaped (already mostly correctly placed in `.claude/skills/`). | Already the right shape; not much to move *into* here, but a few CLAUDE.md passages read more like a skill than a standing rule (flagged below). |

**The test for "does this WHY line survive the cut"**: would a future agent make a *worse decision* without it? Line 88's "Lead Dev determined empirically the ephemeral worktree suffices even for the dev-server" is load-bearing — without it, someone could re-propose the same exception without knowing it was already tested and rejected. Line 428's "3 leadership session logs were trapped on worktree branches" is NOT load-bearing in the same way — the *rule* (push to main routinely) stands on its own; the specific incident count doesn't change how anyone should act today. That's the boundary HOST asked me to protect, applied concretely.

## 3. Inventory — every "used to be X, now Y" passage found, with disposition

| Location | Current shape | Disposition |
|---|---|---|
| L25, L383 (session-log filename convention) | "Historical logs (pre-2026-06-29) used `-code-opus`..." | **Keep, trim.** Functional — agents need to recognize legacy filenames when they see them. Cut the "why it changed" clause, keep "if you see this format, here's what it means." |
| L88 (worktree model) | Full history of Model A deprecation + Lead Dev's empirical test + exception rubric, ~250 words | **Compress + link.** Current truth: "Canonical: ephemeral Option-B worktree per session; Model A (dedicated per-role worktrees) is not used, no current exceptions." Keep one sentence of WHY (the empirical-test finding, load-bearing per §2's test). Move the full exception-rubric mechanics + Lead Dev's specific reasoning to `cohort-plan-of-record-2026-06-12.html` (already the stated source of truth — CLAUDE.md should point harder at it, not duplicate it). |
| L149-158 (decisions.log) | "dormant Aug 2025 → Jun 2026; reinstated by HOST 2026-06-13" | **Trim.** One clause of scene-setting, low cost, but cuttable — the two-surfaces table is the actual rule and stands alone. |
| L177 (`#1124` dispatch migration) | "28→15 sites as of 2026-06-09" — a hardcoded snapshot | **Fix as a bug, not just a style cut.** This number is already stale (the migration continued past 6/9). Replace with a self-updating reference: "see `MAX_DISPATCH_SITES` in the enforcement test for the current count" — never re-embed a snapshot number here again. |
| L237 **and** L388 (log-maintenance-reminder hook) | The *same fact* — "currently clock-based, being realigned to event-based, Lead Dev coordinating" — stated independently in two different sections | **Real duplication bug, not just staleness.** Fix in one place: verify current hook status directly (read the hook's actual code) rather than trust either copy, state it once, delete the other copy or make it a cross-reference. |
| L244-253 ("Log in one place" background) | Full displacement-trap narrative + v1.5 dual-surface history before the current rule | **Compress hard.** The comparison table (session log vs. cycle log) is a good CURRENT-STATE clarifying device — keep it. Cut the "Background" paragraph's origin story to one sentence; the rule doesn't need the whole story to be followed correctly today. |
| L428 (sign-off discipline origin) | "Established 2026-04-28 after recurring incidents... (Apr 27: 3 leadership session logs were trapped...)" | **Compress.** Rule stands alone; incident count isn't load-bearing (see §2 test). One clause, not a paragraph. |
| L438 (sync-pm-local.sh paragraph) | Dense: current behavior + "Known limitation #1" + "Known limitation #2 (found/resolved with dates)" — a full debugging history inline | **Split.** Keep: what the script does today, and "if it doesn't work as expected, flag it — don't route around it." Move: the dated Known-limitation archaeology to the script's own header comment (verify it's not already there — likely is, scripts in this repo tend to carry their own history) or a linked doc. CLAUDE.md shouldn't be the debugging-history archive for a script that has its own file. |
| L501-573 (4 separate gotcha sections: SSH-443, GH Projects v2 full-replace, GH auto-close negation, Keychain `_api_key`) | ~75 lines total of detailed, dated incident post-mortems with full "what happened" narrative | **Extract to a linked doc.** Propose `docs/internal/operations/github-and-tooling-gotchas.md` (or fold into an existing gotchas doc if one exists — Docs to check). CLAUDE.md keeps one tight paragraph per gotcha: the rule + the one-line consequence + a pointer. This is the single biggest length win in the file — these 4 sections are pure "gotcha reference," not identity-level behavioral floor, even though the *rules themselves* are absolutely worth keeping prominent. |
| L637-658 (Git Worktrees / Model-A setup instructions) | Full `git worktree add` setup walkthrough for a model that's explicitly deprecated with no current exceptions (per L88's own admission: "retained for the exception case + history") | **The clearest case in the file.** ~20 lines of active how-to instructions for a mechanism nobody currently uses. Move the whole section to a linked doc (or fold into `cohort-plan-of-record-2026-06-12.html` alongside L88's content — they're describing the same retired model). CLAUDE.md keeps one line: "Model A worktree setup, if a genuine exception ever arises — see [doc]." |
| L617 (mailbox workflow, "old bridge dance") | "The old bridge dance (stash → checkout main → git add mailboxes/ → push → switch back) is retired" — describes the dead mechanism's steps before saying it's dead | **Cut the mechanism description entirely.** Nobody needs to know the old steps to follow the current ones. If someone's debugging why an *ancient* memo exists somewhere, git log has it. |

**Not flagged for change** — good existing examples of the right shape, worth citing to HOST/Docs as the pattern to match rather than reinvent:
- L43 (self-attribution-drift): states the current rule + a one-line pointer to the full incident doc, doesn't retell the incident. This is the target shape.
- L579-591 (the two HARD RULE boxes): tight, WHY preserved in 1-2 sentences, pointer to canonical doc for detail. Also the target shape.
- L577 itself ("Branch/Worktree/Mailbox Discipline... 60-second summary... read that doc for the full rule set") — this section already explicitly names itself as a compressed pointer to a canonical doc. More of the file should work this way.

## 4. Proposed pass structure

1. **CIO (this doc)** — architecture decisions + inventory. Done, pending HOST/Docs read.
2. **Docs** — executes the actual text changes per the inventory above: extracts the 4 gotcha sections + the Git-Worktrees/Model-A section to linked docs, compresses the flagged passages to current-truth-only, fixes the L237/L388 duplication (verify actual hook status first, don't just pick one copy), fixes the stale L177 snapshot number. Tracks what moved where for cross-references (anything else in the repo linking to a since-moved CLAUDE.md section).
3. **HOST** — final behavioral-norms completeness review: confirm every WHY line that survived the cut is still there, confirm no safety/trust rule lost its rationale, flag anything CIO's inventory got wrong (cut something load-bearing, or kept something that should've gone).
4. **PM** — ratifies.

**Not in scope for this pass** (flagging so it doesn't get folded in as scope creep): the Progressive Loading table (L277-297) and the Subagents/Multi-Agent-Coordination sections are candidates for a *second*, separate pass (possible skill/linked-doc migration) but aren't "used to be X now Y" bloat — different problem, don't conflate.

---

*Companion to the mail cover note sent to HOST + Docs (cc PM), 2026-07-13.*
