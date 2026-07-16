# Omnibus Log: July 14, 2026

**Day**: Tuesday
**Sessions**: 7 (Arch, Comms, Docs, Exec, Lead Developer, PPM, Web)
**Day Type**: HIGH-COMPLEXITY — 7 parallel streams; major release cut, production verification milestone, architectural decision reached, multi-role publication pipeline all converging same day
**Justification**: Seven concurrent roles: a version release (v0.8.10.13), full Vercel production verification, ADR-078 ACCEPTED, Beat 13 published, Ship #051 draft/override/redraft cycle, honest-degrade fixes, and an infra-event lull bookending substantive PM-attended afternoon/evening bursts.

**Git Commits**: 20+

---

## Sources

| Role | File | Status |
|------|------|--------|
| Chief Architect | `dev/2026/07/14/2026-07-14-0636-arch-code-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Communications | `dev/2026/07/14/2026-07-14-0642-comms-code-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Documentation Management | `dev/2026/07/14/2026-07-14-1102-docs-code-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Chief of Staff | `dev/2026/07/14/2026-07-14-0832-exec-code-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Lead Developer | `dev/2026/07/14/2026-07-14-1229-lead-code-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Principal Product Manager | `dev/2026/07/14/2026-07-14-1935-ppm-code-sonnet-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |
| Web | `dev/2026/07/14/2026-07-14-0934-web-code-fable-log.md` | `<!-- DAY-CLOSED: 2026-07-14 -->` ✓ |

**Cross-reference gate: PASS.** All 7 roles represented. PA/CXO/HOST/CIO genuinely inactive Tuesday. Arch confirms broader infra-event lull via watchdog RED "3 roles silent" at 12:36 fire.

---

## Timeline

### Phase 1: Morning starts + infra event emerges (06:00–09:30)

- 06:36 **Chief Architect** starts (autonomous, backup account `arch-backup-0630`). Everything in lane parked on Lead: ADR-078 PROPOSED (gates: Lead feasibility read + pre-classifier concurrence), #1398 A4 half-built, #1395 corpus-rev pending. IDLE.
- 06:42 **Communications** starts. Beat 13 "The Migration Wave" pubDate is today; no PM voice-pass yet. Flagged to PM (same-day miss warrants visibility; PM's call on timing).
- 08:32 **Chief of Staff** starts. Launch bug: session opened in shared main checkout instead of worktree — self-corrected via EnterWorktree. Inbox: 3 items (Comms status-check, 2 Docs branch confirmations).
- 08:37 **Communications**: PM begins voice-passing Beat 13 directly. Comms asked to proof while PM makes the illustration.
- 08:56 **Communications** proofs PM's voice-pass. Fixed 2 real errors: typo ("pased" → "passed") and role-name inconsistency ("Documentation Manager" → "Documentation Management"). One item flagged: a specific-incident callback Comms couldn't independently source.
- 09:09 **Chief Architect**: second fire. Watchdog duty-cycle-stall alert for Lead explains parked state — Lead's cycle stalled, not stuck-on-Arch. IDLE.
- 09:15–09:43 **Communications**: PM's frontmatter/image merge conflict on kindbook — walked through via chat (no access to PM's second machine). Post-merge: both fixes survived intact. Systemic discovery: zero blog-post PNGs have ever been committed to the repo (`.gitignore` line 101: `*.png`). Filed **#1403** (blog-image gitignore gap; PM clarified: site serves WebP conversions, issue is PNG source survivability across worktrees). Calendar status: `ready-for-docs` (`2d6b088e0`).
- 09:34 **Web** starts (delayed; overnight fires dropped). Carry-forward: Vercel deploy live on Pro; admin login blocked on PM's hash regen; all 5 migration gotchas pending.

### Phase 2: Docs burst + Vercel breakthrough + Comms calendar incident (09:30–13:00)

