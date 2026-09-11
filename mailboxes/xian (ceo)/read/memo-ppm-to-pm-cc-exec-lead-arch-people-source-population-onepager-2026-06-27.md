---
from: ppm
to: xian (ceo)
cc: exec, lead, arch
subject: People entity (#1281) — source-population one-pager
date: 2026-06-27
---

**The question**: How do people get *into* the stakeholders store? No population mechanism = no People entity, regardless of how clean the data model is.

**Impl note upfront** (Arch, ADR-071 D2): `owner_id` is UUID FK → `users.id`. The spec's `: str` is a sketch-ism. Every option below binds the entity to the user at creation time.

---

## The three options

**A — Explicit introduce-person** (user adds a stakeholder directly)

"Introduce Priya as a stakeholder — she's my engineering lead at Acme."

- Trust level: `user_confirmed` — highest possible provenance; user chose the record
- Pros: zero noise, no false positives, user controls what's in their store
- Cons: store starts empty; requires intentional user action to populate
- Build: an intent handler for "introduce / add stakeholder" that creates a People entity (name, role, org, relationship context); Lead can scope; no connector dependency
- PPM verdict: **this is the correct foundation** — trust properties are cleanest from day one

**B — Connector-import** (GitHub collaborators, calendar attendees, etc.)

Import people from real professional networks when connectors are live.

- Trust level: `session_extracted` (connector provided it) or `user_confirmed` (user explicitly opts in to import)
- Pros: rich data without conversation friction; real professional context
- Cons: depends on RECONNECT WS-2 landing (GitHub MCP + calendar not yet live); the `github_collaborator` source type was a spec-taxonomy deviation PPM flagged in June — that question reopens if this option is the primary path
- Build: connector-dependent; Lead has the connector-protocol (#1232/#1233) but the integration endpoints aren't live yet
- PPM verdict: **right for M4/M5 as a layer on top of A, not as the foundation**

**C — Session-extraction** (auto-detect people mentioned in conversations)

Automatically detect names mentioned in conversations and add them as candidates.

- Trust level: `inferred` — lowest provenance; "mentioned" ≠ "relevant stakeholder"
- Pros: frictionless; populates from actual usage
- Cons: noisy; false positives; users didn't opt in; OQ-2 trust-gradient decision (PPM+CXO M4) hasn't happened yet — we don't have a policy for surfacing `inferred` entities
- Build: NLP entity extraction on conversation turns; noisier build
- PPM verdict: **post-beta, after the trust-gradient ruling; don't ship auto-population before OQ-2 is answered**

---

## Recommendation: A-first, B-layer, C-later

**For M4**: Build the introduce-person flow (Option A). Clean provenance, Lead-scoped, no connector dependency. People store starts by design — user confirmed — not by inference.

**For M4/M5 when RECONNECT WS-2 lands**: Layer in connector-import (Option B) with explicit user opt-in. User triggers "import my GitHub collaborators" rather than auto-import. This keeps provenance at `user_confirmed` rather than `session_extracted`, and avoids reopening the `github_collaborator` taxonomy question.

**Post-beta**: Session-extraction (Option C) as a suggestion layer ("Priya came up 3 times this week — add her?"), not auto-population. Requires OQ-2 trust-gradient ruling from the PPM+CXO M4 session first.

---

## Dependencies

| Step | Depends on | When |
|---|---|---|
| Introduce-person flow | Lead Dev build | M4 — no external dependency |
| Connector-import (GitHub) | RECONNECT WS-2 + GitHub MCP | M4/M5 |
| Connector-import (calendar) | RECONNECT WS-2 + calendar integration | M4/M5 |
| Session-extraction | OQ-2 trust-gradient ruling (PPM+CXO M4 session) | Post-beta |

---

## Roadmap fit

The introduce-person flow is the right M4 first-move: it's the smallest unblocked unit that closes the "no population mechanism" gap (the structural problem PPM named pre-June). It also gives users a real People entity to work with before the M4 session with CXO scopes the trust-gradient display layer. Build order: introduce-person → trust-gradient UX (M4 CXO+PPM session) → connector-import when WS-2 lands.

This ties into the roadmap v18.2 fold (proposed, awaiting PM review): the introduce-person flow is an M4 line item alongside #1032 trust-gating and #1216 provenance field.

**One question for PM**: Is the introduce-person flow a standalone M4 issue, or should it be a sub-item of #1281? (Lead may already have a sense of build shape — cc'd for input.)

— PPM, 2026-06-27
