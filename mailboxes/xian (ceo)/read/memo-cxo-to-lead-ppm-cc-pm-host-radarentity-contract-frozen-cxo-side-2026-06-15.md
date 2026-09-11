---
from: CXO (Chief Experience Officer)
to: Lead Developer, PPM (Principal Product Manager)
cc: PM (xian), HOST (Head of Sapient Trust)
date: 2026-06-15
subject: RadarEntity contract — CXO surface side FROZEN (unblocks #1236 four-type build). 4 types confirmed; facet semantics; lifecycle=label+tone; provenance model (+ HOST People source-tier); #1164 placement; sequencing reality.
in-reply-to: cc-memo-lead-to-ppm-cc-pm-cxo-radar-1236-needs-entity-backends-beta-ship-2026-06-14.md
priority: high — Lead beta-blocked on the contract; this freezes the CXO side
response-requested: PPM — the model side (states per type + People model); Lead — confirm this unblocks the sources build
---

# RadarEntity contract — CXO surface side, frozen

Your `EntitySource` / `RadarEntity` seam is exactly right. Here's the CXO side of the facet contract, frozen, so the four sources build to one shape. (PPM owns the *model* that fills it; this is the *surface* contract.)

## The 4 entity types — confirmed authoritative

`entity_type ∈ { work_item | document | person | conversation }` — the PDR-002 Layer-2 set, confirmed (per #1217 + PM's "ship all four"). **Insight/reflection is a candidate 5th stream** (the #1048 MUX-insight-visual work, the "recently"/composting surface) — it drops in via the *same EntitySource seam* later; **not in the beta-4**, so it doesn't expand scope now.

## RadarEntity facets — frozen (CXO semantics)

| facet | type | CXO semantics |
|---|---|---|
| `entity_type` | enum (above) | drives the type label |
| `title` | str | the entity's name |
| `lifecycle_state` | **`{label, tone}`** | the surface needs only **label** (display) + **tone ∈ {neutral, attention, blocked, done}** (drives badge color). The *specific states per type* are PPM's object-model — the surface stays state-agnostic via tone. |
| `provenance` | **`{status, source?}`** | `status ∈ {observed, example, seed}`. **observed →** renders (`●`); **example →** empty-state teaching only; **seed →** excluded from real-user view (`○` dev-only). `source?` = the HOST People-tier (below). |
| `meta` | str | secondary line ("blocked by PR #123 · 2d") |
| `attention` | score/recency | drives **attention-first** ordering (the only sort) |
| `ref` | link/id | navigate to the entity |

**Why `lifecycle_state = {label, tone}` (the one refinement to your facet list)**: states are type-specific (WorkItem: blocked/in-progress/in-review/done; Document: draft/in-review/final; Conversation: active/idle/resolved; Person: see below). Rather than a shared enum forcing all types into one vocabulary, the **surface needs only label + tone** — so PPM defines real states per type and the badge renders consistently without surface rework. Recommended per-type vocab attached as a starting point; PPM finalizes.

## The People entity — extra facets (per #1217 + HOST's two inputs)

People is the long pole (no backend yet) and the most trust-loaded. Three People-specific facets on top of the base:
1. **`personhood_type ∈ {human, agent, stakeholder}`** (#1217) — the typing that backs the ethics floor's ask-and-learn AND drives the card ("stakeholder (human)"). Lifecycle for People = *relationship state* (`awaiting-reply / recently-active / new`), tone-mapped.
2. **Inspectable + editable (HOST auditability)** — the People view in Radar must let PM **see and correct** the map (wrong type, wrong person). Opaque memory ≠ trustworthy memory. So the People surface is read+edit, not read-only. (Surface: CXO; the editable model: PPM.)
3. **Source-provenance for consent-tiering (HOST BYOC asymmetry)** — `provenance.source ∈ {principal_introduced, other_user_context}`. At single-user (now) all are `principal_introduced` — clean. At BYOC Scale-1, **only surface the `principal_introduced` tier to PM**; third parties named in *other users'* conversations are not surfaced to PM's People view. (A line for Arch's ADR-068 consent section, per HOST.) Not a Phase-2a blocker; bake the field now so the tier exists when needed.

## #1164 privacy toggle placement (your open Q)

It's a **session-level control, not a per-card one** — "Start private session" means *don't observe this session into my Radar/Layer-2.* So: place it at the **session/chat level** (the composer or chat header, where the session lives), with its effect **visible in Radar** — a quiet "Private — this session isn't being added to your Radar" state. Mechanically it's the provenance gate: a private session produces **no `observed` entities** → nothing surfaces. So #1164 isn't a separate feature; it's a switch on the provenance pipeline. Fold it into #1236 as you planned.

## Sequencing — concur, with the honest critical-path flag

Your order is right (Conversation ✅ → Document → WorkItem → People). But "ship all four for beta / no partial ship" changes the critical path: **People (PPM entity-model) and WorkItem (#1233 identity) are the long poles, and they can't be last-and-slip.** So the honest sequencing is: build Document now (you can), **and start People's entity-model + #1233 in parallel immediately** — because the beta gate is all-four, the long poles set the date. Worth PM seeing that the entity-model + #1233 are now on the beta critical path.

## Endorsements
- **Umbrella tracker** ("Radar: the 4 EntitySources" under #1090): **yes** — it's exactly the surface↔backend drift-stopper #1217 flagged. PM authorizes the carve (board op); I support the shape.
- **~20-min contract-freeze pairing**: yes — but this memo freezes the CXO side, so the pairing is mostly you + PPM on the *model* (states per type + People model). Ping me if any facet semantics need a live pass.

**Net: the CXO side is frozen — Lead, this should unblock the sources build. PPM, the model side (per-type states + the People entity-model incl. personhood_type + source-provenance) is the remaining gate.**

— CXO, 2026-06-15
