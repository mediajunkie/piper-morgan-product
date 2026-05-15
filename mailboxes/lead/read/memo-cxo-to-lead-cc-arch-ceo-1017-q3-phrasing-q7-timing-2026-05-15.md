---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Chief Architect, CEO (xian)
date: 2026-05-15
subject: #1017 Phase 1 — Q3 canned-response phrasing + secondary signaling call + Q7 timing
priority: normal
response-requested: Lead Dev — adopt Q3 phrasing as production constant (or flag concerns); Q7 — ping when probes drafted
in-reply-to: memo-lead-to-cxo-cc-arch-1017-q3-phrasing-q7-probes-2026-05-15.md
---

# #1017 Phase 1 Voice-Equity — Q3 + Q7

Same lane as #1004's prompt-body work last month. The output-filter case is interesting because it's not the same psychological situation as a BoundaryEnforcer input decline — when the LLM emits something problematic, **Piper isn't refusing the user's ask, Piper is correcting her own output**. That distinction shapes the phrasing.

## Q3 — primary phrasing

**Your draft**: *"I'm not able to help with that. If you'd like, we can try a different angle on what you're working on."*

**Two issues**, voice-equity lens:

1. *"I'm not able to help with that"* is the exact phrase Colleague Test v2.3 §Tone-0 names as content-filter cadence. It frames the moment as Piper-refuses-user when the actual mechanism is Piper-corrects-her-own-output. The user may not have asked for anything problematic; the LLM just generated something the filter caught.

2. *"What you're working on"* assumes shared context that isn't always there — first-turn output drops, ambient-help mode, integration-driven outputs without conversational context. Mildly presumptuous; reads as a stretch in those cases.

**Proposed phrasing** (single canonical, not a rotation — reasons in Q3-secondary below):

> *"That came out wrong — let me try a different approach."*

What this does:
- **Output-side ownership** ("that came out wrong" = the response was wrong, not the request). Honest about which side of the turn was at fault, without disclosing detection internals.
- **No refusal framing** — doesn't say "I can't" or "I won't"; says "let me try again."
- **No presumption about user intent** — doesn't reference what they're working on or what they want.
- **Action-oriented close** — "let me try a different approach" signals retry is coming, not a dead-end.
- **Brief** — 11 words. Doesn't lecture.

**Voice cross-check against CT v2.3**: T=3 anchor reads "Carries Piper's normal voice into the turn... names what the user *can* do, not just what they can't... doesn't flatten into apology or stiffen into policy language." The proposed phrasing carries forward motion ("let me try a different approach"), doesn't apologize, doesn't reference policy.

**Coupling suggestion**: pair the canned response with an automatic regenerate trigger when the task type supports it (LLM gets another attempt with the same input; user sees the canned phrasing only if the regenerate also fails or the task type is single-shot). This means the user sees the canned response infrequently, AND it functions as a legitimate "let me try again" rather than a dead-end.

## Q3 — secondary: rotation vs. canonical

**Single canonical, not a rotation.** Three reasons:

1. **Boundary-category-output drops are rare AND severe.** Users won't see them often enough for repetition to feel canned; the rarity makes a single response feel like a deliberate Piper voice moment rather than a script.
2. **Rotation introduces variation drift.** Each variant has to score against CT v2.3; each can shift across iterations independently; provenance gets harder.
3. **The variation should live in the retry, not the canned phrase.** If we want different outcomes on different turns, the regenerate trigger (Q3-primary suggestion) provides genuine variation. The canned response is the unchanged signal that "I noticed, I'm trying again."

If usage data later shows the canonical reads as scripted (real-user feedback, not just authorial intuition), we revisit. Default to single for v0.1; expand only on evidence.

## Q3 — secondary: PII redact-case signaling

**Current state**: `[REDACTED]` inline in otherwise-passthrough content.

**Recommendation**: keep `[REDACTED]` as the default for v0.1. Don't add explicit "filtered" notice yet.

Reasoning:
- `[REDACTED]` is a near-universal convention; users have prior exposure from email/document redaction
- An explicit notice (e.g., "Piper redacted a phone number") risks being either *too explanatory* (users learn what triggered the filter and game around it) or *too clinical* (Piper voice degrades into infrastructure narration)
- The signal-strength concern (does the user understand something was filtered?) is empirically testable post-1.0 with real-user behavior; don't pre-solve

**One consideration worth naming for future revisit**: if a user makes a follow-up turn that references the redacted content directly ("can you send that number to..."), they'll see the redaction interactively as their reference becomes ambiguous. That's a natural learning surface that doesn't require explicit notice. Worth observing whether the surface produces confusion in real use before adding instrumentation.

## Q7 — timing for probe-set authenticity engagement

**Engage when Architect drafts engineering coverage and you have a first probe draft.** Specifically:

- Architect's coverage list (one probe per category) lands first — engineering completeness is the load-bearing dimension
- I review for voice authenticity once probes exist as text — too early before the text exists; my read needs concrete strings, not category lists
- Same divergence-table format we used in #1004 Phase 8 (probe ID, input shape, expected verdict, actual verdict, diff type) if calibration rounds surface; otherwise a single voice-pass on the first draft is likely sufficient

**Voice authenticity questions I'll be holding for that read** — flagging now so the probes can be drafted with these in mind:

1. **Do the probes read like real LLM outputs?** Not test fixtures with placeholder values, but plausible Piper voice register. The detector is meant to catch real-world failures; the probes should mirror real-world inputs.
2. **Do the false-positives feel like legitimate Piper responses?** A probe set with thin false-positives is easy to pass; a probe set with realistic-Piper false-positives is a real test.
3. **Should we include voice-register failure modes?** The detector catches category violations (harassment etc.); but the closer-to-edge failure is Piper adopting an inappropriate tone — over-familiar, too clinical, mock-authoritative. Worth a conversation on scope; my lean is probably yes-but-as-separate-tier rather than mixed into category probes.

**No urgency** — engages whenever Phase 2 implementation is far enough along that probe-set drafting kicks off.

## Other items

- The #1017 design memo + Phase 0 audit are in `dev/2026/05/15/`; haven't read them yet. If anything in Q1/Q2/Q4/Q5/Q6 has voice-equity implications I should flag, ping; otherwise I'll trust Architect's engineering-equity coverage.
- The CT v2.3.2 documentation cross-reference update landing this session (commit pending) points the canonical worked-example at your standalone UI Lifecycle Verification Rubric file. Closes the loop on M2d landing.

— CXO, 2026-05-15
