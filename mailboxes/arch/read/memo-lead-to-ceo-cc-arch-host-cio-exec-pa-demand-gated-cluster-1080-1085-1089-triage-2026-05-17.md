---
from: Lead Developer
to: CEO (xian)
cc: Architect (Chief Architect), HOST (Head of Sapient Trust), CIO (Chief Innovation Officer), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: Demand-gated cluster triage — #1080 (NOTION-WRITE) + #1085 (Slack recent-activity) + #1089 (KG-PRIVACY-FILTER) — one decision call for three
priority: low — triage memo; clears backlog state without rushing demand
response-requested: PM disposition per issue: defer / ship-when-triggered-with-blueprint / activate-now
---

# Demand-gated cluster triage — three issues, one decision call

Per PM directive after #1101 close (~10:15 PT) — bundling the three demand-gated issues into a single triage memo so the disposition call happens once with cohort context.

All three share the same structural shape: **AC-1 is a trigger condition or PM ratification**, not a Lead Dev technical gate. Building speculatively violates the issues' own design (each names "leave dormant until..." in the body). The right move for each is one of three options below.

## The three issues, side by side

| | #1080 NOTION-WRITE | #1085 Slack recent-activity | #1089 KG-PRIVACY-FILTER |
|---|---|---|---|
| **Priority** | priority:low | priority:low | priority:low |
| **Milestone** | Fast Follow | Fast Follow | MVP (M2g label) |
| **What's missing** | Activation of existing `update_document` capability (router+handler+adapter exist; gated by `USE_SPATIAL_NOTION` flag) | New aggregator helper analogous to `_compute_recent_activity` for GitHub | Real privacy filtering on KG read/write paths (placeholder methods removed in #1010) |
| **Code in tree today** | Yes — full path; just flag-gated | No — would build new | No — would build new (defense-in-depth layer) |
| **PM-manual gate** | **Yes** — PM confirms write-scope on integration token (AC-2) | No | No (but AC-2 needs PM+HOST+Architect design call — covered by 2026-05-17 Phase 0 memo `ef8db4168`) |
| **Trigger conditions named** | Alpha user explicitly asks; recurring PM workflow surfaces; 1.0 feedback signals chat-driven doc updates | Alpha asks for Slack in "what happened?"; weekly Ship surfaces Slack as load-bearing; cross-team Slack-Notion-GitHub feed needed | Multi-tenant becomes load-bearing; alpha user reports KG-derived flagged content; Pattern-045-style audit identifies unfiltered → KG path |
| **Demand signals as of today** | None observed | None observed | None observed |
| **Recovery cost if deferred** | Zero (code stays in tree, flag-gated) | Zero (no code yet; build when needed) | Low (#1089 Phase 0 design memo at `ef8db4168` is the implementation blueprint for later) |
| **Cost to activate now** | ~1-2 hr Lead Dev + ~30-60 min PM smoke + PM token-scope step | ~4-6 hr Lead Dev (new aggregator + tests + multi-source fail-graceful) | Multi-day (per #1089 Phase 0 — design ratification + implementation) |

## Disposition options (per issue)

For each issue, three options:

- **(a) Defer (close as still-deferred)** — clears backlog state; reopens instantly when a trigger fires. Issue body remains the spec for later.
- **(b) Ship-when-triggered with blueprint** — leave issue open; commit to writing the design / phase-0 memo now so when demand fires, implementation is unblocked. (#1089 is already at this state per the memo I filed.)
- **(c) Activate now** — build / flip the flag despite no demand signal. Use sparingly; runs into "we built features users didn't want" anti-pattern.

## My recommended disposition (per issue)

### #1080 NOTION-WRITE → **(a) Defer / close**

- Code is fully in tree behind a flag; flipping it later is a 1-line config change + a PM token-scope step
- AC-2 ("PM confirms write-scope on integration token") **blocks any agent activation work** — I can't do that step
- "Most PMs author in Notion's native editor; chat-driven document updates are a narrower use case" (from the issue body) — honest assessment
- Reopen when an alpha user asks for it, or when you have a specific workflow in mind

### #1085 Slack recent-activity → **(a) Defer / close**

- No code to lose if deferred — building is the cost
- Recovery cost zero per the issue body
- Slack integration exists for messaging but no surfacing surface today; building one needs both schema unification + Slack-source aggregator + cross-source-fail-graceful — a real chunk of work
- Reopen when a "what happened?" query surfaces Slack channel activity as load-bearing

### #1089 KG-PRIVACY-FILTER → **(b) Ship-when-triggered with blueprint** (current state)

- Phase 0 design memo at `ef8db4168` is the implementation blueprint
- HOST + Architect still owe input on Q2 (privacy_level semantics) + Q3 (read vs write priority) + Q4 (placement)
- Threat model: defense-in-depth value GROWS with KG-write surface area (e.g., if #1080 activates, Slack integration writes to KG via context, etc.)
- Stays open as "design ratified, implementation gated on demand or first independent KG-write path landing"

## Net backlog effect

If you ratify my preferences:
- **#1080 closes** (deferred)
- **#1085 closes** (deferred)
- **#1089 stays open** (with Phase 0 memo as substrate)

Open M2g count drops from current 1 to 1 (just #1089). Open Fast Follow count drops from 35 to 33.

## Alternative if you want something different

If you'd prefer one of these activated despite no demand signal, name which and I'll proceed. The cheapest activation is #1080 (~1-2 hr) since the code is already there — flipping the flag would let you/alpha-users start asking "update my Notion doc X" and see if it's a workflow that lands. If that's the intent (proactive activation to surface demand), say so and I'll set up the flag + smoke.

## What this memo IS

- Single triage call for three demand-gated issues sharing the same structural shape
- Honest cost / recovery cost / demand assessment per issue
- Lead Dev recommendation (a/a/b) but PM's call

## What this memo is NOT

- Not closing anything yet — waiting for PM ratification before any state change
- Not changing #1089's Phase 0 memo state — that's still awaiting HOST + Architect input on Q2-Q4
- Not gating other Lead Dev work — backlog is otherwise drained; happy to take new direction while you decide

## Cross-references

- #1080 (NOTION-WRITE) issue body
- #1085 (Slack recent-activity) issue body
- #1089 (KG-PRIVACY-FILTER) issue body + Phase 0 design memo `ef8db4168`
- M-backlog snapshot 2026-05-17: `dev/active/M-backlog-snapshot-2026-05-17.md`
- Pattern-067 (Issue-Body Reality Mismatch) — caveat against building before triggers fire

— Lead Developer, 2026-05-17 ~10:25 PT
