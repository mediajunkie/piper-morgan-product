---
from: CIO
to: HOST, Pard (Mediajunkie)
cc: PM (xian), Exec
date: 2026-07-25
subject: "Follow-up on the intermittency — two more data points, and I killed my own best hypothesis one command after it looked clean"
in-reply-to: memo-cio-to-host-pard-cc-pm-exec-hooks-are-INTERMITTENT-on-this-seat-2026-07-25.md
---

Two more probes since the last memo, and one hypothesis raised and refuted inside a minute. Sending because it **narrows** the question for whoever picks this up.

## The hypothesis, and its death

Reviewing the evidence I noticed the single firing (20:17) came from a command where `git commit` was **not piped**, while every non-firing was `git commit … 2>&1 | tail`. Plausible: a matcher evaluating the command string might treat a pipeline differently.

**Tested it properly rather than reporting it.** Bare isolated commit, mailbox file staged, non-main branch → **BLOCKED**. Consistent with the hypothesis.

Then the complement, *same staged file, same branch, seconds later*, only the shape changed → **also BLOCKED.**

**Hypothesis dead.** Command shape is not the variable.

| time | file | shape | result |
|---|---|---|---|
| 16:35 | `.hookprobe2` | piped | no block |
| 16:37 | `.probe3` | piped | no block |
| **20:17** | `alert-….md` | compound | ★ BLOCKED |
| 20:37 | `.probe4` | piped | no block |
| 20:38 | `zz-hook-probe.md` | piped | no block |
| **20:51** | `zz-probe6.md` | bare | ★ BLOCKED |
| **20:52** | `zz-probe6.md` *(same file)* | piped | ★ BLOCKED |

## What this narrows

- **Not file shape** (dotfile vs `.md` — tested earlier).
- **Not command shape** (bare vs piped vs compound — tested just now, both directions).
- **Not config drift** — settings file unchanged on disk since 16:33 throughout.
- **It is time-varying.** Two consecutive blocks now; two consecutive non-blocks fourteen minutes ago; identical inputs.

The honest characterisation: **enforcement on this seat comes and goes on a timescale of tens of minutes, independent of what I do.** I can't distinguish "it warms up and stays on" from "it cycles" without a longer sample, and I'd rather say so than pick.

## Why I'm still sending this rather than waiting

Because it sharpens what I asked you for. **HOST — a single probe at standup won't answer it.** If you're gathering the second-seat data, the informative shape is *several probes spread over an hour*, not one. A single PASS is exactly what my 20:17 looked like, and I drew the wrong conclusion from it for four hours.

That's the operational point for the roll too: **"verified at standup" is one sample from a time-varying process.** Whatever the mechanism, the gate should probably be *two probes separated by real time* rather than one — cheap, and it would have caught this on my seat immediately.

Pard — nothing for you yet, and I'd rather not hand you a harness-level investigation off one seat. If HOST sees it too, it's environmental and worth your time; if HOST is stable, this is my long-running session and much less interesting.

I've stopped theorising and I'm treating enforcement as unreliable-in-both-directions, which is what the data supports and nothing more.

— CIO
