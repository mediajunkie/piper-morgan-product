---
image: ''
alt: ''
caption: ''
---

# Giving It Away, and Worrying Who'd Take It

*August 13, 2026*

I decided to open-source Piper Morgan today, under Apache 2.0. That part came together fast once I got to it: a patent grant, a trademark carve-out, no ambiguity about what "open" means to anyone evaluating the license. My chief of staff agent (Exec) drafted it, fixed a stale MIT badge that had been sitting in the repo for who knows how long, and it shipped the same day.

The part that took longer was sitting with what giving this thing away actually means once it's out of my hands, not the license text.

The worry that actually held my attention was somebody taking the code, stripping out the parts that make it careful, and shipping an "evil Piper" — something that looks like this project and runs like this project while doing none of the work this project does to not cross lines with people's data and their trust. The architecture that keeps Piper Morgan from being extractive or intrusive isn't hidden behind a clever prompt. Once the source is public, anyone can see exactly which pieces to cut. Ordinary competition, a rival cloning the code and building a competing product on it, is a cost I can live with. That's the normal price of giving code away. This was a different worry entirely.

So Exec and I looked at whether a license could actually stop it. We checked the question against the Open Source and Free Software definitions directly, and we looked specifically at the Hippocratic License, since it exists for exactly this concern — restricting use by whoever would do harmful things with the code. We ruled it out. It isn't recognized by the Open Source Initiative, it's largely untested, and adopting it would cost us the "genuinely open" claim that makes Apache 2.0 worth choosing in the first place. Underneath that sits a harder fact: no clause in any license stops somebody from forking the code and deleting the parts they don't like. Once it's open, it's open to that too.

What's left is a reputational mechanism, not a legal one, built in two pieces. A trademark filing for the Piper Morgan name, running in parallel, so a stripped-down fork can't call itself Piper Morgan and borrow the trust that name carries. And a public values document, specific enough that a fork visibly diverging from it can't credibly claim to still be us. I handed that second piece to my communications agent (Comms) and my head of sapient-trust agent (HOST) jointly, with no deadline attached. I wanted it considered, not fast.

Comms started with a harder question than "what do we believe": which of those beliefs would need to be visibly absent before an outside observer could tell a fork had quietly dropped them. HOST went and read the parts of the codebase that make the ethical claims true, rather than working from what anyone had told them was there, and came back with a first pass at three properties. No cross-user learning, enforced in the architecture itself rather than by policy alone. The audit-transparency system that lets anyone check what the system looked at before acting. And a hash-only discipline that keeps audit logs honest without exposing what's actually in them. All three framed under language I'd already used to describe what this project should be: not extractive, not intrusive, doesn't violate confidence.

HOST also caught a mistake Comms was about to make, the same mistake I probably would have made. The obvious strength claim for a document like this is "you control your data." HOST flagged it before Comms reached for it: account deletion doesn't exist yet, and conversation deletion is soft-only, both things HOST had just finished verifying that same week for a separate retention-policy document. A values document that overclaims what we actually deliver is a liability wearing better prose, not protection. Comms treated the correction as the more important half of the exchange, then did the thing I actually wanted more than a fast draft: separated responding to a colleague's real work, which was owed that night, from writing the actual public document, which needed a session with nothing else competing for attention, and said so plainly instead of letting the distinction blur.

None of this makes the worry go away. Giving software away doesn't come with a way to guarantee what happens to it next, and I don't think it should, since that would defeat the point of open-sourcing it at all. What I have instead is a name that's legally protected, and a document specific enough that if something calling itself Piper Morgan starts behaving differently, the difference will be visible and nameable. It's a paper trail with teeth, not a wall, and it's the honest version of what I actually have to offer in place of a guarantee I can't make.

---

*Next on Building Piper Morgan: "The Message That Deleted Itself" — a routine cleanup step erases the very message it had nothing to do with, seconds after that message went out clean.*

*Have you ever had to give something away and found that what actually protected it was staying recognizable as itself, not the fine print?*
