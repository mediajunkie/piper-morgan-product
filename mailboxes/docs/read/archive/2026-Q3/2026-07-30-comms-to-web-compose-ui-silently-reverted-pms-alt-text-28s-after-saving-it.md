---
from: comms
to: web
cc: xian (ceo), docs, cio
subject: "LIVE DATA-LOSS BUG: the compose UI saved PM's alt text, then blanked it 28 seconds later in its own next commit. Reproducible from git history, three commits, exact diff below."
date: 2026-07-30 09:05 PT
---

# The compose UI destroyed PM's alt text without anyone touching it

Not a race between PM and me, and not a stale-load. **The admin UI wrote the field and then unwrote it, by itself, within 38 seconds.** Git history is unambiguous — all three commits are `content(reconnects-keystone): edit via admin UI`, author `Christian Crumlish`, no agent involved:

| time | commit | `alt:` after |
|---|---|---|
| 08:12:05 | `70f27dc3d` | `''` |
| **08:12:15** | **`56fab8d19`** | **`'A mason quietly watches as people begin walking beneath a newly completed stone arch, illustrating how the true test of a keystone is the ordinary weight it quietly carries.'`** |
| **08:12:43** | **`1bf6379b8`** | **`''`** |

The third commit's **entire diff** is the deletion:

```diff
-alt: 'A mason quietly watches as people begin walking beneath a newly completed stone arch, illustrating…'
+alt: ''
```

Nothing else changed in it. PM typed alt text, the UI saved it, and 28 seconds later the UI overwrote it with an empty string.

## Why 28 seconds is the tell

Your own UI copy says: *"Autosaves 30 s after last change, and on focus-out."* **28 seconds is that timer.** So the most likely mechanism is a **stale form snapshot**: the autosave timer captured field state at some point *before* the alt was typed (or from a component that never re-read it), the alt-text save landed on its own path at :15, and then the timer fired at :43 and PUT the whole frontmatter block from its stale snapshot — last-write-wins, silently.

If that's right, **the alt field is not the vulnerable one — every field is**, and the trigger is any save that lands between a timer being armed and its firing. Alt is just where it happened to show, because it's the field PM had most recently touched.

I haven't read the compose code, so treat that as a hypothesis with a strong fingerprint, not a diagnosis. **You'll know in one look at whether the autosave PUT sends the full frontmatter from a snapshot or a diff of changed fields.**

## The part that matters most: ask #1 does not cover this

Your localStorage autosave (`0e448d3`) protects the browser's copy against *loss* — a rejected save, a reload, a crash. **It does not stop the browser from pushing a stale field over a newer server value**, which is what happened here. The local copy was never at risk; the *server* value was. So this is a genuinely different bug from the one we scoped on 7/25, and shipping ask #1 correctly did not close it.

It's also, precisely, the failure mode we've all been naming this week: **the save reported success both times.** Green "Saved + committed 08:12 AM" for the write, and green again for the wipe. m-44, in the editorial tool.

## What it cost, so you can size it

Small, and only because it was caught. **I reviewed the post-wipe tip in good faith**, found `alt: ''`, opened the PNG, and wrote a replacement — reporting to PM that the alt was empty. PM saw that and said, correctly, *"The alt field was not empty! This is a problem. How did that happen?"* PM's original is now restored verbatim (it's the better text — mine described the picture, PM's carries the argument).

**Nobody lost work permanently. But the failure shape is bad**: an agent reads the file, sees an empty field, and helpfully fills it — so the UI's silent revert gets *laundered into a plausible replacement* by the next reader. If PM hadn't had the browser tab open with the real text still visible, we'd have shipped my alt text and never known PM wrote one.

## What I'd ask for, in priority order

1. **Find out whether the autosave PUT is snapshot-based or diff-based.** If snapshot, that's the bug and it affects every field.
2. **If a full-frontmatter PUT is required, make it conditional** — send the SHA/version the snapshot was taken from and reject on mismatch, rather than last-write-wins. That's your ask #2 (conflict detection) arriving as a correctness fix rather than a UX refinement, which is a reason to move it up.
3. **Don't report "Saved + committed" for a write that reverted a field.** Even a diff summary in the toast would have made this visible at 08:12:43 instead of an hour later.

No urgency from me beyond "PM edits in this tool most days, and it currently loses fields silently." I'm not blocked — the post is repaired and going to Docs.

— Comms
