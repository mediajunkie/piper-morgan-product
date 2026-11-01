---
type: concept
title: Alpha liveness, the watch and the restarter (#2085)
last_updated: "2026-11-01"
owner: HOST (the watch), Arch (the restarter's guards), xian (approves each restart)
---

# Alpha liveness: the watch and the restarter (#2085)

This is the concept doc for two mechanisms. It says why they exist and what they must do, so each can
be checked against it (methodology-56). Each workflow's header holds the detail; this page holds the
reasons.

- `.github/workflows/alpha-health-watch.yml`: the watch (#2085 track 2, #2101).
- `.github/workflows/restart-alpha-postgres.yml`: the restarter (#2085 track 1). It runs from the
  `ops/restarter` branch, which a ruleset protects. The copy on main is the readable one.

## Why they exist

In October 2026, alpha went down twice in three days. Each time the kernel killed Postgres inside the
one `piper-morgan-db` machine, but the machine stayed `started`. Fly restarts a machine when it exits,
and Fly's Postgres image lets Postgres die without the machine exiting, so nothing restarted it. Both
outages were found by a person who happened to look, and each waited for someone at a terminal.
Two gaps came from that:

1. **No one is told when no seat is awake.** Seats' checks run only when seats run. Alpha needs an alarm
   with a reader outside the cohort (methodology-57: an alarm needs a reader).
2. **The cure needs a person at a terminal.** A restart should be one approval, not a session.

## What the watch must do

- Probe alpha's `/health` about once a minute. Alert on a stall of about three minutes, and stay quiet
  on a single missed probe.
- A probe misses on no 200 within 10 seconds, or on `"status":"degraded"` (the app is up and its
  database check failed, #2083).
- **Reach a person through two channels.** These are GitHub's failure email (xian's notification
  settings decide who gets it) and one reused issue, "Alpha health watch: failing", assigned to the repo
  owner. The issue sends mail through a second channel and is visible on the repo whatever the mail
  does.
- **Its acceptance test is the reader, not the probe.** A forced-failure dispatch has to produce the
  email and the issue comment.

Known limit: a stall that starts and ends between two runs (GitHub's five-minute floor plus its delay)
is missed.

## What the restarter must do

The restarter is dispatched by a seat on an open watch alert. GitHub then asks xian to approve the
`alpha-db` environment, and the run log is the record. Before its one restart it checks three guards
(Arch, 10-21):

1. **Only for the database's own fault.** Alpha's `/health` must read the database as not healthy, and
   the Postgres machine's own `pg` check must read failing. A healthy but unreachable database isn't
   cured by a restart.
2. **One restart, then a person.** It refuses if any run restarted the machine in the last 30 minutes.
   A restart that doesn't cure the fault fails its run, so the failure reaches a person instead of
   looping.
3. **Capture first.** Machine state, events and the last Postgres log lines go into the run log
   before the restart erases them.

Custody (HOST, 10-21): the token is the environment secret `FLY_API_TOKEN_ALPHA_DB`, scoped to
`piper-morgan-db`. The capture filters out anything that looks like a credential or an environment
value. After the restart, the job polls `/health` for three minutes. Either way, it comments the run
URL on the watch's open issue.

## How to check them against this page

- **The watch:** a forced-failure dispatch delivers both the email and the issue comment.
- **The restarter:** its run log shows the three guards in order before any restart. Its history shows
  no second restart within 30 minutes.

Neither is tested by reading its YAML.
