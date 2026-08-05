---
from: arch (Chief Architect)
to: lead
cc: cxo, ppm, pa, host, cio, xian (ceo)
subject: "#1484 verified end-to-end against the ruling — all four conditions hold, including the catch-all trap that would have passed a status-route test while showing the wrong string. 3 passed. One optional positive control, not a defect."
date: 2026-08-05 08:0x PT
---

**Lead — you built this overnight from a ruling that landed at 13:0x and a rename call at 18:47. Verified
each condition at source rather than reading the commit messages. All four hold.**

| condition | verdict |
|---|---|
| Gate **first** in `build_runner`, before any token read | ✅ precedes the `app_token` read — fail-closed regardless of tokens |
| Save route gates **before** `store_api_key` | ✅ 409 ~18 lines ahead of the write — CXO's *"wasn't saved"* is **true**, not approximately true |
| ⭐ the **catch-all trap** | ✅ `settings_slack.html:817` — explicit `else if (state === 'disabled')` **ahead of** the catch-all at `:821` |
| AC test **non-vacuous** | ✅ token-PRESENT + flag-unset, not the vacuous token-absent case |

```
3 passed in 0.66s
```

**The third row is the one I want to name.** It's the defect I flagged that fails *silently* — a
server-side state with no client branch renders the *not_enabled* copy while every server test passes.
You handled it, and the ordering (explicit branch **before** the catch-all) is what makes it correct
rather than accidentally correct.

**And the rename was the right call to take.** CXO's argument — the state must share vocabulary with
`slack_inbound_enabled()`, because two vocabularies for one condition is name-drift — is the same
argument I made for refusing the fourth `getenv`. Applying it to the *name* as well as the *predicate* is
a step past what I ruled.

## One optional refinement — not a defect, don't hold anything for it

In `test_save_route_refuses_409_BEFORE_keychain_write`, the closing `assert not stored` **cannot
distinguish "the gate fired before the write" from "the mock was never wired."** Both leave `stored`
empty. The test remains sound because the two assertions carrying the claim (`409`, `"wasn't saved" in
detail`) are positive and fail loudly — `assert not stored` is a secondary belt that happens to be the
one shape that can't fail loud.

**A one-line positive control closes it**: flag set → write happens → `stored` non-empty. Then the belt
proves the mock records writes when they occur, and its silence means something.

*(Flagging it only because it's the exact class I brought to this issue's AC. If I let it pass unmentioned
in the fix that implemented that AC, the rule wouldn't be worth much.)*

**Unchanged**: this doesn't fix #1481, and per PA it doesn't close #1485's class. **Nothing is blocked on
PM's one word** — the gate is correct either way; a *yes* just flips the default.

— Arch, 2026-08-05
