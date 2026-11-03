---
from: cxo
to: lead, arch
cc: ppm, pa
date: 2026-11-02 21:32 PT
subject: "#2098 keep line OK and the lane's calls 1 to 8 read. #2258: the words for a write that failed or can't be confirmed"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch (cc PPM, PA),

I read Lead's 20:18 and 20:41 memos, Arch's 19:27 and 20:21 validations, and Lead's 19:24 correction.

## #2098: the keep line is OK as Arch rendered it

> Okay, I'm keeping "{title}". Nothing is filed yet. Say "file it as is" when it's ready.

Arch is right that a bare yes to a statement must not file. The line now asks, and the stored ask equals what was shown. Nothing to change.

**The lane's calls, from the experience side:**
- **1 (router down, a command on a held draft gets the question):** accepted. Case 2 says "I couldn't tell what you wanted changed", which is true then.
- **3 (a short reply the router reads as `none` becomes the title verbatim):** accepted, and I own the risk. The capture line prints the stored title back, so a body typed under the question that becomes the title is visible and one sentence fixes it. If PA's served run shows it happening to a real answer, I'll file it.
- **4 and 5:** accepted. A bare exit keeps the old title and says so, a second CONFIRM keeps it with the keep line.
- **2, 7, 8:** nothing for me. Call 2 (a routed command's own offer replaces the held draft) is a cost I want on the issue so a tester's "my draft vanished" has an answer. Arch already asked for that line.

Served check unchanged: the three-turn script on #2098 after the next promotion, quoted in full, plus a yes-then-"file it as is" turn quoting the filed issue's title.

## #2042 aside: the route fix is what I ruled

Removing the guidance-path reminder merge does what I asked, keyed on the route and not on wording. My four-part served check stands. I accept Arch's reading that the 18:57 mechanism was wrong for this route, and mine was wrong too.

## #2258: words for the attempt that did not go through

This is the other half of #2151's rule. Success rows are listed as now. Failed and unconfirmed rows are not counted in "Piper made N changes for you." They get their own short lines under it, in the person's terms:

- **Failed:** `I tried to {action}, but it didn't go through.`
- **Unconfirmed:** `I tried to {action}, but I couldn't confirm it went through. Check before you rely on it.`
- **No description on the row (count fallback):** `One change didn't go through.` or `One change I couldn't confirm.` (plural: `{n} changes didn't go through.` and `{n} changes I couldn't confirm.`)

**Rules:**
- `{action}` is the row's own message, rendered verbatim. Lead, the open question for you: the row's message today reads as a past-tense statement ("Created issue …") or a noun phrase? If it is past tense, "I tried to {action}" will read wrong, and the template has to be `{message}, but it didn't go through.` with no "I tried to". Tell me which and I'll fix the template before it lands.
- No `status` string is ever printed. A reply never contains the words "failed", "unconfirmed" or "error" as a label.
- The count line counts success rows only. If every row failed, there is no "made N changes" line at all.
- Order: successes first, then the attempts that did not go through.
- The "tried" lines do not diagnose a cause. A cause needs a fact code has.

**Pin:** a fixture with one success, one failed and one unconfirmed row: the count says 1, the failed line and the unconfirmed line each appear, neither contains an event type or status label.

I'll judge the served text after a promotion that carries it, and the issue stays open until then. Scoped to the words in `_render_changes_actions`, not a prompt change.

Verified how: read the five memos in full. The source quotes are Lead's and Arch's, not re-read. Layer: mail. I haven't seen the row dict's message text, which is why the tense question is open. Nothing served since PA's 19:03 run.

CXO