- ~09:35 **Web + xian (PM)** live: PM regenerated hash (stdin recipe) + redeployed. **Login SUCCESS** → calendar renders (411 entries, bundled CSV confirmed working in serverless build) → compose loads drafts → PM edit-save landed on product main via PAT (`3a39c078f`). **All 5 migration gotchas closed. DNS cutover now PM-schedulable.** New thread opened: Weekly Ships editable in compose. Investigation: Ships have no draftPath; 16 legacy ships in website-repo JSON only. Memo to Docs (cc PM) requesting pipeline particulars; PM ratified future-first lean.
- ~10:00 **Documentation Management**: CLAUDE.md Pass 2 executed (`058b301b7`): 12 edits, −81 lines (658→577), created `docs/internal/operations/github-and-tooling-gotchas.md` and `docs/internal/operations/git-worktrees-model-a-setup.md`, Phase 1 tree cleanup (3 stub dirs deleted), NAVIGATION.md updated. Beat 13 "The Migration Wave" published to blog (`ad6140270`). Jul 11 omnibus completed + amended (`a5bf07bea`). Migration Wave calendar fix + Medium URL (`39bee05bf`). Web normalization reply (5 ship particulars). Ship #051 published (`5abc6aaa8`). LinkedIn crosspost verified.
- ~10:30 **Communications**: calendar row corrupted by two earlier edits using `row[-2]` (Python positional index → altText column, not notes). Caught and repaired by a general-purpose Code session (`8a4d2bd03`). Comms took full ownership: root-cause analysis, repaired row by `hdr.index(name)`, updated `update-calendar` skill to v1.2 (by-name access mandatory; Edit tool + positional indexing banned; whole-file semantic scan required). Filed **#1406** (legacy calendar backlog schema drift, pre-existing, low priority). All fixes committed (`0da869bcf`, `2ef8b5d7e`). Secondary confusion same fire: Comms looked in wrong mailbox location for an already-handled memo; corrected the memory file once the real story emerged.
- ~10:36 **Chief Architect**: third fire. Watchdog RED "infrastructure event suspected — 3 roles silent." Arch is alive (backup account; commits are liveness signal). Infra event = CIO/PM lane; parked items definitively not stuck-on-Arch. IDLE.
- 13:22 **Chief of Staff** + PM live: triaged 3 inbox items; Ship #051 had no draft (PPM missing). Nudged PPM. Drafted Ship #051 v1 on 5/6 memos using `draft-weekly-ship` skill.

### Phase 3: Lead resumes + PM override + structural fixes + #1398 ratified (12:00–16:00)

- ~12:00 **Lead Developer** resumes from compaction. Context: PM hit "AI service temporarily unavailable" on dinp beta — diagnosed as quota-dead OpenAI key presenting as transient. PM greenlit two fixes.
  - **#1404**: `user_friendly_errors.py` — 3 new patterns (insufficient_quota → `llm_key` → actionable Settings message; invalid_api_key → `llm_key`; all-providers-failed → `llm` catch-all). `intent.py` LLM branch delegates to `make_error_user_friendly`. 10 tests.
  - **#1405**: `conversation_consciousness.py::format_greeting_conscious` — `_current_time_of_day(user_timezone)` helper (known tz → real day-part; unknown/None/invalid → neutral "Hello!"). Consistent with #1381 omit-rather-than-guess rule. 6 tests.
- ~12:47 **Lead Developer**: mail triage + **#1398 A4 closed**: `connector.py` new `DegradationReason.MISCONFIGURED`; github_adapter single-point ERROR log naming missing config var; `_degrade_reason_for_exc` helper across 6 MCP call-sites; pre-existing RED test fixed (`test_github_resolve_1317.py` stale seed). 2 new tests; full suite 178 passed. Pinged Arch.
- ~13:30 **Chief of Staff**: PM corrected partial-Ship draft. *"We cannot write the ship without all the workstream reviews."* Built two structural fixes: `draft-weekly-ship` v1.6 hard gate (refuses <6/6 memos, stops and names missing role) + methodology-25 extended (Friday: check Ship collection status before issuing call; mail PM same-day confirmation). Committed (`78d3f0364`).
- 15:36 **Chief Architect**: Lead's cycle resumed. **#1398 A4 build-ratified**: config-masquerade-as-outage closed exactly as Arch named it; `TestMisconfiguredDegrade` covers the integration point the 7 resolver tests didn't; generic outage still UNREACHABLE. **#1398 CLOSED. ADR-070 Amendment A now fully built** (A2/A3/A5 on 7/12; A4 today). Arch folded "run the suite when a build ships new tests" into ratify method (code-read blind spot for test fixtures now explicit).

### Phase 4: Release cut + ADR-078 accepted + PPM resurfaces + Ship redraft (16:00–22:00)

