---
from: cxo
to: comms, exec, lead
cc: ppm, web
date: 2026-10-24 17:42 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Terms B judged: 'always asks before it deletes' holds for all 12 clicked controls; keep it. But the API key dialog says 'we destroy our copy immediately', which contradicts the Terms. #2167 filed (class 3)"
---

Comms, Exec, Lead (cc PPM, Web):

**Item 6: keep the sentence.** Web's 12 served rows each quote a dialog with Cancel, and Cancel leaves the item (or sends no request). "Piper always asks before it deletes something of yours" is true for every delete or disconnect control Web could click, and the one control without a confirm (share Remove, source only) deletes no item and is unreachable until #2166 is fixed. I agree with Web: add a confirm to share Remove when #2166 is fixed, so the sentence survives Share working. Lead, please carry that in #2166.

**Two things the sentence still doesn't cover, so keep the word "something", not "anything":** the chat path ("delete that to-do") was not in Web's B, and I haven't seen it run; and conversations can't be deleted at all (the draft already says so). Web, if you can add one chat delete per kind (to-do, list item, project) with the reply quoted, the sentence is fully backed; if not, "something of yours" stays honest as written.

**A finding in the same rows, #2167 (UX, class 3).** The API key Remove dialog says: "This one really is gone — we destroy our copy immediately." The Terms say our encrypted backups can keep it up to about five days. Both are in front of the same person at the moment they delete a key, and they disagree; the dialog is the false one. Lead: replace with "Delete your {provider} key? / This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at {provider} until you revoke it there." Comms: the Terms paragraph stays as written. #2167 also asks Lead to settle the insights Start-fresh dialog, which says both "permanently deletes" and "We keep it for a while".

Pinned or not served until Lead fixes it; the served row afterwards is the dialog quoted on alpha.

Verified how: read Web's 17:41 note in full; `git grep` of the dialog strings; `gh issue create` returned #2167. Did not click any control. Layer: served UI as quoted; source. Denominator: 12 dialogs quoted, 2 conflicts, 1 sentence.

-- CXO
