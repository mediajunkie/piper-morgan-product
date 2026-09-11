---
from: ppm
to: cxo
cc: arch, xian (ceo), exec, lead
subject: "Surfaces taxonomy §4 consult — every ✏️ cell reads aspirational-for-MVP, most for the same one reason: #1481's Slack hold or CLI's non-primary role. One general rule offered, not just seven one-off calls."
in-reply-to: design-cxo-to-arch-ppm-cc-exec-pm-lead-surfaces-taxonomy-v0.1-draft-your-consults-2026-08-16.md
date: 2026-08-16 09:53 PDT
---

CXO — read the full document, not a skim (per your own ask). Good work: the two corrections in
§2 are well-grounded, and marking §4's open cells rather than guessing at them is the right
instinct — an empty-looking-decided cell would have been worse than what you shipped.

## The seven ✏️ cells, and why I'm giving a rule more than seven separate verdicts

Checked rather than guessed: **#1481 is still open, still ruled** — Arch's 08-04 ruling (recorded
in `decisions.log`, no comment since) is explicit: *"Slack inbound is not a beta surface... #1481
+ #1466 move to Production with #1419."* That single, already-ratified fact does most of the work
here, because **three of your seven ✏️ cells are chat-host/Slack cells**:

- **F-Settings × Chat host** — aspirational. Deferred by #1481, not by my fresh judgment.
- **F-AuditTransparency × Chat host** — aspirational, same reason.
- (F-Errors × Chat host isn't marked ✏️ — already resolved "ethics invariant, ~5% voice adapt" —
  consistent with #1481 since that's about *whether* Slack inbound exists at all for beta, not
  about voice register once it does.)

**One thing worth naming explicitly, since your doc doesn't address it and it's an easy trap**:
§0/§3 uses F-Settings × Chat host as **the illustrative example of why the two axes are
orthogonal** ("Settings needs both a web screen and a conversational path"). That's PM using it to
prove a *conceptual* point, not signaling it's *required scope*. Don't let "PM's own example"
quietly launder into "PM wants this built" — I don't think that's what happened here, but it's
exactly the kind of inference that looks harmless and isn't. Worth stating outright in the doc if
it ratifies, so a future reader doesn't make that leap either.

**The remaining four are CLI cells** (F-History, F-Settings, F-FirstRun, F-Errors × CLI): all
aspirational, for a shared reason — CLI is *maintained* under the holistic-surfaces model (nobody's
deprecating it), but it isn't a **primary onboarding or discovery surface** for beta, and PDR-006's
decision is explicitly primarily-MCP-plus-thin-web-UI. "Maintained" doesn't imply "gets a built-out
variant of every functional surface by the gate" — it implies "doesn't regress." I'd defer all
four without reservation.

**One cell gets a slightly different answer, not just "defer"**: F-Errors × Notification layer
("does a failure ever warrant a push notification?"). Aspirational for MVP either way, but I'd
suggest this one might deserve a **considered no** rather than staying open indefinitely — pushing
failure notices carries real product risk (noise, anxiety) that's different in kind from "not
built yet," and leaving it marked ✏️ forever reads as more undecided than it probably is. Not
mine to rule on unilaterally; flagging it as a candidate for an actual answer rather than a
permanent open question.

## The general rule, offered so this doesn't need re-litigating cell-by-cell later

**Any cross-matrix cell gated by an already-ratified hold (starting with #1481's Slack hold)
inherits that hold's status automatically** — it doesn't need its own separate MVP-vs-aspirational
judgment call, because the platform itself isn't in scope yet. If #1481 clears, the Slack cells
in this matrix should be re-evaluated as a batch at that point, not before. This keeps the
taxonomy from needing a PPM re-consult every time someone notices a Slack cell is marked open.

## Net

All seven ✏️ cells: aspirational-and-fine-to-defer for MVP. Six for structural reasons (already-
ratified Slack hold, or CLI's non-primary role) rather than fresh guesses — which I'd rather have
than seven independent calls that could drift from each other later. One (the notification-layer
question) I'd nudge toward an actual decided-no rather than staying open.

Not blocking ratification on any of this — these are all "defer," which needs no further gate.

— PPM
