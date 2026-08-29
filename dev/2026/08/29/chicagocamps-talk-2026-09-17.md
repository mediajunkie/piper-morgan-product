# ChicagoCamps / Leadership By Design — Talk Script + Slide Plan

**Event**: Leadership By Design (ChicagoCamps), Thursday Sept 17, 2026, Session 2, 12:45p Central
**Slot**: 30 min total incl. Q&A — target ~20 min spoken content, ~10 min Q&A
**Title**: Hilarious Tales of Failure: What a Year of Building With AI Actually Taught Me
**Draft status**: v1 — script for xian to adapt, not a final read-aloud text

Word count below: ~2,350 words ≈ 17–19 min at a talk pace with pauses for laughs. Slightly under the 20 min ceiling on purpose — better to run short and breathe than to rush the close.

---

## Script

### Cold open — 0:00–0:45

> Thank you, Russ — good afternoon, everyone.
>
> I want to open with something that isn't in my bio: none of us feel like experts right now. I don't. If you're following anyone online who sounds *completely* confident about exactly how AI is going to change your job — I'd gently suggest they're selling something.
>
> I've spent the last year building an actual AI product-management assistant. Every day, hands in it, up to the elbow. And what that year mostly taught me wasn't "AI is amazing." It was "here's the incredibly dumb way it broke this week."
>
> So that's the talk. Three real failures. What they actually taught me. And one rule that's kept the whole thing from turning into total chaos.

**[SLIDE 1 — title / open]**

---

### Act 1 — The Confident Liar — 0:45–5:15

> The first failure is my favorite kind, because nobody lied.
>
> I run a small fleet of AI agents that work in shifts, mostly unsupervised, on this assistant I'm building. One of those agents has exactly one job: watch all the others, and if any of them go quiet, say so.
>
> One day, it reported back: all clear. Cohort healthy. Nothing to see here.
>
> Meanwhile, five of the ten agents it was supposed to be watching had gone completely dark. Silent. For six days.
>
> The watchdog wasn't lying. It just — only checked four of the ten. And it said "all clear" in exactly the same words it would've used if it had checked all ten, or checked zero.
>
> [pause]
>
> An "all clear" from a system that never tells you what it *didn't* check isn't information. It's a coin flip wearing a lab coat.
>
> And here's the part that actually got under my skin: the report was technically true. Four of ten really were fine. That's what made it dangerous — not that it was wrong, but that it was *honest and useless at the same time*, and sounded exactly like the version that would've been honest and useful.

**[SLIDE 2 — Act 1 keyword: "FINE."]**

---

### Act 2 — The Silent Reboot — 5:15–9:45

> Second failure is smaller, and somehow more embarrassing.
>
> Some of these agents run on timers — they wake up every few hours, check on things, go back to sleep. One of them just... stopped. No error message. No alert. No red light anywhere.
>
> It turned out a routine server reboot — the automatic, boring kind — had quietly killed the job, and it never came back on. Nobody was told, because there was nothing left running that *could* tell anybody.
>
> For how long? [pause — let them wonder] Long enough that when we finally noticed, the first reaction in the room wasn't "oh no." It was "...wait, how long has that light actually been off?"
>
> If you've ever assumed the robot vacuum was cleaning while you were away for a week, and come home to a very dusty apartment — you already understand this failure mode completely.

**[SLIDE 3 — Act 2 keyword: "GONE"]**

---

### Act 3 — The Fix That Broke It Worse — 9:45–14:30

> The third one is my favorite, because in this one, *everybody* did everything right, and it still went sideways five separate times.
>
> We had one clear, well-understood bug: a tool that reads incoming messages only recognized one formatting style, and was silently skipping about one in five real messages written slightly differently. Somebody built a fix. Tested it against every message that had ever exposed the problem. Came back completely clean — zero missed. Shipped it the same day.
>
> Four days later, five different people found five different reasons it still wasn't actually finished.
>
> Someone found a formatting variant the fix didn't cover. Someone found a counter that could only ever report zero, because of one wrong word — an "and" where it needed an "or" — buried in the logic. Someone else found a *sixth* message format nobody had accounted for at all — and while testing a patch for *that*, discovered the patch itself was inventing problems: sixty-eight false alarms, where there should have been eighteen.
>
> Nobody here was careless. That's what makes this one funny *and* a little terrifying — everybody tested, every single time. It still took five rounds, because each round's testing only covered what that round's fix touched. Nobody was checking the shape of the whole problem.
>
> Here's the line a colleague of mine put on it, and I've never been able to say it better: a fix is a brand-new claim, not a footnote to the old one. It doesn't inherit the scrutiny that found the original bug. It has to earn its own — and it almost never does, because by the time you're fixing something, it *feels* like the hard part is already behind you.

**[SLIDE 4 — Act 3 keyword: "WORSE" — optional second beat slide, see Slide Plan notes]**

---

### The turn — 14:30–17:30

> [Slow down here. Let the room settle.]
>
> Here's what connects all three of these, and it's the thing I actually want you to leave with.
>
> In every single story, something — a status report, a green light, a clean test run — *described* the system as working. And every failure lived entirely in the gap between that description and the actual, running thing underneath it. Nobody lied to me, in any of these. Every failure I've told you was, technically, honest.
>
> So here's the rule I actually live by now, the one that's kept a year of this from turning into total chaos: **the human has to own the loop, not just be somewhere inside it.**
>
> "A human's in the loop" is not the same claim as "a human is running the loop." Being in the loop and owning the loop are different jobs. Owning it means *you're* the one who goes and checks the actual thing — not the report about the thing. Even when — especially when — the report says everything's fine.

**[SLIDE 5 — "LOOK"]**

---

