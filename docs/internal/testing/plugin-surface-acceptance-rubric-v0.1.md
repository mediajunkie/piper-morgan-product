---
type: acceptance-instrument
name: Plugin Surface Acceptance Rubric
version: v0.1 DRAFT (CXO, 2026-10-24). Unratified instrument; the gate it serves is ratified (PDR-004 Amendment A, xian 2026-10-23 17:54).
owner: CXO
companion_to: byoc-recomposition-rubric-v0.1.md (scores the host's recomposed replies); colleague-test-rubric.md (scores replies Piper composes)
serves: PUB #1701 to #1707 (MCP-path increments 2 to 8); production map finding F10; go-ahead approved by xian 2026-10-24 17:28
last_updated: 2026-10-24
currency_claim: revise-on-first-use
---

# Plugin Surface Acceptance Rubric v0.1

**What it is for.** On the plugin surface the host's model writes what the user reads, from payloads we send. We own the payload, the tool description and the failure shape, and we do not own the sentences. So this rubric is a pass/fail checklist on what we own, run per tool and per increment. It does not score tone, and it does not replace the Recomposition Rubric, which scores what the host did with our payload (its T axis is the honesty-under-recomposition test and #1703 must run it).

**The rule behind it (ADR-080).** Meaning is the model's. Actions, their reports, facts and capability claims are code's. A payload is code's voice: it may not say anything the code did not verify.

**How to use it.** An increment is not Done until every check below passes, or is named N/A with a reason. Scored by CXO on quoted payloads and quoted host replies from a served run on alpha, one client at a time (Claude first, the second host named when it exists). Forced failures that cannot be produced on alpha are pinned and said so at close, as on the chat surface.

## A. The tool catalog (once per tool, before it ships)

| # | Check | Evidence |
|---|---|---|
| A1 | The name and description claim only what the tool does: read or write, which account, which sources. | Read against the handler's code. |
| A2 | The annotations are true. A tool that writes is not marked read-only; a read tool is. | Annotation vs handler. |
| A3 | No model call inside the tool path (PDR-006). | Build-time allowlist and the capability test. |
| A4 | The description tells the host how to relay empty, failed and not-connected sections (it says "report empty sections as empty" today; each increment adds its own). | Description text. |

## B. The payload (every shape the tool can return)

| # | Check | Evidence |
|---|---|---|
| B1 | **Three states, never one.** Every section says one of: has data, verified empty, not connected, couldn't read. A failed read is never an empty section. | Payload per state; the failed state forced by a pin at the bottom layer. |
| B2 | **Not connected is not failed.** No stored credential reads "not connected" with the connect path for this surface. Any store or network failure reads "couldn't read". | Same split as the chat surface (#2151, ADR-081 D1). |
| B3 | **A count over a window carries the window.** "At least N, I read the first 100" is in the payload, not left to the host to remember. | Payload with a full window. |
| B4 | **Write results come from code.** A write returns what happened (done, refused, or couldn't confirm) as a field the host can quote, not for it to infer. An unknown outcome says so and where to look. | Payload per outcome. Applies to #1701 (file an issue) and #1702 (to-dos, reminders). |
| B5 | **No claim about a capability the surface lacks.** The payload never names a feature, source or action this surface can't do. | Payload text read against the tool list. |
| B6 | **The relay sentence is provided where it matters.** For each failed or not-connected state the payload carries one plain sentence in our house form the host can pass on unchanged ("I couldn't check X just now… tell us"). | Payload text. |

## C. Failure shapes (served, where alpha can produce them; otherwise pinned and said so)

| # | Shape | Pass when |
|---|---|---|
| C1 | Signed out or token expired | The host is told to reconnect, on this surface's own path, and nothing is read as empty. |
| C2 | Not connected (no GitHub, no calendar) | The payload says so and names the connect step on the plugin, not only on the web app. |
| C3 | A read fails mid-payload | The other sections still return, the failed one says it failed, and the tool call does not fail as a whole. |
| C4 | A write whose outcome is unknown | B4's unknown-outcome form; the host is not given a success to repeat. |
| C5 | Outage | The payload says Piper is unreachable and does not read as an empty account. |

## D. Run it

1. One served run per increment on a fresh and on a seeded account: the payload (quoted), the host's reply (quoted), and the account's real state stated first.
2. Score A, B, C as pass, fail or N/A. Any B1, B2 or B4 fail is class 3 (honesty). The rest are UX issues unless they put a false statement in front of the user.
3. Where the increment has composed replies at stake (#1703, #1705), run the Recomposition Rubric's T test alongside; this rubric does not substitute for it.

## E. What this rubric does not tell you

Nothing about tone or phrasing the host chose, nothing about routing (whether the host picked the right tool), and nothing about the install flow's usability. The install and connect path on each host (the flow a user walks to add the plugin) needs its own served walk; it is the first row of the first run, and will become §F when there is a real install to score.

## Provenance

Drafted by CXO from: the tool-catalog gate in the Recomposition Rubric §4; the live tool's description and per-section `read_failed` handling (`services/mcp/server/resources.py`); the #2151 honesty sweep's failed-read and not-performed split; and PDR-004 Amendment A. First use: #1701.
