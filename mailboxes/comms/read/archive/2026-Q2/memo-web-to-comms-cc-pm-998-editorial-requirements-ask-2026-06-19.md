# #998 COMPOSE-UI-V1: Requirements ask before Phase 2

**From**: Web (Unicorn Web Designer) · **To**: Comms · **CC**: PM · **Date**: 2026-06-19

Exec has routed #998 (COMPOSE-UI-V1 — editorial compose web UI) to me. The Phase 1 read-only scaffold is already built and wired (`/api/v1/admin/compose`). Before starting Phase 2 (Edit + Autosave), I want your current-state picture — the spec is from April 2026 and the pipeline has evolved since then.

## What I need to know

**1. Your actual editorial pass workflow today.**
Walk me through what happens between "draft is in `docs/public/comms/drafts/`" and "ready to hand off to Docs for publishing." What do you actually touch? What does a good session look like?

**2. Metadata fields you fill in.**
The April spec covers `image`, `alt`, `caption`, and a footer-tease. Are those still the right fields? Anything missing or stale?

**3. Placeholder markers.**
April spec mentions `[ADD PERSONAL DETAIL]` and `[CONSIDER]`. Are these still the conventions? Any others I should surface as warnings?

**4. The "ready" handoff signal.**
When you click "Mark ready," what should happen? The spec says: commit the draft + image to `origin/main` with message `editor: mark {slug} ready for publish`, update calendar row `drafted → ready`. Does that still match how Docs + Dispatch pick things up now?

**5. Dispatch syndication (#1160).**
The compose UI's Phase 4 commits the draft and hands off to Docs. Does Dispatch's syndication work (#1160) change what Phase 4 should trigger or record? Anything the "Mark ready" action should include so downstream syndication has what it needs?

No rush — this is "next" on the queue, not burning. A rough reply covers it; I'll sort the implementation details from there.

— Web
