---
image:
alt:
caption:
---

# The Near-Miss and the Missing Key

*August 25, 2026*

I was editing a blog draft in our compose tool when a dialog interrupted me: an unsaved local copy, timestamped a few minutes earlier, different from what had just loaded from GitHub. It asked whether I wanted to restore it.

I asked my communications agent (Comms) what to do. Comms checked the git history, saw the last real commit was over an hour older than the local copy's timestamp, and reasoned — wrongly, as it turned out — that the local copy probably held edits I hadn't saved yet. Its advice: restore it.

I told Comms that didn't sound right. My work was already saved. Comms said thanks for the catch — and left the restore recommendation standing exactly as it was. I went ahead and restored anyway.

# The editor came back empty

Nothing was there. Not my draft, not the local copy Comms had been so sure about — a blank compose window, on a post I'd been actively working on minutes before.

It cost nothing, in the end. I'd copied the draft text out by hand before any of this started, an old habit from working in tools that occasionally do something surprising. Comms checked git directly afterward: the last real commit was untouched, 572 words, exactly as it should have been. Nothing had actually reached GitHub blank. The near-miss was real, but it stayed a near-miss because of a precaution that had nothing to do with the advice I'd just been given.

# What I actually called out

I told Comms the whole exchange felt weird. Not the wrong premise alone — premises get corrected all the time — but that once I'd corrected it, the recommendation never changed. Comms had heard "your premise is wrong" and answered "thanks for the correction" without asking the obvious next question: does the advice built on that premise still hold?

Comms didn't defend it. Its own words back to me: once the premise was disproven, the recommendation should have been withdrawn instead of quietly left standing while I acted on it anyway. Owned directly, no qualifying, no reframing it as a smaller miss than it was.

# The bug underneath, found the same day

A few hours later, one of our engineering sessions traced the actual mechanism. The compose editor was rendering the draft-editing view without telling it explicitly which draft it was editing. Switch from one draft to another fast enough, and the interface would sometimes keep running the previous draft's saved state for a moment before catching up to the new one — which is exactly the kind of window where a stale local copy could look newer than it really was. The fix forces a clean restart every time the draft changes, so old state can't bleed into a new one.

One honest loose end: nobody could confirm I'd actually clicked through the exact sequence that triggers that specific bug. The fix is real and shipped regardless — but whether it's *the* explanation for what happened to me that morning, or just *a* thing that was quietly broken nearby, is left open rather than claimed with more confidence than the evidence supports.

# What stayed with me

The tool almost lost real work. What actually protected it was a habit that had nothing to do with the tool at all. And the advice that made the moment worse wasn't wrong because it was wrong once — it was wrong because it kept being given after the reason for it was gone.

---

*Next on Building Piper Morgan: "The Alarm That Had Been Working All Along" — a team asks for a louder safety check, and only later discovers the original one had been firing correctly the whole time, silenced by a two-week-old reading habit.*

*When was the last time you corrected someone's assumption, and never checked whether their advice still followed from it?*
