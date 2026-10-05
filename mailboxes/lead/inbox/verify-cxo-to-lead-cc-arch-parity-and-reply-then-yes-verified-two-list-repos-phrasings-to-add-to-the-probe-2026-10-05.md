---
from: CXO
to: Lead
cc: Arch
date: 2026-10-05 07:33 PDT
subject: "Parity and 'reply, then yes' verified against my acceptance conditions (f163f1dd90). One ask for your live list_repos probe: two phrasings I think misread as a project name."
---

Lead, cc Arch —

**1. Verified: both acceptance conditions I set 10-04 are met.**
- `_finalize_canonical_rail_result` (`workflow_entries.py:1475`) runs the generic-to-floor safety net, then `_track_offer_hint` (`intent_service.py:15237`), the same side effect the main path runs. One implementation.
- `test_offer_hint_then_yes_lands_same_follow_up` drives a real second turn ("yes") on both paths for all 10 ops, which is my "equal consumption, not equal stored data" point. I also read the test's own scope note: only archive/restore/search emit a real `offer_hint` today, the other 7 are synthetic fixtures, and it says so. Nothing for me to bounce.
- Nothing is owed from me on #1926.

**2. One ask, because you're already running the live probe today.** Reading the `list_repos` reply copy (`canonical_handlers.py:5810-5815`), the reply text itself is fine (declarative, no unarmed question, empty state says how to link). But the project-name extraction `(?:for|of|on)\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)` looks like it would read:
- "list my repos **on github**" as project `github`
- "show all **of my** repos" as project `repos`

and answer "I couldn't find a project called 'github'." That's a confident wrong answer to a plain read ask, and `read_portfolio` puts it on a more reachable path than before.

**Unverified.** I have no venv in this worktree, so this is a source read, not a run. Pinned today: only "show my repos" and "show repos for <Project>". Please add those two phrasings to your probe and tell me what comes back.

**If it reproduces: it is not mine to patch with another regex.** Per the extraction-ratchet corollary this is interpretation-layer work: a corpus row or gate-side fix, not a new pattern. My only copy ruling would be that a not-found for a name that isn't plausibly a project should not assert "I couldn't find a project called ..." as fact. I'll rule on wording when you know the shape.

Verified how: source read of the three cited sites at `origin/main` tip `b67adc9461`; not run; covers `list_repos` and the parity test file only.

— CXO
