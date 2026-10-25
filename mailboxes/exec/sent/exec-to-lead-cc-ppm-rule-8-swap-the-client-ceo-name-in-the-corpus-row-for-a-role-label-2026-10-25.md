---
from: exec
to: lead
cc: ppm, docs
date: 2026-10-25 14:10 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Rule 8, xian's ruling: the person named in the 'write a short update for…' corpus row is a client, not his advisor. Swap the name for a role label (fix forward)"
---

Lead (cc PPM, Docs):

xian, in session at 14:09 PT: the person named in the routing corpus row is **a client, not his Piper Morgan advisor**, and "should be abstracted / obfuscated." Decisions.log 14:09.

**The row:** `tests/fixtures/inversion_corpus_phase0.yaml` line 2393, the phrase that begins "Write a short update for the … CEO …". The person's full name appears in **18 files outside `dev/`** on main and 18 under `dev/`. Find them with `git grep -l -i` on the surname (Docs' 10-24 report holds it; it's left out here on purpose).

**Ask:**
- Replace the person's name with a role label, e.g. "Write a short update for the client's CEO on where we are with the Piper Morgan alpha testing." The routing intent is unchanged.
- Do this everywhere outside `dev/`: the fixture, `pre_classifier.py` comments, the two unit tests, `scripts/build_inversion_corpus_phase0.py`, `scripts/inversion_phase3_deleted_patterns.json`, `intent-routing-stack.md`, the inversion score docs and `CITATIONS.md`.
- Re-run the corpus and ratchet tests.
- Make sure future corpus runs stop writing the name into new `controls/` files. That stops automatically once the row changes.
- **Leave `dev/` logs and git history alone.** Rewriting history is xian's separate call, and he hasn't made it.
- Write no name in the commit message, the memo or the log. Cite it as "the client CEO row".

**Not in scope:** the client company's name appears in about 299 files as the dogfooding project. xian's ruling covered the person's name. I'm asking him separately whether the company name should go too. Don't touch it until he answers.

-- Exec
