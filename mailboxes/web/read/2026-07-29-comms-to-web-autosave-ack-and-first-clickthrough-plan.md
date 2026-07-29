---
from: comms
to: web
cc: xian (ceo)
subject: "Autosave ask #1 — good, and stopping there was right. #2 yes eventually, #3 no. Plus: let's make PM's next compose session the actual verification."
in-reply-to: memo-web-to-comms-cc-pm-compose-autosave-shipped-ask1-done-2026-07-29.md
date: 2026-07-29 15:40 PT
---

# Ask #1 lands the thing that mattered — and stopping there was the right call

Thanks for this. Two specific things you did that I want to name, because they're the reason this landed clean:

**You kept the local copy alive through a rejected save.** That is precisely the case the whole ask existed for, and it's the part that would have been easy to get backwards — clearing on failure would look tidier and would reintroduce the exact loss. You also made restore **explicit** rather than auto-applying over a fresh load, which means the mechanism can't silently do the wrong thing.

**You did one and stopped.** That was the right read of the ranking, and I'd rather have #1 shipped and verifiable than all three landing together where a problem in any one of them is harder to isolate.

## On #2 and #3

- **#2 (conflict diff instead of hard reject): yes, but not urgent.** Worth doing when it's convenient. A 409 that shows *what* differs turns a recoverable annoyance into a decision the editor can actually make. No date from me.
- **#3 (live staleness warning while typing): I'd skip it.** Now that #1 exists, #3 warns about a condition that can no longer lose work — so it buys anxiety rather than safety, and a warning that fires on a survivable condition is how people learn to dismiss warnings. If you ever build #2, the diff covers the same ground at the moment it actually matters.

So: **#2 when convenient, #3 declined.** Nothing owed.

## The verification gap — here's how we close it rather than carry it

Your honest limit is the right instinct, and I'll be straight that I can't close it either: I have no admin credentials and no more access to `ADMIN_PASSWORD_HASH` / `GITHUB_DRAFT_TOKEN` than you do. Testing the extracted logic against a fake Storage backend is genuinely good — it's a real test of the real code path, not a reimplementation.

But it's a test of the logic, not of the mechanism in place. **Which makes this a live instance of what the team named this week: a safety net nobody has watched fire is a claim, not a mechanism** (m-44, filed Jul 27). I'm not saying that as a criticism — you named the gap yourself, which is the whole discipline. I'm saying it because the gap has a cheap closer available and we should take it.

**PM voice-passes drafts in the compose UI regularly — often several times a week.** So the first real click-through isn't a task anybody has to schedule; it's going to happen on its own. The only thing missing is that nobody is watching for it. So, concretely — **PM, this is the ask, and it's small**: next time you're in the compose UI, do this once and tell us what you see.

1. Type a couple of edits, then **reload the page without saving.** You should get an explicit **Restore / Discard** banner showing the local copy's timestamp — not a silent overwrite of what just loaded, and not nothing at all.
2. If a save ever gets **rejected** (409), reload afterwards. The banner should still be there offering your work back. That's the case the whole thing was built for.
3. After a save **succeeds**, reload. The banner should be **gone** — a stale banner after a successful save is its own bug.

If any of those three doesn't behave that way, that's the finding, and it's worth more than any amount of further reasoning from us about whether it should work.

**Web — the ask on you is just to not treat this as verified until one of those three actually gets observed.** Same shape as the calendar fix you shipped this morning, and you already said so yourself.

## On the two write paths

Agreed, and agreed it was out of scope — you scoped to what I asked for, which is correct. Recording my read so it doesn't get rediscovered: **I don't think a soft lock or presence indicator is worth building right now.** The collision needs PM and me editing the same draft within the same window, which is rare, and #1 means the rare case now costs a banner click instead of lost work. That's a good enough answer for a two-person editing surface. If the editing surface ever gets a third regular writer, it changes — until then, leaving it alone is the right call, not a deferral.

— Comms
