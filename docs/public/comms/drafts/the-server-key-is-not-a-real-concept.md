---
image: ''
alt: ''
caption: ''
---

# The Server Key Is Not a Real Concept

*September 13–15, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. PM writes
the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Slot: Thu 2026-11-12 (building). Beat 3, after Tue 11-10 "Never Green in a Thousand Runs" (Sep 9–11). xian said yes
11-04 and may change the title.
Merge with beat 4 ("The Wall")? Recommend NO. See the bottom of these notes.
Footer teases whatever follows on the calendar (nothing after Thu 11-12 yet except Ships). Pick it at the weekend.
Sources: decisions.log l.1885, 1887, 1889, 1891 (09-14); Lead 09-14 log (l.102-110, 140-152, 177-221); Exec 09-14 log
(l.118-164); Arch 09-14 log (l.84-86); PPM 09-14 log (l.150); omnibus 09-13 (l.126-131), 09-14 (l.141, 160-192, 225) and
09-15 (l.31-82, 186-193). Facts gathered by a Sonnet subagent. Comms re-opened the key quotes at source.
The tester is never named in this post or this file (rule 8). Some sources name them. Do not copy that.
-->

---

## Title options (pick one, or your own)
- **The Server Key Is Not a Real Concept** (working). Your ruling, nearly word for word.
- **Why Does the Operator Have Money to Spend?** The question that turned a fix into a deletion.
- **Authentication Is Not Billing.** Lead's diagnosis.
- **Hold Until We Stanch This Leak.** Your hold, as typed (minus the typo).

## The story in one sentence

An outside tester's invitation was minted and ready to send when Lead found that any signed-in user with no key of
their own would spend yours, and that the tester's key would silently replace yours. You held the invitation, and then
asked the better question: why does the operator have money to spend at all?

## Beats, in order (facts verified, source in brackets)

**1. Someone asks to join.** Sun Sep 13, about 1:00 PM: you forwarded an outside tester's request to join the alpha.
HOST checked alpha was live and routed the invite. By Monday HOST had it minted: "ready whenever you want to send it."
[omnibus 09-13 l.126-131, Exec 09-14 l.124-127]

**2. The fallback.** Mon Sep 14, 1:02 PM: you made server-key exposure the top priority. Lead found that the code
looked for a key in order: the request, the user's stored key, then the **server key**, for any signed-in caller. An
earlier fix had closed it only for anonymous callers. The code comment called it "safe, because the caller is a
known, authenticated identity". Lead: "that conflates authentication with BILLING AUTHORIZATION. True enough when the
only authenticated identity was PM; false the moment a second person logs in." [Lead 09-14 l.102-108]
- Fixed and deployed by 1:25 PM. Four existing tests had pinned the hole as intended behavior. [Lead l.140-152]

**3. Worse.** The setup flow also copied every user's key into one shared slot, last writer wins. The tester's first
setup would have made their key "the server key": billing them for anything that still used it, and displacing yours.
Exec: sending the invite "IS the trigger." [Exec 09-14 l.118-135, omnibus 09-14 l.225]
- Exec's aside: the shared write survived a whole security epic because its comment read like plumbing ("so LLMClient
  can find keys during server startup"). [Exec l.136-139]

**4. The hold.** About 4:05 PM, as you typed it: "yes hold under we stanch this leak." Arch's bar: the shared write is
gone, and that is seen in a real setup flow, not only in a test. [Arch 09-14 l.84-86, decisions.log l.1885]

**5. The question.** 5:30 PM, your ruling: "THE SERVER KEY IS NOT A REAL CONCEPT AND WILL NOT BE SUPPORTED IN ANY
SENSE." And why: "I don't understand why anybody should ever be able to spend the operator's money or why the
operator even has money to spend… The software that we're building should never be accessing an API for its own
purposes." [decisions.log l.1887]
- The reason in one line: "We don't use the business model of reselling tokens or anything like that." [l.1889]
- Left open on purpose: "unless someone can describe some sort of minimal bootstrap situation." Nobody could. Lead's
  census found background jobs make zero model calls. [l.1891, Lead l.177-189]
- What it meant: the concept was deleted, not gated, and your own hosted use would need your own stored key like
  anyone else's. [decisions.log l.1887, Lead l.199-214]
- Lead, on its own day: "I spent the day fixing WHO may spend the operator's money without ever asking why the
  operator has money to spend." [Lead l.221]

**6. Held twice more before it went.** The shared-slot fix closed that evening. HOST refused a test-only proof and
waited for the observed flow (9:55 PM), then lifted the hold. Tue Sep 15, 6:47 AM: a new find, a tester's own stored
key was never read, so the invitation was held again. It closed on a real rejected call made with a throwaway key, so
your key was never spent. HOST lifted the hold at 9:53 AM. [omnibus 09-14 l.160-192, 09-15 l.31-82]

## Careful with these (accuracy)
- **"Truth is more important than the feeling of progress" is NOT about the key.** It's your exact wording, the same
  evening (5:29 PM), but it ruled on reopening an epic rather than starting a successor. [Lead l.190-191, PPM 09-14
  l.150] The planning doc's one-line summary attached it to the key. That was wrong. Use it only as "the same hour,
  you also said…", or leave it out.
- **The invite exposed two things, not one:** your key spent by a keyless tester, and the tester's key replacing yours.
- Hold, then ruling: the hold (4:05) came before the ruling (5:30). The ruling answered the question you asked after
  Lead's fix.
- Did the invitation actually go out? Ship #062 says reissuing access for two testers was held to the following week.
  Check your own memory before saying it was sent on Sep 15.
- Never name the tester, their employer or their words.

## Already told elsewhere: don't retell
- **Ship #060**: the bug was "closed before the first outside tester", and the invite was held until the fix was observed.
- **Ship #061**: "an alpha tester could have spent the operator's money", plus the hold twice and the observed-flow
  bar. The public record has the what. This post is the why: your question about the operator's money.

## Beat 4 ("The Wall", Sep 15–18): recommend keeping it separate
Different cause, different story. The weekly usage limit hit 97% on Sep 15 from heavy Saturday work plus a lower
ceiling, and on Sep 16 you suspended every duty cycle until the Thursday reset. Ten of eleven seats parked. HOST's
row was missed and went dark about 39 hours. Restarting from handoff notes on Sep 18 showed which seats' records held
up. [omnibus 09-15 l.186-193, 09-16 l.38-46, 09-17 l.61-63, 09-18 l.15, 45-50] It stands as its own beat, or folds
into beat 5. Your call at the weekend.

## Your angle, maybe
- Why "why does the operator have money at all" was the question nobody had asked, and what bring-your-own-key means
  for what Piper is.
- The comment that read like plumbing: how a security hole hides in a sentence that sounds harmless.

---

*Next on Building Piper Morgan: [TEASE: the next post after Thu 11-12 (not yet on the calendar). Confirm the title
first.]*

*[Reader question, yours to write. A start: "Is there money in your product that nobody has asked why it's there?"]*
