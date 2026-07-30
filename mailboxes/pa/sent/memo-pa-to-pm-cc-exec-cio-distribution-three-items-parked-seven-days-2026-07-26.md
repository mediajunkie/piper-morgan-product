---
from: pa (Piper Alpha)
to: xian (ceo)
cc: exec, cio
subject: "Three distribution items have been parked on you for 7 days — two of them are 5-minute unblocks with external lead time. Re-verified today; the picture actually changed in a way that makes the two quick ones MORE urgent, not less."
date: 2026-07-26 13:00 PT
---

> ## ⛔ CORRECTION 2026-07-29 — THE OPEN-SOURCE "DECISION" IN THIS MEMO DOES NOT EXIST
>
> **The repo has been PUBLIC the whole time.** Verified 2026-07-29:
> `gh repo view mediajunkie/piper-morgan-product` → `"visibility": "PUBLIC"`, `"isPrivate": false`.
> So the "hard requirement: public GitHub repo" for the plugin track **was already satisfied**, and
> every downstream framing of this as a pending PM decision was wrong. **PM had answered it multiple
> times.** It kept regenerating because this memo said it was open and nobody ran the 30-second check.
>
> **Also superseded here**: the Team/Enterprise framing. Chat now installs plugins on all paid plans and
> plugins bundle skills + connectors + MCP, so the connector track's unique audience has collapsed and
> **Team is dropped, not deferred.**
>
> Canonical: `dev/active/distribution-submission-tiers-resolved-2026-07-26.md`. — PA

PM — first PA session on Amber. Predecessor went dark 7/19 after a clean close; no handoff exists,
so I picked this up from artifacts. **Routing this to you directly rather than via Exec** — the
7/19 version went to Exec for relay and has sat a week. Not Exec's failure; the relay hop just
isn't the right shape for something whose whole cost is elapsed time.

## The three items, re-verified today

From PA's 7/19 plugin-directory research (`mailboxes/pa/sent/2026-07-19-pa-to-exec-cc-pm-plugin-directory-research.md`):

| # | Item | Blocked on | Time to unblock |
|---|---|---|---|
| 1 | **Claude Track A** — connector listing (hosted MCP URL only) | Verify Piper Morgan's claude.ai account tier. Requires **Team or Enterprise**; individual/Pro can't reach the submission portal. | ~5 min |
| 2 | **ChatGPT** — remote MCP listing | **Start OpenAI identity verification.** No other dependency. Individual accounts can verify; no company entity needed. | ~15 min to start, then external wait |
| 3 | **Claude Track B** — full plugin (CLAUDE.md + hooks + skills) | Your call on **open-sourcing** that package. Public GitHub repo is a hard requirement. | a decision, not a task |

## What changed since 7/19 — and why it cuts toward acting now, not later

I checked rather than restating a week-old memo:

- **`mcp.pipermorgan.ai` is not deployed.** It appears only in PDR-006 and planning docs. No Fly
  service, no endpoint.
- **No public privacy policy page exists** on the site (only in-app privacy *settings* templates).
  Both directories require one.

So the *submission* itself is further out than the 7/19 memo implied — the server needs to exist and
be stable for a few weeks before either directory will accept it.

**That is precisely the argument for doing #1 and #2 today.** They are the only long-external-lead-time
steps, and they're the only two that don't depend on the server existing. Every day they sit is a day
added to the end of the chain, not absorbed by it. The prep work (server, annotations, privacy policy)
can run in parallel — but only if the verification clock has already started.

- **Item #1 may have a different answer now.** The cohort migrated to the pipermorgan.ai account on
  7/25. Whatever the tier was on designinproduct.com on 7/19 doesn't answer the question for the
  account you're on today. Worth a fresh look regardless of what you remember.

## What I'd ask of you

Two things, both small:

1. Check the claude.ai account tier for pipermorgan.ai (Team/Enterprise vs. Pro).
2. Start OpenAI identity verification.

Item 3 (open-source decision) is not time-critical in the same way — it gates only Track B, and
Track A gets us a Claude listing without it. Happy to write up the tradeoffs if that would help.

## What I'll advance without you

Unless you say otherwise, I'll pick up the shared prep that doesn't need your input:
privacy-policy draft, the tool-annotation requirement (`readOnlyHint`/`destructiveHint`) as a spec
against the eventual MCP tool catalog, and the docs/logo/test-account checklist. None of that is
blocked and all of it is needed for both directories.

## One adjacent item, also stale

**PDR-006 is still "Arch/CXO/PPM review pending."** Arch acked on 7/19 promising a dedicated read
"next fire" and flagged a real coupling — the colleague-model question overlaps the live spatial
committed-theory review. Seven days, no review memo from any of the three. I'll ping them; noting it
here because PDR-006 gates the implementation epic.

— PA
