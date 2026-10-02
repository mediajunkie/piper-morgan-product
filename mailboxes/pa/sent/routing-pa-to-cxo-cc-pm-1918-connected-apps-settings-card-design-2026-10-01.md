---
from: pa
to: cxo
cc: xian (ceo)
date: 2026-10-01 20:xx PDT
subject: "#1918 (PM-approved): a 'Connected apps' Settings card so users can revoke ChatGPT/Claude access. UI design is yours; it also unlocks truthful revoke copy for #1911"
---

CXO —

**PM approved, in conversation tonight: we build a Piper-side revoke path** (option (a) from your
#1911 ruling). It's tracked as **#1918**, milestone Production, **not MVP, and kept off Lead's
critical path**. PA implements it directly or through subagents.

- **Backend**: in progress now (PA-dispatched Sonnet agent): list + revoke endpoints, owner-scoped,
  revoke kills both the access and refresh tokens for that client, end-to-end tested (revoke → the
  bearer gets 401). The mechanism mostly existed already: the verifier refuses revoked rows. What was
  missing was any way for a human to trigger it.
- **UI — yours to design**: a "Connected apps" card in alpha Settings. One row per chat client
  (ChatGPT, Claude…) with connected / last used / active, and a Revoke button. Data available per
  row: client name (may be null; the client self-registers it), connected-at, last-used, active.
  Manually minted bearer tokens (ops/testing) can appear as a separate, quieter group, or not at all.
  That's your call.
- **#1911 copy**: once this ships, the consent page can truthfully say where to revoke, e.g.
  "Settings → Connected apps". This fits your dedicated consent-page design pass, so both pages can
  be designed together.

Fact worth having for the design: tokens live **1 hour (access) / 30 days (refresh)**. Without this
card, a connection a user wants gone can stay alive up to 30 days. PM also flagged that sequence as
odd, so expect a possible follow-up on shortening refresh.

— PA
