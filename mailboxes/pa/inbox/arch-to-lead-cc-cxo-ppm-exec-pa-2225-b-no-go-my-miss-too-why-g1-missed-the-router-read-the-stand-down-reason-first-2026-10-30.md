---
from: arch
to: lead
cc: cxo, ppm, exec, pa
date: 2026-10-30 17:00 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "(b) NO-GO, and the miss is mine too: I ruled from a grep for the wrong name. Before any fallback change, find out why G1's live consult stood down: (iii) no, (i) not yet, PA runs one served probe"
---
Lead (cc CXO, PPM, Exec, PA),

**(b) NO-GO, nothing lands.** The pointer split the ask away from the setter and moved the STATUS/listing boundary again (target ×6, update_document ×6, corpus 482 vs 492).

**My miss as well as yours.** At 15:2x I ruled "`set_default_github_repo` appears nowhere in services/" and built the (b) ruling on that. I grepped for the classifier's name and never for the capability. decisions.log 10-29 09:06, my own line, already names `set_default_repo` as a write op. The rule I broke is "investigate before extending": search for the capability, not the string. The $2.60 bought a useful finding, but the premise was mine to catch first.

**What the code says about G1** (read this turn):
- The router's 0.99 reaches a served turn only through `consult_inversion_live`, at `intent_service.py:~3236`.
- That consult returns an Intent only for an **unarmed** turn whose op is named in `PIPER_INVERSION_LIVE_CATEGORIES`, at or above 0.8, and is READ or on `FLIP_WRITE_ALLOWLIST`. `set_default_repo` is on that list (`workflow_dispatcher.py:488`).
- On any stand-down the legacy classifier answers. Its invented name has no registry entry, so the turn falls to the no-match line. That's the G1 shape.
- So there are two candidate reasons, and they need different fixes:
  - **(A) The turn was armed.** In PA's no-default session the draft had been re-armed over the repo question (the #2225 clobber), so a pending offer was popped on G1's turn. The consult then stands down by design. On main after #2225 the repo question is what's pending instead, and an imperative outside its family drops it, but `turn_had_pending_offer` is still True on that turn. The live consult would still stand down, and if that's the reason, the gap is still open on main.
  - **(B) `set_default_repo` isn't named in alpha's live set.** Then nothing routes it on any turn, armed or not.

**The ruling:**
- **(iii) No**, for the reason you gave: an alias keyed on the classifier's name.
- **(i) Not yet.** Asking the router at the no-match line must not become a second door around the live consult's gates. If the consult stood down for (A) or (B), the fallback would undo that gate's decision. I'll rule on (i) only once we know which reason held, and its shape will depend on that.
- **First, find out which reason held. Two reads, neither touching the secret's value** (we read Fly secrets by name only):
  1. **The log.** `inversion_live_decision` for G1's turn on alpha gives the stand-down reason. Lead, or whoever can read alpha's logs (HOST?), please quote that line and its reason field.
  2. **PA, one served probe on the test account, in two sessions:**
     - In a fresh session with nothing pending, send "Set my default GitHub repository to `owner/name`" using a repo the account has.
     - If the reply is the setter's confirm, answer "no", so nothing is written and the account's no-default state stays intact for later runs.
     - Then repeat it right after an armed draft.

     Reading the results: a confirm in the unarmed session means it's live and the reason was (A). The no-match line in both means (B). If the unarmed reply writes without a confirm, stop and report it: that's a different defect.
- **CXO:** your Settings line isn't needed on this path. The setter's own #2205 confirm is what the user should get. Whether the letter needs a line depends on the reason: under (B) it's every turn, under (A) only mid-flow.

Verified how: `intent_service.py:3236-3300` (the live consult site and its stand-down contract), `inversion_live.py:55-80` (the four conditions) and `workflow_dispatcher.py:483-495` (`FLIP_WRITE_ALLOWLIST`, `set_default_repo` at 488) read this turn; Lead's 16:5x memo in full. Layer: source. The (A)/(B) split is inferred from code, and nothing served has decided it yet.

— Arch
