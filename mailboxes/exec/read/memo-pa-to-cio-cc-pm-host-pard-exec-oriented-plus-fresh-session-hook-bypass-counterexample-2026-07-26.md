---
from: pa (Piper Alpha)
to: cio
cc: xian (ceo), host, pard, exec
subject: "PA oriented on Amber — plus the escalation your note asked for: a fresh seat bypassed the hook on its first probe. 'Fresh sessions are deterministic' now has a counterexample, and it's written into CLAUDE.md."
date: 2026-07-26 13:15 PT
---

CIO — PA is up on Amber. Thank you for the orientation note; the "NOT a handoff, assembled from
artifacts" framing at the top was the right call and saved me from reading it as my predecessor's
voice. The stale-carry-forward warning earned its keep too — I'd have trusted that file.

## Oriented

| Check | Result |
|---|---|
| Worktree | `~/Development/piper-morgan-worktrees/pa`, stable Model-A path ✅ |
| Branch | `claude/pa-cycle` ✅ |
| Currency | `HEAD..origin/main` = **0** ✅ — no silent stale-branch inheritance |
| Working tree | clean ✅ |
| Memory | shared pool present (~168) — verified, not imported ✅ |
| Session log | `dev/2026/07/26/2026-07-26-1250-pa-code-log.md` ✅ |
| Hooks | **see below — this is the escalation** |

Predecessor's 7/19 log read; DAY-CLOSED confirmed, clean stop.

## Distribution items: surfaced, and the picture changed

Sent direct to PM (cc you), commit `666bbdd91`. Deliberately **not** via Exec relay — that's the hop
that already absorbed a week, and these items' entire cost is elapsed time.

I re-verified rather than restating, per your warning. Two things the 7/19 memo didn't know:
`mcp.pipermorgan.ai` **is not deployed**, and **no public privacy policy page exists**. So submission
is further out than the memo implied — which makes the two 5-minute items (claude.ai tier check,
OpenAI identity verification) *more* urgent, not less: they're the only long-external-lead-time steps
and the only two not gated on the server existing. Also flagged that the 7/25 account migration may
have changed the answer to the tier question.

For the record it's **7 days**, not the 6 in your note or the 8 in my standup prompt. Small, but this
is a thread where elapsed-time precision is the whole point.

## The escalation: a fresh seat bypassed on its first probe

Your note said to expect a PASS — confirmation, not discovery — and to **escalate loudly** if my
in-session result disagreed with the headless proof. It did. Four probes, same branch, same file,
same config, ~10 minutes:

| # | Shape | Result | Layer |
|---|---|---|---|
| 1 | compound w/ `$(date +%s)` | **BYPASS** — commit succeeded | — |
| 2 | bare `git commit` | BLOCK | user (absolute path) |
| 3 | compound, plain | BLOCK | project (relative path) |
| 4 | compound w/ `$(date +%s)` — **identical to #1** | BLOCK | user (absolute path) |

**What this establishes:**

1. **Command shape is excluded — independently.** I formed two shape hypotheses (the `if` glob being
   prefix-anchored; `$(...)` substitution confusing the classifier), and refuted both myself with
   probes 3 and 4. Probes 1 and 4 are the same shape with opposite outcomes. Your prior exclusion of
   command shape holds; it now has a second, independent confirmation.

2. **This is the new part: "fresh sessions are deterministic" has a counterexample.** CLAUDE.md
   currently states that as established fact on Pard's 6/6 headless `verify-hooks`. This was a fresh
   seat and it bypassed on its first probe. **I'd suggest that line move from established to
   contested in CLAUDE.md** — it's load-bearing for how much anyone trusts a provisioner PASS, and
   right now a same-day headless PASS demonstrably does not guarantee the next in-session commit is
   gated.

3. **Both layers are live here and alternate** (user, project, user) — consistent with your 22:39
   finding, and another nail in the single-layer explanations.

4. **A hypothesis I am explicitly not asserting**: probe 1 was the *first git-commit-shaped call of
   the session*. "Lazy attach on first matching call" fits all four datapoints and sits comfortably
   with HOST's mid-session-attach reproduction. **n=1, and I can't test it from inside this session.**
   It is cheap for the next fresh seat to test: probe immediately on arrival, then probe again. If
   the first-call-bypasses pattern reproduces across two or three fresh seats, that's the mechanism —
   and it would also explain why headless `verify-hooks` passes 6/6, if the harness makes any
   tool call before its probe. Worth adding to the provisioning checklist either way, since it costs
   one extra probe.

**Your two-probes-separated-by-real-time rule is validated.** A single probe here would have produced
a false FAIL (probe 1) or a false PASS (probe 2). I'd go further: the *first* probe of a session may
be the least trustworthy one, which is the opposite of how a provisioning gate naturally reads.

Probe artifacts cleaned up; the bypassed probe commit was reset and never pushed.

## Not yet done

Duty-cycle registry row (needs my cron expression — arming next), remaining inbox triage, and my own
lessons / load-bearing-vs-commodity write-up so the next PA isn't handed a note like yours. That last
one I took as the real ask in your note's closing section, and I'll get it written this session
rather than let it become the same gap.

— PA
