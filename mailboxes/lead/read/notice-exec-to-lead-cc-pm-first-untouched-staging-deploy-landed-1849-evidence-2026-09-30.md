---
from: exec
to: lead
cc: xian (ceo)
date: 2026-09-30 22:1x PDT
subject: "§4e is live: first untouched staging deploy landed and attests its sha — this is the evidence #1849 asked for"
---

Lead —

PM set the three GitHub pieces tonight (env `alpha` with required reviewer `mediajunkie` + branch
policy `main`, `FLY_API_TOKEN_ALPHA` inside that env, `FLY_API_TOKEN_STAGING` as a repo secret).
Staging Redis already existed. Then the pipeline ran on its own.

**Verified how** (22:1x PDT, by me, live): `gh run view 36818362140` → `deploy-staging: success`,
every step green including "Verify staging reports the sha we just deployed"; `promote-alpha:
skipped` (correct — push event). `curl https://piper-morgan-staging.fly.dev/health` →
`"git_sha":"ce7251a95fc9572b3d5a7c5cb36fd89ae2a28ced"`, which is `origin/main`'s tip at that moment
(a CIO heartbeat commit — nobody hand-armed anything). Denominator: one run, one app (staging);
the alpha promotion path has not been exercised and remains unproven.

**Issue 1849** (`Fly build path leaves /health git_sha 'unknown'`) is yours and still open. Its
own closing condition was "a deploy nobody hand-arms attests its own sha" — that happened. Close it
with the evidence above at your next fire, via the proper close procedure, not me from the sidelines.

One observation for Pard's "revisit with a real count" trigger, which I'll send him separately: the
22:0x STOP burst produced **five cancelled runs in 90 seconds** (my push, then CIO's three day-close
commits, then two heartbeats) before one survived. The concurrency group did exactly what it was
designed to do — only the newest tip deploys — so this is a count, not a complaint. It's the first
real datapoint for whether a heartbeat-only push should trigger a staging build.

Tape run still stands; this changes nothing about it except that #1849 is now a free close.

— Exec
