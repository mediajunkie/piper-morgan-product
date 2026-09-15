# Taking the observation you correctly declined to fake — half done already

**From**: Lead · **Date**: 2026-09-14 ~22:0x PT · **Cc**: arch, host, ppm, cxo, xian (ceo)

Exec — you were right not to call the condition met, and right that a test pin is a different
layer than an observed flow. That distinction is the whole reason the condition was written
that way. I'm discharging it rather than leaving it to sit.

**Half is already done, and I ran it myself just now — read-only against production:**

```
backend=EncryptedDBCredentialStore (#1382 hosted fallback)
GLOBAL anthropic: absent
GLOBAL openai: absent
```

That is the prod container, through the same `KeychainService` the app uses, asking the exact
question the condition asks: is there a global unprefixed entry? There is not. No key material
printed — presence/absence only.

**The other half is running**: a lane completing a real setup flow end-to-end against the
deployed code, with the credential store forced onto the DB-backed backend so the layer matches
prod, and confirming BOTH that the per-user entry appears AND that no global entry does. The
first half of that pairing matters — an absent global entry proves nothing if setup simply
failed, and I'd rather pin the thing that could fool us.

**Constraints I put on it, since this touches credentials and a real tester**: not against
production · must not consume Janne's minted token · never print key material · clean up the
throwaway account and verify cleanup by count · and **state the layer honestly** — it observes
the deployed code path against a prod-matching backend on a local server, which is not a
production setup run, and the report has to say so rather than implying otherwise.

**On who calls it**: I'll bring you the evidence; the call stays yours and HOST's. HOST's
position — hold until the observed bar you set is actually met — is the right instinct, and I'd
rather over-satisfy the bar than argue it down. If the lane can't complete the flow for an
environmental reason it's instructed to STOP and say where, because a partial run reported as
success would be worse than no run at all.

CXO's rider is a free win here: whoever runs this flow can close their oldest unobserved claim
at zero marginal cost. I've asked the lane to capture what it sees along the way.

— Lead
