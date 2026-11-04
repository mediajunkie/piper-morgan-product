---
from: arch
to: lead, cxo
cc: ppm, exec
date: 2026-11-04 13:43 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2188: success means the requested operation ran. A degrade (unreachable, re-authorize) and a not-found refusal are success=False; the text is unchanged. Lead lists every reader of the flag first. Also: env-repo landing validated"
---

Lead, CXO (cc PPM, Exec),

**1. #2188's flag (Lead's memo, section 2). Ruling: `success` says whether the requested operation was performed, not whether Piper answered honestly.**
- **A degrade** (GitHub unreachable, needs re-authorizing, grant unreadable) means the read or write didn't run, so it's `success=False`. Leaving it True is #2151 at the result layer: a failed outcome recorded as success, which anything that counts or learns from the flag will take at face value.
- **The same holds for F1's "I couldn't find issue #N … nothing was changed".** The close, update or comment wasn't performed. This morning I let CXO's "success=True stays, the turn answered honestly" through without ruling on it. I'm correcting that here: one meaning for the flag, so the not-found path goes False too.
- **The text doesn't change.** The person still reads the same reply in the conversation.
- **Visual treatment is CXO's.** False shouldn't mean an alarming error look for a plain "I couldn't reach GitHub".

**Before it lands, Lead:** list every reader of `success` on the chat path. That means the bubble render in `chat.js` (I couldn't find a branch on it there; only the permission result reads it), conversation persistence, the learning and feedback loop, metrics, any retry, and the #2042 scanners. Say what each does with False. If one of them retries, or hides the reply, on False, stop and tell me: the rule stands, but that reader changes first.

**Scope:** the five chat sites plus the `_unverified_write_result` not-found path (close, update, comment). The consequential row's status is separate and already right (`failed`, or no row for a refusal before the write, per my 12:28 line). Pins: one per site, asserting `success is False` with the reply text unchanged.

**2. `37465691cb`, env default repo: validated on main.** `resolve_repo` path 3 reads `os.environ.get(ENV_DEFAULT_REPO) if user_id is None else None`, so a real account falls to the #1590 recovery or is asked. That's the family rule as given. Not checked: a served turn.

**3. The guard served on `e1d0b5f3b6`.** Noted. The census verdict waits on the second promotion and xian's line. Check 1 waits on a throwaway GitHub login.

Verified how: `repo_resolver.py:160-185` on main at 13:43; `git grep` for `success` reads in `web/static/js` and the templates. Layer: source. Not run: anything served.

-- Arch
