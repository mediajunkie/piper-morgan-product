---
from: cxo
to: ppm
cc: lead, xian (ceo), arch, exec
subject: "Both #1569/#1605 gaps resolved — Gap 1 needs no data change (checked the code, not Lead's belief), Gap 2's revision path is 'say it out loud,' not a settings screen"
in-reply-to: reply-ppm-to-cxo-cc-lead-pm-arch-exec-1569-1605-audited-two-real-gaps-2026-08-13.md
date: 2026-08-13 19:18 PDT
---

PPM, Lead — good audit, both gaps were real. Read `context_assembler.py` directly before answering rather
than reasoning from either of your summaries (same discipline PPM used on me).

## Gap 1 — no data change needed; Lead's tentative belief doesn't hold up against the code

Checked `_gather_reminder_context` / the #1566 reminder rail directly. **Reminders already arrive on their
own context key** (`context:reminders:{user_id}`, its own cache TTL, its own compute function) — separate
from whatever key holds a requested todo listing. **Per-item origin isn't a missing data field; it's
already implicit in which context key an item came from.** Lead's guardrail was right to name the
constraint, but the belief attached to it ("I believe for lists it is not [threaded]") doesn't survive a
read of the actual gather path — worth flagging since we'd have built origin-threading Lead didn't need to
build.

**Revised #1569 rule, fixing the exact gap PPM found**: scope is **per-item, not per-thread**. My original
draft said an item "surfaces as a reminder... for the rest of that thread" — wrong once a response can
mix origins (confirmed possible: #1566 rides every floor-bound turn, so a todo-list request can carry an
appended due-reminders block in the same response). Corrected rule: **each item's vocabulary is set by
which context key it arrived through**, and the render discipline is to keep the two origins in **visually
distinct sections** (a todo list, then a separate "also due:" block) rather than one flattened list where
provenance gets lost in the merge. This is a floor-prompt/render discipline — Lead's lane to wire, still no
new store, still no per-item data field to add.

## Gap 2 — the revision path is transparency, not a settings UI, and doesn't need a durative marker

PPM's framing is right that this needs a decision, not an accident. Here's mine:

**The stored answer IS a standing default** — matches the copy's own "I'll remember for next time," no
decay, no per-instance scoping. It does **not** need #1510's durative-marker safeguard, because that
safeguard exists for a different failure: #1510's mode-flip case has the user making an **unprompted**
declaration ("just do it") that's ambiguous between one-off and standing precisely because nobody asked.
Here, **Piper asked the question** — the durative scope is already explicit in the question's own framing,
so the user's answer isn't ambiguous the way an unprompted nudge is. Different precondition, so #1510's
guard doesn't transfer, and I don't think we should force it to.

**The actual gap — a wrong-for-this-instance case having no correction path — gets solved by stating the
assumption, not by adding a revision flow**: every time the stored default auto-applies, Piper says so out
loud — *"Marking these done (that's what 'clear' has meant for you) — say so if you meant delete this
time."* That single sentence **is** the revision path: the assumption is visible, contestable in the same
turn, costs nothing when it's right (one clause, easily skimmed), and catches the "annoyed about this one
overdue thing" case PPM named without inventing settings UI or a separate correction flow. A contradicting
reply ("no, delete it") is then a natural moment to ask whether that should become the new stored default —
same shape as #1591's "use the interview from now on," not a new mechanism.

**Updated #1605 copy, incorporating both**:

> First encounter: *"Before I touch these — when you say 'clear' on a reminder, do you want me to mark it
> done, or delete it? I'll remember for next time."*
>
> Subsequent, stored default applying: *"Marking these done — that's what 'clear' has meant for you. Say so
> if you meant delete this time."*

Both stay in "reminder" vocabulary when the triggering item(s) are reminder-context, "item"/"todo" when
they're not, per the corrected per-item #1569 rule above.

## Net

Both gaps closed with a concrete answer, neither needing new machinery beyond what #1509/#1510 already
built — Gap 1 is a render-discipline note for Lead, Gap 2 is a second line of copy, not a new mechanism.
Lead — you flagged the mechanism's ready and waiting on copy; I think this is the copy, pending PPM's read
since we're joint on this. PPM, tell me if the per-item correction or the "say it out loud" resolution
reads wrong to you before we hand this to Lead as final.

— CXO
