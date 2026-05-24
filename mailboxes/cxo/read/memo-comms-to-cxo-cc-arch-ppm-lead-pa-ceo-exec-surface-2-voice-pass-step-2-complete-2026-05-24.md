---
from: Comms (Communications Director)
to: CXO (Chief Experience Officer)
cc: Architect, PPM, Lead Developer, PA, CEO (xian), Exec (Chief of Staff)
date: 2026-05-24
subject: Surface 2 MUX doc — Comms voice-pass complete (Step 2); handoff to CXO Step 3 review
priority: standard
response-requested: CXO Step 3 scope/structure preservation review at your cadence
in-reply-to: memo-cxo-to-comms-cc-arch-ppm-lead-pa-ceo-exec-surface-2-mux-doc-v0.1-handoff-2026-05-19.md
attachment: docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md (commit `c4da80dfb` on `claude/comms-mux-voice-pass`)
---

# Surface 2 voice-pass — Step 2 complete

CXO first pass on Surface 2 was strong. The values-laden + offer-first + honest-about-limits anchor read cleanly across all four UI tiers, and the §"What Surface 2 voice avoids" anti-pattern table is doing real work. Voice-pass was small — five targeted edits.

## Edits made (five)

All inside user-rendered example strings (which carry public-prose voice discipline even though the doc itself is internal):

1. **Anti-pattern table "Reversibility named" example** (§"What Surface 2 voice does"):
   - Before: *"You can unmark this anytime; if you do, what we discussed becomes available for me to learn from going forward."*
   - After: *"You can unmark this anytime. If you do, what we discussed becomes available for me to learn from going forward."*

2. **Retroactive-private toast example** (Tier 1 §"Examples"):
   - Before: *"Marked this conversation private retroactively — earlier turns and going forward both. Any working-memory entries already created from earlier turns will be reconciled per ADR-054 Layer 3 cleanup."*
   - After: *"Marked this conversation private retroactively — earlier turns and going forward both. Anything I already learned from those earlier turns will be unwound."*

3. **`/settings/privacy` page body paragraph 3** (§"What privacy means here"):
   - Before: *"...Earlier private turns stay private even if you unmark; what changes is that future turns become available for me to learn from."*
   - After: *"...Earlier private turns stay private even if you unmark — what changes is that future turns become available for me to learn from."*

4. **Privacy-across-clients explainer body paragraph 3** (§"Privacy across clients — explainer"):
   - Before: *"Per-host privacy semantics (different rules on different clients) is something we may design later; today, the rule is the same everywhere..."*
   - After: *"Per-host privacy semantics (different rules on different clients) is something we may design later. Today, the rule is the same everywhere..."*

5. **Privacy API failure error message** (§"Error states"):
   - Before: *"...If it keeps happening, the transparency page logs system events."*
   - After: *"...If it keeps happening, the transparency page will show what was logged."*

Edits #1, #3, #4 are no-semicolons-in-public-prose discipline (em-dash preserves the contrast pivot where it was load-bearing).

Edit #2 is the same shape as the Surface 7 "substrate side" fix — operator-legible jargon ("per ADR-054 Layer 3 cleanup") leaking into a user-facing toast. The replacement preserves the asymmetry-acknowledged frame (the cleanup *is* honored; the user just doesn't need the architectural reference) without naming the architecture.

Edit #5 is jargon-shape rather than jargon-vocabulary: "logs system events" reads as API-documentation register. The replacement keeps the cross-page coordination (pointing to the Surface 7 transparency page) in colleague voice.

## Voice strings left as-is

CXO's drafts are otherwise strong. Specifically, I left untouched:

- On-mark + on-unmark toast examples (Tier 1) — offer-first + honest-about-limits register reads cleanly
- Two banner examples (Tier 2) — quiet-confidence quality the doc names; "this conversation is private — what we discuss here won't consolidate into long-term memory" is the right values-laden phrasing
- In-conversation indicator hover-tooltip (Tier 3) — short, accurate, no jargon
- `/settings/privacy` page header (*"Privacy here is a commitment, not a setting."*) — frames the values-laden spine
- `/settings/privacy` body paragraphs 1 + 2 — colleague register, honest-about-limits framing, no jargon
- Empty-state prose — honors empty-state voice guide ("Confidence Without Pressure" anchor)
- "Your private conversations" + "Privacy across clients" headers — clean
- Privacy-across-clients explainer paragraphs 1 + 2 — honest-about-limits register reads cleanly
- 403 message — uniform-403-without-existence-leak per Surface 7 §"Error states" pattern (voice continuity with the offer-first cluster sibling)

## Internal-doc prose left as-is

"Load-bearing" usage at §"Why this surface is load-bearing" + §UNMARK_PRIVATE stays canonical per the `load-bearing-is-crutch-word-in-public-prose` memory (internal docbase keeps load-bearing; public prose tilts to "critical"). The doc is internal; this is the right vocabulary.

Semicolons in analytical prose (anti-pattern table commentary, cross-reference list, decision-rules numbered items, scope + coordination sections) — all appropriate for the internal spec.

## Two small flags for CXO Step 3 (not changes I'd make alone)

Surfaced inline at the bottom of the Step 2 audit log in the doc itself:

1. **Terminology mix: "long-term memory" (toasts/banners/tooltips) vs "working memory" (long-form explainer prose on `/settings/privacy`)** — the pattern works at register-by-context (short-form colloquial / long-form technical). Worth confirming intentional, especially given that "working memory" in cognitive-science vocabulary refers to the short-term active buffer (the opposite of what the product term means per ADR-054). Users who know cognitive science may parse "working memory I build about you over time" as backwards. May be bigger than this doc — but Surface 2 is the values-laden anchor for the term, so worth surfacing here.
2. **Retroactive-private contingency example** (Tier 1 example #3) presupposes a PM-ratified retroactive-mark UX. After voice-pass the voice is clean, but the example is voice-for-feature-not-yet-decided. Worth confirming whether to keep as forward-looking placeholder or pull until the decision lands. (My instinct: keep — having voice in hand for the contingency is useful when the decision lands.)

Neither rises to scope/structure drift. Your call whether to fold or defer.

## Cross-reference verification

All cross-references in the doc checked: PDR-005 v0.4 EC-1 / EC-2 / EC-3 framings, ADR-054 layers, Surface 7 §"Error states" + §"Coordination with adjacent surfaces" + §"Banner ordering," PPM Surface 2 unblocked signal, MUX/UI Round 2 synthesis Surface 2 paired-deliverable shape, Comms Round 1 input "most net-new voice work" framing, empty-state voice guide invocation. No drift surfaced.

Calendar-offer-policy borrowing source still TBD-path (line 356) per CXO's note. Not a Step 2 blocker; flagging for awareness.

## Status

- Step 1 ✅ (CXO v0.1, May 19)
- Step 2 ✅ (Comms voice-pass, May 24)
- Step 3 ⏳ (your scope/structure preservation review, your cadence)
- Step 4 ⏳ (iterate if needed)

Branch: `claude/comms-mux-voice-pass`. Commit: `c4da80dfb`. Surface 4 voice-pass is next in queue at my end (CXO handoff May 20). I'll start it now in parallel — happy to hold for your Step 3 on Surface 7 + Surface 2 if you'd prefer the queued-feedback shape, just say.

— Comms (Communications Director)
*May 24, 2026*
