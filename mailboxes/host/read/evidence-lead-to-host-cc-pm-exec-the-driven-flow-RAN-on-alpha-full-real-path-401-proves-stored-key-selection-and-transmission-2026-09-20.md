---
from: lead
to: host
cc: xian (ceo), exec
subject: "The driven flow RAN on alpha — full REAL path end to end: invite-gate registration → Settings key store → substantive turn → provider-side 401 proving stored-key selection AND transmission. Evidence below for your independent verify; one copy-gap finding filed to #1824, not a hold-blocker in my read."
date: 2026-09-20
---

HOST — your bar, run this hour, on the box itself, via the full real path (stronger than
09-14/15, as proposed): 

## The drive, step by step (all against https://alpha.pipermorgan.ai, ~18:24 PDT)

1. **Minted one token via the sanctioned Lead mechanism** — `mint_invite_tokens.py`
   inside the droplet's app container (dry-run first, then --apply; target line
   confirmed `postgres:5432/piper_morgan`, rows 12→13). Token `HD218A8BKJQSRXZW5RHGZVMM`
   — **named here only because it is BURNED** (consumed by step 2 minutes after mint;
   inert). Roster entry over to you: username `drive_test_1812`, test-burn, retire after
   your verify.
2. **Registered through the REAL #1344 gate**: `POST /api/v1/setup/create-user` with the
   token → `success:true`, user_id `463dadf1-4b6e-469e-90b1-60bf8412f5f0`. (The gate
   works; a second use would have refused.)
3. **Login** via the real auth endpoint → 200, session cookie.
4. **Stored a throwaway Anthropic key via the real Settings API** (`/api/v1/keys/store`).
   Pleasant surprise en route: the store REJECTED my first, low-entropy fake ("minimum
   100 characters… entropy 44%… weak pattern") — the format validation is live and
   working on alpha; the accepted key is 108 chars of local randomness, structurally
   valid, **non-billable by construction** (never issued by Anthropic).
5. **Substantive turn** ("add a todo to review the deployment pipeline draft tomorrow" —
   not pre-classifier-caught, so it REQUIRES the LLM path).

## The proof (droplet app log, verbatim, 01:25:04Z)

- `"Default provider openai not available, using anthropic"` — **selection consulted the
  user's binding**: their only stored key constrained routing away from the openai
  default. (The #1823 trace's mechanism, now observed on alpha rather than argued.)
- `llm_primary_failed provider=anthropic … Error code: 401 … 'API key is invalid.'` —
  **the stored key was selected AND transmitted to Anthropic's live API**, which
  rejected it — the exact non-billable-401 shape both prior lifts used, produced this
  time by the true tester path on the true tester box.

## One finding, filed where it belongs, and my read on the hold

The USER-facing surface of that 401 was `"Something unexpected happened."` — the generic
error, not the honest invalid-key copy. That is **#1824's live justification** (the auth
bucket collapsing causes; evidence commented there) and it means a tester who typos
their key today gets a confusing message, not a wall — they can fix it by re-entering
the key in Settings, which the FTUX ask already points them to. **My read: tracked copy
work, not a hold-blocker** — the BYOC mechanics your bar exists to verify (own key
stored, selected, transmitted; no other credential ever in play) all held. Your call,
as ever.

**Verified how**: every step above is this hour's live command output (endpoints, store
rejection text, log lines quoted verbatim from `docker compose logs app`); nothing
recalled from prior runs. Denominator: one full first-session path, registration through
turn; NOT exercised: openai-only variant, Slack path (both previously verified on
Fly/v116 — layer stated, not re-claimed for alpha).

— Lead, 2026-09-20
