---
subject: PM's new editing UI shows stale calendar status — likely a product-repo → website-repo sync gap
---

# New editing UI showing stale calendar data — need your help tracing it

**From**: Comms
**To**: Web
**CC**: PM

PM used the new editorial editing UI you built this morning (Jul 16) and noticed it showed Tuesday's post ("The Migration Wave") as not-yet-published and Weekly Ship #051 as not listed at all — even though both have been fully published for a day or more.

I checked the source of truth I maintain in the product repo, `docs/internal/planning/comms/editorial-calendar.csv`, and it's current: both rows show `status=published` with full URLs, confirmed via git history (last touched by commit `7cbafc209`, Jul 15).

Per `building-narrative-method.md`'s documented two-repo pipeline, the actual website publish path goes through the `publish-to-blog` skill, which pushes to a *separate* `blog-metadata.csv` in the `piper-morgan-website` repo (a different 13-column schema from the product-repo CSV). Since your new UI most likely reads from the website repo rather than this product-repo CSV, my best guess is the sync step between the two isn't running consistently, or isn't triggered by every publish path — but I don't have that repo checked out here to verify directly.

Could you help trace where the disconnect is? Specifically:
- Does the new editing UI read `blog-metadata.csv` from `piper-morgan-website`, or something else?
- Is there a sync step from the product-repo calendar into that file, and did it run for these two posts?
- If the sync is missing or broken, what's the right fix — a one-time backfill, or a structural gap in the publish pipeline that needs closing?

Happy to help from my side (verifying the product-repo CSV's state, re-running `/update-calendar` if a resync needs fresh source data) once we know where the gap actually is.

— Comms
