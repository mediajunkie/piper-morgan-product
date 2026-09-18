---
image: ''
alt: ''
caption: ''
---

# The Message That Deleted Itself

*August 14, 2026*

Friday morning, my chief of staff agent (Exec) sent out the week's workstream-review kickoff — a message to ten different roles across the team, asking each of them to write up their week for the regular Friday report we call Ship. The message went out clean. It landed in all ten inboxes, plus my own copy, plus Exec's own sent folder, and Exec checked that it had actually landed before moving on to the next thing on its list.

Twenty-two seconds later, it was gone.

Exec's next task was unrelated: clearing out some already-handled mail from its own local queue, a routine tidy-up pass. The mail system agents use to talk to each other works by taking whatever file paths you hand it and comparing them against what's already on the shared record, then recording the difference as the message. The cleanup pass happened to reference the very same file paths the kickoff had just used, paths that, in Exec's own local copy, had already been swept back to their pre-send state as part of normal bookkeeping. When that second, unrelated call ran, the system saw content on the shared record that didn't exist in Exec's local copy and read it the only way it could: as something that had just been deleted. So it deleted it. The kickoff vanished from all ten inboxes, from my cc copy, and from Exec's own sent record, less than a minute after it had gone out. Nothing malicious happened, and no one touched the file by hand. A tidy-up step and a delivery step used the same paths in the same short window, and the second one erased the first one as a side effect of doing its own unrelated job.

Nobody caught it right away, because nothing looked wrong from the outside. Hours later that evening I asked, mid-conversation, for the workstream responses to land that night instead of waiting for the usual Saturday deadline. Exec sent that correction out to everyone. And that's when three separate roles wrote back with the same observation, independently and without comparing notes: my experience-design agent (CXO), my documentation agent (Docs), and my principal product-management agent (PPM) all reported that the only message they'd actually received was the evening correction. The original morning kickoff had never reached them at all. None of the three assumed they'd simply missed an email in a busy inbox. Each one stated the gap as a fact and moved on to writing its report anyway, working from the correction memo since that was what it actually had.

Exec went looking for the actual mechanism instead of taking the coincidence of three matching reports as good enough evidence on its own. It walked the commit history, found the original send, found the second call twenty-two seconds later, and worked out exactly what had happened: not a delivery failure, but its own earlier action erasing its own earlier message. It confirmed the state directly against the shared record rather than trusting its own account of what it thought had happened, rebuilt the original kickoff word for word with a note explaining the accident, and sent it again in a single clean call. This time it checked that the message had actually stuck before running anything else that touched those same paths.

What makes this one worth telling is the shape of the failure, not that a message got lost (mail gets lost sometimes, and that's ordinary): the same mechanism that delivered the message, run a second time for an entirely different reason, read the message's own freshly-arrived presence as evidence that it should be removed. The message arrived, was verified, and was then unmade by its own sender's very next, completely unrelated action — not a failure to arrive, but an arrival undone by what came right after it, because that action reused the same coordinates without checking what was currently sitting on them. Exec's response is the part I want to hold onto: it reported the mistake to me in full, plainly, rather than quietly re-sending and hoping nobody noticed the gap, and the three roles who found the hole in their own inboxes reported that gap as a fact about the system rather than a fact about themselves. That's the difference between a mistake that gets buried and one that gets fixed for good.

---

*Next on Building Piper Morgan: "The Feature That Was Never Real" — a feature everyone believed was working turns out, on inspection, to have never functioned once in fifteen months.*

*Have you ever had a message, a file, or a piece of work quietly erased by your own very next action, one that had nothing to do with the first and never meant to touch it at all?*
