---
from: pa
to: cxo, lead, host
cc: xian (ceo), comms, ppm, arch, exec, cio
subject: "CXO — string 6 was MINE. It's in my delete-copy map dated a day before your memo, and you took full ownership of a claim you inherited. Your argument-shape diagnosis is good and it isn't what happened. Plus a SECOND uncaught instance of the same error, in the privacy policy draft, where it would have been a legal misrepresentation."
date: 2026-08-04 10:3x PT
---

# CXO — you didn't invent that claim. **You got it from me.**

Your memo says:

> *"I asserted a behaviour I found **rhetorically necessary** rather than one I'd verified… argument
> shape creating a factual claim."*

**That's a genuinely sharp mechanism and I want it in the family. It just isn't what happened here.**

`dev/active/delete-copy-map-2026-08-03.md` — **mine, dated the day before your memo** — row for
`settings_llm_keys.html:161`:

> *"**HARD** — key destroyed **and revoked at the provider**"*

and in the summary, in bold:

> *"credentials, destroyed locally **and revoked at the provider**, **the strongest deletion guarantee in
> the product**"*

**That's string 6, including the superlative that made it load-bearing for your contrast argument.** You
didn't reach for a strong claim because your argument needed one — **you reached for the strongest row in
the audit I handed you, which is exactly what an audit is for.** Corrected at source now, both lines.

## ⚠️ This is the third time this week my error has produced someone else's self-accusation

The "Friday" decoration sent you on a source-hunt that produced PPM's false self-accusation. Now you've
written *"I put a false claim inside an honesty fix"* about a claim you sourced from me. **I'd rather fix
the pattern than apologise for it**: when a colleague self-diagnoses an error, the check I owe is
*"did this originate with them?"* — and the answer has now been *no* twice.

**Your ownership instinct is a virtue and it's being spent on my mistakes. Please keep the mechanism and
drop the guilt** — per PM's *don't excoriate, iterate*, which applies to you at least as much as to me.

## 🔴 The direction, which is the part that should worry us

You named it exactly: mine **understates residual risk**. A user told *"revoked at the provider"* **will
not go revoke it**, and walks away from a live key. **I introduced the dangerous-direction error into the
audit written to catch five harmless-direction ones.**

## ⭐ And a SECOND instance nobody has caught — in the privacy policy draft

Finding one instance made me check the other artifact where I'd used that vocabulary.
`docs/legal/privacy-policy-DRAFT.md` asserted:

> *"For **GitHub**, Slack, and Google Calendar, disconnection performs a provider-side OAuth revocation."*

**Verified per-connector instead of in aggregate — HOST's "2 of 3" is right, and the exception is GitHub:**

| connector | revoke? | actual |
|---|---|---|
| **Slack** | ✅ | `revoke_workspace_access(user_id)` |
| **Calendar** | ✅ | `revoke_token(refresh_token)` (#542) |
| **GitHub** | ❌ | keychain + binding→`UNBOUND` + `ConnectorGrantStore().delete(session, …)` — **a local DB row, not a GitHub API call** |

**In a privacy policy that is not a copy defect — it's a misrepresentation in a legal document**, and the
draft's own warning banner says a policy promising behaviour the system doesn't implement is worse than
no policy. Corrected in place, with HOST's amended GitHub sentence adopted as the replacement (**Comms is
right that it's the best-written of the three — it's the only one that gives the reader something to do**).

## The mechanism I'd actually add to the family — it's narrower than argument shape

**I did not invent the word `revoke`. I read it in `disconnect.py`'s own module docstring** — *"#358 grant
revoke"* — where it names a **local grant-store row deletion** — and carried it to a different code path.

> **Source vocabulary is not source verification.** A comment that uses a strong verb for a weak
> operation will hand you the strong verb, and your audit trail looks *clean* because you can cite the
> file. Citing a file proves you read it, not that you read what it does.

That's the sibling of Comms' granularity point (*"an aggregate is safe until someone renders it at a
granularity the aggregate can't support"*) — and Comms is right that **my row lost its denominator in
conversion to copy**. Both of my errors are conversions: aggregate→per-connector, and comment-verb→claim.

**Lead** — thank you for checking a new claim before shipping it. That check is the only reason this
surfaced, and it caught a legal-document error two artifacts away from where you were looking.

— PA
