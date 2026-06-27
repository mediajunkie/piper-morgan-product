# Anthropic billing model — two surfaces, two pools

**Purpose**: kill the recurring confusion between **Claude-subscription usage caps** (what the agent cohort runs on) and **Anthropic API spend** (what the Piper Morgan product runs on). They are separate accounts, separate meters, separate controls, and separate failure symptoms. Conflating them is what made the 2026-06-27 "I refused overages but still got a fee" surprise confusing.

**Author**: Exec, 2026-06-27 (at PM's ask). Verify any specific numbers/tier names against the live console — this captures the *model*, not current figures (which drift).

---

## The two surfaces

| | **Claude subscription** | **Anthropic API** |
|---|---|---|
| What it is | Max/Pro plan via your **claude.ai account** | Pay-per-token via **console.anthropic.com** |
| **Used by** | **The AGENT COHORT** — Claude Code sessions (`/login` with the Claude account) | **The PIPER MORGAN PRODUCT** — the app's LLM calls via `ANTHROPIC_API_KEY` |
| Billing | Flat-rate; usage **CAPS** (no per-token charge) | **Pay-per-token**; prepaid / auto-reload credits |
| Limits | Rolling ~5h window + weekly caps; you hit a wall and wait for reset | Rate limits (tokens/min, requests/min) by **usage tier**; credits drain |
| Symptom when exhausted | "busy signal" / "rate limit" / "limit reached, resets at X"; **session stalls** | HTTP 429s / credit depletion / an **unexpected invoice** |
| Control lever | subscription tier; spread sessions across accounts | console **spend limit + budget alert** |
| "Credits" | **N/A** — there are no credits here | **THIS** is where credits live |

---

## Symptom → surface (the 10-second diagnostic)

- **An agent (Claude Code session) stalls** with a busy-signal / rate-limit → **subscription** cap. *(Every agent stall 2026-06-25→06-27 was this.)* More credits won't help; spread sessions across accounts or wait for the window to reset.
- **A fee / charge / "scaling tier" / "higher rate limits on the Claude API" email** → **API/product** side. *(The 2026-06-27 fee + tier bump were this.)*
- **Rule of thumb**: mentions *console.anthropic.com, usage tier, TPM/RPM, or credits* → **API**. Mentions your *Claude/Max plan or Claude Code* → **subscription**.

---

## The "I refused overages but still got a fee" trap

"Refuse overages" is a **subscription-side** setting. It does **NOT** cap API spend. The API is pay-per-use; its only hard ceiling is a **monthly spend limit + budget alert** in the console billing settings. The 2026-06-27 fee was straightforward product API consumption (a tester actively using the alpha) drawing against the API account, entirely independent of the subscription overage setting. **Action if you want a real product-spend cap: set the console spend limit.**

---

## "Scaling tier" (the 2026-06-27 email)

Anthropic auto-promotes API accounts to higher **usage tiers** as payment history + volume grow. **"[No Action Required]" = a ceiling raise, not a charge.** It's a good sign: product API usage grew enough (alpha-tester load — Jake) to trip the next tier, and the product now won't hit rate-limit walls as testers expand.

---

## Efficiency levers (API/product side ONLY)

The subscription side has no efficiency knob — it's flat-rate; you just live within the caps. The **API side scales with usage**, so it's where efficiency matters as the alpha grows:

- **Model routing** — send cheap/simple calls to **Haiku** instead of Sonnet/Opus (large cost delta).
- **Prompt caching** — ensure the cache layer is actually cutting repeat input tokens.
- **#1152** — multi-LLM / local-model fallback (the structural cost lever).

Tracked as a cost-efficiency thread → see the exec→CIO+Lead memo `memo-exec-to-cio-lead-cc-pm-product-api-cost-efficiency-2026-06-27.md`.

---

## One-line summary

**Agents = subscription = caps = "busy signals" (wait it out).  Product = API = credits = fees (cap it in the console).**  Different pools; they don't trade off against each other.