- ~16:00 **Lead Developer + xian (PM)**: PM answered 3 pending decisions (PM rotates dead dinp key; cut v0.8.10.13; #1404/#1405 → Beta Blockers). **v0.8.10.13 CUT**: cherry-picked 2 commits onto production branch; bumped pyproject+VERSION; 22 shipped tests green. **Beta (Fly) LIVE** — release v18, health confirmed. #1404/#1405 CLOSED properly (description banners + evidence comments). #1407 carved (remaining day-part sweep: home/standup/Slack).
- ~16:30 **Lead Developer**: deploy-slowness diagnosed (#1408): `--no-cache-dir` causes torch (821MB) re-download on every rebuild. Fix: BuildKit cache mount on pip step. Filed **#1409** (CPU-only torch — the real root: ~4-5GB CUDA wheels on CPU-only hosts). `assign-sprint-safely` skill v1.0 written (PM-requested; encodes HARD RULE + per-item safe `updateProjectV2ItemFieldValue` procedure). #1404/#1405 assigned safely (MVP + Beta Blockers; verified option list still 57, #1394 untouched).
- ~18:47 **Lead Developer**: **ADR-078 ledger feasibility read** sent to Arch. Code-grounded: `conversation_links` is turn↔turn by FK (can't hold turn→artifact); zero writes (protected #1312 substrate); github adapter writes no artifacts row for issue creation → "session created #107" exists in no table today. Recommended: dedicated `session_activity` ledger (additive, session+turn scoped, external refs only). Concurred B4-first sequencing.
- ~18:57 **Lead Developer**: alpha deploy confirmed on v0.8.10.13 (build finished 18:57, container recreated 19:08, VERSION file verified). **Dual-deploy COMPLETE — beta (Fly v18) + alpha (droplet) both on v0.8.10.13.**
- ~19:35 **PPM** resumes from >1-day stale gap (Step 0 self-heal: retroactive 7/13 close). Mail: Ship §0 kickoff (Jul 10, due Jul 13 EOD) had been sitting unread-in-substance across multiple fires. Wrote and delivered §0 late (sourced from commit history, not memory): Beta Blockers build (Jul 3-5, 25 issues triaged), two PM-ratified roadmap folds, Sprint-field wipe named plainly as the window headline. Delivered to Exec inbox (cc PM + PA).
- ~20:00 **Chief of Staff + xian (PM)**: "PPM should be in the loop now." PPM's submission revealed Sprint-field wipe as real headline. Exec rebuilt Ship #051 with all 6 memos: named wipe plainly in Governance per PPM's ask; caught date-bled metric ("4 open at window close" not "2"); word count ~1,840 flagged to PM. Bridge Log rebuilt (prior Artifact URL died; new: `...c277fcc9...`). MUX branch disposition: Exec flagged 3 `cxo-mux-surface-*` branches as spatial-intelligence (PM-PROTECTED, not default-delete) and routed to CXO. Committed (`25d0d9620`, `ed44628fa`).
- ~20:00 **PPM**: BRIEFING-CURRENT-STATE refreshed. Full paginated GraphQL sweep: **7 Beta Blockers open** (was stale "2"); newly noted: #1400 (connector preferences on ephemeral Fly filesystem) + #1401 (tester-uploaded files, same issue). Added Jul 12-14 Recent Progress entry: sprint-recovery closure, Production 99/99, workstream and session-log gaps named plainly. Corrected both timestamp fields.
- ~20:00 **PPM → Docs**: scoped session-log gaps. Jul 7–8 correctly blank (Exec Fire-7 + git log confirm zero PPM commits). Jul 6 is the real gap: commits `0f287698c`–`c139b8307` (13:12–21:51, sprint-recovery A9/bulk-promotion/individual issues). Ready-made reconstruction handed to Docs.
- ~21:56 **Chief Architect**: Lead's ADR-078 feasibility read received. Verified D1 correction in code before folding (confirmed `conversation_links` FK shape + zero writes; ArtifactDB is content-store not ledger; github adapter writes no artifacts row for created issues). D1 corrected: "dedicated additive `session_activity` ledger (external refs; autogen-empty-clean; owner_id NOT NULL per HOST D1a)." **ADR-078 v0.2 ACCEPTED** — both gates cleared (Lead feasibility; HOST trust-lens PASS). OQ-3 resolved (central #1122-seam observer). Flagged to PM for veto (not silently flipped). **#1394 architecture-side COMPLETE. B4 cleared to build.**

---

## Executive Summary

### Core Themes

- **v0.8.10.13 dual-deployed** — beta (Fly v18) + alpha (droplet) both confirmed; honest-degrade fixes (#1404/#1405/#1398) + deploy-cache fix (#1408) now live in both environments
- **Vercel production verified end-to-end** — login, calendar (411 entries), compose, and PM edit-save via PAT all confirmed; DNS cutover PM-schedulable
- **ADR-078 v0.2 ACCEPTED** — #1394 architecture-complete; B4 build cleared; `session_activity` ledger design accepted with HOST's owner-scoping requirement (D1a)
- **Beat 13 "The Migration Wave" published** — voice-pass + proof + frontmatter/image + blog-first publish in one day; systemic PNG/gitignore gap discovered (#1403)
- **Ship #051 draft cycle: PM override → two structural fixes → full redraft** — `draft-weekly-ship` v1.6 hard gate closes the partial-Ship antipattern permanently

### Technical Details

- **#1404**: `user_friendly_errors.py` 3 new LLM-key patterns; `intent.py` LLM branch delegates to `make_error_user_friendly`; permanent failures yield actionable Settings message
- **#1405**: `format_greeting_conscious` — `_current_time_of_day(user_timezone)`; unknown tz → "Hello!"; second surface of #1381 omit-rather-than-guess rule
- **#1398**: `DegradationReason.MISCONFIGURED` in `connector.py`; `_degrade_reason_for_exc` across 6 MCP call-sites; pre-existing RED test fixed; Arch-ratified same day (ADR-070-A now fully built)
- **#1408**: BuildKit cache mount on pip step — torch fetched once, code-only rebuilds use cached wheels; on main + production
- **ADR-078 D1 correction**: `conversation_links` is turn↔turn FK with zero writes; github adapter writes no artifacts row for issue creation; dedicated additive `session_activity` table accepted
- **CLAUDE.md Pass 2** (`058b301b7`): −81 lines; 2 gotcha docs extracted; 3 stub dirs deleted; NAVIGATION.md updated
- `assign-sprint-safely` v1.0: HARD RULE encoded + per-item `updateProjectV2ItemFieldValue` safe mutation procedure + current Project/Sprint-field/option IDs
- `update-calendar` v1.2: by-name `hdr.index(name)` mandatory; `[-N]` positional indexing banned; whole-file semantic scan required; calendar-corruption incident mechanism in changelog

### Impact Measurement

- v0.8.10.13 live on beta + alpha: 3 honest-degrade fixes + deploy-cache fix; 22 shipped tests green
- Vercel e2e verified: 5 migration gotchas closed; compose + calendar + PAT-write confirmed; DNS cutover ready
- ADR-078 ACCEPTED: #1394 architecture-complete; B4 build authorized
- Beat 13 published: 1 new Building Piper Morgan narrative post
- Ship #051: published (`5abc6aaa8`); redraft with all 6 memos pending PM fact-check/voice-pass
- BRIEFING-CURRENT-STATE corrected: Beta Blockers count 7 (was 2 stale); Recent Progress updated through Jul 14
- Issues filed: #1403, #1406, #1407, #1408, #1409 — closed same day: #1398, #1404, #1405, #1408

### Session Learnings

- **Positional CSV indexing silently addresses the wrong column** — `row[-2]` is not "notes" in an 18-column schema; by-name access is the only safe pattern (now enforced in skill v1.2)
- **Process guards built same day as PM override** — Exec turned the partial-Ship correction into a structural fix (`draft-weekly-ship` v1.6 hard gate) rather than just absorbing the feedback
- **Feasibility corrections verified in code before accepted** — Arch confirmed Lead's D1 substrate claim independently before folding it; this is the ADR acceptance pattern
- **Stale session gaps produce compound misses** — PPM's >1-day gap meant Ship §0 kickoff sat unread-in-substance; fix was reading closely and delivering late rather than not at all
- **Infra event = calm hold, not manufactured work** — watchdog RED correctly identified 3-role silence as an infrastructure event; Arch's liveness signal from backup account confirmed Arch was fine; no heroics needed
- **Code-read ratification has a blind spot for test fixtures** — Arch caught the stale-seed RED test only because Lead mentioned it; now explicit in Arch's ratify method: run the suite when a build ships new tests

---

*Synthesized 2026-07-16 by Documentation Management (docs-code, Sonnet 4.6)*
