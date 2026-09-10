# Omnibus Log: September 9, 2026

**Day**: Wednesday
**Sessions**: 14 (Comms, Documentation Management, Chief Architect, Lead Developer, Web, Piper Alpha (PA), HOST, CXO, PPM, Chief of Staff (Exec), CIO, and 3 separate Coding Agent (prog) delegations from Lead)
**Day Type**: HIGH-COMPLEXITY: COORDINATION — 12 distinct roles, sustained cross-agent handoff chains and roundtables shaping the day's direction, not independent parallel tracks.
**Justification**: Four genuine coordination threads ran through the day, each with real back-and-forth: (1) the multi-day Excellence Flywheel re-evaluation challenge round closed today via a live Arch↔CXO↔HOST↔Exec↔Lead exchange; (2) a cross-project accessibility proposal (Dispatch-PM → Web → Docs → Web) was root-caused, spec'd, and shipped same-day across three cc'd memos; (3) PM's real-data correction to Exec's throughput narrative fanned out into four directives that PPM, Arch, CXO, and CIO all built on same-day; (4) three independent acceptance-contract findings (Lead, Arch, CXO, Exec) converged into one governance ruling built same-day. None of this is independent parallel work — each thread required one role's output to change another's next move.
**Git Commits**: 20+ (product + website repos combined; see Technical Details)

---

## Chronological Timeline

### Phase 1: Pre-Dawn Publish and Governance Housekeeping (6:03 AM – 7:22 AM)

**6:03 AM**: **Communications** starts pre-cron at PM's direct request —
PM has completed the voice-pass on Weekly Ship #059 ("The Verifier Is Not Exempt") and asks for review.

**6:03–6:11 AM**:
**Communications** runs full `template-audit` under the Ship calibration table, cross-checks the acronym-linter's NO-GLOSS warnings against 5 prior published Ships rather than assume they're real findings (confirms bare role short-forms are established Ship-genre convention), catches 2 real typos no mechanical check would find ("extend"→"extent," "accesss"/"too us"→"access"/"took us"), commits (`0a0514828`), sends PUBLISH-READY to Docs.

**6:03–6:11 AM**:
**Communications**, on PM's observation that Ship-genre and blog-series conventions differ ("we should keep track of the distinct conventions"), bumps `template-audit` to v1.13 (`5ac933587`) —
a fifth calibration row, narrowly scoped to the acronym-glossing sub-check only;
hard-acronym findings still block.

**6:09 AM**:
**Documentation Management** starts pre-cron (PM-initiated ahead of the 06:57 fire), picks up Comms' PUBLISH-READY memo, confirms yesterday's `DAY-CLOSED` marker present.

**6:15 AM**: **Documentation Management** proofreads Ship #059 independently of Comms' report —
verifies acronym linter, checks live #058 precedent for the footer-teaser question (established no-teaser practice, not a defect specific to this draft), verifies all 7 body links live (200), runs `publish-post.js --dry-run` clean, publishes for real (`d983687`, hashId `d5d96e000593`).

**~6:20 AM**: **Documentation Management** finds a live render problem and does not accept a bare 200 as proof:
the published page's title reads "Ship Not Found" with an embedded 404 despite a 200 status.

**~6:25 AM**: **Documentation Management** investigates rather than assumes broken —
reads `shipping-news/[slug]/page.tsx`, confirms the JSON entry's `slug`/`category` fields are correct (ruling out a real data bug), compares response headers against known-working Ship #058 (both tagged `x-vercel-cache:
PRERENDER`), concludes a genuine deploy-propagation delay (the 200 was a stale cached not-found fallback), not a defect in the publish.

**~6:30 AM**:
**Documentation Management** re-polls with an actual content check (title, image, body-text fragment) rather than a fixed guess-length wait, confirms the page is genuinely live before reporting resolved.

**~6:35 AM**: **Documentation Management** catches a git gotcha for the second time this week —
a commit staging a `git mv`-renamed file alongside separately-staged modifications only picked up the rename (1 file);
caught via post-commit `git status`, fixed with an explicit re-add and separate commit;
flags it as a standing discipline (verify `git status` after any commit mixing a rename with other changes).

**6:39 AM**: **Chief Architect** starts.
Drains CIO's no-new-challenge ack and **CXO's structural finding from overnight**:
v3.0.1 "fixed" the flywheel enforcement table by amending the note while the table's own cells still carried the pre-amendment "Enforced" labels —
the same caveat-in-the-footer shape the fix itself was meant to correct ("your memo says the column now says Present.
The column does not. The amendment note does").

**6:40 AM**: **Chief Architect** ships v3.0.2 (`ba8b6a582`) —
the table corrected in place, per-artifact labels in the cells, amendment section kept as the dated record with a pointer note.

**6:49 AM**: **Web** starts, mail loop genuinely empty (inbox holds only MANIFEST), standing items unchanged (all three PM-gated:
obs-pass, site walkthrough, Buttondown).

**6:56 AM**:
**xian** sends **Web** a screenshot (in chat, misaddressed to "Docs") of Ship #059 rendering with washed-out light-gray-on-light-gray text in dark mode.

**6:57 AM**: **Documentation Management** — Fire 2 (first scheduled fire).
Finds a self-caught lapse: Comms' original PUBLISH-READY memo was acted on this morning but never moved to `read/` —
exactly the "act-on-a-memo-during-a-PM-session but forget to triage" gap the carry-forward already names.
Fixes it.
Updates the calendar to `distributed` after Dispatch-PM confirms the LinkedIn syndication leg is live, checking Ship #058's own row for precedent (empty altText/caption there too) before leaving #059's fields empty to match.
Notes but doesn't chase a pre-existing data gap on #058's own row (empty `linkedinURL` despite `canonicalSite=distributed`).

**7:00 AM**: **Piper Alpha (PA)** starts — inbox empty;
re-verifies carry-forward is current (nothing new landed against yesterday's rewritten PM-attention section);
spot-checks the known-broken `chrome-devtools` MCP path against `https://pipermorgan.ai/privacy`, confirms it's still the same old broken Chrome path despite a context compaction since the last retest —
sharpening the boundary that **a compaction does not restart the MCP subprocess either, only a genuine new session does.**

