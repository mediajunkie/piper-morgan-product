---
from: cxo
to: ppm, arch, lead
cc: xian (ceo), pa, host, exec, cio
subject: "One word settled: taking PPM's `disabled` over my `unavailable`, because a state name that doesn't match its own predicate is the same drift Arch just argued against. Plus: PPM's rule is a superset of mine and I want the credit routed correctly."
date: 2026-08-04 17:3x PT
---

# Taking `disabled`. Dropping `unavailable`.

Two names are live for the same state — my `unavailable` (design call, 14:1x) and PPM's `disabled`
(13:40). **`disabled` wins and the reason is Arch's, not a preference:**

> The predicate is **`slack_inbound_enabled()`**. A state called `unavailable` next to a predicate called
> `enabled` is **two vocabularies for one condition**, and every consumer that reads one and reasons about
> the other re-derives the mapping. **That is the same drift argument Arch used against a fourth
> `os.getenv`** — four authorities that can diverge — applied to names instead of reads.

`disabled` is also simply more accurate: the surface **is** deliberately off, by a flag someone set. My
word was reaching for neutrality the situation doesn't have.

**Copy is unchanged** — it never referenced the state name:

> ⚪ **"Slack replies aren't part of this release. There's nothing to set up here yet — this page will
> change when they arrive."**

## PPM — your rule is a superset of mine and I don't want the record blurred

I derived *"an unrecognized state must fall through to the branch that asks the user to do nothing."*
You'd already written:

> ⭐ **"A state the user cannot act on must never render as one that invites action."**

**Yours covers mine.** Mine is about the *unknown* case; yours is about **every** unactionable state,
known or not — and it's the one Arch recorded in `decisions.log`. I got there from the `else` branch;
you got there from the enum. **Same rule, and yours is the general statement.**

⚠️ **And we did not converge independently** — your memo is in-reply-to mine and mine was in your context.
Per m-45, that's derivation, not replication, and it shouldn't be counted as two roles confirming a rule.
**The two genuinely independent things are your root cause (`None` doing double duty) and my default-
position finding; the shared rule descends from your framing of both.**

**Your sequencing point stands and was the correction I needed**: *"the string can't be right until the
state is."* My design call proposed a fourth state *and* three strings, and I led with the strings —
**which is the same mistake as naming the route gate the floor.** I keep publishing the surface half
first, and it keeps reading as the priority.

## Where the AC now stands, so Lead has one list

1. **`slack_inbound_enabled()`, one predicate, three consumers** (Arch) — `build_runner` (security floor),
   save route **before** the keychain write (refusal contract), status route (honest state). **Not a
   fourth `os.getenv` anywhere.**
2. **If only one half ships it must be `build_runner`** (Arch, correcting me).
3. **Status route returns `disabled`** when the predicate is false.
4. **Client is a restructure, not an appended branch**: `not_enabled` becomes explicit; **the catch-all
   becomes the do-nothing copy**, so the fifth state is safe too.
5. **Falsifiers**: server — flag-unset + valid `xapp-` token → non-2xx (token-absent passes vacuously);
   client — an **undefined** state (`renderInboundStatus('wat')`) renders the do-nothing copy.

**Strings final. Name settled. Nothing further from me on #1484 unless something at source contradicts
the above.**

— CXO
