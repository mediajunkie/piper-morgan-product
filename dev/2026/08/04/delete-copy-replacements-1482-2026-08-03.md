# Delete copy — exact replacement strings (#1482)

**Owner**: CXO · **Status**: READY TO APPLY · **Date**: 2026-08-03
**Map**: PA's `delete-copy-map-2026-08-03.md` — six surfaces, every claim sourced, no files changed.
**Tracked**: #1482 (PPM). **Application is Lead's** — copy is mine, code is theirs (the #1466 division).

> **Rule this applies** (HOST's ruling as amended, CXO's correction adopted): this is a **retraction**,
> not a disclosure. Five surfaces make a **false** claim; one makes **none where it would be true.**

---

## The replacements

### 1. `templates/home.html:1552` — delete conversation *(SOFT)*

❌ `'This cannot be undone.'`
✅ **`'It'll stop appearing in your workspace. We keep a copy for a while — ask if you need it back.'`**

> ⚠️ The function's own comment three lines above reads `// Issue #715: Delete a conversation (soft
> delete)`. **The correct fact was already in the file.**

### 2. `templates/insights.html:439` — delete an insight *(SOFT)*

❌ `'permanently remove … cannot be undone'`
✅ **`'This insight will stop being used. We keep it for a while — ask if you need it back.'`**

> **"Permanently remove" has to go first.** It's the strongest false claim in the set: not merely
> overstating durability, but naming a guarantee the system doesn't implement.

### 3. `templates/insights.html:478` — reset all insights *(SOFT — `soft_delete_all`)*

❌ `'cannot be undone. Type RESET'`
✅ **`'Piper will stop using everything it's learned about you so far. We keep it for a while — ask if you want it back. Type RESET to confirm.'`**

> **Keep the RESET ceremony.** The friction is right — this is a big action and deserves a speed bump.
> **What changes is the reason for it**: it's consequential, not irreversible. A type-to-confirm gate
> justified by a false claim teaches users that our ceremonies are theatre.

### 4. `templates/insight_controls.html:296` *(SOFT)*

❌ `'cannot be undone. I'll need to start learning from scratch.'`
✅ **`'I'll stop drawing on what I've learned about you and start fresh. We keep the old material for a while — ask if you want it back.'`**

> The *"start learning from scratch"* half is **true and worth keeping** — it's the consequence the
> user actually cares about. Only the permanence claim is false.

### 5. `templates/insight_card.html:608` *(SOFT)*

❌ `'permanently remove … cannot be undone'`
✅ **`'This will stop being used. We keep it for a while — ask if you need it back.'`**

### 6. ⭐ `templates/settings_llm_keys.html:161` — delete API key *(HARD — the inversion)*

❌ `confirm("Remove your <provider> key?")` — **no claim at all**

🔴 **MY FIRST VERSION WAS FALSE — corrected before shipping by Lead (2026-08-04).** I wrote *"we
destroy it here and **revoke it at the provider**."*

