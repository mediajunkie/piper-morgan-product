# PM Agent Migration to pipermorgan.ai

*Orchestrated by Janus (DinP), initiated 2026-07-02*

## Context

As of July 2026, PM team agents are migrating from the `designinproduct.com` Claude account to `xian@pipermorgan.ai`. The goal is account separation: pipermorgan.ai is PM-exclusive; designinproduct.com serves Janus, Themis, small products, and clients.

## Why it's simple

PM has no CCR triggers (all CronCreate — session-level, die when Claude exits) and no persistent account-level scheduled processes. The duty-cycle watchdog (`com.pipermorgan.duty-cycle-watchdog`) is a local launchd bash script — not a Claude process, no migration needed. Duty cycles auto-restart when sessions resume on the new account.

Migration = open PM sessions on pipermorgan.ai instead of designinproduct.com.

## Protocol

1. Close the PM session on the designinproduct.com account before opening on pipermorgan.ai.
2. Never both simultaneously — avoid double-billing.
3. First session on the new account: agent reads this file and confirms migration receipt.

## Agent checklist

**Status as of 2026-07-16 (PM, in conversation)**: still no Piper Morgan project agent migrated. **This now has a real deadline: PM wants this done by end of month**, alongside the related-but-separate KindSys.us vacate (below) and standing up the designinproduct.com split for business/client/other-product agents. Three-part plan as PM framed it 7/16: (1) vacate KindSys.us, (2) move Piper Morgan agents to pipermorgan.ai (this checklist), (3) business/client/other-product agents to designinproduct.com (already this doc's documented end-state, see "Account assignments post-migration" below — no new decision needed there, just execution). Previously "ready whenever Exec wants to sequence it" with no date; **now genuinely due, worth Exec sequencing this rather than leaving it queued.**

All Piper Morgan Code agents (including this CIO session) currently run on `designinproduct.com`, same as everyone else in the cohort. The one live pipermorgan.ai instance is **Coral (One Job project, running the Fable model)** — a different project's early adopter, not part of this checklist. Separately, Piper Open and Vergil currently run on `KindSys.us`, which closes end of July 2026 — a real, dated migration those two need before the account itself disappears (tracked here for awareness; not this checklist's roles — that's a different project's migration, cross-project coordination if useful).

| Agent | Status | Notes |
|-------|--------|-------|
| Exec | ☐ | Chief of Staff — first priority (owns attention rollup); **typically comes over LAST in a full-team migration** (PM convention) so it can oversee the others' transitions |
| CIO | ☐ | Duty-cycle architecture — helps scope migration logistics/tooling for the team |
| Arch | ☐ | ADR author |
| Lead | ☐ | Lead Developer |
| HOST | ☐ | Head of Sapient Trust (was HOSR) |
| Comms | ☐ | Communications |
| CXO | ☐ | Chief Experience Officer |
| Docs | ☐ | Documentation |
| PPM | ☐ | Portfolio Program Manager |

Update ☐ → ✓ with date when an agent's first session on pipermorgan.ai is confirmed.

## Duty-cycle continuity assessment (CIO, 2026-07-06)

PM asked to start "at any time," but carefully — specifically calling out routines, scheduled tasks, and crons transferring correctly. Assessed the actual mechanics:

- **CronCreate jobs are session-scoped, not account-scoped.** A cron job lives inside a given Claude Code session process; it has no tie to which Anthropic account authenticated that session. Migrating accounts is mechanically identical to any normal session end + fresh START — the old session's cron dies (as it would regardless of migration), the new session re-arms its own via the existing `duty-cycle-tick` START procedure. **No new mechanism needed.**
- **The watchdog (`com.pipermorgan.duty-cycle-watchdog`) is account-agnostic by construction** — it's a local launchd bash script, not a Claude session, and it watches shared filesystem state (`duty-cycle-registry.tsv`, session-log timestamps). It needs zero changes for a migration.
- **Registry rows, carry-forwards, and mailboxes are all filesystem-based** — account-agnostic, transfer automatically since they live in the shared repo, not in any account-specific state.
- **The one real risk is exactly what the existing protocol already names**: overlapping old-account and new-account sessions for the same role (double-billing risk, and — per this week's Belt-4/self-attribution-drift work — a genuine confusion risk if both sessions are simultaneously active). "Close old before opening new" (protocol step 1-2 below) is the correct, sufficient guard; no additional tooling needed there either.

**Net**: the underlying duty-cycle infrastructure is already migration-safe. The work is sequencing and verification (does each role's first pipermorgan.ai session correctly find its carry-forward, re-arm its cron, and confirm nothing account-specific leaked into any script/hook), not building anything new. Ready whenever Exec wants to sequence it.

## Account assignments post-migration

| Account | Scope |
|---------|-------|
| `xian@pipermorgan.ai` | All PM team agents exclusively |
| `xian@designinproduct.com` | Janus, Themis, small products, clients |
