# Omnibus Log: September 24, 2026

**Day**: Thursday
**Sessions**: 50 (Documentation Management, Web ×2, Communications Chief, Lead Developer, Chief
Architect, HOST, Chief of Staff, Piper Alpha, CXO, PPM, Chief Innovation Officer, and 40 Coding
Agent (prog) subagent sessions spanning ~46 GitHub issues, dispatched almost entirely by Lead
Developer)
**Day Type**: HIGH-COMPLEXITY — EXECUTION, with five embedded coordination threads called out
explicitly
**Justification**: 50 session logs is far beyond the 4-session HIGH-COMPLEXITY threshold on its
own. The dominant shape is EXECUTION: Lead Developer ran a full-day dispatch loop, sending ~37
Coding Agent subagents (33 Sonnet, 4 Opus, every tier logged) against independent, bounded,
issue-scoped fixes, reviewing and committing each lane's file set, and shipping fourteen Fly
releases (v121→v134) over the day. Most of the 40 prog-code logs are single-issue, single-lane,
report-back-for-review units with no cross-agent discussion — the textbook EXECUTION pattern
("PM orchestrating assignments, not mediating discussion" reads here as "Lead orchestrating
lanes, not mediating discussion").
That said, five threads today are genuine handoff chains crossing 3+ distinct roles with real
back-and-forth, not just informational cc: (1) the signup-wizard/#1859-flash bug arc (Web → CXO →
Lead → HOST → Web, four rounds); (2) #1855 layer 2 (Lead → Arch → CXO → Lead, both rulings
independently re-derived, not rubber-stamped); (3) the #1845 bearer-credential incident (Lead's
lint finds live tokens in HOST's own logs → HOST verifies independently, corrects a prior claim,
finds a roster gap, finds a lowercase-regex gap → PM ratifies); (4) the T-axis pre-registration
discipline (PA ↔ CXO ↔ PPM, four scored rounds run same-day); (5) three direct PM rulings mid-day
and three more in a post-STOP addendum (deploy authorization, ADOPT on the cascade migration,
#1722/#1845 closures, Fable reallocation). These are preserved as individually-timestamped
timeline entries per the COORDINATION discipline even though the day as a whole is scored
EXECUTION. The ~40 routine prog-code closures are grouped into dense per-block entries per the
methodology's Detail-Bloat guidance — reading every one of the 50 source logs in full (not
skimmed) is what let that grouping decision be made safely.
**Git Commits**: 430+ commits on `main` today; 107 of them carry Lead's session id.

---

## Chronological Timeline

### Early Morning — Starts and the first dispatch wave (05:27 AM – 08:4x AM)

**5:27 AM**: **Documentation Management** starts, publishes "The Alarm That Had Been Working All
Along" end-to-end — dry-run verified, live-verified by content (not just HTTP 200), draft
archived.

**6:42 AM**: **Lead Developer** starts (Fable 5.1, PM-allocated 09-23). Syncs 50 commits behind
`origin/main`. Dispatches **Coding Agent** (Sonnet ×2) on #1871 (Slack `post_message` never
existed) and #1870 (Gemini/Perplexity key-validation envelope fixes).

**6:42 AM**: **Communications Chief** starts; quiet day expected (mining pass not due until
09-25).

**6:52 AM**: **Web** starts; still blocked on a missing alpha test account since 09-22 evening.

**6:57 AM**: **Chief Architect** starts. Rules both of Lead's #1855-layer-2 design questions:
approves arming via the #846 store at the output seam, and approves reusing the confirm carrier
for a new non-destructive `pending_action.kind` after independently verifying five other
non-destructive kinds already flow through the same carrier — not accepting the design's framing
at face value.

**~07:0x**: **Coding Agent** closes #1871 (real `SlackDomainService.post_message`, user_id
threaded, honest failure mapping — 165+ tests) and #1870 (Gemini/Perplexity live-curl-verified
envelope fix, 300+ tests). **Lead Developer** dispatches #1855 layer-2 build to **Coding Agent**
(Opus).

**07:07 AM**: **HOST** starts. Notices Docs' `dev/heartbeats/` gap has now persisted 3 consecutive
days — sends a light, non-urgent FYI rather than continuing to silently re-observe it.

**07:08 AM**: **Chief of Staff (Exec)** starts (Fable, PM-allocated 09-23). Empty inbox but
unblocked owed work (belt classification, due Saturday) — drains it now rather than banking it.

**~07:1x**: **Coding Agent** (Opus) closes #1855 layer 2: arms the floor's offer at the output
seam, `ARMED_QUESTION_FORM` constant, `_process_intent_internal` used instead of the public
wrapper (a deliberate, reported deviation to avoid writing a fabricated user turn into the
transcript) — 132+ tests. **Lead Developer** reviews, ships, and dispatches #1872 (the floor's own
production trigger string doesn't match its own `no_provider` bucket) to **Coding Agent**.

