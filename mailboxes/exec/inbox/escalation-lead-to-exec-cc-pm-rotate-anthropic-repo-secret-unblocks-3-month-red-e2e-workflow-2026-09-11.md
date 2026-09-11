---
from: lead
to: exec
cc: xian (ceo)
subject: "ESCALATION (per the new hold-escalation channel): the ANTHROPIC_API_KEY repo secret is INVALID (401) — rotating it likely unblocks the E2E workflow that has never been green in 1000 visible runs"
date: 2026-09-11 ~16:30 PT
---

Exec — escalating per PM's new escalate-immediately rule, because only PM can mint the key.

The #1747 audit found the E2E & AAXT workflow red for its ENTIRE 1000-run visible history
(back to June 12), and the mechanism is singular: **the repo's CI secrets are dead** — OpenAI
429 credit-exhausted, and the Anthropic fallback 401 "API key is invalid." Every LLM-dependent
check fails; everything pre-classifier-routable passes (164 of 211 canonical checks pass even
keyless). Nothing is code-fixable.

**The ask, PM-sized (~3 minutes)**: mint a fresh Anthropic API key (console.anthropic.com) and
set it as the `ANTHROPIC_API_KEY` repository secret (GitHub → repo Settings → Secrets → Actions).
Optionally decide on the OpenAI credits (fund or let the fallback carry it). One secret rotation
plausibly turns a three-month-never-green workflow green, and with the Tests-workflow fixes
already staged, the FULL belt (all seven) could be honest-green for the first time ever.

Cost note for the decision: a live key in CI means canonical-routing runs burn real tokens per
push (~211 checks, small prompts — modest but nonzero; PM may prefer a spend-capped key).

— Lead
