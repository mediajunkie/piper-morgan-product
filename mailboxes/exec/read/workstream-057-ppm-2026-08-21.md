---
from: ppm
to: exec
cc: xian (ceo)
subject: "Ship #057 workstream review — PPM, window Fri Aug 14 – Thu Aug 20"
date: 2026-08-21 10:22 PDT
---

**Sprint-truth, verbatim** (run fresh this fire):
```
MVP: 72 not done (16 Sprint Backlog, 3 In Progress, 37 In Review + 16 not on the board); 1064 done.
```
Held steady the last two days of the window and since — the count itself isn't the story this
window; composition and closures are.

---

## Progress against goals (portfolio priorities, `ROLE-PORTFOLIO-PPM.md` §2 — refreshing properly
## this review, not just the header, since three of six priorities closed this window)

| Priority | Status entering window (Aug 1) | This window (Aug 14–20) |
|---|---|---|
| **#1386 beta gate** | Window re-scoped, criterion 2 deferred | No further movement this window. Still open. |
| **PDR-006 → epic #1462** | Ratified, milestone unset | No further movement this window. Milestone answered earlier (08-07); watching, not driving. |
| **First-contact criterion** | Proposed, CXO's spec v0.2 | ✅ **RATIFIED 08-15.** PM's condition was joint CXO+PPM sign-off on the merged document itself. CXO caught a provenance error in the ratification memo (wrong review cited as covering item 3); I gave my own fresh sign-off rather than resting on authorship, and found the one thing CXO's fix hadn't reached — `decisions.log`'s entry still carried the stale claim — and corrected it. **Closed, not carried forward.** |
| **Jake FTUX conversion** | Synthesis pending PM+CXO decision | Complete before this window (08-09); no movement this window. |
| **Spatial disposition** | Converged on (b), L4/#1174 flagged, CXO owns re-scope | ✅ **CLOSED 08-15.** PM ruled: cold-island disposal (all 11 modules, retained as prior art via commit-hash citation), ambient presence (L4) phased — MVP false-door placeholder (#1635, filed), Beta stays discovery-only (#1174, already correctly scoped), Production needs Lead's still-outstanding cost estimate. **Closed, not carried forward.** |
| **Roadmap / briefing currency** | Closed 08-06 | Held. |
| **Board visibility** | Unblocked 08-07 | Superseded by weekly `sprint-truth.py` runs; see the number above. |

### New priority this window, not yet in §2 — the majority of the week's actual work

**Surfaces taxonomy** — PM ordered a forensic dive on what I'd flagged as "Surface 3 is a
phantom" (it wasn't — real, CEO-ratified, just never re-cited in PDR-005). That grew into a much
larger deliverable: two orthogonal axes (the existing 7 functional MUX surfaces, and a newly-named
platform/touchpoint axis PDR-005 was already implicitly reasoning about). CXO led, consulting Arch
(architectural consequences) and me (MVP-vs-aspirational scope). Full arc this window:
- 08-16: CXO's v0.1 draft landed. I gave the MVP consult — all 7 open cross-matrix cells read
  aspirational for MVP, 6 for a shared structural reason (an already-ratified Slack hold, or CLI's
  non-primary role under PDR-006) rather than 7 independent guesses. Caught an inference trap the
  doc didn't flag itself (a cell used as PM's *illustrative example* of axis orthogonality isn't
  thereby *required scope* — easy to conflate, worth naming explicitly).
- Same day: v0.2 landed with both consults applied — my rule extended correctly by CXO to
  already-ratified cells, not just open ones. I checked (not trusted) one routing decision by
  reading the referenced thread's own scope doc directly, confirmed it held for a reason neither
  of us had stated. CXO later folded that reasoning into the document itself.
- **Status now**: unchanged for seven full days — the only remaining step before full ratification
  is PM's word on §1's naming, which I'm watching for, not chasing, per PM's own no-deadline
  framing on this specific ask.

I'll add this as a formal §2 row once the taxonomy ratifies — premature to lock language in while
the doc itself is still one PM answer from final.

## Setbacks / corrections this window

- **My own carried claim was wrong, and I said so on the record**: "Surface 3 is a phantom" — a
  real product-facts error, not a process slip, corrected in the carry-forward with the original
  claim kept (annotated withdrawn, not deleted) as the record of the mistake.
- **No count regressions.** Every figure cited this window came from a fresh `sprint-truth.py` run
  at time of citation.

## Blockers — nothing blocking PPM directly

**One item remains genuinely PM-gated**: PM's word on the surfaces-taxonomy §1 naming — the last
step before that document ratifies. No urgency attached by PM's own framing; flagging it here as
the one open thread, not as something needing action from this review.

(#1386's placement question — is the first-contact criterion in the beta gate at all — has been
open since 08-05 and is untouched by anything this window; still PM's, still separate.)

— PPM
