---
type: methodology
title: An Alarm Needs a Reader
valid_from: "2026-10-31"
last_updated: "2026-10-31"
---

# An Alarm Needs a Reader

**Status**: Emerging. Five instances over three months, from four roles' lanes. Graduation conditions are below.
**Filed**: 2026-10-31 by CIO. **Origin**: #1967's leftover, which HOST named twice before CIO answered.
**Companions**: [[methodology-44]] (a clear is not a measurement; this is the alarm-side twin) ·
[[methodology-36]] (mechanisms over vigilance) · [[methodology-53]] (chokepoint vs bolt-on)

## The rule

**A detector isn't finished until its output has a named reader, at a named time, through a named step.
Write all three in the same commit as the detector. A flag that nobody reads works the same as no flag.**

The test, before you call a check done: *if this fires tonight, who sees it tomorrow, and which step of
theirs shows it to them?* If the answer is "whoever happens to run it" or "the log", the check is a log.

## How this differs from methodology-44

m-44 is about the *clear*: an all-clear looks the same whether the check measured something or never ran.
This entry is about the *alarm*. The check ran, measured correctly and said so, and the finding went
nowhere. The fault is in delivery, not measurement, so making the detector more accurate doesn't help.
Each instance below had a detector that was right.

## The instances

1. **Main CI red for 8.5 hours (#1892, 09-24).** Lint was red across about 35 pushes from 7 seats. The red
   was on GitHub for anyone who looked, and nobody's routine step looked. Fix: duty-cycle-tick Step 1e
   (`main-ci-status.sh` at every START). A second instance in the same class followed on 10-05:
   Architecture Enforcement was red for 41 runs because Step 1e then read one workflow only.
2. **A red workflow nobody watched (#1449, #1457).** `windows-clone-test` was correct: it failed at
   checkout because of `dev/2025/11/10/3.`. `ci.yml` was then red for 100+ runs, and "red is normal" meant
   nobody read it. The file broke every Windows clone for four months. Fix (10-31): the check moved into
   `lint.yml`, which is green and read at START.
3. **Generated issues nobody polled (HOST Step 1a, 08-07).** A workflow opened `role-health-check` issues
   every four weeks. The issue's own template said HOST's duty cycle polls for them, but nothing did, for
   over two months. Fix: one line in HOST's fire.
4. **A scanner nobody ran (#1967, 10-31).** `owed-scan.py` was built on 10-09 and correctly reported
   Exec's trailing-tag markers as UNPARSED, 66 in 14 days. It had no scheduled caller, so its output
   reached no one. The skill also told seats to write `]:`, a rule whose only enforcement was that unread
   scan. HOST asked where the scan should run on 10-29, and CIO, its owner, didn't answer until HOST named
   it again on 10-31. Fix: each seat runs `owed-scan.py --role <slug>` at START (duty-cycle-tick v1.61).
5. **A warning printed on every green run (link checker, 10-31).** The ratchet prints
   `::warning:: broken links 60 are BELOW ceiling 63 — lower CEILING` on each green run. Annotations on a
   green run are read by no one's routine. The cost showed up the same morning: 3 links of headroom let
   network weather turn main red. That's not this entry's fault, but nobody had acted on the warning that
   pointed at the headroom.

## What to do

1. **When you build a detector, name its reader in the same commit.** Use a role, a step, and the moment it
   runs: "every seat's START (Step 1e)", "Exec's rollup build". "Agents can run it" names no one.
2. **Put the output where the reader already looks.** A START step, a gate that blocks a merge, a rollup
   xian reads. A new place to look is a new habit, and m-36 says habits decay.
3. **A warning on a green run needs an owner or a fail.** Either someone's step reads it, or it should fail
   the run, or it should be removed. A warning that is printed forever and never acted on teaches readers
   to skip the annotations, the real ones included.
4. **Ask after a silent stretch.** When a detector you own has produced no visible effect for a while,
   check whether that's because nothing happened or because nothing read it. This is m-44's question,
   pointed at your own alarms.

## Graduation

Proven when a sixth instance is caught *before* it costs anything: a reviewer or the author asks the
reader question at build time and names the reader in the commit. Until then this records the failure,
not a working practice. Review at the 12-09 methodology audit.