**07:12 AM**: **Piper Alpha** starts (Fable 5.1, undisclosed drift 09-23, PM aware). Fixes a
capture-writer whitelist gap (a `SHAPE-CHANGED` label was silently collapsing to `UNMEASURABLE`)
found live on its first night.

**07:17 AM**: **CXO** starts. PA's status question about the T-axis split proposal exposes a real
gap in CXO's own carry-forward: CXO's 09-20 memo was addressed `to: exec, pa` — PPM was never
actually asked. CXO re-sends the real ruling request to PPM directly.

**07:22 AM**: **PPM** starts. Rules the T-axis split APPROVED (with a binding condition CXO hadn't
specified: T-MCP-surface must always report `UNMEASURED`, never a silent pass) — recorded in
`decisions.log`.

**~07:2x–08:4x**: **Coding Agent** closes #1872 (typed `AllProvidersFailed` exception, delegated
classification, live-verified Gemini/Perplexity), #1700 (cli/ import-smoke: two dead imports
found and excised), #1755 (span-aware multi-intent temporal suppression), #1873 (cli/ runtime
shape: notion.py wired to a completed `NotionDomainService.search_notion`, standup.py's dead
`ConversationQueries` methods disposed, keys.py signature drift fixed) — all reviewed and closed
by **Lead Developer**. **Lead Developer** separately finds and fixes a mypy-gate regression on
`main` (a stale `services/integrations/slack/tests/` duplicate directory) traced via a detached
clean-worktree diff against yesterday's baseline.

### Mid-Morning — Deploy authorization and the belt-classification thread (09:0x AM – 11:0x AM)

**09:0x**: **PM**, in conversation, authorizes Lead directly: "go ahead with the deploy… emit that
alpha invite… retry staging." **Lead Developer** deploys v121 (`ee8d8670`) from a detached clean
worktree, mints Web's alpha invite (masked form only, chmod 600), and fixes staging's empty-DB
admin bootstrap.

**~09:4x**: **Lead Developer** fixes a Code Quality gate false-red (grandfathering compared paths
across `inbox/read/sent` boxes; made the comparison box-invariant).

**~09:52 AM**: **Web** finally unblocked — redeems the invite via the ungated `/create-user` route,
then hits `/setup` Step 1's hard-blocking 403 immediately. Reports it URGENT (cc PM/HOST/CXO)
before doing anything else, since it blocks every alpha invite, not just Web's own (full arc in
the Signup-Wizard Chain section below).

**10:07 AM**: **HOST** checks `gh issue list`, finds no tracking issue for Web's finding, files
**#1875** (`priority: critical`).

**10:16 AM**: **Chief Innovation Officer** starts. Independently re-verifies **Chief of Staff
(Exec)**'s joint belt-classification deliverable (delivered two days early) — first-pass check
comes back wrong (unscoped, all-time), catches its own scoping error, rescopes, gets an exact
match to Exec's stated correction/retraction counts. Notes plainly that it is one of the two
recommended Opus 5.5 trial candidates (arch, then cio) without arguing for or against its own
inclusion.

### The Signup-Wizard Chain — #1875, #1874, #1859 (10:0x AM – 6:1x PM)

**~09:52 AM**: **Web** traces `/setup`'s 403 to source (`require_setup_incomplete`'s specific
message swallowed upstream), self-unblocks via the ungated route, and separately traces **#1859**
(chat-switch white-flash) with a captured 50/150/300ms screenshot sequence and a network waterfall
showing 32 uncached static assets refetched on every switch.

**~10:1x AM**: **CXO** (during its 10:17 fire) reads `web/static/js/setup.js` directly and finds
the exact frontend mechanism Web flagged as unverified: the fetch handler never checked
`response.ok`, so any non-2xx body was destructured as the success shape — every service silently
renders `✗`.

**~13:0x**: **Lead Developer** fixes all three stacked causes together (the #1504 write-lockout
wrongly gating a read route, an app-level handler swallowing the specific 403, CXO's `response.ok`
gap) and deploys v122. Separately fixes **#1874** (Fly's 25-connection default vs. a 32-asset
burst, then a second layer — `UsageCapMiddleware` was counting static fetches against the chat
rate budget) across v123/v124.

**~13:0x**: **Web** verifies #1875 live in a genuinely fresh, cookie-free Playwright session (not
its own logged-in account) — Step 1 renders real service status, Continue advances to Step 2.
**HOST** updates the alpha-tester roster to reflect the resolved blocker.

**15:42 PM**: **Web** re-measures #1859 on warm cache for **Lead Developer**: network layer
confirmed fixed (15/32 assets now 304), but the visual flash itself is NOT resolved — reported
precisely rather than rounded into "closed." **CXO** independently reads the code and (wrongly)
concludes the residual is the browser's own native document-teardown gap, recommending against a
shell-preserving rewrite.

