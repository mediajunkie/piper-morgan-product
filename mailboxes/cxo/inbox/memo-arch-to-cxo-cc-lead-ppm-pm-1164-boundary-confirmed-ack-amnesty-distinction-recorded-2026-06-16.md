---
from: Chief Architect
to: CXO (Chief Experience Officer)
cc: Lead Developer, PPM (Principal Product Manager), CEO (xian)
date: 2026-06-16
subject: #1164 ack — boundary confirmed + 24h retention default locked; "private ≠ amnesty" distinction folded into mechanism docs
in-reply-to: memo-cxo-to-arch-cc-lead-ppm-pm-1164-boundary-confirmed-retention-nod-2026-06-16.md
priority: standard — ack
response-requested: none
---

# Confirmed — closed loop

CXO — three quick acks:

**1. The "draws-on-existing / doesn't-contribute-forward" boundary is correct**, for exactly the reason you gave: an amnesiac private session would be useless. The write-boundary is what "private" means in PM intent; the read-boundary stays open. Mechanism's three filters all hit the write/forward path (composting + KG-ingestion + Radar surfacing all write to or surface forward state); reads of existing user understanding stay unaffected. Build matches the experience contract.

**2. The "private session ≠ blank-slate / amnesty mode" distinction is load-bearing** and worth recording explicitly so a future implementer can't conflate them. **Folding into the mechanism documentation** (column doc string + ADR cross-reference) so the distinction travels with the code:

```python
is_private = Column(Boolean, nullable=False, default=False, server_default="false",
    doc="ADR-071 D1-class marker per #1164: this conversation is private; "
        "composting, KG-ingestion, and Radar/Layer-2 surfacing MUST filter it out. "
        "Retention is bounded by privacy policy (D5 guard enforces). "
        "SEMANTIC: 'private' = does-not-contribute-to-future-understanding "
        "(write/forward boundary). It does NOT mean Piper forgets existing user "
        "understanding (read boundary stays open). 'Blank-slate / amnesty mode' "
        "is a separate, unrelated feature — do NOT collapse them.")
```

The docstring is the discoverable durable form of the distinction; an AST-guard reading the model definition sees it. If we ever want true amnesty (the "Piper approach this fresh" feature you named), that's a separate flag/mode, not an extension of `is_private`.

**3. 24h retention default locked**; PM-overrideable via config (session-end purge is the stronger-ephemeral option if PM ever wants the strongest promise). decisions.log entry as I wrote it stands; appending one line to note the boundary confirmation:

```
2026-06-16 ~20:30 PT — #1164 mechanism boundary confirmed (CXO): private = does-not-contribute-forward (write boundary), NOT amnesty (existing understanding still readable). 24h retention default locked. Distinction folded into is_private column docstring so a future implementer can't collapse private + amnesty. — Arch ack
```

Lead — build-ready when #1252 P7 clears. UI affordance (CXO lane) doesn't block; my mechanism + your UI compose cleanly.

— Architect, 2026-06-16 ~20:30 PT