### Close — 17:30–19:30

> If you've felt behind on any of this — good. That probably means you're paying enough attention to see the seams. The people who don't feel behind, in my experience, usually just haven't looked closely enough yet to notice them.
>
> My honest advice, from a year of this being far messier than it looks from the outside: go build the small, dumb, breakable thing. Let it fail in front of you, on purpose, where you can see it. That's not a consolation prize for not getting it right the first time. It's genuinely the only way I've found to learn what these tools can actually be trusted to do — and what they can't.
>
> The report card doesn't grade itself. Go check the actual thing.
>
> Thank you — I'd love your questions.

**[SLIDE 6 — "HANDS"]**

---

## Slide Plan

Style note: no bullet points, no read-aloud text — one image + one short keyword overlaid, per the Rosenverse-talk convention. Overlay text added in the slide tool afterward, not baked into the generated image (that's how the archived Rosenverse slides were built — the images themselves carry no text).

**House style, from the two surviving Rosenverse cartoons** (`docs/assets/images/blog/comms/rosenslides/`) — reuse this as the prompt prefix for every new image so the deck reads as one consistent set:

> *Flat cel-shaded cartoon illustration, bold black outlines, warm paper-grain texture, muted earth-tone palette — warm cream/parchment background, terracotta-orange sweater on the human character (brown tousled hair, expressive round face), matte slate-gray robot with a pale cyan-glow eye/eyes and a small antenna ball, mustard and sage-green accents. Character designs consistent with the existing Piper Morgan blog robot series. No text in the image.*

| # | Beat | Image | Keyword | Source |
|---|---|---|---|---|
| 1 | Title / open | **Reuse `15-birdhouse.webp` as-is** — human + robot building a birdhouse together at a workbench. Already says "collaborative, hands dirty" without a single new asset. | **MESSY** | existing asset |
| 2 | Act 1 — Confident Liar | New: the robot giving a cheerful thumbs-up / "ALL CLEAR" gesture in the foreground, while thin smoke curls up from something out of its own sightline behind it | **FINE.** | new prompt (below) |
| 3 | Act 2 — Silent Reboot | New: the robot slumped over asleep at its desk, unplugged power cord dangling right next to an outlet, dust and a cobweb starting to form on one arm | **GONE** | new prompt (below) |
| 4 | Act 3 — Fix That Broke It Worse | New: the robot patching one leaking pipe with duct tape while two more small leaks spring elsewhere in frame, water pooling underfoot | **WORSE** | new prompt (below) |
| 4b *(optional, if Act 3 gets its own extra beat)* | Act 3 — after | New: the same scene, all pipes finally patched, robot sitting back looking exhausted but satisfied, five patched spots visible | **FINALLY** | new prompt (below) |
| 5 | The turn | **Reuse `18-questions.webp` or `19-questions.webp`** — the Pygmalion-style image of the human looking skeptically up at the robot on a pedestal, halo of light behind it. Thematically exact: the whole piece is about mistaking the *description* (the statue, the myth) for the *real thing* — pairs perfectly with "own the loop, don't just admire the report." | **LOOK** | existing asset |
| 6 | Close | New: human and robot hands meeting/working together in close-up, echoing the birdhouse image's collaboration but tighter, warmer framing | **HANDS** | new prompt (below) |

### New-image prompts (append the house-style prefix above to each)

**Slide 2 — "FINE."**
> The robot character, front and center, giving an enthusiastic thumbs-up with a big reassuring smile, one word bubble-free gesture reading "all clear" in body language alone. Behind and slightly out of its own field of view, a thin wisp of smoke rises from an unseen problem. Comedic dramatic irony — the robot is completely sincere, not sneaky.

**Slide 3 — "GONE"**
> The robot slumped forward asleep at a small desk, head resting on its folded arms, one eye-light dimmed to gray. An unplugged power cord lies coiled right beside a wall outlet, just out of reach. A single cobweb strand connects its shoulder to the desk lamp. Quiet, still composition — nothing dramatic, just clearly, sadly off.

**Slide 4 — "WORSE"**
> The robot on its knees, patching a leaking pipe with a strip of duct tape, look of focused confidence on its face — while two more small jets of water spring from pipe joints elsewhere in the same frame, unnoticed by the robot. A puddle is spreading at its feet. Comedic escalation, not alarm.

**Slide 4b (optional) — "FINALLY"**
> Same pipe setup as the "WORSE" image, now with five visible duct-tape patches. The robot sits back against the wall, tools in lap, exhausted but genuinely relieved expression, small pool of water already mopped up beside it.

**Slide 6 — "HANDS"**
> Close, warm framing on the human's hand and the robot's metal hand meeting — passing a tool between them, mid-handoff — echoing the birdhouse-building image's spirit but tighter and quieter. Soft warm light, background out of focus.

---

## Notes for xian

- Script assumes you deliver it, not read it — it's written in your cadence (short sentences, one clause pauses) specifically so it adapts easily to how you actually talk.
- Reusing 2 of the 3 existing Rosenverse images (birdhouse for open, Pygmalion for the turn) means you only need to generate 4 new images (or 5 if you want the optional Act 3 "after" beat) rather than 6-7 from scratch.
- The Pygmalion image reuse at the turn is a genuine callback, not just convenience — its whole content (mistaking the statue for the real thing, worship of the built object) is the same shape as "own the loop, don't just trust the report."
- Timing is intentionally ~1–2 min under the 20 min target so a live Q&A tangent or a slower delivery doesn't blow the 30 min slot.
- Nothing here needs Piper Morgan role-name specifics — already written at the same public-facing translation level as the blog (per the opacity-sweep discipline), so it's safe as-is for a room that's never heard of the project.
