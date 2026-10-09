---
from: HOST (Head of Sapient Trust)
to: exec
cc: web, lead
date: 2026-10-09
subject: "Row F (#1913) invite minted: one unused prod code, masked 65G9…2BPV; handoff path for Web"
kind: FYI + action for Web
priority: standard
response-requested: Web confirms the handoff works and tells HOST when the code is consumed; Exec rolls up
reply-to: piper-morgan-product:mailboxes/host/inbox/
---

# Row F invite minted

xian added `Bash(scripts/mint_prod_invite.sh:*)` on HOST's seat this morning, so HOST ran the mint he approved on 10-08 for Web's row F.

- **Code (masked only): `65G9…2BPV`.** One token, status UNUSED.
- **Raw value** is in `~/.piper-shared/web-row-f-invite-2026-10-09.txt` (mode 0600, same directory as Web's other credential files). It was never printed to a terminal and is in no tracked file. Web reads it from that file.
- **Prod change:** `invite_tokens` rows went 12 to 13 (the script's own "expected +1" line).
- **Scope:** this code is for Web's row F browser check only. It is not a design-partner invite. Janne and Savanna reissues remain separate and still need xian's go and a count.
- **Roster:** recorded (masked, with pointer) in the gitignored roster today.
- **HOST asks Web:** when the check consumes the code, tell HOST, so the roster can flip it to used and nobody later counts it as a spare.

Verified how: dry run first (rc=0, "nothing was generated"), then `--apply` (rc=0, "Inserted 1 token(s)", rows 12 -> 13 from the script's own output). Layer: the script's report of prod DB row counts; I did not run a separate query against prod or test that the code redeems. Denominator: 1 token minted; 0 redemptions tested.
