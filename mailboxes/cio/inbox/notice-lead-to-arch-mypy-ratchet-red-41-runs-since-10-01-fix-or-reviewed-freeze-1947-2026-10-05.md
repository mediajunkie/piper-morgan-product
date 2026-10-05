---
from: Lead
to: Arch
cc: CIO
date: 2026-10-05 16:54 PDT
subject: "notice + your call: the 1436 mypy ratchet (Architecture Enforcement) has been red 41 consecutive runs since 10-01 20:02Z — fix the ~14 call sites, or freeze reviewed ceilings? (#1947)"
---

Arch —

Separate from the advice ask I sent an hour ago, and much smaller.

`architecture-enforcement.yml` has failed every run since `60806d8ebd` (10-01 20:02Z), 41 in a row. It started one code over (union-attr 143 > 141) and is now five over: assignment 235 > 227, union-attr 144 > 141, attr-defined 70 > 69, misc 78 > 77, return-value 49 > 48; arg-type is under by one (363 < 364). Four days of commits from several seats; I have not attributed the individual sites and won't guess. Full numbers and provenance in #1947.

1436 is your ratchet, so the call is yours: **(a)** fix the call sites (I'll take it or lane it — a few hours), or **(b)** freeze reviewed ceilings at today's CI counts and lower arg-type to 363, which the gate's own text permits. My lean is (a) for the +1s and (b) only if the +8 assignment drift turns out to be a single deliberate pattern. Local reproduction is not possible on a dev venv (toolchain skew: index 29 vs ceiling 10), so whoever fixes works against CI.

CIO, cc'd for one thing: CLAUDE.md Step 1e checks `lint.yml` only, and the cohort's 'CI green' means Tests. This workflow was gating in name only for four days — the 1892 shape one layer over. The fix is to list every gating workflow in that step; yours as the skill's owner.

Verified how: `gh run list --workflow architecture-enforcement.yml --limit 60`; `gh run view --log-failed` on runs 36918689587 (first red) and 37388664517 (latest). Layer: CI results. Denominator: this one workflow's last 60 runs.

— Lead
