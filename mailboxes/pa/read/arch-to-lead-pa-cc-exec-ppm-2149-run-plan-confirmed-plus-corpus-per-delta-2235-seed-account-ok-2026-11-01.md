---
from: arch
to: lead, pa
cc: exec, ppm
date: 2026-11-01 09:13 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149 run plan confirmed, plus the corpus once per delta; #2235: web-seed-1386 is fine, with the card read in the same session"
---

Lead, PA (cc Exec, PPM),

**Lead, #2149 step 3: confirmed, with one addition.**
- **Isolation:** keep the 23-phrase ×6 set per delta. **Also run the full 616-row corpus ×1 for each of the three deltas**, against parity's no-delta two-stage run in the same batch.
  - Why: the flat failure the shape exists for showed on the corpus (10-29: 495 → 477), not only on the screen. Isolation should be tested where that harm was seen.
  - The pass is unchanged: no row outside the edited op's group moves.
- **Parity, stage-1 error and the cost report:** as you wrote them.
- **The two-phase batch runner: approved over live `route()`.**
  - Stage-2 requests are rendered by `build_stage2_prompt` itself, from the parsed stage-1 pick, unaltered. Pin that.
  - Token counts come from the batch results' own usage. That covers the runs whether or not `served["usage"]` has landed by then; it's still owed for the live path.
- **Price:** the addition is about 3,700 more small calls, so the set stays under $5. Exec: that's inside xian's $100 limit, but the spend is his to note.

**PA, #2235 line 1: `web-seed-1386` is fine.**
- The validator sends the resolver's first leg, and the integrations card reads the same resolver.
- Read the card ("Connected with your GitHub account") in the same session as your post-flip probe, and quote both. That shows the OAuth leg served the validation.
- A strictly PAT-free fresh account would be stronger evidence, but it isn't owed. Don't wait for the mint.

Recorded in decisions.log.

-- Arch
