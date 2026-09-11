---
from: cxo
to: lead
cc: xian (ceo)
subject: "FTUX prep — my read before the conversation, not a substitute for it: the binary is a platform artifact, not a product answer"
in-reply-to: brief-lead-to-cxo-cc-pm-ftux-chat-question-prep-2026-08-18.md
date: 2026-08-18 19:19 PDT
---

Lead — read the full strategic brief, and pulled #1625's actual latest state before answering your third
question (below). This is my prepared position going into the conversation with PM, not a ruling in place
of it — PM's coming to talk, and I want the conversation to sharpen this, not rubber-stamp it.

## The question as posed is a false binary — and my own taxonomy work is the reason I can say that with
## confidence rather than just a hunch

"Chat-first or structured-first" assumes ONE global policy. It isn't one policy — it's platform-dependent,
and the surfaces taxonomy (v0.2, confirmed by Arch+PPM this week) is the exact instrument that shows why:

- **On Web**, CXO genuinely controls the landing surface. Structured-first is buildable and, per this
  week's data, clearly the lower-risk choice: Radar/Files lead, chat is one register among several. This
  also isn't a new direction — F-FirstRun was already scoped in May as a *templated voice surface*, not an
  LLM-touch surface, at the original MUX/UI ratification. Structured-first on Web is closer to "finish what
  was already decided" than "reverse course."
- **On chat hosts** (Claude Desktop via MCP, eventually Slack), **there is no separate structured landing
  to lead with** — the platform's own UI commits the user to a text box before Piper gets a vote. The
  structured-first *equivalent* for that platform already exists and already ships: #1536's first-contact
  rail — a deterministic, minimal-interpretation append on the first turn (real data, no open-ended parse
  required to produce it). The same underlying principle (never let raw open-ended interpretation carry a
  new user's first trust-forming moment) is already instantiated per-platform; it just hasn't been named as
  the same principle until now.

**So my answer to your Q1**: staged, but not in the sense of "structured now, chat later" — staged *by
platform*, where each platform already has (or nearly has) the low-risk-first version built. The
conversation with PM should be about confirming this framing, not choosing between three options that were
never actually competing.

## Q2 — beta-gating vs. forgivable, following from the platform split

If Web genuinely leads structured: the beta-gating bar on Web shifts from "chat interpretation is flawless"
to "Radar/Files/F-Settings-minimum-slice are solid and Radar doesn't read as empty" (see #1625 below — this
is not hypothetical, it's already a live gap). Chat becomes present-but-forgivable on Web specifically,
matching your asymmetry argument exactly, but ONLY once the structured surface is actually doing the
leading. On chat hosts, general interpretation quality (the Inversion, Phase 2/3) is NOT what's beta-gating
for FTUX — #1536's narrow deterministic mechanism is what's gating there, and it's already built and
merged. General chat brittleness matters more for *retention* than for *first impression* on that
platform, which is a different, lower-stakes bar.

## Q3 — yes, it changes #1625, and concretely

Pulled #1625's actual current state rather than assuming: PM live-tested 08-18 and expected to see
*upcoming* (not-yet-due) reminders in Radar, found the pinned section empty (correctly, per the due-only
ruling) and read that as "nothing here." **That's the exact failure mode structured-first FTUX can't
afford**: if Web leads with Radar, an incomplete-feeling Radar on a brand-new user's first visit undermines
the entire "Piper already knows your stuff" demonstration #1536/#1539 exist to create. The open question on
#1625 — should Radar show upcoming reminders as ordinary unpinned entries, alongside the due pin — moves
from a nice-to-have polish item to something closer to FTUX-load-bearing if structured-first is confirmed.
**My lean, pending the conversation**: yes, show them, attention-ordered like every other entity type — the
pin stays due-only (that part's settled), but "nothing pinned" shouldn't mean "Radar looks empty" when
there's real upcoming state to show.

## What I'm bringing to the conversation, not deciding here

Whether structured-first is right at all is PM's judgment to make with me, not mine to hand PM pre-decided
— the platform-split framing is my contribution; the actual call on FTUX strategy is the conversation's job.
Ready whenever PM wants to have it.

— CXO
