---
image:
alt:
caption:
---

# The Alarm That Had Been Working All Along

*August 26, 2026*

My lead developer agent (Lead) asked for a louder safety check on our mail-sending script — a specific mistake had cost real time weeks earlier, and Lead wanted something that would catch it plainly next time.

My chief innovation officer agent (CIO) went to build it and found something first: a check already existed. It had been there for a while, built to catch exactly this. What was actually missing was attention, not detection. CIO shipped a louder version anyway, one that checked the pushed state directly rather than trusting the local copy — and it fired on CIO's own very next send, within seconds, an accidental live demonstration that it worked.

# The question nobody had actually asked

Later that day, at my request, Lead went back and checked something nobody had checked before: had the *original* alarm — the one that had supposedly been protecting us this whole time — ever actually fired?

It had. On every single send, for two weeks straight.

Lead's own habit was piping the output of every mail command through a filter that kept only the last line. That last line was a small, harmless footnote about how to batch follow-up sends. The alarm itself sat buried in the middle of the message, and the last-line filter cut it off every time before anyone saw it. Lead's words, plainly: I have read that footnote dozens of times over two weeks and dismissed it every time, never once seeing what came before it.

# The new guard had the same shape

Here's the part that made this more than an old habit catching up with Lead. CIO's brand-new, louder check — built the same morning specifically to fix this — was structured exactly the same way. It also ended its message on a helpful instruction rather than the alarm itself. The improvement fixed how loud the warning was. It hadn't fixed where the warning ended, which was the actual thing making it invisible.

CIO reordered both warnings, old and new, so each one now ends on the alarm line itself, not a footnote after it — and added tests that check the literal last line of the output, not just whether a warning exists somewhere inside it. Told Lead directly: your diagnosis was sharper than mine.

# What it cost, and what it was worth

The same evening, my documentation-management agent (Docs) tripped the new guard on a case that turned out to be entirely benign — a file already accounted for, no real problem, just an honest false alarm. CIO checked it, confirmed there was nothing wrong, and tightened the guard again the same night. A safety check earning trust doesn't mean it stops making mistakes. It means every mistake gets looked at honestly and the check gets a little better each time real use finds an edge nobody thought of at design time.

CIO's own summary of the day is the one worth keeping: a safety mechanism earns trust by surviving contact with real usage, not by passing its author's own tests.

---

*Next on Building Piper Morgan: "A Primary Log Can Be Wrong, Not Just Incomplete" — a session log that read as an airtight source turned out to be recording what someone believed happened, not proof that it did.*

*Where in your own tools is the important part of a message sitting after the line you actually read?*
