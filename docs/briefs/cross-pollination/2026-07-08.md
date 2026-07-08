
# Cross-Pollination Brief — July 8, 2026

One clean architectural finding from Piper Morgan: ADR-075 Component B closed a multi-user personalization leak not by adding a guard that detects unscoped data reads, but by redesigning the repository layer so unscoped reads and writes can't be expressed at all. One Job ran rc.7 through rc.9 and is near TestFlight promotion, but no new cross-pollination methodology emerged from those sessions. Klatch was quiet this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Make multi-user data isolation inexpressible, not just detectable

**From:** Piper Morgan, Architect + Lead Dev (ADR-075 Component B, commits `9929fd3` + `82b526a`, July 7)

**Relevant to:** Any project adding per-user data scoping to a previously single-tenant system; Klatch (if multi-user support ships alongside the portability/migration use case)

Piper Morgan's alpha deployment exposed a privacy issue (#1366): a module-level singleton loader served PM's personal system prompt, priorities, and GitHub default-repo to every user on the shared `alpha.pipermorgan.ai` instance. The fix followed the pattern already established by ADR-058 (credentials), ADR-070 (connector bindings), and ADR-071 (content stores): build a new `owner_id`-scoped store and require the scope at the repository method signature level.

Arch's BUILD ratification noted: "the FK-constrained, always-scoped repository methods mean an unscoped read or write *can't be expressed*, not merely that it's avoided." There is no method on `PersonalizationContextRepository` that takes fewer than the required `owner_id` parameter. The FK constraint rejects non-existent IDs. The wrong code can't be written — this is the difference between *detectable* and *inexpressible*:

- **Detectable**: add an enforcement hook that fails the build if someone writes an unscoped call — catches the mistake after it's written, requires hook maintenance
- **Inexpressible**: design the method signature so there's no unscoped call to write — no mistake to catch

ADR-075 also settled a three-category taxonomy for configuration ownership: per-user (system-prompt context, default-repo, default-labels), PM-domain-global (shared PM-authoritative content), and install-wide (numbering format). The taxonomy matters: "scope everything by user" is itself a defect — install-wide config doesn't need per-user plumbing, and the D5 enforcement guard must distinguish legitimate category-3 reads from category-1 leaks.

**Suggested action:** Before adding per-user isolation to an existing shared data layer, decide the taxonomy first (which fields are per-user, which are instance-wide) and then design new repository methods that require scope as a typed parameter rather than patching existing methods with an optional scope argument. The FK constraint enforces it at the database level; the method signature documents the requirement. The ADR-058 → ADR-070 → ADR-071 → ADR-075 family at PM is a clear template for how to layer these decisions across credential, connector-binding, content, and configuration concerns.

## Sources Read

- **Klatch** — git log (48h): cross-pollination brief delivery + cycle log entries only. Cohort in prep for v1.0 cut (xian's authorization). No new methodology.
- **Piper Morgan** — Lead Dev + Arch session logs (`dev/2026/07/07/`); `docs/internal/architecture/current/adrs/adr-075-configuration-personalization-ownership.md` (full read); `docs/internal/architecture/current/adrs/adr-076-usage-cap-enforcement.md` (status line). ADR-075 Component B closed with live verification (`9929fd3`); ADR-076 closed with live verification (`bc82269`); Epic E closed whole (9 issues: wizard invite-token fix, email-or-username login, PM-issued password reset, `8156b1d`); #1305 EncryptedJSON shipped (`9edf21b`); deploy runbook drafted (`b826e0d`). 11 beta blockers closed total (20→10 open). Mostly operational; one transferable insight above.
- **One Job** — git log (48h); `development/coral-logs/2026-07-07-coral-log.md`. rc.7 (chain rooms at every depth — completed sub-cards visible with breadcrumb), rc.8 (sifting in chain rooms via vertical swipes), rc.9 (sub-card edit loss fixed — `onUpdateTask` now wired through SubstackView, and TaskDetails refuses to enter edit mode if no save path exists). Website overhauled; pricing proposal drafted. TestFlight promotion near. No methodology that clears the cross-pollination bar independently of yesterday's brief.
- **atlas, globe, cuneo, optilisten** — no commits in 48h window; skipped.
- **nyt-crossword, weather** — automated status/delivery commits only; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
