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

| Agent | Status | Notes |
|-------|--------|-------|
| Exec | ☐ | Chief of Staff — first priority (owns attention rollup) |
| CIO | ☐ | Duty-cycle architecture |
| Arch | ☐ | ADR author |
| Lead | ☐ | Lead Developer |
| HOST | ☐ | Head of Sapient Trust (was HOSR) |
| Comms | ☐ | Communications |
| CXO | ☐ | Chief Experience Officer |
| Docs | ☐ | Documentation |
| PPM | ☐ | Portfolio Program Manager |

Update ☐ → ✓ with date when an agent's first session on pipermorgan.ai is confirmed.

## Account assignments post-migration

| Account | Scope |
|---------|-------|
| `xian@pipermorgan.ai` | All PM team agents exclusively |
| `xian@designinproduct.com` | Janus, Themis, small products, clients |
