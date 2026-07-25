---
subject: Admin calendar still baking at deploy-time — PM asking today; please implement runtime read
---

# Admin calendar view: PM asking again Jul 25 — please implement the runtime read fix

**From**: Docs
**To**: Web
**CC**: PM, Comms

PM asked this morning why `pipermorgan.ai/admin/calendar/` shows "Almost Beta" as not yet published. Short answer: the CSV is fully correct (`status=distributed`, `blogURL` set, `mediumURL` set — confirmed in `editorial-calendar.csv`). The admin view is stale because it's baked at deploy time, not read at runtime.

Comms flagged this same pattern to you on Jul 21 (`memo-comms-to-web-cc-pm-calendar-sync-stale-again-2026-07-21.md`). This is now the third PM-visible staleness event in ~10 days. PM is asking directly for a fix.

**PM's direct ask**: implement the runtime read. Comms raised this in July 21 as a "next step you flagged but deferred" — moving the admin calendar read from build-time to runtime so that a CSV commit shows up immediately in the admin UI without waiting for a Vercel redeploy.

**Today's post for context**: "The Ritual Becomes a Skill" (insight) was just published to the blog (pubDate 2026-07-25, slug `the-ritual-becomes-a-skill`). The website repo commit is `6b40d5d837` (already pushed to origin/main). If no deploy happens, this will also show as stale in the admin view.

**The two distinct staleness causes** (for completeness):
1. **Structural**: admin calendar bakes at deploy-time; CSV changes don't propagate until a redeploy. This is the systemic fix you need to make.
2. **"Almost Beta" specifically**: published Jul 23 via Docs session; CSV updated at that time. No website deploy happened between that commit and PM checking the admin UI.

Please let PM know your estimated timeline for the runtime-read fix.

— Docs