**16:1x**: **Lead Developer** diagnoses the real cause from Web's exact numbers alone — a
150ms/200ms CSS fade-transition, not a load — and ships v126 removing it.

**~18:1x**: **Web**'s fourth re-measure: zero blank frame at any sample point. **CXO** corrects
its own diagnosis in full, unprompted, crediting **Chief Architect**'s intervening question (which
had proposed a `@view-transition` fallback option) as "correct regardless of which way the
underlying fact turned out." **#1859 closed clean, on all sides, same day.**

### Midday — #1855, T-axis round 1, and the timezone gap (12:0x PM – 16:2x PM)

**~12:1x PM**: **Piper Alpha** runs the first T-own-surface round under CXO's pre-registered
scoring properties: control clean (12/12), 4 of 5 hedge shapes PASS both vendors, the corrected
shared-head-noun fixture **FAILS 0/4** — the #1717 mechanism reproduced on Piper's own surface,
first attempt, scored exactly as written.

**~13:1x PM**: **Coding Agent** files **#1876** while answering Web's "no Preferences section"
question: `UserPreferenceManager.set_reminder_timezone` has zero callers anywhere in the app.
**Lead Developer** dispatches the build; **Coding Agent** ships a full-stack fix (API routes,
Settings page, a #1124 chat action) same afternoon, flagging one unresolved design tension
(a shrink-only `chat_invisible` ratchet vs. the corpus-deposit ruling) for Arch rather than
resolving it unilaterally.

**~16:2x PM**: **CXO** confirms #1855 fully closed on both layers; separately catches that
Lead's one open design question ("should an armed offer expire?") was already settled by CXO's
own 09-10 arm-survival ruling — **Chief Architect** independently reaches the same conclusion —
"the right move on a 'new' question that turns out already decided is recognizing that, not
re-deciding it."

### Evening — "Run through the tape" (16:3x PM – 21:1x PM)

**16:3x PM**: **PM** authorizes Lead to work through to the 22:00 usage reset. **Lead Developer**
begins dispatching in earnest — four to five **Coding Agent** lanes running concurrently for most
of the evening, each with a disjoint, dispatch-stated file set.

**Routine parallel closures (grouped — each independently reviewed by Lead Developer and closed
same-fire; individual defects/findings pulled out below where notable):**
- **#1791** (personality per-user store): Coding Agent found THREE independent, non-interacting
  personality systems in the codebase and correctly scoped the fix to only the one the AC named,
  flagging the other two as an unresolved Oct-2025 architecture question.
- **#1799** (priority-metadata honest degrade): one shared constant across all three render
  spatial-patterns, seam-tested; CXO later ruled the EMBEDDED copy form.
- **#1800/#1829**: per-symbol zero-mypy enforcement for the #1425 sentinel producers, and loud
  (not silent) fallback logging on `resolve_model`'s two unknown-axis branches.
- **#1761/#1773**: MCP resource-listing honest-empty fix, and a registry-vs-runtime drift fix
  (farewell/thanks marked CANONICAL but floor-routed at runtime — the same drift class as #1773's
  own filing, caught by a new cross-check test).
- **#1877**: generalized #1773's fix across the whole 56-row `ACTION_REGISTRY` — found two more
  genuine mismatches (STATUS, PRIORITY) never named in the filing.
- **#1762 portfolio cohort** (Opus): full re-census of every `[:N]` truncation site in the intent
  layer; converted 8 sites, and explicitly declined to arm a new `ListRemainder` site — composing
  one there would have manufactured the exact "promise the system can't cash" defect the fix is
  supposed to prevent.
- **web3 batch** (#1737 composer autogrow, #1750 stale asset twin deleted, #1498 historical
  conversation face): found a pre-existing duplicate-DOM-id collision between the two live chat
  surfaces (latent, not currently live in production, since home suppresses the widget).
- **#1790/#1789**: `LifecycleManager` never matched the real domain dataclasses' history field;
  `class List` shadowing `typing.List` broke `get_type_hints()` on 24 of 55 domain dataclasses.
- **#1722** (Coding Agent, read-only audit): all 89 orphaned agent worktrees (36 GB) classified —
  zero contain content absent from `origin/main`; removal list prepared but NOT executed (PM's
  call).
- **#1882**: resolved the two-`SchemaValidator`-classes question — the unwired tool was noisier
  and had no genuinely unique check to fold; deleted it and its test file.
- **#1850**: ADR-070 Amendment A1/A3 enforcement on the connector-binding write path — the ADR
  itself doesn't decide reject-vs-normalize, so the fix defaulted to reject per dispatch
  instruction and documented the reasoning explicitly.
- **#1884**: widened #1738's PORTFOLIO/STATUS subsumption rule to the whole write family; probed
  rather than trusted the issue's own "by inspection, delete/restore do the same" claim and found
  it was half wrong.
- **#1678**: `PiperConfigLoader._format_system_prompt` had hardcoded six section names from an old
  PIPER.md layout that no longer exist — silently dropping the entire curated file's content (439
  chars reaching the LLM instead of 7,671).
