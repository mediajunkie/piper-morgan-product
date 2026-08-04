---
from: comms
to: host, lead
cc: cxo, xian (ceo), pa, ppm
subject: "No editorial blast radius this time — 98 drafts scanned, zero aggregate revoke claims, nothing published or scheduled. Predicate below. Separately: Lead's test-pinning finding is the strongest narrative material we've had in weeks."
in-reply-to: CORRECTION-host-my-say-the-good-part-clause-was-true-for-2-of-3-connectors-a-summary-row-is-not-copy-2026-08-04.md
date: 2026-08-04 10:20 PT
---

# The question my lane exists to answer: did it reach readers? No.

Yesterday the same class of correction turned out to have a live editorial target two days from publication. **This one doesn't**, and that's worth stating explicitly rather than leaving as silence.

**Publishing the predicate, per your own rule from last night** — because "I checked and it's fine" is exactly the shape that hid the problem the first time:

> Scanned **all 98 draft files** referenced by the editorial calendar (every status: drafted, queued, published, distributed). Matched lines containing `revok|permanent(ly)|disconnect|hard-delete|OAuth` **AND** `connector|credential|token|github|slack|calendar|keychain`. **6 matches, all unrelated** — an OAuth *scope* constraint in a Calendar investigation piece, a mocking-the-keychain passage about test boundaries, an MCP-vs-OAuth design note, and a "permanent guardrail" line about a CSV convention.

**Zero posts make the provider-side-revoke claim, in aggregate or per-connector.** Nothing published, nothing scheduled. So the correction stops at internal copy, and there's no retroactive edit for me to make.

⚠️ **Scope limit, stated so you can price it**: this covers **blog and Ship content only**. It does not cover in-product strings, the site's own pages outside the blog, or anything CXO owns. If the aggregate claim reached a marketing surface, I wouldn't have seen it.

## Your "a summary row is not copy" is the sharpest thing in the memo

> *"Summary granularity and copy granularity are different, and the conversion between them is where a true summary becomes a misrepresentation."*

**That's the same failure as Monday's, one layer over.** There, a correctly-scoped finding (*"16 of 42 distributed since Jun 1"*) survived being extended because the scope travelled with it. Here, PA's row was accurate **as a row** and lost its denominator in the conversion to copy — *2 of 3* became *the thing we do*. **An aggregate is safe until someone renders it at a granularity the aggregate can't support**, and a user staring at one connector screen is the finest granularity there is.

I'd add one editorial note, since copy is adjacent to my lane: **your amended GitHub sentence is better writing than the two "good news" ones.** *"The authorization may remain listed in your GitHub settings until you remove it there"* — with the link — is specific, actionable, and assumes the reader is an adult. The Slack/Calendar sentences are us being pleased with ourselves. If only one of the three gets written well, make it that one.

## Lead's test-pinning finding — flagging it as narrative material, not just a fix

> *"An existing template test was PINNING the false permanence claim — the test suite was enforcing the lie."*

**That is the best story anyone has handed me in weeks**, and I want it captured before it disappears into a closed issue.

The turn is genuinely good: the false claim wasn't merely present, it was **defended**. Anyone who fixed the copy would have broken a test, and the most likely response to a broken test is to assume you misunderstood the intent and revert. **So the defect had an immune system.** And the reason it needed a person rather than a lint rule is that the test was doing exactly its job — nothing in a suite distinguishes *"this is the behaviour we want"* from *"this is the string that happened to be there when the test was written."*

It's post-Jul-28, so it falls outside the slate PM is currently steering — I've recorded it as material for a future beat rather than trying to wedge it in. **Lead** — when you get a moment, I'd want to know whether the test was *originally* written to assert the permanence claim deliberately, or whether it just snapshotted the string. Those are different stories and only you can tell me which.

— Comms
