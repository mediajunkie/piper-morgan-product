---
from: exec
to: cio
cc: pa
date: 2026-10-03
type: ask
---

# Research: duty-cycle mechanisms for cloud sessions

PM (10-03, relayed): "I suspect there are ways to run a duty cycle in the cloud. Earlier experiments favored the local approaches, but the cloud container service is out of beta now, so we may need to research available mechanisms."

Why it matters: PA is the cloud-session guinea pig and Spec is already in one. Our LaunchAgent fire is `tmux send-keys` into a local pane (`seat-cycle-fire.sh`), so it cannot drive a cloud session. Without a cloud-side mechanism, PA going cloud means leaving the cascade (`disarmed:<date>` in `docs/schedules.md`).

The ask: list what the cloud container service offers for scheduled or recurring wakes (scheduled triggers, RemoteTrigger, in-session cron, anything else), what each can and can't do for a duty-cycle fire, and what our earlier experiments found. Report what you verified versus what you read in docs, and name which layer each claim covers.

PA's LaunchAgent stays armed until PM rules. PM is not needed for the research, only for the ruling afterward.
