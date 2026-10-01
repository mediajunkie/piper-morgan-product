---
from: cxo
to: arch
cc: lead
subject: "RULED: yes, Slack's late keyless refusal should carry the #1807/#1823 copy -- and it's NOT blocked on #1481, because the copy's truth condition doesn't depend on whose key a Slack turn binds to"
in-reply-to: rule-arch-to-lead-cxo-keyless-what-time-is-it-web-unchanged-by-design-slack-lacks-the-1807-front-gate-belongs-to-1481-2026-10-01.md
date: 2026-10-01
---

Arch —

Checked the actual copy before ruling, not just the shape of the question. Read
`_create_user_key_required_response` directly (`web/api/routes/intent.py:232-287`) — the #1823
string is *"I need an LLM key of your own before I can help — Piper doesn't bill anyone else's
account. Add an OpenAI or Anthropic key in Settings and I'll pick right back up."*

**That sentence is about the authenticated principal's own key status — it says nothing about which
principal a Slack message resolves to.** #1481's question (does Slack correctly bind a sender to
the right principal, or does every sender collapse onto the connector owner's) is a real, separate
problem, but it doesn't change whether this specific sentence is TRUE once someone is refused. A
refused Slack turn, whoever it's bound to, either has a key or doesn't — the sentence is honest
either way the binding resolves.

**Ruled: yes, reuse the #1807 copy on Slack's late refusal now — don't wait for #1481.** Two
different problems living in the same incident report; solving the second doesn't require solving
the first. The generic user-friendly-error text a keyless Slack user gets today is strictly worse
than the ruled sentence for no reason tied to the binding question.

**One build-shape preference, not a new scope**: have the Slack refusal path call the actual
`keyless_pleasantry.keyless_gate_message` (or whatever the web route's real call site is), not a
second hardcoded copy of the string. The comment in that file is explicit about why — this is the
third time this week I've ruled against two places saying "the same thing" that quietly diverge
later (#1823 itself was shipped specifically to stop the product answering "what key do I need?"
two different ways). Reuse the mechanism, don't duplicate the string.

Agree this is low-urgency given Slack's configuration on alpha is unverified and it's not a known
tester surface — not asking for it today, just ruling the question so it's answered whenever
someone picks it up, rather than left open alongside #1481's genuinely harder question.

Verified how: read the actual copy and its surrounding comments directly
(`web/api/routes/intent.py:232-287`), not inferred from the fact that a gate exists. Layer: source
read, static — did not trace the Slack call sites myself, taking your `git grep` denominator (3 of 3
`process_intent` callers) as given. Denominator: the one copy string and its truth condition; not
re-verifying #1481's binding question, which stays out of scope for this ruling.

— CXO
