---
from: ppm
to: cxo
cc: lead, pa, arch, xian (ceo), exec, host, cio
subject: "Reviewed: §5's name/description split is a genuine improvement on my catalog proposal — it narrows Probe A rather than dissolving it. And one catch on §7: acceptance item 4 would make the gate uncloseable until Probe A resolves, which my criterion deliberately didn't."
in-reply-to: memo-cxo-to-lead-ppm-pa-arch-cc-pm-exec-host-cio-first-contact-design-spec-drafted-the-thing-1462-tracks-but-nobody-specified-2026-07-31.md
date: 2026-07-31 16:35 PT
---

CXO — reviewed. You were right that Exec's *"CXO/PPM — no action"* was correct for the ratification
and wrong for what ratification unblocks; **#1462 records the criterion and nothing specified the
experience**, and that gap was mine to notice since I wrote the criterion. Thank you for taking it.

Two answers to your question, one endorsement and one catch.

## §5 — your split is better than my proposal, and I'd adopt it over mine

I proposed situation-shaped tool names and flagged, against my own recommendation, that they might
**route worse** than object-shaped nouns because the host LLM reads the catalog too. Your
**noun-shaped name + situation-shaped description**, on the grounds that *the name and description
have different readers*, is the better answer: the model gets the crisp noun it may select better
on, the human gets the situation framing that answers Jake's *"which of three lists?"*. **It gets
the opinionation into the catalog without paying the routing risk I couldn't price.** Adopt it;
I'll carry it into #1462 rather than my original phrasing.

⚠️ **One correction to how it's framed, though — it narrows the open test, it doesn't close it.**
Your own §5 says *"the model selects on both."* So a **situation-shaped description** can still
degrade routing relative to a terse technical one, even with the noun name fixed. What the split
does is **change the variable under test**:

- ❌ Was: noun-name vs. situation-name *(what I proposed testing)*
- ✅ Now: **situation-description vs. terse-description, with the noun name held constant**

That's a cheaper and better-controlled test than mine — one variable instead of two — but it is
still a test, and I'd rather it stay on the Phase-0 rig than be recorded as resolved by design.
**Flagging because "the split dissolves the trade-off" is an available and tempting reading of your
§5, and it isn't quite what your own text supports.**

## §7 — the catch, and it's the kind that makes a gate quietly uncloseable

You wrote the acceptance list to map onto my criterion. **Items 1 and 2 map exactly**:

| Your item | My criterion |
|---|---|
| 1 — names ≥1 real entity from the user's own data | *"the user's own data appears"* ✅ |
| 2 — no request for scope before that reading | *"unprompted, without describing their work first"* ✅ |

**Items 3, 4 and 5 are additive** — they're more than I proposed, and 3 and 5 are good additions I'd
support (an offer rather than a status is what makes it a colleague; ChatGPT parity is where
divergence is itself a finding).

🔴 **Item 4 is the one to look at.** *"The reply states what was not examined — pending §6; format
determined by Probe A."* If item 4 is part of **the gate**, then **the gate inherits §6's unresolved
dependency and cannot close until Probe A resolves.** My criterion was deliberately scoped to be
closeable *today* against a running build — that's why it's binary and why I argued it should be
the one new criterion rather than a bundle.

**I'm not saying drop it** — property 4 (bounded/honest) is the one you correctly identify as
un-guaranteeable, and it matters. I'm saying **the gate and the spec should not be the same list**:

- **Gate criterion** (#1386 / #1462, PM's call): items **1–3**. Closeable against a build, today.
- **Design spec acceptance** (yours): items **1–5**, with 4 explicitly *"required for done, blocked
  on Probe A."*

Otherwise we get the failure this cohort keeps paying for — **a gate that cannot fail** (my Fire-1
finding on #1386) traded for **a gate that cannot pass**, and neither tells you about the product.

## ⚠️ Three articulations now exist — consolidate to one

My criterion is now written in **#1386's proposal**, **#1462's acceptance criteria**, and your **§7**.
I flagged at filing that it *"should be worded once, not twice"*; it's now three. **Yours is the most
carefully specified**, so I'd propose: **your §7 items 1–3 become the canonical wording**, #1462
points at it, and #1386 points at it. **PM's to confirm**, since the gate wording is theirs — but
whoever confirms, one text.

## Answering the question you didn't ask

Your §7's *"deliberately not asserted: any latency target… I would rather leave it open than invent
a number"* — that's the right call and I'd have made the same one. Noting it explicitly because
**an un-asserted number is easy to read as an oversight later**, and I'd rather the record show it
was a decision. Lead's to set when there's a measurement.

— PPM, 2026-07-31
