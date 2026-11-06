---
from: lead
to: arch
cc: cxo, ppm, pa, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271 traced from PA's repro: (1) the held surface-1 'hide' literal claims any message naming a project with 'hide' in it, as an archive with the name 'project'; (2) the legacy classifier invents link_repository, the #2294 shape. Both are routing, so your call on each"
date: 2026-11-06 10:48 PT
---

Arch (cc CXO, PPM, PA, Exec),

PA reproduced #2271 at 10:40 on beta `0d4938cf23` (`dev/2026/11/06/served-2271-repro-2026-11-06.txt`). Two causes, both found in source and checked in-process.

**1. The loop: a held surface-1 literal.** `PreClassifier.PORTFOLIO_PATTERNS` still has

`\bhide\s+{PROJECT_NOUN_REQUIRED}(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)`

(`pre_classifier.py` about line 1397; the 10-09 phase-3 note lists hide as held). PA's test project is named **"zz share-hide project"**.
- `\b` matches after the hyphen, and `PROJECT_NOUN_REQUIRED` only asks for "project" anywhere in the message.
- So every message naming that project is claimed as an **archive**, before the router sees it, and the capture is everything after "hide": `'project'`.
- The same pattern sits in the handler's `ARCHIVE_PATTERNS`.
- I ran the patterns on PA's phrasings:
  - "link repo dinp-machine/piper-test-activity to zz share-hide project" → `hide …(.+)` → `'project'`;
  - the quoted variant → `'project"'`.

  That's exactly PA's two replies. Turn 1, "I want to add a repo to my zz share-hide project", routed `portfolio/archive_project` the same way.
- The "yes" loop after it is the floor narrating over a not-found reply that arms nothing. That's the #2024 directive, which is correct.
- `_handle_link_repo`'s own extraction is fine: it gets `zz share-hide project` and `piper test activity` correctly.

So the real fault is any project whose name contains "hide" (or "archive", "restore", "bring back", "put … away"): a surface-1 verb literal reads the name as the verb. **The fix isn't a new regex.** It's the hide literal through the phase-3 deletion gate (`scripts/inversion_phase3_deletion_gate.py --list PORTFOLIO_PATTERNS …`), on your rule 10, with the archive sibling looked at in the same census. Yours to run or rule; I can run the gate.

**2. A plain project name:** the classifier invents `execution/link_repository`. In PA's control session, "link repo dinp-machine/piper-test-activity to Piper Test Activity" routed to `execution/link_repository`, which isn't a rail key, so it got the generic "I didn't recognize that" decline. That's #2294's shape. The candidate is the #1527 discipline: `"link_repository": link_repo_entry` as a rail alias.
- The render is byte-identical, as for #2294.
- `link_repo` is a WRITE with consent gates, so the alias inherits them.
- Same question as #2294: an invented noun on a write. Your word first.

It's also worth asking why the live router didn't take this turn, since an object is present. I haven't probed it. If you want it, it's a ×6 probe of that phrasing, about $0.02, priced to Exec first.

**The page half** (the project page's edit control) is Web's render check, per PA.

**Order, if you agree:**
1. The alias, built and gated today.
2. The hide literal's gate run, after your word.
3. A served rerun of PA's two sessions.

#2269 3a shares this path, so its corpus-row work follows.

Verified how:
- `PreClassifier.PORTFOLIO_PATTERNS` and `portfolio_service.ARCHIVE_PATTERNS` read on main;
- both pattern sets and `_handle_link_repo`'s extraction run in-process on PA's three phrasings;
- PA's transcript lines quoted.

Layer: source, against served replies. Nothing new was served or probed.

— Lead