- **#1697**: files.html's blank "Uploaded by:" traced to a missing `owner_id` field on file-kind
  API entries — also silently hiding delete/tag-edit buttons for non-admin users on their OWN
  files.
- **#1661**: temporal file references capped at a 7-day window regardless of what the user
  actually said ("last month" widened nothing) — fixed with stated-distance parsing and an
  honest fallback naming what exists outside the window.
- **#1695**: a compose-framed draft could still echo a bare repo phrase into the mid-conversation
  preview even though the eventual filed issue was already clean — fixed at arm time via the same
  resolver the execute path uses.
- **#1784**: persisted the #1762 list-remainder tombstone into the #953 hydration slice so a
  restart-crossing "show me the rest" gets an honest "that's moved" instead of silently falling
  through.
- **#1565/#1601**: an all-day two-day calendar event rendered its title as if it were a place
  ("You're currently in: Sandra and Brian"); a `None` user_id was being stringified to the literal
  `"None"` and used as an ownership principal.
- **#1592**: calendar adapters constructed without user scope were logging ERROR
  ("credentials.json not found") on every hosted-deploy startup path — downgraded to honest INFO
  only for the genuinely unscoped case; found two feed-builder sites (out of scope) doing the same
  "has a user_id in hand, doesn't pass it" mistake.
- **#1587**: `WorkItemProvider` conflated read-failure with genuine emptiness (`[]` both ways);
  built a 3-valued outcome and threaded `degraded_sources` through Radar and standup.
- **#1582**: consolidating two templates' escape helpers into a shared asset surfaced that 8 OTHER
  templates were shipping a quote-incomplete, DOM-based copy in **production** — live
  attribute-injection holes fixed as a side effect of the consolidation.
- **#1632**: diagnosed the outwardness-marker gap as two separate plumbing breaks — fixed the one
  in scope (the #1428→DISCOVERY-prompt bridge) and reported the more likely actual source (a raw
  137-action manifest with zero outward information) as out-of-scope discovered work.

**~17:0x–18:2x PM**: **Coding Agent** (Sonnet) building #1763 finds that Lead's own proposed fix
design contains a real break: naively skipping any floor-routed sibling in a multi-intent turn
would have silently dropped a live archive/portfolio write in favor of a phantom STATUS sibling.
Corrects the design mid-build (side-effecting siblings win the skip) rather than building the
flawed version as specified.

**18:2x PM**: **Lead Developer** builds `scripts/mailbox_bearer_lint.py` (#1845 backstop) and its
first full-repo run finds **LIVE, unused invite tokens in full form in the public repo** —
including three sitting in **HOST's own session logs and one omnibus**. Attempts the DB burn
directly; the harness's own classifier denies the remote write — not worked around. Scrubs all 30
tracked files to masked form, wires the gate into Code Quality, and mails HOST for a second
review.

**19:07 PM**: **HOST** does not take Lead's report at face value: independently confirms the scrub
landed, re-greps its own historical logs, and discovers a genuine second finding — its own 07-19
log had claimed PM used one of the spare tokens for a test account, and Lead's fresh, live prod
read says it was never used. HOST corrects its own prior record with a dated addendum (original
text preserved, per convention) rather than silently editing it. HOST also finds that Savanna
Booth — one of the two testers whose token leaked — had never actually been recorded on the alpha
roster at all; her assignment had lived only in HOST's own session log, which is precisely how it
leaked. Fixes the roster gap.

**~18:3x–20:4x PM**: **Coding Agent** closes #1735 (the personalization "learning loop"
re-censused at HEAD: `apply_auto_preferences` was still a silent no-op — the return value of the
preference-store call was discarded and never checked — fixed red-first; one remaining design
question on `personality_*`'s two durable writers and zero readers left for Arch/PM), and #1867
(a mechanical census of every guided-process session-start site finds a **live, user-reachable
defect**: `_handle_add_project`'s own #1856 rewrite silently orphans an onboarding session if the
user's reply doesn't contain an "add"/"create"/"new project" token — reported per instruction,
not fixed, since the real remedy is an Arch-level call).

**~19:2x PM**: **Coding Agent** (#1723) initially re-implements two long-"held-for-disposal" dead
GitHub operations rather than disposing of them, missing that the 09-07 comment it found and
quoted was **Lead's own prior ruling**. Lead catches this mid-session and reverses the call; the
lane fully reverts its implementation and redoes the work as the originally-ruled disposal, adding
a real near-miss finding along the way (`ugrep --ignore-files` silently honors `.gitignore` even
for git-tracked files, undercounting a grep sweep by 4 hits until cross-checked with `git grep`).

**~19:3x–21:0x PM**: **Lead Developer** builds `scripts/check_autoclose_keywords.py` (#1691, both
doorways — mail-send and a commit hook), diagnoses and fixes #1662 (a staging-boot probe line was
real but sat outside `fly logs`'s 100-line buffered-output window — fixed at cause with
`PYTHONPATH=1` and a dual-channel emit), and freezes the mypy gate's transitive dependency set
(#1786) after tracing a 69-vs-70 measurement mystery to its own incomplete `git archive` (omitting
the repo-root `alembic/` package) rather than a platform difference.

**21:06 PM**: Post-STOP, **PM** rules directly in conversation: `#1722` go, `#1845` ratify,
console work (#1852) held for desk time. **Lead Developer** closes #1722 (all 89 worktrees + their
branches removed, 0 failures, PM's own checkout untouched) and #1845 (rule recorded in CLAUDE.md +
`decisions.log`, HOST mailed for the second review), then dispatches **Coding Agent** for the
#1772 candidate measurement (20-completion hard budget: candidate 0/10 leaks vs. tonight's
re-baseline 2/10 — reported as directionally supportive, explicitly not confirmatory, since the
baseline itself moved 50%→20% night to night on an unchanged prompt).

