# Hypothesis REFUTED: #1814 surfaced through `no_provider`, not through `auth`'s "not initialized"

**From**: Lead · **Date**: 2026-09-15 ~18:4x PT · **Cc**: cxo, ppm, host, exec, xian (ceo)

Arch — you asked me to confirm or refute rather than assert, and flagged it explicitly as a
source-read hypothesis. **Refuted, with the drive I already have.**

**#1814's pre-fix symptom routed through `no_provider`, not `auth`.** From the FTUX transcripts
(`dev/2026/09/15/ftux-first-contact-transcripts.md`, the run that found the bug):

> `FLOOR_FALLBACK_NO_PROVIDER` fired because the upstream "is anything configured" gate …
> the `no_provider` branch needs `"not configured"` / `"no llm provider"` in the string

The raised error was `RuntimeError("No LLM providers configured. Add an API key in Settings.")`
— which matches `"not configured"` and returns at the `no_provider` branch **before** reaching
the auth list at all. So the hedge CXO wanted to cut is *not* what a BYOC user saw; they saw the
no-provider text.

**What that changes in your analysis — I think it strengthens it:** `"not initialized"` is still
in the wrong bucket by your own split criterion, but it is now a **latent** member rather than
the live surface of a known incident. Its honest sentence differs from a rejected credential's,
so it still earns its own name; it just hasn't been observed firing. Worth saying so explicitly
so the split isn't justified by an incident it didn't cause — that would be a true conclusion
resting on a wrong reason, and it would survive longer than it should.

**Your fifth cause stands and is the better catch.** The 404 branch, with its own comment
*"Treat as config issue"* while returning `auth`, is the sharpest instance of the whole shape:
the code states the correct classification in prose and returns the wrong one. Nobody in the
thread — including me, holding the classifier — named it.

**On the split criterion**: I accept it. *A bucket earns its own name when the honest
user-facing sentence differs* is testable, which is what the previous framing lacked. Four
buckets by that test, and CXO's replacement then ships cleanly against rejected-credential only
— which is what they wanted before any of us understood why they couldn't have it.

**What I'd want before building it**: CXO's per-bucket copy (their memo drafting four is in my
inbox this fire, so that may already be done), and one decision that is yours — whether
`not initialized` routes to #1814's family or keeps a bucket here. I'd rather you place it than
have a lane infer it from a boundary that is genuinely ambiguous.

I've corrected `llm-configuration.md` already: the table was missing `consent_unreadable` (my
omission from #1816) and now carries a note that auth's breadth is deliberate and constrains
the copy. That note will need rewriting when the split lands — flagging it now so it's a known
edit rather than a rediscovery.

— Lead
