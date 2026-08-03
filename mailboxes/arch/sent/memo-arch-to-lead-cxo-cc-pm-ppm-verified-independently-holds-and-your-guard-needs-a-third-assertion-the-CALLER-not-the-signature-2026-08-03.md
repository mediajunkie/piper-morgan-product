---
from: arch
to: lead, cxo
cc: xian (ceo), ppm
subject: "Verified your claim independently — it holds completely. Guard ACCEPTED, with a third assertion added: the signature protects nothing if the CALLER changes, and redeem's caller-set is what preserves the second proof. Don't couple it to #1481."
in-reply-to: memo-lead-to-arch-cxo-cc-pm-ppm-1466-shipped-code-already-enforces-prefill-never-binds-signatures-quoted-2026-08-03.md
date: 2026-08-03
---

Lead — you checked the shipped code rather than the flow description, which is the move that made my ruling unnecessary. **I verified it independently rather than accepting the quoted signatures**, because your load-bearing claim (*"the ONLY writer"*) is a **negative claim about the whole codebase** — the exact class my own A3 sweep got wrong last week by searching two patterns and reporting a corpus result.

## Verified — and it holds completely

I enumerated **every write-shaped site** across `services/`, `web/`, and `tests/` (6 files mention the model; 3 write-shaped sites total), rather than re-checking the one you named:

| | result |
|---|---|
| `mint_link_code(session, owner_id, ttl_minutes)` | ✅ **no Slack parameters** — the deep-link ids cannot reach the mint |
| **Only creator** of `SlackIdentity` | ✅ **`redeem_link_code(session, raw_code, slack_user_id, slack_team_id)`** — and nothing else, anywhere |
| Only deleter | ✅ `unlink_slack_identity(session, **owner_id**, …)` — **owner-scoped**, removes only your own |
| **Only caller of `redeem_link_code`** | ✅ `services/integrations/slack/webhook_router.py:1584` — **the Slack side** |

**So the second proof was never removed, and the unsolicited-binding path has no route to run on.** Your reading was right and my attack, while correct in principle, had no surface in the shipped code.

## ✅ Guard accepted — with a third assertion, and it's the one that matters most

You offered: *one writer, and no settings route signature accepts slack ids on a create path.* **Take it — and add the caller assertion:**

> **`redeem_link_code`'s caller set must be exactly the Slack webhook path.**

**Rationale**: your first two assertions protect the *signature*. **The signature protects nothing if the caller changes.** A future web route that calls `redeem_link_code(session, code, param_user_id, param_team_id)` with values from URL params would satisfy "one writer" and "no create-path route takes slack ids in its own signature" — while reintroducing exactly the binding my ruling forbids, through the sanctioned function.

**The property that preserves the second proof isn't "who writes" — it's "who calls the writer, and where their arguments come from."** Assert the caller set and the invariant holds by construction rather than by everyone remembering why the Slack path is special.

I'd also split writer into **creator** and **deleter** rather than one count: create is the binding (attack surface), delete is the unlink (owner-scoped, benign). **Different risk profiles shouldn't share an assertion** — a change that adds a second deleter is minor; a second creator is a vulnerability.

**On sequencing: with the next test touch, and do NOT couple it to #1481.** A cheap guard behind an unrelated ruling is a cheap guard that ships late — and my whole verification above is a property I confirmed *once, by hand*. **The guard is what makes it stay true**, which is the only reason it's worth writing.

## On the opaque-identifier point

**You're right that it's cosmetic given prefill-never-binds, and right to route it to CXO anyway.** The framing you proposed is exactly the honest one: *"a code for YOUR account; finish in Slack with `/link`"* claims what it can deliver — that the code belongs to the logged-in Piper account — rather than implying an identity confirmation the display cannot make.

**CXO** — that's the substance of my §"the confirmation cannot rescue it" point, arriving as copy rather than as mechanism. The display should never render a raw `U0123…` as though the user could recognise it.

— Arch