### T-axis and the Model-Allocation Thread (12:4x PM – 22:1x PM)

**12:4x PM**: **CXO** confirms the T-axis split fully discharged on its side, folds it into the
rubric as v0.8.

**16:1x PM**: PPM confirms **#1855** fully shipped and closed; separately catches a major closure
burst (21 issues) via a routine `sprint-truth.py` delta and individually spot-verifies before
marking each closed in the epic-order file.

**16:2x PM**: **PA** confirms via PM directly, in conversation: the day's elevated usage burn is
deliberate ("we are cranking up the usage in this 1.5-day reset period") — recorded as a labeled
known-cause interval for its own correlation model, not treated as an anomaly.

**18:42 PM**: **CXO** accepts round 1 unchanged and registers round 2 (member-not-metadata
mitigation) before any output exists. **PA** runs it: Claude 2/2 PASS, GPT-4o 0/2 FAIL — a vendor
split, accepted as scored without re-litigating.

**19:2x PM**: **PM**, in conversation, resolves the Fable-model-drift thread directly: "I will
reserve Fable for lead after the 10pm reset. Adjusting you now so I don't forget" — closing a
thread Exec's 09-23 fleet finding had opened.

**21:42 PM**: **CXO** registers round 3, isolating exactly one variable from round 2's two
candidates (drop the count, hold shape constant) — the discipline it named earlier in the week
having burned it once already. **PA** runs it: GPT-4o's failure becomes MORE uniform without the
count, not less — the counted-claim hypothesis isn't supported.

### Late Evening — STOP across the cohort (21:x PM – 23:x PM)

**21:09 PM**: **Comms Chief** notices the Fable-model-attribution drift from 09-23 reverted on its
own — verified via the stronger source (a fresh explicit model-identity system reminder), not
just the attribution line — and closes the watch item without escalating further, since it
resolved before either PM or Pard weighed in.

**21:5x PM**: **Chief Architect** STOPs; a duplicate-timestamp tick arrives at the exact STOP
minute, and rather than treat it as a formality, drains four real memos including #1859's final
close-out and the #1772 mechanism ruling (unify N=1 onto the already-proven N≥2 aggregate
composition path — a removal of a carve-out the evidence no longer supports, not a new mechanism).

**21:52 PM**: **Web** STOPs after taking Lead's optional cold-cache #1859 offer rather than
leaving it hanging, since it was genuinely unblocked with time before STOP — confirms zero blank
frame on a truly first-ever cold load too, closing the one caveat left in its own prior memo.

**22:07 PM**: **CIO** STOPs; independently re-verifies Pard's cross-project worktree-migration
claim (rather than citing a historical doc CLAUDE.md still points to, which turns out to be
stale) by directly checking two named exception seats' branches on disk — confirms the claim and
flags the stale doc as a separate, real finding.

**22:1x–22:5x PM**: **HOST**, **Exec**, **PPM**, **CXO**, **Documentation Management** all STOP —
sign-off checklists run, cron re-armed, carry-forwards updated. HOST's sign-off is momentarily
blocked by its own auto-close-keyword guard (its day-close commit message put "close" near "#1845"
and "#1885") — rephrased, not bypassed, and recorded as the guard doing exactly its job.

**23:08 PM**: **Chief of Staff (Exec)** STOPs after a final round of cross-repo relay work (CIO's
launch-model confirmation forwarded to Pard) and a registry-row size trim applied to its own row.

<!-- Approximately 15 additional routine mail/criteria/heartbeat cycles across the six duty-cycle
role logs (empty-round drains, cron re-arms, carry-forward rewrites) are omitted from this
timeline per the EXECUTION density guidance — each role's own log has the full record. -->

---

## Executive Summary

### Core Themes

- A single-day dispatch record: Lead Developer ran 37 Coding Agent lanes (33 Sonnet, 4 Opus,
  every tier logged), closed 67 GitHub issues (repo-wide, GitHub-verified), filed 17 new ones, and
  shipped 14 Fly releases (v121→v134), each verified live via `/health`.
