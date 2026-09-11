---
from: host
to: xian (ceo)
cc: exec
subject: "Retention policy scaffold drafted — headline trust property, hosted/self-hosted split, and one open question I actually weighed rather than just recording your lean"
in-reply-to: brief-exec-to-host-cc-pm-draft-a-retention-policy-your-remit-per-pm-2026-08-13.md
date: 2026-08-13 13:3x PT
---

Drafted: `docs/legal/data-retention-policy-DRAFT.md` (`4015271f4`).

**Spot-checked Exec's ground truth before building on it** rather than accepting it at face value —
ADR-079's CI wiring, `user_id` scoping in both learning-path files, and the #1366/#1373/#1613 issue
numbers all confirmed independently. All held.

**Structure, following your four framing points:**

1. **The no-cross-user-learning claim leads, as you asked** — framed as a scope claim, not a duration
   claim: *"What you tell Piper, and what Piper learns from working with you, stays yours."* Backed by
   ADR-079 being CI-blocking (a ratchet test, not a convention), with the honest #1366 precedent cited
   rather than hidden — I think stating "this happened once, here's what changed structurally
   afterward" is a stronger trust claim than implying it never could happen, and the draft says so.
2. **Hosted vs. self-hosted split as two separate claims**, not one policy with a footnote. Self-hosted
   section says plainly there's nothing for us to promise there — it's not our data.
3. **Hosted retention practice stated as fact**: indefinite, no self-service deletion, matching what's
   already in the privacy-policy draft's 🔍 marker.
4. **The default-retention-limit question — I gave you an actual read, not just your lean back to you.**
   I agree with "no default limit," but for a reason I'd stand behind independent of your steer: the
   product's own pitch is persistence as a core function, and a default expiry would quietly undercut
   that promise rather than serve it. Written into the draft so it's a position with a reason attached,
   not an echo.
5. **The settings question (should users get configurable retention prefs) is left genuinely open**, as
   you framed it — I did note it gets a stronger case *if* §4's "no default limit" holds: a product
   that won't impose a limit has a better story if it can point to a user-controlled one. That's a
   connection worth having in view when you decide, not a pre-decision.

This is a scaffold to react to, same spirit as your ask — not a locked draft. Whenever you're ready.

— HOST
