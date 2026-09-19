---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
date: 2026-09-19
subject: `integration-reveals-all` workDate is a placeholder, not a blank — narrowed from "do you recall?" to one yes/no
---

# The ask, first

**Was `Integration Reveals All` worked on around the week of 2025-05-26 — most likely 2025-05-27?**

Yes/no/close-enough is all I need. If you'd rather not guess, say so and I'll blank the field
instead, which is at least honest (see the last section).

This has been sitting on my standing items since it was handed to me as "no dateline, no chatDate,
nothing derivable — PM recall only." That framing was right that it isn't derivable, but wrong in
one way that mattered: **the field isn't empty. It's wrong.** That makes it invisible to any
find-the-blanks sweep, which is probably why it sat.

# What's actually true

`data/blog-metadata.csv`, row `integration-reveals-all`: `workDate = 2025-06-27`, `pubDate =
2025-06-27`. Identical. The row hasn't been touched since the original archive import (`58da3dd`,
"Import full blog archive - 164 posts restored") — so the workDate was never derived; the import
copied pubDate into it.

**It is the only row in the corpus like this.** Of 396 posts:

| | count |
|---|---|
| `workDate` == `pubDate` | **1** (this post) |
| `workDate` != `pubDate` | 395 |
| `workDate` empty | 0 |

And the direction is unanimous: **395 of 395 have workDate strictly *before* pubDate**, minimum lag
2 days, median 22. So `workDate == pubDate` isn't merely unusual — it's a value the corpus never
produces. That's what makes me confident it's a placeholder rather than a real same-day post.

*(I checked `chatDate` too, since it was cited as evidence of underivability — it's empty on 277 of
396 rows, so its absence here is ordinary and tells us nothing either way.)*

# Where the date estimate comes from

This post is the **oldest in the blog** by pubDate (2025-06-27). The earliest workDate anywhere in
the corpus is **2025-05-27**, and the next posts published after this one carry workDates of
2025-05-28 and 2025-05-29.

So: certainly before 2025-06-27, and almost certainly in the same late-May cluster where the
project's written record starts.

⚠️ **Stated as the weak link it is**: publication order is only workDate-monotonic in 74% of
adjacent pairs, so "it published first, therefore it was worked first" is a tendency, not a rule. I
am not treating it as proof, which is why this is a question to you and not an edit I made.

# It's also visible on the live site — verified in a browser, with a control

`BlogPostCard.tsx:126` renders the labeled pair only when `workDate !== publishedAt`; otherwise it
falls through to a single bare date (line 135). Since this row's two dates are equal, it takes the
fallback.

Observed live on `pipermorgan.ai/blog?page=16`, target against the ten other cards on the same page:

- **Every control** — two `<time>` elements: `Work: May 28, 2025 • Published: Jul 1, 2025`
- **This post** — one `<time>` element, unlabeled: `Jun 27, 2025`

So the blog's oldest post is the one card in 396 missing the Work/Published treatment. Cosmetic and
minor, but real, and it's a consequence of the data rather than a separate styling bug — fixing the
date fixes the render.

**Not claimed**: I saw a sorter in `blog-utils.ts:19` keyed on `workDateISO`, which *would* mean a
wrong workDate also misplaces the post in ordering — but the position I actually observed is
consistent with pubDate ordering instead, so I have not established which sorter this view uses.
Flagging it as unverified rather than asserting it.

I also nearly reported "this post renders with no date at all" — my first check tested for the
string `Published:`, which only exists in the labeled branch, so the bare date read as absent. The
control row is what caught it.

# What I'd do with each answer

- **You recall a date** → I set it, regenerate `medium-posts.json`, verify the card renders the
  labeled pair like every other post.
- **You don't** → I'd rather **blank the field than leave a wrong one**. A blank is honestly
  missing and will show up in any future sweep; `2025-06-27` is a wrong value wearing a correct
  value's clothes, and it has already cost one round of "nothing derivable here."

Your call on that second one — it's a content-truthfulness question, not a code question, so I'm
not making it unilaterally.

**Verified how**: `data/blog-metadata.csv` read directly and parsed with `csv.DictReader` (396 rows,
full-corpus comparison, not a sample); `git log -S` on the slug for provenance; live Playwright
render against `pipermorgan.ai/blog?page=16` comparing the target to ten controls on the same page;
`BlogPostCard.tsx:126–136` read for the mechanism. **Not verified**: the true workDate itself, which
is exactly what I'm asking you, and the sort-order consequence, flagged above.

— Web
