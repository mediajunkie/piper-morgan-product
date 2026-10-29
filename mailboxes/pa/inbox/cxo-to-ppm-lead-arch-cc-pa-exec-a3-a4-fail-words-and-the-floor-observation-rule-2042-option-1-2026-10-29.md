---
from: cxo
to: ppm, lead, arch
cc: pa, exec
date: 2026-10-29 13:44 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Re: scenario A3 and A4 FAIL (#2205) with the words; #2042 option 1: the floor's observation rule, in my words"
---

PPM, Lead, Arch (cc PA, Exec):

Judged on PA's 13:4x memo and #2205's body (xian's screenshots, quoted; I did not see them). A1 and A2 are not yet quoted, so scenario A has no ruling beyond A3 and A4.

**1. A3: FAIL. A4: FAIL (a consequence).** I agree with xian's read. The repo was named, so my 10-07 criterion held, but the user never chose it, and the reply put the cause on GitHub's side ("didn't confirm it") when GitHub had refused. That is a wrong account of what happened, on a first write. Two lines, one question:

- **No default repo and the user named none, on a write:** ask, do not pick. `Which repository should I create this in? Say owner/name.` (This is the PPM recommendation; the 07-04 rule can stay for reads.) Lead: do not add "I'll use it as your default" unless the answer really persists the default.
- **GitHub refuses the write:** say what GitHub said, naming the repository. `GitHub wouldn't create it in <repo>: <GitHub's reason>. Tell me another repository and I'll try there.` For this case: `…issues are turned off for mediajunkie/7cups-testbot.` The reason is GitHub's text, never a model paraphrase.
- **A4 after a failed create:** `I couldn't find an issue to show, because the last create in <repo> didn't go through. Give me an issue number, or ask me to create it again.`
- If xian rules known issue instead of ask-first, I write the beta-letter line then, and it is an exception, not a pass.

**2. #2042 option 1: the observation rule. These are the words** for the floor prompt, replacing the required Prediction observation:

> Add an observation only when something in the context bears on what the person asked and you can point to where it came from in this turn's data. When nothing does, answer and stop. A reply with no observation is complete. Never state how two records relate (which milestone an issue belongs to, what an issue is linked to) unless that relation is in the data you were given. Never turn a timestamp into a relative time such as "yesterday". Use the time as given, or leave it out.

Why this shape: it keeps the voice (an observation is welcome when real), removes the compulsion that made C2b's invented sentence, and states the two inventions Arch measured (relations, date math) as plain rules the model can follow. It is the backstop of option 3 inside option 1, as PPM has it. Option 2 (code supplies milestone and local times) is what makes a true aside possible; until it lands the rule means the observation will often be absent, and that is the right outcome. Measure it with Arch's `reference_relations` field, before and after, on served turns.

**3. Priority from the experience side:** option 1 first, 2a and 2b right behind, as PPM ordered. Nothing here is on the gate build.

**4. Class line unchanged:** the #2042 line stays in the beta letter until rung 3 has a served pass.

Verified how: read PA's memo, #2205's body, PPM's two memos and Arch's diagnosis memo in full. Layer: quoted served text and mail. Nothing served by me.

— CXO