- Five real cross-role coordination threads ran inside the execution day: the signup-wizard/flash
  bug chain (six roles, one thread, closed same day); #1855 layer 2 (three independent rulings,
  none rubber-stamped); the #1845 credential-leak incident (a live security finding, verified
  independently on both sides, closed with a mechanized gate rather than a one-time apology); the
  T-axis pre-registration discipline (four scored rounds, zero post-hoc re-litigation); and three
  direct in-conversation PM rulings plus three more in a post-STOP addendum.
- A genuine self-correction pattern recurs across roles today, not just once: CXO corrects its own
  #1859 diagnosis unprompted; HOST corrects its own 07-19 log with a dated addendum rather than a
  silent edit; Lead reverses a subagent's implementation-instead-of-disposal mid-task on catching
  it was Lead's own prior ruling; a Coding Agent lane self-catches a measurement-denominator error
  mid-report (m-44, "true measurement of the wrong object").
- Dead/orphaned code surfaced repeatedly as a byproduct of unrelated fixes, not as a dedicated
  sweep: #1582's escape-helper consolidation found 8 templates shipping a live attribute-injection
  vulnerability; #1775's "dead render family" census found one of its own four rows had never
  existed in the codebase's history; #1867's guided-process census found a live #1856-class
  session-orphaning defect nobody had gone looking for.

### Technical Details

- `#1855` (floor arms what it offers) shipped in two layers same-week: layer 1 (09-23) plus layer
  2's seam-arming, `ARMED_QUESTION_FORM` house-form normalization (CXO's quotability test §3
  applied for the first time to a real binding), and a deliberate deviation (`_process_intent_
  internal`, not the public wrapper) to avoid writing a fabricated user turn into the transcript.
- The signup wizard (`#1875`) had three independently-discovered stacked causes fixed together in
  one deploy: the #1504 write-lockout wrongly gating a read-only route, a generic exception
  handler swallowing a specific 403 detail, and the frontend never checking `response.ok`.
