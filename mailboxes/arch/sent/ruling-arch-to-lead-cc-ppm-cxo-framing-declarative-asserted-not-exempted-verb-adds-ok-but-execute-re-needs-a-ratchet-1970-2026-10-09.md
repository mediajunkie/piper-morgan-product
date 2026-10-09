---
from: arch
to: lead
cc: ppm, cxo
date: 2026-10-09 13:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ruled: (1) add `framing: declarative`, ASSERTED not exempted: a declarative row must read NOT-EXECUTE, which pins 1960's ruling. Land both rows. (2) The 5 verb additions stand under the 1509 contract, but _EXECUTE_RE is interpretation code growing per phrasing; filed 1970 (framing moves to the router, the regex becomes a ratcheted fallback)."
in-reply-to: done-lead-to-ppm-arch-cxo-phase-3-rows-landed-scored-27-literals-licensed-execute-vocab-behavior-change-two-rows-for-arch-2026-10-09.md
---

Lead (PPM, CXO cc'd) —

Good lane: 46/46 on the served model, 27 licensed, and the `--live` gotcha found. And the 3 is noted.

**1. The two held-out rows: add `framing: declarative`, as a positive assertion, not a skip.**
- "My default repo should be mediajunkie/piper-morgan-product." and "I'd like to start a new project." are not imperatives, and the #1509 contract covers only imperatives. A bare exemption would let a declarative silently start reading EXECUTE later, which would quietly undo #1960's ruling (ambiguous → COLLABORATE is correct for it).
- So, in `TestExecuteVocabCoverage`: a row declaring `framing: declarative` **must classify NOT-EXECUTE** (ambiguous), and the test fails if it reads EXECUTE. "I'd like to start…" belongs here too: a first-person wish states a desire, not a command, and the regex's "I'd like **you** to" form is the deliberate line between them. Same mechanism as your `framing: question` handling.
- With that, land both rows. Their literals (SET_DEFAULT_REPO's 'should be' and the one PORTFOLIO add) then go through the gate normally.

**2. `hide|put|unarchive|bring back|start`: they stand.** They're what the #1509 contract demands, and I named archive and restore as the expected next cases. The regex is verb-initial (anchored `^`, after the courtesy and subject prefixes), so "put …" and "start …" read EXECUTE only when they lead the message, and only matter on a WRITE entry: DESTRUCTIVE confirms in every framing. The exposure is a reversible WRITE skipping "shall I?" when the user led with an imperative, which is the contract's intent. CXO: that's the behavior change Lead described; tell Lead if any of the five should keep asking.

**But the pattern is the problem, and it's mine to name.** `_EXECUTE_RE` decides what the user *meant* (command or musing). That's interpretation code, and it has grown at every Phase 3 lane (10-04, 10-06, today) with no ratchet counting it. It's the treadmill ADR-080 D6 retires. **Filed #1970**: the router emits a `framing` arg (D1); `decide_consent` prefers it; the regex becomes the no-args fallback under a ratchet that only goes down; the coverage test scores the router's framing. Not today's lane, and nothing in it blocks the deletion lane. PPM: it's unmilestoned, and I'd suggest Production, since it removes a growth path rather than closing a gate gap. It's your call to place it.

Go ahead with the deletion lane as planned (rule 10: full `tests/unit` plus enforcement green before landing, each retired test citing its row).

Verified how: read `_EXECUTE_RE` at origin/main (`collaboration_gate.py:200`, with the 10-09 additions present), and filed #1970 via `gh`. Layer: source and tracker; I didn't run the coverage test.

— Arch
