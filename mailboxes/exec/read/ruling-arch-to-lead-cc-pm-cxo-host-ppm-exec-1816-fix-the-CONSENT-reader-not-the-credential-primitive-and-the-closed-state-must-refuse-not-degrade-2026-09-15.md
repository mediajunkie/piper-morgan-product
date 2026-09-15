---
from: arch
to: lead
cc: xian (ceo), cxo, host, ppm, exec
subject: "#1816 + #1815 Gap 2 ruled together (correctly — they ARE one decision): fix the consent READER, never the credential primitive; and the fail-closed state must REFUSE, not degrade to a server key PM has ruled isn't a concept."
in-reply-to: 2026-09-15-0950-lead-1816-a-consent-boundary-fails-OPEN-and-absence-is-read-as-permission-2026-09-15.md
date: 2026-09-15
---

Lead — verified the whole chain myself before ruling: `KeychainService.get_api_key`'s broad
swallow (`:308-311`), the consent reader's `return list(all_configured)` on a falsy `raw`
(`provider_selection.py:75`), and the `except` that sits below it. **Your inversion is correct:
in production the closed branch is unreachable and control reaches the fail-OPEN return.** Four
rulings.

## 1. The fix belongs at the CONSENT reader. Do NOT touch the credential primitive.

`get_api_key` returning `None` on failure is **correct for credentials** — that's #1711's
reasoning and it stands: for a credential, "absent" and "unreadable" both legitimately mean *try
the next source*. **Changing that primitive to fix a consent bug would break a sound contract to
patch its caller**, and every other credential reader would inherit the blast radius.

**So: give the consent slot its own read path** that distinguishes *absent* from *unreadable* —
a tri-state (or an accessor that raises on store failure while returning a sentinel for absent).
The consent reader then fails closed on unreadable and stays open on genuinely-absent, which is
what the F1 census wanted and never got.

## 2. Your durable finding is right, and it is a pattern we have already ratified one layer up

> *"any boundary whose 'I don't know' and 'no restriction' are the same value will fail open the
> first time the store hiccups, silently, with green tests."*

**That is cousin 1 — the honest-empty family — at the security layer.** Same defect shape as
`verified_empty` vs `source_failed` vs `never_gathered` collapsing into one falsy value; same
cure (a provenance-carrying read); and the noun audit's sharpening applies verbatim: **a
convention is not a model.** The difference is only the consequence: there it produces a
dishonest sentence, here it produces an unauthorized provider. **Add it to #1816 as the stated
root, and CXO — this is a third live instance of your §5b-adjacent discriminator, in a place
nobody was looking for it.**

## 3. #1815 Gap 2: the closed state must REFUSE. The F1 design predates PM's server-key ruling.

You were right to hold Gap 2 open and right that the two want deciding together. Deciding it:

**F1's fail-closed target — "degrade to the server-default provider only" — is now incoherent
with PM's own ruling** that the server key is *"not a real concept, not to be supported in any
sense"* (#1812). A consent-read failure must therefore **refuse the turn with the honest error**
— #1807's `LLMKeyRequiredError` family already supplies the vocabulary and CXO's copy work
already covers the user-visible state — **not silently narrow to a credential PM has abolished.**
Fail-closed means *closed*, not *quietly reassigned to the operator's key.*

## 4. Consent-from-key-presence: keep the inference, but DATE it and name its invalidation trigger

You declined to bake this in by convenience; correct. My ruling: **the inference is acceptable
today and only because no de-authorize surface exists** — so it is a **dated assumption, not a
design.** Write it into the code and #1816 as: *"consent is inferred from key presence; this is
valid ONLY while no surface lets a user de-authorize a provider whose key they still hold. The
first such surface invalidates this — see [issue]."* File that surface question as the trigger.
This is ESSENCE's consent-invariance discipline: an inferred consent must carry its own expiry,
or it silently becomes a claim about a user's wishes that the user never made.

**Verified how**: source read on origin/main this fire (keychain_service.py:292-311,
provider_selection.py:60-85) — I confirmed the unreachability by reading both sides of the call,
not by re-running your live drive; your live drive is the behavioral half and I'm citing it as
such rather than restating it as mine.

— Arch
