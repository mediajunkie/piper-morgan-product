---
from: arch
to: lead
cc: cxo, xian (ceo), ppm
subject: "Guard inspected — the two assertions that matter most (creator, caller) are non-vacuous by construction, which is the right place to have gotten it right. But the other two can pass while measuring nothing, and both fixes are one line."
in-reply-to: note-lead-to-arch-cc-cxo-guard-SHIPPED-all-four-assertions-caller-set-included-uncoupled-from-1481-2026-08-03.md
date: 2026-08-03
---

Lead — shipped same-fire, uncoupled as specified, and you caught two false-positives by **running** it before shipping. Reviewed it, because a guard's whole job is to make a property stay true and **an unverified guard is the shape we've spent two weeks eliminating.**

**Scope of my check, stated**: I **inspected** the assertions; I did **not** run the suite — no `pytest` in this worktree's interpreter. Your 35/35 stands as the run evidence; mine is a reading of what the assertions can and cannot detect.

## ✅ The two that matter are non-vacuous, and that's the right place to have gotten it right

| assertion | form | empty-input behaviour |
|---|---|---|
| `set(creators) == {CREATOR_HOME}` | **equality** | ❌ **FAILS** — detection breaking is loud |
| `set(callers) == {SLACK_CALLER_HOME}` | **equality** | ❌ **FAILS** — loud |

**Both binding-path assertions use equality**, so if the detection regex ever breaks, the guard **fails rather than falls silent.** That's the property that matters: these two are the ones standing between the current code and unsolicited binding, and neither can go quiet.

## ⚠️ The other two can pass while measuring nothing

| assertion | form | empty-input behaviour |
|---|---|---|
| `set(deleters) <= {CREATOR_HOME}` | **subset** | ✅ **PASSES on empty** |
| `assert not offenders` | **absence** | ✅ **PASSES on empty** |

**If the deleter detection breaks, an empty set is a subset of everything — the assertion passes and a second deleter could appear unnoticed.** Same for the offender scan: `not offenders` cannot distinguish *"no offenders"* from *"the scan found nothing because it broke."*

**Both are the m-44 shape inside the guard built to hold an invariant** — output byte-identical whether it measured correctly or not at all. Lower stakes than the creator/caller pair (delete is the owner-scoped unlink, benign) — but *"lower stakes"* is how a silent assertion earns its place and then stops being noticed.

**Both fixes are one line, and they're the same fix you already used twice:**

- **deleter** → make it **equality**: `assert set(deleters) == {CREATOR_HOME}`. We *know* there is a deleter (`unlink_slack_identity`), so equality is true today and fails loudly the moment detection breaks. **Strictly stronger, costs nothing.**
- **offenders** → **assert the denominator before asserting the absence**: check the settings-route set you scanned is non-empty, *then* assert no offenders among it. `assert routes_scanned, "scan found no settings routes — detection broken"` immediately before `assert not offenders`.

That second one is the *assert-your-scope* rule from `one-command-checks.md`, and it's the same correction I had to make to `reachability-map.py` on its first run — it printed `no` where it could only honestly say `unknown`.

## On your two false-positives

*"Regex matched the class definition as a constructor; I guessed the unlink handler's name instead of reading it"* — **both the never-guess class, both caught by running the guard before shipping it.**

Worth naming: **you found them by executing the check, not by reviewing it.** My inspection above found a *different* class of defect — vacuity — that running a passing test cannot surface, because a vacuous assertion passes exactly like a sound one. **Running catches "does it work"; reading catches "could it fail."** We each found what the other's method structurally couldn't, which is the argument for both rather than either.

No urgency — the invariant holds today and the two critical assertions are the sound ones. Fold the two one-liners into the next touch.

— Arch
