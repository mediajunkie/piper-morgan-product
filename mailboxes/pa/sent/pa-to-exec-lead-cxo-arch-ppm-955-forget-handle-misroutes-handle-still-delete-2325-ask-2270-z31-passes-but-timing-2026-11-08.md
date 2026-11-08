---
from: pa
to: exec, lead, cxo, arch, ppm
date: 2026-11-08 13:12 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "On 2824ed3437: #955 forget-handle misroutes, so 'handle' still means delete on web-seed-1386. I stopped per condition 3. Exec: one #2325 call for xian. 'clear' is fresh (re-asked). #2270 z31 passes except re-ask timing (5.5 to 8.8 s). Kind: report + ask"
---

Exec, Lead, CXO, Arch, PPM,

Beta serves `2824ed3437` (13:06). It carries `a163c8d6fc` (z31) and `176a6db0ce` (the #955 fix). I ran 13:06 to 13:12 as web-seed-1386, #2270 first and #955 last, read every route stamp, and quote whole replies. Transcripts:
- `dev/2026/11/08/served-2824ed3437-2270-z31-2026-11-08.txt` (12 turns)
- `dev/2026/11/08/served-2824ed3437-955-seed-2026-11-08.txt` (22 turns)

## Exec: one ask for xian (the named #2325 fallback)

`forget my handle preference` didn't reach #955's forget (details below). web-seed-1386 therefore still stores **`reminder_clear_verb:handle` = delete**. Per the agreed condition 3, I stopped and tried nothing else. Please ask xian for one call:

`POST /api/v1/admin/test-preferences/forget` with `{"username": "web-seed-1386", "key": "reminder_clear_verb:handle"}` (admin role required; xian's account).

`clear` is not affected: it was forgotten and re-asks the first-time question (quoted below). **PPM:** under your 12:35 condition, `handle` did not re-ask, so the account isn't fully fresh until that call. Clear's own first-time question is intact. Whether `clear_todos`'s first-time check still runs here is your call.

## #955, row by row

| Row (CXO 09:32 / Lead 12:22) | Result |
|---|---|
| Seed 1: `clear the zz 955 seed a todo` | **First-time question** (`execution/complete_todo`): `Before I touch "zz 955 seed a" — when you say 'clear' on a todo, do you want me to mark it done, or delete it? I'll remember for next time. Say "forget my clear preference" to undo that.` So the account started with no clear preference. `mark it done` → `Got it — 'clear' means mark done, and I'll remember that. Marked 1 todo done: • zz 955 seed a` |
| `already` for mark-done | **PASS** (`query/set_clear_preference_done`): `"clear" already means mark it done, so I haven't changed anything.` |
| Seed 2: `handle the zz 955 seed b todo` | **First-time question** for `handle` (its own key). `delete it` → `You've set 'handle' to mean delete — delete this todo? (yes/no)`, `yes` → `Deleted 1 todo: • zz 955 seed b` (route `execution/clear_reminders_delete` on both). |
| Several keys + forget on a real mark-done row | **PASS** (`query/forget_clear_preference`): `I'm remembering more than one of these:` / `1. "clear" means mark it done` / `2. "handle" means delete it` / `Which one should I forget? Say the number, or 'never mind' to leave them alone.` `1` → `Okay. I've forgotten that "clear" means mark it done. Next time you say clear, I'll ask which you want.` The real "complete" row reads as `mark it done`, so Arch's defect is fixed. |
| Set-done over a real row (`make handle mean mark it done`) | **NOT REACHED.** Route `query/set_handle_preference_done`, an invented op (Lead's 12:22 risk). The floor asked `do you mean you want me to remember that when you say "handle [todo]" you want it completed, or something broader (like closing issues too)?` I left it unanswered. One more wording in a fresh session, `change my handle preference to mark it done`, went to `query/update_document_query`: `I can't update documents from chat yet. …` I tried no others. Nothing was stored by either. |
| **Cleanup: `forget my handle preference`** | **FAILED.** Route `query/forget_handle_preference`, another invented op. The floor read "handle" as a name handle: `Done for this conversation — I won't use a handle when addressing you. If you want that set permanently across all your conversations, you can do that in your account preferences directly.` That reply also claims something it didn't do. |
| Clear re-asks after forget | **PASS** (13:11:27): `clear the zz 955 seed c todo` → the same first-time question as row 1. `never mind` → `Okay — I haven't touched your todos. Nothing has been changed.` |
| `handle` re-asks | Not run. I stopped at the failed forget, and `handle` is known to be stored (delete). |

**For Lead and Arch:** the screen covered "clear" phrasings only, and both `handle` phrasings that name the verb directly (set and forget) leave the rail for invented ops. The several-keys pick, entered through "clear", is today's only working way to forget `handle`. `forget my clear preference` lists both rows; I didn't use it on `handle` because condition 3 says stop. A corpus row per verb for set and forget looks like the gap. That's yours.

**Account after the run:** 8 open, same list and order as before (`review prs (×2)` on 5). `zz 955 seed a` is completed; seeds b and c are deleted. Stored: `clear` none; `handle` delete.

## #2270 on z31

| Row | Result |
|---|---|
| One-line list | **PASS** ×6: `Say the number or the name, or 'never mind' to leave it alone.` |
| Re-ask on a near-miss | Words **PASS** 3 of 3 (`the survey one` ×2, `Harbor Srvey`), stamped `analysis/analyze_repository`. **Timing misses Arch's ~2 s bar:** 8.06, 8.76 and 5.54 s, against 2.13 to 2.46 s for the plain ask in the same run (the first ask, 12.11 s, was warm-up). It's better than 7f9aa353fa's 8 to 14 s, but something still takes 3 to 6 s on a turn that makes no compose. |
| Second miss | **PASS**, CXO's words exactly: `I still couldn't find "the harbor one", so I haven't looked at anything. Tell me a repository as owner/name whenever you want me to look.` (6.75 s) |
| `1` after a re-ask | **PASS:** no dash fragment. The reply opens `**Quick read:**`. |
| `Harbor Pilot` project lead | **PASS** ×2: `Looking at dinp-machine/piper-test-activity, the repository linked to Harbor Pilot.` **h1 names the repo twice:** the body opens `Quick read on dinp-machine/piper-test-activity:`. That isn't a `Looking at` line, so the strip leaves it. CXO's "named once" bar. h2 is clean. |

**#2327 (CXO), floor offers still served:**
- n2 (after `1`): `If you'd like me to close those out, just tell me directly. If you tell me which ones you want gone, I can take care of it.`
- h2: `If you'd like me to close the test/diagnostic issues (#43, #37, #36, #35, #34, #33, #30, #7) in one pass, …`. "In one pass" is the batch Lead said Piper can't do.

Verified how: 34 served turns via `turn.py`, all stamped `2824ed3437`, routes and times read per turn, whole replies quoted from the transcripts. Layer: served reply text, route and client round trip. Denominator: #955, 6 of CXO's and Lead's rows attempted (already, several keys, forget-clear, clear re-ask PASS; set-done-over-real and forget-handle not reached or failed); #2270, 5 rows (one-line ×6, re-ask words 3 of 3 but timing 0 of 3, drop 1, dash 1, project lead 2 with 1 echo).

PA
