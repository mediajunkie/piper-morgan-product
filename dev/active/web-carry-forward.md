# Web carry-forward — 2026-08-29 (active), cron ID last updated 2026-08-29

**Session**: Amber / pipermorgan.ai, Opus 5 · cron `22 6,9,12,15,18,21 * * *` (job `a9631fd9`) · registry row `dev/active/duty-cycle-registry.tsv` line `web`

⚠️ **Trimmed 2026-08-29** — everything this file carried from 2026-08-03 through 2026-08-25 was
fully-resolved historical record (marked CLOSED/FIXED/SHIPPED/SETTLED at the time), sitting in
what's supposed to be ephemeral session state well past its own events. Compressed to one-line
pointers below (same principle `web-standing-items.md` already applies to its own "Recently
completed" section — point forward, not back). Full detail for anything referenced is in the dated
session logs (`dev/2026/MM/DD/`) and git history if ever needed again.

## ⭐ Web is the browser-automation pilot (since 2026-08-28) — "no browser on this host" no longer true

PM blessed headless Playwright on Amber (via Pard/Exec); Exec assigned Web as the pilot role.
Smoke-tested same night (08-28): `npx playwright` works, Chromium cached, launched headless,
navigated the live site, got a real title/DOM measurement/screenshot on the first attempt. Full
detail: `dev/2026/08/28/2026-08-28-0652-web-code-log.md`, STOP section.

**First real design use, 08-29**: shipped the above-the-fold blog redesign (website `b21d89e`) —
replaced the generic marketing `<Hero>` on `/blog` with the pre-existing, previously-unwired
`organisms/FeaturedPost` component (extended with a `compact` prop), populated with the actual
most recent post. Verified with a real Playwright screenshot against a local prod build, directly
compared to the 08-28 "before" baseline: post-grid section now visible at y=688 in an 800px
viewport, vs. barely peeking in before. Full diff and evidence:
`dev/2026/08/29/2026-08-29-0652-web-code-log.md`.

**Tool report (per Exec's ask)**: genuinely unblocked this fix — no way to confirm the visual
claim otherwise, which is exactly how the 08-09 partial `compact` fix shipped without catching
that the real problem was still there. No false starts (yesterday's smoke test worked out the
launch pattern already). Reported to Exec cc PM 08-29
(`mailboxes/web/sent/report-web-to-exec-cc-pm-browser-automation-pilot-first-result-2026-08-29.md`).
Open thread, not blocking: configuration is still ad-hoc (`npx playwright` invoked per-script)
rather than a settled per-repo config — worth deciding a permanent shape eventually. PM hasn't
seen the live result yet — worth an eyeball pass next time PM is on `pipermorgan.ai/blog`, but
this ships as shipped-pending-PM-reaction, not shipped-pending-PM-approval.

## ⚠️ Environment facts worth re-verifying each fire, not assuming

- **Two worktrees, two repos**: `piper-morgan-worktrees/web` (cohort infra — mail/logs/`dev/`) on `claude/web-cycle`; `piper-morgan-website-worktrees/web` (actual Web lane) on `claude/web-cycle`. Both share the basename `web` — disambiguate via `git remote -v`, not just `basename "$(pwd)"`. Confirm which one before every commit.
- **`CronCreate` jobs are session-only** — in-memory, never written to disk, gone when this session exits; recurring jobs auto-expire after 7 days regardless. My registry row says `watched`, which is only true while this session lives. If a fresh session starts, re-arm and re-verify the row rather than trusting it.
- **`mcp__chrome-devtools__new_page` still fails** (no Chrome DevTools MCP executable), but this is
  no longer "no browser on this host" — headless Playwright via `npx playwright` works fine
  (smoke-tested 08-28, used for real design verification 08-29). Use Playwright directly, not the
  Chrome DevTools MCP tools, until/unless that gap is separately closed.
- **`scripts/duty-cycle-heartbeat.sh` takes `<role>` as `$1`, not a flag** — `--help` alone is
  parsed as the role name and writes+auto-pushes a garbage heartbeat file rather than showing
  usage (hit and cleaned up 08-29, commit `7779a4d79`). Correct form:
  `scripts/duty-cycle-heartbeat.sh web work --if-quiet`.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** — can exercise failure/fallback branches locally but not the real success path for anything touching the compose API or the live GitHub-backed calendar read. Vercel has these; first real click-through after a deploy is the actual test.
- **No login credentials for the Piper Morgan product app's shared dev server** (PID 67615, port
  8001) — no self-serve `/register` (pruned per #1504), no documented test account. Anything
  needing an authenticated view of the app (todos, settings, etc.) is blocked for Playwright
  verification until either a test account or an isolated seeded instance gets provisioned. Pre-auth
  flows (login redirects, public pages) are unaffected — those verify fine. Found 08-29 during the
  In Review round; see Active threads above.

## Active threads

### OPEN, awaiting PM — piper-ship image relocation, discussed not built (2026-09-02)
PM asked (direct conversation, not mail) to show `piper-ship.webp` fully/uncropped on the Shipping
News landing page and remove it from individual Ship posts — but explicitly said "discuss first,"
since Dispatch was actively publishing this week's Ship and PM didn't want a collision.

Investigated before responding: same single static asset either way (currently OG-meta-only on
the index page, small+cropped via `object-cover` on every `ShipPostContent.tsx`); no
`publish-post.js` changes needed. Checked the actual collision risk rather than reassure blindly —
confirmed via `git log` that Ship #058's content commit landed directly in the website repo this
morning (also confirms yesterday's compose live-calendar fix worked in practice). Read: low
collision risk (disjoint files), but said plainly I don't have full visibility into Dispatch's own
automation this week, so PM's caution stands regardless of my read.

Responded with findings + one clarifying question (banner-style vs. more contained treatment). **Did
not implement anything** — PM's explicit ask was to discuss first. **Waiting on PM** for design
direction and a go-ahead once Dispatch's publish window is clear.

### CLOSED — composer 404 on new calendar rows, fixed same fire (2026-09-02)
Exec root-caused (with two honest false-starts noted) a real bug PM hit editing Ship #058: the
composer looked up calendar entries via a build-time CSV snapshot, so any row added since the last
deploy 404'd. Asked Web for a rebuild plus a judgment call: switch `/api/compose` to
`loadCalendarLive()` (already used by `/admin/calendar`/`/admin/publish-queue`) or a hybrid.

**Went with the full switch** — both of Exec's "against" arguments turned out already handled by
the existing function (same token the draft body already uses; rate/reliability bounded by its
existing 15s TTL cache, proven in prod on two other pages). Filed `piper-morgan-website#38` with
full reasoning + evidence, fixed, `tsc`/build clean, ran a real local test (no
`GITHUB_DRAFT_TOKEN` here, so this exercised the fallback path): confirmed honest snapshot
fallback reporting and confirmed the async entry-lookup finds known drafts correctly end to end.
Pushed (`fda78ca`) — one push covered both the code fix and the rebuild Exec asked for. Confirmed
the Vercel deploy actually succeeded via `gh api .../commits/.../status` rather than assume.
**One honest gap flagged in the reply**: no live admin credentials for the composer, so the exact
authenticated end-to-end scenario (opening #058's URL) wasn't independently confirmed — reported
precisely rather than either overclaim or block on access I don't have.

Reported to Exec cc Docs/Comms/PM:
`mailboxes/web/sent/reply-web-to-exec-cc-docs-comms-pm-fixed-composer-now-reads-calendar-live-2026-09-02.md`.
**Nothing further pending** unless someone with composer access wants to confirm the last mile.

Separately, `website#37` (publish should archive the source image) was filed by Exec — addressed
to Docs for a shape check, Web's to eventually build, **nothing owed today**.
CIO broadcast a new cohort-wide convention (every standing-items row needs a filed/added date) plus
a direct audit of Web's file with ready-to-paste dates and one real candidate: "Phase 4" (compose UI
mark-ready + git handoff, `#998` family) had sat 43 days undecided and wasn't on my own radar.

**Applied the dates, then verified rather than trusted**: ran `scripts/aging-standing-items.sh`
against my own file after dating it diary-entry-style (per the broadcast's literal wording) — still
showed as a COVERAGE GAP. Read the script directly: it only parses markdown **tables** with a
`Filed` header column, no inline-prose fallback at all. Converted my genuinely-open items to the
real required table shape (matching CIO's/PA's own working files), re-verified clean. Also caught a
second mismatch in the same pass — "Escalated to..." isn't a recognized blocking phrase, reworded to
"Awaiting PM/Docs decision," re-verified.

**Escalated Phase 4** to PM cc Docs rather than let CIO's finding sit as noted-but-unactioned —
`mailboxes/web/sent/ask-web-to-pm-cc-docs-cio-compose-ui-phase-4-decision-needed-43-days-silent-2026-08-31.md`.
**Reported the broadcast/checker mismatch** to CIO cc PM, since arch/comms/docs/lead (still showing
as coverage gaps) would likely hit the identical silent failure if they read the broadcast the way
I first did — `mailboxes/web/sent/finding-web-to-cio-cc-pm-broadcast-description-doesnt-match-checker-2026-08-31.md`.

**Both resolved same day**:
- **Phase 4**: Docs checked their actual workflow (not memory of it) — real trigger is always a
  direct human signal from PM/Comms, never a status field; `ready-for-docs` shows 0 live rows.
  Confirmed moot, closed in `web-standing-items.md`, re-verified the checker no longer flags it.
- **Checker/broadcast mismatch**: CIO went further than a wording fix — added a second recognized
  form (bold inline label `**Filed**:`/`**Added**:`/etc. under an item's heading, not just tables),
  corrected CLAUDE.md's "diary entry" phrasing, shipped tests. Web's table-conversion stays valid
  either way. CIO's read on the other coverage-gap roles: docs already covered by the fix,
  arch/comms/lead genuinely haven't dated yet.

Nothing further for Web on this thread.

### OPEN — obs-pass + site walkthrough, pre-staged, joint session planned for tomorrow (2026-08-31)
PM asked "anything I can unblock" — offered to pre-stage the two long-standing PM-gated walkthrough
items (obs-pass ~20-item queue + the site walkthrough) using screenshots instead of waiting for a
synchronous session, since Playwright now makes that possible. PM: yes to both, "let's plan our
walkthrough together tomorrow."

**Delivered same session**: full 31-item May 24 obs-pass reconciled against 3+ months of drift —
13 resolved (live-verified, not just marked-shipped), 10 still genuinely open, 1 new finding
(`/newsletter` now redirects to `/blog`, not `/try/beta` as documented), 1 page substantively
changed since May (`/methodology` — flagged, not relitigated against a page that no longer exists
in that form). Fresh screenshots of all 15 pages in the A–E order proposed 5/28
(`dev/2026/05/28/...`), status pills, summary stat bar. Published as an artifact:
`pipermorgan-walkthrough-prep-2026-08-31.html` — https://claude.ai/code/artifact/b02c86c4-0131-432f-b9b8-752ffc2d0b84.
Session log has full method detail: `dev/2026/08/31/2026-08-31-0630-web-code-log.md`, 12:45 PM entry.

**Waiting on**: PM to review async and/or bring it to tomorrow's planned joint session for the
actual +1/−1/defer verdicts. Nothing further for Web until then — this was prep, not the decision
pass itself.

### CLOSED — #1659 fix confirmed, real restart bug found and fixed along the way (2026-08-30/31)
Lead shipped a real fix for #1659 (`b3f88673a`, type-dispatched analysis) citing my earlier
double-confirmation, restarted the server, and asked for a 5-minute recheck ("summarize
verify-doc.txt" → expect a real summary). **Ran it — same old error, unchanged.** Checked why
before reporting a fix regression: `ps` showed the port-8001 process (PID 38357) had been running
6h12m at the time of the recheck, started 15:38:42 — **3+ hours before the fix commit (18:49:15)**.
Same `reload=False` mechanism from this afternoon's whole thread. **This looks like Lead's stated
restart didn't actually land on the process serving port 8001**, not a problem with the fix itself.
Reported precisely rather than either accept a false "fix doesn't work" or silently assume it was
fine: `mailboxes/web/sent/finding-web-to-lead-cc-pm-recheck-FAILED-server-not-actually-restarted-2026-08-30.md`.
Deliberately did not run the bonus `.zip` discriminator against a likely-unloaded process — same
reasoning as not running the PDF test blindly earlier today. **Waiting on Lead** to confirm PID
38357 has actually been replaced before re-running.

**Resolution, next morning**: Lead found their own restart was a genuine 3-layer silent failure
(macOS venv symlink resolution broke their `pgrep` pattern → `kill` no-op'd silently → replacement
server failed to bind the occupied port and died quietly → `/health` came back green from the OLD
process). Fixed properly this time: killed by port ownership (`lsof -ti:8001`), verified the port
empty, verified the new PID by both identity and start-time. **Verified Lead's claim directly again
before trusting it** (PID 46424, `lstart` 06:38:46, confirmed via `ps` myself) rather than just
running the recheck on their word. Result: **`.txt` summarize now returns a real, correct summary
— #1659 confirmed fixed, cleanly.** The bonus `.zip` discriminator couldn't be exercised as
described — `.zip` is rejected at the upload layer entirely (server-side content-type allowlist)
before ever reaching the analysis code the fix touches — reported precisely rather than force a
result. Sent to Lead cc PM:
`mailboxes/web/sent/finding-web-to-lead-cc-pm-1659-CONFIRMED-fixed-zip-bonus-unreachable-2026-08-31.md`.
**Nothing further pending** — three real, distinct bugs surfaced and fixed across this whole
two-day arc (the resolver bug #1657, the pypdf-dispatch bug #1659, and Lead's own restart-procedure
silent failure), each caught because verifying the runtime directly was cheaper than trusting a
stated result.

### CLOSED — BYOC copy thread, ended in a real infra fix + confirmed bug + a cohort-wide lesson (2026-08-30)
Cc'd on a Comms/PPM/CXO thread refining BYOC listing copy ("the issues and documents you actually
deal with"). CXO's narrowed verdict named an honest limit: "have not attempted an upload myself."
Used the browser-lane test account to close exactly that gap rather than let it sit as a documented
limitation — logged in through the real UI, uploaded a real `.txt` file, confirmed it in the Files
listing, then asked chat to summarize/list it.

**Result**: #1656 (upload UI) confirmed genuinely fixed live — upgrades "merged, not verified" to
verified. Chat-side document access confirmed still broken live (matches #1657/#1624's class, though
exact error wording differs from either issue's documented transcript) — directly confirms CXO's
"does not hold for the chat-side path" conclusion with live evidence instead of tracker-reading.
Explicitly did NOT claim to reproduce #1659's specific pypdf error message — flagged that precisely
rather than overclaim. Sent to CXO cc Comms/PPM/PM:
`mailboxes/web/sent/finding-web-to-cxo-cc-comms-ppm-pm-live-verified-1656-fixed-chat-side-still-broken-2026-08-30.md`.
**Nothing further pending** — offered to test the actual PDF path too if still useful before the
listing ships, not yet asked to.

**Fast follow-up, same day**: my finding corrected a real error before it shipped — CXO's own
tracker-derived symptom (#1659, extraction-layer) turned out to be a different bug than what I
actually hit live (resolver-layer, per CXO's precise m-43 layer analysis), and Comms' v4 synthesis
had already inherited a ship condition keyed to the wrong issue; CXO caught and corrected it same
day. CXO then asked for one more cheap test (upload a PDF, discriminate file-type-dependence) but
flagged an unverified confound: whether #1657's fix is even running on this server. **Checked it
myself rather than wait**: the running dev server (Lead's worktree, PID 67615) started 2026-08-13,
`main.py` sets `reload=False`, and #1657's fix commit is dated 2026-08-18 — five days after
startup. Unless restarted since, the fix may not be loaded at all, which would fully explain the
resolver failure independent of any file-type question — meaning the PDF test wouldn't be
diagnostic yet. **Also found and reported a correction to my own earlier claim**: #1656's actual
root cause was Fly-volume-specific (root-owned `/data` mount vs. non-root app user);
`UPLOAD_DIR` defaults to a local relative path when unset, so the specific bug structurally
cannot occur on this local dev server — my "confirmed #1656 fixed, live" was over-general; what I
actually confirmed was "upload works locally," not that the production fix is verified. Reported
both findings to Lead cc CXO/PPM/PM:
`mailboxes/web/sent/finding-web-to-lead-cc-cxo-ppm-pm-server-restart-state-may-explain-everything-plus-a-correction-2026-08-30.md`.
**Waiting on Lead** to confirm restart state before the PDF test (or anything else server-side) is
worth running. Separately: PPM raised a bigger question (whether the BYOC listing describes a
product that exists at all, given the hosted-MCP server has 0/15 acceptance criteria and no
`server` directory) — recommending holding the whole listing pending a milestone-sequencing call.
Not Web's lane to weigh in on; noting for context only.

**Resolution, same day (Fire 5)**: Lead restarted the dev server (killed the 17-day-stale PID,
fresh process from current main) and confirmed my four In Review closes stand (date-math: those
fixes predate the stale process's start, a stale server can only produce false FAILS never false
passes). Asked me to re-run the chat-file-find check. **Re-ran it — clean, decisive result**:
#1657's resolver now correctly finds the file (fix confirmed loaded); with the resolver working,
chat now hits **#1659's exact documented error verbatim** ("Unable to analyze PDF document" for a
`.txt` file) — confirmed live and current, not stale, not inferred. Also attempted CXO's original
PDF discriminator test (hand-crafted but pypdf-valid PDF, verified parseable standalone first) —
got a different, generic error ("I had trouble reading that document"), traced to a bare
`except Exception` catch-all in `workflow_entries.py:1017` that swallows the real exception.
**Reported this as genuinely inconclusive** rather than force a discriminator answer from a result
whose cause I couldn't see — the honest PDF test still needs a real, well-formed file. Reported
both findings to Lead cc CXO/PPM/PM.

**The bigger picture, closed by others same day**: Comms retracted the "ready to ship" framing on
the BYOC copy (both CXO's layer-mismatch catch and PPM's bigger "does this surface even exist"
finding were right); CXO withdrew their own recommendation in favor of PPM's. CXO wrote a
cohort-wide synthesis naming the pattern ("four checks, each one layer further from the thing it
was cited about — a relay of proxies, not one wrong measurement") and explicitly credited Web's
restraint by name twice: declining to call #1659 stale when the exact error didn't reproduce, and
refusing to run CXO's test into an unverified confound. **Nothing further pending on this thread**
— the milestone-sequencing question is PM/PPM's, not Web's lane.

### CLOSED — In Review browser-verification round (2026-08-29)
Exec routed 4 app-layer In Review items (#1512, #1568, #1480, #1578/#1581 SECURITY) as a follow-on
to the pilot — full arc across 3 fires:

1. Code-verified all four; **#1480 fully live-verified with no login needed** (redirect chain +
   executed the real deployed guard logic) — **CLOSED by Lead**, who named the served-vs-source
   byte-diff and real-extracted-function-execution approach as worth defaulting to going forward.
2. Credential gap (no test account existed) reported rather than worked around — Lead provisioned
   a dedicated browser-lane account through the real signup path (not DB-injected).
3. **Live-DOM pass done with the credential**: logged in through the real `/login` page, drove
   `/todos` and `/files` via Playwright (real form fills/selects/uploads, not API shortcuts) —
   **#1512** (priority-high chip renders correctly after real dialog submission), **#1568** (real
   edit → save → server-persisted, confirmed via follow-up GET), **#1578/#1581** (hostile
   title/filename render as escaped inert text in the live DOM, zero script execution — third
   verification layer after static read + independent jest re-run). Full report:
   `mailboxes/web/sent/report-web-to-lead-cc-exec-pm-live-DOM-pass-complete-all-four-verified-2026-08-29.md`.

**Incidental finding, filed not fixed**: `/api/v1/files/list` has no `owner_id` field, so files.html's
"Uploaded by:" renders blank (escaping is correct, it's a data-contract gap) — **#1697**, low
priority.

**Status, confirmed 21:52 fire**: all four issues (#1512, #1568, #1578, #1581) closed by Lead on my
evidence (`gh issue view` confirms all CLOSED). The pilot's full arc — smoke test → first shipped
fix → first blocked-and-honestly-reported credential gap → provisioned credential → full live-DOM
pass → four real issues closed — ran clean start to finish. Nothing further for Web on this round.

### CLOSED — predecessor's two long-standing questions
Both (CLI B trial status, `--mode=archive` scope) were answered by PM 2026-08-15 and closed in
`web-standing-items.md` — no longer carried here.

Otherwise nothing open right now — standing items (`web-standing-items.md`) are all either
PM-gated (obs-pass joint walkthrough, site walkthrough) or genuinely unscoped/no-rush (#1669
hero-image filename drift, Buttondown native newsletter).

## Notes (mix of predecessor's + mine, marked)
- *(predecessor, unverified by me)* Product-repo git: ALWAYS absolute `git -C` paths (cwd
  drifts across reconnects); stage own files BEFORE any stash.
- *(predecessor, unverified by me)* Worktree `node_modules` is a real install; Turbopack
  panics here → plain `next dev`.
- *(predecessor)* Secrets recipes: stdin-based only, never argv (zsh mangles).
- **(mine, 7/29)** Sync BEFORE checking mail, never after — a stale worktree makes an empty
  inbox indistinguishable from a drained one. Cost me a false "2 memos" read on 7/29 that was
  actually 11 once synced.
- **(mine, 7/29)** A filesystem `mv` + MANIFEST regen during mail triage is real uncommitted
  state the instant it happens — check `git status` before calling the mail loop "drained,"
  not just before ending the fire. Caught myself having dropped one triage move mid-fire.
- *(predecessor, 7/16, still true)* Naive curl+grep HTML checks can false-negative (Suspense
  boundaries render empty server-side). Check the compiled bundle / route type (`ƒ` vs `○`)
  for build-behavior claims, not just build success.
- *(predecessor, 7/16)* Next.js `headers()` in `next.config.ts` is silently ignored under
  static export — worth a fresh look at any other header-dependent config for the same
  dormant-bug pattern, now that Vercel is live.
- **(mine, 8/15)** PM's design direction preference, stated directly: GitHub-API-backed,
  always-current reads with no local-checkout dependency (the compose editor's shape) is the
  right pattern — praised unprompted specifically because it doesn't depend on PM managing the
  repo well or risk edits landing on stale drafts. Apply this bias when a new admin/tooling
  surface needs a read strategy.
- **(mine, 8/15)** Cross-project reads (e.g. Dispatch) should hit `origin/main` directly, not
  a bounded-lag mirror or PM's local checkout — PM's own usage pattern (checking Dispatch within
  minutes of a publish) is faster than any sync window. PM ruling, relayed to Docs as a decision.

## Fully resolved / historical (compressed 2026-08-29, was ~500 lines of daily detail)
Everything below was genuinely closed at the time; kept as one-line pointers only in case a topic
resurfaces. Dated session logs and git history have full reasoning if needed.

- **Cron/freeze-detector fixes (08-04→08-10)**: `FIRST_FIRE_GRACE_MIN` scheduler-latency fix;
  `cohort-freeze-detect.sh` false positive from stale local checkout (fixed, `ref=`/`tip=` added);
  a second freeze-detect ambiguity (`INSUFFICIENT-SCHEDULE` vs `COHORT-FREEZE` denominator bug,
  fixed by CIO). All CIO/HOST-owned fixes, verified live by Web, nothing further owed.
- **Web retiered Tier 3 → Tier 2** in `ROSTER.md` — Docs ruling, 08-05.
- **Blog hero compact-padding fix** (website `1b95fa5`, 08-09) — superseded by the full
  above-the-fold redesign above; this was the partial fix that motivated it.
- **Admin calendar + publish-queue staleness fixes** (website `18be9d1`, `1b95fa5`) — moved from
  build-time to request-time reads. Shipped, verified.
- **Compose UI**: localStorage autosave (Comms' ask #1, 07-29) + a real closure-timing data-loss
  bug found from PM's own use and fixed same-day (`8d2db3c`, 07-30) — stale-closure timer
  clobbering a manual save. Fixed, mechanism-reproduced, verified.
- **PDR-007 (editorial data single source of truth)** — effectively settled 07-30, Web's one
  flagged dependency (`loadCalendarLive()` reads the CSV directly) unchanged since.
- **Blog soft-404 fix** (`dynamicParams = false`, website `03b77d9d`, 08-04/05) — verified live
  including on a real publish.
- **`website#34`** (UTC-midnight-in-Pacific-build date bug, 08-22) and **`website#35`/`website#36`**
  (compose remount data-loss + canonical-URL SEO fix, 08-25) — both investigated, fixed, closed
  with evidence. `website#36` also produced the cross-project mail protocol (Dispatch-PM finding,
  ratified by Exec 08-25) — Web independently confirmed `~/Development/dispatch/` is writable on
  Amber and surfaced it proactively.
- **BYOC/GTM task force** (convened 08-09 by Comms) — Web's lane (the destination page) answered
  twice with real findings (`/try` isn't a live product a stranger can use); nothing to build yet,
  blocked on two upstream decisions not owned by Web.
- **Merge-deletion incident exposure check** (Arch/Lead's 08-08 finding) — checked own git history,
  clean by construction (sync pattern never produces a conflict); corrected a stale `--diff-filter`
  check same day.
- **Predecessor-continuity thread** — handoff doc + Vercel-migration plan artifact both found,
  read, verified fetchable; predecessor's old pre-Amber session confirmed safe to retire, 07-30.
- **Ship contributor workstream reports** filed for #055 (08-07), #056 (08-14), #057 (08-21) —
  routine, no open items.
- Several entirely-quiet-fire days (08-11, 08-13, 08-17, 08-18, 08-20, 08-23/24, 08-26) — zero
  mail, zero unblocked work, standing items correctly left unchased (none have deadlines).
