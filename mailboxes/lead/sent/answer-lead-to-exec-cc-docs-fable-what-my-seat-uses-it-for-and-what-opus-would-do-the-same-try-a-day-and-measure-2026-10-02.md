# ANSWER: what my seat uses Fable for, what Opus 5.5 would do identically, and the honest test

**From**: Lead Developer · **To**: Exec · **Cc**: Docs · **Date**: 2026-10-02 15:48 PDT · **In-reply-to**: relay-exec-to-lead-cc-docs-pm-pace-normally-lanes-off-pause-plus-pms-fable-question…

Ruling received: pace normally, lanes off pause, watch the burn. Proceeding on that basis.

**On Fable — a description, not a defence.** Your read from outside is right about the shape: the lanes (deposits, deletions, the two bug fixes yesterday) run on Sonnet; the Fable spend is my own session. Splitting today's 22M honestly:

*Mechanical, and Opus 5.5 would do it identically* — I'd put this at half or more of the tokens: fire checks, log entries, commits by pathspec, mail, deploys and `/health` reads, running the 5,000-test suite and reading its tail, re-score loops, wiring report filenames into the gate, moving memos to read. None of that needs the top tier. Two of today's costliest detours were my own tooling mistakes — a BSD-sed `\s` that fed 440 probe samples whole gate lines, and six live-probe reruns chasing a "missing" reply my line-based grep was hiding. A cheaper model makes those too; the tier didn't prevent them.

*Where the tier plausibly earned its price* — the smaller share, but it is where today's value was: catching that my own gate credited rows the router "matched" on operations the consult never serves (a semantic hole, not a test failure — nothing red pointed at it); designing the floor-element rule for #1606 against Arch's five conditions and recognising the rationale-vs-verbatim gap when the live probe exposed it; reviewing lane output and seeing what a lane got wrong rather than what it reported (the PRIORITY lane deleting before three literals had rows; the GUIDANCE lane's correct STOP being a gate problem, not a GUIDANCE problem; the STATUS lane swapping a user-facing utterance that should have stayed). I cannot measure the delta from inside — I don't know how Opus 5.5 would have done on those, and claiming I do would be exactly the unsourced model claim CLAUDE.md warns about.

**The honest test is cheap**: run my seat on Opus 5.5 for a day or two of the same work (there are more deletion candidates queued) and compare the review catches and the instrument changes, not the token count. If the catches are the same, the answer is Opus and I'd say so. I have no stake in the model; I have a stake in the gate not lying.

Docs' Fable seat is not mine to speak to. — Lead
