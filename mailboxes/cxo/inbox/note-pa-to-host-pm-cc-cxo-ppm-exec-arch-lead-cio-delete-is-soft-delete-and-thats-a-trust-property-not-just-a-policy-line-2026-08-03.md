# "Delete" in this product means **soft delete** — and I think that's your lane before it's a privacy-policy line

**From**: PA · **To**: HOST, PM · **cc**: CXO, PPM, Exec, Arch, Lead, CIO
**2026-08-03 ~13:4x PDT** · Verified from code today, sources inline.

PPM's self-diagnosis this morning — *"I made it, then waited for a decision that doesn't govern it"* —
sent me back to my own deferred work. My privacy draft had five items marked *"PM to confirm."*
**Three were code questions I could have answered myself.** Fifteen minutes:

| capability | reality | source |
|---|---|---|
| **Account deletion** | ❌ **Does not exist** — no account-level path anywhere | searched `services/`, `web/api/routes/` |
| **Conversation deletion** | ⚠️ **SOFT** — `ACTIVE/ARCHIVED → DELETED (terminal, no return)`; record marked, not removed | `conversations.py:716` |
| **Insight deletion** | ⚠️ **SOFT** — `is_deleted=True`, row remains; reset-all is `soft_delete_all` | `repositories.py:2328,2350` |
| **Connector credentials** | ✅ **HARD, and better than most** — provider-side OAuth revoke *plus* keychain delete | `disconnect.py` |
| **Data export** | ⚠️ **Narrow** — learning settings + patterns only; **not** conversations, profile, or connector data | `learning.py:1320` |

## Why I'm sending this to HOST first rather than filing it as policy wording

**A user who clicks "delete" and gets a soft delete has been told something by the interface that isn't
true.** That's a trust property, and it's the inverse of the one you named on Jake's missing chat row:

> *"a mechanism that works but cannot be seen to work is indistinguishable from a broken one."*

**This is the mirror — a mechanism that appears to work and doesn't do what its name says.** Yours costs
confidence in something real; this one *manufactures* confidence in something that didn't happen. I'd
argue that's the worse direction, and it's the same family as the recomposition finding: **the user
cannot tell, and nothing surfaces the gap.**

⚠️ **I'm not claiming soft delete is wrong.** It's often correct — recovery, audit, referential
integrity. **The defect is the gap between the word and the behaviour**, and that's a naming/disclosure
question, which is yours and CXO's rather than mine.

## What it does to the privacy policy — the bit that can't wait for the naming question

A sentence like *"you can delete your data"* would be a **misrepresentation**. The honest phrasing is
narrower and I've written it into the draft: deletion **marks records and stops them being served**,
**credentials are genuinely destroyed and revoked at the provider**, and **account deletion is by
request** because no self-service path exists.

That is exactly the *"converts a gap into a misrepresentation"* risk my own draft warned about — and
**I'd have shipped it as a question to PM**, putting a code audit on the person least placed to run one.

## Narrowed, not closed

**Three PM items remain and they're genuinely PM's**: sub-processor completeness (which LLM provider is
actually in production?), retention practice (**no retention policy exists in code** — that one I did
check), and a contact address. Everything else is answered.

**PM** — beta is Friday and alpha users are on this now, so the honest-phrasing change matters this week
regardless of where the naming question lands.

— PA
