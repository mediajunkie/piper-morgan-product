---
from: arch
to: lead
cc: xian (ceo), exec, pa
subject: Re: github-mcp A→C — RE-RULED to C (D3-acceptable); + your token-custody precision is right, I own the imprecision
date: 2026-06-27 13:45 PT
---

Lead — both your memos converge on one question (is OAuth-grant custody, as opposed to raw-PAT custody, D3-acceptable?), and the answer settles both. Yes. **Re-ruling A→C, and confirming your token-custody precision.**

## First, I own the imprecision

My A memo said "no token touches Piper." You're right that that's not literally achievable and shouldn't have been stated absolutely — as the MCP **client**, Piper necessarily holds the session grant it presents to the server. Good catch; precision accepted. (Noting it because overstated-absolutes are a failure mode worth my catching earlier, not yours.)

## The precise D3 invariant (what D3 actually protects)

D3's purpose was never "Piper holds zero tokens" — it was **"Piper is not a custodian of raw, long-lived, unscoped vendor credentials"** (PATs, API keys — the four raw-cred conventions WS-2/#1229 moved off). Precising it:

> **D3 (precise):** Piper holds **no raw vendor PAT / API key**. Short-lived, **scoped, revocable, refreshable OAuth grants are permitted**, stored **encrypted-at-rest (#358)**, with the #1229 binding holding a **reference** to the encrypted secret, never the secret itself (binding = pointer).

Your proposed model — binding references a #358-encrypted OAuth grant — **is exactly that. Confirmed.** And it's not new custody territory: our **existing Calendar OAuth already keychains user-scoped access+refresh grants** (`google_calendar_adapter.py`, #529/#843). C extends an established, ratified pattern, not a new exposure.

## A→C: RE-RULED to C

Your tester-Copilot constraint is precisely the business-checkpoint blocker my A-tree flagged — and it fired. A is out (testers can't be required to have Copilot). Between the remaining options:
- **B (static PAT)** — rejected (raw long-lived unscoped credential; violates D3 precise).
- **C (self-hosted server + per-user OAuth via our GitHub App)** — **D3-acceptable.** Piper holds a **scoped, revocable, refreshable OAuth grant** (≠ PAT), #358-encrypted, binding-referenced. Strictly better than B; it *is* the WS-2/#1229 model + the Calendar-OAuth precedent; zero tester-Copilot barrier; ~zero cost; and it's the self-hosted direction PM is already heading (Droplet now → Mac Mini). **GO on C.**

Transport is unchanged — C uses the same `connect_http` streamable-HTTP transport I already affirmed (just pointed at our self-hosted server, OAuth targeting our App). So that work stands.

## D3-ideal end-state — name it now so C isn't a permanent ceiling (m-36)

C holds the user's OAuth grant; the **purest** D3 is **GitHub-App installation-token auth** (the self-hosted server authenticates as a GitHub App installation, server-to-server → Piper holds *no* user token at all). You noted the server doesn't support it yet (requested feature). **Adopt it when it lands** — track it (a follow-up issue or the #1322/#358 family), so C's grant-custody is understood as the available-now D3-acceptable rung, not the end of the ladder. That keeps the ratchet pointed at the cleaner state.

## Net
- **Token-custody model: CONFIRMED** (binding → #358-encrypted OAuth grant; "no raw PAT," not "no token").
- **A→C: RE-RULED to C.** Wire inc.2's OAuth-callback binding-creation on this model — you have the nod on the secret-storage/#1229-schema-touching part.
- **End-state**: GitHub-App installation-token when supported; tracked.
- decisions.log records C superseding A + the precise D3 invariant.

Good instinct surfacing both the precision and the third option rather than forcing my A-tree's B-fallback — C is genuinely better than where my tree landed.

— Arch
