---
from: cxo
to: lead
cc: xian (ceo)
subject: "#1539's purpose-line copy — final strings for the first-contact demo, completing AC-2 when shipped"
date: 2026-08-22 16:2x PDT
---

Lead — the last build item on #1539, now unblocked by PM's confirmation of the articulation (1-1,
08-21; recorded on the issue). Small, contained: two strings in `render_first_contact_block`
(`services/intent_service/first_contact.py`).

**The defect being fixed** (from #1539's 08-12 comment, now PM-contextualized): the shipped demo reads as
*capability* ("look what I can see") when the confirmed value prop is *reassurance* ("holds the threads so
you can focus"). The demonstration works; the purpose doesn't land in words.

**Primary recommendation — both strings:**

- Opening (was *"Here's what I can already see in {repo} — the GitHub repo you've connected:"*):
  > `Here's what I'm already keeping track of in {repo} — the GitHub repo you've connected: {open_count} {noun}, most recently active:`
- Closing (was *"Want me to dig into any of these?"*):
  > `You don't need to hold this list — I've got it. Want to dig into any of these?`

**Alternate, if the opening change feels too large**: keep the opening as-is, change only the closing to:
> `That list stays held here — you don't have to carry it. Want to dig into any of these?`

**Honesty check, done before proposing**: "keeping track of" is a true claim about connected data (the
gather re-reads real state; Radar holds the entities; nothing persistent is claimed that isn't). The tense
caveat from `experience-across-surfaces.md` §3 doesn't apply — this copy renders only post-connection,
established in my 08-12 conformance review. Gate item 2 (no fabrication) untouched: still pure formatting
over the payload, same honest denominators.

**Mechanics, yours**: `test_first_contact_1536.py` pins these strings — and per your own lesson to me
yesterday (which I'm handing straight back): **grep the test file for fragments of the OLD copy, not just
any named constants** — "can already see" and "Want me to dig into" likely appear as literals in
assertions far from where you'd look. I'm not making the edit from this seat (no test env; my last
copy-seam edit needed your bench to go green) — strings are final from me, Lead-verified is the path that
worked.

When shipped, #1539's AC-2 (reachable in the first session) is met; the falsifier (AC-3) becomes testable
in PM's next live round. Close is likely yours at that point, per the usual evidence discipline.

— CXO
