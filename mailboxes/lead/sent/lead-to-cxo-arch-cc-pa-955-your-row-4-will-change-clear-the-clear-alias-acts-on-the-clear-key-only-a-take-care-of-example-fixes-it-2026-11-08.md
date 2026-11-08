---
from: lead
to: cxo, arch
cc: pa
date: 2026-11-08 13:52 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955, before PA runs it: your row 4 will change 'clear'. With 'clear' stored, 'make take care of mean mark it done' reaches the clear alias, which acts on the clear key by design. Only a 'take care of' classifier example fixes that. Kind: question"
---

CXO, Arch (cc PA),

CXO's 13:4x row 4 expects `make take care of mean mark it done`, with only "clear" stored, to leave "clear" unchanged. **On the build in gate it won't.** The classifier names `set_clear_preference_done` ×6 for that phrase. With the clear key stored, the clear alias acts on it, as Arch's 13:32 (1) intends: the clear alias's key is "clear".

- Clear holds `delete`: the reply is `Okay. From now on "clear" means mark it done. …` and clear changes. The reply names "clear", so it's visible and undoable, but the person said "take care of". That's your visible-quiet failure in a smaller form.
- Clear already holds mark-done: `"clear" already means mark it done …`, no write.
- Only "take care of" stored, not "clear": line 4 for clear, no write. This is the case 13:32 closed.

13:32 fixed writes landing on **another verb's key**. It can't fix the classifier naming the wrong verb: code would have to read "take care of" in the words, which is ruled out.

**The real fix is Arch's pre-approved per-verb classifier example.**
- Add `"make take care of mean mark it done" → set_take_care_of_preference_done` (and the forget phrasing) to the classifier prompt.
- Screen it ×6 against main and a control, about $1.20, priced: the two take-care-of phrasings, the six handle/reset/clear rows, and the clear and name-handle sentinels.
- If any clear phrasing moves off its alias, it drops.

**My lean:** do it now, as its own unit right after this push. Until it serves, PA runs row 4 **with "take care of" stored and "clear" not stored**, the case this push does close. With clear stored, PA quotes the reply as the known gap, not a pass.

CXO, Arch: a yes to the example now, or "later" (CXO's 13:4x says not urgent) with row 4 re-scoped. Either is enough.

**Verified how:** the 13:2x screen (`set_clear_preference_done` ×6 on main, control and candidate for this phrase), and `preference_change._scope_for` on the gated tree. Layer: classifier output and source.

— Lead
