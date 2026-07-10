
# Cross-Pollination Brief — July 10, 2026

Two findings from Piper Morgan today. First: when injecting contextual data into an LLM prompt, wrong-confident context is worse than absent context — a fix to the time-of-day flourish encodes this as a durable principle. Second: a stall-detection watchdog that only covers 4 of 11 roles is structurally invisible to the other 7 — "we have a watchdog" and "the watchdog watches everything that matters" are different claims that fail silently apart. Klatch applied the July 9 `.gitignore` suggestion; no new methodology of its own this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Wrong-confident context is worse than absent context — omit rather than inject the server clock as user time

**From:** Piper Morgan, Lead Dev (fix `c4995f5`, `#1381`, July 9)

**Relevant to:** Any project that injects ephemeral context — current time, location, device state — into LLM prompts or system prompts. Klatch (channel/entity system prompts); One Job (LLM context in future integration layer); DinP (Janus session context).

Piper's floor had a helper that injected a `current_time` flourish into the conversational context — letting Piper say things like "It's 4:30 AM — you're either an early riser or deep in a late night." On a multi-user deployment, that helper read the server's configured timezone (UTC on the droplet), so every user got the server's clock, not their own. Piper was confidently narrating predawn hours to users sitting at their desks at 9:32 PM Pacific.

The fix is not just the bug fix — it's the rule it encodes:

> **Precedence for user-contextual data: user's own data → per-tenant config → omit. Never fall back to server state and present it as user state.**

The floor's renderer already skips absent keys gracefully. An absent `current_time` = no flourish. A server-clock `current_time` = confidently wrong flourish. The absent path is always preferable to the confident-but-wrong path.

This generalizes beyond time: any datum you're injecting into a prompt as "the user's X" should come from the user's own personalization context. If you don't have it for this user, omit the feature rather than substitute a server-side proxy. The subtle failure mode is that the wrong-confident version often looks fine during single-user development (developer's machine timezone matches) and only breaks on multi-user deployment.

**Suggested action:** Audit any LLM system-prompt or context-injection that includes a user-contextual datum (current time, location, timezone, preferences). For each: verify the data path leads to user-specific data, not server state. If the path can fall to server state, add a skip/omit branch rather than a server-state fallback.

---

### 2. A watchdog's coverage list is itself a monitoring gap — audit what the watchdog is actually watching

**From:** Piper Morgan, Exec role (memo to Janus, `docs/mail/memo-exec-piper-to-janus-week-update-2026-07-09.md`, July 9)

**Relevant to:** Any project running duty-cycle agents or cron-driven processes where a monitoring or stall-detection system exists. Klatch (Calliope, Argus duty cycles); DinP (Janus + Themis pulse cycles); One Job (Relay + Coral sessions).

PM's stall-detection registry covers 4 of 11 active roles. The other 7 are structurally invisible to it: they look correctly-alive by the watchdog's logic because the watchdog was never asked to look at them. One role went dark for 11 days with no alert firing. The watchdog itself was healthy; it was just watching a subset.

The lesson isn't about PM's specific registry — it's about a second-order monitoring assumption that almost every team makes:

> **"We have a watchdog" and "the watchdog watches everything that matters" are different claims. The gap between them fails silently.**

A monitoring system is only as good as its coverage list, and the coverage list can become stale just like any other hand-maintained inventory. A role added after the registry was first set up won't automatically be added to the registry. A role that changes scope may no longer be covered by its existing registry entry. The watchdog won't tell you about this; it doesn't know what it doesn't know.

**Suggested action:** For any monitoring or stall-detection system: enumerate all the things it's supposed to be watching. Cross-reference that list against the full set of agents, crons, or services that currently run. Identify what the watchdog is *not* watching. Then decide whether each uncovered item is intentionally excluded or an oversight. This audit is worth repeating whenever new roles or crons are added — coverage assumptions drift silently in both directions.

## Sources Read

- **Klatch** — git log (48h): `.claude/projects/` added to `.gitignore` (applying July 9 brief suggestion; confirmatory); brief delivery commits. No new methodology.
- **Piper Morgan** — commit log (48h, full): `#1381` fix (`c4995f5`, Lead Dev); exec-to-Janus weekly update memo (`2fcce12`); ADR-077 routing-integrity contract (Arch, July 9 — two-altitude enforcement for LLM action routing; confirmatory of derive-don't-maintain pattern already covered); `#1312` schema reconciliation CI-guarded (confirmatory of impossible-by-construction pattern from July 8 brief). Two new findings above.
- **One Job** — git log (48h): brief delivery and prior-window commits (philosophy page, temperament capture — source material for July 9 insight); no new methodology this window.
- **mediajunkie (Pard)** — git log (48h): Janus-to-Pard memo requesting push of 3 days of local-only work (operational; not insight-worthy).
- **atlas, globe, cuneo, optilisten, weather** — no commits in 48h window; skipped.
- **nyt-crossword** — automated status commits (fetch/print/remarkable); skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
