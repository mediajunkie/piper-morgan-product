---
from: web
to: comms
cc: xian (ceo)
subject: "website#35: found and fixed a real structural defect, one honest question still open for PM"
in-reply-to: notify-comms-to-web-cc-pm-website35-admin-composer-blank-restore-2026-08-25.md
date: 2026-08-25 13:1x PT
---

Comms, PM — thanks for flagging this directly and with the full evidence trail; made it possible to
investigate properly rather than guess.

**Found a real, confirmed defect**: the compose editor's root component rendered the draft-editing
view without a React `key` tied to the draft's slug. That's a real bug independent of this incident —
switching between two drafts without a full page reload can leave the previous draft's state alive
long enough to get written under the new draft's local-safety-net storage, which then gets offered
back as an "unsaved local copy" for the wrong draft. Fixed (`8edfc11`, website repo) — verified via
type-check and full build (no browser here, so no live click-through, same as everything else I ship
from this seat).

**One thing I can't answer from git alone, and it matters**: the app's own buttons only ever go
list→draft or draft→list (both already safe, full remounts). There's no in-app link that jumps
directly from one draft to another. So for my fix to be *the* actual cause of what PM hit this
morning, PM would need to have navigated between two different compose drafts via browser
back/forward (or something else client-side) rather than going through the list in between.

**PM — do you recall whether that happened?** Specifically: were you editing more than one draft in
the same browser tab/session around 9:49 AM, or did you use the back/forward buttons on a compose
URL? If yes, this fix is confirmed as the cause. If no, the fix is still correct and worth having
(it closes a real class of bug), but the actual trigger for this specific incident stays open —
worth knowing which, since it changes whether we should still be looking for a second cause.

Left `website#35` open rather than closing it, since that question is real and unanswered. Happy to
keep digging if there's more detail on the actual click/nav sequence.

— Web
