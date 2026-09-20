# Web carry-forward — 2026-09-19 (DAY-CLOSED), cron ID last updated 2026-09-19 21:57

**Session**: Amber / pipermorgan.ai, Opus 5 (since 09-14; Fable access ceiling) · cron
`22 6,9,12,15,18,21 * * *` (job **`f1f73a46`**, delete-then-create 2026-09-19 21:57 STOP, was
`580a4989`, CronList-verified exactly one, expires ~2026-09-26) · registry row
`dev/active/duty-cycle-registry.tsv` line `web`

## 🔴 FIRST THING TOMORROW — two PM answers may have landed overnight

1. **`integration-reveals-all` workDate** — PM asked a yes/no (~week of 2025-05-26, likely 05-27?).
   If answered: set it in `data/blog-metadata.csv`, regenerate `medium-posts.json` via
   `sync-csv-to-json.js`, and **verify the card renders the labeled `Work:/Published:` pair** on
   `pipermorgan.ai/blog?page=16` (it currently shows a single bare date — that's the tell).
   If PM doesn't recall: **blanking the field is the proposal**, but it's PM's call, not mine.
2. **website#43 — the Vercel `source/` move, READY TO EXECUTE, DO NOT SHIP UNPROMPTED.**
   ⚠️ I told PM at 18:52 I'd ship absent a reply, then **revised that out loud** at STOP: Exec put
   a sequencing decision in front of PM (*"set retention, note the Usage number, then tell Web to
   go — or tell Web to go first"*). **Trigger is now PM's word, either order** — shipping
   unprompted preempts a live decision and destroys the clean before/after. Exec's read: Web's
   payload finding **supersedes retention as the first lever**. Plan: `git mv
   public/assets/blog-images/source` → a non-served path, update `SOURCE_DIR` in six scripts
   (`match-blog-images`, `verify-images`, `inventory-report`, `list-missing-images`,
   `inventory-gaps`, `image-matcher-helper`); **move, not delete** (website#37 wants the archive).
   Knock-on: `docs/matching-data.json`'s 80 paths go stale — regenerable output, not a blocker.

⭐ **2026-09-19 — context cleared deliberately at ~08:23 (Wave 2, Amber fleet renewal; Pard
conducting, Janus certifying, xian overseeing).** Context clear, **not** a session exit. Consequence
worth carrying: **the cron OBJECT survived the clear with the same id (`580a4989`), and the 09:22
fire then DELIVERED** — so this is now a *third* observation of "session restarts, cron survives,"
and the first where delivery across the restart was confirmed rather than assumed. The 09:22 fire
reached me at 09:52, i.e. **~30 min late**; noting the latency without diagnosing it (could be
scheduler lag or queueing — one sample, and I can't see the scheduler). Arrival block with full
detail: `dev/2026/09/19/2026-09-19-0652-web-code-log.md`.

## ⭐ Web's GitHub criteria line (the third queue source) — WRITTEN 2026-09-19

Per PM's v1.33 ruling, "drained" = mail **+** standing-items **+** newly-observed GitHub issues
meeting this role's own criteria. **Web had no criteria line at all until today** — which meant
this seat's third source was silently empty every fire, not checked-and-clear. Naming it and
fixing it in the same fire rather than logging the gap and moving on.

**Web's criteria line** (run both; open each hit with `gh issue view`, never judge from the list):

```bash
gh issue list --repo mediajunkie/piper-morgan-website --state open --limit 50
gh issue list --repo mediajunkie/piper-morgan-product  --state open --search "label:web" --limit 20
```

Rationale for the denominator: Web **owns `piper-morgan-website` outright**, so every open issue
there is in-lane by construction — no label filter, and the label filter is what a product-repo
query needs instead, since Web is one lane among many there. **Explicitly NOT in the criteria**:
product-repo issues Web merely *filed* (e.g. #1697) — filing is not owning, and #1697 is assigned
to PM under milestone MVP, i.e. backend lane. Reading those back in would manufacture work.

**Reading on 2026-09-19 12:5x**: website open = **0**; product `label:web` = **0**. Third source
genuinely checked and empty — a measured zero, with the denominator stated.

## Open threads opened 2026-09-19 (none blocking)

- **#1827 mail-send case-normalization** — filed AND fixed same fire (`348a83232`). The #1716
  recipient check warned on *correctly delivered* mail because `[ -d mailboxes/CIO ]` is
  case-insensitive on macOS while the path compare is case-sensitive. Warning-only path, cannot
  affect delivery. ⚠️ **STILL end-to-end unconfirmed as of the 15:52 fire.** That fire's send ran
  clean — **but its header was `to: cxo, cio, pard`, all lowercase, which the OLD code wouldn't have
  warned on either.** A clean run there is not evidence. **Confirmation requires a send whose
  `to:`/`cc:` capitalizes a role name** (e.g. `to: CIO`). Don't manufacture one; when it happens
  naturally, check for spurious warnings and close #1827 then.
- **Interior heartbeat coverage — instrument shipped** (`scripts/heartbeat-interior-coverage.py`,
  `1d95e3f14`). Refutes CXO's "interior coverage is unmeasurable": session-clustering on commit
  gaps makes it measurable; validated against 3 confirmed positives + 1 known-covered negative.
  **Today: 9 of 11 roles, 10 of 44 sessions uncovered**, incl. a **mid-day** one (exec 12:54–13:57,
  7 commits) proving this isn't confined to renewal mornings. Deliberately NOT wired into the
  shared belt — CIO's lane. Threshold-sensitive (45–60m defensible, 90m false-negatives 2 of 3
  knowns); if anyone cites the number, they need the sensitivity table with it.
- **Step 5b / heartbeat coverage gap (CIO's root cause, reproduced here)** — arrival protocols and
  ad-hoc PM-directed work never trigger Step 5b. Confirmed on web's own seat this morning (08:24
  arrival, real commit, no heartbeat). **It was masked** because an in-skill START had already
  written today's row, and the belt only asks "is there a row today?" — so detection requires the
  failure to be *total*. CIO proposed a post-commit hook, routed to Pard; Web replied supporting it
  and flagged that **fixing emission doesn't fix detection**. Nothing owed by Web; watch for Pard's
  ruling.
- **Fire-delivery lag**: two consecutive fires arrived exactly **+30 min** after their slot
  (09:22→09:52, 12:22→12:52). Not diagnosed — scheduler isn't visible from here. **Third
  observation is the one worth acting on**; two identical offsets is suggestive, not a finding.

**Open — two items; one just moved from blocked to awaiting-a-one-line-answer:**
1. **Vercel usage Q1** — genuinely access-blocked (no CLI, token, or dashboard from this seat).
2. **`integration-reveals-all` workDate** — ⬆️ **sharpened 2026-09-19, no longer "PM recall only,
   unbounded."** The field is **not empty — it's a placeholder**: `workDate == pubDate ==
   2025-06-27`, untouched since the archive import (`58da3dd`). That combination occurs in **1 of
   396 rows** (this one); **395/395 others have workDate strictly before pubDate**, min lag 2 days —
   so it's a value the corpus never legitimately produces. Also **live-visible**: `BlogPostCard.tsx:126`
   only renders the labeled `Work:/Published:` pair when the two differ, so this card alone shows a
   single bare date — observed on `pipermorgan.ai/blog?page=16` against 10 controls. Sent PM a
   **yes/no** (`was it ~week of 2025-05-26, likely 05-27?`) plus a fallback proposal (blank the
   field rather than keep a wrong one). **Waiting on PM.**
   ⚠️ **Deliberately NOT claimed**: the sort-order consequence. `blog-utils.ts:19` sorts on
   `workDateISO`, which *would* misplace the post — but the position I actually observed matches
   pubDate ordering, so I haven't established which sorter that view uses. Unverified, not asserted.

✅ **website#35 CLOSED 2026-09-18** with evidence, not on merits — extended the jest net to the
local-draft restore path and answered all three unknowns the issue listed. PM's tabs-vs-navigation
question was never answered; closed on the navigation mechanism's evidence, with **multi-tab
explicitly named as uncovered**. If it recurs, reopen and suspect tabs.

✅ **DISCHARGED, do not re-open**: WYSIWYG toggle (09-14, `bb579b5`) · **P0 compose typing-reversal**
(09-15, `45ab4a9` — my own regression from `bb579b5`; the draft corruption it wrote to disk was
repaired separately in product `0ccb9314e`) · **website#42** (09-15, `d1dfc8b` — jest + `next/jest`
+ `npm test` + 4 assertions on the compose body field; CI wiring deliberately left to PM since it
changes deploy gating).

**Standdown + outage (09-16 → 09-18), resolved**: cohort-wide suspension on PM's directive (weekly
account allowance exhausted). Two gaps, one root — account ceiling delayed 09-16 fires ~6h, then
~42h with no turn at all; **13 ticks arrived stacked**. Full account in
`dev/2026/09/16/…-web-code-log.md`'s retroactive-close section. Self-report + token-efficiency input
sent to HOST/Exec cc CIO/PM (`ec685accd`); HOST has since proposed the shape as a confirmed 4th
STALE cause across two seats, CIO agreed.

⚠️ **Three distinct dark-gap causes now seen on this seat — they are NOT interchangeable:**
- **Model switch (09-14)**: restarts the session and **drops** pending firings, but the cron OBJECT
  survives with the same id — so `CronList` showing a job is NOT evidence fires are delivered, and
  Step 1's "zero crons → re-arm" self-heal never triggers. Cost 11.7h.
- **Account ceiling (09-15/16)**: fires **queue and deliver late**, not lost. Looks identical from
  outside; resolves itself on its own.
- **Session-unreachable (09-16→18)**: cron alive and firing into a session that gets no turn.
  Returns as a **pile of stacked ticks** — that pile is the diagnostic tell distinguishing it from
  the other two.
**Only a live fire proves delivery** — in all three cases.

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

### OPEN, blocked on PM/access — Vercel usage-limit warning Q1 (2026-09-09)
PM saw a Vercel plan/usage warning, wants it understood before an outage. Exec resolved Q2 live
(beta app is on Fly, website on Vercel — separate accounts, one ceiling can't take both down). Q1
(which resource, how close, what happens at the ceiling) routed to Web — genuinely blocked, not
deferring: no `vercel` CLI, no auth token, no dashboard access in this environment, and no existing
plan/usage docs in either repo. Replied to Exec cc Pard/CIO/PM naming the exact blocker and what
would unblock it (the actual warning text/screenshot, or Vercel API credentials). PM's own framing
via Exec: "next-working-day, not tonight" — genuinely not urgent, correctly not chased further.
Tracked as standing item #4.

### CLOSED (Web's part) — FTUX interview render-check (2026-09-07/08)
CXO asked Web to log in with a cold account and capture the first `PIPER_FTUX_INTERVIEW` exchange
verbatim. Both blockers cleared 09-08: Lead provisioned a genuinely cold account
(`web-ftux-cold`, real signup flow) and restarted the dev server with the flag confirmed in its
process env; the digest-ambiguity question Exec raised the night before resolved separately as a
false alarm (both flags genuinely `1`, deliberate shared vocabulary per a named test).
Re-verified the flag directly before acting (same PID/start-time as Lead's report), logged in via
real Playwright browser interaction (not an API shortcut), sent a first message, captured the
exchange: **leads with CXO's two-line copy verbatim, asks the question**. Found and reported a
third paragraph in the same reply — traced to `personalization_service.py`'s ADR-075 OQ-3 notice
(CXO's own prior direction, not the cut `why_asking` string) — as a precise fact for CXO to rule
on, not a bug Web gets to call. Reported to CXO cc Lead/Exec/PPM/PM with the verbatim exchange and
screenshots, layer named (local dev server, not live production). Closed as standing item.

**Follow-up, 09-08 same day**: CXO confirmed the render answers (yes/yes) and validated the
third-paragraph finding as real promise-language leakage the phrase-pin doesn't catch — credited
naming the layer as what made the finding usable. CXO also asked whoever picks it up to establish
whether the preferences surface is reachable in the hosted beta (their own #1604 comment's premise
may be stale). Picked this up directly — checked unauthenticated HTTP status for both the real
gated route (`/personality-preferences`, 401, correctly gated) and the specific file CXO named
(`/assets/personality-preferences.html`, 200, publicly reachable) against both the local dev
server and the actual hosted beta (`piper-morgan.fly.dev`). Found the public one is a **different**
artifact — hardcodes `user_id: "default"`, untouched since 2026-02-05, predates the real gated
route. Filed as **#1733** with full evidence rather than leave it in mail per Discovered Work
Discipline. Replied to CXO cc Lead/PPM/Exec/Arch/PM with the precise answer.

**Thread closed, 09-08 evening**: Lead dug further into `personalization_service.py`'s mechanism
after #1733 and found two more real defects — filed **#1734** (SECURITY: the preferences page's
save path silently rewrites the instance-wide config overlay, not a per-user one) and **#1735**
(the "learning" the notice promises and the actual tuning mechanism never touch — zero live
callers). CXO's first self-correction ("the inverse — a real surface exists") turned out wrong in
a specific, named way: the page that exists edits tone, not the role/priorities context the cut
promise referenced — widened correctly, checked the wrong nearby artifact. Final copy call: **cut**
the promise clause entirely (not soften into "may tune" — PPM confirmed this matches their own
09-03 no-promise-language ruling exactly), keep only a checkable capability claim ("nothing here
needs setting up first"), no pointer to the tone page (would repeat #1604's original
misdirection). CXO explicitly credited the reachability check as "the right instinct... a real
find I'd have walked straight past." Both received memos were cc's confirming/closing the thread,
no action needed from Web — read and triaged.

### CLOSED — piper-ship banner hero, shipped and deployed (2026-09-03)
PM returned 2026-09-03 with concrete direction (big banner-style hero clearly branding the
Shipping News landing page, image fully/uncropped, optionally feature the most recent Ship).
Dispatch-collision concern re-checked and clear (`git log --since="3 hours ago"`, nothing
in-flight). Implemented: `shipping-news/page.tsx` new hero (title/description above a full
16:9 `object-contain` image, no cropping even if a future differently-shaped image is
swapped in, plus a "Latest: [Ship title]" link); removed the old cropped per-post image from
`ShipPostContent.tsx`. Verified desktop+mobile via Playwright screenshots before commit.
Commit `2e8bc64` → website main, Vercel deploy confirmed `success`. Full detail:
`dev/2026/09/03/2026-09-03-0648-web-code-log.md`.

Discovered (not blocking, filed separately): a real, pre-existing, likely-sitewide dark-mode
text-color bug found while visually verifying this in dark mode — unlayered critical-CSS in
`layout.tsx` permanently beats the layered `dark:` Tailwind variants for `text-text-dark` /
`text-primary-teal-text` / `text-text-light`. Filed as website#40 with full mechanism +
evidence, not fixed this fire.

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
- **(mine, 9/08)** Filename-case gotcha in mail triage: `mv` on this filesystem is
  case-insensitive, so `mv .../flag-is-on-....md read/` silently matches a real file
  actually named `flag-is-ON-....md` and moves it — but git and `mail-send.sh` treat
  the two casings as genuinely different paths. Result: the read-side landed fine
  (under the wrong-case name), but the original inbox-side path was never deleted on
  `origin/main` — a stray duplicate that only surfaced because `mail-send.sh`'s
  "left behind" warning caught it. Always copy the exact filename from `ls` output
  before constructing a `mv`/mail-send path rather than retype it from memory.
- **(mine, 9/07)** ⭐ Standing ask from CXO, no deadline/no scheduled work, no reply
  needed: if a live ethics decline or degraded/error-path response is ever hit
  incidentally during browser-lane work (not gone looking for one), capture it
  verbatim (user turn, reply, account/connection state) and pass to CXO — their
  decline-voice watch needs a real delivered response to score, has none from a live
  account. Passive watch-item only; do not construct or go looking for a decline.
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
