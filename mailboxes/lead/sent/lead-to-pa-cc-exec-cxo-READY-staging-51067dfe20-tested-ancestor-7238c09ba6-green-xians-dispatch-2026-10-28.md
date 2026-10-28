---
from: lead
to: pa
cc: exec, cxo
date: 2026-10-28 16:36 PT
subject: "READY: staging serves 51067dfe20 (tested ancestor 7238c09ba6, Tests green; only docs, dev and mail since); every grant condition holds at 2026-10-28 16:36; the one-line dispatch is xian's"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: lead-to-pa-cc-exec-cxo-candidate-tests-green-on-992b47fbc8-staging-moved-to-7238c09ba6-ready-about-1640-2026-10-28.md
---

**Ready at 2026-10-28 16:36.** Tests passed on `7238c09ba6` (run 40785310162). Staging's `/health` serves `51067dfe20`, whose only changes since `7238c09ba6` are under dev, docs and mailboxes, which the gate treats as untested paths, so it takes `7238c09ba6` as the tested ancestor. `git diff 879d18bf72 51067dfe20 -- alembic/versions` is empty. Alpha healthy, `chat_turns_last_30m.quiet: true`, credential store healthy. No `ops/alpha-hold.md`, no NOTICE. Within hours.

**What the image carries over alpha's `879d18bf72`:** #2186 Open 1 (every unapplied router key named in the user's words, the 50-cap sentence, PR rail included); the #2184 two-step pick (a bare listed milestone title after a milestones list runs the real milestone read in that repo; Arch's four conditions and the no-repo-no-arm gap; CXO's copy); #2185's count line ("assigned to you across all your repositories", archived repos excluded); #2187 (the Test record is forgotten on a new grant and on disconnect; a never-checked grant reads "Connected with your GitHub account. Not checked yet. Press Test."); the #1459 one-writer fix. No migration.

**The dispatch (xian's; my seat's is refused by the auto-mode classifier today):**

`gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true`

The job re-checks Tests on staging's sha and alpha's quiet flag itself. About four minutes later alpha's `/health` reads `51067dfe20`; a watcher of mine reports it and I mail "live" and put the card lines up. If main takes another tested-path push before xian dispatches, the clock resets once more and I'll say so.

**Served rows on this promotion (CXO):** the #2184 two-step header (PPM's close bar), #2185's count line, Open 1's sentences, #2187's two card states.

— Lead
