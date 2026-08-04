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
✅ **`'Delete your <provider> key? This one really is gone — we destroy it here and revoke it at the provider. You'll need to paste a new key to reconnect.'`**

> **This is the only surface in the product where "really is gone" is TRUE, and it's the one place we
> don't say it.** Adding it is not extra ceremony — it's the strongest guarantee we ship, currently
> invisible.

---

## Why the set works as a set, not six edits

**The contrast is load-bearing.** *"This one really is gone"* only carries information **because the
other five are honest.** Today all six sound alike — five falsely grave, one silent — so **no delete
in the product tells the user anything about its own reversibility.**

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
- **"We keep a copy for a while"** ⚠️ — *"a while"* is deliberately vague **because I don't know the
  retention period, and neither does the copy.** If a real retention window exists, say it
  (*"for 30 days"*) — that is strictly better. **If none exists, "a while" is the honest word and the
  retention gap is itself a finding for someone.**
