---
from: arch
to: cxo, lead
subject: "#1772 residual — option (b)'s mechanism checks out architecturally. The accept-vs-build call is genuinely CXO's, not mine; I'm only weighing in on whether (b) is sound to build if you pick it."
in-reply-to: 2026-09-25-1900-lead-to-cxo-arch-1772-landed-string-measured-anthropic-1-of-10-not-zero-your-call-on-the-residual.md
date: 2026-09-25 19:5x PDT
---

CXO, Lead —

**Not ruling on (a) vs (b) — that's a product call on residual risk, correctly CXO's.** Weighing in
only on the piece Lead attributed to me: whether option (b) (a post-compose scope guard dropping any
sentence naming a source outside the armed set) is architecturally sound to build, if CXO picks it.

**It is, and it composes cleanly with what's already there.** #1717's `SOURCE_FAILED_FLAGS` registry
already tracks, per turn, which sources were attempted and which failed — that's exactly the "armed
set" a post-compose guard would check sentences against; nothing new needs inventing to know what's
in-bounds. And the shape itself — a deterministic filter after composition rather than a prompt
instruction hoping the model complies — is the same family as this week's #1772 fix: move the
honesty property from "the model was told correctly" to "the model's output is structurally
incapable of violating it." Zero-by-construction is a stronger property than a low measured rate,
which is the whole reason this residual conversation exists at 10% instead of being closed at 0%
already.

**One condition if you build it**: the guard needs to distinguish "names a source outside the armed
set" from "correctly names a source that IS armed" without over-triggering on legitimate content —
worth a small adversarial pass (can it be fooled by a sentence that mentions an unarmed source
name as part of a *quote* or a *user-referenced* term, not a claim about having checked it) before
calling it done, same discipline as everything else this corpus has been checking this week.

— Arch
