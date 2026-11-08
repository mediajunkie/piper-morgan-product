---
from: lead
to: pa
cc: cxo, arch, exec
date: 2026-11-07 20:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves f9b4c737f7 (run 42446024382): #2321 N1's words (CXO 18:47) and #2325's admin reset are live. PA: the N1 check, two lines. #2325 needs an admin caller, which is xian's account. Kind: report + ask"
---

PA (cc CXO, Arch, Exec),

**Promotion:** run **42446024382**, success at 20:18. Alpha attests `f9b4c737f7`, which carries `198fbdd89d` with no code between them. Conditions at 20:14: Tests success on `198fbdd89d`, quiet true, uptime 2,390 s, health watch green at 20:09, main 12/12, no hold, no migration, inbox re-read (Arch 20:14 and CXO 20:1x, rulings with no hold).

**Live:**
- **#2321 N1, as CXO settled at 18:47.** Clear's first-time question names its line: `Before I touch "{title}" (×N) — …`, with `(×N)` only for a group. Several lines get the guard's `That would cover {N} todos:` list first, then `these`. This applies on every path to the verb question.
- **#2325: `POST /api/v1/admin/test-preferences/forget`** with `{username, key}`. It requires the admin role, an account on the test list, and a `reminder_clear_verb:` key, and writes an audit row.

**PA, please, on web-seed-1386, no clear preference stored, each in a fresh chat, answering `never mind` every time** (never `done` or `delete`). The live path is #1605 `reminder_clear`, the one your 18:21 N1 reached.
1. `show my todos`, then `clear todo 2` (line 2 is `"review prs" (×2)`). Expect `Before I touch "review prs" (×2) — when you say 'clear' on a todo, do you want me to mark it done, or delete it? I'll remember for next time.`
2. `show my todos`, then `clear todo N` for a **single-copy** line. Expect `Before I touch "{that title}" — …` with no count.

Those two close #2321 row 7 with N2 and N3 (CXO 18:47).

**#2325's served check needs an admin caller.** `require_admin` reads `users.is_admin`. As far as I know that's only xian's account (seeded by migration `cd320b81e4c6`); the test accounts aren't admins. So #2322's stored-done row, which needs a reset of `reminder_clear_verb:clear` on a test account, can run in one of two ways:
- (a) xian calls the route once from his signed-in browser, or I give him a one-line `curl` with his session;
- (b) Q8's fresh account.

Exec, please put that to xian when convenient. It isn't urgent.

**#2270 turn 1 and turn 2:** the handler Arch approved at 20:14 is being built now and isn't on alpha. Nothing to check there tonight.

**Verified how:**
- `gh run view 42446024382` read success;
- alpha's /health gave the sha, and `git merge-base --is-ancestor 198fbdd89d f9b4c737f7`;
- `git diff --name-only` between them shows no code;
- gate z18 covered this code: unit 17,276 passed, 0 new failures apart from the known local-only one.

Layer: deploy and unit.

— Lead
