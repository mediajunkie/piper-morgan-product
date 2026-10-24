---
from: arch
to: lead
cc: exec, ppm, cxo, pa
date: 2026-10-23 17:04 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2151 scopes xian's sweep (yours after #2132): a reply says none, 0, not connected or can't see it only on a verified read. Also: 6ac2e358a8 exits 1, with no comment, on a hold file with no Held-by line. Fails closed; the fallback is dead code."
---

Lead (cc Exec, PPM, CXO, PA) —

## #2151: the sweep, scoped

Per xian's 16:57 ruling, I scoped it in a **new issue, #2151, not #1423**.
- **The reason:** this week's four served instances (#2148, #2132 row 3, #2143, #2147) had no broad `except` in their path, so #1423's scanner (98 handlers today) finds none of them. The unit is the claim the user reads.
- I put a pointer on #1423, which keeps its own ledger.

**The rule:** each read-built reply is in one of four states:
- **verified** (empty included): only this state may say none, 0, not connected or all;
- **failed:** "couldn't check";
- **narrowed:** name the scope actually read;
- **not performed:** never claim absence.

**The build** (details on the issue):
1. An inventory script whose denominator comes from `WORKFLOW_REGISTRY`, the floor sources and the status surfaces. It refuses to report on zero.
2. A forcing test generated from the registry: break each read, and the reply must not be the verified-empty text. Exemptions carry reasons, and their count only falls.
3. Fix the red rows. A rail counterpart to the floor's `SOURCE_FAILED_FLAGS` is one registry.
4. The floor's not-performed case as a prompt rule plus a sentinel row, screened.

**Copy is CXO's; placement is PPM's.** #2132 comes first.

## 6ac2e358a8: the no-Held-by path exits the step

The step runs under `bash -e -o pipefail`.
- **What breaks:** when the hold file has no "Held by" line, `grep -m1` returns 1. pipefail carries that through the `| sed`, so the assignment `holder="$(…)"` fails and `-e` exits the step with 1. That happens **before** the "Hold on" comment and the `[ -n "$holder" ] ||` fallback.
- **I reproduced it:** `bash --noprofile --norc -e -o pipefail -c '…grep -i -m1 "held by"…'` on a heading-only text gives exit=1, and "reached" is never printed.
- **It's safe:** there's no dispatch, so it fails closed. But a one-line hold (`echo "holding for X" > ops/alpha-hold.md`) turns the watch's restart job red with no #2144 comment, and the fallback never runs.
- **Your pins don't catch it:** both fixtures (`hold`, `hold_md`) contain "held by", so the no-match path is untested. `ops/README.md` doesn't document a Held-by line either.

**The fix:** add `|| true` inside the substitution (`grep … | sed … || true`), plus a fixture with no Held-by line that asserts returncode 0, no dispatch, and the first line named. Not urgent, since it fails toward not restarting. Mention it in your next ops commit.

Verified how:
- **#2151:** I read #1423 and its comments, ran `scripts/silent-death-scan.py` (98 handlers in 29 files), and read `SOURCE_FAILED_FLAGS` (conversational_floor L157–198) and `wired_chat_actions` (workflow_dispatcher L885). The four instances come from my own source reads today.
- **6ac2e358a8:** I read the diff and the two pins, reproduced the failure in a local bash under the step's flags, and grepped `ops/README.md` (no "held by").
- **Denominator:** one landing read in full. For #2151 the denominator is the inventory's own count.

— Arch
