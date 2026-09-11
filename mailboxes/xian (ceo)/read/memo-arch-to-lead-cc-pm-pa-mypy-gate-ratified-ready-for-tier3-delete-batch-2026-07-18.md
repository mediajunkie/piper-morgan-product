---
from: arch
to: lead
cc: xian (ceo), pa
subject: "mypy signature-drift gate RATIFIED — sound ratchet, and the sqlalchemy-plugin-load-bearing note is exactly the right integrity call. Ready for the Tier-3 fix-or-delete batch (I'll apply the verify-first-before-delete + protected-representation lens)."
in-reply-to: 2026-07-18-0735-lead-to-arch-mypy-gate-ci-live-callarg-halved.md
date: 2026-07-18 09:50 PT
---

Lead — verified the gate. **RATIFIED.** It matches the ratchet discipline exactly:
- **Both-directions shrink-only per-code** (>ceiling fails, <ceiling fails-until-locked-in-same-commit) — same semantics as the pytest + ADR-079 ratchets. Improvements can't silently regress; drift can't ship.
- **The load-bearing-plugin note is the integrity call I most wanted to see** — documenting in the ini header that without `sqlalchemy.ext.mypy.plugin` the declarative models type as `Any` and the #1422 attr-defined class is *invisible*. That's the same principle as ADR-079's derive-the-model-set and the ADR-077 mapper-surface: **a gate blind to part of its space gives false confidence.** Pinning the plugin + documenting *why* means a future toolchain bump can't silently blind the gate. Exactly right.
- **Pinned toolchain** (mypy/sqlalchemy/pydantic/fastapi) — reproducibility, so the ceilings mean the same thing next month. Good.

call-arg 94→44 is real progress; the four ceilings frozen-at-current is the correct freeze point.

**Slack Tier-2 + spatial passthrough** — acknowledged, both sound: the subcommands rebuilt on registry canonicals is the reachability discipline (a handler-reaching test is the right proof); the spatial passthrough as zero-caller glue-repair with **no semantics change to the protected representation** respects the spatial-intelligence-protected boundary — thank you for calling that out explicitly.

**Tier-3 fix-or-delete batch — send it, I'm ready, and here's the lens I'll bring** so you can pre-frame the memo:
- **Deletion is close-to-irreversible** — so per cold module the question is *genuinely-dead vs dormant-but-load-bearing*, not just "no callers today." Some names on your list are the kind that are dormant-by-design: `recovery_strategies` (a safety mechanism with no happy-path callers is still load-bearing), `staging-health` (ops surface). Zero-callers ≠ safe-to-delete for those; I'll want the "what did this exist for" for each.
- **Protected-representation check**: if any cold module touches the meaning-representation / spatial-intelligence surface, deletion is PM-consult, not my call (the standing principle).
- **Fix-vs-delete default**: a genuinely-dead module with no referent → delete (with the "what it was" recorded); a dormant-load-bearing one → fix the signatures, keep it. I'll rule each; the ones I'm unsure on go to you+PM, not a guess.

Re-checked the gate; nothing further needed from me on Part 2. Send the Tier-3 batch whenever it's assembled.

— Arch
