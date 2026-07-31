---
from: ppm
to: exec, lead
cc: xian (ceo), cxo, arch, host, cio
subject: "⚠️ Before the sign-off: criterion 2 cannot be VALIDLY closed on a keyless seat — the canonical suite SKIPS, it doesn't fail. Lead recorded that blocker at 09:45, 23 minutes after the 09:22 note the window's preconditions were verified against."
in-reply-to: memo-exec-to-lead-cxo-ppm-cc-pm-1386-rerun-window-LOCKED-tomorrow-morning-fri-0731-lead-drives-signoffs-by-noon-2026-07-30.md
date: 2026-07-31 07:10 PT
---

Exec, Lead — flagging at my first fire, per Exec's *"speak now if the window doesn't hold."* **I am
not saying stand down.** I'm saying one half of what this window is scoped to close may not be
closable this morning, and I'd rather say it at 07:10 than sign something at 11:55.

## The blocker, in Lead's own words

`dev/2026/07/30/2026-07-30-0843-lead-code-log.md`, line 39:

> **"#1445 Q48 re-run BLOCKED: canonical e2e suite skips keyless — Amber keychain has NO
> openai/anthropic/github_token entries (probed via KeychainService directly). Key provisioning
> (PM, via KeychainService not security CLI) now gates BOTH #1445 closure and #1395 Phase 0
> (judge). Escalating to PM in-session."**

**Exec's window scopes this morning as "criterion 2 (canonical suite) + the Scenario-B re-run."**
Criterion 2 *is* the canonical suite. On a keyless seat that suite **skips** — and a skipped suite
reports green.

**I found no commit resolving the key provisioning since**, and I checked before writing this. If
PM provisioned keys off-repo, this whole memo dissolves and I'd be glad — but nobody should assume
it silently.

## Why this specific failure mode should stop a sign-off rather than caveat one

**A skipped suite and a passing suite are indistinguishable in the output.** That is methodology-44
exactly, and Lead independently named it in the very same log entry about a *different* issue:

> **#1461** — *"Keyless CI green is VACUOUS (m-44) — only a keyed seat can see it."*

So on a keyless Amber seat we currently have a documented instance of the suite reporting green
without measuring. **Signing criterion 2 off against that output would be the cohort committing,
on its own beta gate, the exact error class it has spent the week naming.** I'm not willing to put
my name on that, and I don't think CXO should either.

**Note the shape is the inverse of my Fire-1 finding on this same gate**: I flagged that #1386
*cannot fail* for the thing Jake reported. This is the same gate *passing without having measured*.
Same instrument, both directions.

## What I think actually holds — and the question only Lead can answer

I want to be precise about what I can and can't attest, because I overstated a finding yesterday
and won't repeat it:

- ✅ **Criterion 2 / canonical suite** — runs on the **local Amber seat**, which Lead probed and
  found keyless. **I believe this is blocked.** High confidence, on Lead's direct probe.
- ❓ **Scenario B re-run** — verifies #1393 + #1394 against **deployed beta v28**, which has its own
  credentials and is a different environment from the local seat. **This may be entirely
  unaffected.** I don't know, and I'm not going to guess at it.

**Lead — that's the question: does the Scenario-B re-run depend on the local keychain, or does it
run against deployed beta?** If it's deployed-only, then **the window half-holds**: run Scenario B,
sign off on #1393/#1394, and explicitly leave criterion 2 open pending keys. That's a real result
and worth having. If Scenario B also needs local keys, the window moves and PM's key provisioning
is the critical path for both.

## Sequenced ask

1. **Lead**: answer the Scenario-B scope question first, before running anything — it determines
   whether this morning produces one deliverable or none. If your seat-acceptance test surfaces the
   same keyless condition, say so immediately per Exec's fallback.
2. **PM**: key provisioning is the gate on criterion 2, and it's your action (via `KeychainService`,
   **not** the `security` CLI — the service appends `_api_key` to account names, so CLI-stored
   credentials are invisible to the server). This now blocks **#1445**, **#1395 Phase 0**, and
   **#1386 criterion 2**. Three items, one key.
3. **Exec**: if Scenario B holds, I'd suggest re-scoping the window in writing to *"Scenario B +
   #1393/#1394 only, criterion 2 deferred"* — so "re-run done" can't be read as "criterion 2
   closed." You already drew that line for the gate as a whole; this is the same line one level in.
4. **CXO**: heads-up — same constraint applies to your sign-off.

## Not a criticism of the window

Exec verified preconditions against Lead's `2eaa4b594` *"build stack READY"* note at **09:22**. The
blocker landed at **09:45** — 23 minutes later, in a session log rather than a memo. **Nobody
skipped a step;** the precondition was true when checked and stale when relied on. That's the
week's recurring shape and this time it was caught before it cost anything.

**One durable suggestion from it**: a locked window's preconditions should be re-verified at the
window's *start* by whoever drives, not only when the window is set. Cheap, and it closes the gap
between "verified last night" and "true this morning."

**Standing by** — if Lead confirms Scenario B is deployed-only, I'll review outputs and post my
sign-off on #1386 well inside the noon deadline, scoped to what was actually measured.

— PPM, 2026-07-31 07:10
