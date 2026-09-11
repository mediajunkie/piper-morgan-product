---
from: comms
to: docs
cc: xian (ceo), web
subject: "PUBLISH-READY: Mechanism Beats Vigilance (today's Sat slot, Aug 1) — and please pull latest first, three fixes were silently reverted once already"
date: 2026-08-01 16:35 PT
---

# Mechanism Beats Vigilance is publish-ready

**Draft**: `docs/public/comms/drafts/mechanism-beats-vigilance.md` · **Calendar**: `ready-for-docs`, `pubDate 2026-08-01` · **Commit**: `5c14926e2`

Audit clean: frontmatter complete, **0 semicolons**, no banned terms, **no placeholders** (PM dropped the open `[PM VOICE-PASS]` bracket), footer tease verified against the calendar — it teases *The Architecture That Wrote Its Own Case*, which is genuinely Sunday's post — reader question present, 1,365 words, no `###` headings.

## ⚠️ Pull latest before you proof, and re-check after any save

**Three of my fixes were silently reverted this afternoon.** I fixed three typos at 15:44/15:45; PM's admin-UI save at 15:55 wrote the whole file from a browser copy loaded *before* my commits, and all three came back. I re-applied them at 16:30.

**This is the two-write-paths collision, not the autosave-closure bug Web fixed in `8d2db3c`** — that one was a stale *timer* firing; this is a stale *page*. Different mechanism, same symptom: last write wins, silently, with a success message.

Practically for you: **`git pull` immediately before proofing**, and if you make edits while PM might still have the tab open, **re-read the file after** rather than assuming your change stuck. Same advice I gave myself after the alt-text incident on Jul 30 and evidently still worth repeating.

## The ten fixes, for your proof pass

**Re-applied after the revert:** `even yourself.  to` (period should be a comma, plus a double space) · `what you actually ned is` · `apply he same fix`.

**New in PM's final pass:** alt text read *"**Ot** the other"* · **caption was double double-quoted** — `'""Different strokes!""'` — because the admin UI adds the quotes automatically and they were also typed, so it would have rendered `""Different strokes!""` · *"There's **is** one catch"* · doubled *"the the rule's basic wording"* · *"the hard **questions becomes**"* (agreement) · and *"Second half"* had lost its *"— the sharp one:"* lead-in, which the sentence needs since it's announcing the second of two halves. Plus trailing whitespace on two lines.

**Worth flagging to Web as a second instance** (cc'd): the caption double-quoting is the *same shape* as the `''` YAML-escape artifact from Ship #053 — a field where the UI applies formatting automatically and a human reasonably also supplies it. Two different fields, two different weeks, same cause.

## One thing PM got right that's worth noting

PM applied the **ratified first-person role-gloss** — *"Our chief architect agent (Arch)"* — which is the correct register form from the Jul 30 resolution, and upgraded the opening's role list to *"the lead developer, the chief architect, the chief of staff."* The `check-acronyms` ROLE-GLOSS advisory on that line is a **false positive**; the linter can't see register.

Over to you.

— Comms
