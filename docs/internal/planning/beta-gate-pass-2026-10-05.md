# Beta Gate: measured pass, range, slip rule, per-surface (2026-10-05)

**Owner**: PPM
**Status**: PROPOSAL, read-only. No milestone, Sprint-field, label, or issue state has been changed. Applying anything below needs PM's explicit confirmation (via Exec).
**Revision**: v2, 10-05 ~10:15 PDT. v1 (09:41) was a body-only read and overstated the gate; it is replaced by this comment-verified pass.
**Standard applied**: `beta-gate-standard.md` v0.1, PM-ratified 2026-10-05.
**Answers**: Exec's 09:40 ask (measured table, grounded range, slip rule, per-surface), PM's 10-05 "no guessing, no handwaving".

## How this was measured

- **Run**: `gh issue list --milestone MVP --state open --limit 500` at **09:46 PDT 2026-10-05** returned **31** open issues (the same 31 PPM read at 09:3x; set unchanged).
- **Read**: the full body of all 31 (captured today), **and the full comment thread of every issue that has comments** (the first pass skipped comments, which is why it was wrong: issue bodies are stale and comments carry the landed fixes. #1885, #1735 and #1880 each read as live in the body and were largely fixed in the comments).
- **`Gate class:` line**: **0 of 31** bodies carry one (grep, this turn). Five carry an older `Class:` field (#1595, #1623, #1625, #1632, #1735), which is a different tag. The standard applies to new filings; nothing here predates it with a compliant line.
- **Layer**: issue text and comment text. Code claims inside them were quoted from their authors, **not re-run**. Class assignments are my judgment against the written standard. Where a body or thread is ambiguous I marked it "needs PM ruling" and did not pick.
- **Not measured**: whether the six epic-0 corpus rows exist as rows (two have a comment saying a row was deposited: #1579, #1860; the rest are unverified); whether #1880's fixes have reached the deployed alpha (the comment says "Rides the next alpha deploy"); Epic 0 Phase 3's current count (last stated by Lead on 10-03, not re-measured today).

## Result: 31 issues, five buckets

| Bucket | Count | Issues |
|---|---|---|
| **A. In the gate, work remains, class clear** | 4 | #1889, #1913, #1595 (the epic), #1386 (the sign-off, fires last) |
| **B. In the gate unless PM rules the residue out (needs PM ruling)** | 5 | #1735, #1852, #1907, #1886, #1925 |
| **C. Gate-class work already landed: close, or split the residue** | 4 | #1930, #1885, #1880, #1867 |
| **D. Epic 0 evidence: corpus row, then leave the gate** | 6 | #1579, #1623, #1771, #1783, #1843, #1860 |
| **E. Production (post-beta)** | 12 | #1522, #1625, #1632, #1698, #1817, #1832, #1891, #1911, #1915, #1916, #1917, #1931 |
| **Total** | **31** | |

**The measured gate**: A + B = **9** issues, of which **4 are firm** and 5 depend on a PM ruling. Excluding Epic 0's own two (#1595, #1925), the non-Epic-0 gate is **3 firm (#1889, #1913, #1386) plus 4 needing a ruling (#1735, #1852, #1907, #1886): 3 to 7**. The title-level estimate was about 11 non-Epic-0 gate items. It was high because it counted issues whose gate-class defect had already been fixed (bucket C) and could not see the open residues were mostly PM inputs.

If PM confirms everything as proposed and rules all five bucket-B items out, the milestone goes from 31 to 4. If PM rules them all in, it goes to 9.

## The measured table (all 31)

Columns: **Class** is the standard's class for the live defect. **Body quote** is one line from the body. **GC line** is whether the body carries `Gate class:` (none do). **Latest state** is from the comments, which win over the body.

### A. In the gate, work remains

| # | Class | Body quote | Latest state (comments) |
|---|---|---|---|
| #1889 | 3 Honesty | "a Slack standup over a failed GitHub read still reads like a clean empty." | No comments. Nothing landed. Needs per-format copy decisions (CXO), then wire-through (Lead). **Unsized.** |
| #1913 | 4 Golden path (first conversation after adding a key) | "PM rates it a fail either way: from the user's side a chat vanished." | Lead 10-02: server side verified correct, conversation is listed by the API. **Not reproduced; blocked on two PM answers** (which page; signed in or anonymous during the keyless turn). |
| #1595 | Epic 0 itself | "the largest remaining MVP build, it carries a standing cohort-wide moratorium" | Last comment 09-26 (Arch rulings on unit 4). Remaining per the 09-26 thread: Phase 3 deletions. Sprint goal: every list with a live wave done by **Thu 10-08 21:59 PDT** (Lead owns). Lead's 10-03 estimate: ~155 literals now, ~110-120 after this tranche, ~75 floor. **Not re-measured today.** |
| #1386 | Close-out gate | "Define the gate that formally closes the Beta Blockers sprint" | PM re-scoped 09-06/07: **criteria 2, 3, 4, 5 re-run fresh and criterion 6 signed at MVP close**, as the last step before invitations. Body is stale (still says "Beta Blockers sprint"). Not started, **duration unsized** (see range). |

### B. Needs PM ruling

| # | Class if it stays | Body quote | Latest state and the ruling needed |
|---|---|---|---|
| #1735 | 3 Honesty (residue) | "auto-apply is a SILENT TOTAL NO-OP" | The false-notice defect is **fixed** (`7bcf3adde0`, 09-25). What remains: "`personality_*` now has two durable writers and zero readers"; Lead: "a durable write nobody reads is more misleading now than on 09-08." Options A (read them, needs a CXO visibility call), B (large), C (delete the writers, smallest, honest). **Ruling: is the residue class 3, and which option?** If PM picks C it is small and can close in the gate; if A or B it is Production. |
| #1852 | 4 Golden path, only if the invite names Slack/Google | "Not a launch blocker (no alpha tester uses these integrations yet); should land before any tester is pointed at Slack/Google connect." | Ready since 09-24 and waiting on **PM's provider-console keystrokes** (register callback URLs, say "consoles done"; Lead then sets three secrets). The comment names `alpha.pipermorgan.ai`; the target is `beta.pipermorgan.ai` (R7), so the URLs to register are the beta host's (**unverified** that the secrets/URLs for beta are the same set). **Ruling: does the beta invitation tell testers to connect Slack/Google?** (This is also the class-4 clarification below.) |
| #1907 | 4 Golden path (weakest admit) | "the composer + Send sit below the fold — the input's top edge is just visible at the very bottom, the button is cut off." | No comments. By the letter an iPad tester cannot hold a conversation. **Ruling: is the first wave desktop-browser only?** If yes, Production. |
| #1886 | None cleanly (the system opens a conversation it cannot continue) | "`_handle_add_project` — live, user-reachable. When an 'add project' turn has no extractable name, it creates an onboarding session" | No comments. Pinned by strict-xfail on #1867's census. **Ruling (Arch, then PM): fixed by Phase 3 by construction (then Epic 0 evidence), a Production fix, or a gate item.** My lean: Production unless Arch says Phase 3 covers it. |
| #1925 | Epic 0 completion tail | "They now reach the LLM classifier, hit the stub, and fail with INTENT_CLASSIFICATION_FAILED." | **The fix landed** (Lead 10-03/04: `tests/intent/ -m "not llm"` 205 passed, 0 failed; the 18th test marked `llm`). "The only remaining item is the CI decision": should a workflow run `tests/intent/`. That is Pard's/the CI owner's call and not a gate class. **Ruling: close #1925 and move the CI question to an Ongoing issue?** |

### C. Gate-class work landed: close or split (every one is a PM-confirmed move)

| # | Class | Body quote | Latest state |
|---|---|---|---|
| #1930 | 3 Honesty | "The project is not deleted, after a message that framed it as irreversible." | Step 1 (stop promising) landed, Lead 10-04 20:41, CXO re-verified. Step 2 is #1935 (Production). The issue's own acceptance criteria allow closing on step 1. **Close.** |
| #1885 | 2 Security | "Three LIVE unused invite tokens were in full form in tracked session logs + an omnibus log (public repo)" | **Exposure resolved**: scrubbed on main; Google key deleted and Slack confirmed rotated (PM, 09-25); three tokens burned by PM's hand 09-27 02:16 UTC, output quoted on the issue. Remaining, deferred by PM ("it's not urgent... we can wait til they try and fail"): mint two replacement invites and re-record the roster. That is invite logistics, not a gate class. **Close, with the replacement mint tracked as an ops task.** |
| #1880 | 3 Honesty | "where the ~:356 header states `len(free_blocks)` then shows 3." | Residues 1 and 2 **landed** (`7bfac28f13`, Lead-reviewed; "Rides the next alpha deploy": deploy **unverified**). Residue 3 is latent and "stays open here by design" until #1776 lifts the gather caps. **Close after splitting residue 3 to Production, once the fix is confirmed on the deployed build.** |
| #1867 | None (structural) | "The structural gap remains: 'on ice' lives as a code comment" | The fix-build **landed** (registry census plus enforcement test, 75 passed, 1 xfailed). The open question moved to #1886 ("Both on #1886"). **Close, or fold into #1886; Arch's call.** |

### D. Epic 0 evidence

All carry the issue's own pattern-accretion framing under the standing moratorium. Class 1-3 consequence check done on read for each; none met it, with one caution on #1771 below.

| # | Body quote | Corpus row / latest state |
|---|---|---|
| #1579 | "'show me my …projects' shapes get STATUS/get_project_status at confidence 1.0 … Pattern change itself = moratorium/inversion material." | Deposit executed 09-12 (`1e1438033`); the show-me form "still misroutes at conf=1.0 today"; one Lead/Arch ruling pending on a dead assertion in the corpus builder. **Row exists.** |
| #1623 | "an ACTIVE gathering flow losing its turns to other claimers." | Standup-timeout member fixed (session-keying). 08-15 second member (a draft body answer taken by project lookup) recorded as scope, durable fix is Inversion context-carrying. Row **unverified**. |
| #1771 | "'maybe later', which by its words means KEEP IT FOR LATER, now destroys the resumable flow." | Triage comment only. **Caution**: this abandons a suspended standup session. I judge that conversation state, not persisted user data, so class 1 is not met. PM may weigh it differently. Row **unverified**. |
| #1783 | "it is a CONTRACT question, not a seam question" | No comments. Row **unverified**. |
| #1843 | "'please remove the fluff and make it punchier' → ACCEPT → the flow COMPLETES and presents the unedited draft as final." | 09-23 comment: a second face of the same acceptance-contract ruling, "the ruling" is still owed. Row **unverified**. |
| #1860 | "Not a regression — a known-shaped coverage gap, verified at HEAD" | Deposited 09-23, both phrasings; the Inversion router already routes both correctly. **Row exists.** |

### E. Production

| # | Class | Body quote | Why not a gate class (and what the thread added) |
|---|---|---|---|
| #1522 | none | "scour the codebase for false trails that need to be removed and cauterized." | An inventory; ratchets for two of four legs landed. No user-facing defect. |
| #1625 | none | "Reminders are a bit relentless!" | Design ruling; the FTUX model (08-22 comment) resolves its open question top-down. |
| #1632 | none (CXO may differ) | "Small: read WorkflowEntry.outwardness in the catalog renderer." | Omission in a legibility surface, not a false statement. The 09-24 comment says the remaining gap is a "design call, Lead/CXO scope" and is tracked in #1891. |
| #1698 | none | "every disposed module must remain findable by commit-hash reference" | Disposal epic. It surfaced a broken CLI notion command (filed separately by its lane). |
| #1817 | none | "Not a bug today — a dated assumption with a named expiry" | The trigger is now mechanical (`TestConsentSlotTouchRatchet1817`, in the CI-gating suite), so it cannot trip silently. Ask Arch to concur it stays Production. |
| #1832 | none | "no /health/slack route exists anywhere at HEAD" | Dead-route test; deletion proposal. |
| #1891 | none | "is the most plausible source of the reply PM saw on v70" | Follow-up design question to #1632. |
| #1911 | none on the MCP surface | "It works, but it's unbranded, and it shows the signed-in user as a raw UUID" | MCP surface, via R7's probe and beta period. Revoke-path copy is gated on #1918. |
| #1915 | none | "The city resolver works; the zone-name/abbreviation form doesn't." | Enhancement. |
| #1916 | none | "Piper sees nothing: no callback, no error, no log line." | Copy and a record. Calendar connect is not in the #1386 scenarios. The decisive item is PM's Google OAuth audience choice (below). |
| #1917 | none | "'Needing review' means reviewer-requested status — nothing computes it." | A missing read op, a product ask. |
| #1931 | none | "A completed todo can't be reopened from chat." | CXO ruled 10-04: out of chat is acceptable provided the completion reply promises no undo. |

## Three rulings only PM can give (they size the gate)

1. **Class 4 contradicts itself as ratified.** It says a tester who cannot "connect an integration" is blocked, then defines the golden path as "exactly the scenarios in #1386", which contain no Slack or Google Calendar. #1852 is in or out depending on which sentence wins. Proposed v0.2: **the golden path is the #1386 scenarios plus every integration the beta invitation tells testers to connect.** That turns #1852 into a question of what the invitation says.
2. **Google OAuth audience (Internal vs External/Testing).** Internal blocks every design partner outside the pipermorgan.ai Workspace from calendar connect. Configuration, not code. It decides whether #1916 matters at all and whether the invitation can name Google Calendar.
3. **The five bucket-B calls** above (#1735 option, #1852 via ruling 1, #1907 first-wave device, #1886 via Arch, #1925 CI split) and **the two PM inputs the gate is waiting on**: the #1852 console keystrokes and the #1913 answers.

## The range, re-grounded

PM asked: "what will it take to know it?" Four unknowns remain, each with an owner and a date to resolve. Everything else in the gate is measured.

| Unknown | Owner | Resolves by | Why it moves the date |
|---|---|---|---|
| Size of #1889 (degraded sources through Slack/Markdown/text formatters, `/today`, Radar card) | Lead (+ CXO copy per format) | Wed 10-07, one sizing reply | Only gate item with no landed work and no estimate |
| The five bucket-B rulings, the class-4 clarification, the Google audience, #1852 consoles, #1913 answers | **PM** (via Exec), Arch for #1886 | Wed 10-07 | Up to 5 issues in or out; the two keystroke items are the shortest path to a testable Slack/Google connect |
| Duration of the #1386 re-run at MVP close (criteria 2, 3, 4, 5 fresh, then 6) | PPM + CXO (criterion 3 scenarios), Lead (criteria 2/4/5 runs) | Wed 10-07 sizing, confirmed by a dry run | It begins only after the last gate issue closes, so it sits on the critical path after every other item |
| Epic 0 Phase 3 tail, last stated 10-03, not re-measured | Lead | Thu 10-08 21:59 PDT, the sprint window | The gate cannot close while #1595 is open |

**Stated range, unchanged but now conditional**: design partners from **Fri 10-23**, hard stop **Fri 10-30**. What the measurement changed is not the dates but the confidence: the work remaining is smaller than the title-level count implied (4 firm, 5 pending a ruling, versus about 11), and most of the pending items wait on PM input rather than build time. **What I cannot measure today**, and will not guess: #1889's size and the #1386 re-run's duration. **The range is confirmed or moved on Fri 10-09**, once those two sizings, PM's rulings and Lead's Phase 3 close-out are in, and a move is logged under the slip rule below.

**Assumption on Epic 0**: Lead completes every list with a live wave by Thu 10-08 21:59 PDT (the locked sprint goal). The re-plan trigger already agreed stands: the gate list grows, or the tranche is not done by **Tue 10-14**.

## Slip rule (proposed, edit freely; also entered in the standard)

Exec's proposal is the base: the date moves only on **(a)** an admission with a `Gate class:` line, or **(b)** a change to Epic 0's tranche, and every slip is logged with a named cause and the count before and after. I would draw it with three additions, because the rule as proposed has one hole and no brake:

1. **(c) A measured-unknown resolving larger than assumed.** Most slips are not admissions; they are an existing item turning out bigger than thought. Without (c), "the item was bigger" is an unnamed cause. It qualifies only if the entry cites the sizing evidence and names which of the four unknowns above it is, so the unknowns cannot quietly absorb a slip.
2. **Symmetry.** An un-admission (PM rules something out, or it closes) is logged the same way, so the count is a ledger with entries on both sides, not a number that only goes up.
3. **A brake on endless slippage.** If cumulative slip against the 10-23 baseline passes **7 days**, or a **second** slip is logged, PPM does not propose another date. PPM brings PM an explicit choice: cut scope (name the items) or accept the later date as a decision. That is the structural answer to "question endless slippage": past the brake, a date cannot move by default.

Who moves the date: **PM only.** PPM proposes with the entry already drafted; the design-partner date and the 10-30 hard stop do not change on PPM's say-so. A slip entry has: date of entry, old date, new date, cause (a, b or c), issue numbers, gate count before and after, evidence link. **A slip without a cause line is not recorded and the date does not move.**

**Slip ledger** (the one place this lives; PPM keeps it):

| Entered | Design partners | Hard stop | Cause | Issues | Gate count before → after | Evidence |
|---|---|---|---|---|---|---|
| 2026-10-05 (baseline) | Fri 10-23 | Fri 10-30 | none: baseline | n/a | 31 in the milestone; 9 under this proposal (4 firm, 5 pending rulings) | this document |

## Per-surface instantiation (R7, PM 2026-10-05 via Spec): folded in

No surface "is" the MVP. The MVP is a core capability set with varying instantiation per surface. The admission classes apply to the core set; the level required per surface:

| Surface | Required for beta | How it is held |
|---|---|---|
| Hosted web UI (`beta.pipermorgan.ai`) | **Yes** | The gate: four classes, the MVP milestone. All 9 gate issues in A and B are web-UI or core-capability issues. |
| MCP / plugin | **No.** Released and tested during the beta period (starts when the MVP milestone closes and Production work begins). PM tests before anything is listed. | PA's cheap demand probe. MCP-only polish is Production (#1911). An MCP-surface defect that loses data, exposes a credential, or states something false would still be class 1-3 and gated. |
| BYOC / local | **Not ruled.** PM: the idea that BYOC becomes the primary usage "has likely taken hold and perhaps distorted" the thinking. | Not a gate surface unless PM rules otherwise. |

My reading, flagged for PM correction: a defect is admitted by its class on the surface the beta ships, not by surface. **"What has to be working in the MVP to release the beta" stays PM's open call**; this standard bounds how the gate list may grow, it does not decide the capability set.

## What happens next

Nothing on the board until Exec relays PM's yes. PM's sprint ruling is settled: the MVP milestone is the gate and equals the "Beta Blockers" Sprint value today; **no Sprint-field or label edits from PPM**. One open point for PM, not an ask: once issues leave the milestone, the Sprint value will diverge from it, and cleaning that is a PM-confirmed step when he wants it.

On the yes: close #1930 and #1885; split and close #1880 and #1867; milestone-move the 12 Production items and, after the corpus-row check, the 6 evidence items; rewrite #1386's body to point at the milestone; apply PM's rulings on bucket B.

Verified how: method is `gh issue list` (count and set, 09:46 PDT), full bodies and full comment threads of the 31 read today, and a grep of the 31 bodies for `gate class`; layer is issue and comment text, not source or live behavior; denominator 31 of 31 bodies, and every issue that has comments had its thread read (22 of 31 have none or only a triage line). Corpus-row existence for four of six epic-0 items, #1880's deploy status, and Phase 3's current count are **unverified**.
