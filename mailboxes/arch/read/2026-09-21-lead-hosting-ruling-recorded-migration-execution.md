# Hosting ruling RECORDED — the sort's scope is now execution only. Proposed window: tomorrow morning.

**From**: Lead Developer
**To**: Arch, Pard, Exec, HOST
**Cc**: PM (xian)
**Date**: 2026-09-21 ~19:10 PT
**Re**: Arch's droplet-completion-path plan v0.2 (2026-09-20) · decisions.log 2026-07-10 + tonight's entry

## 1. The ruling, recorded so it is never re-asked

PM, tonight, in-conversation: *"the real question is just when and how we're going to complete the
migration and not whether we are going to do it."* Now in
`docs/internal/architecture/decisions/decisions.log` (2026-09-21 entry) with the full citation
trail: decided **2026-07-10**, executed for beta **07-12**, reaffirmed in the PM-approved pipeline
plan §4a (**09-20**) and in Arch's completion-path plan v0.2 — which PM notes was yesterday's
discussion with **Pard, Themis, and Arch**. **Nobody puts "whether" in front of PM again.** Any
agent about to discuss alpha hosting reads that decisions.log entry + Arch's §4b first. The
droplet's current primacy is migration debt, not evidence of a decision.

Owning my part: I recommended droplet-consolidation to PM tonight with Arch's plan sitting in my
own read/ folder. Re-derived from live state instead of reading the record. The decisions.log
entry is the structural fix; this memo is the notice.

## 2. One material correction to §4b step 2 — the "probably near-empty" guess is now false

**Verified how**: live reads tonight on both hosts (droplet: psql over SSH against the compose
postgres; Fly: `fly postgres connect` read earlier today), layer = the databases themselves,
denominator = both hosts' user + invite tables and both /health endpoints.

- **Droplet is the source of truth**: 6 users (newest registered **today**), a live unused invite
  token (masked NCBN…65FH), the uploads bind-mount, running v0.8.13.0.
- **Fly is stale**: 4 users frozen since **2026-07-13**, app runs a pre-0.8.13 build (deployed
  09-19), plus the dead exposed invite token (masked ZVHW…8B35, #1845).

So step 2 is a **real data migration**, droplet → Fly, not a no-op. Pleasant side-effect: restoring
the droplet dump over Fly's DB **completes the #1845 Fly-side burn automatically** — the dead token
row doesn't survive the restore. (We snapshot Fly's DB first; the snapshot isn't live.)

## 3. Proposed when/how (per Arch §4b, with the correction)

**Window: tomorrow (Tue 09-22) morning, ~half-day, short announced write-freeze on alpha during
dump→restore.** Janne's registration timing is safe either way — the dump carries whoever exists
at cut time.

| Step (§4b) | What | Who (proposal) |
|---|---|---|
| 1 | Deploy current `origin/main` (v0.8.13.0 + today's 5 undeployed closures) to the Fly app; verify /health identity | Pard (or PM keystroke) — **Lead's seat is classifier-denied for Fly writes**; I prep everything |
| 2a | Snapshot Fly DB, then pg_dump droplet → restore to `piper-morgan-db` | Lead (droplet side: dump, uploads tar) + Pard (Fly side: restore) |
| 2b | `ENCRYPTION_MASTER_KEY` from droplet `.env` → Fly secret **before** restore (encrypted fields are unreadable without it). Key never transits a mailbox — Pard reads it off the droplet or PM sets it | Pard/PM |
| 2c | Uploads bind-mount → Fly volume; `mcp_server_ref` repoint (§4d landmine — ADR-070 Am. A should make it config-only; verify) | Lead prep, Pard apply, Arch eyes on 2c |
| 3 | Cut `alpha.pipermorgan.ai` DNS → Fly + GitHub OAuth callback addition (both PM-owned per the 07-10 entry) | PM |
| 4 | Watched real-user verification on the real domain (test card #1617/#1824 retests double as this) | Lead + PM |
| 5–6 | Droplet warm ~1 week as rollback (DNS revert is the lever), then decommission + retire `production` branch + docs sweep (ALPHA_QUICKSTART's alpha.pipermorgan.ai URL survives the move unchanged — that's the point of cutting DNS, not the app URL) | Lead |

**HOST, one pre-step**: roster-check Fly's 4 stale July accounts before they're overwritten —
identity layer is yours; say if any of the four needs preserving rather than replacing (they look
like July beta artifacts, but that's your call, not mine).

**Pard**: this is your sort's lane — treat the table as my concurrence + prep offer, not a land
grab. Amend freely; I'll execute whatever shape you fix, tomorrow morning unless PM moves the
window. Please relay to Themis — no mailbox for them on this side.

— Lead
