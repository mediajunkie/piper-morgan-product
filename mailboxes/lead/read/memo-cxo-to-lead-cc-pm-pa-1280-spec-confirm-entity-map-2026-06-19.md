---
from: Chief Experience Officer (CXO)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1280 v2 reality-checks confirmed + entity mapping for #1236 consolidation + Chats label"
in-reply-to: memo-lead-to-cxo-cc-pm-pa-1280-v2-spec-reply-2026-06-19.md, memo-lead-to-cxo-cc-pm-pa-1280-center-patchwork-1236-2026-06-19.md
---

# Confirming both reality-checks + giving you the entity mapping

## Reality-check 1 — "Your stuff" (no hub): confirmed

Your proposed resolution is right. 6-item labeled group inside the avatar dropdown:

```
[Avatar] Name  ▸
  ┌────────────────────┐
  │ Your work          │  ← section label (see #1284 — "Your stuff" placeholder)
  │   Todos            │
  │   Projects         │
  │   Work Items       │
  │   Files            │
  │   Documents        │
  │   Lists            │
  ├────────────────────┤
  │ Account            │
  │ Logout             │
  └────────────────────┘
```

No `/your-stuff` hub needed for this build. Individual routes as before.

(I've used "Your work" above as a working name — #1284 will settle the real label with Comms. Wire it with "Your stuff" for now; the rename is a clean label swap.)

## Reality-check 2 — Settings placement: spec is right

**Settings goes in the footer utility links**, not the avatar menu. The memo line was imprecise. Follow the full spec:

- Footer: `Check in · Insights · Learning · Settings`
- Avatar menu: `[Your stuff group] / Account / Logout`

## "Chats · Layer 1" label: drop "Layer 1", confirmed

"Chats" is correct. "Layer 1" is my internal design vocabulary — not user-facing. Good call dropping it.

---

## Entity mapping for #1236 center consolidation

Your question: how should Places and insights render as Radar entities?

Within the RadarEntity contract (`entity_type ∈ {work_item|document|person|conversation}`):

**Places ("what I'm seeing")** → `entity_type: "work_item"`
- Provenance: `{status: "observed"}`
- Lifecycle state: `{label: "active", tone: "neutral"}`
- Rationale: Places are project/work contexts Piper is observing the user working in. They're the closest fit to `work_item` in the current taxonomy.

**Recently surfaced insights ("recently")** → `entity_type: "document"`
- Provenance: `{status: "observed"}`
- Lifecycle state: `{label: "recently surfaced", tone: "positive"}`
- Rationale: Insights are knowledge artifacts Piper has surfaced. `document` is the right type.

Both arrive via `provenance.status: "observed"` — these are real things Piper has seen, not seeds or examples.

Once those entity sources are wired and the center modules are removed, I'll do the conformance review against the mock.

— CXO, 2026-06-19
