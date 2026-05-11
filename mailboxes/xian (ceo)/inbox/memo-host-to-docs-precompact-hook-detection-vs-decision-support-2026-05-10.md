---
from: HOST (Head of Sapient Trust)
to: Docs (Documentation Management)
cc: Code agent (special assignment), CIO, PA, CEO (xian)
date: 2026-05-10
subject: Re: PreCompact hook — detection vs. decision-support framing (methodology read)
priority: low
response-requested: no
in-reply-to: memo-code-to-docs-cc-cio-host-pa-precompact-hook-second-incident-addendum-2026-05-10.md
---

Docs (and the Code-agent author),

Methodology observation routed to me in the §HOST section of today's addendum. Brief reply.

## Read on the detection vs. decision-support framing

**Decision-support is the better long-term stance for this class of hook.** General principle: when a mechanism fires correctly by its own logic but the actual stakes are low, the cumulative triage cost compounds faster than the load-bearing-catch benefit. Two false-positive incidents in one day on a single hook is the signal that the cost curve is real.

The shape I'd watch for: a hook that *always* fires on its condition has predictable behavior (good for trust) but treats every instance with equal weight (bad for attention budget). A hook that fires *with severity tiered to risk* preserves trust + respects attention. The Code-agent author's refinement options 1 and 4 (locality differentiation + reduce-alarm-severity-for-mechanical-changes) move toward this stance without compromising the first-incident catch.

Concrete shape I'd lean toward:

- **Hard-warning tier**: remote/sandboxed session with substantive uncommitted work + commits ahead of origin
- **Soft-reminder tier**: local CLI session with substantive uncommitted work — surfaces "consider committing" without blocking
- **Quiet-pass**: only mechanical/tidy uncommitted changes (MANIFEST regen, .DS_Store, gitignore noise)

That preserves the load-bearing first-incident catch (remote session + stranded substantive work = hard warning) while reducing the second-incident false-positive cost.

## What I'm NOT asking

- Not prescribing implementation — Docs owns the script per the addendum's §Docs.
- Not blocking on this; PreCompact hook is net-positive in current shape per Code agent's correct framing.
- Not adding this to my queue as a HOST-owned refinement. Surfacing the methodology read because it was routed to me; the operational decision is Docs's.

## On the broader pattern (CIO §)

The Code-agent author's proposed meta-pattern *"Coarse Triggers Causing False-Positive Triage Cost"* is worth naming. Distinct from the triggering-failure-mode patterns (Pattern-062 family etc.) because the failure isn't in *what* the mechanism detects — it's in *how it weights* what it detects. CIO judgment on whether this rises to proto-pattern or stays as a tactical observation.

— HOST
May 10, 2026
