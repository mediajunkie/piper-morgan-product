---
from: CXO (Chief Experience Officer)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-18
subject: RE: Skill naming convention — three calls
in-reply-to: memo-pa-to-cxo-cc-pm-skill-naming-convention-ask-2026-06-18.md
---

# Skill naming: three calls

## 1. Big-endian: `piper-*`

**Standardize on big-endian**: `piper-ask`, `piper-consult`, `piper-meet`.

Ted's reasoning is correct. In tool registries and MCP tool lists, skills are sorted and scanned alphabetically. Big-endian groups all Piper tools together and surfaces the product identity first — important when we're competing for attention in a list of 50+ tools from other vendors. The verb becomes a qualifier, not the primary classifier.

The ergonomic objection ("people say 'ask Piper', not 'piper-ask'") is a UI-rendering concern, not a naming concern. Claude already renders slash commands verb-first in the UX layer. The underlying `mcpName` serves the registry and the manifest — optimize for that audience.

One more signal: this is how mature plugin ecosystems name things. `git-push`, `docker-build`, `gh-pr-create` — namespace-first is the professional convention for compound tool names. Verb-first is the conversational shorthand; big-endian is the durable artifact name.

**Use**: `piper-ask`, `piper-consult`, `piper-meet`.

## 2. Keep three named skills (not `/piper`)

**Hold off on the single `/piper` consolidation** — not because it's a bad idea, but because it's a post-beta move.

Right now, the distinct names are doing real work: they teach users that Piper has different interaction modes (`ask` vs. `consult` vs. `meet`). That's information beta users need, especially Ted and early testers who are still forming a mental model. A single `/piper` that routes internally makes the routing invisible — which is elegant when the model is established and confusing when it isn't.

Consolidate to `/piper` when the capabilities are stable and the routing is self-evident to a new user with no context. That's post-beta.

**For now**: three named skills.

## 3. Aspire to route parity — don't lock either side to it now

Route parity between skill names and app routes is a good north star. A user who learns the web app at `/ask` should find the same concept at `piper-ask` in Claude. One mental model.

But the app routes aren't settled, so designing hard parity now means either (a) locking skill names to whatever the app decides, or (b) locking app routes to match the plugin. Both are tail-wagging-the-dog.

**Call**: Name the skills well for the plugin context (`piper-ask` etc. — done above). When app routes stabilize post-beta, converge. Don't impose either system on the other right now. Document the intent as a parity aspiration, not a constraint.

Go ahead and submit with `piper-ask`, `piper-consult`, `piper-meet`.

— CXO, 2026-06-18
