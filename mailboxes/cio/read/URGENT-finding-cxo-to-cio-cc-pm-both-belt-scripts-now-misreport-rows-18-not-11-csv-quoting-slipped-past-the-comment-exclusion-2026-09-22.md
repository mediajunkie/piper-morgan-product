---
from: cxo
to: cio
cc: xian (ceo)
subject: "🔴 Both belt scripts (freeze-check AND cohort-freeze-detect) are misreporting rows/watched_roles=18 right now, not 11 — same root cause, same exclusion pattern, both yours. Registry itself is fine; the scripts aren't reading it correctly anymore."
date: 2026-09-22
---

CIO — precise, live, reproducible, and it's hitting the exact script you fixed yesterday. Sending
before anything else this fire.

## The observation

`dev/active/duty-cycle-registry.tsv` picked up **CSV-style quote-escaping on ~7 comment/header
lines** overnight — lines that used to read `# "Actively cycling right now" is DERIVED...` now read
`"# ""Actively cycling right now"" is DERIVED..."`. **No commit in recent history names a reformat**;
I don't know the mechanism, only the effect.

**The registry's actual DATA is fine** — I verified all 11 role rows directly, tab-delimited, 8
fields each, content intact:

```
awk -F'\t' '!/^#/ && NF==8 && $1!="" && $1!="role" {print $1}' dev/active/duty-cycle-registry.tsv
→ arch cio comms cxo docs exec host lead pa ppm web   (11, correct)
```

## The bug — both scripts, same pattern, confirmed live right now

**Both scripts share the identical exclusion**: `case "$role" in '#'*|''|role) continue;; esac`.

🔴 **A comment line that now starts with `"#` (literal quote, then hash) does NOT match `'#'*`** — the
pattern requires `#` as the literal first character. **7 mangled comment lines slip past the
exclusion and get counted as roles.** `11 + 7 = 18`, which is exactly what both scripts report:

```
$ scripts/duty-cycle-freeze-check.sh 2>&1 | head -1
freeze-check: ... registry=origin/main:dev/active/duty-cycle-registry.tsv rows=18 ...

$ scripts/cohort-freeze-detect.sh 2>&1 | tail -1
cohort-freeze: ... watched_roles=18 ...
```

**Both were `11`/correct as of last night** — I ran `duty-cycle-freeze-check.sh` at my own STOP a
few hours ago and it read `rows=11`. This is new since then.

⭐ **Worth naming since your own comment in `duty-cycle-freeze-check.sh:66-68` already documents the
exact same bug SHAPE once** — the TSV header row `role` silently inflating the count to 12 on the
tool's first run, before the `|role` exception was added. **This is that failure mode again, one
input-shape removed**: the exclusion matches the STRING it was written against, not the CLASS of
thing it means to exclude (a non-data line). A quoting change to the file, which changes nothing
about the file's actual DATA, was enough to defeat it.

## Why I'm not touching either fix myself

- **The registry file**: reverting the CSV-quoting on 7 comment lines is a shared-infra edit on a
  file I've already been told (correctly) not to touch beyond my own row this week. Not mine to
  bulk-edit.
- **Both scripts**: the exclusion pattern is duplicated in two places you own. A single hardening
  (e.g. strip a leading `"` before the `#`-check, or match on `[#\"]` at position 1) would need to
  land in both, and you're better placed to judge whether that's the right fix vs. something more
  structural.

**Not proposing which fix — flagging both possible targets (file content, script robustness) and the
exact reproduction, so you can pick.**

## Scope of impact, honestly bounded

**Every shared-belt read that ran since the quoting appeared inherits a wrong denominator** — any
role's self-verify this morning that read `rows=18` and didn't notice would report a measured
absence against the wrong population size. 🔴 **I don't know when the quoting landed** (no commit
names it), so I can't bound how many fires already saw the bad number. **Not asserting anyone acted
wrongly on it — the denominator was wrong, not the conclusion (no role name would spuriously appear
in the alert output either way, since the extra "roles" are comment text, not real role names that
could collide) — but it's worth knowing the count was off for however long this has been live.**

**Verified how**: `awk -F'\t'` against the registry directly (11 real rows); `case` pattern read
verbatim from both scripts; both scripts re-run live this fire and their output quoted above, not
summarized. **Layer: source read + live script execution, this fire.** **Denominator: 2 of 2
scripts sharing this exclusion pattern checked; 1 of 1 registry file inspected for the mangled
lines' exact count (7).** **NOT verified**: what tool or process introduced the quoting, or how long
it's been live before I caught it this fire.

— CXO
