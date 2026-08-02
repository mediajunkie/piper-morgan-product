# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — this is one of the few real paths to PM.**

---

## PM Attention

*(Whole-file rewrite at the 2026-08-01 STOP. Timestamp verified with `date`. Live items only.)*

- 🔴 **UNRESOLVED, and PM should not inherit it as settled: the `lead` composer draft.** Someone typed *"ok keys are in the keychain now, try #1445 again"* into lead's input box and never sent it; **PM does not recognise writing it**, and its timing is unknown. Per Exec, provisioning must go through the app's **`KeychainService`, NOT the `security` CLI** — consistent with PA's 7/31 finding that Amber's keys are unprovisioned. **The draft wants sending or clearing deliberately, and the key state verified through the app path** rather than inferred from an unattributable line.
- 🟢 **`lead` is awake** — dark 07-30 09:45 → 08-01 22:03, now committing. **I reported it healthy on 7/31 and was wrong**; see the log. Its wake was on Exec's critical path the whole time.
- 🟢 **THE MIGRATION HAS TAKEN — and the number keeps climbing.** `closed today: 9/11` (8 on 7/31, **1 on 7/29**). 11/11 live, 11/11 registry rows, belt clean.
- 🟡 **The innovation agenda — PM asked for it once the migration landed, and nothing blocks it.** It has now waited three days behind migration follow-through. **This is the next substantive thread and I should stop letting operational corrections crowd it out.**
- 🟡 **claude.ai account tier** — PA's surviving item. Still PM\'s, still open, and deliberately kept visible so the OpenAI retraction does not bury it.
- 🔴 **Memory-index guard is on the GENERATOR, not the FILE.** Direct edits to `MEMORY.md` succeed silently past the ceiling; the platform reminder says *"compact this file"*, pointing at the unguarded path. Four agents have refused it **on judgment**, which is not a safety property. **Guard placement is the prior question; format choice (prune / two-tier) is PM+HOST\'s.**
- 🟡 **`host` / `comms` / `web` registry rows carry no job id.** The cron is session-scoped with two silent death modes, so a row records **intended cadence, not a live job**. Convention is in the registry header; not chased role-by-role.

## Shipped today

**`duty-cycle-tick` v1.23** — the pane-reading method, fixed at the method rather than the instance (Janus\'s amendment, verbatim): *read ABOVE the input separator, or corroborate with an artifact a real exchange produces; a quoted "user" line in the input box is a claim ABOUT the user, not a message FROM them*; and capture twice, minutes apart.

## Lower priority / queued

- **Nothing expires a negative claim** — still the strongest mechanism candidate, now with two expensive instances (the OpenAI referent, the blind-sweep note).
- **Nothing re-verifies an inherited action\'s REFERENT** — *"is it still open?"* is checkable and gets checked; *"is it still the right thing?"* is neither.
- **No composition test for multi-part changes** · **nothing consumes a review\'s second-order findings.**

## Cron

`7 10,16,22` LEAN — job **`44e16ee9`**, **auto-expires ~2026-08-07**. Verified alive at today\'s first fire and the registry row matched — the job-id convention working on its first real check. ⚠️ Session-scoped: dies silently on session exit *and* at expiry.

⚠️ **Two fires lost this week to classifier outages** (7/30 STOP, 8/1 START). Both left the day unlogged or unclosed until the next fire caught it. **An outage-blocked fire is indistinguishable from a skipped one in the record** unless the next fire says so.

<!-- Whole-file rewrite 2026-08-01. Rewriting the TOP is not rewriting the FILE. -->
