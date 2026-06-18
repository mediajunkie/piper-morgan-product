---
from: Lead Developer
to: PA (Piper Alpha)
date: 2026-06-17
cc: PM (xian)
subject: "Caddy bearer-gate (Ted's 401) — what I understand + what I DON'T (you had BYOC working before, so you'll know what regressed) + a security interaction with the #1162 fallback you/PM need to decide BEFORE the gate comes off"
priority: high — blocks external testers; the security interaction below is the load-bearing part
response-requested: PA — the Caddy config + what regressed; PM — the fallback-policy decision (below)
---

# Caddy gate — explainer + the one thing that must be decided before removing it

PM asked me to write this up. **Caveat first, honestly**: I am **not** on the Caddy / hosted-infra config — I haven't seen it. Everything in §1 is inferred from your #1162 do-now memo + how Caddy generally works. **You had the BYOC path working before, so you'll know the actual config + what regressed far better than I can.** This is explainer + handoff, not a fix (PM: not mine to fix). §3 is the part I *can* speak to with authority (it's my server-side code) and it's the one that needs a decision before the gate comes off.

## 1. The issue as I understand it (inferred — please correct)
- `alpha.pipermorgan.ai` sits behind **Caddy** (reverse proxy / TLS terminator) in front of the Piper app (`main.py`, the FastAPI server).
- Caddy has an **auth directive** that requires a **static bearer token** (an `Authorization: Bearer <shared-secret>` check, or `basic_auth`/a matcher) — requests without the token get **401 at the edge**, before reaching the app.
- xian's own setup has the token; **Ted doesn't**, so his plugin's calls 401 at Caddy. That's the "install and it works" gap.
- Net symptom: the **edge gate**, not the app, is rejecting Ted.

## 2. What I DON'T know — and what you likely do (the "worked before" angle)
You had BYOC working for xian's testing, so:
- **What's the actual Caddy auth config?** (a `forward_auth`? a static-token matcher? basic_auth? a Caddyfile snippet?)
- **Was external (non-xian) access ever working, or only xian-with-the-token?** If external worked before and broke, **what regressed** — a Caddy config change, a token rotation, a deploy that re-added the gate, a cert/host change?
- Is the bearer token per-user or one shared secret? (The memo said "our static bearer token" = sounds like one shared secret.)
- Where's the Caddy config managed (skunkworks? a server-side Caddyfile? a deploy script)?

These are yours/ops to answer; I can't see them from the product repo.

## 3. ⚠️ The security interaction that MUST be decided before the gate comes off (this part IS my code)
The #1162 plan is "remove the gate because users supply their own LLM key." But my server-side fallback (per PM's spec) is: **request *without* `X-User-Api-Key` → fall back to the server's configured Anthropic key (xian's).** That fallback is safe *today* **only because the Caddy gate restricts who can reach the endpoint** (just token-holders).

**If the Caddy gate is removed and nothing else changes, the endpoint is open to anyone, and any request that arrives without a user key will bill xian's Anthropic key.** That's an open door to your LLM billing (and an abuse/DoS surface). The gate and the fallback are load-bearing *together* — you can't remove one without addressing the other.

**So before/with removing the Caddy gate, a decision is needed (PM):**
- **Option A (recommended):** remove the Caddy gate **and** change the server so the **server-key fallback only applies to authenticated requests** (xian via JWT/cookie); an unauthenticated/external request **must** carry `X-User-Api-Key` or it's refused (never silently uses xian's key). **This server-side change is mine** (~a small refinement to the #1162 fallback logic) — I'll do it when PM rules, since it's the safe end-state.
- **Option B:** keep a lighter edge gate (rate-limit / per-user token) — but that reintroduces a token Ted needs, partially defeating "install and it works."

My recommendation: **Option A** — it's what makes "users pay their own way" actually true and protects xian's key. But it means the gate removal (ops/you) and the fallback-gating (me) ship **together**, or there's a billing hole in between.

## Net
- The Caddy gate itself: **yours/ops** (config + what regressed) — not mine to fix.
- The **fallback-security interaction**: PM decides the policy (A vs B); if A, the server-side fallback-gating is **mine** and I'll do it on your word.
- Don't remove the gate in isolation — pair it with the fallback decision, or xian's Anthropic key is exposed.

— Lead Developer, 2026-06-17
