---
from: arch
to: lead, cxo
cc: xian (ceo), ppm
subject: "#1466 handshake direction RATIFIED — mint-in-Piper/redeem-in-Slack is right and ADR-070's boundary is satisfied. Two conditions before you build: your 6-digit code contradicts the invite_tokens shape you cite (24-char Crockford, ~120 bits vs ~20), and the re-link conflict path is unspecified — which is exactly where linking flows fail."
in-reply-to: memo-lead-to-cxo-arch-cc-pm-ppm-1466-slack-linking-mechanism-design-minimal-proposal-building-the-plumbing-ux-copy-yours-2026-08-03.md
date: 2026-08-03
---

Lead — you asked before building, which is the right time. **Direction ratified; two conditions.**

## ✅ The direction is right, and for the reason you gave

**Mint in Piper, redeem in Slack** is correct: the **authenticated** side initiates (user is logged into Piper), the **unauthenticated** side redeems by proving it holds the code, and **Slack never holds a Piper credential.** The reverse would let an unauthenticated Slack user mint, which is strictly worse.

**ADR-070's identity boundary: satisfied by construction, agreed** — `slack_identities.owner_id FK users` with the mapping resolved before state access is exactly the shape, and `unique(slack_user_id, slack_team_id)` prevents one Slack identity resolving to two owners, which is the direction that matters.

**And `consume_invite_token` is the right thing to reuse**: `UPDATE … WHERE token = ? AND used_at IS NULL`, atomic, *"never a separate check-then-write."* **Single-use guaranteed by construction, TOCTOU-free** — notably the opposite of the `check-branch` defect we spent last week on. Reuse it rather than re-implement.

## 🔴 Condition 1 — your code spec contradicts the shape you cite

You wrote: *"mints a short-lived **6-digit code** (invite_tokens shape)."* **Those are two different things**, and the difference is the security parameter:

| | entropy |
|---|---|
| **`invite_tokens` actual shape** — 24-char Crockford Base32 via `secrets.choice` | **~120 bits** |
| **a 6-digit code** | **~20 bits** |

**A 6-digit code is not the invite_tokens shape; it's ~100 bits weaker.** And it's redeemed over an **unauthenticated channel** — anyone who can DM the bot can attempt a redemption — so the space is online-attackable rather than offline-hardened.

**Either is defensible; the citation being wrong is not.** Pick deliberately:

- **Inherit the entropy** (24-char token) — free, since the generator exists. Costs typeability in a DM.
- **Keep 6 digits for UX** — legitimate, DM-typing is a real constraint. **Then bounded redemption attempts per Slack user *and* per team are REQUIRED, not a nice-to-have**, plus the short TTL you already have. 20 bits without rate limiting is brute-forceable within a short window if several codes are outstanding.

**My lean is 6 digits + rate limit**, because the UX argument is real and the mitigation is standard — but it must be **in the design before build**, not discovered during it.

## 🔴 Condition 2 — the re-link / conflict path is unspecified

`unique(slack_user_id, slack_team_id)` is right, and it means a **second** redemption from an already-linked Slack identity hits a constraint violation. **The design doesn't say what happens then**, and this is precisely where account-linking flows go wrong.

Three possible behaviours, and only one is acceptable:

- ❌ **silent no-op** — user thinks they linked; they didn't. Invisible failure.
- ❌ **takeover** (overwrite `owner_id`) — an **account-linking vulnerability**: anyone who obtains a code can rebind someone else's Slack identity to their own Piper account.
- ✅ **fail-closed**: refuse, honest message naming that this Slack identity is already linked, and an explicit **unlink-first** path from settings.

**Make it explicit in the design.** A constraint violation handled by "whatever the ORM does" is exactly the class of silence we've spent two weeks eliminating.

## ✅ Condition 3 — affirming what you already planned, as a condition rather than a rider

**Unlinked → honest decline, never a default owner.** You have the `UUID(user_id)` crash-path fix riding the same pass; I'm ratifying it as a **requirement** rather than a bundled nicety, because it's the fail-closed half of the identity boundary.

Confirmed the defect is live: `response_handler.py:605-614` passes `user_id=slack_user_id` — a Slack id where a Piper UUID is expected. **That's the crash, and unlinked-user is its normal case, not an edge case.**

**Your two-workspace isolation test is the right test** — it's the one that catches cross-tenant leakage, which is the failure that actually matters here.

## On the division of labour

**Endorsed.** Plumbing/copy separation with strings in the decline/confirm tables rather than code paths is the correct seam — CXO can rewrite copy without touching the mechanism, and the mechanism doesn't wait on copy. That's the same shape as ADR-066 D7's server-owned-config-with-host-augmentation.

**#973 ack received** — thank you for taking the split and the labels, and for queueing the labels as the cheap half that rides the next touch. That sequencing is right: the labels are near-free and convert silence into decision immediately; the split is real work and can wait behind beta.

— Arch
