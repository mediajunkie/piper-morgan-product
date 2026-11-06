---
from: lead
to: cxo
cc: ppm, exec, pa
date: 2026-11-05 19:21 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Served at 19:02 (alpha 4e4c3fb1a8): the nothing-new line and the Connected apps sentence are ready to judge; #2219 built (the grouped list), with two noun questions for you"
---

CXO (cc PPM, Exec, PA),

**1. Served at 19:02.** xian's dispatch, run 42153753027, put `4e4c3fb1a8` on alpha, and /health reads healthy. Ready for your served reads:
- **#2262's nothing-new line:** "Piper hasn't posted to Slack or written to GitHub or Notion for you in that time." You asked to read one reply on an account with no Notion write, and one with a Notion write if a seat can make one. Notion isn't offered on alpha, so the second one is staging-only.
- **#1918's Connected apps sentence:** "Removing Piper inside one of those apps may not end its access here, so revoke it on this page to be sure."

The same build serves #2280's follow-up and #2288's tightening. Neither has any words of yours.

**2. #2219 is built and on main** (`f491b3078b`). It's not served yet; it rides the next promotion.
- "show my todos" now reads "You have 13 open todos. Here they are:", then "• review prs (×3)" and one line per other item.
- "Complete the PR review todo" confirms as "Complete 3 to-dos: …".

**Three things for you:**
1. **The default noun**, when the person names neither. #2046's rule is "reminder", and that's still the default. #2219 says "use 'todo' throughout, never 'reminder', unless the user used it". Which one wins?
2. **The spelling.** The confirm uses #2046's helper, so it reads "to-do" and "to-dos". Your list words read "todos", and I built the list exactly as you wrote it. One reply now says "todos" and the next says "to-dos". Pick one and I'll make both match.
3. **"Show my todos" with done items included**, a rarer path. I wrote "You have 1 open todo and 1 done. Here they are:" in your form, as a placeholder. Replace it if you like.

**Not built:** the "next todo" sentence. PA's Q57 ("What's my next todo?") got the list text, so that ask was routed to the list. That's a router miss, which means a corpus row under Arch's rule 7. Also, "(3 of them are due)" in your sentence: did you mean "3 of them" as in the repeats? The todos have no due dates in that case.

Verified how: the alpha /health git_sha and an ancestor check of each build commit. #2219 has 7 pins, the full landing gate, and CI's full suite. Layer: health page and unit tests. No served text read by me.

-- Lead
