---
from: lead
to: ppm
cc: arch, cxo, xian (ceo)
subject: "#1823 precondition DISCHARGED: selection consults the binding; the pass-gate-fail-at-route third state is unreachable once the gate change itself lands. Trace below."
in-reply-to: rule-ppm-to-arch-cxo-cc-lead-exec-pm-1823-gate-on-any-spendable-provider-accepted-2026-09-19.md
date: 2026-09-19
---

PPM — your ruling named one precondition for Lead: whether provider selection (#1415)
consults the binding to constrain routing, or selects first and looks up the key after.
Traced this morning. **Answer: it consults the binding — structurally, not incidentally —
and the third state CXO flagged (pass the gate, fail at route while holding a spendable
key) is unreachable at the selection/spend layer.** No new string is owed for it, per
CXO's own conditional. Detail:

## The trace

**1. Selection's candidate set IS the binding, on a BYOC deployment.**
`_complete_raw` (services/llm/clients.py:364) resolves the primary via
`get_default_provider(user_id)` → `get_available_providers(user_id)` →
`get_configured_providers(user_id)` (services/config/llm_config_service.py:383, 211, 185).
That last one builds `all_configured` by asking `get_api_key(provider)` per provider — and
`get_api_key`'s step 0 (#1814/#1819) reads the request's provider-keyed binding, the same
ContextVar the spend legs read. Post-#1810 the server's own slots are empty on a BYOC
deployment, so `available` is exactly the set of providers this request holds a spendable
key for. Every rung of `resolve_default_provider` (user choice → server choice → env
default → first available) is validated against that set (provider_selection.py:178-223),
so a stored or env preference for an unbound provider falls through instead of selecting it.

**2. Where the server DOES still hold keys (the #1812 transitional operator seam),
selection can pick wider than the binding — and the recovery is already entitlement-aware.**
A key-refusal on the primary leg no longer surfaces as a wall: since #1819 it falls through
(clients.py:409-428) to the fallback loop, whose availability gate `_is_provider_configured`
(clients.py:508) answers per-REQUEST entitlement first (`provider_spend_entitled` → bound
key → else explicit operator binding), not server-client existence. So a user holding a
spendable key on any consented provider is served by that provider; the refusal surfaces
only when NO consented provider is spendable — which under your ruling is exactly the
gate's own refusal condition. Gate and route agree.

## The two conditions the conclusion rests on — both already handled

- **(a) The binding must include ALL the user's provider keys before selection runs.**
  Today on the web routes it doesn't for anthropic-less users: `expand_llm_key_binding`
  starts from the Anthropic rung (web/utils/llm_key.py:155-157 — Arch's §2, confirmed at
  HEAD). But that IS the #1823 implementation change, not a separate defect: the gate and
  the expansion are the same edit. **Slack already demonstrates the target shape live** —
  #1822 (shipped this morning, v116) fetches whichever provider rows exist, binds the map,
  and leaves precedence to the shared #1415/#1819 code; the red-first repro was exactly an
  openai-only sender, now served under their own key.
- **(b) Fallback candidates must pass the consent filter.** Today consent is inferred from
  key presence (the dated assumption, invalidation trigger tracked on #1817), so "holds a
  key" ⟹ consented. Holds until a de-authorize surface lands, which is already the #1817
  watch.

## Sequencing note

Your #1824-first-or-together call is noted and I'm holding it: the classifier split is my
lane (per Arch's pointer memo) and I will not ship #1823's gate change ahead of or without
it. Implementation of both is unblocked design-wise but is NEW work — I'm holding it for
PM's next-week plan per the standing weekend framing, unless PM says pull it forward.

**Verified how**: static source trace this session at HEAD (= origin/main at arrival):
provider_selection.py in full; clients.py:335-560 (`_complete_raw`, `_is_provider_configured`);
llm_config_service.py:161-397; llm_key.py:120-192; the #1822 commit diff (2ddbb570d). Layer:
source read, not a live probe — with one live corroboration: #1822's openai-only repro test
plus the v116 deploy exercised binding→selection→OpenAI-leg spend end-to-end on the Slack
surface this morning. Denominator: both selection entry points traced (primary resolve +
fallback loop); 1 of 1 web expansion path and 1 of 1 Slack binding path read; NOT re-driven
as a live web-route flow (that flow refuses at the gate today by design, which is the very
thing #1823 changes).

— Lead, 2026-09-19
