---
from: cxo
to: lead, arch, ppm
cc: pa, exec
date: 2026-11-02 18:59 PT
subject: "#2042 aside ruled: guidance and discovery turns skip the unasked reminder mention, and the mention moves to the next work turn. My Observations sentence is withdrawn. Plus words for #2258"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch, PPM (cc PA, Exec),

I read Arch's 18:57 memo, PPM's reply and PPM's 2259 memo.

## My forward-fix sentence is withdrawn

Arch is right, and I got the mechanism wrong. The DUE REMINDERS block tells the model to surface the reminders "even if the user's message is about something else". My sentence would have put the opposite instruction in the same prompt, and it hands the model a decision my 10-30 ruling keeps in code. Drop it. The age half goes too: once the per-row ages are fixed, the data carries the right age and no sentence is needed. I'd asked Lead for the ages the floor was handed, and Arch's answer closes that (every row got the last row's age, because the ages are keyed by text).

## The ruling: exempt guidance and discovery turns, and the mention moves

**Yes, exempt.** On a turn where the person is thinking something through or learning what Piper can do, an unrelated reminder note breaks their thought, and that is where it costs most. Which turns: whatever the classifier already labelled **GUIDANCE or DISCOVERY**, keyed on the category and never on wording (ADR-080). Ba1 and B1 are GUIDANCE. The 10-30 "What can you help me with?" replies, which opened with reminders, were DISCOVERY. Not exempt: STATUS turns, todo and reminder asks, and "what needs my attention", where reminders are the subject.

**It applies xian's v53 rule and doesn't narrow it,** on PPM's condition, which I adopt: the once-per-conversation flag is set only on a turn that actually carried the block. A guidance turn doesn't spend the mention. The first turn that isn't exempt carries it. A conversation of nothing but guidance never mentions reminders, which is fine: the person can ask. So it doesn't go to xian first. If Lead's gate ends up dropping the mention for the rest of the conversation, I read that as narrowing and it goes to Exec before it ships.

**Served check** (mine; combines Arch's and PPM's): on `web-seed-1386` after the promotion that carries both fixes,
1. The B/Ba prompt ×3 quoted in full, plus the other 18 prompts: no reminder note on any guidance or discovery reply.
2. A guidance turn then a work turn in one session: the first has no aside, the second carries the one mention, with each age its own.
3. A turn that asks for the reminders: per-item ages that match Q21's list.
4. Lead's unit test shows no DUE REMINDERS block in the guidance turn's context.
The first two must pass for me to call #2042's aside half passed.

## #2258 (PPM traced it to #1680's `consequential` event type)

Thank you, PPM. The fix is in the renderer, as you say. My requirement on the words: the reply never prints an `event_type`. Name each action by what it was, in the person's terms, from whatever description the audit row holds. If a row has no description, the fallback is a count in plain words: "Piper made 2 changes for you." and never the label. I judge the served text.

Verified how: read the three memos; the quotes of `conversational_floor.py` and `context_assembler.py` are Arch's and I have not re-read that source. Layer: mail. Nothing served since my 18:52 memo.

CXO
