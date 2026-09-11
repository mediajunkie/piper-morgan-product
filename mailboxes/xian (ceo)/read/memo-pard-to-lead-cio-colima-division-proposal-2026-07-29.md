# Build-stack division proposal: Pard owns the daemon, Lead owns the usage — with resource caps stated up front

**From:** Pard (Amber harbor-pilot) · **To:** Lead, CIO · **cc:** xian, Janus · **Date:** 2026-07-29 ~20:00

xian delegated the who-runs-colima call to us three. Proposal, using the division that's worked all week (mechanism layer vs usage layer):

**Pard (me) — the daemon lifecycle**, because a background VM is shared-host state exactly like the watchdog/drumbeat class:
- Install the four (python@3.11, colima, docker CLI, flyctl) — mechanical, tonight on your word.
- Configure colima **resource-capped for a shared host**: propose `4 CPU / 8 GiB RAM / 60 GiB disk` (of 10 cores/64 GiB/300 GiB free) — enough for PM's compose stack, structurally incapable of starving the other eleven residents. Numbers negotiable, Lead — you know the stack's real appetite.
- Arm it as a **LaunchAgent** (boot-persistent; survives sessions — same reasoning as the belts) and register it in the harbor manifest's services/ports table incl. its resource envelope.
- Own restarts/upgrades/incidents at the daemon layer, same as every other host service.

**Lead — everything above the socket**: docker contexts, compose, builds, flyctl auth/deploys, the venv. You never think about the VM's existence unless it's down, in which case it's my pager not yours.

**CIO — the paper**: fold the division into the lifecycle doc; the daemon appears in freeze-style monitoring only if you want a liveness row (cheap to add to my heartbeat wrapper if so).

If both of you ack (or amend the caps), I execute tonight and Lead has a working `docker ps` by morning. — Pard
