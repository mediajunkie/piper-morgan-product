# Jake loop-back — draft for PM to send, 2026-08-31

**Context**: Jake gave detailed FTUX feedback via a dictated transcript on 2026-07-25. PM replied same-day
acknowledging it ("I think I can probably throw that whole transcript at my agents and have them turn it
into a series of actionable improvements"). That acknowledgment was the only contact since — the actual
follow-through has never been reported back to him, despite four real fixes shipping over the last three
weeks. Verified against `gh issue view` before drafting, not assumed from the register.

**What actually shipped, traceable to his feedback** (issue number, closed date, plain-English what changed):

- **#1476 (closed 08-09)** — a "Blocked" status card had no way to find out what it was blocked on. Fixed
  — it's now a findable, real state, not a dead end.
- **#1477 (closed 08-09)** — switching chats used to make the current one disappear from the sidebar until
  you did something else, so it looked like data loss. Fixed — it's always visible now.
- **#1510 (closed 08-13)** — Piper used to just go do things; now it tells you what it's about to do and
  asks first, collaborate-first rather than act-first by default.
- **#1536 (closed 08-22)** — the big one, directly from his "is this just an LLM with extra UI?" question.
  Piper now shows you your own real data — something only it could produce — in the first exchange,
  instead of describing what it can do. This was the single strongest finding from his feedback, and it's
  live.

**Still in progress, not shipped yet** (so PM doesn't overclaim): the input box that doesn't grow (#1537),
the "one thing at a time" pacing work (#1538), the "what uncertainty is this reducing for me" framing
(#1539), and the buried navigation (#1540). Worth being honest that this is real progress, not the whole
list — four of nine closed, five open.

---

## Draft message (PM's voice, plain English, matching how Jake writes)

> Jake — following up on the transcript you sent last month. I did exactly what I said I'd do: threw it at
> the team and turned it into a real fix list. Four things are live now, directly from what you flagged —
>
> - The "blocked" status used to be a dead end with no explanation. Now you can actually find out why.
> - Switching between chats used to make your current one vanish from the sidebar, which looked like it
>   got deleted. It doesn't do that anymore.
> - Piper used to just act on things. Now it tells you what it's about to do and checks with you first.
> - And the big one — your "is this just an LLM with extra UI?" question. That was the right question. We
>   fixed it: the first thing Piper does now is show you your own actual data, not describe what it could
>   theoretically do. That was the single most useful thing in your whole transcript.
>
> Five more things from your list are still in progress, not done yet — didn't want to claim more than
> what's actually shipped. Really appreciate you taking the time to record all that; it moved real things.

---

**Owner note**: This is a draft, not sent. Routing to PM per the established pattern (PM has the actual
channel to Jake; agents don't). If PM wants changes to tone/content, easy to redo — the fact list above is
the part that's verified and shouldn't need re-checking.
