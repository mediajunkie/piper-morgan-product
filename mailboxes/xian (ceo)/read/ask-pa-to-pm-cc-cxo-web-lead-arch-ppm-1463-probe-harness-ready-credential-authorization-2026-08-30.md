---
from: pa
to: xian (ceo)
cc: cxo, web, lead, arch, ppm
subject: "#1463 probe: harness built and ready — need your go-ahead to spend real API credential (~28 calls, 2 vendors)"
date: 2026-08-30
---

PM — CXO asked me (or Web) to run the #1463 recomposition probe, since CXO structurally can't be
both subject and scorer. Did the prep work rather than either running it unilaterally or sitting
idle waiting on you: built the harness, checked the blocker, found one thing worth flagging before
you say go.

## What's ready

`dev/active/probes/probe_b_recomposition_2026-08-30.py` — adapted from July's Probe A harness,
matching CXO's packet exactly: 6 corpus items × prose/structured variants (12 trials) + 2 negative-
control trials = **14 trials per vendor, 28 total across Claude + GPT**. Compiles clean, not yet run.

## What changed since Probe A's original blocker

Checked rather than assumed: **both Anthropic and OpenAI keys are now present in the Keychain** (via
`KeychainService`, verified live just now). Probe A's August blocker — no credential available at
all — no longer applies. This is a real, cost-bearing external API call, not a free check.

## Why I'm asking rather than just running it

My own carry-forward has carried this note since Probe A: *"it needs API spend against your
credential — your 'yes you may' was scoped to Probe A, so I'm not extending it silently."* This is a
different, newer packet (CXO's design, not mine), so I'm treating it the same way — a precise ask,
not a silent extension of old authorization, per the standing lesson from Probe A's own history
(*"an agent that reaches into a keychain to unblock itself is a worse failure than a probe that
waits"*).

## One thing to flag before this runs, not after

The packet specifies a negative control using bare, unhedged payloads for items 1 and 6. Item 1's
form is unambiguous (`{"todos": []}`). Item 6's isn't spelled out verbatim — I interpreted it as a
confident success claim (`{"action_performed": true}`), reasoning that a negative control's job is
to confirm the harness doesn't over-hedge a genuinely unhedged payload either. **Flagged in the
script's own comments** for CXO to confirm or correct before this is treated as final — didn't want
to silently guess on a probe whose whole point is that guessed interpretations don't count.

## The ask

Say go and I'll run all 28 calls, score against the rubric's T axis, and report with the
denominator CXO's packet asks for (N items × M vendors × 2 variants = K trials, H fabrications).
**No deadline from CXO's own packet** — this sits ready whenever you have a moment, not urgent
today.

— PA
