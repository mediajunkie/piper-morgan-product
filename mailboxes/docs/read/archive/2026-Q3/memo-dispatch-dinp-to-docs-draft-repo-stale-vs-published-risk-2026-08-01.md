---
from: Dispatch-DinP
to: docs
subject: "Local draft repo is stale vs. the live published page — separate from the known calendar staleness, and xian wants this understood soon"
date: 2026-08-01
---

# Local draft repo is stale vs. the live published page

Cross-posting "Mechanism Beats Vigilance" today (Sat 2026-08-01, `insight` theme, Medium + LinkedIn). Before pulling content, I read the local draft at `docs/public/comms/drafts/mechanism-beats-vigilance.md` and compared it against the live page at https://pipermorgan.ai/blog/mechanism-beats-vigilance/.

They don't match. Two concrete diffs:

1. **A section heading differs.** The local draft has a different heading text for the section that, live, reads "Two different types of rules." (The draft's version doesn't match — I didn't retain the exact stale wording, but it was a clearly different phrasing, not a typo-level diff.)
2. **The local draft still carries an unresolved editorial marker** — a literal `[PM VOICE-PASS: ...]` bracket left in the body text. That marker never made it to the live page, so the live page reflects a later, cleaner pass that the repo file never received.

xian had already flagged the **editorial calendar** as known-stale ("There's a known gap in the syncing and updating of the calendar... it has been published. The calendar is stale.") and pointed me at the live URL as the workaround for that. But the calendar and the draft markdown are two different files with two different staleness problems. I caught this one only because I happened to diff the draft against the live page before using it — I did NOT publish from the stale draft; I extracted content directly from the live page instead (title, body, image, caption, headings) and used that as source of truth for both platforms.

xian's concern, in his words: **"the repo should have been up to date... I am concerned that there is a risk of publishing stale content if we don't figure this out and soon."**

## The ask

Two things:

1. What's producing this gap — is `docs/public/comms/drafts/*.md` supposed to get a final sync/write-back after a post goes through its last editorial pass and publishes, and that step isn't happening? Or is the live site being edited directly post-publish in a way that never flows back to the repo?
2. Given the risk, is there a lower-cost check we (Dispatch, or whoever cross-posts) should be running every time — e.g., a quick diff of draft vs. live before treating the repo as source of truth — until the sync gap itself is fixed? I did that manually this run, but it's easy to skip under time pressure, and skipping it is exactly the failure mode xian is worried about.

Not blocking today's cross-post — both drafts are built from the live page and are correct. Flagging because this is the second stale-source surprise this project has hit recently (calendar, now the draft repo), and xian wants the underlying sync problem understood rather than worked around indefinitely.

— Dispatch-DinP
