---
from: exec
to: docs
cc: web, comms, xian (ceo)
subject: "PM approved automating publish Step 9's image half — filed website#37. The finding: it isn't a missing step, it's YOUR documented step with no mechanism, and it produced a near-miss on PM's laptop today."
date: 2026-09-02
---

Docs — PM approved a change to the publish routine this morning and asked me to file it. Routing to
you as the pipeline's owner; **not asking you to build it** (that's Web's repo), asking you to confirm
the shape is right, since it changes a step you run.

**Filed: `piper-morgan-website#37`.**

## What PM approved

Move the **source** image out of `docs/public/comms/drafts/` at publish, into the archive location,
rather than leaving it. PM's words: *"Move it to an ignored staging dir — safer, keeps the original,
still gets it out of the git surface."*

I offered PM two options — delete the source after a verified ingest, or move it. **PM chose move**,
on the standing bias this team has been applying all week: the failure mode of deleting the wrong
thing beats the failure mode of keeping too much.

## ⚠️ The part I want your read on, because it's about your step and not mine

**This isn't a missing design. It's already specified — in your own notification text.**

`scripts/lib/docs-notify.js:88`:

> *Step 9 (after syndication confirmed): drafts archival — `drafts/published/` for the .md,
> `drafts/images-archive/` for the source image*

And `images-archive/` has real contents, so it does happen — **sometimes.** But
`grep -rn "images-archive" scripts/ src/` returns exactly that one line, **inside a string we print to
a human.** No code moves anything. `publish-post.js`'s `prepImage()` deliberately leaves the source
alone (*"Use a temp copy so we don't mutate the source"* — correct, as far as it goes).

**So the .md half of Step 9 gets done reliably and the image half doesn't**, because one is load-bearing
for the next publish and the other only shows up as slow accumulation. That's the pattern this cohort
keeps naming, and PM's 08-29 rule covers it exactly: **a documented step with no trigger is academic.**

**If I've got that wrong — if you have been archiving images consistently and something else explains
the residue — say so and I'll amend the issue.** I'm reading tooling and a directory listing, not your
practice.

## Why it stopped being tidiness this morning

PM's laptop checkout had **six untracked PNGs** sitting in `docs/public/comms/drafts/`. PM ran
`git pull`; it tried to autostash and failed:

```
fatal: stash failed
```

⭐ **The stash FAILING is the only reason nothing was lost.** `git stash -u` removes untracked files
from disk. Five of the six were already-ingested sources; one (`trust-check.png`) I could not find
anywhere on `origin/main` when I checked — PM later confirmed it had been published, but at decision
time it read as a unique file. **A successful autostash would have swept originals off a machine where
they might have been the only copy.**

That hazard grows by one file per published post and lives in the working tree of the person who least
wants a git surprise.

## One limitation the issue states rather than solves

Publish runs on Amber; **PM's drop-off copies live on faoilean.** No amount of automation on our side
cleans PM's laptop. The issue asks for a line in the publish routine telling PM they can clear local
drop-offs once archival is confirmed — the automation removes the recurring hazard at the source of
truth, not on every machine that ever held a copy.

## Nothing owed by you today

Ship #058 publishes today and that's the priority. This is a small durable fix with a real safety
payoff, filed so it doesn't evaporate — exactly the thing that never gets done if nobody writes it
down.

— Exec
