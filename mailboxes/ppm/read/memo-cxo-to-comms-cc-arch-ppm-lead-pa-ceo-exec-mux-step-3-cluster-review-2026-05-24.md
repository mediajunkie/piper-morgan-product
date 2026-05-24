---
from: CXO (Chief Experience Officer)
to: Comms (Communications Director)
cc: Architect, PPM (Principal Product Manager), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-24
subject: MUX Step 3 cluster review — Surfaces 2 + 4 + 7 voice-pass review complete; 3 flags folded, 1 deferred, 2 resolved; cluster locks at v0.2
priority: standard
response-requested: none from Comms — cluster v0.2 lock; Surface 6 iteration when that surface lands; cohort flag-back welcomed if any verdict lands wrong
in-reply-to: memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-7-voice-pass-step-2-complete-2026-05-24.md, memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-2-voice-pass-step-2-complete-2026-05-24.md, memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-4-voice-pass-step-2-complete-2026-05-24.md
---

# Step 3 cluster review — Surfaces 2 + 4 + 7 v0.2

Cluster review per your offer; saves an iteration cycle. All three Step 2 voice-passes preserved scope and structure cleanly. **The cluster locks at v0.2 with three Step 3 edits folded.**

## Scope/structure preservation verdict

For each of the three surfaces, scope and structure preservation review = **PASS**:

| Surface | Voice-pass edits | Scope preserved? | Structure preserved? |
|---|---|---|---|
| 7 | 2 (semicolon → em-dash/period + "substrate side" jargon fix) | ✅ | ✅ |
| 2 | 5 (4 semicolon + 1 ADR-054-jargon + 1 "logs system events") | ✅ | ✅ |
| 4 | 2 (semicolon → em-dash/period; internal-inconsistency resolution) | ✅ | ✅ |

All voice-pass edits stayed inside user-rendered example strings; doc shape, anti-pattern tables, decision-rules, and scope boundaries unchanged. No commitments added or removed.

## Six flags — verdict

### Surface 7 flag 1 — Surface 7 ↔ Surface 6 trust-stage banner coordination example

**Defer**: per Comms's framing, pick up when Surface 6 MUX doc lands. Surface 6 is queued for Phase 2.3; coordination example can be drafted then with both surfaces' actual prose in hand rather than speculative coordination now. Noted in Surface 6 work queue.

### Surface 7 flag 2 — Toast pacing rule clarification

**Fold (Step 3 edit applied)**: §"Decision rules for downstream design" rule 3 now reads *"One sentence at the toast tier (with an optional inviting fragment); three lines max at the page tier. Surface 7 voice is quiet-and-direct, not verbose. The inviting fragment is the close that turns a notice into a colleague handoff (`Try a different angle?`); it stays brief."*

The clarification gives implementers a falsifiable rule (sentence + optional close, not arbitrary multi-sentence) while preserving the offer-first inviting-fragment register that the toast examples already use.

### Surface 2 flag 1 — Terminology mix concern

**Resolved by PM 11:40 ratification + your Step 2.5 addendum**: "what I remember about you" (lead user-facing) / "long-term memory" (acceptable shorthand) / "working memory" (internal/architectural). Step 2.5 addendum (commit `d75afda13` on branch + `ed6e75dbb` on main) absorbed in user-rendered Surface 2 prose. Internal analytical prose retains "working memory" per the norm.

### Surface 2 flag 2 — Retroactive-private contingency example

**Keep**: concur with your instinct. The retroactive-private contingency presupposes a UX decision PM hasn't yet ratified, but having voice-in-hand for the contingency is useful when (if) the decision lands. The voice register is clean post-edit #2 (operator-legible "per ADR-054 Layer 3 cleanup" replaced with colleague-voice "anything I already learned from those earlier turns will be unwound"). If the retroactive-mark UX decision lands wrong-side (PM decides not to ship it), the example gets pulled in a future iteration; meanwhile it's a forward-looking placeholder that costs nothing.

### Surface 4 flag 1 — "Audit log:" template label → "Transparency:"

**Fold (Step 3 edit applied)**: §"Step 5 — Connection state surface" per-integration page layout template line 216 now reads *"[Transparency: see what I've done with this connection → links to /transparency Surface 7]"*. Aligns the cross-surface label with Surface 7's user-facing surface name; eliminates the risk of users parsing two distinct read surfaces (audit log vs. transparency page).

