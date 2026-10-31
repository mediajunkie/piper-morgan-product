---
type: methodology
title: methodology-48 — A Proxy Count Is Not The Quantity (and at selection time it propagates)
valid_from: "2026-08-10"
last_updated: "2026-10-30"
---

# methodology-48 — A Proxy Count Is Not The Quantity (and at selection time it propagates)

**Status**: Proven (two independent instances, opposite directions, 2026-08-09→10)
**Filed**: 2026-08-10 (CIO) · **Found by**: PPM and CXO independently · **Framed by**: Arch
**Companions**: [[methodology-43]] · [[methodology-44]] · [[methodology-45]] · [[methodology-47]]

---

## The rule

**A count that is easy to obtain is not the quantity you care about, and substituting it is not a
measurement.** The commonest form here:

> ⭐ **A correction count measures ATTENTION, not FAULT.** An artifact accumulates corrections because
> someone examined it. An artifact with none may be flawless or may be unread, **and the count cannot
> tell you which.**

🔴 **The specific danger is that this operates at SELECTION time.** It decides which document becomes
canonical, which tool is trusted, which estimate is carried — **and it does so before anyone reviews the
content**, so the error propagates into everything downstream of the choice.

## The two instances

**PPM, 2026-08-09** — told their artifact should become canonical because the rival had accumulated
three corrections in a day:

> *"Mine hasn't needed three corrections. **It has never been AUDITED.** Those are not the same fact, and
> only one of them is evidence. §7a looks worse **because it was examined.** Choosing the unexamined
> artifact because the examined one accumulated corrections is **SELECTING FOR ABSENCE OF SCRUTINY**."*

**CXO, 2026-08-10** — naming the identical error from inside their own argument, in the opposite
direction:

> *"I used a correction count as a defect-density measure. **Corrections are evidence of attention, not
> of fault.**"*

**Arch's placement**: *the vacuity family applied to artifact selection.*

## The family this belongs to — each found separately, by a different role, in a different artifact

| instance | proxy used | quantity meant |
|---|---|---|
| *convergence is not importance* (CXO, 08-08) | four-lens agreement | significance |
| **corrections are not defects** (PPM/CXO, 08-09→10) | correction count | defect density |
| *an aggregate is not a per-category score* (the ratchet, 08-09) | total | per-category |
| *a total is not its parts* (sprint-truth) | sum | composition |

**Four re-derivations in three days.** That recurrence is the argument for a slot rather than a memo.

## ⚠️ A worked example from the filer's own lane, because it cuts both ways

`cohort-freeze-detect.sh` has been **corrected three times in four days** — stale-local read, crash-exit
code, and a dispatch-lag denominator. **Under this error that reads as "an unreliable tool."**

**It is equally available to read it as "the most examined tool we have,"** and *that inference is just as
unwarranted*. **The count supports neither claim.** Three corrections is genuinely a lot; it is also
exactly what you get when three colleagues run a new tool and report what they see. **The honest position
is that the count tells you about the attention, and you must look at the artifact to learn about the
artifact.**

### Second worked example, same filer, 2026-10-14: a citation count read as a status

The 10-14 methodology audit's subagent marked 7 methodology docs SILENT, because no session log in 26 weeks cited them. I wrote them up as "undecided" and promised Docs dispositions. **The disposition already existed.** B3's tracker (Arch-ratified 09-01) had ruled all 7 EFFECTIVE, and said in plain words that "citation count mispredicts effective". The count measured *attention*, as this entry's rule says, and I substituted it for the quantity I cared about, *status*, at selection time: which docs to act on. Caught before any doc changed, by reading the tracker before writing the dispositions. Corrected in the audit and by mail the same hour. **What to do, sharpened:** before acting on a count-derived verdict about an artifact, look for the artifact's own decision record. A ratified disposition outranks a proxy.

### Third and fourth worked examples, same filer, 2026-10-28/29: a signal of one act read as another

Neither is a count. Both are the same substitution: an easy signal standing in for the act you care about.

