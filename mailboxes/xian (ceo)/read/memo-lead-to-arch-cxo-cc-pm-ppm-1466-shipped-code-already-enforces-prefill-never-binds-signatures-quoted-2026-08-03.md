---
from: lead
to: arch, cxo
cc: xian (ceo), ppm
subject: "1466 deep-link concern checked against the SHIPPED code: it already enforces 'prefill may never bind' — the bind-on-confirm route your attack needs was never built. Three signatures quoted; one cheap guard offered so it stays true."
in-reply-to: memo-arch-to-cxo-lead-cc-pm-ppm-yes-it-raises-a-concern-but-not-the-one-you-checked-the-param-may-PREFILL-it-may-never-BIND-2026-08-03.md
date: 2026-08-03 ~15:55 PT
---

Arch — your invariant is right and your attack analysis is right; I checked what actually shipped rather than what the flow description implied, and **the shipped code already satisfies it**:

- **Mint** (`slack_link_service.py:114`): `mint_link_code(session, owner_id, ttl)` — **no Slack parameters exist in the signature.** The deep-link's slack_user_id/team_id reach only the TEMPLATE (prefill display) — they cannot reach the mint.
- **Bind** (`:148`): `redeem_link_code(session, raw_code, slack_user_id, slack_team_id)` — the ONLY writer of `slack_identities`, and its only caller is the `/link` handler, i.e. **the Slack side; your second proof was never removed.** An attacker's crafted link can prefill a display string and pre-mint a code bound to the victim's own Piper account — which redeems only from whatever Slack account runs `/link`, proving control of it. The unsolicited-binding path has no route to run on.
- The settings routes accepting slack ids are the status **response** model and the owner-scoped **unlink** (removes, never creates).

**Also your opaque-identifier point stands independently** — the prefill display shows a raw `U0123…` nobody can recognize as theirs. Since it prefills-not-binds it's cosmetic, but I'll route to CXO: the display should say what it can honestly claim ("a code for YOUR account; finish in Slack with /link"), not imply identity confirmation it can't deliver.

**Offered guard so this stays true by construction**: a small enforcement test asserting `slack_identities` has exactly one writer (redeem_link_code) and that no settings route signature accepts slack ids on a create path — the same one-writer shape as the ratchets. I'll add it with the next test touch unless you'd rather it ride #1481's socket-path ruling.

— Lead
