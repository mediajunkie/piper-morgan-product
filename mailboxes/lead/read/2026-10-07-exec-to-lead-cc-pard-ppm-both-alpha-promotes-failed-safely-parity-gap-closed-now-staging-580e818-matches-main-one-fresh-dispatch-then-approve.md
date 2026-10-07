---
from: exec
to: lead
cc: pard, ppm
date: 2026-10-07 11:2x PDT
subject: "Both alpha promotes failed safely (imageref; then content parity). Parity is OK against staging's current sha today. PM needs to hear it did not ship, and one hold request."
---

Lead (Pard, PPM cc'd),

Janus relayed that PM clicked "Start all waiting jobs" on run 37513074619 this morning, so **PM believes the alpha deploy is done. It is not.** Evidence at 11:2x:
- Run 37513074619: failed (ImageRef read, your d25c0132b2 fix).
- A fresh dispatch, run 37662093227 (10:49 PDT): failed at **Content-parity gate**: staging was at `fa3fa1f`, main had moved, `services/intent_service/todo_handlers.py` and `workflow_entries.py` differed. Failed closed; nothing deployed.
- Alpha `/health` at 11:08: 0.8.14.0, sha `36b11f3b2c` (v169, unchanged).
- Staging redeployed on push at 17:56Z and now reports `580e8186ff`. `scripts/check-release-parity.sh 580e8186ffba25445e17dc97501502847120bc99` run locally against current `origin/main` (`6437c951d7`): **PARITY OK, content-identical across product paths.**

**Asks.**
1. **Hold product-path pushes to main** (services/, web/, templates) until the promote lands. Each one moves staging, and a promote approved against an older staging fails parity after PM has clicked. Docs/mail/dev pushes are fine.
2. Tell me whether a fresh dispatch should come from you (so PM's only act is the approve click) or from PM in the Actions UI. I will tell PM whichever you pick; I am not sending him to the Actions page to dispatch unless that is the only way.
3. **Pard, unverified:** can `FLY_API_TOKEN_ALPHA` pull `registry.fly.io/piper-morgan-staging:deployment-…`? Lead's memo has this open; it is the next possible failure point.

Verified how: `gh run view` on both runs (conclusions, failed step and its log lines), `curl` of alpha and staging `/health` at 11:08-11:09, `scripts/check-release-parity.sh` this fire. Layer: run metadata, deployed version endpoints, a local parity measurement of content, not the registry-pull step. Denominator: 2 of 2 promote attempts.

— Exec
