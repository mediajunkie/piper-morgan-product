---
image: 'storm-window.png'
alt: 'A writer watches as a single page lifts from a neatly stacked manuscript and blows out through a slightly open window, illustrating how a brief window of vulnerability can put valuable work at risk.'
caption: '"I meant to close that!"'
---

# The Server Crashed Mid-Draft

*May 17–21, 2026*

I was drafting a post one evening — somewhere past the halfway point, deep into the part of the writing where revision and forward motion blur into the same activity. The session ended unexpectedly. Server error, network drop, something on the platform side I couldn't see and couldn't recover. When I came back to look two days later, I expected to find my draft as an untracked file in the working tree.

It wasn't there.

I'd saved it, but I hadn't "committed" it. Untracked files don't always survive a hard session crash. The post was gone.

# The category

This is a specific category of vulnerability that's easy to miss because most of the time it costs you nothing. New files in untracked state — files you've written to disk but not yet committed to version control — exist in a small window where they're visible to you, accessible to your tools, present on the filesystem, but completely outside the repository's safety net.

A `git pull` may move them or warn about them or proceed past them depending on flags and conflicts. A `git checkout` to a different branch may or may not preserve them depending on what the destination branch has at the same path. A `git stash -u` will sweep them into the stash and remove them from disk. A session crash that loses the working directory entirely loses them silently, with no rollback path and no diagnostic trail.

This is git working exactly as documented. The vulnerability lives in the gap between *I wrote this* and *this is in the history.*

# Why it's hard to remember to close the window

In normal flow, the cost of an uncommitted file feels low. You can see it. You know where it is. You'll commit it in a few minutes when you reach a natural stopping point. The vulnerability window is short. The probability of a session crash inside that window is small.

The trouble is the probability is small *but nonzero*, and the consequences are total. Most of the time the few-minute window costs you nothing. Sometimes it costs you the file.

That asymmetry — high-frequency tiny win, low-frequency total loss — is why people ignore disciplines for years without consequence and then catastrophically regret skipping in a single moment. Wear a seatbelt every car ride. Back up your laptop weekly. Commit immediately after writing a new file. The first two are old wisdom. The third one I had to learn the way you learn most things — by losing the file. And I still treat it like flossing!

# What "immediately" actually means

The discipline that came out of the incident is mechanical: after writing a new file with substantive content, run `git add` and `git commit` and `git push` *in that order, before any other substantive tool call*. Thirty seconds of overhead. Closes the window from minutes-or-hours down to a few seconds.

The commit doesn't have to be polished. The message can be "WIP draft" or "scaffolding the structure" or "initial sketch." The commit is a checkpoint, not a release. What matters is that the file exists in the repository's history, not just on disk.

Push matters too, separately. A local commit survives most session crashes — git's object database is durable on disk. But the worktree's disk itself can fail. Network outages and hardware faults aren't the most common failure mode, but the cost of the push is so low that there's no good reason to defer it. Push is what makes the file survive everything below the level of the remote.

# The variance is what kills you

Loss of an uncommitted file isn't proportional to its size. Reconstructing a fifteen-hundred-word post from memory is a few hours of focused work, in a state where you've already done the hardest part — the original drafting — and you're now doing it again, more slowly, with the friction of *I already had this and I lost it.* The reconstruction is usually worse than the original.

Reconstructing a one-line commit message is seconds. The variance of recovery cost on uncommitted work is wildly skewed. New files with substantive content sit at the high end. New scaffolding files that haven't been touched since you created them sit at the low end. The category that warrants the discipline is the high-cost end. You can be looser about the low-cost end — but the discipline that says *just always commit immediately* is easier to follow than the discipline that says *commit immediately when the cost-of-loss is high.* The first one is mechanical. The second one requires judgment in the moment you're least likely to apply it.

*I will be honest, though. I am still sloppy about this. Some of it is the context switching. I am editing directly on my Mac, in a file editor. To commit the work after editing means switching to a terminal or development tool. I am lazy. "Can't you do it for me?" is my whiny refrain.*

# What rescued me this time

The draft did get recovered, two days later. I remembered the through-line clearly. I'd been writing in voice that returned naturally. The reconstruction landed close enough to what I'd lost that the post made it to production on its original schedule.

That's a happy ending, but not one I want to count on. The recovery took a real chunk of focused work — attention I'd planned to spend on something else. The discipline I now run is the alternative: thirty seconds of commit-immediately, no recovery cost, no detour.

The math isn't subtle. The math is almost too obvious to write down. The seductive thing about the few-minute window is that it almost always feels safe. Each individual instance you skipped the commit and got away with it reinforces the *almost always.* The instance where you don't get away with it is the one that pays for all the times you did.

# The deeper read

Every workflow has invisible failure modes. The mature response isn't to avoid the failure modes — that's mostly impossible. The mature response is to identify the windows of maximum vulnerability and close them mechanically.

Commit-immediately-after-write is one of those mechanisms. There are others: regular pushes, version-control-everything-not-just-code, treating your editor's autosave as no substitute for git history, treating cloud sync as no substitute for either. Each closes a particular kind of window. None of them are clever. All of them are habits.

The discipline is about recognizing where you're exposed and shortening the window, not about being unusually careful. Once the discipline is muscle memory, the cognitive cost drops to near zero — the keyboard knows to type the commit before the next thought arrives. The vulnerability window collapses from minutes to seconds, and the few-minute window stops existing as a category of risk.

The post I lost did come back. The next post won't have to. Thirty seconds of immediate commit closes a window that, in retrospect, never should have been open.

---

*Next on Building Piper Morgan: "The Migration Wave" — a realignment, the team gone worktree-native, a confabulation caught, and a launch: the arc's resolution, told as operational-not-finished.*

*What's a discipline you only adopted after losing the file the discipline would have saved? Where in your workflow do the few-minute windows still live? What does it take to make a mechanical habit out of something that mostly costs you nothing?*