> ⚠️ **ATTRIBUTION CORRECTED 2026-08-04 (PA), and I verified it rather than accepting it.** I wrote below
> that my argument shape *produced* this claim. **It didn't — I inherited it.** PA's
> `delete-copy-map-2026-08-03.md` (`a570c87f0`, 08-03 **19:15**) already read *"key destroyed **and
> revoked at the provider**"* and called it *"the strongest deletion guarantee in the product."* My memo
> is `214d4e4a5`, **22:18 — three hours later.** The words are PA's; the shipping claim is mine.
>
> ⭐ **And the real mechanism is worse than the one I proposed, because it's one I had already written
> down.** I took a row out of an audit and promoted it into user-facing copy **without re-verifying it at
> the moment of copying** — which is *precisely* **m-46, Promotion Is a Re-Verification Event**, authored
> by me four days earlier. *A durable artifact is a COPY. Every copy needs a named source and a re-check
> at the moment of copying.* I had the named source. I skipped the re-check. **Authoring a methodology
> entry does not install it** — that's m-46 applied to m-46, and it belongs in the entry.
>
> **What survives of the argument-shape diagnosis, in reduced and more accurate form**: it doesn't explain
> where the claim came from, but it does explain **why I never doubted it.** The row was the strongest
> one in the audit, and my contrast argument *needed* a strong hard-delete claim — so the one row most
> load-bearing for my argument was the row I was least likely to challenge. **Argument shape as a
> suppressor of verification, not a generator of claims.** That is compatible with PA's account and, I
> think, the durable half.
>
> **PA also found a second instance** of the same inherited vocabulary in `docs/legal/privacy-policy-DRAFT.md`
> (GitHub disconnect asserted a provider-side OAuth revocation it doesn't perform) — where it was a
> misrepresentation in a legal document, not a copy defect. Corrected at source. `delete_user_key` removes the keychain entry and
the DB row; **no provider-revocation call exists, and none is possible** — only the key's owner can
revoke in their console.

⚠️ **And it was false in the more dangerous direction than the five it accompanied.** Those overstate
permanence harmlessly. **Mine understated residual risk**: a user told we revoked it **will not go
revoke it**, and walks away believing a live credential is dead. **A false claim causing inaction on an
active key**, introduced inside a fix premised on *the word must match the behaviour*.

✅ **Shipped (Lead), then voice-polished (CXO):**

> **Delete your `<provider>` key?**
> **Our copy is destroyed immediately and can't be recovered.** The key stays valid at `<provider>`
> until you revoke it there.

**Fact boundary (pinned by test): no provider-side revocation may ever be claimed; the residual step
must survive.**

⭐ **Note what the correction did to the contrast** — it made it *accurate*. Soft: *"we keep a copy —
ask if you need it back."* Hard: *"can't be recovered here."* **That is the true axis.** My *"really is
gone"* was reaching for a totality we don't deliver, and **the contrast argument was the pressure that stopped me
CHECKING the overclaim** (see the attribution correction above — I inherited the claim, I didn't invent
it): I had argued string 6's strength was load-bearing for the set, so the strongest row in the audit was
the row I was least likely to challenge. *A rhetorical structure that needs one element to be strong is a
pressure to under-verify that element.*

## Why the set works as a set, not six edits

**The contrast is load-bearing.** *"Can't be recovered here"* only carries information **because the
other five are honest.** Before the set, all six sounded alike — five falsely grave, one silent — so
**no delete in the product told the user anything about its own reversibility.**

*(This paragraph quoted "this one really is gone" until 2026-08-04 — the wording string 6 no longer
uses. Chased within the document, since a spec that argues for a phrase it no longer contains is the
same drift at smaller scale.)*

Fix five and skip the sixth and you've removed the falsehood but not restored the signal. **Ship them
together.**

## Three things deliberately preserved

1. **The RESET type-to-confirm gate** (#3) — friction is right, justification changes.
2. **"Start learning from scratch"** (#4) — true, and the consequence users actually care about.
3. **Every affordance.** Nothing is removed or made harder. **This is a copy change only** — no schema,
   no flow, no backend.

## What is NOT covered

- **Account deletion by request** — HOST's (c); needs a verified runbook before any policy sentence
  ships. Not copy, and not mine.
- **The privacy policy's erasure language** — PA/HOST's narrower phrasing; separate surface.
- **"We keep a copy for a while"** — ✅ **ANSWERED 2026-08-04 (Lead): no retention or purge policy
  exists.** No scheduled purge anywhere; soft-deleted rows are kept **indefinitely**. So *"a while"* is
  **honest but unbounded**, and it stays as written — **copy cannot fix the absence of a policy, only
  stop lying about it.** ⚠️ **The absence is a real finding** and routes to HOST's account-deletion
  runbook item (their (c)), not to copy: *"we keep it"* with no horizon is an unbounded claim of a
  different kind.
