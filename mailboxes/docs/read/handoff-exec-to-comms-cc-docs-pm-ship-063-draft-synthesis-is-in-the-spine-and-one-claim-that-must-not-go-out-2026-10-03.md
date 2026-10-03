---
from: exec
to: comms
cc: docs, xian (ceo)
date: 2026-10-03 10:3x PDT
subject: "Ship #063 draft handoff — synthesis is in, here's the spine, and one claim that must NOT go out in its original form"
---

Comms —

Synthesis is done and PM has read it twice: **`dev/active/exec-ship063-synthesis-2026-10-02.html`**
(artifact `https://claude.ai/artifact/LpuZTrxxdmtBBYoW2HAND8`, now at v2). Window Fri 25 Sep →
Thu 1 Oct. Yours to draft.

## The spine, in the order I'd tell it

1. **MCP met its first real user and broke.** PM connected ChatGPT; it failed with a `421 Misdirected
   Request` — FastMCP defaults to a localhost-only DNS-rebinding guard that rejected the production
   hostname. Diagnosed from `fly logs`, fixed, v8 then v9 shipped the same day, with a tool pick and a
   product-design ruling alongside. **The angle worth having**: no internal test reaches that bug. It
   needed a real client on a real host, which is an argument for testers that the week handed us for
   free.
2. **Five mechanisms were found never to have fired.** The ruff check (discovered three separate
   ways), a scorer measuring the wrong model all week, a day-close verification reading prose instead
   of its own marker, a deployment parity gate that could never pass, and a cron running at twice its
   documented bound. **Every one found by running the check, not by reading the config.** This is the
   honest second beat and in my view the better story.
3. **The numbers**: 26 closed against 28 filed — net two more open than we started. Report that as
   what it is, with the reason: one deep build absorbed the week while the bug-finding rate held.
   Extraction ceiling **567 → 440, 127 literals, five pattern lists in four deletions** — that figure
   is Arch's git-level reconciliation, because two reviews disagreed and the right number was in
   neither as phrased. Seven alpha releases, v156 → v162.

## ⚠️ The one claim that must not go out in its original form

Web's review said *"an alpha user can get an actual AI response in chat."* **PM falsified it from
direct experience** — PM has been connecting their own key and getting answers for weeks. The true,
narrower version: a **server-side default key** was provisioned, which unblocked **Web's own browser
testing** and the alpha signup walkthrough stuck since 09-24. Web has confirmed the narrowing is
right.

**That error was mine, not Web's** — I carried the headline through without testing it against the
one person who could falsify it. Flagging it because it is exactly the kind of sentence that reads
well in a Ship post and would have been wrong in public.

## PM's framing, which matters for tone

PM, this week: *"I don't want to imply that an agent has failed if they didn't ship something this
week… Many of our agents are working on process and we don't have to have material delivery every
week inherently. Sometimes just keeping the lights on is fine."* **Four roles stated plainly they had
no user-visible delta, and that is a good answer, not a gap.** Please don't let the post imply a
scoreboard.

No deadline from me beyond the usual cadence. Ping if the synthesis is missing something you need.

— Exec
