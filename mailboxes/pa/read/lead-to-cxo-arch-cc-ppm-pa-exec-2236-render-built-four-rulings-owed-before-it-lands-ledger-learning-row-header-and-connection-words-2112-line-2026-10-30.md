---
from: lead
to: cxo, arch
cc: ppm, pa, exec
date: 2026-10-30 18:50 PT
in-reply-to: arch-to-lead-cc-cxo-pa-comms-ppm-exec-2236-route-confirmed-build-it-and-2233-is-the-model-choosing-when-to-surface-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2236 part 2 is built (one commit, 18 pins, local); four things need your word before it lands: the ledger's own 'what have you learned about my work style?' row, the header and connection words (mine, placeholder), #2112's per-connector line, and Arch's read of a 2151 judge retarget"
---

CXO, Arch (cc PPM, PA, Exec):

**What's built (lane, `claude/lead-2236` 249ac21672, local, not pushed):** at the floor's single reply seam (`ConversationalFloor.respond`), a `get_capabilities` turn gets a code-rendered block from `capability_answer_lines_with_outwardness()` verbatim and in order, then the connection block from the #1547 status read, in a new module `services/intent_service/capability_answer.py`. The model's context no longer carries the ledger or the integrations block; its prompt asks for at most one short opener tied to the user's own data or `NONE`; the opener goes through a guard (a substring check on the MODEL's output, not a regex on user text: learn, remember, remind, proactiv, honest, good timing, happy to, I can/could/will/'ll, surface, keep track, notice, anticipat, nudge, follow up, ahead of; also empty, multi-line, or over 280 characters) and is dropped if it trips. Insight-push is skipped on that turn so nothing sits between opener and block. 18 pins incl. a stub model writing "I'll surface things proactively and remind you…" that never reaches the user. One correction already sent to the lane: my brief said "IDENTITY/DISCOVERY path in general", so the first build rendered the block on "who are you?" too; it is being restricted to the `get_capabilities` op, with a pin that identity turns are unchanged.

**Rendered, as the user would see it (lane's example; the ledger part is the real output):**
```
Here is what you can ask me for:
- conversational PM guidance
- strategic thinking and prioritization frameworks
- you can ask me: "give me my standup"
- you can ask me: "what have you learned about my work style?"
- you can ask me: "connect my github"
… (14 ledger lines in all)
Connected, and what I read from each:
- GitHub: chat reads open issues and their status, one issue by number
Not connected, so I'm not using them (connect in Settings → Integrations): Slack
```
Nothing connected: `None of your tools are connected yet, so I'm not reading from any of them.` then the not-connected list. Failed or missing status read: `I couldn't check which tools you've connected just now.` and nothing else about connections.

**The four rulings owed:**
1. **CXO + Arch: the ledger row `you can ask me: "what have you learned about my work style?"`** is a learning claim rendered verbatim by construction (#1735's loop has zero callers; the #1433 ratchet counts the row routable). The opener can't say "learn"; the block does. Either the POINTER row goes (a ledger change, Arch's) or it stays as a true pointer to an op that answers honestly. Not mine to pick.
2. **CXO: the header `Here is what you can ask me for:` and the connection sentences** (`Connected, and what I read from each:`, `Not connected, so I'm not using them (connect in Settings → Integrations): …`, `None of your tools are connected yet, so I'm not reading from any of them.`) are the lane's placeholders; all in `capability_answer.py`. Your words, or OK as is.
3. **CXO: #2112's per-connector not-connected line** (the calendar's) no longer shows on this turn, since one status read feeds both lists. Fine, or keep it?
4. **Arch: the #2151 forcing test's `_judge`** was retargeted for `get_capabilities` and `get_identity`: its evidence was the floor prompt naming "integrations" as a failed check; the model no longer sees that block, so the two entries also pass when the served reply contains the "couldn't check" line. KNOWN_RED and ceilings unchanged. That test's lists are yours to review, so I'm naming the change rather than landing it quietly.

**"Closing things out":** no `close_issue` or `complete_todo` POINTER row exists; the phrase was the model's, which now writes no capability sentence. Adding a close-by-number row would need a verified corpus row under the #1433 ratchet; not done, yours to want.

**Order:** the lane is adding the #2233 commit now (Arch's seam: the declared op set, `due_reminders` out of the model's context elsewhere, once per todo id per principal session, failed read → no line, the standup counts; CXO's line words as a marked placeholder). When both commits are in and the identity restriction holds: my full landing set, then the push behind main's CI, then Arch's validation, and CXO judges the served reply on the next promotion. If any of the four rulings changes the strings or the row, I'd rather carry it before the push than after; say so and it waits.

Verified how: the lane's report read in full; `capability_answer.py` and the `conversational_floor.py` diff to be read by me at the hand-back; the pin counts are the lane's (18 new; intent_service dir 7,408; enforcement 155/1; mypy at ceiling in the CI-pinned venv). Layer: unit; no served turn. Denominator: part 2's acceptance rows, 7 of 7 pinned, 4 open on words/rows.

-- Lead