**7:07 AM**: **HOST** starts (Day 47 on Amber). Checkers (drift, invariants, promises) all `rc=0`; 0 open issues.
Drains 4 memos:
independently verifies CXO's table-vs-footer finding by reading the file at `origin/main` directly and finds Arch's v3.0.2 already shipped it;
notes CIO reviewed the full flywheel synthesis directly and confirmed no new challenge on D4/D2;
notes CIO also reopened #1731, correctly rescoped to PPM's still-open reconcile-sequencing hypothesis rather than closed on the coattails of an unrelated zsh retraction.
**Lead's engineering-lane response concurred on D4 with real usage data** (a two-week count of name-the-layer/state-the-denominator invocations, every one in verification, none in scoping) and gave explicit concurrence on D1/D3/D5/D6/D7 rather than let silence be read as agreement.

**7:17 AM**: **CXO** starts.
Verifies v3.0.2 in the file rather than trust Arch's memo —
confirms the exact resolution proposed, and finds P5 came back reading "Enforced-by-D7 once the first closing gate runs it;
Present until then," sharper than the original ask.
D4 and D2 both stay declined;
CXO adds no independent evidence to Lead's D4 concurrence ("I still have no independent evidence and am not adding a voice to a count I can't back").

**7:17 AM**: **CXO** runs the mandated voice-watch structural review (per the row's own 09-07 correction:
a landed-copy commit triggers a structural review, not a Colleague Test) on 4 copy items Lead landed overnight —
all land verbatim, 2 exceed the original ask (the generic decline split into `_RECOGNITION`/`_RECOVERY`, two different claims rather than one blob;
Lead's echo-implementation naming the actual `marked.parse()`/`innerHTML` rendering layers and a degraded fallback CXO didn't know existed).

**7:17 AM**: **CXO** finds a real, test-invisible gap:
the five `*_source_failed` flags are hand-maintained in three separate places (five if-sites, a gating tuple, and the test's own copy);
a sixth flag would render its FAILED line, be invisible to the tuple, and produce no test failure.
Routes it to Lead as a refactor (derive the gate from the appended lines), not an add, and explicitly does **not** ask for the aggregation cap her own earlier #1717 concern implied —
her own live-run evidence and PM's "has one real case proven this needed?" test both say no.

**7:17 AM**:
**CXO** closes 4 tracker rows on verification (10→7, re-run to confirm) and catches herself editing the carry-forward with a scripted `.replace()` one fire after writing "never regex-edit the tracker" —
reads the whole file back to confirm it's intact, notes the rule should have been general, not file-specific.
Separately checks (rather than reflexively resends) a `mail-send.sh` "STRANDED" warning on `MANIFEST.md` —
an empty diff against `origin/main` proves nothing is actually stranded this time.

**7:22 AM**: **PPM** starts. `sprint-truth.py`: MVP 52 not done (34 Sprint Backlog, 3 In Progress, 15 In Review), 0 unmilestoned.
Drains CIO's #1731 reopen (declines the repro work, citing yesterday's own governance-role boundary —
"pulling infra work they diagnosed isn't theirs to claim just because the context is fresh") and CXO's voice-watch findings —
no PPM action on either.
#1386/#1688 hold their closed/watched state; two flywheel challenge-round acks (CIO, Lead) triaged, watching passively as decided yesterday.

### Phase 2: Dark-Mode Fix Shipped, Figure/Figcaption Handoff Opens, Voice-Watch Gap Closed (6:56 AM – 10:22 AM)

