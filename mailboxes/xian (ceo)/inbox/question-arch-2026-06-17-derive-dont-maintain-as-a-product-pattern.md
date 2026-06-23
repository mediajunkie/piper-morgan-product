---
from: Chief Architect (arch-code-opus)
to: xian (ceo)
date: 2026-06-17
type: question-box (Letters convention — AI prompts human)
topic: derive-don't-maintain as a *product* pattern, not just an internal one
---

# A question from today's ADR-072 work

The load-bearing idea in ADR-072 today wasn't really about skill-routing. It was the realization that the routing metadata should be **derived from one source** (the SKILL.md frontmatter) and fed to every consumer, rather than hand-maintained in three places that inevitably drift. The proof was sitting right there: our own `SKILLS.md` index was already a month stale. Same shape as the mailbox MANIFESTs we made derive-only (#1106), the stale briefings, the status docs nobody updates. Pattern-073 — "documentation-asserted-behavior drift" — is the whole family. The cure each time is the same: *make drift impossible by construction; derive, don't maintain.*

Here's what I keep circling, and it's a genuine question, not a rhetorical one:

**We keep discovering this principle for *ourselves* — our process, our infra. But the people Piper Morgan serves live in exactly this drift, all day.** The spec that no longer matches the code. The roadmap that's three weeks behind the truth. The status doc updated the night before the review and stale by morning. A PM's job is half *narrating a moving target* — and the narration rots the instant they stop hand-feeding it.

So: **do you see "derive-don't-maintain / make-drift-impossible-by-construction" as something Piper should eventually do *for* users** — not just *describe* a PM's world but *derive* the parts that drift (status from the source of truth, so the PM stops maintaining a rotting doc)? Piper already wants to be the thing that catches itself (Ship #047). Is "catch the *user's* drift the way we learned to catch our own" a real product direction —

or is it too prescriptive? PMs may *want* to control the narrative — the hand-written status doc is sometimes a political artifact, not a truth artifact, and auto-deriving it removes a lever they use on purpose. Maybe the drift is a feature of how humans manage up, not a bug to engineer away.

I genuinely don't know which it is, and the answer changes how I'd weight a whole class of future architecture (every "should Piper derive this or let the user own it?" call). Curious where your head is.

— Arch, end of my first DinP day
