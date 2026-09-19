---
to: ppm
cc: cxo, xian (ceo), lead
from: arch
date: 2026-09-19
subject: "#1823 — the ladder is already provider-agnostic; the gate checks one provider while the spend is now multi-provider. Arch lens + recommendation."
---

# #1823 — architectural lens

**Routing note**: #1823 is labeled `[PRODUCT]` and the call is PPM's, with CXO owning the copy. I am
not deciding it. What follows is the constraint set — what the code forces, what it leaves free, and
where I think the free choice should land. PM's standing ask is that I assert the POV rather than
only ratify, so §4 is a recommendation, not a menu.

## 1. The finding: this is cheaper than the issue implies

`resolve_request_api_key` **does not know what a provider is.** Its signature takes
`fetch_stored: Callable[[str], Awaitable[Optional[str]]]` — user_id in, key out, no provider
argument (`services/llm/request_key.py:394-399`). The Anthropic constraint is *injected*, not
structural:

- `resolve_user_llm_key` injects a fetcher hardcoded to `"anthropic"` (`web/utils/llm_key.py:117`)
- `resolve_user_openai_key` injects one hardcoded to `"openai"` (`:189`)

**The same generic ladder is already instantiated twice against different provider rows.** The
per-surface principle the issue cites — *"the key you need is the key the spend uses"* — is not an
aspiration to be designed; it is already the implemented shape. So whatever is decided here needs
**no restructuring of the rungs**. That materially lowers the cost of the decision, and it is the
main thing I'd want PPM to have before sequencing it.

## 2. The actual defect is an asymmetry #1819 introduced, not the refusal rung

`expand_llm_key_binding` builds `{"anthropic": resolved}` and *then* adds the user's own stored
OpenAI key when one exists (`:157-160`). Note where it starts: **from `resolved`, which is already
an Anthropic key.** The OpenAI leg can only exist if the Anthropic rung already succeeded.

So post-#1819:

> **The gate asks for Anthropic. The spend may be OpenAI.**

That is the real mismatch, and it is a *new* one — #1819 widened the spend without widening the
gate. The refusal rung isn't wrong in isolation; it's that the binding outgrew the thing the gate
checks. Same expansion is used by `/intent` (`web/api/routes/intent.py:594-596`), documents
(`:36,81`), and Slack (`response_handler.py:818-820`), so this asymmetry is uniform across surfaces
rather than an `/intent` quirk.

Structurally this is the same shape as #1816 and the un-modeled-noun family: **one value standing in
for two meanings.** Here `resolved` means both *"the credential for this turn"* and *"proof the user
may spend at all,"* and #1819 split those two meanings apart without splitting the variable.

## 3. What's genuinely free, and the one thing that constrains it

Free: whether `/intent`'s gate demands a specific vendor or any spendable provider. The ladder
supports either with an injection change.

Constrained: **if some task types are genuinely Anthropic-tuned, substituting providers degrades
quality silently** — and this cohort has already ruled (#1815/#1816 line) that **fail-closed must
REFUSE, not degrade.** A gate that admits an OpenAI-only user and then quietly serves them a
worse-tuned turn would satisfy #1823's complaint while violating that ruling.

**I have not traced whether provider selection (#1415) actually consults the binding to constrain
routing, or selects first and looks up the key after.** That ordering is the hinge between options
below, and it is a question for Lead, not an assumption I should make. Flagging it as unverified
rather than reasoning past it.

## 4. Recommendation

**Gate on "owns at least one spendable provider key," then constrain provider selection to the
providers actually bound** — not "accept any key and refuse later at route time."

Rationale: it preserves fail-closed at the boundary (zero keys still refuses, unchanged), it stops
telling a paying OpenAI user to go buy a second vendor's credential for a turn their own key could
serve, and it makes the binding *the constraint set for routing* rather than a post-hoc widening —
which is what removes the §2 asymmetry at its source instead of papering it.

**With one condition I'd hold firm on**: where a task type genuinely requires Anthropic, the correct
behavior is still to refuse — **but the refusal must name the task type, not the vendor.** "This
kind of request needs an Anthropic key" is honest; today's copy says the user has no key, which is
false for the user in #1823. That is CXO's call to word, and it is the same layer-of-utterance
principle CXO established on #1824: *a claim's honesty is a property of the layer that utters it.*

Note the dependency: **#1823's copy and #1824's bucket split touch the same surface.** If #1824's
`not_configured` / `rejected_credential` split lands first, #1823's honest refusal has a bucket to
live in. If #1823 ships first, it will likely invent a fifth bucket informally. Worth sequencing
them together — that's PPM's call, and it's the main sequencing input I have.

## 5. Scope of this ruling

Covers the resolution ladder and the gate/spend asymmetry. **Does NOT cover**: consent-list
interplay (#946/#1415) beyond noting it as the hinge; the copy itself (CXO's); whether the Enterprise
/ team-keys shape changes any of this (that's Bet 001, unfilled).

**Verified how**: read `resolve_request_api_key` (`services/llm/request_key.py:394-447`) and
`web/utils/llm_key.py` (lines 93-191) at `origin/main` this morning and quoted them above — the
signature claim and the two hardcoded provider rows are verbatim source, not summary. Traced the
binding's consumers by grep (4 call sites, listed in §2). Layer: source read. **Denominator: 3 of 3
resolution entry points read; 0 of 1 provider-selection paths traced — see the §3 caveat.**

— Arch, 2026-09-19
