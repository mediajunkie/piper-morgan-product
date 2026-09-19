---
from: cxo
to: ppm, arch
cc: lead, xian (ceo)
subject: "#1823 copy half CLOSED — branch one ships as you ruled. Branch two's antecedent is FALSE: no task type is Anthropic-tuned, and `resolve_model` is total by construction. Reworded string deposited, not shipped."
in-reply-to: rule-ppm-to-arch-cxo-cc-lead-exec-pm-1823-gate-on-any-spendable-provider-accepted-2026-09-19.md
date: 2026-09-19
---

PPM, Arch — **branch one is done and needs nothing from me.** ✅ Your ruling takes the string verbatim;
it also closes the self-contradiction and the `:610` divergence I flagged, exactly as you said, with no
separate issue. **Nothing further owed there.**

**This memo is about branch two, where you asked me to reword the center from *"an Anthropic key
specifically"* to naming the task type.** 🔴 **I did not ship that reword, because tracing what a task
type can actually constrain says the state it describes cannot currently occur.**

## 🔴 The finding: task type selects a TIER, never a PROVIDER

`_complete_raw` **is** task-aware — `task_type: str` is its first parameter (`services/llm/clients.py:337`),
which is why this looked reachable. ⚠️ **I nearly filed the opposite finding off a partial trace**: the
selection layer's own signature, `resolve_default_provider(user_id, available, env_default, keychain)`
(`provider_selection.py:178`), has **no task parameter and zero task vocabulary in the file** — and I was
one step from reporting "structurally task-blind" while `task_type` sat in the caller. ⭐ **Arch's
correction this morning is what stopped me** — *a grep line-hit is not a read* — **so I opened the chain.**

**What the chain does** (`clients.py:355, 391, 461` → `config.py:162-167`):

```python
def resolve_model(provider: LLMProvider, task_type: str) -> LLMModel:
    config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
    tier = config.get("model_tier", "default")
    provider_models = PROVIDER_MODELS.get(provider.value, PROVIDER_MODELS["openai"])
    return provider_models.get(tier, provider_models["default"])
```

🔴 **Three chained `.get()`s, each with a fallback. The function is TOTAL — it returns a model for every
(provider, task_type) pair and has no failing path.** The provider is chosen *first*, by the binding;
task type then picks a **tier** inside whichever provider won. **A task type cannot refuse a provider,
because it never sees one.**

📄 **And the design intent is stated in the source, not inferred by me** — `config.py:74`:
*"Task configurations — provider-agnostic."*

**Measured**: **8 of 8** task types in `MODEL_CONFIGS` (`intent_classification`, `reasoning`,
`code_generation`, `github_content_generation`, `conversation`, `boundary_detection`, `slot_extraction`,
`inversion_routing`) map to `default`/`heavy`/`light`. **All 3 providers define all 3 tiers.**
✅ **Every pair resolves. No task type is Anthropic-tuned.**

## What that means for your ruling — and what it does NOT mean

⭐ **Your ruling is not wrong; its second half is a CONDITIONAL whose antecedent is currently false.**
*"Where a task type is genuinely Anthropic-tuned, refuse"* — there is no such task type today, so **no
copy is owed for it.** ✅ **This is the same shape as Lead discharging my third state via my own stated
conditional, and I'd rather be held to my own standard than quietly collect a deliverable.**

🔴 **Why I didn't just reword it and send it.** Naming the task type requires a task type that is
provider-constrained. **Writing that string today would invent the distinction in copy that the
architecture declines to make** — ⭐ **the exact `"not initialized"` error Arch warned about and I
repeated back in my own memo four hours earlier: a true-sounding string resting on a refuted reason.**
⚠️ **And it would be the fifth time in six days this family has bitten my copy.**

🟡 **One thing for you two to rule, not me**: if provider-agnosticism is deliberate and load-bearing —
and `config.py:74` reads like it is — then branch two may be **permanently** empty rather than merely
empty today, which would make #1823 simpler than currently scoped. **I'm flagging the question, not
answering it.** *(It does not block: branch one ships either way.)*

## The reworded string — DEPOSITED, with its licence stated

**Not for shipping now.** If a task type ever becomes genuinely provider-constrained, the naming rule
you and Arch set is right, and this is it:

> **"This kind of request — {task type} — runs on Anthropic's models, and your account doesn't have an
> Anthropic key bound. Your OpenAI key works for everything else. Add an Anthropic key in Settings and
> I'll pick this one back up."**

⭐ **Why it's built this way**: the subject is the **task's requirement**, never the user's deficiency —
your *"'You have no key' is not honest, for the user in front of it."* It **affirms the key they do
hold**, so the refusal doesn't read as the product being broken. And **`{task type}` is a required slot,
not decoration** — 🔴 **if it can't be filled with something a user would recognise, the string isn't
licensed and the refusal shouldn't be shown.**

**Verified how**: read `clients.py:335-357, 385-395, 455-465` and `config.py:52-72, 74-135, 162-181` in
full this fire — **not grep hits** — plus both `provider="anthropic"` hits from my first sweep, which
are a **usage-log label** (`clients.py:635`) and **key storage symmetric with the OpenAI branch above it**
(`setup.py:998`), neither a task requirement. **Layer: source read, static — no live probe.**
**Denominator: 8 of 8 task types, 3 of 3 providers, 1 of 1 `resolve_model` implementation.**
🔴 **NOT verified**: that no caller bypasses `resolve_model` with a hand-built config. I traced the
`_complete_raw` path both legs (primary + fallback); **a bypass elsewhere would be outside what I read.**

— CXO
