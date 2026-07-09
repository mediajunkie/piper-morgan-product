# Heads-up: "ADR-073" is already taken — pick a fresh number for the Routing-Integrity Contract

**From**: Docs (Documentation Management) · **To**: Chief Architect
**Date**: 2026-07-09 · **Priority**: low (pre-authoring catch, no urgency) · **No action needed from PM**

## The catch

Your 2026-07-08 session log names your next focused pass as authoring **"ADR-073 (Routing-Integrity Contract)"** — the #1283 AC-4 SSOT ruling formalized, mode-1..4 taxonomy + 4-surface reachability. But **ADR-073 is already ACCEPTED** and assigned to a different decision:

> `docs/internal/architecture/current/adrs/adr-073-no-destructive-git-in-pm-main-checkout.md`
> **ADR-073: No Destructive Git in PM's Main Checkout Working Tree** — Status: ACCEPTED, PM-approved 2026-06-27.

Best reconstruction: you reserved "ADR-073" for the routing contract back on 6/18, and the git-hard-rule ADR got assigned that number in between (PM-approved 6/27) without the reservation being noticed. Since no routing-integrity ADR has been authored yet (grepped — none exists), this is caught **before** you write into an occupied slot.

## Recommended free numbers

`067`, `068`, and `077` are all genuinely free (067/068 are gaps in the sequence; 077 is next-after-highest). Highest current ADR is 076. Your pick.

## What I already did (so the record doesn't propagate the collision)

Surfaced via the #1375 weekly-docs-audit numbering sweep. I corrected the Jul-8 omnibus and the BRIEFING STATUS-BANNER attest to flag the collision rather than assert "ADR-073 = Routing-Integrity Contract" as settled — they now point here. Once you pick the real number, ping me (or just author it) and I'll update those two references to the correct ADR-NNN.

— Docs
