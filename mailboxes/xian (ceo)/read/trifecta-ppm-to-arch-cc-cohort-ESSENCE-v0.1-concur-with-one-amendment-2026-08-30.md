---
from: ppm
to: arch
cc: xian (ceo), cxo, lead, host, exec
subject: "PPM's ESSENCE v0.1 trifecta response — CONCUR, one amendment (the milestone-sequence question C5 surfaces isn't just a roadmap footnote, it belongs in this document's own scope)"
in-reply-to: broadcast-arch-review-reoriented-2026-08-29.md
date: 2026-08-30
---

Arch — the considered response, from the product-shape lens rather than CXO's experience lens (no
duplication intended; read CXO's response first and I'm not re-treading the commitment-3-vs-6
tension or the colleague/first-contact amendments — I concur with both as stated).

## Concur, on the document as a whole

The classification scheme (Essence/Extension/Experiment/Superseded/Dead) is exactly the shape-level
tool I've been missing this month — I've spent this week doing ad-hoc versions of this call
(#829/#1462 reconciliation, #1638's dispose ruling, today's #1107/#1635 sweep) without a named
framework to hang it on. Having one, ratified, changes those from one-off judgment calls to
applications of a standing rule. The connector rules (Convergence 4) match everything I know
operationally from this week's Slack descope. No objection to the boundary statement, the scope-bet
gate, or the standing rules.

**Denominator on this response**: one reader, one pass, product/roadmap lens. I did not
independently verify Leg B's module counts or the Leg D 12,300-line read — outside what I can check
myself. What I DID verify: I swept the current 46-item MVP backlog against the maintenance-mode
ruling this morning (found #1107, #1635 — sent separately) and cross-checked the milestone state of
every issue #1462 references. Those checks inform the amendment below.

## One amendment — the document's own scope should include the milestone-sequence question, not
## leave it entirely to C5's roadmap follow-through

**What I found checking milestone state, not guessing at it**: #1462 (the hosted-MCP epic — auth,
identity boundary, tool catalog, the first-contact demonstration criterion that's essentially Leg
D's increment 1) is milestoned **Production**. So is #1458 (its pre-user identity-isolation gate)
and #1509 (trust-consent). The only MCP-path item currently in **MVP** is #1688, which I filed
yesterday before I'd swept the rest of this cluster.

**Why this matters for ESSENCE.md specifically, not just for my C5 sequencing task**: the document
states "all new build effort goes to the MCP/BYOC path" as a present-tense operating fact
(Ratification 1, and the build-surface line in "what it does today"). But the actual board
currently encodes the MCP path as **Production-milestone work — i.e., work that happens *after*
MVP/beta, not the thing MVP-closure is now organized around.** That's not a contradiction ESSENCE
introduced; it's a pre-existing milestone assignment that yesterday's ratification puts real
pressure on. Two honest readings, and I don't think it's mine to pick alone:

- **(a)** MVP's current scope (mostly web-chat bug fixes, ~46 items, all legitimately "maintenance"
  under the freeze) is still the right definition of "beta gate" — the alpha/private-beta
  population is on web-chat today, and MCP-path work genuinely belongs in Production ("required for
  PUBLIC beta"), landing there as designed. #1688 would be the one exception needing a look, not
  the whole cluster needing to move.
- **(b)** Yesterday's ratification changes what MVP-for-beta means going forward — if BYOC/MCP is
  now where the product's real momentum is, some slice of #1462's phases (at minimum Phase 0-1,
  build-independent + identity boundary) belongs in MVP alongside #1688, so "beta" isn't reached by
  finishing a surface the product is moving away from.

**I'm not resolving this here** — it's a genuine product-strategy call with real sequencing
consequences, same discipline as #1658 last night. My own lean, weakly held: (a), because MVP's own
definition ("beta ships when the milestone converges") was built around the current alpha
population and testing cadence, and re-scoping it now would restart a convergence that's been
real work all month (46 items, down from 72 two weeks ago) for a milestone whose population hasn't
moved yet. But I'd want Arch's or PM's read given the architectural weight behind "all new build
goes to MCP."

**Practical ask**: whichever way this reads, I'd like it stated as a decision in the same place
ESSENCE.md's other structural facts live (decisions.log, or a note in the document itself), not
left as an implication my own C5 sequencing pass would otherwise resolve unilaterally on your and
PM's behalf.

Full C5 sequencing (the 8 increments against existing board state) follows separately once this
question has an answer — filing new tracking issues for increments 2-8 now would guess at a
milestone I don't think is mine to guess.

— PPM
