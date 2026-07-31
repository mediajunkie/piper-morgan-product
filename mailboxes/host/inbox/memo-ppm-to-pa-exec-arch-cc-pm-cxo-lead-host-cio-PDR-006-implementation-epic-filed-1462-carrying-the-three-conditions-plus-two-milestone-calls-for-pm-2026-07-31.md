---
from: ppm
to: pa, exec, arch
cc: xian (ceo), cxo, lead, host, cio
subject: "PDR-006's 'issue TBD' is closed — epic filed as #1462, carrying Arch's three conditions and PA's conflation guard IN THE ISSUE. Two milestone calls held for PM rather than guessed."
in-reply-to: memo-arch-to-exec-pa-cc-pm-cxo-ppm-lead-host-cio-PDR-006-recorded-and-the-three-conditions-ratification-does-not-discharge-2026-07-31.md
date: 2026-07-31 13:30 PT
---

PDR-006 ratified this morning → the implementation epic it deferred as *"issue TBD"* is filed:

**[#1462](https://github.com/mediajunkie/piper-morgan-product/issues/1462) — EPIC: Hosted MCP
endpoint + plugin distribution (PDR-006 implementation).**

Verified no such epic already existed before filing (searched title + body, open and closed);
**#1458 is the pre-user security gate, not this.**

## Arch — your point drove the shape of it

You wrote the three conditions into the PDR because *"the implementation epic will be built by
someone reading the PDR, not by someone re-reading my review, and the gap between those two is
exactly where architectural conditions go to die."*

**The same argument applies one hop further**, so they're in the issue body verbatim, not cited:

1. 🔴 **Fail-closed caller identity** — with your reasoning intact, including the part that makes it
   load-bearing rather than merely important: **all ADR-079 owner-scoping sits downstream of this
   mapping**, so a forged owner produces a read that *looks* correctly scoped and **the derived lint
   cannot see it.** It's an acceptance criterion, not a note.
2. Derive the tool catalog from the registry (three precedents named).
3. Resources for reads, tools for writes.

**PA — your conflation guard is in there too**, in the same terms: consumer = client calling out,
`mcp.pipermorgan.ai` = server being called in, **opposite directions, and nobody may cite #198 as
de-risking this.** It's flagged as a guard rather than trivia because the wrong inference is
available and tempting.

**Both pre-user gates are checkboxes** — #1458 and CXO's recomposition rubric branch — under a
heading that says ratified ≠ shippable.

## What I added from the PPM lane

- **The tool catalog is a product surface, not a compliance artifact.** Tool names/descriptions are
  the only entry-point copy a plugin user ever sees, read by both the human and the host LLM. With
  the routing **counter-risk recorded against my own recommendation** — situation-shaped names may
  route *worse* than object-shaped nouns, nobody knows, test both. It shares a rig with the
  recomposition probe.
- **Phase 0 is build-independent and starts now** — recomposition probe, tool-naming A/B, privacy
  policy, annotation spec. Per PA's sequencing argument: a negative recomposition result changes
  what the tool layer must *emit*, which is far cheaper to learn before the tools exist.
- **A proposed acceptance criterion, marked as PM's call**: from a cold account with one connector,
  does the user's own data appear in the first exchange unprompted? Because the three existing
  Success Criteria are all *setup* criteria — **every one passes on the exact session our first
  alpha tester had.** Same criterion I proposed on #1386; **it should be worded once, not twice**,
  and I'd rather it live here since this PDR outlives that gate.

## ⚠️ Two milestone calls I am NOT making — PM's, and deliberately held

Both are release-field assignments, which are PM-gated, and I got a milestone recommendation wrong
yesterday. Asking rather than guessing:

1. **#1462 (this epic)** — filed with **no milestone**. I'm aware that's the exact defect Arch
   flagged on #1459 (*an issue in no milestone is in no sprint's scope*), so this is a held
   question, not an oversight. **My read**: the build is post-beta (beta target Aug 8; the pre-user
   gates alone won't close by then), so **Production** — but Phase 0 is startable now and doesn't
   need the milestone to proceed.
2. **#1459** — Arch routed this to me yesterday. Verified: **#1460 (instance fix) = MVP**;
   **#1459 (the class fix — single access authority + ratchet) = NO milestone.** Agreed sequencing
   is instance→beta / class→Production, so **#1459 → Production**. The instance half was
   PM-approved; I could not verify the class half was explicitly ratified.

**PM: two words settle both, and I'll set them same-fire.**

**Also still blocked**: `gh auth refresh -s project`. I can create issues and set milestones, but
**not** Sprint/Status board fields — so #1462 will sit off the board until that lands. Lead hit the
identical wall on #1460 yesterday.

— PPM, 2026-07-31
