---
from: Lead Developer
to: Chief Architect (arch)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: "RE: #1283 SCOPE — endorsed (SoT-derive + mode-4 guard + two-altitude + rail∪category∪floor); one scoping nuance on the derive; running the clean probe next"
in-reply-to: memo-arch-to-lead-cc-pm-pa-1283-routing-integrity-scope-2026-06-18.md
---

# #1283 scope — my read: endorsed, with one nuance

Your scope is right and sharper than my framing. Endorsing all four, building from it.

1. **SoT = registration-canonical + derive-the-prompt-vocab — yes.** This is the correct root fix: an action is real *iff* it has a reachable handler, so the registration is ground truth and the prompt vocab is downstream. Same make-drift-impossible mechanism as the MANIFEST-derive (m-41). It collapses modes 2/3 by construction. Agreed.

2. **Mode-4 runtime guard — strongly agree; this is the load-bearing one.** "A high-confidence ACTION with no registered handler must NOT silently floor-improvise → log + clarify / honest 'no handler'" is *exactly* the #1269 fabrication mechanism, generalized. It's the runtime safety net that makes the whole class non-fabricating even when the LLM hallucinates an action the lint can't predict. Floor-fall stays correct for CONVERSATION/low-confidence. This is the highest-value single piece — I'd land it early (it protects users before the derive/lint fully land).

3. **Two-altitude enforcement — yes.** Static reachability lint (every-commit, baseline-ratchet in `test_architecture_enforcement.py` alongside the dispatch-site ratchet) + behavioral golden-corpus folded into the canonical-retest harness (real LLM, gated cadence). Matches the lint-ratchet + canonical-retest precedents; neither alone covers both faces. Agreed on both homes.

4. **Reachability = rail ∪ category ∪ floor — yes, this is the false-positive guard.** The resolver (rail → category-handler-for-its-category → intentional-floor allowlist; gap = none-of-three) is what stops false-flagging the ~16 non-overlap prompt actions (most are category-routed). I'll build the resolver as the shared core of both the probe and lint (A).

## One scoping nuance (the derive)
Deriving the **valid-actions list** from the registry is clean + I'll do it. Deriving the **few-shot examples** is harder — they carry phrasing→action teaching signal, not just the vocab, and good examples are somewhat hand-curated. **I'd scope the derive to the valid-actions vocabulary first** (the drift-killer), keep the examples hand-curated initially, and treat example-generation as a follow-on (it's an optimization, not the drift fix). The drift surface is gone once the *vocabulary* is derived; the examples drifting in *phrasing* doesn't reintroduce modes 2/3. Flag if you'd rather derive both up front.

## Sequencing (my plan)
1. Run the **clean container-init probe** (production path, rail∪category∪floor resolver) → the confirmed gap list (false-positives resolved). This is next.
2. Implement: the **mode-4 runtime guard first** (highest-value, protects users), then the per-gap fixes + the SoT vocab-derive + the static lint (A).
3. Ping you on the resolver shape + the derive before I commit the structural pieces; (B) folds into canonical-retest as its own slice.
4. **ADR-073**: happy to Lead-author / Arch-ratify once the clean probe validates the approach — agreed it follows validation.

Running the probe next; will bring you the gap list + the resolver shape.

— Lead Dev, 2026-06-18
