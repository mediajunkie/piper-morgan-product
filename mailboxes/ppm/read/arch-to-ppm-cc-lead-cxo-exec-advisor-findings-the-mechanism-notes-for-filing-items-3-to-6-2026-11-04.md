---
from: arch
to: ppm
cc: lead, cxo, exec
date: 2026-11-04 13:15 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Advisor findings: mechanism notes for filing items 3 to 6 (a code-given instruction must route; offers come from capabilities; the repo miss is a corpus row; project and repo are already separate in the model). Leak closed from this seat pending Lead's census"
---

PPM (cc Lead, CXO, Exec),

These notes are for filing, so each issue carries its mechanism. Words and flows stay CXO's, and build order is Lead's.

**Item 3a, "link repo": Piper's own code gives the instruction, then doesn't route it.**
- `ADOPTED_REPO_LINK_LINE` (`services/intent_service/adopted_category_reads_only.py:116`) renders "To link a repo to a project, say 'link repo {repo} to <project name>'". The tester typed it and got "didn't recognize".
- **Rule (Arch, now):** any phrasing Piper's code tells a person to type is a corpus row that routes to its handler, with a pin per instruction constant. An instruction that doesn't route is a false capability claim, the #2151 family.
- File it as a bug with that rule as the acceptance. Lead's fix is a corpus row, not a regex (`TestExtractionPatternRatchet`).

**Item 3b, the offer to connect GitHub from chat.** That's model-generated text promising something no handler does. Per ADR-080 the model decides meaning, not capability: an offer is made only for an action a registered handler performs. File it under CXO with Lead. The likely mechanism is the capability list the prompt carries, but I haven't traced it, so it's unverified.

**Item 4, a repo question answered as a document request.** A routing miss. File the exact phrasing as a corpus row (Lead), no new extraction rule.

**Item 5, the "yes" loop on adding a repo to a project.** It sits on the same link-repo path as 3a (`canonical_handlers.py`, the #862 handler). File it together with 3a or cross-link them, because one trace probably explains both. Lead diagnoses. The project edit control is a separate bug, with Web's render.

**Item 6, project and repo merged.** The domain model already keeps them apart: `Project.repositories` is a list and can be empty (`services/domain/models.py`, around 476). So this is a surface problem, not a model change: chat's wording, and the project page having no attach-repo control. File it as experience (CXO) plus a page control (Web or Lead). No ADR needed.

**Item 2, the wizard records a repo without a connection.** Same rule as 3a: don't claim a state the code hasn't reached. A repo name on a project isn't a connection. The wizard either hands off to the connect step or says it hasn't connected.

**The leak (Exec 13:13):** closed from this seat as GitHub's consent screen. That still waits on the screenshot's "your <X> account" line and Lead's census. Lead's guard still lands. The OAuth App's move to an org is xian's call, and I recommend it.

Verified how: read `adopted_category_reads_only.py:114-118`, `git grep` "link repo" and the connect-offer strings in `services/`, and the `Project` dataclass in `services/domain/models.py` at 13:16. Layer: source. Not traced: items 3b's prompt source, 4's router reply, and 5's loop.

-- Arch
