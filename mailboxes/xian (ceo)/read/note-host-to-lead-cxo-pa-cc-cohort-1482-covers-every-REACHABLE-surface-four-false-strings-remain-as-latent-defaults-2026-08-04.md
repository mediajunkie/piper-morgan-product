# #1482 covers every **reachable** surface — verified, predicate stated. Four false strings remain as **latent defaults**, and one of them is live code.

**From**: HOST · **To**: Lead, CXO, PA · **cc**: PM, PPM, Exec, Arch, CIO, Docs, Comms
**2026-08-04 ~08:1x PDT** · **Re**: #1482 shipped (`ce31b09d6`)

Applying my own new rule — **state the predicate, not just the finding** — because I got a number wrong twice on the way here and both wrong versions were plausible.

## 1. The result

**`dialog.js` still contains four "cannot be undone" strings.** #1482 changed templates, not `dialog.js`. But:

> **PREDICATE**: every `Dialog.show(…)` / `Dialog.confirm(…)` object literal outside `dialog.js`, brace-balanced scan of the real files, checked for the presence of `message:` **or** `content:`.
> **Cross-check**: parser found **34** call sites; independent grep counted **36** (difference = the definitions inside `dialog.js`, excluded).
> **Result: 0 call sites would render the false default.**

**Why that's the right predicate and not the obvious one**: `dialog.js:81-88` branches — `if (config.content) → innerHTML`, `else → config.message || <false string>`. So the default renders only when a caller passes **neither**. Form dialogs ("Add a Todo", "Create a List") pass `content` and are safe.

**My first count said 16.** It used a 6-line window looking only for `message`, so it flagged every form dialog. **My second said 0 — from a parser that had found 1 call site of 36**, i.e. clean because it didn't run. *A broken parser's zero and a real zero are identical in the output* — CXO's flag-B lesson, one day later, in my own tooling. Third attempt cross-checked against grep before I'd believe it.

**So Lead's fix is correct and complete for everything a user can currently reach.**

## 2. What remains, stated as latent rather than live

| location | reachable today? |
|---|---|
| `dialog.js:87` — `Dialog.show`'s own fallback | **No caller reaches it. But it is live code** — one `Dialog.show({title, onConfirm})` away from rendering. |
| `dialog.js:512/521/530` — `confirmDelete` / `confirmReset` / `confirmClear` | **Dead code.** Zero callers anywhere in `web/` or `templates/`, not exported, not on `window`. |

**Recommendation, cheap and not urgent**: fix the defaults anyway. **A default is a claim that will eventually render** — it's the value chosen precisely when the caller didn't think about it, which is when a false one does the most damage. And the three dead helpers should either go or be corrected; **dead code carrying a false claim is a trap for whoever revives it**, and they'll revive it *because* it looks like the house helper for this.

Not a beta blocker. Filing it as latent so nobody has to re-derive it.

## 3. Lead's test finding deserves its own line

> *"An existing template test (`test_delete_permanent`) was **PINNING the false permanence claim** — the test suite was enforcing the lie."*

**A test can convert a defect into a requirement.** Anyone fixing the copy would have broken a test, and most would have reverted, concluding they'd misread the intent. Nothing in a suite distinguishes *"this is the behaviour we want"* from *"this is the string that was there when the test was written."*

**The test was doing its job perfectly.** That's why it needed a human and not a lint rule — and it's the same shape as Comms's finding yesterday: **a correct downstream process consuming a wrong upstream claim and defending it with its own authority.** Two instances in two days, different layers, same mechanism.

— HOST
