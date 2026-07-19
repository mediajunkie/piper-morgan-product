# Web session — 2026-07-19 (Sunday)

**Role**: Unicorn Web Designer (piper-morgan-website)
**Account**: DinP (xian@designinproduct.com)
**Model**: Claude Fable 5 (continued session)
**Trigger**: duty-cycle START fire 06:52
**Branch**: claude/condescending-jackson-c9a65b worktree → pushes to main

---

## Boot (06:52)

### Continuity from 2026-07-18 close

**Jul 18 log**: DAY-CLOSED ✓ (verified at START Step 0). Quiet weekend day, one
routine automated blog publish, no Web action needed.

**Carry-forward state** (last substantive update 7/16 evening, still accurate):
- Ship Phase B: awaiting Docs's backfill paths; PM owns the nudge, not Web
- Three PM-gated optional cleanup items, none urgent: orphaned ConvertKit scripts,
  disabled Medium RSS workflow, GH Pages custom-domain release
- Two durable lessons already in memory/notes: verification rigor, dormant-header-
  under-static-export Next.js gotcha

### Mailbox sweep
Inbox: empty (MANIFEST only).

### Website repo
Unchanged since Saturday's automated publish.

---

## Fire log

| Fire | Time | Action | Notes |
|------|------|--------|-------|
| 06:52 tick | 06:52 | START | Jul-18 close verified. Inbox zero. Website unchanged. All open threads externally gated. Holding. |
| PM | 08:29 | WORK | Remote-control catch-up: a delayed PM message from Sat 7/18 5:04pm landed — unprompted warm praise for the compose editor, specifically citing agent-discoverability of edits via git (the exact human-first-agent-aware-interfaces principle). Updated that memory with the concrete confirmed-in-practice instance rather than just filing it away. PM asked for the exact principle text — quoted it verbatim (their own 2026-05-16 words) plus the operational breakdown. PM then went AFK for the day, coordinating via Exec, asked Web to advance what's possible directly and batch questions. Advanced: (1) corrected a materially stale web-standing-items.md section — "#998 COMPOSE-UI-V1" described a FastAPI implementation (product repo) with "Phase 3 Image Upload — next"; verified that implementation never reached product main (only in abandoned worktrees) and is fully superseded by this week's actual Vercel/Next.js compose work, where image upload already shipped 7/16. Rewrote the section to reflect current reality. (2) Sent a second Phase-B nudge to Docs (checked first: no ship-related mail activity to/from Docs since 7/17, confirmed genuinely unaddressed for 3 days — safe to nudge, phrased gently in case PM's own promised follow-up happened out-of-band). Batched for PM's return, not acted on: the 3 pre-existing optional-cleanup items (ConvertKit scripts, Medium workflow, GH Pages domain) remain PM's call; also flagged the "Publishing tooling" section of standing-items (CLI B, Web GUI v2, --mode=archive) as possibly similarly stale given the compose system now live — did NOT rewrite it, less certain than the #998 case, needs PM input rather than a guess. |
| PM | ~10:xx–12:xx | WORK | **413 upload bug diagnosed + fixed.** PM hit a 413 on a routine 3.2MB image, asked why. Traced precisely: bodyParser.sizeLimit ('4mb') was measured against RAW request-body terms but my app-level check compared ORIGINAL FILE size — a 3.2MB file's base64+JSON body is ~4.27MB, exceeding the bodyParser cap before my own "under 4MB" check ever ran; the error message was also flatly wrong (promised a ceiling the transport couldn't deliver). Checked Vercel's docs directly rather than trust my own earlier "~4.5MB" estimate — they don't publish an exact figure. Fixed conservatively: MAX_ORIGINAL_FILE_BYTES=3.3MB as the real enforced limit (margin under the commonly-cited-but-unverified ~4.5MB platform cap), bodyParser.sizeLimit raised to 8mb so THIS route's own accurate message fires instead of Next's generic one for any realistic overage. Verified with REAL measured payloads, not estimates: built an actual 3.2MB random-content file, measured its true wire size (4.27MB), confirmed 200 where it previously 413'd; built a 5MB case, confirmed the new friendly message fires instead of Next's generic string. Type-check/lint/build clean, pushed + verified on origin. PM also asked "what is the exact principle" (re: the human-first-agent-aware memory update) — quoted verbatim + explained. PM said the principle is "good, capture it somewhere durable" — searched for the right existing shared mechanism rather than just re-writing my own private memory; ruled out docs/internal/architecture/decisions/decisions.log (Arch's dense backend-decision stream, wrong domain) and docs/internal/development/methodology-core/ (a much heavier system with formal Emerging→Proven promotion gates and cross-role filing-authority rules — wrong weight-class for an already-two-months-settled Web-role design tenet). Landed it in the website repo's own CLAUDE.md as a new "Design Principles" section — genuinely durable, cohort-visible, correctly-scoped. Pushed + verified. |
| PM | 12:xx | WORK | **PM approved the 3 cleanup items + asked for staleness review of Publishing tooling.** Before deleting the Medium workflow, caught something important: cross-verified via GitHub API and confirmed `.github/workflows/update-blog-posts.yml` (the file I edited THURSDAY during Phase 6, assuming it was "the still-active daily RSS fetch, kept running as-is") has actually been `disabled_manually` since 2026-04-14 — my own Thursday log entries describing it as active were factually wrong. Corrected via today's commit message rather than rewriting the closed 7/16 log. Scoped the deletion precisely: confirmed scripts/fetch-blog-posts.js itself is STILL live (wired to package.json's fetch-posts/fetch-medium, documented in CLAUDE.md) — only the dead scheduled-automation workflow file is gone, not the underlying script. Deleted all 3 (2 ConvertKit scripts + the disabled workflow), verified type-check/lint/build clean, pushed. Staleness review of "Publishing tooling": Web GUI v2 confirmed stale with high confidence (same superseded-plan pattern as #998 — the real next-gen GUI already shipped via an entirely different path) and corrected; CLI B and --mode=archive I could NOT resolve with confidence (CLI B's script still exists but whether PM has tested it is genuinely unknown to Web; the --mode=archive memo no longer exists in any live mailbox) — flagged as explicit questions for PM rather than guessed. |
| Docs | ~13:xx | WORK | **Phase B backfill: complete.** Docs applied draftPath directly to the calendar CSV for 8 of 9 ships (only #040 has no recoverable source — legitimate, same shape as the legacy-17 gap). Verified for real (checked the actual commit d87b01878, spot-checked ship #36's row) before trusting the memo. Replied: approved moving #050 to drafts/published/ for consistency (it's already published), confirmed #040's gap is expected/fine. Ship normalization is now fully resolved: Phase A live+proven, Phase B complete, Phase C deliberately deferred. Also noted (no action needed): a PPM cross-cc memo explained that my own Sunday nudge memo to Docs was briefly, silently reverted by an unrelated agent's git-plumbing bug (tree-object reuse across a re-fetch) and already restored+verified by PPM before I even noticed — informational only, Docs's reply proves the memo reached them fine regardless. |
