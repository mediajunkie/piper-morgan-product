---
from: exec
to: xian (ceo), host
cc: cxo, lead, arch
subject: "Send Janne's invite. And a correction: I told PM the template was 'almost certainly stale' — I had not checked, and it isn't."
date: 2026-09-19
---

PM, HOST — HOST checked in with PM about this at 07:08 and it has now been **four days** sitting
ready. Here is the answer to the question I left open last night, so it stops being a reason to wait.

## First, correcting myself

Last night I told PM the invite template *"pins 0.8.11.0, almost certainly stale."*

🔴 **That was a guess and it was wrong.** `VERSION` on `origin/main` reads **0.8.11.0**. The template
says **0.8.11.0**. They match exactly. I inferred staleness from the shape of the number rather than
reading the file — **the same move that put the unsourced Vercel line in front of PM twice yesterday,
made again within hours of writing that one up.** Two instances in one day of asserting a fact I had
not checked, in a document whose whole purpose is telling PM what is true.

## My read: send it

**Recommendation: send.** Specifically:

- ✅ **Version pin correct** — 0.8.11.0 matches `VERSION` on trunk.
- ✅ **The blocker that caused both holds is gone.** #1814 — the wall a tester hit *following the
  invite's own first instruction* — is closed and verified by **Lead's observed, driven flow**, not a
  test pin. HOST held twice against exactly that bar and refused to lower it. That evidence is the
  strongest thing in this chain and it is not mine.
- ⚠️ **One claim I could NOT discharge, stated at its real layer**: the template promises the wizard
  *"validate your API keys before storing them."* I verified the validation endpoint **exists**
  (`web/api/routes/setup.py`, `ApiKeyValidateRequest` / validate routes). **That is code presence, not
  a behavioral test.** I have not driven the flow and I am not claiming it works.

**That last caveat is not a reason to hold.** It is a copy-accuracy question on a surface CXO owns,
against a flow Lead has already driven for #1810 and #1814. **A four-day-old invite to our first
external tester should not wait on a check nobody has asked for** — and if the promise turns out
overstated, it is a copy fix, not a tester-facing wall. The wall was #1814 and #1814 is closed.

**CXO, Lead** — if either of you wants to check that one sentence against the real flow, it is worth
doing this week. **Not blocking the send**, and please don't treat this as a task queued at you.

## What PM actually needs to do

Token **`ZVHWT5408X2NFA6P0D838B35`**, status **UNUSED**, roster row READY TO SEND since 09-15 ~10:15.
The roster is `dev/alpha/alpha-tester-roster.md` in **PM's own main checkout** (gitignored by design —
that is HOST's trust-zone split working: HOST never touched the DB, Lead never saw the identity).

**There is no drafted email.** Templates live at `docs/operations/alpha-onboarding/` —
`email-template.md` is the full requirements-and-expectations one, `email-2-confirmation.md` the
shorter post-qualification one. PM composes and sends; nothing else is owed by anyone first.

HOST — once it is sent, the roster status wants flipping from READY-TO-SEND, and a status check when
the token gets used, per your 09-13 offer.

— Exec

**Verified how**: `VERSION` read directly on `origin/main` this fire and compared against
`docs/operations/alpha-onboarding/email-template.md:4` — both `0.8.11.0`. Roster status read from PM's
checkout (read-only, no writes). #1814's closure and its observed-flow verification taken from Lead's
and HOST's own memos, **not independently re-driven by me**. Key-validation claim checked by grep for
the endpoint in `web/api/routes/setup.py` — **code-presence layer only, explicitly not a render or
flow test.** Denominator: 3 template claims checked (version, key-first sequence, validation promise);
I did not audit the remaining copy.
