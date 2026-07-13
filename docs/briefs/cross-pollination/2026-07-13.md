
# Cross-Pollination Brief — July 13, 2026

Two findings from Piper Morgan. First: transition prose in agent behavioral documents ("the old approach is retired — here's what replaced it") doesn't suppress the old pattern for LLM readers — both activate simultaneously. The fix is to state only current truth and move historical narrative to git log. Second: a pair of cross-turn continuity failures revealed a structural principle: keep the LLM routing classifier stateless, and resolve cross-turn referents explicitly at a dedicated pre-classifier step rather than injecting conversation history into the routing prompt. Klatch and all secondary sources quiet this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. "X is deprecated, use Y" in a system prompt doesn't suppress X — it activates both

**From:** Piper Morgan, HOST role (memo `mailboxes/cio/inbox/memo-host-to-cio-cc-docs-pm-claudemd-refactor-proposal-2026-07-12.md`, July 12)

**Relevant to:** Any project maintaining agent behavioral documents — system prompts, CLAUDE.md files, briefings — that accumulate historical migration prose over time. Klatch (CLAUDE.md and COORDINATION.md); DinP (CLAUDE.md and agent layer files); One Job.

Piper Morgan's CLAUDE.md has accumulated substantial transition prose: "the old bridge pattern is retired — here's the new approach" language added each time a norm changed. HOST's diagnosis, ratified by PM: LLM readers don't bracket deprecated content the way humans do. Where a human reader would read "X is retired" and mentally file X away, an LLM activates both X and its replacement as potentially live heuristics. PM's framing: "stale info propagates loosely because an agent reads 'acidity rule — something about oranges, also apples' and treats both as live, even when the text explicitly deprecated apples."

**The cut to make:** historical narrative (how the project got here, why a given norm replaced an older one) vs. behavioral rationale (why a *current* rule exists). The first category belongs in git log — it's already durable there. Only the second belongs in the live document. The fix is deletion, not compression: removing "we used to do X" passages rather than shortening them. A sentence that explains *why the current rule exists* stays; a sentence that explains *what the previous rule was* goes.

**Suggested action:** Scan your CLAUDE.md or agent briefing files for "used to be", "deprecated", "the old", "replaced by", "previously", "until YYYY-MM-DD" language. For each, determine whether the sentence is behavioral rationale (why the current rule is the rule) or historical narrative (how the project arrived here). Delete historical narrative. If you're unsure whether a passage survives without context, try reading just the surviving text — if it still clearly states what to do and why, the cut was safe.

---

### 2. Keep the LLM routing classifier stateless — resolve cross-turn referents before it sees the message

**From:** Piper Morgan, Arch (ADR-078 PROPOSED, `docs/internal/architecture/current/adrs/adr-078-session-activity-ledger-and-pre-classifier-reference-resolution.md`, July 12; gated pending Lead's feasibility read)

**Relevant to:** Any project using an LLM as an intent router or classifier in a multi-turn conversational system. Klatch (message routing within entity conversations); any future Piper-like system built on Klatch's platform.

Two cross-turn failures landed in PM's production system: a follow-up message ("Actually, change the title…") misrouted to the Notion handler instead of recognizing it referred to an issue just created; and "what did we create this session?" returned nothing, because the floor had no session-scoped artifact record. The natural response — inject conversation history into the classifier prompt — was ruled out (Decision D4). The reason matters:

**The classifier (surface 2) must stay stateless.** It's the layer PM has worked hardest to keep clean and deterministic. Making it conversation-stateful changes *all* routing behavior, risks over-anchoring (a genuine topic switch misread as a continuation), and forces revalidation of the entire routing golden corpus. The routing LLM's integrity depends on it not carrying conversational context.

**The architectural resolution:** both failures stem from ONE missing primitive — a session-activity ledger that records which turn created which artifact. The ledger is not a new artifact store; it's an association layer linking existing turn records to existing artifact records. Once that primitive exists:
- B3 (misrouted follow-up) resolves via a *pre-classifier* reference-resolution step that reads the ledger and rewrites "change the title" to "change the title of issue #107" *before* the message reaches the classifier — the classifier then sees an explicit referent and routes correctly.
- B4 ("what did we create?") resolves via a session-activity reader that queries the ledger rather than falling back to a live-repo query or the ephemeral 10-turn floor window.

**The transferable principle:** when you have a multi-turn conversational system and an LLM routing layer that must stay stateless for integrity reasons, cross-turn context belongs at a dedicated pre-classifier step, not inside the routing LLM. The pre-classifier step is explicit, bounded, testable, and doesn't contaminate routing behavior for messages that aren't cross-turn references.

**Suggested action:** If your routing classifier currently has no conversation history and you're feeling pressure to add it, ADR-078's D4 constraint is the counter-argument: add a pre-classifier reference-resolution step instead. Even a simple pronoun/definite-article detector that rewrites "it", "that", "the issue" against a recent-turn context record keeps the classifier clean while resolving the most common continuation failures.

## Sources Read

- **Klatch** — git log (48h): external intel sweep (`docs/intel/2026-07-13-sweep.md`, automated) + brief delivery commits. No new Klatch-internal methodology this window.
- **Piper Morgan** — git log (48h, full): ADR-078 PROPOSED (Arch, Jul 12 — pre-classifier reference resolution + session-activity ledger); HOST CLAUDE.md refactor proposal (memo to CIO/Docs/PM); Fly.io Chroma flycast bridge (`#1399` — IPv4-only container image unreachable on Fly's IPv6-only 6PN, fixed via `[[services]]` block); sprint-recovery complete (99/99 Production milestone, Jul 12); Docs duty-cycle retired + Belt-4 extended as replacement; CXO/PPM/CIO/Arch/HOST operational day-close. Two transferable findings above; rest operational.
- **weather, one-job** — brief delivery commits only; skipped.
- **atlas, globe, cuneo, optilisten, mediajunkie** — no commits in 48h window; skipped.
- **nyt-crossword** — automated status commits; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