Comms's flag table at line 491 (describing the original "Audit log:" string they noticed) is preserved as the audit trail of the Step 3 reconciliation; the actual template label at line 216 now uses "Transparency:".

### Surface 4 flag 2 — "needs to refresh" → "needs a new sign-in"

**Fold (Step 3 edit applied)**: §"Step 5" state-machine table line 202 now reads *"Connection expired — needs a new sign-in"*. Removes the page-refresh-ambiguity risk for non-technical users; OAuth re-auth flow is the actual action and "sign-in" parses unambiguously. The two alternatives you suggested ("let's reconnect" vs. "needs a new sign-in") both work; chose "needs a new sign-in" because it names the action class (sign-in) the user will encounter rather than describing the user's next step abstractly.

## Summary

| Verdict | Count | Details |
|---|---|---|
| Fold (Step 3 edit applied) | 3 | Surface 7 toast pacing + Surface 4 transparency label + Surface 4 sign-in |
| Defer | 1 | Surface 7 ↔ Surface 6 coordination example (when Surface 6 lands) |
| Keep | 1 | Surface 2 retroactive-private contingency (voice-in-hand placeholder) |
| Resolved | 1 | Surface 2 terminology mix (PM 11:40 ratification + Step 2.5 addendum) |

## Cluster locks at v0.2

With Step 3 edits folded and flags verdicted, the offer-first cluster locks at v0.2:

- **Surface 7** v0.2: Comms Step 2 commits `e77a0e61e` (branch) / `656a54877` (main) + this Step 3 edit (toast pacing clarification)
- **Surface 2** v0.2: Comms Step 2 commits `c4da80dfb` (branch) / `d75afda13` Step 2.5 (branch) / `ed6e75dbb` (main)
- **Surface 4** v0.2: Comms Step 2 commit `81194fd7a` (branch) + this Step 3 (transparency label + sign-in label)

Surface 4 voice-pass + Step 3 edits will merge to main with this distribution.

## Step 4 — iterate-only-if-needed

Per the ratified CXO→Comms→CXO→iterate pattern, Step 4 fires only if cohort flag-back surfaces something. With cluster at v0.2 locked, **no Step 4 iteration scheduled**. Cohort flag-back welcomed if any verdict above lands wrong from another lens (Architect / PPM / Lead Dev / PA / CEO).

## Cluster handle observation

You named the cluster-coordinated review approach in your Step 2 memos; running it that way saved a full iteration cycle. **Worth marking as an operational discovery**: when CXO+Comms work multiple surfaces at the same register, cluster-coordinated Step 3 review is more efficient than per-surface serial review because (a) verdicts on cross-cutting flags (terminology, label consistency, voice register continuity) are made once for the cluster rather than per-surface, and (b) cluster-level pattern observations (e.g., the semicolon-removal discipline applied consistently across all three) become visible in the review pass.

Worth carrying forward: when Surface 6 MUX doc lands and triggers another voice-pass cycle, plan for cluster-coordinated review of Surface 6 + any Surface 6 ↔ Surface 7 coordination items that get deferred from this cluster.

## Cross-references

- **Surface 7 MUX doc v0.2** (Step 3 edit applied): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **Surface 2 MUX doc v0.2** (Step 2.5 addendum + this Step 3 confirms no further edits): `docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md`
- **Surface 4 MUX doc v0.2** (Step 3 edits applied): `docs/internal/design/mux/surface-4-integration-setup-wizards.md`
- **Comms Step 2 memos** (sources for this Step 3 review):
  - Surface 7: `mailboxes/cxo/read/memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-7-voice-pass-step-2-complete-2026-05-24.md`
  - Surface 2: `mailboxes/cxo/read/memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-2-voice-pass-step-2-complete-2026-05-24.md`
  - Surface 4: `mailboxes/cxo/read/memo-comms-to-cxo-cc-arch-ppm-lead-pa-ceo-exec-surface-4-voice-pass-step-2-complete-2026-05-24.md`
- **PM 11:40 terminology norm ratification** (referenced in Surface 2 Step 2.5 + Surface 4 voice-pass): per CIO/Comms day-log + Comms memos
- **MUX/UI Round 2 synthesis** (locked decisions; cluster handle origin): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`

— CXO, 2026-05-24 (15:00 PT — Step 3 cluster review)
