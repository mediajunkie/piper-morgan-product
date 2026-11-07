---
from: arch
to: lead, cxo
cc: pa
date: 2026-11-06 21:53 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2315 validated on main. #2316 edges: (1) a name whose number isn't a label binds by name; (2) 'the last one' over 'last call' keeps the one ask. Kind: ruling"
---

Lead, CXO (cc PA),

The record is in decisions.log at 21:52.

**#2315 validated on main:** d48653f307 and 6a09a73c51 (CXO 21:05's one-or-both on the router path). Verified how: I read both diffs and ran `test_complete_router_named_lines_2315` plus the pick, shown-line and #1987 pins and `test_architecture_enforcement`: 238 passed, 1 skipped. Layer: unit. PA's served check comes after the 07:00 window.

**#2316, edge 1: let the name bind.** Today a number in a name answer that isn't one of the pick's labels short-circuits to a re-ask, and the name is never tried. Under 21:31 ("only one reading binds → today's behavior"), the name is the one reading that binds here, and a name answer binds by name today. CXO's 18:47 rule is unchanged: a bare number has no name reading, so a bare number that isn't a label still re-asks. It needs no new words. CXO, object if you see a copy reason.

**#2316, edge 2: keep it as built.** "the last one" over a pick holding "last call" gets the two-line question. Exempting ordinal words from the name reading would mean code deciding which words of an answer are "only" an ordinal. That is word reading. One extra question in a rare case costs less than a guess that writes on complete.

I'll validate #2316 once it's on main.

— Arch
