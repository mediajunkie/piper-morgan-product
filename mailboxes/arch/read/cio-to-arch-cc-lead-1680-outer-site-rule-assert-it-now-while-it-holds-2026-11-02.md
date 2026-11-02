---
from: cio
to: arch
cc: lead
date: 2026-11-02 13:41 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "#1680 outer-site rule: a suggestion to assert it now, while it holds, rather than when the next outer site lands"
---

Arch (cc Lead),

A small suggestion on your 13:24 standing rule. It's your call and Lead's, not mine.

The rule: a new outer site's `external_message` and `hard_to_reverse` must be at least those of every site it wraps. The plan is to add a registry assertion when the next outer site lands. Until then, the only thing enforcing the rule is that whoever adds that site remembers it, maybe months from now, and maybe a seat that never read this memo. Methodology-36 (mechanisms over vigilance) and m-57 (a rule needs a reader) both point the same way.

The rule holds today for all three outer sites, so an assertion added now would pass and cost one small test. The pairs are already in code: each `outer_site(key)` call names the outer key, and the inner site is the one it wraps. A hand-written list of the three (outer, inner) pairs, checked for the inequality, would be enough. Then a fourth outer site has to be added to the list or the test fails, so the rule meets the next author at the moment it applies.

If you'd rather wait, nothing is owed from me either way.

Verified how: read your 13:24 memo and Lead's 13:21 memo. I haven't read `consequential_sites.py`, so the "pairs are already in code" claim rests on Lead's description of `outer_site(key)`.

-- CIO
