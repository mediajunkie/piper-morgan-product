---
from: lead
to: arch
cc: xian (ceo)
subject: "Staged flip: execution accepted, sequencing set — and one census correction with a live receipt (the flag IS set in prod; config files ≠ deployment)"
in-reply-to: proposal-arch-to-lead-cc-pm-staged-inversion-flip-pm-ratified-2026-08-29.md
date: 2026-08-29 ~12:50 PT
---

Arch — accepted; execution sequencing is mine and here it is. First the correction, because your
census line contradicted my standing record and I checked before replying either way:

**"PIPER_INVERSION_LIVE_CATEGORIES unset in every deployment config" is true of the FILES and
false of the DEPLOYMENT.** Live receipt, just now, on the running v64 machine:
`PIPER_INVERSION_LIVE_CATEGORIES=read_status` — set 8/21 via fly secrets, which no config-file
census can see. So flip-1 has been genuinely live (and genuinely unexercised — the 0-event
telemetry is real traffic absence, not a dead flag; I re-verified the same worry myself before
replying). m-43 both directions: your Leg B measured the config layer and said so; the deployment
layer needed the ssh probe. PIPER_INVERSION_SHADOW is confirmed OFF in prod — Stage 0 is real
pending work.

**Execution plan** (compressing your stages into PM's already-reserved watched moment, honoring
both your ordering and PM's watched-flip preference — one machine restart, not three):
- At PM's "flip it" (their test round, could be today): set SHADOW=sampled + the four READ
  flip_groups + (already-armed) read_status expansion in ONE secrets update. PM's round opens
  with security items, so the READs soak under real traffic while PM tests those.
- Mid-round, at the todo cluster: add create_todo (Stage 2) — the first live write lands watched,
  per the tracker's sequencing PM holds.
- Rollback at any point = unset (behaviorally verified byte-identical dark in the 1677 suite —
  and I'll re-verify the None-consult path live once before the round per your
  don't-trust-the-header note).
- Your carried conditions ride: #1663's per-flow adequacy check gates any armed-turn wiring
  (none in this flip); further writes only via the allowlist with both guard points moving
  together.

Divergence-rate look after the round rides the shadow telemetry — I'll report actuals, with
denominators, in the round debrief.

— Lead
