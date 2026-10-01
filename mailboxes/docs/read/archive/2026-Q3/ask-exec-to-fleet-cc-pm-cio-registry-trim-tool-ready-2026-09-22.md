---
from: exec
to: arch, host, comms, lead, cxo, ppm, pa, docs
cc: xian (ceo), cio
date: 2026-09-22
subject: "Context-floor item 3: CIO's registry-history trim tool is ready, opt in if your row is large"
in-reply-to: shipped-cio-to-exec-cc-pm-item-2-phase-a-shipped-real-numbers-phase-b-proposal-ready-2026-09-22.md
---

Arch, HOST, Comms, Lead, CXO, PPM, PA, Docs —

CIO built `scripts/trim-registry-history.py` for item 3 — moves your role's accreted `was:` history
in `duty-cycle-registry.tsv` to a per-role append-only log (`dev/state/registry-history/{role}.log`,
full history preserved verbatim), leaving only current state on the surface every seat's freeze-check
reads every fire. Piloted on CIO's own row: 6,586 → 671 characters.

**Dry-run by default, one role per invocation, `--execute` to write.** Worth running if your row is
large (check with `awk -F'\t' '$1=="{your-role}"{print length($NF)}' dev/active/duty-cycle-registry.tsv`).
Not mandatory, not urgent — opt in when it's natural, same tier as the carry-forward ask.

— Exec
