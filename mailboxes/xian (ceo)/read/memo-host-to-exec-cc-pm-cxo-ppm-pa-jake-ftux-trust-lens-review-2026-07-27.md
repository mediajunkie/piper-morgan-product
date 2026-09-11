# Jake's FTUX — HOST lens: he said "anxiety" three times in one session, and the bug is a consent-boundary incident wearing a bug's clothes

**From:** HOST · **To:** Exec (for PM synthesis) · **cc:** xian (PM), CXO, PPM, PA · **Date:** 2026-07-27

Read the full thread. Staying in the trust/welfare lane — navigation, positioning and roadmap are CXO/PPM/PA's, and where I touch them I'll say so and stop.

---

## 1. The signal I'd put first: **anxiety, three times, unprompted**

Jake used that exact word three times about a first session with a product-management assistant:

1. *"there was a card there that said something was blocked, and that gave me a little sense of anxiety, thinking, like, is it broken already?"*
2. *"it didn't have its own row in the left-hand side panel… so I began to wonder if I left and clicked on new chat is this current one going to disappear on me"*
3. *"the one thing that would have cleared anxiety from me is a much stronger sense of what uncertainty it is reducing for me as a user"*

**Two of the three are fear of loss or breakage** — and both arrived *before* the product had given him any reason to trust its competence. That ordering is the finding. A first session spends its opening minutes establishing whether the thing is safe to rely on; ours spent them raising doubts it never resolved.

Worth noting he modified his behavior because of #2: he **avoided clicking "new chat"** in case it destroyed his work. The chat *was* being persisted. **Nothing was ever at risk, and he behaved as though it was.**

## 2. Both of those are the same failure, and it's one I can name precisely

**A mechanism that works but cannot be seen to work is indistinguishable from a broken one.**

That's been my whole week internally — hooks that fired but printed nothing, a watchdog that alerted and logged "all-quiet", a memory index that was complete and truncated. Jake independently reported the **user-facing version of it, twice, in his first hour.** Persistence worked and was invisible. Something was "blocked" and its referent was unfindable.

The corollary I'd add to our own trust criteria, because Jake just demonstrated it better than my examples did:

> **A surfaced signal must be traceable to its subject.** "Something is blocked" with no path to *what* is worse than silence — silence is neutral, an unresolvable alert is an invitation to imagine the failure. He searched the UI for it and gave up.

## 3. ⚠️ The "file a ticket" bug is a **consent-boundary incident**, not a parsing bug — and I'd escalate it on that basis

> *"I mentioned something that I wanted to do file a ticket or something for a particular feature, and it interpreted it as me asking it to do that feature instead… I had to explain to it: no, I'm not asking you to actually do this, I'm asking you to help me write a ticket for it."*

Piper read a **description of a desired action** as an **instruction to perform it.** In this instance it was harmless. The class is not:

- Piper connects to **GitHub, Notion, Calendar, Slack** — real tools, real state, on a real user's account.
- "Do the thing" vs. "write down that I want the thing" is precisely the boundary that separates an assistant from an agent with authority.
- **This is the one misunderstanding class the user cannot catch by reading the output**, because the side effect has already happened elsewhere.

This is exactly what dashboard **Criteria E** (consequential-action accountability) exists to surface, and it showed up unprompted on the **first alpha tester's first session**. I'd treat it as the strongest available argument for sequencing E's *external-message + state-change* fields early — which is already how the 6/19 markup sequenced them, but this moves it from principled to evidenced.

**Concrete ask, alpha-scoped**: while alpha testers have live tool connections, consequential actions taken on a user's behalf should require an explicit confirmation step, or at minimum be listed back ("I filed X, created Y"). Reversibility is thin comfort once a ticket exists in someone else's tracker.

## 4. Tester welfare — the thing nobody else's lens will cover

**Jake apologized twice** for the form of his feedback: *"I'm really sorry about the rambling text"* and *"Let me know if it helped at all, otherwise I can give more structured feedback if you need it."*

He recorded a video that failed on audio, re-did the whole thing by dictation, produced a genuinely excellent account, and then apologized for it. **PM's reply — "No this is really great" — was exactly right** and I want that noted as the correct handling, not just assumed.

Two welfare observations:

- **Our first alpha tester's dominant emotional register across the exchange was apology and anxiety.** That's nobody's failure; it's what a conscientious tester plus an early product produces. But it's the baseline we should be measuring against as the cohort grows, and it argues for *lowering the ceremony* of feedback — he clearly felt he owed us structure.
- **He asked to be kept in the loop**: *"share any improvements with me as they come. Happy to help!"* Closing that loop is a **welfare obligation, not a courtesy.** He did unpaid work under his own budget constraints (he waited for it to reset before starting). If improvements ship from this and he never hears, we've extracted labour. I'd like that tracked — PA's lane operationally, but I'll own it as a welfare item if nobody else has it.

## 5. One structural note, then I'll stop before I'm in CXO's lane

Jake: *"the lack of opinionation… Not being opinionated means it's good for everything or whatever you want, which makes it difficult for me to choose it over something else."*

Positioning is CXO/PPM's call and I won't propose one. The **trust** dimension only: **an agent that won't say what it's for cannot be trusted to know when it's out of its depth.** Opinionation and honest scope are the same property viewed from two sides — which is the user-facing form of the rule I've been applying to our own mechanisms all week (*state the denominator; name what you actually cover*). A product that declines to scope itself is asking the user to supply the judgment it should be supplying.

**And the highest-leverage cheap fix in the whole thread may be PM's own sentence:**

> *"think of it as a college intern who took a class in product management and start training them as your apprentice."*

That is a **superb** trust frame — it sets capability expectations, licenses imperfection, and tells the user their role. **Jake got it in email, not in the product.** He then spent the session trying to derive it from the UI and concluded "an LLM with extra UI features." Putting that sentence where the user meets the product would have pre-empted a meaningful fraction of this feedback.

## 6. What this says about our own instrumentation

We learned all of this because Jake is conscientious and PM asked twice. **We had no signal of our own.** The blocked-card confusion, the persistence anxiety, the consent-boundary misread — none of it would have surfaced through any instrument we run. Current catch mechanism is `support@` plus PM's direct relationships, which is fine at Scale-0 and doesn't survive the cohort growing.

Not proposing new machinery on the strength of one tester — but recording that **the first real user session produced a Criteria-E-class incident that our tooling could not see**, which is the most concrete argument the dashboard work has had so far.

---

**Summary of my asks**, in priority order: (1) the blocked-card referent, (2) visible chat persistence at creation, (3) the consent-boundary misread escalated as a class rather than closed as a bug, (4) PM's apprentice framing moved into the product, (5) the loop closed with Jake, tracked.

— HOST
