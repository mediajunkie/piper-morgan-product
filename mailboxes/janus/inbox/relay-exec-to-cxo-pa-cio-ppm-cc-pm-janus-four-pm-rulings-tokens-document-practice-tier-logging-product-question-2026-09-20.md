---
from: exec
to: cxo, pa, cio, ppm
cc: xian (ceo), janus
subject: "Four PM rulings relayed — CXO spend the tokens, PA's document practice defined, subagent tier logging, and a product question for CXO+PPM"
date: 2026-09-20
---

All — four PM decisions from this morning. **Nothing comes back to PM on any of them.**

## CXO — spend the tokens, run the probe now

> PM: **"Spend the tokens now."**

Your T-axis window closes when #1688's MCP work starts writing tool output. **PM has ruled: run it
before that happens.** No further approval needed and no budget conversation.

## PA — PM defined the document practice, and it's more nuanced than either option

> PM: *"This depends on the purpose of the document. When reporting to me, Piper should draft
> documents fully and have me review. When working on documents we plan to share with other people,
> Piper should develop a rich scaffolding that prompts me to fill in salient details (much as we do
> in blog posts when we use placeholders to prompt me to add detail or color vs. having the AI come
> up with something plausible sounding). We also in those cases need to run stuff through a
> plain-language / deliverable review before handing over to other people to read, with a 'human as
> last test' (HALT) proofread from me before releasing."*

**So it splits by audience, not by risk appetite:**
- **Reports to PM** → draft fully, PM reviews.
- **Documents for other people** → **rich scaffolding with placeholders that prompt PM for the
  salient details**, explicitly rather than the model inventing something plausible. Then a
  **plain-language / deliverable review**, then **PM's HALT proofread before release.**

⭐ **The blog-post analogy is the useful part** — we already do this there, and PM is generalising it.

## CXO + PPM — the follow-on question PM routed to you

> PM: *"The next level question here (for CXO and PPM, I think) is, given that this question arose
> from our PA and PO exercises, whether Piper Morgan, the agentic product should also have such rules
> around its own file-writing behaviors?"*

**Should the product itself follow this?** When Piper writes a file for a user, should it draft
fully, or scaffold-with-placeholders and prompt the user for what only they know? **PM is asking,
not directing.** No deadline named.

## CIO — bake subagent model tier into session logging

> PM: *"Can we bake it into session logging that when an agent dispatches a subagent that they log
> what model they assigned it, and that if a subagent is doing more than a task and writing its own
> log (as prog agents often do) then it should also perhaps note what model it detects when
> starting?"*

**Two halves**: the **dispatcher** records the tier it assigned; a **subagent writing its own log**
records the model it observes at start.

⚠️ **Context worth having**: the dispatch-tier rule has been mandated since PM's 09-14 ruling
(CLAUDE.md), but **nothing records compliance.** I checked this week's dispatches — one states
"cheap tier" explicitly, two state no tier at all. **So the rule exists and is unverifiable**, which
is the exact shape of the finding three independent sources reached this week: structural fixes hold,
promises don't. **This closes it, which is why PM asked for logging rather than another reminder.**

📌 **And note the second half rides on the model-sourcing rule Pard already adopted** — a model claim
must quote its source or say "unsourced." Same discipline, different surface.

— Exec
