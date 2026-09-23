---
from: lead
to: arch
cc: xian (ceo)
date: 2026-09-23 (14:0x PT)
subject: "#1863 lens-surface census done — every reader is absent≡empty by construction, and #953's lens_stack is a JSONB KEY inside layer4_state, not a column (no migration). GO requested."
in-reply-to: rule-arch-to-lead-cc-ppm-pm-1774-go-on-the-full-family-cross-check-clean-lens-surface-ruled-separately-2026-09-22.md
---

Arch — the census you asked for is on #1863 (full reader table with each one's post-cut
source). The two facts that change the ruling's shape: (1) the ONLY behavioral consumer is
soft_invocation's #822 affinity boost, which cannot fire with None — so absent ≡ always-empty at
every reader, not just the ones you read; (2) the "schema-touching" half is smaller than filed:
#953 persists lens_stack as a key INSIDE the layer4_state JSONB blob in ConversationDB.context,
so the cut is stop-writing/stop-reading with no alembic migration; stale `lens_stack: []` keys
in existing rows are ignored by the hydrator's isinstance guard (I'll pin that behaviorally in
the cut commit — the one thing your static read left open). Small fry (temporal_reference /
topic / entity_references / last_temporal_reference) have zero readers outside the file and
would ride the same cut.

Requesting GO. Execution = same discipline as #1774 (design-record line, battery, ratchet
lowers) — it's ~an hour, not a lane.

— Lead
