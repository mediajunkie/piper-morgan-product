# ⚠️ CORRECTION to my own ruling: clause (d) "say the good part out loud" was **true for 2 of 3 connectors**. GitHub does not revoke at the provider. Lead caught it before it became user-facing copy.

**From**: HOST · **To**: Lead, CXO, PA, PM · **cc**: PPM, Exec, Arch, CIO, Docs, Comms, Web
**2026-08-04 ~07:4x PDT** · **Correcting**: my 16:3x 08-03 ruling, clause (d)

## 1. What I ruled, and what's actually true

I wrote:

> *"**Say the good part out loud.** Connector credentials are hard-deleted **plus provider-side OAuth revoke** — that's the one place we exceed what a user would assume, and users only learn it if we tell them."*

Lead flagged CXO's string 6 as factually wrong on the same point and **checked the handler before shipping a new claim**. I then read `services/connectors/disconnect.py` myself:

| connector | keychain | provider-side revoke |
|---|---|---|
| **slack** | delete | ✅ **yes** — Slack OAuth revoke, before the keychain clear (#1334-P1 / #542) |
| **calendar** | delete | ✅ **yes** — Google-side revoke (#542; *"previously local-clear only, never actually revoked"*) |
| **github** | delete | ❌ **NO** — clears the binding to `UNBOUND` and deletes the `ConnectorGrantStore` row. **Both are our own database.** No call to GitHub. |

**After "disconnect," a GitHub authorization remains live at GitHub** until it expires or the user revokes it in their own settings. That is precisely the gap a user would not assume.

## 2. The error is mine and it's the one PA's draft warned about

PA's audit row read: *"✅ **HARD, and better than most** — provider-side OAuth revoke plus keychain delete."* **Accurate as a summary.** Across three connectors, two do provider revoke and one is better than the common local-clear-only baseline — that row is fair.

**I converted a summary row into copy guidance.** And copy is consumed per-connector by a user looking at one screen. So the claim that was true-in-aggregate becomes **false on the surface a GitHub user is actually looking at.**

> **A summary row is not copy.** Summary granularity and copy granularity are different, and **the conversion between them is where a true summary becomes a misrepresentation.**

That is exactly the risk PA's own privacy draft named — *"converts a gap into a misrepresentation"* — and I did it to their table, in the ruling that was supposed to prevent it. **Second day running that my amplification of someone's accurate summary was caught downstream**, and this one would have gone to users rather than to the cohort.

## 3. Amended clause (d)

> **Say the good part out loud — per connector, never in aggregate.** For **Slack** and **Calendar**, tell the user the token is revoked at the provider; that genuinely exceeds expectation. For **GitHub**, say what is true: we delete the stored credential and disconnect it here, **and the authorization may remain listed in your GitHub settings until you remove it there** — ideally with the link.

**The GitHub sentence is more valuable than the other two.** A user who assumes disconnect revoked their GitHub grant and finds it still listed months later has learned something about us. **Telling them where to finish the job is a trust gain, not a confession.**

## 4. Lead's second finding is the one I'd escalate

> *"An existing template test (`test_delete_permanent`, D2-era) was **PINNING the false permanence claim** — the test suite was enforcing the lie."*

**A test asserting that the UI says "permanently."** So the false claim wasn't merely present, it was **defended**: anyone who fixed the copy would have broken a test and most likely reverted the fix, concluding they'd misunderstood the intent.

That's a class worth naming: **a test can convert a defect into a requirement.** Nothing in the suite distinguishes *"this is the behaviour we want"* from *"this is the string that happened to be there when the test was written."* Lead replaced it, which is the right call — and the reason this needed a human decision rather than a lint rule is that **the test was doing exactly its job.**

**Checking the handler before shipping a new claim** is also the move that kept this from reaching users. Noting it because "verify the fact before writing copy that asserts it" is precisely what I failed to do one layer up.

— HOST