- **A canary read as "this seat reads its mail" (10-28).** `mail4.py check` said no canary from Exec since 10-23 or from Lead since 10-22. I mailed both that they hadn't read their v4 inbox in 5 to 6 days. Both had. The canary fires on one command, `mail4.py inbox`. Exec reads and acks each message with `read ID` and `ack ID`, which never runs `inbox`. The signal measured *which command ran*; I read it as *whether mail was read*. Fix: `check` now prints each seat's last non-canary ack beside a missing canary (`scripts/mail4.py`, `mail-v4-pilot.md`).
- **An exit code read as "this command exists" (10-29).** To check whether flyctl 0.5.0 renamed any of the 75 gated commands, the obvious test is `fly <path> --help` and its exit code. A control run showed `fly apps zzznotreal --help` exits 0, printing the parent's help. Every path would have "passed". The usage line in the help text is what names the command; comparing that found 73 of 75, plus 2 deprecated ones.

**What to do, sharpened:** before trusting a signal, run it once against a case you know is negative (a nonsense path, a seat you know is reading). If the negative case also passes, the signal measures something else.

### Fifth to eighth worked examples, one day (2026-10-30): the check measured a neighbour of the question

Four in one day, three of them the filer's own. Each check was real and ran clean; each answered a question next to the one asked.

- **"Not on PATH" read as "not installed" (CIO).** I told xian pytest and ruff weren't on Amber and shipped unlinted. `scripts/ensure-pytest-env.sh` and `scripts/ensure-ruff.sh`, one of them mine, print cached copies; `whats-armed` lists both. The question was "can this host run the tools", and `which` answers "is it on PATH".
- **Retry attempts counted, output never read (CIO, caught by Pard).** I checked that `curl --retry-all-errors` retries a DNS failure: three attempts, so it passed. Pard then looked at the output file. With `> file`, every attempt's body is appended, so a 502 then a 200 leaves two JSON documents that won't parse. The question was "does a retried mint produce a usable token".
- **"Untracked and not ignored" read as "what the upload carries" (CIO, found by PA, #2240).** My 10-13 `deploy-mcp.sh` refused stray files with `git ls-files --others --exclude-standard`. A gitignored operator `config/PIPER.user.md` passes that check and still ships, because `fly deploy` uploads the working tree.
- **A test that reads the script instead of running it (the #2240 fix, caught by PA).** The fix's pins checked `.dockerignore` and the script's text. The script itself exited 1, silently, on every clean tree (`grep` no-match under `pipefail`). PA's dry run on a clean tree found it. Lead's replacement pin (`fcac831ae6`) lifts the guard line out of the script and runs it under `pipefail`, once on a clean tree and once with an overlay, and Lead checked it fails on the old line. Lead's own words for the shape: "I keep trusting what reads green instead of what exits green."

**What to do, sharpened again:** name the question in words before you pick the check. Then ask what the check would say in the case you're worried about: the gitignored file, the retried success, the clean tree. If you can't run that case, the check hasn't answered the question yet.

## What to do

1. **When a count is about to decide something, ask what it is a proxy FOR** — and whether the thing you
   want is measurable at all from what you have.
2. **At selection time especially, prefer reading the artifact to ranking the artifacts.** The proxy is
   attractive precisely when reading is expensive, which is when the stakes of choosing wrong are highest.
3. **A clean record is not evidence until you know it was examined.** *(Same shape as [[methodology-44]]:
   an all-clear is emitted identically whether it measured or never ran.)*
4. **Do not invert it either.** "Heavily corrected therefore well-tested" is the same error wearing the
   opposite sign.

## Provenance note, which is part of the finding

**PPM assembled this and routed it rather than endorsing it**, writing:

> ⚠️ *"Three of us now agree it should exist and none of us has filed it. That's the shape where a good
> finding dies of mutual endorsement."*

And neither finder claims novelty: *"both instances were found because someone else supplied the method —
CXO handed me the audit, I handed them the counting question. **Neither of us got there alone**, which is
itself the argument for writing it down where the next person doesn't need a partner to see it."*
