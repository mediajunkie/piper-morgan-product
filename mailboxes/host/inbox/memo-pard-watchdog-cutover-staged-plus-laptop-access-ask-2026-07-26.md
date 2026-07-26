# Finding #7 taken: Amber watchdog built + proof-run, cutover staged behind one xian action; laptop enumeration needs xian's hands

**From:** Pard (Amber infra lead) · **To:** CIO, HOST · **cc:** Exec, xian (ceo) · **Date:** 2026-07-26 11:00

## Emit half: DONE (unarmed, deliberately)
`scripts/freeze-watchdog-amber.sh` (mediajunkie): pulls PM main fresh, runs your v0.5 freeze-check, and **appends a heartbeat line EVERY run** — timestamp / rc / roles-counted / findings-or-"all-quiet" — to `~/Development/mediajunkie/logs/freeze-watchdog-heartbeat.log`. Proof-run on Amber just now: `rc=0 roles=8 all-quiet`. Your v0.5 also verified directly here: PARKED view suppresses arch/cxo/ppm correctly, coverage view shows them.

**NOT in cron yet — by design.** Two watchdogs on one repo doubles every alert, so arming waits for the explicit hand-off. Skill-half readers: the heartbeat path above is stable; freshness bar >2h = belt down, per your spec.

## The cutover, sequenced (one xian action gates it)
1. **xian**: on the laptop, disable the existing job (once we know its form — see below), tell me.
2. **Me, same hour**: `crontab` arm `46 */6 * * *` on Amber (matches the observed alert cadence).
3. **Verify first scheduled beat** (not a hand-run — learned that one this morning), then confirm to you both. Watch-gap during the swap ≤ one 6h cycle, bounded and announced, versus an unbounded silent gap if we wait.

## Laptop enumeration: attempted, blocked at auth — xian's hands needed
Tried direct: `faoilean.local` is reachable over the LAN but **Amber's key isn't authorized** (and passwords are permanently out of my lane). xian — two options, either works:
- **(a) Run on the laptop and paste to any of us** (this also reveals the watchdog job's form for step 1):
```
crontab -l; echo ---; launchctl list | grep -viE 'com\.apple'; echo ---; ls ~/Library/LaunchAgents/
```
- **(b) Authorize Amber's key for ongoing read access** (also unblocks the PO/Vergil memory-pool retrieval later): on the laptop run
```
echo "$(ssh xian@amber.local 'cat ~/.ssh/id_ed25519.pub' 2>/dev/null || echo PASTE-AMBER-PUBKEY)" >> ~/.ssh/authorized_keys
```
(or simplest: on Amber I run `ssh-copy-id xian@faoilean.local` while you're at the laptop to enter the password yourself once).

Agreed on the framing: #7 is a sample, not an inventory — (a)'s output is the inventory, and it's unrecoverable after retirement. — Pard
