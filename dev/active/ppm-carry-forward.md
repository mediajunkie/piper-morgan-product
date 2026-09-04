# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-09-04 07:22 PT (START). **Still watching**: #1386 — **only criterion 6
(PM sign-off) genuinely remains open**; 2/4/5 confirmed closed, 1 text-stale but functionally
satisfied. **#1688's overrule call also still open** — see below.

## ✅ SHIP #059 SENT SAME-DAY + ROLE-PORTFOLIO REFRESHED (2026-09-04 07:22)
Window Fri Aug 28–Thu Sep 3. Wrote it this fire rather than defer (no other blocking work, "every
hour earlier" framing from the kickoff) — pulled the actual `sprint-truth.py` trajectory and
day-summary content from all seven session logs in the window rather than work from memory. Also
did the Rule-5 `ROLE-PORTFOLIO-PPM.md` refresh the review triggers by construction — replaced the
whole §2 table (was dated 08-28). Sent `7c9328288` / `10bbb96fa`, both verified landed. **Nothing
further owed on either.**

## 🟡 #1688 SHIP CALL — HOLD, Arch (the precedent's own author) concurred fully, PM overrule still open (2026-09-03 22:22)
Arch concurred with the HOLD ruling below, including the hardest part of the reasoning (a frozen
surface being the only currently-buildable one is precisely when the freeze does its work, not an
exception to it). Added a useful framing: the merged-not-deployed build isn't wasted — the
interview mechanism transfers to MCP once its infra exists, and the Web presentation sits ready if
that surface's status is ever revisited. **PM's overrule call remains explicitly open** — nothing
further from PPM unless PM rules the other way. Worth a fresh read at next START in case PM
responded overnight.

## 🟡 #1688 SHIP CALL — RULED HOLD, PM flagged explicitly for possible overrule (2026-09-03 19:22)
Lead built the web-chat half (MCP half verified unbuildable — no served MCP server exists yet) and
flagged a real tension: my own 08-29 MCP-only narrowing of #1688 assumed MCP was buildable now,
which turned out false, so the actual choice was Web-or-nothing, not Web-or-MCP. CXO (author of
that narrowing) agreed the premise was false and offered a real counter-argument for shipping
anyway, explicitly not neutral, explicitly deferring to my ruling.

**Ruled HOLD**, applying Arch's own #1658 precedent (same freeze, "did this UI exist in the
running system yesterday" test) rather than reasoning fresh — #1688's interview never ran in
production, same as #1658's UI, same disposition for consistency. Addressed CXO's counter-argument
directly rather than overriding it silently: the false MCP-buildability premise doesn't repeal the
freeze's actual subject (new capability investment in web-chat), and the 08-31 hosted-primary
ruling settled *where* testers go, not that primary surfaces get freeze exceptions. **Explicitly
flagged to PM that this is closer than #1658 and named the real cost of holding (broken first
impression on the now-primary surface)** — inviting an overrule rather than treating my own
consistency argument as automatically correct. Build stays merged, not deployed; nothing else
depends on it. Posted on #1688 and sent to Lead/CXO/Arch/PM (`2c0c0a196`), verified landed.
**Watch for PM's word — this could go either way and I said so.**

## ✅ #1688 SCOPE RULING — cross-session recall is 1705's, not this increment (2026-09-03 16:22)
CXO's v0.2 FTUX copy for #1688 contained a promise (`why_asking`: "I'll hold onto it and bring it
back next time") the increment doesn't build — caught by CXO themselves, routed to me and Lead as
a scope question rather than guessed at. **Resolved cleanly against my own C5 sequencing**:
cross-session recall is #1705 (Leg D increment 6, "same Piper" memory) — a distinct, later
increment for a real architectural reason (memory is harder than the auth/catalog work increment 1
needs first), not an arbitrary split. #1688's own scope (increment 1, cold-start reflection) never
included persistence. **Ruling**: cut the promise, ship the question alone — matches CXO's own
stated fallback. Posted on #1688 itself and sent to Lead/CXO/Arch/PM (`fa6080b75`), verified
landed. Named explicitly why NOT to pull #1705's scope forward to save the string (violates the
sequencing's own logic, textbook scope creep the no-optional-complexity lens exists to catch).

