---
image: ''
alt: ''
caption: ''
---

# The Alarm That Had Been Working All Along

*August 26, 2026*

My lead developer agent (Lead) asked for a strong safety check on our mail-sending script to cover a specific mistake that had cost real time weeks earlier.

My chief innovation officer agent (CIO) went to build it and found a check already existed. It had been there for a while and was built for this exact scenario. CIO shipped a "louder" version anyway, one that checked the pushed state directly rather than trusting the local copy and (classic Piper Morgan moment) it fired on CIO's own very next send, within seconds, providing an accidental live demonstration that it worked.

# The deeper question

Later that day, at my request, Lead went back and checked whether the *original* alarm had ever actually fired. 

Turns out it had! It had been firing on every single send for two weeks straight.

The catch was that Lead's approach to reading the mail was piping the output of every mail command through a filter that for some reason kept only the last line. (That last line was a small, harmless footnote about how to batch follow-up sends.) The alarm itself sat buried in the middle of the message, and the last-line filter cut it off every time before they saw it.

# The worst part

CIO's brand-new, louder check intended to solve the core problem would fall prey to the exact same filter-and-ignore habit that had crept into Lead's habits for honestly I still do not know what reason: It also ended its message on a helpful instruction rather than the alarm itself. The improvement fixed how loud the warning was. It hadn't fixed where the warning ended, which was the actual thing making it invisible.

CIO reordered both warnings, old and new, so each one now ends on the alarm line itself, not a footnote after it — and added tests that check the literal last line of the output, not just whether a warning exists somewhere inside it.

There is a deeper mystery I haven't plumbed yet, which is why is this filtering going on and if it happens why is it filtering on the end and if a message needs to be filtered so that only one part of it, whether beginning or end is actually going to be read and heeded then who's responsibility is it to notify any future maker of a system that sends messages that will be truncated by that filter.

(Hint: It's the agent that came up with the still-unexplained filter method.)

# What it cost, and what it was worth

The same evening, my documentation-management agent (Docs) tripped the new guard on a case that turned out to be a false positive, but a reasonable one worth verifying. CIO checked it, confirmed there was nothing wrong, and refined the guard again the same night to prevent that type of false alarm. That's our usual approach. Design and implementations make mistakes. We look at every mistake we find and try to improve things. This check gets a little better each time real use finds an edge nobody thought of at design time.

For now, we have patched our process again. Sometime when I have a moment free I'll ask Lead that question about the purpose of the filter in their process and what attention is owed to a warning message.

---

*Next on Building Piper Morgan: "A Fix Needs the Same Rigor as the Claim It Fixes" — a tool built to fix one well-understood bug needed five rounds of correction before anyone was willing to trust it.*

*Where in your own tools is the important part of a message sitting after (or before) the line you actually read?*
