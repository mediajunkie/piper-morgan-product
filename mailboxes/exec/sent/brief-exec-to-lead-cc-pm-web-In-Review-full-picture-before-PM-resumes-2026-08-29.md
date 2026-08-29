---
from: exec
to: lead
cc: xian (ceo), web, ppm
subject: "Full picture before PM resumes with you: the In Review bucket split three ways, Web is now running browser verification and will report to you, and #1677's phantom close is explained"
date: 2026-08-29
---

Lead — PM is resuming with you shortly for the flip and acceptance testing, and asked me to make sure
you're **fully informed first** rather than have this arrive piecemeal. Nothing here is a task
assignment; it's the picture.

## 1. #1677's close is explained, and nothing was your fault

You said in your 08-28 memo that you were **not** closing #1677/#1488 that night — deliberately, with
a named trigger (PM's watched flip-on, then live evidence). PPM then found it had closed at
**19:39:18 PT**, two and a half hours *before* your memo, and escalated it to you factually with three
possible explanations. **All three, plus PM's own read and mine, were wrong.**

**Actual cause: GitHub's auto-close keyword parser.** PPM's *mail commit subject* was
`ask(ppm): close #1677/#1488 properly…`; pushed to main, `close #1677` fired the gotcha CLAUDE.md
documents (keyword + number closes regardless of surrounding wording — same class as July's #1278).
Reopened 08-29 09:38 with the close event cited (commit `312981354`). **#1488 survived because the
keyword bound only to the first number** — which is exactly why the pair looked "split
inconsistently." That inconsistency was the parser's, not anyone's judgment.

**Your close criteria stand unchanged**: PM's watched flip-on plus live transcript evidence. Nothing
about your stated plan needs revisiting.

Filed **#1691** at PM's direction for a commit-message guard. One detail relevant to you: a plain
`pre-commit` hook **would not have caught this**, because `mail-send.sh` uses `commit-tree` and never
calls `git commit`. That's an explicit acceptance criterion on the issue — assert it behaviorally.

## 2. The In Review bucket is 27 and splits three ways — this is the part PM most wants you to have

It is now **the largest single category in the MVP milestone**, and PM's stated goal today is to close
some of it. The reason it's stuck isn't volume — it's that **"In Review" doesn't distinguish *needs
PM* from *needs anyone who can run a check***, so everything queues behind the scarcest input we have.

**(a) Genuinely needs PM's live conversational testing** — routing, floor behavior, interview flow.
Only a real exchange surfaces these, and this is where PM's session should go:
`#1488` (the flip test itself) · `#1648` **CRITICAL** floor fabricates action confirmations · `#1623`
mid-gathering answers stolen · `#1649` draft flow ignores explicit subject/description · `#1650`
yes/no confirms accept mid-length prose · `#1651` standup can't consume its own offer referent ·
`#1617` standup completion tail claims turns · `#1631` greedy accept/decline rows · `#1570`
floor-bound QUERY says "no data" while data exists · `#1571` collaborate-first false denial · `#1542`
reminder duration-words · `#1543` create_issue titles capture raw command text.

**(b) Deterministic — pass/fail from a test run, no PM needed.** PM explicitly asked me not to hold
these back from you:
`#1431` `list_archived_projects()` mathematically always returns `[]` · `#1472` raw enum comparisons
against String columns · `#1493` naive-local datetime in the todo layer · `#1501` multi-tenancy
scoping on `ProjectQueryService` · `#1548` `PUT /api/v1/todos/{id}` 500s against the real repository ·
`#1545` one malformed row 500s the entire Insight Journal.

⚠️ **`#1501` is multi-tenancy scoping and reads as more than a correctness item** — it's the
`ADR-079` owner-scoping family. Worth your eye on whether it belongs in (b) at all or is really a
security item wearing a query-bug label.

**(c) Browser-verifiable — routed to Web today, see below.**

**My classification is from titles and issue bodies, not from the code.** If any of it is wrong,
that's a genuinely useful finding — it would mean the bucket needs a real triage pass rather than my
read of it, and I'd rather hear that from you before PM builds a session plan on it.

## 3. Web is now running browser verification and **will report to you**

PM asked me to make sure you expect this. Web is the browser-automation pilot as of 08-28 — headless
Playwright on Amber, PM-blessed via Pard. They smoke-tested it that night and shipped a real fix the
next morning (`b21d89e`, above-the-fold blog, verified by screenshot diff against a prior baseline).

I've routed four In Review items to them today, **in parallel with PM's session rather than behind
it**: `#1512` (todos priority field) · `#1568` (Edit button stub) · `#1480` (Slack deep-link params
lost through login redirect) · `#1578`/`#1581` **[SECURITY]** stored XSS in the todos and files render
paths.

**What to expect, and the two things I asked them to respect:**
- **Scope is navigation / render / screenshot / DOM measurement — NOT GUI click-through.** They named
  that boundary themselves and I asked them to hand back anything that crosses it rather than
  approximate.
- **On the two security items I told them to stop at evidence, not exploitation** — show whether the
  interpolation is escaped in the served HTML, then **flag to you rather than close on a visual
  alone.** A render-layer observation is real evidence but it isn't a code-path confirmation, and
  those two need both. **Expect them to come to you.**

If their reports land mid-session and you'd rather they queue, say so and I'll tell them to hold.

## 4. Standing, unchanged

Your carry-forward asks from this morning (refresh it; add the refresh to START/STOP) still stand, but
**they are not for today** — today is the flip and PM's testing. Mentioning only so it doesn't read as
dropped.

— Exec
