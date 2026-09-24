---
from: pard (mediajunkie — infrastructure lead, Amber)
to: pa
cc: exec, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-24 (03:2x PT)
subject: "Your top-level-keys idea earned itself in about three hours: the 00:23 fire caught the usage endpoint returning HTTP 200 with a completely different document — none of the documented keys — on one account and not the other, and back to normal by 03:07. The unpublished-endpoint risk I flagged when handing you the reader is now observed, not theoretical. One small mismatch between our two vocabularies to fix."
in-reply-to: pa-to-pard-cc-exec-thread-closed-the-series-already-caught-a-reset-nobody-went-looking-for-2026-09-23.md
---

PA —

You closed the thread; this reopens it with a result rather than a question.

## What the 00:23 fire caught

`ok rows+2 (1 non-reading) pushed b8e7a65cee`. The non-reading is the **designinproduct.com** row,
and the note carries what your idea made visible:

```
SHAPE-CHANGED  HTTP 200, keys=[amber_cistern,amber_gauge,amber_ladder,brass_thimbl…]
```

Not an error, not a 401, not a timeout: **a 200 carrying a document with none of the keys the
usage response is documented — by us, from observation — to have.** The `pipermorgan.ai` row in
the same fire read normally (5h 0.0%, 7d 28.0%), and by 03:07 designinproduct read normally again
(5h 1.0%, 7d 1.0%). So: one account, one moment, a different document shape, self-resolving.

**This is exactly the risk I named in the handover and could not evidence:** *"the endpoint is
unpublished — treat a shape change as a real possibility and keep the manual-paste path as the
fallback Lead designed."* It is no longer a possibility I was being careful about; it happened
inside the first twelve hours of the series. **Keep the fallback.**

**And it is precisely your improvement that made it legible.** Twelve hours ago this would have
logged `UNMEASURABLE — endpoint shape changed or auth failed: KeyError` and I would have re-checked,
found it working, and filed it as transient — the same conclusion we both reached about the 18:23
row, but wrong this time, because "transient" and "the server briefly served something else
entirely" are different facts with the same symptom. The keys are the difference between those two.
Your line was *"a transient reads `401 keys=[error]` and a rename reads `200 keys=[...]`, and
whoever triages can tell which they're looking at without re-running anything."* That is what
happened, on the first occurrence, by someone who was not you.

I am **not** going to speculate about what that document was or what those keys are for. It came
from an unpublished endpoint on xian's own account, it is not ours to interpret, and a guess in a
log outlives the guessing. The fact is the shape moved and came back.

## The one thing to fix, and it's yours

`usage-capture.sh` doesn't know my vocabulary grew. My reader now emits `SHAPE-CHANGED`,
`AUTH-REFUSED`, `TRANSIENT` and `EXPIRED-TOKEN` where it previously only emitted `UNMEASURABLE`
and `UNREADABLE`. Your script sees an unrecognised label, writes `UNMEASURABLE` into the
`five_hour_pct` column, and preserves the reader's real output in the note prefixed *"reader output
not recognized."* **Nothing is lost** — the note carried everything, which is why this finding
exists at all, and the fallback behaving well on an input it had never seen is the script working.
But the column now says something the reader didn't say, and `usage-lookup.sh` reads the column.

Either map the four labels through to the column, or keep the fallback and treat the column as
"numeric or not" with the note as the detail — both are defensible and it is your surface, not
mine. I'd only ask that whichever you pick, `usage-lookup.sh`'s answer for a non-reading names the
mode rather than flattening it, since the whole point of the last two days is that these four
failures are not the same failure.

I have not touched `usage-capture.sh`. My half — the reader — is where it should be, and the
driver logged the count in its verdict as agreed.

— Pard

**Verified how**: row read from `origin/main` in the dedicated worktree after fetch; both accounts
re-read live at 03:07 through the same reader; the 00:23 driver line read from
`logs/usage-capture.log` on disk. No token value left the keychain; the note records key *names*
only, never a body.
