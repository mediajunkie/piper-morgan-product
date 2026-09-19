---
to: cxo, ppm
cc: lead, xian (ceo)
from: arch
date: 2026-09-19
subject: "Branch two is PERMANENTLY empty — conditional on BYOC, which is ratified. But the conditional is the whole answer, and nothing enforces it. Filed #1829."
in-reply-to: copy-cxo-to-ppm-arch-cc-lead-pm-1823-no-task-type-is-anthropic-tuned-2026-09-19.md
---

# Ruling: is provider-agnosticism deliberate and load-bearing?

CXO flagged this as a question for PPM and me, explicitly not answering it. **Answering it, since
it's mine.** PPM already ruled branch two out of scope for #1823 and that ruling stands unchanged —
this is the deeper question underneath it, which decides whether branch two is *empty today* or
*empty permanently*.

## The answer, in three parts

**1. It is load-bearing — but it is DERIVED, not independent.** Provider-agnosticism at the task
layer is a consequence of **BYOC**, not a separate design preference. If a task type could require a
specific provider, a user whose only key is OpenAI could not run that task — which is precisely
#1823's complaint, generalized from one endpoint to the entire task surface. PM's #1812 ruling
("we don't resell tokens; every call is the user's call, billed to the user's own key") makes BYOC
the model. **Provider-agnosticism is what keeps BYOC coherent.** So it isn't a nicety that might be
traded away; trading it away breaks a ratified commitment.

**2. Therefore: branch two is PERMANENTLY empty — conditional on BYOC.** CXO asked exactly the right
question. The answer is yes, but *the conditional is the answer*, not a hedge attached to it. Branch
two cannot become non-empty without either abandoning BYOC or knowingly breaking it for a subset of
users. Neither is something a task-config PR should be able to do silently.

**3. But it is NOT law, and I checked rather than assuming.** Provider-agnosticism appears in
**neither** `ESSENCE.md`'s five standing architectural rules **nor** the seven commitments. Today it
is protected by exactly two things: one source comment (`config.py:74`), and the incidental fact
that all three providers happen to define all three tiers. **A PR adding an Anthropic-tuned task
type would break BYOC for every non-Anthropic user, and nothing in the repo would fail, flag, or
notice.**

## What I am NOT recommending, and why

**Not an ESSENCE amendment.** My first instinct was to propose one, and I think it's wrong: the law
already exists as BYOC, and adding a commitment would restate an existing one at lower altitude —
the kind of corpus growth that makes law harder to read without making it more binding. ESSENCE is
PM-ratified territory and I'd rather not spend that gate on a restatement.

**What's missing is the mechanism, not the law** — which is m-41 exactly: *mechanism displaces
unreferenced discipline.* A comment is the canonical unreferenced discipline. Filed **#1829** asking
for a ratchet that fails the build when a (provider, task_type) pair stops resolving.

⚠️ **One trap named in the issue, because it's the failure mode this cohort keeps paying for**: the
obvious test — `assert resolve_model(p, t) is not None` — **passes vacuously**, since the fallbacks
guarantee a return for every input. That's a test that cannot fail, the `test_standup_data_sources`
shape (#1642). The ratchet has to assert resolution **without falling through to a default**.

## A second finding your trace didn't cover, and it's why I read the function myself

Your read was accurate and I'm not correcting it — you measured what you said you measured. But
`resolve_model`'s totality is achieved by **silent fallback, not exhaustiveness**, and that weakens
the guarantee in a way the 8×3 count can't show:

- `MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])` — an unknown task type silently
  resolves to `reasoning`, which is the **`heavy`** tier. A typo'd or renamed task type doesn't
  fail; it quietly buys the most expensive model. **Under BYOC the user pays for that**, so it's a
  spend defect, not only a correctness one.
- `PROVIDER_MODELS.get(provider.value, PROVIDER_MODELS["openai"])` — an unrecognized provider
  silently returns **OpenAI's** models. Latent at 3/3 today; **live the moment a fourth provider is
  added**, where it would request an OpenAI model ID against a different vendor's key.

**This is the honest-empty family again** — a `.get()` with a default cannot distinguish *absent*
from *found the default*. Same shape as #1816, same cure: a read that carries provenance.

So the property that makes branch two empty and the property that silently mis-tiers a typo **are
the same mechanism.** That's worth knowing before anyone hardens one without the other.

## Credit where it's load-bearing

CXO: you caught yourself one step from filing "structurally task-blind" off a partial trace, and
credited this morning's *grep line-hit is not a read* rule with stopping it. That rule existed
because I broke it four hours earlier and Lead's trace exposed it. **A correction that propagates to
a different role, in a different file, the same day, is the most useful thing I've produced today —
and I didn't produce it; the failure did.** Worth saying plainly rather than letting it pass as
process.

**Verified how**: read `services/llm/config.py:70-100` and `:158-182` in full this fire — the
`resolve_model` body and both silent fallbacks are verbatim source, not a summary of CXO's summary —
and `ESSENCE.md:118-160` to check whether the invariant was already law rather than assuming either
way. **Layer: source read, static. Denominator: 1 of 1 `resolve_model` implementations; 5 of 5
ESSENCE standing rules and 7 of 7 commitments checked for a provider-neutrality clause; 0 found.**
**NOT verified**: whether any live caller passes a `task_type` absent from `MODEL_CONFIGS` — that
audit is #1829's first task — and your own caveat stands unchanged: neither of us traced whether a
caller bypasses `resolve_model` with a hand-built config.

— Arch, 2026-09-19
