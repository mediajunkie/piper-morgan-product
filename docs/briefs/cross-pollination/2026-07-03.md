# Cross-Pollination Brief — July 3, 2026

PM closed out its security sprint: #1343 (anonymous billing exposure) shipped to alpha and was verified live; a dot release (v0.8.9.1) was cut to bring the production branch current. The day was process-heavy — hotfix cherry-picks, runbook gaps found and fixed, a self-correction on a test-collection error — but no new methodology worth carrying. One Job produced the single cross-pollination insight: Coral drafted a design for letting MCP agents deal work into the app without compromising its local-first storage model.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### An agent inbox as a mail slot, not shared custody — how a local-first app integrates with MCP without giving up device authority

**From:** One Job, Coral (`docs/MCP-DESIGN.md`, commit `50d12e0`, 2026-07-03)
**Relevant to:** Klatch (local-first SQLite store; same structural tension if agents ever push to it), any team building local-first apps that need to accept agent-generated work

One Job's 1.0 architecture keeps all tasks in device storage — there is no authoritative backend. Integrating with MCP-capable agents creates an immediate tension: an MCP server needs a network address agents can reach, but the phone's local store is the source of truth. Naive resolution — make the server authoritative — undoes the local-first bet.

Coral's design resolves it with an **inbox model**: the MCP server is a per-user mail slot, not a replica of the deck.

```
agent ──MCP──▶ One Job server (inbox, per-user)  ◀──pull── phone app
                                                       │
                                              status reports back
```

The concrete mechanism:
- MCP tools (`deal_task`, `get_task_status`, `list_dealt_tasks`) write to and read from a server-side inbox table — agents never touch the local store.
- The phone app pulls inbox cards into the local deck when the "Agent inbox" integration is enabled — they arrive at the bottom of the pile with a `source` badge. The app's local store remains the only authority over ordering, deferral, and completion.
- Status flows back opportunistically when online, via the existing `external_id`/`source` columns that were already built for adapter sources.
- Failure degrades gracefully: server down → agents queue or error; the human's deck keeps working untouched.

The clever reuse: inbox pull is just another source adapter feeding `createTask` — the same interface the planned Todoist adapter will use. Building the inbox builds the adapter seam.

**Suggested action (Klatch):** If Klatch ever wants to let external agents create conversations or inject context programmatically — for example, an agent that packages a PM standup into a Klatch channel — the inbox model resolves the structural tension. An agent-accessible staging server, with Klatch pulling via the same import-seam as any other source, keeps the local SQLite store authoritative. The risk to avoid: routing agent writes directly into `klatch.db` over the network collapses local-first into a shared-backend model without naming the trade-off.

---

## Sources Read

- **Piper Morgan** — git log (48h): Lead Dev session log `dev/2026/07/02/2026-07-02-0923-lead-code-log.md` (v0.8.9.1 dot release: cherry-pick hotfix branch off `origin/production`, runbook completeness gap fixed — VERSION file never listed; compliance gap — versioning.md listed but repeatedly skipped; `scripts/check-version-consistency.py` added; #1343 deployed to alpha, verified live; #1346 self-correction on test-collection error); Arch session log (Gap-B ratchet ratified; #1344 invite-code shape confirmed as staged Gap-A fix; usage-cap = Redis-backed global ASGI middleware); Docs session log (Jul-1 omnibus; #1328 weekly audit + #1341 quarterly sweep both closed; "The Airport Corrections" published). Activity-heavy day, confirmatory of the July 2 brief's security findings. No new transferable insights.
- **One Job** — git log (48h): `docs/MCP-DESIGN.md` (Coral's inbox model design memo, 84 lines, thinking-document status); `development/coral-logs/2026-07-03-coral-log.md`; FAB ship commit (`f684615` — persistent + button approved; pull-down-to-deal-blank-card recorded as post-1.0 power gesture). MCP design is the cross-pollination entry; FAB is UX execution, no insight.
- **Klatch** — quiet (last commit June 29). No new activity.
- **atlas, globe, cuneo, weather, optilisten, nyt-crossword** — atlas/globe/cuneo/optilisten: no commits in 48h window. weather: brief delivery commits only. nyt-crossword: automated status commits only. All skipped.

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*