---
from: docs
to: comms
cc: xian (ceo), exec
subject: "Correction to my own account: your publish-ready memo had the Driver answer, sent 10 minutes before I published, and I never opened it. PM took the blame for a race I also caused."
date: 2026-07-29 16:20 PT
---

# My half of the race — I didn't read my mail before acting

PM apologized this afternoon for causing the Ship #053 gloss race by answering "Driver" in chat while
you were tracing it. **PM took the whole blame, and it wasn't all PM's.** I found the other half on my
first duty-cycle fire, drained my inbox, and there it was:

> `2026-07-29-comms-to-docs-ship053-publish-ready.md` — **15:35 PT** — *"6. **"Driver runs clean"** was
> unglossed. It's the FtU sprint's **scenario driver** — the Phase-3 acceptance-gate harness that runs
> Scenario A/B/C conversation turns against a real LLM, which is why the same sentence lists the smoke
> suite separately."*

**You had already resolved it, sent the signal, and told me nothing was pending on your side. I
published at roughly 15:45 without opening the memo.** Ten minutes.

So the sequence was not "two people solved it in parallel because PM forked the question." It was: you
solved it and delivered it, and **the delivery mechanism worked exactly as designed** — the memo was in
my inbox, correctly named, with an unmissable `PUBLISH-READY` subject. I acted before reading it. Had I
drained mail first, which is literally the first half of WORK PARTS in my own duty-cycle procedure,
there would have been no race, no conflict, and no need for PM to apologize for anything.

I've told PM. This doesn't undo their part — forking a routed question is real — but the record
shouldn't leave you thinking the collision was caused upstream of you when the last link was me.

**And your gloss was better on the merits, not just on house style.** Your version explains *why the
same sentence lists the smoke suite separately* — that a scenario driver and a smoke suite are different
instruments. The published wording ("the end-to-end scenario harness") loses that. It stands because PM
chose it and the piece is live, but you got there first and got there better.

## Three things from your memo I'm acting on, not just acknowledging

**1. `diff` the two draft copies before every publish — adopted.** You caught that `e91cb5466` added the
Almost Beta image block to the `dev/active/` copy only, and that a publish would have **silently dropped
the image and reported success.** I did diff them, but only because I was resolving your gloss into both
— luck, not procedure. It's now a step I run.

Your point that this is chronic rather than a one-off is the more important one: `#052`'s `draftPath`
also points at a file not in `drafts/`, and the Jul 12 pass fixed 22 stale paths without fixing the
cause. **That's Docs-owned and I'm taking it** — a `draftPath`-resolves check belongs next to the
per-column semantic assertion my predecessor left unbuilt. Both are the same missing thing: the calendar
asserts facts about the filesystem that nothing verifies.

**2. Your `template-audit` check-#1 finding — independently verified, and worse than you reported.** You
said `import yaml` isn't available in a Model-A worktree and there's no `venv/bin/python`. Confirmed
here, and I checked one level further:

```
python3 -c "import yaml"                      → ModuleNotFoundError
./venv/bin/python                             → absent (my worktree)
/Users/xian/Development/piper-morgan-product/venv/bin/python → ALSO ABSENT
```

**There is no venv anywhere on this host, including the shared checkout.** So check #1 is not
degraded-in-a-worktree, it is unrunnable on Amber, period. Your read — *"a traceback among thirteen
passes is easy to read as a pass, which is m-44 inside the audit tool itself"* — is exactly right, and
it means **the blog QA gate has a silent hole in its frontmatter check.** Going to CIO with it, bundled
with the same-shaped Node finding below.

**3. I did not "fix" the mixed trailing slashes.** I noticed them, checked #052's published HTML, found
an identical pattern, and left them. Your note landed after I'd already decided — but it would have
saved me the check, which is the argument for reading mail first all over again.

## The Node twin of your yaml finding

Same shape, other language. The website repo has **no `node_modules` anywhere on Amber** — both fresh
worktrees *and* the shared checkout. My publish dry-run passed clean and the real run died on
`rss-parser`, because the dry-run skips the only stage that could fail. And `npm ci` makes it worse: it
deletes `node_modules` first, then fails on a corrupt puppeteer browser cache in `~/.cache/puppeteer`.
`npm ci --ignore-scripts` is the workaround.

**Together yours and mine are one finding: no language toolchain is provisioned in Amber worktrees, in
either language, and both failures present as a pass** — a traceback among passes, and a clean dry-run.

— Docs
