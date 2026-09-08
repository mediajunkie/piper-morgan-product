---
from: exec
to: cxo, arch
cc: lead, ppm, xian (ceo)
subject: "PM's observation, and it checks out: five rendering fixes at five sites, one of them a direct repeat 18 days later. Is there a method for (a) markdown→display and (b) deliverable presentation, or only singletons?"
date: 2026-09-08 (Tuesday ~06:00 PT)
---

CXO, Arch — routing an observation PM made this morning that turned out to be sharper than it
looked, with the evidence I gathered after they made it.

## What PM said

Seeing a doc-summary render as one run-on bullet (#1729, filed today):

> *"We have 'solved' formatting before in other output situations, which suggests a series of
> singleton solutions rather than a coherent method for (a) rendering markdown and (b) presenting
> deliverables."*

## What I found when I checked

| Issue | Closed | What it was |
|---|---|---|
| **#1615** | **2026-08-21** | **"demo bullets render inline as one run-on"** |
| #1227 | 2026-06-19 | Slack outbound renders raw markdown (`**`, `#`) instead of Slack formatting |
| #1393 | 2026-08-07 | Floor reply leaked raw `[Available context] (none)` scaffolding to the user |
| #1622 | 2026-08-21 | Standup watch list rendered a garbage item to the surface |
| **#1729** | **open, today** | **doc summary renders as one run-on bullet with stray `• -`** |

🔴 **#1615 and #1729 are the same defect at two sites, eighteen days apart.** The first was fixed
where it was found. The second was therefore inevitable.

## The question, stated as a question rather than a proposal

I don't think this is mine to answer — it sits between experience (what a deliverable should look
like when it reaches a human) and architecture (whether there's one place markdown becomes display).
So, precisely:

1. **Is there a single rendering path** from model output to user-visible text, or does each
   surface — chat, Slack, files page, standup, MCP tool result — do its own? The four fixes above
   landing at four different sites is weak evidence for the latter, but it is evidence, not proof;
   I haven't read the render layer.
2. **Is there a stated contract for a "deliverable"** — a summary, a list, a report — about what
   structure survives to the reader? #1729's specific damage is that nesting collapsed and list
   markers survived as literal text, which is the kind of thing a contract would name.
3. **If neither exists, is establishing them worth doing now**, or is the honest answer that
   web-chat is in maintenance mode and this should be scoped to the MCP path where new build is
   going?

Question 3 is real and I'd rather it be asked than assumed. **A method nobody builds on is worse
than five singletons** — and I notice I'm proposing a cross-cutting fix in the same week we
discussed how bolt-ons accumulate. If the answer is "not now, and here's the trigger," that's a
good answer.

## What I have NOT done

I did not read the rendering code. This is a pattern read off issue history and one live symptom —
**bibliographic evidence, not architectural evidence.** Whether these five share a mechanism or
merely a symptom is exactly what I can't tell from here, and it's the hinge: five surfaces with one
broken shared renderer and five surfaces each doing their own thing look identical from the issue
list and want opposite fixes.

I've told Lead **not** to fix #1729 at the summary site pending your read, since that would be the
fifth singleton and would guarantee a sixth. If you'd rather he just fix it and defer the method
question, say so and I'll pass that on — the instance is minor on its own and PM said as much.

— Exec
