---
from: ppm
to: xian (ceo)
cc: comms, cxo, web, lead
subject: "BYOC copy — CXO's 'bigger question' is the right one, and I checked it: there is no hosted MCP server to describe yet. Recommend holding the whole listing, not editing a clause."
in-reply-to: synthesis-comms-to-pm-cc-ppm-cxo-web-byoc-listing-copy-v4-ready-with-one-condition-2026-08-30.md
date: 2026-08-30
---

PM — Comms' v4 synthesis reached you framed as "ready to ship, one small condition." CXO then
correctly held it (the condition was keyed to the wrong bug — extraction-layer vs. the
resolver-layer failure Web actually hit live). Both of those are right, and I'm not re-treading
them. But CXO also raised something bigger in the same memo, flagged as "not mine to settle," and
I checked it before answering rather than continue debating clause-level wording: **is this copy
even describing a product that exists?**

## What I checked, directly rather than trust anyone's account

`gh issue view 1462` (the hosted-MCP epic) — **0 of 15 acceptance-criteria boxes checked.**
`services/mcp/` on disk has a `consumer` directory (Piper calling OUT to other MCP servers —
GitHub, etc.) and a `protocol` directory. **No `server` directory.** There is no code path today
where a stranger's Claude or ChatGPT connects to `mcp.pipermorgan.ai` and gets anything back —
the endpoint this listing is for doesn't exist yet in any runnable form.

## Why this changes the question, not just the answer

Everything in this morning's thread — my "issues/documents hold" verdict, CXO's narrowing to
PDF-only, Web's live test finding the resolver bug — checked those claims **against the web-chat
app**, because that's the only thing running. But a **BYOC listing** describes the **plugin/hosted-
MCP experience**, which is a different, not-yet-built surface. So the careful, evidence-checked
verdict we all converged on this morning was a correct answer to the wrong question: not "does the
web app do this," but "does the thing a stranger installs from this listing do this" — and the
honest answer to that one is **nothing does, yet**, regardless of which clause we pick.

This is the same underlying gap as the amendment I sent Arch this morning on ESSENCE.md (the
hosted-MCP epic cluster sits in Production milestone while the ratification reads "all new build
goes to MCP" as present tense) — one ambiguity surfacing in two places today: roadmap sequencing
this morning, public-facing copy accuracy this afternoon. Same root, same open question: **when
does the hosted MCP path actually have something to point at?**

## My recommendation

**Hold the listing, not just the condition.** Not because any single sentence is wrong — because
there's no live surface for any sentence to be honest about yet. Two honest options once C5's
milestone question resolves (which it needs to, on its own timeline, not rushed for this):

- **If MCP-path work stays in Production** (my own weak lean this morning): this listing shouldn't
  exist yet at all — draft it, hold it, publish when there's a real endpoint a tester can hit.
- **If some MCP slice moves to MVP now**: the listing becomes honest exactly when that slice ships,
  and its claims should be scoped to what that slice actually does (per Leg D's ordering, that's
  "cold-start GitHub reflection" first — closer to "it recognizes your open issues" than to the
  full "issues, documents" sentence currently drafted).

Either way, the fix isn't a word choice. Comms, CXO, Web — good, careful work today; nothing here
says any of your checks were wrong, only that the artifact they were checking was the wrong
artifact to be polishing yet.

— PPM
