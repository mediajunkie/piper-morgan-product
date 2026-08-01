# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — this is one of the few real paths to PM.**

---

## PM Attention

*(Whole-file rewrite at the 2026-07-31 STOP. Timestamp verified with `date`. Live items only.)*

- 🔴 **RETRACTED — "start OpenAI identity verification" is OFF the board. It was the WRONG ACTION, and I carried it here for ten days.** PA read OpenAI's own docs: **API organization verification** (what I kept pointing PM at) unlocks advanced API models — **not on the ratified path and not required for a directory listing**. Directory submission needs a *distinct* **verified developer/business identity**, in the same org **and project** you submit from. **And the ID is rate-limited: one organization per 90 days** — so verifying the wrong org would have **blocked the right one until ~29 October.** I was urging PM to spend a three-month-lockout action on the wrong target and calling it a five-minute unblock. **How it survived**: I inherited it from PA's 7/19 research and re-checked *whether it was still open* (true, always) and never *whether it was the right action* — m-43 on my own carry-forward. Arch and PPM both flagged the ambiguity and **declined to assert an answer**, which is what sent PA to the source. **New dependency worth knowing**: MCP connector submission also needs **domain-ownership verification for `mcp.pipermorgan.ai`, which does not exist yet.**
- 🟡 **claude.ai account tier** — the other half of PA's pair. Still open, still PM's, and **unaffected by the retraction above**; do not let the OpenAI correction bury it.
- 🟢 **THE MIGRATION HAS TAKEN.** 11/11 on Amber, 11/11 registry rows, and **8 of 11 roles closed their own day cleanly today** (was 1 on 7/29). That number is the evidence, not the provisioning count.
- 🟡 **`lead` is not stalled — PM is driving it interactively.** No commits since 07-30 09:45 and 69 unread, but its pane shows a live exchange with PM. It is `parked`, so the belt cannot report it either way. **Check the pane before reporting any silence** — second time this week a role that looked structurally blocked was simply mid-conversation (PA was the first).
- 🔴 **The memory-index guard is on the GENERATOR, not the FILE** — my earlier "loud refusal, annoying and safe" was **right about `rebuild-memory-index.py` and wrong about the path the pressure points at.** Direct edits to `MEMORY.md` succeed silently past the ceiling (HOST + PA tested), and the platform reminder says *"compact this file"* — an instruction to hand-edit. Four agents have refused it **on judgment**, which is not a safety property. **Format choice (A prune / B two-tier) is PM+HOST's; the guard\'s placement is the prior question.**
- 🟡 **`host`, `comms`, `web` registry rows carry no job ID.** The cron is session-scoped `CronCreate` with **two silent death modes** (dies on session exit; 7-day auto-expiry), so a row records **intended cadence, not a live job** — it reads `watched` whether the cron is armed, expired, or never created, and only the owning agent can check. Convention now documented in the registry header; deliberately not chased role-by-role.

## Shipped today

Retroactive close of 7/30 (its STOP was cut off mid-fire by a rate limit) · **stranded `cohort-status` fix rescued and merged rather than clobbered** — HOST/Web had improved the DAY-CLOSED predicate meanwhile, so I took theirs and re-applied only my structural half · registry header now documents the cron mechanism + both death modes · my own row now carries job `7b089a43` and its **~2026-08-06 expiry** · corrected my loud-refusal claim to PM and the cohort.

## Lower priority / queued

- **Nothing expires a negative claim** — still the best mechanism candidate on the list, and the OpenAI retraction is its most expensive instance to date.
- **No composition test for multi-part changes.**
- **Nothing consumes a review\'s second-order findings.**
- **Innovation agenda** — PM wants it reviewed now the migration has landed. **This is the next substantive thread and nothing blocks it.**

## Cron

`7 10,16,22` LEAN — job **`7b089a43`**, created 2026-07-30, **auto-expires ~2026-08-06**. Re-armed at the 2026-07-31 STOP (delete → create → verify). ⚠️ Session-scoped: dies silently on session exit *and* at expiry.

<!-- Whole-file rewrite 2026-07-31. Rewriting the TOP is not rewriting the FILE. -->
