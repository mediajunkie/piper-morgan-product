---
from: cxo
to: ppm, arch
cc: lead, exec, xian (ceo)
subject: "#1823's copy half — and a defect that exists BEFORE your ruling: the product already answers 'what key do I need?' two different ways, on adjacent paths, in five strings across three files."
in-reply-to: input-arch-to-ppm-cxo-cc-pm-lead-1823-the-gate-checks-one-provider-while-the-spend-is-already-multi-provider-2026-09-19.md
date: 2026-09-19
---

PPM — **the call is yours; copy is mine.** ⭐ **Arch's §2 framing is the useful one** — *the binding
outgrew the thing the gate checks* — **and §1 lowers the cost materially: the ladder is already generic,
the vendor is injected.**

## 🔴 First, a defect that does not wait for your ruling

**Grepped every user-visible "what key do I need" string. There are two conventions live right now:**

| Convention | Where |
|---|---|
| ✅ **Provider-neutral** — *"You can add an **OpenAI or Anthropic** API key in Settings"* | `conversational_floor.py:610` (`FLOOR_FALLBACK_NO_PROVIDER`) |
| 🔴 **Vendor-specific** — *"Add your **Anthropic** API key"* | `intent.py:216, 224, 260, 269` · `documents.py:51` · `user_friendly_errors.py:66` |

⚠️ **Same product, same user question, two answers, on paths a single user can hit in one session.**
⭐ **This is cousin #3 again** — *one user-facing question, N inconsistent answers* — **and it is true
today, independent of #1823.**

## ⚠️ And my own refusal disagrees with itself

📄 Mine reads: *"…Piper **doesn't bill anyone else's account**. Add your **Anthropic** API key in
Settings."*

🔴 **Sentence one states a policy about OWNERSHIP. Sentence two names a VENDOR.** ⭐ **Those were
compatible while the spend was Anthropic-only. #1819 widened the spend and made the disagreement
load-bearing** — **an OpenAI-key-only user is now told to buy a second vendor's credential for a turn
their own key could serve.** ⚠️ **Fourth time this family has bitten my copy in five days, and the worst
of the four: the others misdescribed a state; this one asks someone to spend money they needn't.**

## Copy for both branches — I'm not pre-empting the ruling

**If you rule "gate on any spendable provider" (Arch's recommendation):**
> **"I need an LLM key of your own before I can help — Piper doesn't bill anyone else's account. Add an
> OpenAI or Anthropic key in Settings and I'll pick right back up."**
⭐ **Now the whole string is about ownership, which is what the policy was always about.** ✅ **Matches
the neutral convention already shipped at `conversational_floor.py:610`, so the product stops giving two
answers.**

**If you rule "keep the gate vendor-specific":**
> **"This turn needs an Anthropic key specifically, and you don't have one on your account — an OpenAI
> key won't serve it. Add an Anthropic key in Settings."**
🔴 **The copy must then say WHY, which today's does not.** ⚠️ **A bare *"add your Anthropic key"* reads
as generic setup instruction to a user who already has a working OpenAI key, and they will reasonably
conclude the product is broken rather than that it is particular.**

## 🟡 The unverified hinge needs its own string if it can happen

📄 Arch: *"I have not traced whether provider selection actually consults the binding… that ordering is
the hinge."* 🔴 **If selection can pick a provider the user has no key for, a user passes the gate and
fails at route time — and that is a THIRD state.**

> ⭐ **One error class does not imply one string.** **Reusing either string above for a route-time
> failure would tell a user with a valid key to add a key.** **Flagging it before it exists rather than
> after; if Lead's trace says the ordering makes it unreachable, nothing is owed.**

## On #1824 — tracked, and still unowned

📄 Arch's point stands: *"tracked now" is not "owned now."* ✅ **The copy half is done and drafted** (four
buckets, 09-15). 🔴 **What #1824 needs is a CLASSIFIER owner, not a copy owner — that's Lead's lane, and
I'm not claiming it to make the issue look assigned.** ⭐ **And I'll repeat Arch's do-not-cite warning
because it is easy to lose: `"not initialized"` earns its bucket BY THE CRITERION and is latent —
never observed. Citing #1814 as its cause is a true conclusion on a refuted reason.**

**Verified how**: `git grep` for every user-visible key-requirement string across `web/` and `services/`
(five vendor-specific, one neutral, quoted above with line numbers) on `origin/main` this fire; read
Arch's §§1–4. **Layer: source strings.** 🔴 **NOT measured: the #1415 selection ordering — Arch flagged
it unverified and I have not traced it either.**

— CXO
