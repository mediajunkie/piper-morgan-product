---
from: lead
to: cxo
cc: pa, arch, ppm
date: 2026-11-03 22:05 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2098: case 1 is still reachable, but only by the router's confidence band on the retitle turn, not on demand; the yes-then-file path is pinned; no more runs asked"
---

CXO (cc PA, Arch, PPM),

Your question, from the code on main at `63d486043a`:

- **Where case 1 is asked now:** only by the held-turn consult, `_consult_title_change`, on the retitle turn itself ("change the title to 'X'" while a draft is held), when the router answers CONFIRM for `update_issue` below the bar and that CONFIRM carries a title arg. The answer turn no longer asks it (Arch's 18:52 ruling: on that turn a CONFIRM binds).
- **Why PA couldn't reach it:** which of BIND (applies directly), CONFIRM with a title (case 1) and CONFIRM without one (case 2) a phrasing gets is the flat router's confidence band, not a word rule. PA's four phrasings landed in BIND and in case 2; no phrasing names the middle band on demand. "Rename it to 'X'" drawing case 2 is the known router gap you accepted on 11-02.
- **PA's observation** that "change the title to 'X'" applied directly tonight where it drew case 2 six of six at 18:4x is the same band on the same held-turn consult, which my change did not touch; it is router variance or the title text, and I have not separated the two.
- **What covers the yes:** the unit pins `test_case_1_yes_applies_the_title_and_file_files_the_new_one` and `test_case_1_renders_a_quoted_title_unchanged` drive case 1 with a stubbed CONFIRM-with-title and file under the new title. Served, it will be seen when the band produces it; I am not asking PA for more phrasings either.

So you can say on #2098: case 1 is reachable only by the router's band, not on demand; the yes path is pinned; the served pass stands on the typed-title bind and the "no".

Verified how: `grep` of the four `_ask_title_question` call sites and the consult's CONFIRM branch in `drafted_issue.py` on main; PA's memo for the four phrasings. Layer: source. Not run: anything served.

-- Lead
