---
from: cxo
to: xian (ceo)
cc: exec, lead, ppm, pa, arch, host, cio
subject: "One missing provisioning step is blocking four lanes at once — the beta gate's criterion 2, PA's Phase-0 probe, #1445 and #1395. It reads as four separate slips and it's one action. Also: PA was right to stop, and my green-light didn't authorize what it stopped for."
date: 2026-07-31 07:4x PT
---

PM — a short one, because I think this looks like four unrelated stalls this morning and it's one
cause.

## The single cause

**The Amber seat has no API credentials reachable by the tooling.** Lead probed it directly on 07-30:

> *"Amber keychain has NO openai/anthropic/github_token entries (probed via KeychainService
> directly). Key provisioning (PM, via KeychainService not security CLI) now gates BOTH #1445
> closure and #1395 Phase 0 (judge)."*

## What it is blocking, as of 07:4x today

| Lane | Blocked thing | Who found it |
|---|---|---|
| **Beta gate** | **#1386 criterion 2** — the canonical suite **skips** keyless, and a skipped suite reports green | PPM 07:10, corroborated by me |
| **PDR-006 rubric branch** | **PA's Probe A** — honesty-under-recomposition; harness written and runnable, cannot execute | PA 07:15 |
| **#1445** | Q48 re-run | Lead 07-30 |
| **#1395** | Phase 0 (judge) | Lead 07-30 |

**Four lanes, three roles, one provisioning step.** Each was reported separately and reads as its own
slip; none of the reporters had the others in view when they wrote.

**The one with teeth is criterion 2**, because its failure mode is silent: a skipped suite and a
passing suite look identical in the output. I've **withheld sign-off** on that criterion and posted
the reasoning on #1386 (per Exec's "evidence belongs on the issue"). It's a *not yet*, not a *no* —
provision keys and I'll sign the same day on a keyed run.

**Not everything this morning is blocked**, and I'd rather not overstate: **Scenario B runs against
deployed beta v28**, which has its own credentials and is a different environment from the local
seat. It may be entirely unaffected, and if Lead runs it I'll review and sign it on its own merits.
Keeping those halves separate is the difference between "one criterion slipped" and "the window
died."

## PA stopped rather than routing around it, and that was right

PA wrote the Probe A harness — five payloads, each exercising a different *kind* of honesty so a
failure identifies which kind is fragile — and then **did not run it**, because the only reachable
credential is yours in the macOS Keychain. PA's reasoning:

> *"pulling PM's credential to fund an experiment PM did not specifically authorize is distinct from
> the app using it in normal operation… CXO and PPM green-lit the probes; neither authorizes spending
> PM's key."*

**That reading is correct and I want to confirm it explicitly**, because the green-light was mine.
**I authorized the probe's design, not the spend of your credential**, and I hadn't thought about the
distinction until PA drew it. It's the right instinct and I'd rather it be reinforced than treated as
over-caution — an agent that reaches into a keychain to unblock itself is a worse failure than a
probe that waits.

## What I'd ask

**One decision, not four**: provision the Amber seat's keys (Lead notes it must be via
`KeychainService`, not the `security` CLI — the service appends `_api_key` to account names and
CLI-stored credentials are invisible to the app). That unblocks all four lanes.

If you'd rather not fund the probe specifically — it costs a handful of API calls against both
Claude and GPT — **say so and I'll design the branch without it**, on stated assumptions rather than
measurement, and flag the rubric as unvalidated. That's a worse outcome but a legitimate choice, and
it's yours rather than mine.

No urgency beyond the window: Exec has sign-offs wanted by noon, and my position is already on the
issue either way.

— CXO
