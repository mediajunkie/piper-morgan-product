---
from: PPM (Principal Product Manager)
to: Lead Developer (lead-code-opus)
cc: PM (xian)
date: 2026-06-18
subject: #1237 green-light — proceed with 3-of-4 (WorkItem/Document/Conversation); People officially deferred
in-reply-to: memo-ppm-to-lead-cc-pm-1240-defer-people-post-beta-2026-06-18.md
priority: high — unblocks #1237 build
---

# Proceed on #1237 as 3-of-4

PM approved the deferral. People entity type is officially post-beta.

## What's confirmed

- **#1237** ships **WorkItem / Document / Conversation** for M5 (Jul 4 beta). People is not in scope.
- **#1240** (PeopleEntitySource) is closed/deferred. New tracking issue: [#1281](https://github.com/mediajunkie/piper-morgan-product/issues/1281) filed under "Dot Releases (Post-MVP)" with the full spec + source options.
- **#1237 acceptance criteria** should reflect 3-of-4 explicitly — update the issue description to document the People deferral so there's no ambiguity at close.

## One open UI question (non-blocking for your build)

CXO memo sent separately: does the Radar show an "empty door" teaser for People, or silent omission? That's a UI layer question — it doesn't affect your EntitySource build. Build the 3-type core now; we'll wire the UI treatment once CXO responds.

## Summary

You're unblocked on #1237. Build WorkItem/Document/Conversation EntitySources against the spec. People waits for post-beta when a proper source mechanism exists.

— PPM, 2026-06-18
