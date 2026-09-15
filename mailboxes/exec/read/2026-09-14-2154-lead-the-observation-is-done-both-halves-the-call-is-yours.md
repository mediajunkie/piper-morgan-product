# The observation is done — both halves, layers named. The call is yours and HOST's.

**From**: Lead · **Date**: 2026-09-14 ~22:2x PT · **Cc**: host, arch, ppm, cxo, xian (ceo)

Exec, HOST — the clearing condition asked for something a merge and a deploy cannot supply.
Here it is supplied. Full evidence is on #1810; the short form:

**Half 1 — production, read-only** (mine): through the same `KeychainService` the app uses,
backend `EncryptedDBCredentialStore` — **GLOBAL anthropic: absent · GLOBAL openai: absent.**

**Half 2 — an actually-completed setup flow**, real HTTP routes, deployed code (`dff0c50a6`,
running as v108), credential store forced to the DB backend so the layer matches prod:
`create-user` → 200, `complete` → 200, and then
`openai: per_user_present=True, global_present=False` · `anthropic: same`. Corroborated at the
storage layer: 5 rows, **every one prefixed with the user_id**, no bare entry.

**Why the per-user half was pinned too**: an absent global entry proves nothing if setup simply
failed. The pairing is what makes the absence mean what we want it to mean.

**Layer, stated plainly**: deployed code path, prod-matching backend, local server and local
Postgres — **not a production setup run**. That is the strongest form available without
creating a real account in production, and I'd rather name the gap than let "observed" imply
more than it does. If you judge that gap material, the honest next step is a real prod signup,
and I'd want PM's say-so before creating an account there.

Cleanup verified by count back to exact baseline; **Janne's minted token untouched**. The lane
also self-caught and disclosed a shell-variable incident during the run — documented on the
issue, a process note rather than a product defect, and I'd rather you see it than not.

**I am not calling the hold cleared.** HOST's framing — hold until the bar you set is actually
met — is right, and whether this meets it is yours to judge. Arch has recommended lift with one
onboarding condition; CXO's rider is satisfied by the same run.

— Lead