**6:56–8:00 AM**: **Web** investigates the dark-mode report rather than guess —
confirms dark mode is active (the theme toggle's sun icon), traces `ShipPostContent.tsx`, finds the real cause in the compiled Tailwind config:
`dark:bg-dark-bg` references a token (`dark-bg`) that has never existed (the real token is `dark-background`, `#0F172A`);
Tailwind's JIT compiler silently drops classes referencing undefined tokens rather than erroring.
`git log -S` confirms this was never a regression — always broken since the site's initial 2025-08-08 commit.

**~8:00 AM**: **Web** finds the scope is far larger than the one reported page —
`grep` surfaces 10 occurrences across 8 files (every blog post template, every Ship post template, the Shipping News landing page, and 5 admin pages:
login, calendar, compose, publish-queue, AdminGate).
Fixes all 10 to the real existing token rather than add a duplicate alias, verifies count matches exactly (10 before, 10 after, 0 remaining), confirms the fix compiles real CSS (`.dark\:bg-dark-background{background-color:#0f172a}`), ships (`70791c3`), deploy verified `success`.

**9:12 AM**: **Communications** — quiet fire;
product repo picks up routine Arch/Lead traffic, website repo picks up the dark-mode Tailwind fix, unrelated to Comms' own lane.

**9:31 AM**: **Lead Developer** receives CXO's voice-watch structural review this fire —
confirms all four copy items landed (two exceeding the ask) and the one real test-invisible gap (the five `source_failed` flags enumerated twice —
the "parallel-enumeration drift class," in code merged the day before).
Starts a fix lane running the same fire:
single-source registry + AST-derivation test (the #1685 mapper idiom), so a sixth flag is unaddable without a red build.

**~10:00 AM (Lead's ~10:3x fire)**: **Lead Developer** closes CXO's gap structurally (`3215e64e5`, verified 3,735+49 tests, pushed) —
one registry, gate and test denominators both derive from it, hand tuple deleted and the literal-tuple form banned, a planted sixth flag caught and named by the red-proof before removal, byte-identity confirmed across all 32 flag subsets.

**9:39 AM**: **Chief Architect** — WORK fire.
Drains **Lead's D4 concurrence with the heaviest-user datapoint** ("your concession matches the data") and CXO's voice-watch structural review of the same overnight copy items, with the one test-invisible gap flagged as Lead's lane.
Round state: D4 concur+data, D2 unopposed x2; window holds through EOD.

**9:49 AM**: **Web** —
mail loop finds Dispatch-PM's proposal to standardize `<figure>`/`<figcaption>` markup for captioned images (a real accessibility gap, measured live at zero coverage sitewide, tied to a documented 07-16 defect where the missing structure caused a false "no caption" report).
Dispatch-PM explicitly scopes item 1 (hero image) as "in your hands, probably small" and item 2 (in-body markdown teaser) as "as much Docs's convention as your template."

**~9:50 AM**: **Web** ships only the hero half —
wraps the existing image-container div and caption `<p>` in `<figure>`/`<figcaption>` (zero visual change, same Tailwind classes moved over), verifies with a real Playwright browser render, not just a clean build (the component is `'use client'`, so a curl check would miss it) —
confirms exactly one `<figure>`/`<figcaption>` pair, ships `fbfe813`, deploy `success`.
Corrects a routing mistake before sending the reply (Dispatch-PM has no `mailboxes/` directory in this repo;
the ratified path relays via Exec's inbox, not a direct write), cc's Exec/Docs/Comms/PM.

**9:57 AM**: **Documentation Management** — Fire 3.
Finds Web's reply names the in-body-teaser half as "Docs's call, not mine to make unilaterally," and discovers the original Dispatch-PM proposal was never actually delivered to Docs' own inbox despite the cc —
reads it directly from Web's `read/` folder rather than act on the reply alone, per "investigate before extending."

**~10:00 AM**:
**Documentation Management** reads `convertToHtml()` in `publish-post.js` directly rather than guess, root-causes Dispatch-PM's measured variance (two blocks on 09-02, one joined paragraph on 09-09) as source-adjacency —
a blank line between image and caption markdown splits them into separate blocks via existing detectors;
no blank line lets the generic multi-line-paragraph collector join them.
Confirms Ship #059's own draft already uses the correct (adjacent, no-blank-line) convention, and sends Web a concrete implementation spec —
a new block-type check ahead of the paragraph fallback, same shape as the file's existing pattern-detection blocks —
cc Exec/Comms/PM, explicitly not urgent, implementation routed to Web since it's a converter-logic change in the website repo.

**10:17 AM**: **CXO** — Fire 2.
Verifies all five of Lead's registry-fix claims in the source, not the memo —
every one holds (registry at line 144, gate deriving at 1202, `DIRECTIVES = dict(SOURCE_FAILED_FLAGS)` with no bare 5 left, AST association asserting exact order and rejecting duplicates, the pre-fix drift form banned).
Notes the fix didn't patch her critique, it made it unstatable —
"twice this week a peer returned something sharper than the ask" (the same shape as Arch's P5 the day before).
States her own limit: no pytest on this seat, so Lead's red-proof is his evidence, not hers.

**10:17 AM**: **CXO** investigates a recurring "STRANDED" `mail-send.sh` warning instead of re-refuting it a second time —
reads `mail-send.sh:145–169` and finds a real structural script defect:
`MANIFEST.md` lives permanently in both `inbox/` and `read/` by design (a per-directory regenerated index, never a moved memo), so any send passing only the read-side copy always warns.
Names why it matters more than a stray line:
the alarm was deliberately moved to be the last, most-visible line after a real strand once hid for weeks —
an always-false alarm in that exact position teaches people to ignore it.
Routes it to Lead as a script fix, affecting every role several times a day.

**10:22 AM**: **PPM** — WORK. Pure Lead/CXO follow-through thread (the registry fix and its independent verification); no PPM action.

### Phase 3: The Acceptance-Contract Convergence (10:37 AM – 1:22 PM)

**10:37 AM**: **CIO** starts.
Mail loop: PPM confirms yesterday's #1731 reopening and explicitly hands the repro to CIO/Lead rather than claim it;
two cc's read for context —
CXO's `mail-send.sh` finding (addressed to Lead, who owns the check) and Lead's flywheel challenge-round concurrence.

**~10:40 AM**: **CIO** attempts the #1731 repro PPM explicitly handed off —
builds the fixture (send path X alone, then touch it again without an intervening sync) in several shapes over ~20 minutes.
Cannot reproduce the failure;
reports the negative result honestly on the GitHub issue as "tried, didn't reproduce," not a refutation of PPM's original observation, and cleans up all test fixtures from `origin/main` afterward (verified via `git ls-tree`, not just a local `rm`).

**~10:40 AM**: **CIO** finally moves standing-item 7i (#1277, canonical-ops-recipes) from a fourth deferral to genuinely in-flight —
reads the issue directly rather than from memory, dispatches a worktree-isolated subagent with explicit scope (recipes 2 and 3 require real codebase verification;
state gaps rather than guess), instructed not to close the issue itself.

**~11:00 AM**: **CIO**'s subagent finishes within the hour;
CIO reviews the actual drafted file, not just the completion summary, and spot-verifies four load-bearing claims independently before merging (an exact `keychain_service.py:290` line match, three exact `integrations.py` line numbers, a confirmed-absent file via `ls`, and verbatim cron expressions) —
all four match.
Closes #1277 same day it started, cleans up the subagent's own worktree using CIO's own `worktree-safety-sweep.sh` tool rather than leave it for a bulk sweep.

**~12:31 PM**: **Lead Developer** closes 6 more issues on PM's live In Review pass (#1649, #1571, #1543, #1648, #1542, #1492 —
#1648 verified against the GitHub artifact, not the chat claim) and names **THE CONVERGENCE**, echoing PM's own words ("capturing patterns, not whack-a-mole"):
#1617 fired a state change on a bare question with no affirmative token, while the #1631/#1650 family rejects a bare "yes" —
"no single arming contract;
tuning either side makes the other worse." Files the umbrella issue (#1739) to Arch (shape/sequencing) and CXO (what acceptance should feel like per tier).
Notes #1738 (a third member of the #1570/1736 family — the assistant reasons over its own rendered text) is in front of Arch via Exec.

**12:39 PM**: **Chief Architect** rules on Lead's predicate-as-single-source shape question: shape RIGHT —
the modeled-noun move (an acceptance is a per-seam noun) plus what Arch calls "ESSENCE commitment 5" reaching the seam layer —
with three sequencing conditions:
(a) input-adequacy before DESTRUCTIVE-adjacent adoption (a predicate fed no stored question returns confidence, not judgment), (b) adopt by EffectClass ascending, and (c) a shrink-only KNOWN_UNADOPTED ratchet so the contract is a chokepoint, not a convention.

**12:57 PM**: **Documentation Management** — Fire 4.
**The figure/figcaption spec closes out same day**:
Web implemented the in-body-teaser fix exactly per Docs' spec (`5cb3a93`), reusing the file's existing detector conventions, added 2 entries to the project's own 19-entry regression harness.
Docs verifies independently —
reads the actual commit diff (matches the described implementation precisely) and runs the real test suite personally rather than trust the report:
21/21 passing, both halves of Dispatch-PM's proposal now genuinely done (`fbfe813` hero, `5cb3a93` in-body).

**~12:49 PM**:
**Web** implements the in-body-teaser fix, reads `publish-post.js`'s existing standalone-italic detector and paragraph collector directly to confirm the described gap, reuses the same `it1`/`it2` regex-and-guard pattern for the caption side.
Catches and corrects a self-fabricated `website #1737` citation before committing (checked `gh issue list`, found no matching issue, cited the mail thread instead).
Runs the project's own `scripts/test-publish-post-corpus.js` (19→21 entries, all pass) rather than write a throwaway script.
Separately investigates — without fully resolving —
a genuine oddity:
4 untracked stray corpus-file copies discovered in the wrong (product) repo, ruled out as a symlink/mount artifact via `realpath`/inode comparison, mechanism undetermined;
removed as harmless.

**~1:00 PM**:
**Chief of Staff (Exec)**, working the same PM In Review round independently, closes the same 6 issues and reaches the identical convergence finding as Lead —
"a mechanism that accepts a question and rejects a `yes` has no arming contract, not a threshold problem" —
routed as one pattern per PM's own framing.
Files #1738 for Arch (Piper described its own truncated 6-to-5 render as an upstream data limit —
"it described its own render as an upstream result"), plus #1736 (chat read-back fabricates "No description" for an issue that has one) and #1737 (composer should scroll, not ticker-tape;
PM volunteered it).
Corrects two of Exec's own near-misses before acting:
nearly filed "the issue body was dropped" until `gh issue view 112` showed the body present (the write was fine, the read-back was false), and nearly re-described #1431 as open when it was already CLOSED by Lead's code verdict the day before.

**13:17 PM**: **CXO** — Fire 3.
Notes MVP fell 52→46 between the 07:17 and 13:17 fires and (at this point in the day, not yet corrected) treats the criterion-3 trigger as "days away, not weeks." Reads the code rather than the memos and corrects both Arch's and Lead's shared citation:
"strictness scales by EffectClass" is half the ratified law —
`decide_consent(effect, framing, mode, outwardness)` takes **two** axes, and outwardness was ratified PM+CXO+PPM on 08-15 on CXO's own argument (quoted in `shared_types.py`:
the ticket Jake didn't ask for was a plain WRITE, but the reason it could hold a release was that his teammates would see it).
An effect-only predicate collapses two structurally different acceptance bars into one —
concretely, `OUTWARD/WRITE/compose` and `OUTWARD/WRITE/ambiguous` both return the same verdict as their PRIVATE counterparts.

**13:17 PM**: **CXO** rules question-forms as a different speech act entirely —
"answer the question, never fire, never bare re-prompt" —
naming this as the error behind #1617 and, inverted, the re-prompt Exec caught in #1579.
Builds a per-verdict acceptance table anchored to the four `ConsentDecision` verdicts with deliberately no new vocabulary, and one hard rule:
a PROCEED_WITH_DISCLOSURE line must be declarative, never interrogative, or it manufactures a "yes" with nothing armed to receive it.
Flags arm-lifetime as an open **question**, not a finding — explicitly has not verified whether arms drop on topic change.

**13:22 PM**:
**PPM** triages the convergence (fully owned by Lead/Arch/CXO/Exec, no PPM ruling needed) plus #1736/#1737/#1738, verifying no collateral damage.

### Phase 4: PM's Epic-Factoring Directive and Lead's Intake-Rule Discovery (1:22 PM – 4:37 PM)

**~1:15 PM**: **Lead Developer** answers PM's "how am I blocking never-started work" question honestly: PM wasn't, Lead was.
The mechanism: inbound drained first every fire for two weeks meant "idle" never occurred, so the intake step never ran —
each fire locally correct, the sum wrong.
Starts a mechanical fix immediately: one never-started item gets a lane every fire, regardless of inbound; inbound triages around it.
Files Exec's factor-by-cause directive as consistent with this diagnosis.

**~1:20 PM**:
**Chief Architect** concedes CXO's two-axis correction same-day, naming the error class explicitly ("I cited 'strictness scales by EffectClass' as ratified law —
half the law...
cited law from memory of its shape, not its signature") — amends condition (b): the predicate takes both axes;
outward WRITEs accept at the DESTRUCTIVE bar.

**14:11 PM**: **Coding Agent (prog)**, delegated by Lead, builds #1739 (the acceptance contract) per both governance passes —
`evaluate_acceptance(message, *, effect, outwardness, armed_question, taught_accepts)` returning ACCEPT/DECLINE/STATE_QUESTION/PASS, two-axis tiering (DESTRUCTIVE-any-outwardness and WRITE×OUTWARD → strictest NAMED_OBJECT tier;
READ and WRITE×PRIVATE → LOW_CEREMONY), an input-adequacy guard refusing NAMED_OBJECT accepts against a falsy armed question, and a shrink-only KNOWN_UNADOPTED ratchet with a watched red-proof (a planted call to the legacy detector is caught and named by test, then removed).
Absorbs #1650 as a delegate over the new predicate.
Ships READ-tier adoption at the #1617 standup site (PM's verbatim "are we done with that standup?" now pinned to a status-answer response that stays in REFINING) plus the generic offer seam and the #852 contextual last_offer binding.
Test evidence: 3,807 + 53 + 597 + a targeted 656-test sweep, all passing;
DESTRUCTIVE-adjacent tier deliberately deferred, not adopted this lane.

**~2:30 PM**: **Lead Developer** confirms #1739 built and both governance passes honored —
"the never-started counter moved on its first fire under the new intake rule —
filed at noon, built by mid-afternoon." Next queued: #973, then #1732, then PPM's ordered 28.

**15:31 PM**: **Lead Developer** — intake rule, second consecutive fire honored:
#973 lane running (the 97-day elder per Lead's own earlier note;
verify-first mandatory since its premises predate the disposal campaign).
Files one cc — Exec's sprint-shape directive to PPM/Arch (Product Backlog default, ordered epics) —
as consistent with the same intake diagnosis.

**16:1x PM**: **Coding Agent (prog)**, second delegation, runs a verify-first freshness audit of #973 (created 2026-04-13 —
149 days old, not the 96 days an earlier note had assumed, and milestoned Production, not MVP).
Finds the issue's whole premise superseded by #984 (CONTEXT-CACHE, closed 2026-05-12) —
`ContextCache` already implements Redis TTL caching across 11 gatherers/helpers, richer than the original ask.
Corrects a live falsehood in the module docstring ("not implemented yet," wrong for 4 months, also quoted stale into `five-layer-context-mapping.md`).
Executes only the doc-only residue (docstring correction + per-request notes on the deliberately-uncached methods), zero behavioral change, and recommends closing #973 as superseded —
the AC2 stable-content-first premise is moot under the current per-source-cache architecture, not executed.

**~4:00 PM**: **Lead Developer** closes #973 accordingly (verified 49 tests, pushed), correcting his own prior sequencing note —
the wrong pile by milestone meant the intake rule's second pick was off-target, but the issue's actual substance (a 4-month-stale docstring falsehood) still needed the fix it got.

**~1:00 PM (parallel to the acceptance-contract thread)**: **Chief Architect** executes PM's live epic-factoring directive:
pulls the live sprint truth (49 not-done / 37 Sprint Backlog), classifies all 37 into 8 cause-groups + 7 honest singletons, states the cousins are load-bearing for 10 items (arguably 18 counting the acceptance-contract control case), refuses to force the remainder into groups ("taxonomy theater"), sends dependency notes to PPM (acceptance-contract first, security before beta, #1687 named as "the quiet tax") with Lead deliberately not cc'd per PM's protect-Lead's-attention directive.

**15:37 PM**:
**Chief of Staff (Exec)**, working the same afternoon, self-corrects two throughput numbers given to PM earlier the same day —
MVP closures average ~25/week historically (not the 4-7 figure Exec had quoted, "a narrow recent window presented as steady state"), and the 08-31 collapse to 7-11/week isn't misdirected effort (MVP stays 82%+ of all closures) but plausibly verification-gating during PM's absence, stated as a falsifiable hypothesis rather than an asserted cause.

**16:07 PM**: **HOST** — Fire 4.
Routine hygiene:
`MEMORY.md` drift detected (one new memory file from another agent, not a stale hand-edit), regenerated clean (191 entries).
Logs PM's four backlog/epic directives landing and Exec's same-day self-correction of both throughput numbers.

**16:17 PM**: **CXO** — Fire 4.
Catches her own fabricated trend from three hours earlier: at 13:17 she wrote MVP "fell 52→46… days away, not weeks";
by 16:17 MVP is back up to 49.
Names the error precisely — extrapolating a direction from two points three hours apart —
and notes Exec made the identical error on the same metric the same afternoon, independently, calling it evidence the pull is in a visibly-moving metric, not either individual's carelessness.
Fixes both her own state files with a rule: re-read the count every START, don't carry a remembered number or a remembered direction.

**16:22 PM**: **PPM** — the day's largest deliverable.
Builds `dev/active/mvp-epic-order-2026-09-09.md`:
37 items ordered into 8 dependency-ranked epics + 6 singletons, re-verifying Arch's count and membership independently before ordering (matched exactly), running a bounded closeable-items audit across the 6 singletons plus #1522 (found nothing, explicitly stated as a partial check, not a clean bill of health for the whole backlog), and naming PPM's own scope-guard role as an open mechanism question rather than solving it alone —
"standing up a 'PPM reviews weekly' habit today would be exactly the failure shape everyone just spent the afternoon diagnosing." Adopts PM's fourth directive (protect Lead's attention, route non-Lead-specific items through PPM/PA) explicitly.

**16:37 PM**: **CIO**, reading the same directive thread as a cc (not directly addressed), offers a scope-guard chokepoint sketch —
deliberately not a finished design, since Arch owns most of the infrastructure it would live in.
Applies methodology-53's own test ("Chokepoint vs.
Bolt-On —
Attach the Obligation to Something That Can't Be Skipped"):
hook the check to a merge-to-main (already mandatory, already CI-gated) rather than a new periodic duty.
Explicitly names what's left open (GH Action vs.
duty-cycle-tick step is Arch's infrastructure call; the named consumer;
false-positive tuning), files as standing-item 7t, proposes joint design with Arch, no timeline committed.

### Phase 5: Epic Order Live, Scope-Guard Accepted, Flywheel Round Closes (4:17 PM – 7:22 PM)

**18:1x PM**: **Coding Agent (prog)**, third delegation, ships both items at the top of PPM's newly-ordered epic list.
Item 1, **#1734 [SECURITY]**:
verifies the filing's claims first (`personality_integration.py` ignores `user_id` entirely and writes the shared global config file;
the PUT route has no auth dependency), chooses the smallest-diff shape —
admin-gate the PUT via the existing `require_admin`/#1508/#1598 idiom, leaving GET and the read-only `/enhance` untouched —
and ships 7 new pinned tests (non-admin 403 with the overlay hash provably unchanged, no payload echo in the 403, unauthenticated 401 before admin lookup, admin PUT 200 and persists).
Item 2, **#1637**: reproduces the issue's 2026-08-16 claims before touching anything —
the 6 standalone failures still reproduce exactly;
the combined-run cross-contamination poisoning **no longer reproduces** on this commit (A/B'd both ways, 4,036–4,042 passed either way).
Fixes all 6 standalone failures individually (all stale pins or test bugs, zero product-code changes) and hardens a collection-time `TestClient` module-level side effect —
the exact shape that made the original poisoning possible — even though the poisoning itself had already drifted away.

**18:31 PM**:
**Lead Developer** confirms #1734 and #1637 both closed (verified 4,042 combined tests + 49 architecture-ratchet tests, pushed) —
"five never-started/standing items moved in one day": #1739 built, #973/#1734/#1637 closed.

**18:39 PM**: **Chief Architect** replies 6/6 to the afternoon's threads:
**accepts the scope-guard joint design** with Arch's own added sequencing condition (a new Action doesn't join a standing-red channel until #1687's CI-red fix lands);
rules the named-consumer question as *the* design question —
the Action's output must be a mailbox memo (the one surface with mandatory verified drain) not just an issue comment, with advisory-first status measured for two weeks;
names CXO as cousin-1's copy owner with #1717 as the acceptance test;
notes CXO's cousin-4 offer (the Decline class has a worked case, with a copy-shaped risk flagged).

**19:07 PM**: **HOST** — Fire 5.
Logs PPM's ordered-epic file (re-verified 37-item membership independently, bounded audit found nothing and said so explicitly) and CIO's chokepoint sketch, explicitly offered as co-design rather than a unilateral ship.

**19:17 PM**: **CXO** —
Fire 5, off the epic ordering fifth but delivered same-day per her own stated seat rule (name the user-facing-contract owner before the copy gets written, and the acceptance test is live right now).
Delivers `docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`, and in writing it finds the audit's own framing wrong:
aggregation for N-failed-slices already exists —
in the deterministic composed-orchestrator path (`_combine_results:280–291`, one note, topics comma-joined) —
but **not** in the floor's directive path (five LLM-instructed sites that don't aggregate at all).
The epic is "unify two mechanisms;
a half-adopted model here yields two differently-honest voices in one product," not "add a new rule." Re-diagnoses Exec's earlier live case (a caveat rider on a succeeding turn) as a **reportability** defect, not an aggregation defect —
the composed path already emits one sentence for N topics, so fixing aggregation would leave the actual bug untouched.
States the core rule this reframes: "a failure is reportable iff, had it succeeded, its content would have appeared in THIS answer" —
and warns that hedging a `verified_empty` claim is its own dishonesty, "the same failure wearing humility."

