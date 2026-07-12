---
from: lead
to: exec
cc: xian (ceo)
subject: "Cutover-day status (PM-requested update): beta.pipermorgan.ai LIVE end-to-end; #1390 scanner-starvation found+fixed+deployed same hour; sprint issue-list drained; #1386 gate execution starting now"
date: 2026-07-12 ~13:45 PT
---

Exec — PM asked me to update you as today's work landed (PM is heads-down on Klatch for a stretch). It has landed:

## Landed today
- **beta.pipermorgan.ai is LIVE end-to-end**: PM's DNS + cert issued; dedicated "Piper Morgan Beta" GitHub OAuth app registered + secrets set (PM-driven, secret never in chat); URL vars flipped to the beta domain; health/auth/chat/GitHub-read all verified on the real hostname. Alpha continues untouched in parallel (deliberate — internal testing + alpha invitees + PM/PA MCP-rig work stay on alpha).
- **#1390** — minutes after public exposure, ten internet-scanner IPs filled the ADR-076 session gauge and authenticated users got "at capacity." Root-caused (anonymous principals shared the user-session gauge), fixed (gauge counts authenticated sessions only; per-IP rate limit unchanged), 15/15 tests, deployed to beta, live-verified. Found before any tester saw it.
- **#1332 CLOSED** (66h soak, zero recurrences) → **the Beta Blockers sprint issue-list is fully drained.**
- **Deploy-environments doc** (PM-requested): `docs/internal/operations/deploy-environments-and-release-train.md` — current two-branch/two-environment practice + the phase 2-4 proposal (canary split → public-beta flip → 1.0 three-tier), phases 2-4 explicitly unratified.
- Reply-ledger memo you already have: PA remains the one open thread.

## Starting now (PM pre-authorized: unblocked Beta Blockers + gate testing + Production-milestone cherry-picks)
#1386 gate execution, per PPM's gate-against-the-Fly-artifact recommendation: criterion 5 (boundary-integrity in the deployed artifact), criterion 2 (canonical suite fresh run), scenarios B/C via the live API (scenario A's fresh-account OAuth needs a human browser — it doubles as PM's cutover smoke). Then #1388 / ADR-070-A resolver from the Production milestone.

— Lead
