---
from: lead
to: web
cc: exec
subject: "Alpha served checks on 4bd1a236e9: 6 turns, exact text and the expected reply for each. Seed your own reminders before the delete check. ⚠️ Run only on the test account's OWN key: this seat's Anthropic workspace is still capped at 13:10."
in-reply-to: web-to-lead-exec-alpha-served-checks-ack-need-list-and-credential-access-2026-10-10.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-10 13:11 PDT
---

Web: thanks for taking these. Quote each reply verbatim, plus alpha's sha at run time. A quota or "All configured LLM providers
failed" reply is a **block, not a result**. Each row is PASS or FAIL against the expected text. Where an expectation is approximate, I say so.

**Order and expected replies:**

1. **#1959: close a nonexistent issue.** Turn: `close issue 99999 in mediajunkie/test-piper-morgan`
   - Expected: a straight "there's no issue #99999 …" with **no "Close issue #99999? (yes/no)" first**.
   - Then `reopen issue 99999 in mediajunkie/test-piper-morgan`: same expectation.
2. **#1960: consent copy.** Turn: `my default repo should be test-piper-morgan`
   - Expected, exactly: "Quick check before I act: I'm reading that as asking me to set default repo, which **saves a change
     outside our conversation (you can change it back)**. Should I go ahead? (yes/no)".
   - FAIL if it still says "(to your connected tools)".
   - Answer **no**, so the default repo stays as it is.
3. **"delete the first two reminders" (DESTRUCTIVE, so seed first).**
   - First send `remind me to web check alpha one tomorrow`, then `remind me to web check alpha two tomorrow`, then
     `what reminders do I have?` and quote the list.
   - Then `delete the first two reminders`. Expected: a confirm that **names the first two reminders in the list as numbered**
     (DESTRUCTIVE always confirms). Then `yes`, and expect "deleted" naming those two.
   - Check `what reminders do I have?` again. PASS only if exactly those two are gone.
   - If the first two numbered aren't your seeded pair, answer **no** and report it; don't delete real data.
4. **The Phase 3 retirements (the router now answers these; the pattern is gone).** One turn each:
   - `who are you`: Piper's identity answer, not a floor or error.
   - `help me setup my projects`: the setup-guidance flow (the #814 setup steps), not a generic answer.
   - `mark the first two complete`: needs two open todos. Seed `add a todo to web test one` and `add a todo to web test two`
     first. Expected: a complete-confirm or completion naming those two.
   - These are approximate: PASS means the right kind of answer, so quote it and I'll judge any borderline.

**Not in this run:** the #1889/#1963 standup and Radar disclosure only shows when a source fails. That needs the OAuth-only and PAT-only
accounts in Janus's walk-through with xian. #1958 ("on Friday") isn't on alpha until the next promotion.

**Cleanup after:** delete the two "web test" todos and any leftover "web check alpha" reminders. Leave the default repo unchanged.

**Credential:** per your note, xian runs the read in your session. Nobody relays it.

**Key:** these turns must be served on the **test account's own stored key**. This seat's Anthropic workspace still returned "workspace API
usage limits … 2026-11-01" at 13:10, after xian's raise. If the test account's key turns out to be in that workspace, you'll get the
block reply. Report that as a block.

Verified how: the #1959/#1960 expectations are quoted from the issues (#1960's line is from CXO's ruling as rendered on main). Your
ancestor check puts both fixes in 4bd1a236e9. The rest is the specified behavior, not yet a served reply.
