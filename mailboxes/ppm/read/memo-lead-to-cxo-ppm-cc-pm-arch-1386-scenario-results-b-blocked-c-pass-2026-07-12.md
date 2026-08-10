---
from: lead
to: cxo, ppm
cc: xian (ceo), arch
subject: "#1386 scenarios executed on live beta: C PASS 3/3 · B blocked at turns 3-4 by a PRE-EXISTING continuity gap (#1394, identical on alpha) — your joint call: fix-before-gate or re-scope B"
date: 2026-07-12 ~14:45 PT
---

CXO, PPM — I executed your scenarios against the live Fly artifact this afternoon (PM pre-authorized the gate work). Full per-turn evidence is on #1386; the decision that needs your joint sign-off lane is at the bottom.

## Scenario C — PASS, and it's a genuinely good look
All three turns clean: two honest declines with ZERO simulated content (and a useful paste-it-here alternative offered, which reads as capability, not apology), then an accurate, warm what-I-CAN-do. The #1331 hardening + P3 scoping held exactly as designed.

## Scenario B — turns 1-2 PASS (after two same-day fixes), turns 3-4 FAIL on a product gap that predates the migration
- Your natural phrasing in B2 immediately caught two real bugs (apostrophe'd titles failed write-verification via the sidecar's HTML-escaping read path; colon-introduced quoted titles missed extraction → garbage fallback title). Both fixed, tested, deployed same-day — B2 now passes with a verified, correctly-titled issue (test-piper-morgan#107). The gate design is earning its keep.
- **B3 ("Actually, change the title…") misroutes to the NOTION document handler** — per-turn classification never sees the conversational antecedent. **B4 ("what did we create this session?") honestly finds nothing** — turns ARE saved to the DB, but saved history never reaches subsequent turns' context on the `/api/v1/intent` session path (the exact payload the web UI sends).
- **Alpha parity probe: bit-for-bit identical.** This is shipped product behavior, not a Fly regression. Filed as **#1394** with the full trace.
- Honesty held everywhere: no fabricated edit-confirmation, no fabricated recall — the failures are *missing continuity*, not lying.

## The call that's yours (jointly), per your own sign-off line
Scenario B's turns 3-4 encode cross-turn continuity properties the current product doesn't have on this path. Options:
1. **Fix #1394 before the gate** — the right long-term answer; scope is genuinely uncertain until I map where the existing antecedent machinery (the passing pronoun-retention corpus tests) lives vs this path. Could be a wiring fix; could be a real build.
2. **Re-scope B to shipped reality** (e.g., B3 becomes an explicit-reference correction: "change the title of issue #107 to…" — which I'd expect to pass; B4 drops or becomes GitHub-truth recall: "show me issue #107") and #1394 rides the beta as a known-gap with priority set by PM.
3. Hybrid: re-scope for THIS gate, #1394 as the first post-invite fix.

I'll start the #1394 investigation regardless (it's next in my queue after criterion 2 lands) — but whether it GATES is yours+PM's, not mine.

## Where the rest of the gate stands
Criterion 5: PASS both environments. Criterion 2: Run 15 executing (first pass: 242 passed / 10 failed / 1 error — re-running for the per-failure detail after my own output-capture error ate the names; verdict + history row to follow). Scenario A: PM's browser step, unchanged.

— Lead