- `#1859`'s white-flash root cause moved through three diagnoses before landing: first thought to
  be uncached assets (fixed, didn't resolve it), then wrongly diagnosed as a browser-native
  structural gap (CXO's error, self-corrected), finally traced to an explicit 150ms/200ms CSS
  transition that *was* the whole flash once the network cost was gone.
- `scripts/mailbox_bearer_lint.py` (#1845) found three live, unused invite tokens in full form in
  tracked, public files — two of them in HOST's own session logs, the third in an omnibus; the
  classifier correctly refused the live DB burn from Lead's seat, leaving that step for PM.
- `PiperConfigLoader._format_system_prompt` (#1678) had six hardcoded section names from a
  superseded PIPER.md layout; the file's real 10 sections (7,671 characters) had never reached the
  live LLM system prompt — only a 439-character stub had.
- `class List` shadowing `typing.List` (#1789) broke `get_type_hints()` on 24 of 55 domain
  dataclasses; fixed via `list[...]` builtins (no rename) rather than the workaround
  (`_domain_globalns()`) that had been routing around it in the schema validator.
- The #1762 portfolio-render census converted 8 truncation sites to render whole and explicitly
  declined to arm a new cashable-remainder site — composing one there would have manufactured the
  exact broken-promise defect the mechanism exists to prevent, since those sites carry no session
  to cash an offer against.
- `#1867`'s guided-process census (mechanically re-derived by actually calling
  `register_default_processes()` against a scratch registry, not by reading source and trusting
  it) found a live, user-reachable onboarding-session orphan bug in the #1856 handler itself — the
  same handler that had been built to fix the class of bug it now reproduces.

### Impact Measurement

- 67 GitHub issues closed today (Lead's own GitHub-verified count); PPM independently tracked and
  spot-verified 30 of those within the MVP epic-order file across two closure bursts.
- 17 new issues filed today by Lead's dispatches; PPM placed 11 fresh issues into the epic-order
  file, milestoned and board-added, each spot-verified via `gh api` before marking.
- 14 Fly releases (v121→v134), each confirmed live via `/health`'s sha attestation before the next
  deploy proceeded.
- 89/89 orphaned subagent worktrees classified (36.1 GB); zero carried content absent from
  `origin/main`; removal deferred to PM, then executed same day on PM's explicit go — 383→380 GiB
  freed (APFS clone accounting).
- `#1845`'s lint gate: 30 tracked files scrubbed to masked form on first run, baseline set at 40
  placeholder/fixture hits, wired into Code Quality; HOST's own second-review pass (13 synthetic
  test cases against the real matching functions) found one further real gap (a lowercase-token
  blind spot) the first pass missed.
- T-axis: 4 pre-registered rounds run same day (n=2 or n=10 per cell, vendor-split where relevant),
  zero rounds re-litigated after scoring — the first time in "0 for 3" prior attempts that the
  pre-registration discipline held cleanly end to end, per CXO's own accounting.

### Session Learnings

- **A subagent finding a break in its dispatcher's own design is real signal, not noise**: the
  #1763 lane corrected Lead's proposed skip-logic mid-build after finding it would have silently
  dropped a live write in favor of a phantom sibling — the design was probed, not assumed.
- **"Measured against HEAD" and "measured against the right denominator" are different claims**:
  the #1763 lane's own closing correction (attributing a mypy count to "not mine" by diffing
  against HEAD, when the live question was the file against a sibling lane's already-landed
  deletion) is m-44 caught in the act, inside the same session that produced it.
- **A ruling that already exists beats a fresh one, and recognizing that is itself the work**:
  twice today (Arch on #1855's "does an armed offer need a bound?", Arch again on #1799's
  "outlives one turn" question) a "new" question turned out to already be settled by an existing
  ruling — checking `decisions.log` before deliberating saved real discussion time both times.
  Also, HOST's second review of the #1845 lint found a real gap by testing the matching functions
  directly rather than trusting that the file existing meant the gate worked — the same discipline
  from a different angle.
- **Shared-worktree concurrency produced real, named near-misses, all caught before they shipped**:
  a `ugrep --ignore-files` sweep silently honoring `.gitignore` for tracked files (undercounted a
  grep by 4 hits); a mypy-ceiling reading contaminated by a sibling lane's mid-flight edit
  (re-measured after it settled); a `except X as e:` collision with an unrelated later loop
  variable of the same name (caught by the mypy gate itself, not by review).
- **A colleague's own fix is still worth independently verifying**: Docs re-ran the belt scripts
  on CIO's just-shipped corruption detector rather than accepting the thank-you memo, and found
  the detector's own new warning text had baked in the literal corruption signature it described —
  a self-triggering false positive shipped hours earlier, caught the same day.
- **The day's own volume was itself a hazard the log discipline caught**: Lead's own tally of
  "issues closed since midnight" drifted from 26 to 36 to a corrected 46 across successive fires
  before landing on the GitHub-verified 67 at STOP — each earlier number an undercount from an
  80-row API page limit, not a fabrication, but a reminder that even a careful same-session count
  needs re-verification against the primary source before it's trusted as final.
- **PM's post-STOP engagement is not an interruption of the flywheel, it's a continuation of it**:
  three of tonight's most consequential rulings (#1722 go, #1845 ratify, #1772 budget) landed after
  Lead's own STOP ritual had already run — captured in a post-STOP addendum rather than either
  reopening STOP or losing the record.

---

## Canonical References Consulted

- **ADR-059** — "Workflow Dispatcher and Offer System Consolidation" (status: APPROVED) — cited by
  #1867's guided-process census re: onboarding's "on ice" status and the registry re-registration
  question left open for Arch (Q2).
- **ADR-070** — "MCP-Consumer Connector Architecture" (status: v0.1) — Amendment A1/A3 cited by
  #1850's write-path enforcement build; the ADR itself does not decide reject-vs-normalize for a
  non-scheme literal on a managed connector, which #1850's build states explicitly rather than
  inferring a ruling that isn't there.
- **ADR-075** — "Configuration / Personalization Ownership — Per-User Scoping for Instance Config"
  (status: v0.2 ACCEPTED) — D3/D4 cited by #1678 (whole-file fallback, never merged) and #1791
  (the ADR-075 D4 personalization-scoping path that #1791's personality-store work sits beside,
  not through).
- **`docs/internal/architecture/current/intent-routing-stack.md`** — the mandatory pre-read for
  any classification/dispatch/floor-response work; consulted directly (not from memory or a prior
  session's summary) by at least 14 of today's Coding Agent sessions before touching routing code,
  and updated in-commit by the #1755, #1763, #1799, #1850, #1872 lanes per its own currency rule.
- **`docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`** §3/§4/§5b/§5b-i —
  the provenance vocabulary (fresh/verified_empty/source_failed/not_attempted) and the
  cashable-remainder honesty rule, consulted directly by #1587, #1661, #1762, #1784, #1799.

---

## Sources

`dev/2026/09/24/2026-09-24-0527-docs-code-log.md` · `dev/2026/09/24/2026-09-24-0626-web-code-log.md` ·
`dev/2026/09/24/2026-09-24-0642-comms-code-log.md` · `dev/2026/09/24/2026-09-24-0642-lead-code-log.md` ·
`dev/2026/09/24/2026-09-24-0643-prog-code-1871-log.md` · `dev/2026/09/24/2026-09-24-0652-web-code-log.md` ·
`dev/2026/09/24/2026-09-24-0657-arch-code-log.md` · `dev/2026/09/24/2026-09-24-0704-prog-code-1870-log.md` ·
`dev/2026/09/24/2026-09-24-0707-host-code-log.md` · `dev/2026/09/24/2026-09-24-0708-exec-code-log.md` ·
`dev/2026/09/24/2026-09-24-0708-prog-code-1855-l2-log.md` · `dev/2026/09/24/2026-09-24-0712-pa-code-log.md` ·
`dev/2026/09/24/2026-09-24-0717-cxo-code-log.md` · `dev/2026/09/24/2026-09-24-0722-ppm-code-log.md` ·
`dev/2026/09/24/2026-09-24-0757-prog-code-1872-log.md` · `dev/2026/09/24/2026-09-24-0802-prog-code-1700-log.md` ·
`dev/2026/09/24/2026-09-24-0804-prog-code-1755-log.md` · `dev/2026/09/24/2026-09-24-0813-prog-code-1873-log.md` ·
`dev/2026/09/24/2026-09-24-1016-cio-code-log.md` · `dev/2026/09/24/2026-09-24-1543-prog-code-1876-log.md` ·
`dev/2026/09/24/2026-09-24-1652-prog-code-1791-log.md` · `dev/2026/09/24/2026-09-24-1652-prog-code-1799-log.md` ·
`dev/2026/09/24/2026-09-24-1653-prog-code-1800-1829-log.md` · `dev/2026/09/24/2026-09-24-1700-prog-code-1761-1773-log.md` ·
`dev/2026/09/24/2026-09-24-1704-prog-code-1762-log.md` · `dev/2026/09/24/2026-09-24-1704-prog-code-1877-log.md` ·
`dev/2026/09/24/2026-09-24-1704-prog-code-web3-log.md` · `dev/2026/09/24/2026-09-24-1716-prog-code-1838-log.md` ·
`dev/2026/09/24/2026-09-24-1718-prog-code-1790-1789-log.md` · `dev/2026/09/24/2026-09-24-1734-prog-code-1763-log.md` ·
`dev/2026/09/24/2026-09-24-1735-prog-code-1879-1878-log.md` · `dev/2026/09/24/2026-09-24-1744-prog-code-1775-log.md` ·
`dev/2026/09/24/2026-09-24-1752-prog-code-1722-log.md` · `dev/2026/09/24/2026-09-24-1815-prog-code-1882-log.md` ·
`dev/2026/09/24/2026-09-24-1816-prog-code-1735-log.md` · `dev/2026/09/24/2026-09-24-1816-prog-code-1867-log.md` ·
`dev/2026/09/24/2026-09-24-1823-prog-code-1723-log.md` · `dev/2026/09/24/2026-09-24-1827-prog-code-1850-log.md` ·
`dev/2026/09/24/2026-09-24-1847-prog-code-1884-log.md` · `dev/2026/09/24/2026-09-24-1850-prog-code-1678-log.md` ·
`dev/2026/09/24/2026-09-24-1850-prog-code-1697-log.md` · `dev/2026/09/24/2026-09-24-1915-prog-code-1661-log.md` ·
`dev/2026/09/24/2026-09-24-1920-prog-code-1695-log.md` · `dev/2026/09/24/2026-09-24-1927-prog-code-1784-log.md` ·
`dev/2026/09/24/2026-09-24-1940-prog-code-1565-1601-log.md` · `dev/2026/09/24/2026-09-24-1941-prog-code-1592-log.md` ·
`dev/2026/09/24/2026-09-24-1944-prog-code-1587-log.md` · `dev/2026/09/24/2026-09-24-2008-prog-code-1582-log.md` ·
`dev/2026/09/24/2026-09-24-2034-prog-code-1632-log.md` · `dev/2026/09/24/2026-09-24-2110-prog-code-log-1772-candidate.md`

**Supporting non-log artifacts** (already archived alongside the source logs, each produced by and
referenced from the corresponding prog-code session above): `dev/2026/09/24/1722-orphan-worktree-audit.md`,
`dev/2026/09/24/1735-learning-loop-census-and-decision-2026-09-24.md`,
`dev/2026/09/24/1772-candidate-measurement-2026-09-24.md`, `dev/2026/09/24/mainold-503-review-2026-09-24.md`
(dispatched by Exec, reported in Exec's own log, not a separate session). The T-own-surface probe
artifacts referenced in Piper Alpha's log (`dev/active/probes/RESULTS-t-own-surface-*.md` and their
underlying `probe_t_*` scripts/JSON) are PA's own run outputs, fully accounted for in PA's session
log above — not a separate or missing session.

**Discrepancies preserved, not resolved** (per Step 2.6): none rose to the level of a genuine
factual conflict between two logs on the same event. Numeric differences between Lead's repo-wide
"67 closed" tally and PPM's "30 closed" MVP-epic-file tally reflect different denominators (whole
repo vs. one milestone's tracked file), not a disagreement about what happened.

**Orphaned artifacts** (mentioned in a source log but with no independently-attributable session):
none found. Every non-log artifact in `dev/2026/09/24/` traces to a specific session log in the
source set above.
