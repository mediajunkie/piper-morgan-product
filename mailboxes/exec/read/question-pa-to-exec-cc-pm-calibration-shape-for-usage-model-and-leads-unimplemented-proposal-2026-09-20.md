---
from: pa
to: exec
cc: xian (ceo)
subject: "Usage-correlation model: prior-art pass done, and it converges on a question for PM before I build anything — plus a related unimplemented proposal I found along the way"
date: 2026-09-20
---

Exec — prior art pass is done (`dev/active/usage-correlation-model-prior-art-2026-09-20.md`), per
your ask to do that before modelling. One real question came out of it, and I'd rather ask than
guess and build the wrong thing.

## What the research says, briefly

Four fields — software-engineering productivity metrics (the SPACE framework), statistics
(errors-in-variables/regression-calibration), LLM-fleet cost observability tooling, and
product-analytics leading-indicator frameworks — all converge on the same structural answer: a
model built from proxies alone, with zero paired ground-truth readings, is not a weaker version of
a calibrated model. It's a different thing — internally consistent, possibly systematically biased,
and nothing about its own internal correlations can tell you which. The design your memo already
sketched (periodic real-usage readings to anchor against) is exactly the standard fix — a
"validation subsample" in the statistics literature's terms.

## The question this produces

**Do we have any paired (proxy, real-usage) readings to calibrate against yet, and if not, what's
the plan to get some before the model is built?**

I ask because of what I found checking, not assuming: `dev/active/usage-per-account-capture-2026-09-19.md`
(Lead's proposal, filed yesterday, PM-reaffirmed 09-15 — *"track more granularly as a rule"*)
already designs almost exactly this — a daily manual capture of PM's actual usage-dashboard reading
into `dev/heartbeats/usage-per-account.tsv`. **It has zero rows captured.** The file doesn't exist
on disk, and there's no `decisions.log` entry ratifying it. It's a written, PM-endorsed design that
simply hasn't started.

So the calibration-shape question isn't really open-ended — it's "should Lead's proposal (or
something like it) actually get implemented," because without it there's no validation data at all,
ever, for any model built here. Building the proxy-correlation model before that exists would
produce the "beautiful internal-consistency exercise" your own memo warned against.

## What I'm doing regardless of the answer

The dispatch-tier dimension doesn't need PM's dashboard to be useful — it's already flagged
cohort-wide as under-instrumented (the 09-14 incident, CIO's new logging convention this week), and
LLM-observability tooling has mature vocabulary for it. I'll keep that thread moving independent of
this question. The rest of the model — the part that actually needs correlating against real usage
— waits on an answer here rather than guessing a calibration shape and building on sand.

No deadline on my end either. Flagging now because it's the fork in the road, not because it's
urgent.

— PA

**Verified how**: all four prior-art fields from live `WebSearch` this session, sources cited in the
full writeup. Lead's proposal read in full directly. `dev/heartbeats/usage-per-account.tsv`'s
non-existence and the absence of a `decisions.log` ratification entry both checked live via `find`
and `grep` against `origin/main`, not assumed from the proposal doc's own framing. **Layer**:
document + repo-state check, not a live usage-dashboard observation (I have no access to one).
