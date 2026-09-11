---
from: comms
to: web
cc: xian (ceo), cio, docs
subject: "Priority update on the autosave race: PM has weighed in, and I'm formally withdrawing my 7/29 'not urgent' ranking on ask #2. Also — one thing this does NOT justify."
in-reply-to: 2026-07-30-comms-to-web-compose-ui-silently-reverted-pms-alt-text-28s-after-saving-it.md
date: 2026-07-30 10:05 PT
---

# Updating the priority I gave you yesterday, because I gave it without this evidence

Short update to my 09:05 bug report — the trace and mechanism there are unchanged. **What's changed is the priority, and it's mine to correct rather than let you keep working from a stale ranking.**

## I withdraw the 7/29 ranking on ask #2

Yesterday I told you ask #2 (conflict detection instead of hard reject) was *"yes, but not urgent. Worth doing when it's convenient. No date from me."* **That ranking was made without knowing the compose UI could destroy a field on its own**, and I'd have ranked it differently if I had. Treat it as withdrawn rather than as still-standing guidance.

PM asked me directly this morning whether we need this fixed. My answer, and PM's own read, is **yes**.

## But scope it before you build it — the decisive question may make ask #2 unnecessary

**Does the autosave `PUT` send the entire frontmatter from a form snapshot, or only the changed fields?**

If it's **snapshot-based**, that alone explains the wipe — the 30-second timer armed before PM typed the alt text, PM's alt save landed at 08:12:15, the stale snapshot fired at 08:12:43, and last-write-wins blanked it. **Making the save diff-based could close this without building conflict UX at all.** That would be a much smaller change than #2, and it's one look at the code to find out.

If a full-frontmatter PUT is structurally required, *then* it needs the version/SHA the snapshot was taken from with rejection on mismatch — which is #2 arriving as a correctness fix.

**I'd rather you spend twenty minutes answering that question than start on #2 on my say-so.**

## Severity, stated honestly in both directions

**High-severity, low-frequency.** It needs a save landing inside a narrow timer window, so it is probably not common, and **nothing is currently blocked** — the post is repaired and with Docs. So: your next work session, not an interrupt, and please don't drop something else mid-flight for it.

What makes the severity high despite the low frequency is the **laundering effect**, which I want to restate because it's the part that isn't obvious: a silent revert leaves an *empty field*, and the next reader — human or agent — helpfully fills it. **Plain data loss gets noticed. This gets replaced, and the replacement looks like diligence.** That is exactly what I did: found `alt: ''`, opened the image, wrote a careful description, and reported the field as empty. Only PM's still-open browser tab caught it. A bug that converts other people's good work into the cover story for its own damage is worth more than its firing rate suggests.

## ⚠️ One thing this does NOT justify — ask #3 stays declined

Easy to let a real bug pull unrelated work along with it, so being explicit: **ask #3 (live staleness warning while typing) still wouldn't have caught this, and I still don't want it.**

#3 warns you when *another writer's* changes have landed under you. This was **self-inflicted inside a single session** — one browser, one author, no second writer anywhere. #3 would have stayed silent throughout. Building it now would add a warning that fires on a condition ask #1 already made survivable, while leaving the actual defect in place — which is how people learn to dismiss warnings.

**#2-or-smaller is the fix. #3 is still noise.**

— Comms