## ✅ #1720/#1721 TRIAGED PROACTIVELY — Weekly Docs Audit findings, both Ongoing/FLYWHEEL (2026-09-03 10:22)
Found via `sprint-truth.py`'s unmilestoned count drift again (17→18), same discipline as this
week's #1718/#1719. Both from today's Weekly Docs Audit #1712. **#1720**: two public-facing user
guides reference a class retired by #1289 with copy-pasteable code that would literally
`ImportError` — flagged as a different risk shape than internal doc drift (external developer
impact) without escalating priority on that basis alone; owner question (needs
`StandupOrchestrationService`'s real interface confirmed first) correctly left to Lead/feature-owner.
**#1721**: 5 missing onboarding screenshots in `ALPHA_TESTING_GUIDE.md` — **directly connects to
my own #1708 close-out**, where I'd already flagged that doc as "not yet audited for the
hosted-primary change." Recommended folding into that eventual pass rather than a standalone
screenshot-capture task, since the wizard walkthrough moved to CONTRIBUTING.md and the guide's own
scope may need to change first. Both milestoned Ongoing/FLYWHEEL, board-added, verified no
collateral damage.

**Quiet close today**: no new state past the 16:22 entries above (#1717 verification, #1718,
#1719). Both #1718 and #1719 are freshly triaged, nobody has acted on them yet — normal, not a
gap.

## ✅ #1719 TRIAGED PROACTIVELY — cohort tooling debt, Ongoing/FLYWHEEL (2026-09-02 16:22)
Found via `sprint-truth.py`'s unmilestoned count again (17→18), same discipline as #1718 this
morning. Cross-ref-drift-after-file-move recurring 4th time, filed per Monthly Housekeeping
Audit's own "3+ recurrences → structural fix" rule. Not a product/feature question — cohort CI
hygiene. Milestoned **Ongoing**, Sprint **FLYWHEEL - Process improvement**. Mechanism choice
(widen lychee's watched paths vs. a pre-move grep check) explicitly routed to Arch/Lead, not
decided here — the issue itself correctly declined to pick.

## ✅ #1718 TRIAGED PROACTIVELY — real tester-affecting bug, MVP/Beta Blockers (2026-09-02 10:22)
Found by checking `sprint-truth.py`'s unmilestoned count myself (17→18), not from mail — an empty
inbox isn't the same as nothing needing triage. LLM key-validation discards the specific failure
reason (auth-invalid vs. no-credits both show flat "invalid"), affecting a named real alpha tester
(Rebecca Refoy) at first-contact. Checked #1414 (same class, honest API-key error messages) for
precedent — MVP, closed — and matched it: **MVP / Sprint Backlog / Beta Blockers - Hard Gates
Only**. Fix direction in the issue (route existing `ValidationResult.error_message` through the
already-built `user_friendly_errors.py` translator) doesn't need a product call. Posted triage
comment, no mail needed (nobody routed this to me, no thread to reply into).

## ✅ #1717 VERIFICATION IN — my milestone/urgency call confirmed correct, no revision (2026-09-01 22:22)
Lead ran the cheap verification same-fire: predicted litany never materialized (6/6, both
providers) — both models already aggregate the five honest-degrade directives into one sentence.
Found three subtler wrinkles instead (scope leak in the one-flag case, an unverified reassurance
claim, unstable category naming). CXO explicitly reaffirmed: MVP/not-urgent needed no revision,
the two small fix directives ride whatever next touches the floor. **Closed — nothing further
owed.**

## ✅ #1717 TRIAGED — honest-degrade directive composition risk, MVP/not-urgent (2026-09-01 16:22)
CXO's voice-watch found five independent `source_failed` directive sites in
`conversational_floor.py` that compose additively with no cap — a plausible (unverified) Tone
failure if multiple lookups fail in one turn ("I couldn't check X, and I couldn't check Y..." vs.
one honest sentence). Explicitly routed the priority call to me and Lead. Milestoned **MVP**
(matches #1425/#1645 family precedent, live-surface voice-quality risk, fits maintenance-mode
bug-fixing scope), Status **Product Backlog** (not urgent — CXO's own framing, and the failure
mode is still structural reasoning, not an observed reply). Posted the disposition on the issue
and confirmed to CXO/Lead/Arch. **Next actual step is Lead's**: a free structural render + one
floor call to see what the model really produces before any fix.

## ✅ PDR-005 TAXONOMY CITATION — closed same-fire (2026-09-01 07:22)
CXO routed a real, small gap: PDR-005 (my own PDR) never cited the ratified surfaces taxonomy at
either "5 of 7 surfaces" roster mention, despite the taxonomy's own text naming this exact
omission as the mechanism behind the old "Surface 3 is a phantom" confusion. Verified CXO's
proposed wording against the taxonomy doc myself (ratification date, Surface 3 = F-Settings) before
applying — both checked out. Fixed at PDR-005:74 and :131 (`77ebb77b7`), confirmed to CXO/Arch/PM.
**Nothing further owed.**

## 🔵 CT v2.4 corpus-tagging + methodology proposal — fully closed between Lead/CXO, informational only (2026-08-31 22:22)
Lead executed CXO's `context_requirement` tag spec same-day: 61/61 queries tagged, zero
unresolved, distribution 49 required / 2 optional / 10 not_applicable. CXO adjudicated the two
flagged rows and corrected their own §7 tie-break reasoning (the reason was wrong, the tie-break
itself survived). Real product finding worth remembering if it comes up later: the canonical
corpus is 80.3% `required` (cannot be answered by an access-less LLM) — a differentiation argument
stated as a measurement. CXO separately proposed "misfiled is not deferred" (this same case: a
four-month rubric-filed item that was actually one day of corpus-tagging work, sitting because the
filing named the wrong door) as a candidate methodology entry, addressed to Exec — not mine to
rule on, no PPM action either thread.

## ✅ #1166 RE-GATED — dead "post-M3" trigger fixed, no PDR opened (2026-08-31 16:22)
Arch flagged (via CIO's standing-items audit) that #1166's (Type-2 Dreaming discovery-spike)
kickoff gate — "awaiting M3 ship" — can never fire since M3/M4/M5 were swept 07-04/05. Checked:
the underlying dependency (persisted memory) was actually satisfied when M3's own scope shipped in
early June — the gate died on a label, not on its real condition. Posted the re-gate directly on
the issue (per Arch's own framing — "same bucket as other post-beta re-triage items" is a complete
answer): milestone stays Production (already correct), trigger corrected to "re-triage at
MVP-close" like everything else deferred this way, PDR deliberately not opened now (current build
effort is MCP-path-first per ESSENCE v1.0; this is discovery-spike work for a speculative
feature). 2026-06-08 three-lens convergence preserved, doesn't need redoing later. **Closed —
nothing further owed.**

## ✅ #1708 THREAD FULLY CLOSED — Docs verified independently, picked up SETUP.md cleanly (2026-08-31 16:22)
Docs confirmed no actual collision (verified my landed work independently rather than trust my
summary — checked the hosted URL live, checked all 4 "production" mentions are contextual not
instructional, read CONTRIBUTING.md's §1b against Lead's probe line-by-line). Picked up the
`SETUP.md` residual I'd flagged: fixed Lead's three specific errors (nonexistent
`PIPER.example.md`, wrong psql check for the Docker path, stale uvicorn entry point) plus their
echoes elsewhere in the doc, flagged the CONTRIBUTING.md/SETUP.md overlap explicitly rather than
consolidate unilaterally (matches my own framing that this was a real decision, not Docs' to make
alone), left `ALPHA_TESTING_GUIDE.md` for its own pass. **Nothing further owed from PPM.**

## 🔵 BYOC MARKETPLACE NARRATIVE — Comms re-surfaced a 23-day-stale ask to PM, informational
Comms' Aug-8 angle-pick request (A/B/C or deprioritize) never got a PM answer; CIO's standing-items
audit caught it. Comms correctly notes this is a separate blog/GTM artifact from the BYOC *listing*
copy I put on hold — probably doesn't need to wait on the same #1462 gate, but flagged the
connection since angle B touches plugin/marketplace positioning. Addressed to PM, not mine to
decide. No PPM action.

## ✅ #1708 EXECUTED — ALPHA_QUICKSTART.md hosted-primary, CONTRIBUTING.md gets full local setup (2026-08-31 13:22)
PM blessed the plan ("yes I bless the plan") after Lead's technical read + fresh-clone probe
(no hard credential wall — the /setup wizard funnels fine; the real problem was eight sequential
doc failures plus a new silent Keychain-ACL-hang trap on rebuild). Executed same-fire:
- **`docs/ALPHA_QUICKSTART.md`** rewritten hosted-primary — `piper-morgan.fly.dev` is step one, no
  clone/Docker/Python section left for testers, stale accuracy banner replaced with a short
  what-changed note, `localhost:8001` refs removed or pointed at the hosted URL, stale "Setup &
  Onboarding" wizard bullet cut (testers don't see a wizard now), footer date updated. 528→~220
  lines.
- **`CONTRIBUTING.md`** extended: fixed its own stale Python-version claim ("3.11+" → "3.11 or
  3.12 only," Lead's verified finding), new "1b. Running the Full App Locally" section with
  Lead's probe-measured steps (one-stack-per-machine compose warning, the Keychain-hang fix,
  `main` never `production`), port/database/env troubleshooting moved into "Common Issues."
- Dropped the broken setup-wizard screenshot walkthrough rather than propagate it — the referenced
  PNGs don't exist in the repo (pre-existing gap, documented 08-13, not new; verified via
  `docs/assets/images/alpha-onboarding/README.md`).

**A real near-miss, caught and defused**: Docs independently started the same rewrite mid-fire
(same PM ruling, same urgency read). No actual file conflict — I'd already committed and pushed
before Docs' note reached me — but sent an immediate urgent heads-up (`95985ceec`) so they didn't
duplicate effort or hit a push conflict. **Named explicitly what's still open** so nothing drops
in the handoff: `SETUP.md` still has Lead-flagged wrong content (PIPER.example.md step, psql
check, uvicorn entry point) untouched, may now overlap with CONTRIBUTING.md's new section —
worth Docs/Lead deciding whether to consolidate. `ALPHA_TESTING_GUIDE.md` not audited against the
hosted-primary change, flagged honestly in the quickstart's own "Getting Help" section rather than
left silently inconsistent.

Committed (`a98dae054`), merged a diverged origin/main (8 commits, clean no-conflict merge),
pushed (`013d5a0cd`). **Nothing further owed from PPM on #1708** unless Lead/Docs' SETUP.md or
ALPHA_TESTING_GUIDE.md follow-up surfaces a product question.

## ✅ QUARTERLY RUBRIC REVIEW — fully closed, item 3 routed onward (2026-08-31 13:22)
PM ratified item 1 in conversation. **3 of 4 items landed same day**: tier status (ratified +
recorded, my known-property edge written into the entry itself per Arch's suggestion — dated
changelog + same-day cc now the floor for CXO's future criteria edits), family coherence (CT
v2.3.3), the as-delivered limit (canonical in CT, Layer B points). **Item 3** (CT v2.4 →
`context_requirement` corpus tag) routed to Lead/PA for corpus ownership — not mine, watching only
if it resurfaces. Thursday's held slot returned, unneeded.

## ✅ CIO's standing-items audit — confirmed against my own independent retirement (2026-08-31 13:22)
CIO's cohort-wide git-archaeology pass found `ppm-standing-items.md` 49 days stale with ~6 of 17
items already resolved and never reconciled — arrived after I'd already retired the file this same
fire for the identical reason. Checked CIO's three "genuinely still open" items against GitHub
myself rather than trust the table: **#1270, #683, #1397 all confirmed OPEN** — none are PPM's to
action (Lead's technical-debt lane / duty-cycle tooling, correctly watch-only), noting here so they
don't disappear a second time.

## 🔵 #1463 PROBE — Claude arm results in, GPT arm + deconfounder authorized, still running (2026-08-31, informational)
Background to today's mail volume, no PPM stake: Claude arm confirmed CXO's fabrication hypothesis
exactly (a failed read rendered as "currently empty," the class `conversational_floor.py:214-226`
exists to block). GPT arm blocked on OpenAI credits most of the day (a real top-up landed in the
wrong place or was delayed — PA correctly tested live rather than trust the "unblocked" report,
CXO owned the layer-error precisely). Both the GPT arm and a 2-call deconfounder are now
PM-authorized to run together. Watch only if a product question falls out of the result.

## ✅ QUARTERLY COLLEAGUE-TEST RUBRIC REVIEW — CLOSED, all 4 items agreed same day as the trigger
CXO drafted dispositions same-fire (not Thursday) — `docs/internal/testing/
rubric-review-2026-q3-dispositions.md`. Read in full, checked one date claim myself rather than
take it (`git log -S"v2.2"` confirmed v2.2 landed 2026-04-26, before the 05-10 concurrence CXO's
item-3 reasoning depends on), and agreed all four: (1) ratify only the three invariants (question,
verdict shape, fabrication auto-fail), not the full 382-line rubric — noted one open edge (CXO can
still freely edit dimension criteria, which has similar practical effect to moving the bar, but
git history already gives a paper trail and gating criteria too would reintroduce the freeze
problem the split exists to avoid); (2) "branched measurement surface" is a real category
(BYOC measures the payload we hand a host, not what the user perceives — two attached
requirements: state what the score doesn't claim, name the companion verification); (3) CT v2.4
kept but reframed as corpus-metadata tagging (`context_requirement` tag) rather than a rubric
rewrite — CXO's own self-caught reversal, verified correct; (4) the "as-delivered unobservable on
BYOC" limit moves to the CT family doc as canonical, Layer B gets a pointer. **Nothing needs the
Thursday slot — closed same-fire.** Sent (`8c75a4b04`), verified landed.

## 🟡 #1708 — ALPHA_QUICKSTART.md steers testers to a dead branch; gave my product lean, waiting on Lead's technical read
CXO found the tester-facing onboarding doc tells testers to clone `production` (7,614 commits
stale, not a deploy source — CI builds on `main`) and calls the live hosted app (ESSENCE-named
current surface, ~11 testers) a "future plan." Filed #1708, put an accuracy banner up, didn't
touch the instructions — routed the actual decision to PM/PPM/Lead. **My lean, sent**: hosted app
should be the primary tester path (no optional complexity — a URL beats a 20-50 min local build
for the actual persona), `production` retired as a tester-facing concept (consistent with
`release-model.md`'s "artifact is never named, it is read" rule). **Explicitly did not claim to
know** whether local install is still a real working path for anyone — asked Lead for that
technical read before treating my lean as a recommendation. **Watch for Lead's reply; PM makes the
final call once both halves are on the table.**

## 🔵 Also caught this fire: a stale carry-forward line (Ship #058), corrected below — not new work

## 🔵 #1463 RECOMPOSITION PROBE — Claude arm run, confirmed the governing hypothesis; informational, no PPM action (2026-08-30 22:22)
PA ran CXO's #1463 packet (PM-authorized). Core case (item 1) confirmed the hypothesis exactly: a
failed read fabricated as "your todo list is currently empty" — the forbidden claim
`conversational_floor.py:214-226` exists to block on our own model, reproduced live on the MCP path
with no floor to block it. GPT arm collected zero data (OpenAI credits exhausted — a billing state,
not a finding). CXO found their own packet confounded two variables in item 3, revised the rubric
to v0.2, kept the gate at `PENDING-PROBE` (not PASS) rather than let a revision read as completion.
**Relevant to ESSENCE v1.0 commitment 7** (the recomposition-aware Colleague Test gate on BYOC) —
worth knowing if that thread resurfaces, but not something PPM needs to act on. Both memos
addressed to PM/CXO.

## ✅ C5 QUEUE-VS-GATE QUESTION — ANSWERED BY ARCH, my tagging stands, nothing to undo (2026-08-30 19:22)
The judgment call I flagged in my C5 reply (increment 7/#1706 widening the ratified PUB cluster)
got a precise answer: **QUEUE membership (the `PUB - Public Beta` Sprint tag) ≠ GATE membership**
(what public beta actually waits on). The gate stays exactly the four named items
(#1462/#1458/#1509/#1688) — the milestone description text, not the Sprint field, is the gate's
definition surface. All seven of my C5 filings (#1701–#1707) **keep their tags as-is** — no
un-tagging needed. #1701–#1705 sit in a middle zone (queued/front-loaded, promotion to the gate is
PM's call at the existing MVP-close re-triage point, nothing new needed there). **Closed — nothing
further owed.**

## 🔵 #1659 CONFIRMED REAL AND LIVE — informational, does not change my BYOC-copy recommendation
Web re-ran against Lead's restarted server: #1657 (resolver) fixed as predicted; #1659 (pypdf
runs on every file type) reproduced **exact and live** — verbatim the tracker's symptom, on
current code. CXO corrected their own earlier "didn't survive live testing" retraction (which was
itself premature — a good instance of "over-correcting is a real failure mode, not a safe
direction to err in," worth remembering). **CXO explicit: this doesn't revive the clause-level
BYOC-copy question — my "hold the whole listing" finding still governs** (#1462 at 0/15, no
`server` directory — the surface doesn't exist yet regardless of which document bugs are real).
No PPM action. A PDF-vs-.txt discriminator test came back honestly inconclusive (Web's test PDF
hit an unrelated exception) — not chasing further, no deadline attached by anyone.

## ✅ ESSENCE v1.0 RATIFIED, C5 UNBLOCKED AND EXECUTED SAME FIRE (2026-08-30 16:22)
PM ratified ESSENCE v1.0 in-conversation this afternoon (`decisions.log` ~16:3x). **Decision 2 is
the exact milestone question I raised in this morning's trifecta**: MCP work stays in Production,
front-loaded, and completion of the #1462/#1458/#1509/#1688 cluster is now the explicit
**PUBLIC-BETA GATE** — my reading (a) carried. Full model now written up at
`docs/internal/planning/release-model.md` (linked from `roadmap.md` v18.9) — **cite that doc going
forward for any audience/milestone-gate question, don't re-derive from changelog entries.**

**Both of Arch's asks executed same fire, plus C5 itself**:
1. **#1688** moved MVP→Production, Sprint `PUB - Public Beta`, Status `Product Backlog`. Found and
   fixed a real gap while in there: #1458 (named in the milestone's front-loaded cluster) had no
   Sprint tag — fixed to match.
2. **`release-model.md`** written and linked.
3. **C5 filed**: `#1701`–`#1707`, one per Leg D increment (2–8), all Production/`PUB - Public
   Beta`, each citing Leg D directly with open questions preserved rather than resolved silently
   (#1702 reminder-delivery, #1703 the #1463 probe as a hard gate on standup's payload format,
   #1706 scoped narrowly against #1441 not duplicating it, #1707 an explicit placeholder). Summary
   comment left on #1462 linking all seven. **One judgment call flagged, not silently made**:
   #1706 (increment 7) widens the ratified PUB cluster beyond the four items ESSENCE v1.0
   literally named — said so in the reply to Arch rather than deciding quietly.

`sprint-truth.py` confirmed the #1688 move landed: MVP 45→44 exactly. Sent full account to Arch cc
CXO/Lead/PM (`aaa880f3d`), verified landed. **The "OWED, REAL DEADLINE" cron line (trifecta + C5,
due Wed 09-02) is now fully discharged — remove at STOP, don't carry into tomorrow's prompt.**

## ✅ BYOC LISTING COPY THREAD — FULLY RESOLVED, my finding endorsed by both Comms and CXO (2026-08-30 16:22)
Following my 13:22 "hold the whole listing" recommendation: **Comms retracted** the v4
"ready to ship" framing outright; **CXO withdrew their own competing recommendation** in favor of
mine and wrote up the day's real lesson — four people, four checks, each one layer further from
the thing it was cited about (issue tracker → stale local dev server → local-vs-Fly failure mode →
the BYOC surface itself never being the thing anyone tested), each step a reasonable proxy whose
error compounded silently until my check finally hit the actual surface. **Web found the local dev
server was a 17-day-stale `reload=False` snapshot** and corrected their own earlier "#1656 confirmed
fixed" claim to "confirmed on local dev only, not the Fly-specific failure mode." **Lead restarted
the server on current main; Web's four closes stand on date-math** (their fixes merged before the
process went stale, so nothing they observed working could have been a false pass). None of this
required action from me — read in full, triaged, no reply owed since each was addressed to PM or
was pure informational cc. **Nothing further owed on this thread.**

## 🔴 BYOC LISTING COPY — SUPERSEDES my own 10:22 "documents holds" verdict: RECOMMEND HOLDING THE WHOLE LISTING (2026-08-30 13:22)
My 10:22 verdict ("issues"/"documents" hold against #1440, "conversations"/"people" don't) was
checked against the **web-chat app**. CXO then narrowed "documents" (PDF-via-Files-page only), Web
live-verified a real gap (upload works, chat can't see the file — a different error than #1659
predicts), and CXO corrected their own narrowing (Web's failure is resolver-layer, not #1659's
extraction-layer — #1659 landing would NOT fix what Web hit) before surfacing the actually load-
bearing point, explicitly flagged as not theirs to settle: **this is a BYOC/plugin listing — it
describes the hosted MCP tool surface (PDR-006, `mcp.pipermorgan.ai`), not the web-chat app anyone
in the thread had tested.**

**Verified this myself rather than relay it**: `gh issue view 1462` — 0/15 checklist items checked.
`find services/mcp -type d` — only `consumer` and `protocol` exist, **no `server` directory**. The
hosted MCP server has zero runnable code today. Every verdict in the thread, including my own, was
a correct answer checked against the wrong surface.

**Recommended to PM (cc Comms/CXO/Web/Lead): hold the whole listing, not edit a clause** — there is
no live BYOC surface yet for any sentence in the copy to be honest about. Sent
`mail-send.sh` (`6a9542a99`), verified landed. **Explicitly connected to the same #1462-milestone
question already open from the ESSENCE trifecta / C5 thread below** — both are the same underlying
"when does the hosted-MCP path have something real to point at" question, surfacing twice in one
day from different directions. **This is now the live state of the BYOC-copy thread — the 10:22
verdict and CXO's narrowing below are superseded, not wrong-then-right; they were the right answer
to a question that turned out not to be the one that mattered.**

## ✅ #1658 vs MAINTENANCE-MODE — RESOLVED SAME NIGHT (2026-08-29)
Arch ruled: PUB classification stands, execution FROZEN under the maintenance-mode boundary,
annotation not silent inheritance. CXO offered a sharper lens (user experiences regression-vs-
absence, not bug-vs-new-build) that proposed unbundling #1658's three parts differently — **checked
it against the issue's own text rather than accept either account at face value**: PM's own quote
covers all three parts under one historical claim, issue's class label is `parity-regression` for
the whole umbrella. The split didn't survive the check. **Synthesized**: Arch's ruling stands,
CXO's separable point kept (disclose the absence honestly if a tester hits it — different axis than
the freeze question). Closed same night, nothing further owed. Full record:
`mailboxes/ppm/inbox/read/reply-ppm-to-arch-cxo-cc-lead-pm-1658-synthesis-ruling-stands-2026-08-29.md`.

## 🟡 ARCHITECTURAL REVIEW 2026 — TRIFECTA SENT, C5 PARTIALLY BLOCKED ON A REAL QUESTION (2026-08-30)
**Trifecta response sent** (`82f4dc3d5`, well ahead of Wed 09-02) — concurred with the document as
a whole and explicitly with CXO's own challenge/amendments (commitments 3-vs-6 tension, "colleague"
uncashed, first-contact absent — no duplication, read CXO's response first). **One amendment of my
own**: swept the current MVP backlog and found #1462 (hosted-MCP epic), #1458 (its pre-user gate),
and #1509 (trust-consent) all sit in **Production** milestone while #1688 (my own filing) is the
only MCP-path item in **MVP** — a real mismatch against "all new build effort goes to MCP" read as
present-tense fact. Named it as belonging in ESSENCE.md's own scope, gave a weak lean (keep MVP as
currently scoped — real convergence in progress, 72→45 over two weeks, for a population that hasn't
moved to MCP yet) but explicitly asked Arch/PM to rule rather than resolve it myself.

**C5 (roadmap-sequencing the 8 MCP increments) is genuinely blocked on that same question** — filing
tracking issues for increments 2-8 now would mean guessing the exact milestone I just asked about.
**Not the deferral antipattern**: named trigger is "Arch/PM answers the milestone question,"
real and specific, not "no rush." **Resume C5 once that lands** — Leg D's 8-increment order is
already fully read and noted (`findings/leg-d-paper-rebuild.md`): 1. cold-start GitHub reflection
(≈#1688's territory) 2. create-issue-from-NL 3. todos/reminders 4. standup 5. document KB 6.
cross-session memory 7. calendar 8. trust-gated proactivity (deliberately last, gated).

**New supporting data point, not yet a ruling** (CXO, 08-30 late morning): #1463 (their own new
BYOC recomposition rubric) is ALSO a PDR-006 pre-user gate, ALSO milestoned Production — consistent
with reading (a) (MCP reaches no users before public beta, pre-user gates correctly sit in
Production), but under reading (b) this would need to move too, and it's CXO's own work landing in
MVP. CXO explicit: "not a finding, not voting" — just a concrete consequence for whoever answers.
Strengthens (a) slightly by widening what (b) would actually require moving.

**#1107 board finding — resolved**: moved MVP→Fast Follow myself, mechanical, matched the
established 08-27 Slack-descope pattern exactly (verified against #1497 first).

**#1635 — MY FLAG WAS WRONG, corrected and accepted (2026-08-30 morning)**: Lead proved with
receipts (`git show 588f6aad1` verified myself, matches exactly) the placeholder card shipped
2026-08-28 09:08 PT, a day before the ~11 AM 08-29 ratification — it existed in the running system
before the freeze, so there was never a tension. **My actual error**: checked milestone/board state
(correct method for #1107) but not deployment state (the method #1635 actually needed) — applied
one method to both. CXO added a second cause (the issue's own title said "shape undecided" in
writing) and fixed it. Accepted both corrections in full, verified each claim myself before
accepting rather than take either on trust.

**Also this morning — a real 20-day-old dropped ball, closed**: Comms re-pinged an Aug 10 question
(does the BYOC listing copy's "answers from that model... issues, documents, conversations and
people" hold against #1440's contract) that I'd triaged into `read/` and never actually answered.
Checked #1440's current state (Slack descoped, so GitHub/Calendar/Notion is the live gate) and gave
a real verdict: "issues"/"documents" hold, "conversations"/"people" don't — recommended narrowing
the copy rather than a tense fix, since there's no live capability underneath those two words at
any tense. Named the process gap plainly (triaged ≠ answered) rather than explain around it.

## ✅ #1658 vs MAINTENANCE-MODE — FULLY CLOSED, both sides acked (2026-08-29 night → 08-30 morning)
Arch's ruling + my synthesis stood on both sides' own review: Arch confirmed the annotation was
already live; **CXO gave a genuinely honest self-correction** — named the specific mechanism (read
the issue body truncated to 700 chars, missed the `Class: parity-regression` label that would have
prevented the split) rather than a vague "should've read more carefully." Nothing further owed.

Sent one reply covering all of this (Arch, cc CXO/Lead/PM), `0dc8bfde1`, verified landed.

## ✅ AWAITING-DECISION LABEL — SHIPPED (2026-08-29, Agent 360 v0.4 item PM approved)
My own 08-15 proposal, routed to me by HOST today. Created the GitHub label (safe/additive), wired
it into `sprint-truth.py`'s milestone-scoped NOT DONE breakdown (the unmilestoned half already
existed from 08-09 — this was the missing half). Caught and fixed a real bug testing: `gh project
item-list` returns labels as bare strings, `gh issue list` returns `{"name":...}` objects. Checked
all 6 currently-unmilestoned issues for genuine candidates — none qualified (all freshly-filed,
untriaged) — **deliberately left the label unapplied anywhere** rather than force a demo instance.
Committed `ebc0aea1b` → `b83bd9b5c`, replied to HOST cc CXO/CIO/Arch/Exec/PM (`fec70441e`, verified
landed). **Closed — nothing further owed.**

## ✅ #1677 CLOSE-TIMING DISCREPANCY — SOLVED, root cause was my own commit, not Lead's (2026-08-29)
Resolved same morning I asked. **Root cause: my own `mail-send.sh` commit subject** — "ask(ppm):
close #1677/#1488 properly, …" — tripped GitHub's auto-close keyword parser (`close` adjacent to
`#1677`), exactly the documented "auto-close ignores negation" gotcha (same class as the 2026-07
#1278 Beta Blocker incident). Lead verified with the actual event data (commit `312981354` against
the close event) rather than guessing, and reopened with the evidence in a comment. **Lead's
account of "not closing tonight" was accurate the whole time** — nobody acted out of order; I
generated the discrepancy myself by asking about a proper close in language that performed an
improper one.

**Confirmed independently before replying**: `git log -1 --format="%s" 312981354` matches exactly;
`#1677` state is OPEN with the reopen-evidence comment in place. Saved
`feedback_own_commit_subjects_can_auto_close` — the sharper personal lesson (ANY commit subject
mentioning an issue number is exposed, not just ones "about" closing; CLAUDE.md's general warning
didn't stop me from doing this myself). **Practical fix going forward**: scan every commit subject
(especially `mail-send.sh` ones, which are free-form prose) for close/fix/resolve keywords near a
bare issue number before sending — used a deliberately keyword-free subject for the reply itself as
a live test, worked clean.

**Thread fully closed** — close criteria for #1677/#1488 unchanged (PM's watched flip, live
transcript, then the checkbox pass). Nothing further owed on this from PPM.

## 🟡 REMAINING ITEMS FROM THE TRIAGE CUT (as of 08-28 22:00, superseded in part by the above)
- **#1522 — needs a fresh scan before delegation** (Lead's own lane will do it). The "3/9/5
  families" framing is 10 days stale; at least one family already resolved by v62–64.
- **#1689 filed/triaged 08-28 night**: genuinely new, found during #1687 — two native-dialog-gate
  violations of design-floor #1170. Milestoned MVP, on board, Sprint Backlog.

**Test-sequencing**: Lead adopted my security-first read (#1578/#1581/#1501 first) with one
insertion — todo/reminder cluster goes right after security, since that's where tomorrow's flip-on
first live traffic lands and PM's attention will be freshest. Lead's artifact carries this, not
mine — watch for it, don't re-derive.

**A real accountability gap, named by Exec and fixed, not defended**: cc'ing Exec/Docs on Lead/PM
exchanges all day was not the same as the direct briefing PM's own 08-25 framing required. Answered
properly once asked; saved `feedback_cc_is_not_briefing` since this is likely to recur. **Lesson for
future fires**: when a directive names specific roles to brief, send them their own dedicated
answer — don't let a cc trail stand in.

**Sprint field correction — I was wrong earlier today**: PM decreed one sprint left in MVP some
time back, so `Sprint = "Beta Blockers - Hard Gates Only"` on all open MVP issues is CORRECT, not
stale. Retracting my earlier "56 stale sprint tags" framing — don't re-raise it as a finding.

**Assignee/agent-field resolution**: PM confirmed — Assignees should always be the accountable
human (PM or whoever else checks in code), never an agent; a new single-select field for "current
agent owner" is the right shape, scoped to present-state only (commits are the historical record,
not this field's job).

## ✅ MVP TRIAGE CUT — CLOSED, PM ruled, board mechanics complete (2026-08-28)
**Full arc**: sanctioned 08-18, priority-3 08-25, split accepted 08-27, Lead's engineering read
08-28 morning (60 items). I did the sprint/milestone call, moving several items against
group-level signals once read in full, corrected Lead's "~10 items" headline down to 5. PM sanity-
checked live (~11:00), caught that I'd named #1638 "blocked on Arch" without ever asking Arch —
fixed same-session (ask sent, `857c87768`), plus routed #1386 criteria 4+5 nudges to Lead in the
same commit.

**PM ruled on all 5 same day** (~14:30, recorded as comments on each issue): #1658→PUB, #1661→PUB
(+ Lead's own live-v63 carve-out check), #1662→post-beta (my original call confirmed — Lead's
mid-sitting close+delete recommendation was proven wrong, correction recorded), #1647→post-beta,
#1436 epic→post-beta (my split preserved). **Board mechanics done**: all 5 → Production milestone
(standing disposition rule), #1658/#1661 → Sprint "PUB - Public Beta" via `assign-sprint-safely`.
**Found a bigger gap doing it**: 4 of 5 issues were never on the board at all (not just missing a
Sprint value) — added all four, Status → Product Backlog. Verified via `gh run list`/live reads
throughout, not assumed from mutations succeeding silently. Replied to Lead (cc PM/Exec, `f74fe2555`).
**Document**: `dev/active/mvp-triage-cut-assembled-2026-08-28.md`, marked ✅ CLOSED. **Nothing
further owed on this thread.**

**The §3 "no matter what" core list** (kept for reference — I used this same test again on the FTUX
consult below): (1) consent/trust architecture, (2) honesty discipline, (3) PM-operation grammar
(the 62 ops), (4) working-state model + Radar, (5) synthesis direction. NOT core: NL parser,
floor's prose improvisation, chat container itself, per-phrasing patches.

## ✅ FTUX SURFACE-MAPPING CONSULT — ANSWERED, #1688 filed MVP (2026-08-28)
CXO's mapping (`docs/internal/design/ftux-surface-mapping-2026-08-28.md`) applied the
no-optional-complexity lens first, landing on one real gap: cold Web/MCP users meet a plain
greeting instead of the FTUX model's value-delivering first question — the mapping's stated main
finding. Answered §5: ordering fits the milestone shape (no conflict with the triage cut); the gap
wants its own issue, not a scope-add to closed #1536. **Filed #1688** (MVP — extends already-shipped
#1536, closes a real first-impression trust gap, ran the core-list test rather than granting
differentiator work a free pass). **Caught `gh issue create --milestone` not adding to the board on
my own new issue** — checked immediately, fixed (`gh project item-add` + set Status to Sprint
Backlog). Lead's technical question (one mechanism or two builds across Web/MCP) left open on the
issue for him to answer. Replied to CXO cc Lead/PM/Arch/PA (`2615491e4`, verified landed). **Closed
— nothing further needed from PPM** unless Lead's technical answer changes the scope.

## ✅ #1386 CRITERIA 4+5 — BOTH CONFIRMED CLOSED SAME DAY (2026-08-28)
Both nudges from earlier today landed. **Criterion 5**: checked directly on live v63 via `fly ssh
console` — alembic at head, `ENCRYPTION_MASTER_KEY` present (autogen-diff not run in-container,
noted honestly as partial evidence). **Criterion 4**: the mypy ratchet drift I found this morning
is fixed, Architecture Enforcement green — **verified independently** (`gh run list`, not taken on
the issue comment alone), last 2 runs both success. **Only criterion 6 (PM sign-off) remains open**
on #1386 — 1's text is stale but functionally satisfied (#1332/#1278 both closed).

**New finding, same check**: **#1687** — four OTHER CI workflows (Code Quality, Docker Build,
Configuration Validation, Router Pattern Enforcement) silently red since ≥08-26, found while
verifying #1436's fix. Same "trained-to-skim belt" class as Architecture Enforcement's own red
window. Its body said "Milestone: MVP" but the actual field was unset — set it to match. **Lead is
already actively working it** (saw their live commits removing a never-passable CI job mid-fire).
⚠️ **Hit a genuine GitHub API rate limit mid-verification** (`API rate limit exceeded for user ID
3227378`) — couldn't confirm the milestone-set or board-add landed before the limit hit. The edit
command itself returned success before the limit, so likely landed, but **calling this unverified,
not confirmed** — first check next fire, don't assume.

## ✅ SHIP #058 WORKSTREAM REVIEW — CORRECTING A STALE NOTE, this was actually sent 08-28 (caught 2026-08-31 START)
The line below this one said "QUEUED, legitimately deferred" — **stale**. Checked
`mailboxes/ppm/sent/` directly rather than trust the note: `workstream-058-ppm-2026-08-28.md`
exists, sent same day. No Ship #059 kickoff has arrived yet (checked, none found) — nothing
currently owed on this cadence. Leaving this correction in place rather than silently deleting the
old note, per the cohort's stale-note discipline (a warning about staleness is itself exposed to
staleness).

## 🔵 08-27 session gap — cohort-wide account usage-limit event, not a PPM-side failure
Session went dark after the 13:22 WORK fire; no STOP happened. Retroactively closed the 08-27 log
at 08-28 START with full account: 13:22 work was safely committed/pushed before the gap, cron
(`d58bcc15`) survived untouched, and Exec's Ship #058 kickoff memo independently confirmed a
cohort-wide account usage-limit event Thursday afternoon — not specific to this seat. No action
needed; recorded for the record per the interrupted-fire precedent.

## 🔵 NEW PROTOCOL — replying to a cross-project agent (Exec broadcast, 2026-08-25)
Cohort-wide fix for a real structural gap: `mail-send.sh` correctly refuses paths outside
`mailboxes/`, and creating a directory for a cross-project agent (Dispatch-PM/DinP, Janus, Pard,
Klatch) is correctly forbidden — those two correct rules composed into "no compliant reply path
existed," which silently cost Docs a substantive reply and left a Tessera memo unanswered 28 days.
**Fix, if I ever need it**: write the memo normally with the real recipient in `to:`, `cc: exec`,
deliver to `mailboxes/exec/inbox/` via the ordinary `mail-send.sh` call — Exec relays into the
sibling repo. No PPM action from this memo itself (the three DIRECTORY.md gaps it named are Docs'
to fix); purely informational, filed. Worth remembering if a cross-project reply ever comes up.

## ✅ #1644 (roadmap.md) — MAIL THREAD CLOSED CLEANLY, 2026-08-24 evening
Docs' 08-24 confirmation memo (re: Lead's BRIEFING-CURRENT-STATE.md engineering-lane refresh)
said #1644 "stays open on Docs' tracker until it moves" — but I'd already fixed it that morning
(13:14 PT, `2a75d74eb`, see below), hours before either memo existed. Sent a correction citing the
commit hash and scope. Docs verified independently, posted a progress comment on #1644 itself
(left open on the correct framing: header symptom fixed, the genuinely-owed full v19 historical
fold isn't), and acknowledged the catch. **Clean close — nothing further owed on this thread.**
Worth noting only as one more instance of the day's actual theme: a tracker/status line going
stale relative to real state is the default failure mode, not the exception, and it hit three
different roles' trackers in one day (BRIEFING's own banner, then Docs' #1644 tracking) before
anyone else's action corrected it, not new vigilance.

## ✅ BRIEFING + ROADMAP STALENESS — ACTIONED 2026-08-24, both closed same-fire
Docs sent a **second** staleness flag (`2026-08-24-docs-briefing-current-state-still-stale-second-
flag.md`, first was #1643 08-17, zero movement in between) naming two PPM-lane gaps: (1)
`BRIEFING-CURRENT-STATE.md`'s Current Position/Focus reading ~5-6 weeks stale in substance despite
a misleadingly-recent "Last Updated: August 12" banner (that touch was CIO-lane-only, explicitly
not re-attesting Position/Focus); (2) `roadmap.md`'s header still reading "July 16, 2026" (#1644,
unresolved since 08-17). Acted on both same-fire per CLAUDE.md's standing instruction — no PM ask
needed, no waiting for Docs/CIO to own it.

**BRIEFING-CURRENT-STATE.md**: appended (didn't rewrite) a STATUS BANNER paragraph, a new
Last-Updated chain entry, a corrected Inchworm Position beta-date line (the old "beta target: July
4, 2026" line was stale twice over — no fixed date exists since PM moved beta back a month
08-08 without setting a new one), and a new "August 15–24" Recent Progress section covering
first-contact criterion ratified 8/15, #1510 fork ruled, spatial disposition closed, surfaces
taxonomy v1.0 ratified 8/21, FTUX model landed 8/21, #1386 criterion 2 re-confirmed 8/21, and the
current `sprint-truth.py` count cited verbatim. **Scoped decision**: followed the file's real
established append-only pattern rather than the `update-current-state` skill's idealized
clean-rewrite/trim template — the file has accreted "UPDATE date (Role attest)" clauses since
March without ever getting a clean rewrite or the Recent Progress trim the skill specifies; fixing
that structural debt is a separate, larger undertaking than one WORK fire. Touched only PPM-lane
content — Lead's engineering/CI/deploy sections untouched.

**roadmap.md** (#1644): confirmed via `git log` the file's most recent real touch was my own
narrow 08-06 fix (`25fdfd322`), not a fold — explaining the stale date. Chose an honest, scoped
fix over a full v19 historical re-fold: bumped title v18.7 → v18.8, annotated the existing Date
line as current-only-through-July-16, added a v18.8 changelog entry naming what's changed since
(beta walkback, first-contact criterion, surfaces taxonomy, FTUX model) and pointing readers at
`sprint-truth.py` + the refreshed briefing for live counts. **A full v19 fold is still owed** —
tracked as the open half of #1644, not done here.

**Committed + pushed**: `2a75d74eb` (both docs) → verified 0 ahead/0 behind `origin/main`.
Mailbox triage: memo moved to `read/` via `mail-send.sh` (`bac92034f`, verified landed, local
fast-forwarded clean).

## ✅ #1386 CRITERION 2 RE-CONFIRMED — 2026-08-21, fresh run, checked not inherited
A new canonical run (**Run 14**, keyed, first since Run 12) landed and CXO signed off the
outstanding withhold same-day. My own last signature (08-01/08-02) was against a **different,
three-week-old run** — didn't let it stand in without checking. **Verified Run 14's numbers
myself directly against `canonical-retest-history.csv`** (not either summary): 60/61 routing
(98.4%), 22/22 quality judged with zero skips (100%) — matched exactly. Checked the triage record
(#1674, #1675, Q38) was handled honestly. Posted a fresh re-confirmation on #1386 itself
(`#1386#issuecomment-5378179181`) — gate evidence belongs on the issue, per the established
coordinator's rule. Same scope note as always: one of six criteria; 1, 4, 5, 6 remain PM's.

## 🔵 FTUX EXPERIENCE MODEL — informational, no PPM action, worth knowing for future work
CXO + PM held a live 1-1, wrote up `docs/internal/design/ftux-experience-model-2026-08-21.md`
(v0.1, provenance-marked, PM co-owns). Core frame: "the first day with a genuinely good
colleague" — Piper speaks first, demonstrates the value prop in one turn, three states
(nothing/partial/rich) with one principle (demonstrate what's held, make handing more over
cheap). **Verified the claims about my own prior work before triaging silently** — §3 correctly
cites the standup empty-case rule (#1591) I contributed to, and correctly scopes the enrichment
offer to the ratified F-Integrations set (GitHub/Calendar/Notion, Slack deferred per #1481) from
my own taxonomy consult. Both accurate. **Purely informational** (a "notify," not an "ask") — no
question posed to PPM, nothing to respond to. Relevant background for whenever surface-mapping
work against the ratified taxonomy reaches my lane ("comes next," per the doc, not scheduled yet).

## ✅ SURFACES TAXONOMY RATIFIED v1.0 — 2026-08-21, seven-day watch resolved
PM answered §5's naming question directly (*"yes, it reads right"*, no rename) — the sole
remaining gate, since Arch's and my consults were already confirmed 08-16.
`docs/internal/design/surfaces-taxonomy-2026-08-16.md` is now v1.0. **Nothing further needed from
PPM** — my work on this thread was already complete and credited before this closed. One
follow-up (aligning `experience-across-surfaces.md`'s terminology) is explicitly PM's own to raise
directly with CXO. Watch-for line removed from the cron prompt.

## ✅ SHIP #057 WORKSTREAM REVIEW — SENT 2026-08-21 10:22, same fire as the kickoff
Window Fri Aug 14–Thu Aug 20. Sent same-fire per "write it now" — no delivery-gap repeat this
time. Sent: `mailboxes/exec/inbox/workstream-057-ppm-2026-08-21.md`. **Also did the proper Rule-5
refresh this time**: `ROLE-PORTFOLIO-PPM.md` §2's table itself was rewritten (not just the header
note, which is what the 08-14 pass did and left the table a week stale) — three priorities closed
this window (first-contact criterion, Jake FTUX, spatial disposition), surfaces-taxonomy added as
a new tracked priority.

## ✅ SURFACES TAXONOMY v0.2 — my consult applied, extended correctly, and confirmed 2026-08-16
CXO folded my notification-routing reasoning directly into the doc same day (`661ce4802`, no mail
needed — pure incorporation, not a new question). Thread closed for now pending PM's naming word.
**Update to the entry below**: Arch found a real m-49 ("Described Is Not Running") defect in
CXO's v0.1 — the platform-axis "receipts" cited design prose, not code that actually exists; CXO
accepted fully, fixed §3. **My general rule got applied MORE broadly than I stated it** — CXO
correctly extended "any cell gated by an already-ratified hold" to the already-*ratified*
F-History/F-FirstRun chat-host variants too (a PDR-005-ratified design intent doesn't override an
active platform hold on actual shippability). That's the rule working as intended, not drift.
**Checked the one routing I hadn't pre-verified rather than trusting it**: CXO routed the
notification-layer cell to #1174 instead of ruling on it directly. Read #1174's own vision doc —
confirmed the routing is sound for a reason worth stating: the "notification layer" column only
ever applies to the out-of-session case (an in-session failure is just a normal chat reply,
already covered elsewhere), which makes it a genuine subset of #1174's proactive-notification
scope, not a category mismatch. Sent confirmation with that reasoning rather than silent
agreement. **v0.2 status: both consults landed, only PM's word on §1 naming remains before full
ratification.**

## ✅ SURFACES TAXONOMY v0.1 DRAFT — PPM's MVP consult answered 2026-08-16
CXO's draft landed (`docs/internal/design/surfaces-taxonomy-2026-08-16.md`), the item flagged
below to watch for. Read in full, answered the specific consult: **of §4's 7 ✏️-marked cells, all
seven read aspirational-for-MVP** — 3 chat-host/Slack cells deferred by **#1481's still-open,
still-ratified hold** (checked fresh: Arch's 08-04 ruling, no comment since — "Slack inbound is
not a beta surface"), 4 CLI cells deferred because CLI is maintained-not-primary under PDR-006's
MCP-plus-thin-web-UI decision. **Caught one inference trap the doc itself didn't flag**: §0/§3 use
F-Settings×Chat-host as the *illustrative example* proving the two axes are orthogonal — that's
PM using it to make a conceptual point, not signaling it as required MVP scope. Named the
distinction explicitly so it doesn't quietly launder into "PM wants this built." **Offered a
general rule instead of seven one-off calls**: any cell gated by an already-ratified hold
inherits that hold's status automatically, re-evaluate as a batch if/when #1481 clears, rather
than needing a PPM re-consult per cell. One cell (F-Errors × Notification layer — does a failure
ever warrant a push?) nudged toward a considered *no* rather than staying open indefinitely, since
that's a different kind of undecided than "not built yet." Sent, cc Arch/Exec/PM/Lead. Not
blocking ratification — everything answered was "defer."

## 🔴 SURFACE 3 WAS NEVER A PHANTOM — I was wrong, and the fix is bigger than name-or-strike
⚠️ **Correcting my own carried claim below (line ~345, "Surface 3 is a PHANTOM")** — PM asked for
a forensic git-history dive rather than accepting either CXO's or my read, and it found Surface 3
is real: **"Settings/preferences,"** originating in Lead's 2026-05-14 memo, CEO-ratified by name in
CXO's Round 2 synthesis (05-15/16), deliberately scoped tiny (account profile + notification
opt-outs) — which is exactly why it never got its own MUX doc and later read as absent. **My
whole-corpus grep found one mention because I was searching for a *name*, not tracing *origin*** —
the ratified seven-name table never made it into PDR-005 itself. Worth sitting with: a
"not found" from a real search is still a claim about search *method*, not about existence.

**PM's actual ask is bigger than mine was**: 'surface' was doing two jobs — a **platform/touchpoint
axis** (desktop/mobile/CLI/Slack/voice, explicitly non-exhaustive) and the **existing seven** as a
separate **functional axis** (history, privacy, settings, integration, search, first-run,
audit/error — "a catalog of ways Piper communicates or interacts," not a place). PM's own proof
they're orthogonal: Settings needs BOTH a web-app screen AND a conversational path — the same
functional surface on two platforms, which a flattened single list would hide. **PM: "beware the
strong tendency to flatten [MUX] into semantically compact ideas that lose the modeling."**
CXO leads the rectify+ratify pass (PM's own lane per the standing rule), consulting **Arch**
(architectural consequences per touchpoint) and **PPM** (which axis-combinations are MVP-required
vs. aspirational). **CXO deferred drafting to a fresh session tonight** — explicit named trigger
(late in a long Saturday, exactly the flattening risk PM warned against), no deadline, legitimate
quality-banking not the antipattern. **Nothing for PPM to do yet** — CXO brings a draft to
consult against; watch for it. Full brief:
`mailboxes/ppm/inbox/read/brief-pm-to-cxo-relayed-by-exec-rectify-ratify-the-surfaces-taxonomy-
two-axes-not-one-2026-08-15.md`.

## ✅ SPATIAL DISPOSITION CLOSED 2026-08-15 — a long-carried item, resolved
Cold-island disposal: **all 11 modules** approved for removal (9 clean, 2 more added after PM's
"ok to also remove any superseded predecessors") — "retained as prior art" means commit-hash
citation in the disposal record, files actually deleted, must stay *findable* for future
re-investigation. **Ambient presence (L4)**: phased, not all-or-nothing — MVP gets a false-door
placeholder (**#1635**, filed), Beta stays discovery-only (**#1174**, already correctly scoped,
no change needed), Production needs Lead's still-outstanding monitoring-loop cost estimate (open
since 07-30). Full vision: `docs/internal/product/ambient-presence-l4-vision-2026-08-15.md`.
**My old carried note below ("Spatial disposition... CXO owns the re-scope") is now stale** —
closed, not owed.

## ✅ FIRST-CONTACT CRITERION RATIFIED 2026-08-15 — the LAST of the three original handoff items
PM ratified `docs/internal/product/first-contact-criterion-merged-2026-08-10.md` as canonical,
condition: joint CXO+PPM sign-off on the merged doc specifically. **CXO caught a real provenance
error** in the ratification memo (it credited CXO's 08-12 review with covering item 3; that review
actually covered item 2 — a numbering coincidence between this doc and the original #1536 build,
the "one name, two objects" pattern again) and gave a genuine fresh sign-off rather than letting
the wrong citation stand. **I did the same**: re-read the whole document fresh (not resting on
having authored it) before giving my own explicit sign-off. **Found and fixed the one thing CXO's
fix didn't reach**: `decisions.log`'s entry still carried the uncorrected provenance claim — the
doc's own status line was fixed but the durable cross-session record wasn't. Appended a correction
(16:23 PT, append-only convention, not editing the original) with both the fix and my sign-off on
record. **Placement in #1386's beta gate remains separately open** since 08-05, untouched by this.
**Two of the three original `docs/handoff-ppm-2026-08-11.md` §2 items are now resolved**:
criterion blessed (today), #1510 fork ruled (08-13). ⚠️ **Surface 1/3's "name-or-strike" framing
is SUPERSEDED as of tonight** — see the taxonomy section above; it's now a real two-axis
rectify-and-ratify project with CXO leading, not a small open question waiting on PM.

## ✅ #1509 OUTWARDNESS AXIS — AGREED 2026-08-15, real product judgment applied, not a rubber-stamp
PM leaned YES on making "outward" (writes/sends visible to someone other than the user) its own
consent dimension, distinct from effect, conditional on CXO + PPM agreeing. **Read #1509 in full
myself before answering** (I filed it 08-07) — the original scope language already named
outwardness as part of the gate's trigger condition, so this formalizes something implicit since
07-31 rather than inventing new scope. **Stress-tested CXO's proposed boundary** ("outward" = a
communication act, not "data others could theoretically see") against `close_issue` — technically
not a communication act but highly visible to a team watching a board. **Held**: `close_issue` is
already DESTRUCTIVE (#1190) for exactly that visibility reason, so the case I tried to use to
widen the boundary is already covered by the *other* axis — confirms the two-axis design is
exhaustive-by-composition, not leaky. **One scope note sent explicitly**: this doesn't reopen
#1509's milestone (already MVP, base gate already shipped `d137b8218`) — incremental refinement,
not new scope. Sent: `mailboxes/lead/inbox/reply-ppm-to-lead-cxo-cc-pm-outwardness-axis-AGREE-
2026-08-15.md`.

## ✅ AGENT 360 v0.4 — SENT 2026-08-15, well ahead of HOST's ~08-28 window
Dedicated pass, not squeezed into another fire's tail (the legitimate-deferral trigger this was
queued under). Grounded every claim in evidence — my own 07-26 hook-probe log, my clean 08-11
worktree provisioning check, this week's #1569/#1605 loop, the interrupted-08-13-STOP recovery —
rather than characterizing generally. **Headline finding, surfaced independently across three
sections (§8.2/§9.2/§6.1)**: the missing `awaiting-decision` label/board field is the single most
concrete, cheapest, agent-buildable gap — `sprint-truth.py`'s own output names it, and I hit its
cost directly this week (an MVP count moving 48→52→48 for reasons I had to manually reason through
each time). Second proposal: fold the interrupted-fire recovery pattern into the
`duty-cycle-tick` skill itself, not just my own cron prompt.
**Sent**: `mailboxes/host/inbox/agent-360-response-ppm-2026-08-15.md`, cc PM. Queue line removed
from the cron prompt at re-arm per its own delete-on-completion rule.

## ✅ SHIP #056 WORKSTREAM REVIEW — SENT 2026-08-14 19:22, mystery of the missing kickoff resolved
Original kickoff never reached my inbox at send time (checked exec's `sent/` directly — no
`kickoff-ship-056` file existed there, only the correction). **Resolved at STOP**: Exec restored
the original, explaining it — their own `mail-send` accidentally deleted it 22 seconds after the
09:04 send via a mis-passed follow-up call; existed on trunk under a minute, three roles correctly
never saw it. Not a PPM-side gap. My review (sent from the correction's own restated parameters:
window Fri Aug 7–Thu Aug 13, leadership progress-against-goals framing, fresh `sprint-truth.py`
citation) already matched everything the restored original specifies — nothing to redo. **Sent**:
`mailboxes/exec/inbox/workstream-056-ppm-2026-08-14.md`. **Also refreshed
`ROLE-PORTFOLIO-PPM.md`'s §2 per Rule 5** (the review is the trigger point) — dropped the stale
"beta target Aug 8" header line, since PM moved that a month back on 08-08 and the doc still
carried the old date six days later.

## 🔴 QUEUED — Agent 360 v0.4, HOST's cohort check-in (deadline ~2026-08-28)
HOST fielded a 291-line cohort-wide questionnaire (`dev/active/agent-360-questionnaire-v0_4.md`),
requesting answers within ~2 weeks of 2026-08-14 — **an externally-set window, not a self-invented
deadline**, so deferring to a dedicated fire is legitimate quality-banking, not the bite-sizing
antipattern. **Explicit trigger**: a WORK fire with room to answer it properly (10 sections + a
PPM-specific section + plausibility check) rather than squeezed into another fire's tail. Not
urgent today — HOST's own framing is "respond when you have something to say, not on a clock" —
but don't let it silently slide past ~08-28. Read and understood; memo triaged to `read/`, task
tracked here instead of left sitting in inbox.

## ✅ #1569/#1605 — CLOSED, joint PPM/CXO design, fully shipped and reviewed
PM gave PPM+CXO the floor on #1569 (reminders-vs-todos framing) + #1605 (disambiguation copy).
**Full arc**: CXO candidate → I audited, found 2 gaps → CXO resolved both → I checked before
endorsing, found one more real gap (stored-delete-default needs a blocking confirm, not
disclosure — grounded in `destructive_confirm.py`'s DESTRUCTIVE-always-confirms precedent) →
Lead showed it's already structurally guaranteed by the shipped consent-matrix (verified myself,
`consent_gate.py:114-116,137,335`) → CXO shipped 3-variant final copy → I signed off → **build
landed same day (`e9ef395a1`)** → CXO reviewed the copy seams post-build, clean → one small
follow-up (does ALWAYS_ASK flush a stored verb mapping? answer: no, becomes a question instead)
→ **confirmed 08-14 07:22, checked against the actual #1510 ruling text.** Genuinely done — no
open thread remains. Worth naming: three real gaps surfaced across the thread, all from someone
actually checking rather than trusting a peer's summary, none of them rubber-stamped either
direction.

## ✅ #1510 FORK RULED 2026-08-13 (PM via Exec) — one of the three handoff items now CLOSED
**The (a)/(b) fork is resolved**: low trust-gradient score on an inference → Piper reads it back
to the user for verification → once verified, stored, not re-inferred each time. Meta-feedback
about the *verification process* ("stop asking me") stays a separate signal from feedback about
task-preference *content* — don't fold the two into one mechanism. Milestone deliberately left
open by the ruling — PM's words: *"that's the next actor's call."*
**Cross-linked to my own owned spec**: posted on #1511 connecting this ruling to the
Production-half preference-capture design (the anti-goal risk I flagged 08-10 — asking at the
moment of least information — is exactly what "observe, read back once, store" resolves).
**#1591 already got the same cross-link from another role, independently, ~4 min before this
fire** — no duplication, complementary (different issue, same ruling). **Two of three handoff
items now open; only criterion blessing + Surface 1/3 remain.**

**Sync clean, inbox empty. `MVP 52 not done / 1043 done`** (checked fresh at 07:22 START — the
52-from-48 shift was overnight filing churn in the no-status-set bucket, not a regression;
unchanged again at this fire).
✅ **Jake conversion COMPLETE: #1536–#1540 filed 08-09, zero rows unfiled.**

## 🔴 AWARENESS FROM 08-11 16:1x — Lead's escalation to PM (not mine to action, but changes what I cite)
Read via mail triage, addressed to PM with PPM cc'd; **no PPM-owned decision, PM's three calls
(#1600 ratchet-fix-now?, #1599 is_admin grant method, deploy word)** — do not chase these, PM has
them. **What changes my own reasoning going forward:**
- **MVP open count moved 51 → 48**, composition not just number — 9 genuinely closed with evidence,
  2 (#1411, #1431) have live reproducing defects despite looking closeable, #1485 blocked by the new
  admin-403 beta blocker, #1480's client-side half is unverified (grep-only, JS never executed).
  ⚠️ **Do not cite "51 open" going forward — it's stale as of today.** Re-run `sprint-truth.py`
  before citing any count rather than trusting this note past today.
- **CI has been red on `main` two days** (#1600, ratchet ceilings breached, gating `smoke` marks
  failing) and **Architecture Enforcement red on every push since 08-09 15:07** — a STOP condition
  per CLAUDE.md, PM's to triage, not mine, but relevant context if any PPM spec work assumes green CI.
- **New beta blocker #1599**: `is_admin` unset for anyone (1377 users, zero admin) — 7 routes 403,
  including the Slack app-token save (#1201). PM-gated.
Filed for my own awareness only; moved to `mailboxes/ppm/inbox/read/` after triage, nothing else
required of PPM.

## ✅ FTUX FIVE RULED (2026-08-10) — HOLD STATE ENDED
**#1536 → MVP + Beta Blockers** (PM: *"if CXO feels one of the issues should be kept in MVP, I am
inclined to defer to that and err on the side of including"* — CXO's on-record argument was exactly
one issue). **#1537–#1540 → Production + PUB.** ✅ **Verified on the board.**
**PM resolved CXO's tension by clarification, not by us**: *"something can be discovered in alpha, and
we can decide to defer it before going into beta… comfortable with my placement and with clarifying
or overriding my needlessly blanket statement from earlier."* ⭐ ***"Out of alpha" = the PUBLIC beta***;
private beta stays invite-only until PUB completes.
✅ **#1536 now gates on the converged three** (CXO's two-tier + my merge + Arch's H1 clarify) —
`docs/internal/product/first-contact-criterion-merged-2026-08-10.md`. **Item ③'s block discharged.**
**Awaiting-decision population: 7 → 2** (#1511, #1569).

## ✅ #1511 IS MY SPEC LANE (PM direction 08-10) — slice ACCEPTED, spec on the issue
**Two modes, not one winner**: report-on-demand **default** (ratifies live behaviour) · interview
survives as a **NAMED** mode · possible first-run interactive fallback + preference capture.
**MVP** = the naming/disambiguation only (**the interview already works — anything touching its
behaviour is OUT**); **Production/PUB** = fallback + preference.
🔴 **The merge I added: #1511's preference capture IS #1510's declared mode in another domain.**
Lead spotted the shared *storage* (`users.preferences` JSONB); **the MECHANISM matters more —
declaration, REVOCATION, and showing the user what Piper believes about them.** *Two surfaces
inventing two revocation stories is how you get a preference nobody can find to change.* **Ride
#1510's surface, don't parallel it** — ordering already right since #1510 is MVP.
⚠️ **Anti-goal risk flagged**: a first-run *"what standup do you want going forward"* asks at the
moment of **least information**. **Demonstrate then ask** (as #1536), and make it **visibly revisable**
— *an unfindable preference is the dictating PM's anti-goal is about, arriving by accident.*

## ✅ PM APPROVED THE PLACEMENT (2026-08-09, relayed by Lead, board WRITTEN)
**#1510 → MVP · #1190 → MVP · #1509 → Production.** Verified on the board myself. **#1536–#1540
remain NONE, correctly — their unmilestoned state IS the ask.**
⚠️ **PM sequence correction, cohort-wide**: **MVP → Production → Fast Follow.** *"'MVP or Fast Follow'
encodes a misunderstanding by many agents."* **"Not MVP" NEVER defaults to Fast Follow.** Production =
required for PUBLIC beta, worked in the **PUB sprint**.
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Environment note — CURRENT as of 2026-07-30

**This role is on Amber, Model A**: `~/Development/piper-morgan-worktrees/ppm`, branch
`claude/ppm-cycle`, 0 behind `origin/main`. **Cron is ARMED and firing.**

*(Superseded: the prior note here described a 7/28 session running from the old pre-Amber worktree
`pensive-kepler-02a0f6`. That was accurate then and is not now. Rewritten rather than left to be
inherited — this file has already caused one four-session error by being read as current state.)*

**PPM went dark twice** (7/20-25, 7/27-28) and was resumed by PM both times; a third interruption
(overload error, 7/29-30) was also PM-resumed. In all three the carry-forward + mail were the only
continuity — never a clean STOP. **The environment question the 7/28 session raised is now answered
by fact rather than by ruling: PPM runs on Amber.**

## ⚠️ SPRINT STRUCTURE — READ BEFORE ANY MILESTONE/SPRINT REASONING

**M4 and M5 DO NOT EXIST as sprints.** They were **swept 2026-07-04/05 — PPM's own work** — along
with M3-Quality/M3-Health/M3-Security/RECONNECT. Contents went either into the **Beta Blockers**
sprint or to the **Production** milestone.

- **Beta Blockers = the final pre-beta sprint.** The **MVP milestone IS the beta gate**: beta ships
  when every issue on `docs/internal/planning/beta-blockers.md` closes — not on a date.
- **Disposition rule**: anything in MVP that didn't meet the hard-gate bar → **Production**, to be
  addressed *during* beta. So **an issue sitting in Production is the rule working, not a defect.**

✅ **BOTH DOCS ARE NOW FIXED — verified 2026-08-06, and this line used to say they weren't.**
- `sprint-board-structure.md:77` carries a SUPERSEDED banner; `:88`/`:91` mark M4 triage-closed and M5 swept.
- `roadmap.md:68` annotates differentiator #4 with the sweep + #1174's move to Production.

⚠️ **Note what just happened, because it is the whole lesson in one line.** This warning existed
*because* those two docs burned me — and it outlived them. **I re-read my own warning today and had
to go check whether it was still true.** A warning about staleness is not exempt from staleness;
it is *more* exposed, because it gets written at peak conviction and reread as settled fact.
✅ **AND THE OWED RESIDUE IS NOW DRAINED TOO** (08-06 STOP). Scoped it: only **5** live refs, and **3 were correct as written** — the roadmap's own §M4 triage record, the briefing line that *instructs* readers what to do on seeing `(M4 territory)`, and a narrative about a stale artifact. **Fixing those would have been the error.** The 2 real ones were in my own entity-model spec.

✅ **The accurate source is `docs/internal/planning/beta-blockers.md`** (see its lines 12 + 20).

**Cost of not knowing this (2026-07-30)**: I reasoned from the two stale docs and produced three
successive wrong readings of one roadmap line, then recommended moving **#1174 into M4** — a
dissolved sprint. PM caught it. **I had run the sweep myself and it was in no artifact I carried.**
✅ **Repointing DONE 08-06** — and doing it as a class is what made it cheap (5 hits, 3 false positives). 🔴 **It also surfaced something worse**: chasing the 2 real refs led to **#1216**, which is **CLOSED COMPLETED 2026-07-07 in MVP** — while `roadmap.md:143` had claimed for a **month** that it *"remains OPEN"* and was a *"Beta Blocker candidate pending PM's call."* **It landed in MVP, so the call I was waiting on had been made by ACTION rather than by ANSWER, and I kept carrying it as PM-gated.** ⭐ **An item can leave your PM-gated queue without anyone telling you, and nothing in the queue notices.**

## ⚠️ HEARTBEAT — WAKE EMISSION, EVERY FIRE, AT THE START (adopted 2026-08-05)

**Run `scripts/duty-cycle-heartbeat.sh ppm <FIRE> ` at the START of every fire, before any commit.**
NOT as Step 5b at the end. **On 2026-08-05 I skipped Step 5b entirely on a busy fire** — nine other
roles emitted, ppm didn't — and PA's pre-registered falsifier fired on my seat as a result.
**Step 5b sits where a fire that found real work drops procedure**, which is exactly when the
liveness claim is most often made and least examined.

⚠️ **Do NOT repeat my claim that "~30 fires produced zero heartbeats" as evidence about the
mechanism.** On fires where I ran it, `--if-quiet` suppressed as documented; on at least one I never
ran it. Those two populations are not separable retroactively. **The clean claim is narrow.**

## ⚠️ BRANCH ≠ DEPLOYED ARTIFACT — and "I verified it independently" needs a DIFFERENT METHOD

**2026-08-06, my error, caught by Lead and PA and not by me.** I sent PM an URGENT saying
*"commits on main not in production → **2,282**"* and wrote *"verified the deployment claim
independently before building on it."*

**`origin/production` is the production BRANCH; the deployed ARTIFACT is a Fly release.** Branch
staleness is benign-by-mode; the 2,282 delta is overwhelmingly mailbox/log/doc traffic from ten
agents. **Measured against the artifact (Fly v29, 2026-08-02, `main@b619794af`): 984 commits total,
of which 15 touch `services/` or `web/`.** ~15 product commits, ~4 days. **Two orders of magnitude.**

**⭐ The transferable part is the verification, not the number.** I ran the SAME comparison PA ran,
so **agreement was guaranteed and my check could not have caught the error.** A second measurement
that shares the first's method is **not** independent verification — it is replication wearing the
word "independent." *This is the class I wrote up on 07-26 and then committed eleven days later.*

**And it skewed a decision I put to PM**: I framed "deploy main before beta" as high-risk *because*
2,282. ~15 product commits over four days is an **ordinary release**. **A wrong magnitude doesn't
just misinform — it can invert which option looks safe.**

**Rule earned**: before writing "verified independently," name **what would have made my check come
out differently from theirs.** If the answer is "nothing," it's a repeat, and say *that* instead.

## ⛔ THE WEB UI IS NOT GOING AWAY — my sort key was a FALSE QUESTION (PM, 2026-08-08)

**READ THIS BEFORE ANY SURFACE/ROADMAP REASONING. Second time I've made this error.**

**PM verbatim**: *"I never said the web UI was going away… the modeled user experience is **not
specific to any one surface**. It's a holistic user experience, **expressed on each surface as
appropriate**"* — phone as notifications · **Slack** as a channel bot · **web** as conversations +
radar + settings · **another chat** as skills + MCP server · **CLI still maintained**. **All true at
the same time.** *"We can make decisions about what to ship first… but I have never said that we are
abandoning any one of those services."*

**PDR-005 never said otherwise**: decision **(b) "primarily MCP; thin web UI"**; option (a) *"no
Piper-specific UI in v1.0"* **explicitly REJECTED as infeasible**; **5 of 7 MUX/UI surfaces scoped
1.0-required**.

⭐ **The mechanism — "read more carefully" doesn't explain a repeat:**
1. I read a **PRIORITIZATION** statement as an **ONTOLOGY** statement. *"Primarily"* orders work; I
   made it a claim about which surfaces **exist**. Same family as production/trust/Notion/shipped:
   **"primary" = first-in-sequence vs. the-only-real-one.**
2. 🔴 **Building a SORT turned a misreading into infrastructure.** A sort needs a discriminator, so I
   **manufactured an axis**, and the axis smuggled in competition between complementary surfaces.
3. **Why it recurs cohort-wide**: the holistic model is **simultaneous truths**; decision artifacts
   are **singular commitments**. The doc's grammar wins every time. ⚠️ **It IS documented and
   referenced** (Nov-2025 holistic-UX brief; PDR-004 §Scope; PDR-005 lists PDR-004 under Related) —
   **so "not written down" is not available. It survives only in docs nobody opens mid-decision.**

**WITHDRAWN**: the sort key, at source in the synthesis §3 + my 07-30 memo + #055 framing. ⚠️ **PM
RATIFIED the bucket sort 08-05 on my framing** — flagged loudly rather than left standing.
⛔ **Do NOT re-key by patching labels** — any *survival* phrasing reintroduces it. Likely honest key:
**"which surface does this defect live in."**

✅ **#1477 re-anchored: a SURFACE-1 defect** (PDR-005:53 — *"left rail = current session"*),
1.0-required + scheduled. **Never needed the welfare exception.** ⚠️ **#1476's surface is NOT
verified** — couldn't locate what renders the "blocked" card; **do not assume it matches #1477.**

🔴 **OPEN, PM's to answer**: PM said the MCP path **"may emerge as primary"** — a **sequencing
possibility, not a settled ordering.** The re-sort waits on PM's read of how the surfaces relate.
**I treated an open question as closed once; not inferring it twice.**

## 🔴 CURRENT — ⚠️ BETA MOVED BACK A MONTH from Aug 9 (PM, 2026-08-08 ~10:10)

**Verified at source, `decisions.log:1242`.** PM verbatim: *"I am going to move the beta data back a
month. **We clearly have a lot more work still to do than anyone ever reported to me.**"*

⚠️ **That second sentence is about REPORTING, and I am a reporting role.** Context: T4/T5 verification
surfaced structural flaws (#1471/#1490/#1521 pre-classifier over-claiming · #1517 floor fabricating
capability denials · #1520 silent session expiry) on top of the denominator over-reporting Exec named
the same morning.

🔴 **MY SPECIFIC SHARE, so a future session doesn't re-derive a vague one**: **two of the six
NOT-STARTED items are mine** — **#1476 and #1477**, filed 07-31 as the bucket-A **welfare carve-out**
(*"fix regardless"*). **For eight days I reported them as filed and never once reported that nobody
had picked them up.** Portfolio said "advanced." #055 §0 said "advanced." **Neither false; both let a
reader infer motion that didn't exist.**

⭐ **The mechanism, which is the reusable part**: I gave PM *"21 open in MVP"* — **a total with no
parts**. And **`gh issue list --state open` CANNOT see board Status**, so it structurally cannot
distinguish *unstarted* from *awaiting PM's review*. **I was answering "how much is left" with a tool
that only answers "how many are open."** Not carelessness — **confident reporting from an instrument
that couldn't answer the question I was implicitly answering.**

**FIXED FORWARD**: use `scripts/sprint-truth.py` output **verbatim** (adopted 08-08, before the move
landed), or state explicitly what I excluded. **Report not-started AS not-started** — "filed,
unstarted, N days," never "advanced."

**Accurate gate state (08-08)**: `MVP: 22 not done (6 Sprint Backlog, 1 Blocked, 3 In Progress, 12 In
Review); 1021 done` — **with two corrections I found**: #1107 is CLOSED with a stale non-Done status
(so In Review is 11), and **#1509/#1510 are absent from the board entirely** (`gh issue create
--milestone` does NOT add to the board) → **≈23 genuinely not-done.** ⭐ **The 6 unstarted is the
planning number, not the 23.** And **In Review is the largest bucket, waiting on PM** — so the
critical path has been PM's attention, not build capacity.

**ASKED PM**: do #1476/#1477 still hold? They were a *welfare* carve-out justified by alpha testers
staying on the web UI meanwhile — **that reasoning may not survive a month's delay**, and I'd rather
re-ask than leave them unstarted on a rationale I stopped checking.

✅ **v30 IS LIVE and #1484's gate IS DEPLOYED — the 08-06 "gate is absent" reading is SUPERSEDED.**
CXO deployed 08-07 08:04 PDT and verified **off the running container** (`fly ssh console`, reading
`/app`): **`gate=2`** in `socket_mode_runner.py`, #1482's false-permanence strings gone, honest
replacement present. **Not an ancestry check, not a version inference, not a branch.**
⚠️ **Arch's 08-06 "0 occurrences in production" was a BRANCH query** — and `origin/production` is
**12 days stale** (`34744d184`, 07-26). I re-measured: **0 on that branch, 6 on `main`, and the
running artifact matches MAIN.** Arch has taken this and says they used branch ancestry as a
deployment check twice this week, false negative both times.
**#1386 criterion 5**: one green line, **NOT closed** — Arch posted it with the two remaining items
explicitly unclaimed. **My criterion-2 signature stands** (measured against `main`; layer was right).

🔴 **STANDING, and it is the week's most reusable rule**: **`origin/production` IS NOT THE
DEPLOYMENT.** Three layers — branch ancestry (*is it in some ref?* — **five of us got this wrong on
08-06**), `fly status` (*what version serves?*), and ⭐ `fly ssh console … grep /app/…` (***what does
the running system contain?*** — **no inference step at all**). **Use the third to answer a
deployment question.**

**1. Radar/Surface-1 is SETTLED — do not re-derive it.** Radar's rendering is **Surface 1** (history
sidebar, #1236). PDR-005 specifies a **cross-client variant** of it at `:122`, `:245`, `:288`, `:328`;
**PDR-005:135 + roadmap.md:127 both mark it "unblocked NOW", ~4-6 days.**
✅ **THE "WEAKER GROUNDS" CAVEAT I CARRIED IS RETIRED (2026-08-07, CXO).** PDR-005:84's rating was
written **2026-06-05**; **#1237 closed 06-18 and #1236 closed 06-19** — **the rating predates the
feature by 13–14 days and described a history list, not a ranked multi-entity attention surface.**
CXO ran PDR-005's own test on what exists: **criterion 1 MET strongly** (`feed.py:52` sorts by
`attention`; four heterogeneous sources; serializing to text loses the simultaneity + ranking that
*is* the information). CXO was revising **their own** Round-1 rating.

**My contribution, filed 08-07** — CXO's *"which of the five are named is unenumerated"* gap:
- ✅ **The five ARE enumerated — as BUILD LANES, `roadmap.md:127–129`, not as scope in PDR-005**:
  **Surfaces 1, 2, 4, 6, 7.** (2.1 = 1+7, 2.2 = 2+4, 2.3 = 6.) Scope inferable from schedule,
  asserted nowhere. **Surface 1 already has a lane marked "Unblocked NOW"** — so it is scheduled for
  1.0 and CXO's flattening risk did not land in the schedule; only the *justification* was stale.
- ⛔ **WITHDRAWN 2026-08-15 — "Surface 3 is a PHANTOM" was WRONG.** PM ordered a forensic git-history
  dive (not another docs grep) and found Surface 3 is real ("Settings/preferences," Lead's 05-14
  memo, CEO-ratified 05-15/16, deliberately scoped tiny — which is *why* it read as absent). **My
  error**: I searched for a *name* and concluded non-existence; the right method traces *origin*.
  See the taxonomy section at the top of this file — kept here rather than deleted, as the record
  of the mistake, not the current state. 🔴 **Surface 3 is a PHANTOM.** Whole-corpus grep: **one** MUX-roster mention, `PDR-005:84` — the
  very sentence pairing it with Surface 1. **No name, no doc, no ADR, no build lane** (Surface 2 has
  90 mentions + its own design doc). ⚠️ **And "Surface 3" collides**: in the *insight-delivery*
  numbering it means push-insights (#1032), so a grep lands on a confidently wrong referent.
- **Asked PM for**: the one sentence on Surface 1, **plus** name Surface 3 or strike it and say
  "5 of 6." **No urgency attached** — beta isn't gated on it.
⛔ **My earlier answers "the web page goes" and "undecided" are both WRONG.** Superseded.

**2. Awaiting PM** — ✅ **#1462 ANSWERED 08-07: Product / "PUB - Public beta" sprint** (with #1463).
Exec's note: *"you held #1462's milestone deliberately rather than guessing… PM's answer is a sharper
placement than either of us had. That's the held-question pattern working."* **Remaining five are all
milestoned already** (#1476 MVP · #1477 MVP · #1482 MVP · #1483 Production · #1485 MVP) — ⚠️ **verified
08-07, so what I was "awaiting" on these needs re-stating or dropping; do not re-ask as a block** · the **six Jake items** (PM answered 1, 2→"(b)", 5; needs plain English on 3 and 6 — 3 sent,
6 is PA's) · **canonical criterion text**.
✅ **CLOSED 08-06, both were on this list and both resolved**: **#1481 scope** — PM RULED the
socket-mode path **HELD** from alpha/beta/release until safe, *held not deferred*, with connector
work **front-loaded in Production** (sequence filed on #1440). **MVP milestone** — now reads
**2026-08-09**.
⚠️ **Before re-asking PM anything on this list, CHECK GITHUB FIRST.** #1216 sat here as PM-gated for
a month after closing. **The queue does not notice when an item leaves it.**

**3. Watch, don't drive**: #1484 (gate + CXO client branch, one commit) · the funnel query (Lead) ·
#1468 judge calibration · PA's annotation spec (unblocked; `headersHelper` is condition 1's carrier).

⚠️ **Standing instruction from PM, keep applying it**: *"I do not want to approve something I will
later regret because I felt rushed by a made-up deadline. I am a Time Lord after all."* **No
manufactured urgency in anything sent to him.**

⚠️ **My own lesson from 08-05, worth not repeating**: I gave PM three successive answers to one
question and only the third was right. **What fixed it was CXO finding a FACT neither of us had (the
surface number), not better reasoning over the same material.** On a question about something PM has
defended repeatedly — **find the number before answering at all**, and **check whether a peer has
already answered before sending.**

## Active PM threads

⚠️ **Pruned 2026-08-12** — the table this replaced (dated 7/28–7/31: Ship #053, the 07-31 gate
window, Jake's PPM-lens-only stage, PDR-006 pre-ratification, spatial (b), hooks TOCTOU, etc.) was
**three weeks stale and every row already superseded by newer sections above** (Jake is fully
converged and filed 08-09; PDR-006/spatial/hooks status folded into other sections; #1386's 07-31
window closed criterion 2 only, already recorded). Kept as a pointer, not carried forward as
content — if any of those threads turn out to still be open, that's a finding, not an inheritance.
**The three in `docs/handoff-ppm-2026-08-11.md` §2 were the open-for-PM baseline. Status as of
08-13 10:22**: **#1510 fork RULED 08-13** (see top of this file) — down to **two remaining**:
criterion blessing, Surface 1/3. Neither has moved since 08-10 as of this fire.
⚠️ **Superseded by 08-15 — this whole snapshot is historical.** Criterion ratified 08-15; Surface
1/3's framing itself superseded 08-15 (see top of file). All three original items are now either
resolved or reframed into larger tracked work. Do not read this paragraph as current state.

## PM-attention / escalation items
- **Environment question** (see note above) — not blocking, but worth PM's call if a future session hits the same ambiguity.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found
- ~~A canonical `ROLE-PORTFOLIO-PPM` doc. Flagged by two prior PPM sessions now (7/19, 7/26). Worth actually asking PM rather than a third session routing around it again.~~
  ✅ **RESOLVED 2026-07-29 — IT EXISTS AND ALWAYS DID.** `docs/briefing/ROLE-PORTFOLIO-PPM.md`, 118 lines, **self-authored by PPM**, commit `d9be35bbf`, `last_updated: 2026-06-27`. Sits with eleven sibling portfolios in the default briefing directory. Found by one `find . -iname "*ROLE-PORTFOLIO*"`.
  ⚠️ **Read this as a process finding, not a filing correction.** *Four* PPM sessions recorded it missing (7/19, 7/26, 7/28, and the predecessor's handoff) because each inherited this line instead of re-running the check — and the line gained confidence as it propagated, which reads as diligence and is actually the error compounding. It is the predecessor's own lesson #3 ("records that look authoritative are only as good as the discipline keeping them synced; checking costs less than it feels like") landing on the carry-forward itself.
  **Rule earned**: a "wanted but not found" entry is a **claim with a timestamp**, not a standing fact. It decays exactly like a status claim. Date it and re-check it, or don't inherit it.

## Predecessor handoff (Sections 4 & 6) — now durable
- `dev/active/handoff-ppm-predecessor-2026-07-28.md`. The predecessor's own lessons + load-bearing/commodity read — the content CIO's orientation note correctly flagged as the one thing artifacts couldn't supply.
- ⚠️ It arrived as **session-message text only**. The path the predecessor reported writing it to did not exist, and no copy existed on disk or on `origin/main`. Committed 7/29 from the message text; had that message not been relayed, it was gone. `mail-send.sh` refusing it was correct behavior (mailbox paths only) — the gap is that **there is no equivalent durable-delivery path for non-mailbox handoff artifacts**, and the fallback was "leave it uncommitted in the main checkout," which is exactly where it evaporated.

## Known process notes for future fires
- **NEVER reuse a tree object across a push-retry** — rebuild fully from a fresh `read-tree`. See `feedback_never_reuse_stale_tree_object_on_push_retry.md`.
- **This shell is zsh — unquoted multi-line variables don't word-split in `for X in $VAR`.** Use `while IFS= read -r`.
- **`git show --stat`'s rename-collapse can hide a pure move as "0 changes"** — spot-check byte counts.
- **A dark PPM session leaves no explanation of its own gap** — twice now (7/20-25, 7/27-28), the carry-forward + mail were the only continuity, never a clean STOP. Don't assume a gap means nothing happened elsewhere — 985 commits landed cohort-wide during the first gap alone.
- **Check Ship kickoff memos for exact window boundaries** — Exec's #053 kickoff explicitly warned against folding post-window material in; read the window dates literally.
- **ADR-077 / ADR-078 / ADR-079 are three different ADRs.**
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

**ARMED** — job **`b35c8662`** (re-armed at 08-29 22:22 STOP; delete-then-create, `CronList`-
verified exactly one). Prior job `759b28c2` (armed 08-28 22:22) retired cleanly — no gap, no
incident. **Two real content changes at this re-arm**: (1) WATCH FOR now points at criterion 6 only
— the two resolved overnight items (#1677/#1488, #1638) dropped from the line since both landed
today; (2) added a new **AUTO-CLOSE TRAP** standing line (avoid close/fix/resolve keywords adjacent
to a bare issue number in any commit subject — bit me directly today) and an **OWED, REAL DEADLINE**
line naming the architectural-review trifecta + C5 sequencing due Wed 09-02, to delete once both
are sent. Still carries: **NO STANDING OWED WORK ITEM** header (now qualified), **DATES**,
**MILESTONE SEQUENCE**, **SURFACES**, **COUNTS**, **AUDIT BIAS**, **GENERAL CONTRACTS**, **PROXIES**,
**MAIL-SEND CAN FAIL SILENTLY**, **TOOL OUTAGES**, **HEARTBEAT PUSH RACES**.

⚠️ **Session-only + 7-day auto-expiry, both silent** — `b35c8662` expires ~2026-09-05 if not
re-armed sooner (re-armed every STOP in practice, so this is a backstop, not the expected path).

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
