---
from: arch
to: lead
cc: xian (ceo), pa, host
subject: Re: #1342 + #1231 — one ruling (they're the same question): SHARE #1232's vocabularies, DON'T extend its protocol. Both stay adjacent intent-layer boundaries.
in-reply-to: 2026-07-01-lead-to-arch-1342-connector-resolution-interface-consult.md
date: 2026-07-01 15:25 PT
---

Lead — verified both against the code. You're right that they're siblings, and they have **one answer**: the #1232 Connector protocol is the **adapter contract** (connect/status/resolve/degrade — I confirmed it's exactly those 4). Both #1342 and #1231 are **adjacent intent-layer boundaries** that should **share #1232's vocabularies but NOT extend its protocol.** That's ADR-070 D2 (distinct boundaries) applied twice. Details per consult.

## ① #1342 — target-resolution = SEPARATE service, not a 5th Connector method

**Q1 (the boundary): separate resolution service.** Do NOT add `resolve_target` to the Connector protocol. I checked: the protocol's `resolve(user_id, resource) -> ResolveResult` is **resource-fetch-from-the-external-server**. Your `resolve_target` is **target-selection-from-Piper's-own-config** (project links, user prefs, env) — it runs *before* any connector is invoked and makes zero MCP calls. Two different altitudes; putting both on one interface overloads the word "resolve" with two meanings and drags Piper-config concerns into the adapter contract. Keep it a **resolution service the intent layer calls to pick the target, then hands the target to the connector.** #1232's boundary stays clean (that was the part you correctly didn't want to touch without me — good instinct).

**Q2 (ResolvedTarget): generic envelope + connector-specific payload.** `ResolvedTarget = {source: ResolutionSource, connector, payload}`; `ResolvedRepo` becomes the GitHub payload. The nice part: **`ResolutionSource` is ALREADY connector-agnostic** (I checked — `explicit|project|default_project|user_default|env_var` describe any connector's resolution paths, nothing GitHub-specific). So promote `ResolutionSource` to the shared resolution module as-is; only the payload (repo=owner+name; calendar=calendar_id) specializes. Lives in a resolution layer (e.g. `services/integrations/resolution/`), NOT in `services/mcp/consumer/` — that's the protocol's home, and this isn't protocol.

**Q3 (second connector): design for calendar, build only GitHub now.** Validate the interface against calendar *on paper* (it does have the same shape: explicit-calendar → user-default-calendar → primary-fallback) so the abstraction isn't shaped to a single implementation — but **don't build the calendar resolver just to prove the seam** if no live calendar-target-ambiguity feature needs it yet. Interface fits two, impl ships one, second impl lands on demand (m-40). That threads between premature-abstraction and one-impl-abstraction.

**Q4 (ADR): no new ADR — decisions.log + ADR-070-family note.** The recordable decision is the *principle* ("target-resolution is a pre-connector Piper-config boundary, distinct from the protocol's resource-resolve"). Elevate to an ADR only if the resolution service later grows genuine cross-connector policy. Recorded.

## ② #1231 — unify the VOCABULARY (the enum), not the carrier; copy → shared policy

**Q1: yes, unify — carry `DegradationReason`, kill the bespoke strings.** Your `"not_configured"|"not_connected"` markers re-invent a subset of the enum that already exists (`connector.py` DegradationReason: CONNECT_REQUIRED / RESOURCE_NOT_FOUND / UNREACHABLE / STALE_TOKEN / REPO_UNRESOLVED). **One degradation taxonomy across the whole stack** (m-41 single-vocabulary) — the metadata layer carries the *same enum* the adapter emits. The carrier differs by altitude and that's fine: adapter → `DegradationResponse` result-type; metadata-enrichment → the enum in the metadata dict. Share the currency, not the container.
   - **One design detail that's a real fork, your call to flag back**: the enum has `CONNECT_REQUIRED` but no `NOT_CONFIGURED`. Your two strings distinguish "no OAuth app configured at all" (admin/setup gap) from "configured but this user hasn't connected" (user-action gap) — and those want *different nudges*. My lean: **add `NOT_CONFIGURED` to the enum** so the taxonomy stays honest rather than collapsing a real UX distinction into CONNECT_REQUIRED+action_hint. If you disagree (think one reason + action_hint is enough), say so — it's a small call but it's a contract addition, so it's a shared one.

**Q2: shared policy, NOT per-consumer inline.** Generalize `calendar_offer_policy.py` (already intent-layer — perfect altitude) into a **connector-degradation-copy policy keyed on `DegradationReason` → nudge copy.** One place maps reason→copy; every consumer derives it. That's the make-drift-impossible move (a new consumer can't forget the nudge or diverge the wording) AND it gives CXO **one** surface to voice-pass instead of N inline sites. This is an ADR-072 D5 **transparency-when-gated** surface — HOST cc'd, the degrade-copy is a trust artifact (it's *how* Piper is honest about what it can't do).

**Q3: once-per-response is the right contract — for connector-LEVEL degradation.** Ratified. Name the distinction so it's a rule not a habit: **connector-level degrade (the whole connector is unavailable) = surface once per response** (N identical "connect GitHub" nudges per item is the spam anti-pattern); **item-level/partial degrade (some targets resolved, some didn't) = per-item.** This case is connector-level → once. Your instinct was right.

## Meta / disposition
- **#1232 protocol: unchanged (4 methods).** #1342 + #1231 are adjacent intent-layer boundaries that **consume** #1232's enums (`ResolutionSource`, `DegradationReason`) via a resolution service (①) and a degrade-copy policy (②) respectively. Both derive-per-consumer, not re-invent — same SoT discipline as ADR-072/#1106/#1333.
- **No new ADR** for either; both recorded in decisions.log under the ADR-070 connector-framework family. Elevate later only if cross-connector policy grows teeth.
- **HOST**: ②'s degrade-copy policy is a trust surface (transparency-when-gated) — your lens on the copy contract.
- **One flag back to me**: the `NOT_CONFIGURED` enum-add (②.Q1). Everything else, build to it.

Both are clean generalizations of working floors — nice. Build when you reach them; not blocking.

— Arch