**19:22 PM**:
**PPM** folds both the accepted scope-guard design and CXO's mechanism correction into the epic-order document same-day rather than let a second source of truth form.
Sends an ack to CIO/Arch cc CXO/Exec/PM, verified landed.

**21:57 PM**: **Chief Architect** — STOP.
**Flywheel challenge round CLOSED at EOD as scoped**: D4 concur-with-data, D2 unopposed, all first-wave amendments applied via v3.0.2.
The final v3 ratification text is deliberately deferred to tomorrow's START —
a **named trigger** ("a ratification-grade document deserves a fresh pass, not tail-of-marathon work"), not an unnamed deferral.
Same fire: CXO delivers the cousin-1 contract with a real structural finding (GatherOutcome has two delivery mechanisms —
five LLM-directive floor sites plus the orchestrator's deterministic composer —
and must reach both or the product ships two differently-honest voices, carried into the epic sketch's inputs).
Sign-off clean; cron re-armed (`240711fd`→`360c96ae`).

### Phase 6: Evening Close — Vercel Blocker, Retractions, Day-Arc Wrap (7:17 PM – 10:22 PM)

**19:17–22:17 PM**: **CXO** — Fires 5–6.
Self-audits PM's protect-Lead's-attention directive against her own two days of mail: 9 memos reached Lead's inbox in two days.
Honest split —
3 needed him (the voice-watch review he acted on in 3 hours, the acceptance pass, the FTUX copy call), 1 courtesy ack that could have been three lines, and 1 clear miss (the `mail-send.sh` false-positive routed to Lead when it should have gone to CIO with Lead only cc'd).
Writes a seat rule into the carry-forward: before addressing Lead, ask whether he must *act* — "he wrote it" is a cc, not an addressee.
Notes cc'ing isn't free either (4 of the 9 were cc's).

**22:17 PM**: **CXO** — Fire 6.
Investigates her own open question rather than route it to Lead:
verifies arms live exactly one turn (`intent_service.py:1072` pops unconditionally, before classification), no TTL (plain instance dict), in-process only —
and that this is documented as deliberate in `peek_pending_offer`'s own docstring.
Retracts her own §5 recommendation before Lead could build a redundant topic-change guard on top of behavior that already drops unconditionally —
"had Lead built to my §5 he'd have added a drop-on-topic-change condition to a system that already drops unconditionally." Separately rules out multi-worker state loss as the #1694 mechanism by config (`uvicorn.Config` passes no `workers`;
`fly.toml`: "Single-machine app"), reporting the dead theory rather than the plausible one she'd been chasing.

**20:32 PM**: **Chief of Staff (Exec)** — STOP.
**9 MVP issues closed today** (verified against a full 400-issue pull, not a truncated one that first under-reported) —
the most in a single day since the throughput collapse began (#1492/1542/1543/1571/1635/1637/1648/1649/1734).
MVP: 47 not done (35 Sprint Backlog, 3 In Progress, 9 In Review), 1,129 done, **zero unmilestoned**.
Confirms Lead's own diagnosis beat Exec's three attempted explanations:
"reactive work crowded out intake, one fire at a time, invisibly —
each fire locally correct, the sum wrong." Resolves half of a PM/Pard Vercel-routing question directly via `curl -sI` on both hosts (website is Vercel, beta app is Fly, one ceiling can't take down both), routes the harder half (what actually runs out, how close) to Web.
Own scorecard: 3 throughput numbers given to PM today, 2 retracted — "PM's single nudge got an answer my memo hadn't."

**21:22 PM**: **Piper Alpha (PA)** catches a silently-dead cron job (`CronList` returns zero jobs —
Gap-C, the known compaction-can-kill-it failure mode) and re-arms it (`e0cd56b5`) before doing anything else this fire;
otherwise quiet since the 19:00 informational fire (PPM's epic-order build-out, CIO's scope-guard sketch —
nothing owed to PA either time).

**21:47 PM**: **Lead Developer** — day close. Inbox zero, 19 merged today.
Names the day "the densest intake day yet":
contract built, 4 items closed, a real gap sealed, the flywheel round answered, cron rotated.
Next fires queued: epic 1 remainder, then #1732 (chat-render sanitizer), down PPM's order.

**21:52 PM**: **Web** — STOP.
A final mail sweep surfaces Exec's relayed Vercel question (Q1: which resource, how close, what happens at the ceiling).
Checks what's actually available before replying rather than guess or silently defer —
no Vercel CLI, no auth token, no usage documentation in either repo —
names this as a genuine access blocker, not a deferral of convenience, and states precisely what would unblock it (PM's own warning screenshot, or dashboard credentials).
Matches PM's own "next-working-day, not tonight" framing rather than manufacture false urgency.
Adds it as standing item #4 — a real, named blocker.

**22:07 PM**: **HOST** — Fire 6, STOP. Names the day "calmer...
appropriately" —
the flywheel round converged before HOST's own first fire, and the rest of the day was verification of others' claims (v3.0.2's actual table content, CIO's repro-attempt report, PPM's epic-order build) rather than new HOST-originated findings.

**22:22 PM**: **PPM** — STOP. One mail item (CXO retracting the arm-lifetime flag, pure Lead/Arch build domain, no PPM action).
Names the day's throughline: every substantive claim today —
PM's own throughput correction, CXO's GatherOutcome finding, PPM's own #1731 boundary-check —
was verified against a primary source (git log, live board pulls, an actual code read) before being acted on or repeated.
`sprint-truth.py` at close: MVP 47 not done, 1,129 done, 0 unmilestoned.

**21:12 PM**: **Communications** — day close.
Standing state: 12 drafts in the queue (unchanged from yesterday), all awaiting PM's voice-pass;
"Piper Morgan Eras" runs Saturday 9/12, "Who's Who at Piper Morgan" runs Sunday 9/13;
the ChicagoCamps talk remains PM-gated, no dry-run signal since Sep 5.

**~4:37 PM (log ends without a STOP entry)**:
**CIO**'s log stops after the 16:37 fire, whose own text says "Not a STOP fire (22:07 remains today)" —
but no further entry, and no `DAY-CLOSED: 2026-09-09` marker, exists in the file as provided.
A logging continuity gap, not a work gap:
every other role's cross-references to CIO's afternoon and evening work (the scope-guard sketch, the #1731 repro attempt, closing #1277) are independently corroborated by PPM's, HOST's, and Arch's own logs.

**(ongoing at synthesis time)**:
**Documentation Management**'s own log for today (this omnibus's synthesizer) had not yet reached its 21:57 fire's day-close entry at the time this log was compiled —
by design, per the task's own framing, not a gap.

---

## Executive Summary

### Core Themes

- A four-day-old cross-role challenge round (the Excellence Flywheel re-evaluation) closed today:
D4 conceded with usage data, D2 unopposed, the table-vs-footer defect CXO caught overnight fixed before HOST's first fire —
with the actual v3 ratification text deliberately deferred to tomorrow on a named trigger rather than rushed at the tail of the round.
- A cross-project accessibility proposal (Dispatch-PM's figure/figcaption markup fix) moved from report to fully-shipped-and-tested in one day across three roles, with the receiving role (Docs) independently verifying the implementing role's (Web's) work by reading the diff and running the suite personally rather than trusting the report.
- Three roles (Lead, Exec, and independently Arch/CXO on the mechanism) converged on the same acceptance-contract diagnosis from PM's live testing round the same morning —
PM's own framing ("capturing patterns, not whack-a-mole") named the discipline before the fix existed, and it was built same-day.
- PM's real-data correction of Exec's throughput narrative reshaped the rest of the day:
four directives fanned out to PPM (epic ordering), Arch (six-cousin factoring), CXO (protect-Lead's-attention self-audit), and CIO (scope-guard chokepoint), each landing same-day.
- Two roles (CXO, Exec) independently made and then caught the identical statistical error —
extrapolating a trend from two data points hours apart —
on the same MVP-count metric, in the same afternoon, each catching it themselves before repeating it further.
- Governance roles found and routed genuine defects in shared tooling this week rather than treating tooling as out of scope for content-focused work:
CXO found and routed a real `mail-send.sh` structural false positive to Lead;
CIO applied its own `worktree-safety-sweep.sh` tool to its own dispatch's leftovers rather than leave cleanup to a bulk sweep.

### Technical Details

- **Ship #059 published** (`d983687`) with a genuine deploy-propagation false-negative (stale-cached "Ship Not Found" behind a live 200) diagnosed via response-header comparison against a known-good post, not accepted on status code alone.
- **Sitewide dark-mode bug fixed** (`70791c3`):
a Tailwind class referencing a token (`dark-bg`) that has never existed, silently compiled to nothing since the site's first commit —
10 occurrences across 8 files, confirmed via compiled CSS output, not just a clean build.
- **Figure/figcaption accessibility fix shipped in two halves** (`fbfe813` hero, `5cb3a93` in-body teaser + 2 new regression-corpus entries, 21/21 passing) —
root cause was source-adjacency in the markdown, not renderer drift.
- **#1739 (acceptance contract) built**:
one predicate, two-axis strictness (EffectClass × Outwardness), an input-adequacy guard, a shrink-only adoption ratchet with a watched red-proof, READ-tier absorption of the #1617 standup site and the #852 contextual last_offer binding;
DESTRUCTIVE tier deliberately deferred.
- **#1734 [SECURITY] closed**:
personality-config PUT admin-gated to stop any authed user from clobbering the shared global config file, with 7 new pinned tests.
- **#1637 closed**: all 6 standing test failures fixed as stale pins/test bugs (zero product-code changes);
the 08-16 combined-run poisoning no longer reproduces, but the collection-time `TestClient` side effect that made it possible is hardened anyway.
- **#973 (149 days old, not 96 as an earlier note assumed) closed superseded-by-#984**, correcting a 4-month-stale "not implemented yet" docstring falsehood.
- **CXO's aggregation-guard gap closed structurally** (`3215e64e5`):
a single registry now derives both the gate and its own tests' denominator, making the original critique unstatable rather than merely patched.
- **`mvp-epic-order-2026-09-09.md` built**:
37 Sprint Backlog items, independently re-verified, ordered into 8 dependency-ranked epics + 6 singletons with a stated reason per position.
- **Scope-guard chokepoint jointly designed** (CIO sketch, Arch acceptance): hooks to the merge-to-main CI gate;
output is a mandatory-drain mailbox memo to PPM, not an issue comment; advisory-first for two weeks.
- **`gather-outcome-user-facing-contract-2026-09-09.md` delivered** (CXO):
finds aggregation for N-failed-slices already exists in the composed-orchestrator path but not the floor's directive path —
reframes the epic from "add a rule" to "unify two mechanisms." - **#1277 (canonical-ops-recipes) closed same-day** via a worktree-isolated subagent whose load-bearing claims were independently spot-verified (exact line numbers, a live `gh run list` run) before merge.

### Impact Measurement

- **9 MVP issues closed today** (Exec's count, verified against a full 400-issue pull) —
the most in a single day since the throughput collapse began.
- MVP backlog closed the day at **47 not done / 1,129 done / zero unmilestoned** (opened at 52 not done, 0 unmilestoned).
- Sprint Backlog moved **28 → 34** over the morning even as 6 issues closed —
several of the new arrivals came out of PM's own testing round.
- In Review dropped **15 → 9** on PM's live testing pass.
- **5 never-started or standing items moved in one day** under Lead's newly-mechanized intake rule:
#1739 built, #973/#1734/#1637 closed.
- Figure/figcaption regression corpus grew from 19 to **21 entries, all passing**.
- #1739's implementation alone carried **3,807 + 53 + 597 tests passing** across the touched surfaces;
#1637's fix verified **4,042 passed, 0 failed** on the previously-poisoned combined run;
#1734 shipped with **7 new pinned tests**.
- CIO's #1277 closed same-day after **7 days of correctly-reasoned prior deferral**.
- Real throughput baseline corrected:
MVP closures average **~25/week historically**, not the 4–7/week figure both Exec and an earlier CIO draft had used.
- Comms' publishing queue held steady at **16 draft files** in the pipeline, all linked, unchanged in count from yesterday.

### Session Learnings

- **"A correction not committed has not happened" got a textbook instance**:
v3.0.1 recorded a fix in an amendment note while the table it corrected stayed wrong —
caught by a peer who opened the file instead of trusting the memo (CXO), independently reconstructed in full by Exec's own account of the same sequence.
- **Verifying a peer's claim against the source, not the memo, repeatedly produced findings the memo alone would have missed** —
CXO on Lead's registry fix, CIO on a subagent's line-number citations, Docs on Web's implementation diff, PA on the MCP subprocess boundary, HOST on CXO's own table-vs-footer claim.
- **Two independent, same-day self-corrections of the identical statistical error** (a trend from two points, hours apart) on the same metric argue the pull is structural to a visibly-moving count, not a lapse specific to either role —
both roles caught it themselves before the wrong conclusion propagated further.
- **A false alarm that repeats is a defect, not a re-confirmed non-issue** —
CXO's second encounter with the same `mail-send.sh` STRANDED warning prompted reading the code instead of re-refuting the symptom, surfacing a real structural false-positive class (MANIFEST.md's dual-directory existence, not a moved-memo detection failure).
- **Deferring a document with a named trigger, mid-victory, held under real pressure** —
Arch closed the flywheel round today but explicitly pushed the final v3 text to tomorrow's fresh session rather than draft it at the tail of a long day.
- **A discipline can retract itself before it ships** —
CXO investigated her own open question rather than route it to Lead, found the answer inverted her own recommendation, and retracted it before anyone built the (unneeded) fix.
- **PM's protect-Lead's-attention directive produced a same-day, quantified self-audit** rather than a vague behavioral promise —
CXO counted her own memos to Lead and split them honestly into needed/borderline/miss;
PA independently saved the same directive to memory the moment it landed, naming it the mirror image of an existing standing rule.
- **Governance-lane role boundaries held under real pressure to help**:
PPM and PA both explicitly declined to claim #1731's repro work despite having fresh relevant context, on the same stated principle (governance surfaces are mail and standing items, not infra investigation just because context is fresh) —
and when CIO did attempt it, an honest negative result was reported rather than a false close or an over-extended chase.
- **A logging continuity gap surfaced by omission, not contradiction**:
CIO's log ends mid-day with no STOP entry despite its own text anticipating a later fire —
a reminder that "no DAY-CLOSED marker" is itself informative and shouldn't be silently smoothed over in synthesis.

---

## Notable Discrepancies and Gaps (preserved per Step 2.6)

- **CIO's session log has no day-close entry.** The log ends after the 16:37 fire, whose own text says "Not a STOP fire (22:07 remains today)" — but no further entry, and no `DAY-CLOSED: 2026-09-09` marker, exists in the file as provided. Every other role's cross-references to CIO's afternoon work (the scope-guard sketch, the #1731 repro attempt, closing #1277) are corroborated independently by PPM's, HOST's, and Arch's own logs, so the day's substance is not in doubt — only CIO's own record of closing the day is missing.
- **No factual contradictions found** between roles on the day's two headline threads (the Ship #059/figure-figcaption arc and the flywheel round closure). Comms', Docs', Web's, and Exec's independent accounts of the figure/figcaption handoff agree on sequence, commit hashes, and disposition of both halves. Arch's, CXO's, HOST's, and Exec's independent accounts of the flywheel table-fix agree on the v3.0→v3.0.1→v3.0.2 sequence and on D4/D2's resolution.
- **CXO's own log flags and corrects its own error inline** (the 13:17 MVP-trend fabrication, retracted at 16:17) — preserved here as a session learning rather than treated as an inter-role discrepancy, since CXO is the same role catching its own claim, and Exec independently made and caught the same error class the same afternoon on the same metric.

---

## Sources

- `dev/2026/09/09/2026-09-09-0603-comms-code-log.md` (Communications)
- `dev/2026/09/09/2026-09-09-0609-docs-code-log.md` (Documentation Management)
- `dev/2026/09/09/2026-09-09-0639-arch-code-log.md` (Chief Architect)
- `dev/2026/09/09/2026-09-09-0647-lead-code-log.md` (Lead Developer)
- `dev/2026/09/09/2026-09-09-0649-web-code-log.md` (Web / Unicorn Web Designer)
- `dev/2026/09/09/2026-09-09-0700-pa-code-log.md` (Piper Alpha)
- `dev/2026/09/09/2026-09-09-0707-host-code-log.md` (HOST)
- `dev/2026/09/09/2026-09-09-0717-cxo-code-log.md` (CXO)
- `dev/2026/09/09/2026-09-09-0722-ppm-code-log.md` (PPM)
- `dev/2026/09/09/2026-09-09-0902-exec-code-log.md` (Chief of Staff / Exec)
- `dev/2026/09/09/2026-09-09-1037-cio-code-log.md` (CIO)
- `dev/2026/09/09/2026-09-09-1411-prog-code-log.md` (Coding Agent, delegated by Lead — #1739 acceptance contract)
- `dev/2026/09/09/2026-09-09-1534-prog-code-log.md` (Coding Agent, delegated by Lead — #973 freshness audit/close)
- `dev/2026/09/09/2026-09-09-1832-prog-code-log.md` (Coding Agent, delegated by Lead — #1734 + #1637)

**Cross-reference gate (Step 2.5)**: all roles mentioned across the 14 source logs (Lead, Docs, Arch, CXO, CIO, PPM, Exec, HOST, PA, Comms, Web) are represented in the source set. Two additional names recur throughout (Dispatch-PM, Pard) — both are cross-project/external parties without Piper Morgan duty-cycle session logs of their own, consistent with every log's own treatment of them as mail correspondents, not gaps in the source set.

**Canonical references verified verbatim against source (Step 7)**: m-43 — "Name the Layer — We Verify the Proxy Nearest to Hand, Not the Claim" (`methodology-43`); m-44 — "'Clear' Is Not a Measurement — An Instrument Must Assert What It Looked At" (`methodology-44`); m-52 — "Open It — A Summary Is Not Its Contents" (`methodology-52`); m-53 — "Chokepoint vs. Bolt-On — Attach the Obligation to Something That Can't Be Skipped" (`methodology-53`); ADR-075 — "Configuration / Personalization Ownership — Per-User Scoping for Instance Config" (referenced by Web regarding the #1734 fix's deferred per-user data model).



