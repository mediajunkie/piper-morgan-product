# CIO Memory Export — pre-migration full backup

**Purpose**: full, verbatim export of CIO's auto-memory store, ahead of migrating to a new Anthropic account (pipermorgan.ai) and device (Amber). Claude Code's memory system is scoped per-account (and, separately, per-filesystem-path) — none of this content is automatically visible to a session running under a different account, regardless of device or repo path. This file exists so the content survives the account boundary: it's git-tracked, which is account-agnostic.

**Source**: `~/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-product/memory/` on the designinproduct.com account, exported 2026-07-24 directly from the file listing on disk (not from `MEMORY.md`'s own index, which was found to be stale — 146 indexed entries vs. 162 actual files, a ~16-file gap not otherwise investigated here).

**How to use this on a fresh session**: read this file (or have it summarized) at first orientation on the new account. It won't restore Claude Code's native per-file memory retrieval UX, but the actual content — every rule, correction, and piece of project context — is all here, verbatim, organized by type.

---

## FILE: feedback_accessibility_over_precision_in_blog_review.md

```markdown
---
name: accessibility-over-precision-in-blog-review
description: "When fact-checking or reviewing PM's public blog drafts, distinguish factual/attribution errors (always flag) from internal-jargon-for-accessibility trades (a deliberate, repeated editorial choice — don't reflexively \"correct\" these back to the precise internal term)."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

When reviewing or fact-checking PM's public-facing blog drafts (Building Piper Morgan series), two different things can look similar but need different treatment:

1. **Factual/attribution errors** — wrong timestamps, misattributed quotes, inflated counts, claims that don't match the source logs. Real errors regardless of context; always flag and fix.
2. **Internal-jargon-for-accessibility trades** — swapping a precise internal term (e.g. "M2", "Model A") for a more legible one (e.g. "MVP", a plain-language description) even though the swap loses some internal precision. This is a deliberate, repeated editorial choice for this blog series, not sloppiness — don't reflexively flag it as an "error" the way a wrong timestamp is an error.

**Why:** 2026-07-07, PM pushed back when I "corrected" a sentence back from PM's own edit — PM had rewritten "the M2 quality gate closed at 82%" as "we closed our MVP quality sprint," and I reverted it, reasoning that MVP (the overall unshipped 0.9.0 milestone) isn't the same thing as M2 (one gate within it). PM's response: "I don't think characterizing M2 as the MVP's quality sprint is incorrect at all." On reflection PM was right — "we closed our [MVP quality] sprint" doesn't literally claim MVP shipped, it names one sprint via a descriptive label (same construction as "our Q2 planning sprint" not claiming Q2 itself ended) — and the M2→MVP swap was consistent with everything else PM had directed that same session (dropping "Model A," spelling out cron-lifecycle/worktree in plain language instead of internal shorthand). I had over-indexed on matching the old sentence's internal terminology instead of weighing the accessibility trade-off PM was making on purpose.

**How to apply:**
- Before flagging a "this doesn't match the internal/precise term" finding, ask whether it's actually a *factual* error (the claim is untrue) or a *legibility* choice (a technically-less-precise but reader-friendlier substitution for insider terminology). Only the former is a hard finding.
- When genuinely unsure which it is, surface it as an open question ("this trades X precision for Y readability — intentional?") rather than unilaterally "fixing" it back to the internal term.
- Don't fold instantly when PM pushes back, either — genuinely re-examine the specific wording used (e.g. "closed our MVP sprint" vs. a stronger claim like "MVP shipped") before conceding; anti-sycophancy cuts both ways, but so does actually being persuadable by a good argument.
- This composes with [[feedback_three_registers_dont_assume_reader_context]] (drafting side: don't leak internal terms to readers) — this is the reviewing-side corollary: don't re-introduce internal terms during a fact-check pass in the name of precision.
- Still verify claims that ride along with an accessibility swap independently — in this same instance, PM's rewrite also introduced a new acronym (MVP) needing its own first-use gloss, and I initially glossed it wrong from memory ("minimum viable product") — this project's canonical glossary deliberately defines it as "Minimum Valuable Product" (`knowledge/piper-morgan-glossary-v1.1.md`), added after a prior Ship-edit false-unpacking incident of this exact mistake. Never spell out an acronym from memory, even mid-review, even when the swap itself is legitimate — check the glossary.
- **Confirmed from the other direction, 2026-07-11**: when *I* dropped an internal-catalog reference during a fact-check (a "Pattern-073 instance #14" attribution that turned out to be misapplied per the methodology owner's own ruling — softened to a vaguer "thirteen instances on file" rather than assert a wrong specific number), PM confirmed the softened version was the right call independent of the factual issue: "I think references to #14 are too detailed for many people anyhow." Internal catalog/pattern/issue numbers are reflexively droppable for general-audience legibility — this isn't only something to watch for when PM does it, it's a good default move for me too when resolving a factual snag in a specific-number claim.

```

---

## FILE: feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately.md

```markdown
# Read-and-used items move to read/ immediately — no "addressing" hold

**PM correction 2026-05-15 ~11:29**: "Why are the workstream memos not moved to read, btw?"

## The wrong pattern

Holding read-and-absorbed items in `inbox/` with status `addressing` while a downstream artifact (Ship draft, synthesis memo, etc.) is in flight. The inbox accumulates "currently using" items that have actually been processed; the manifest gets noisy; new arrivals get buried by held items.

## The right pattern

Once you've **read** an item AND **used** it (absorbed into a draft, synthesized into a response, factored into a decision), move it to `read/`. The downstream artifact (Ship draft, the response memo, the decision-log entry) is the record that the item was used. The inbox does not double as a workspace for in-flight synthesis.

- Synthesis happens in `dev/active/` (Ship draft, working docs)
- Source memos go to `read/` once absorbed
- Inbox is for arrivals not yet read OR not yet acted on

## Applies to

- Workstream review memos (move once synthesized into Ship draft)
- CC awareness items (move on frontmatter-read)
- Direct asks (move once the action is taken or the response is sent)

## Anti-cases (legitimate inbox holds)

- Items genuinely waiting for an unblocked moment to act on
- Items that need a specific external signal before processing
- Items where the action itself is "review and respond" and the response hasn't gone out yet

If you can't name a specific blocked action, the item belongs in `read/`.

## Operational sharpening (PM 2026-05-24 ~14:28)

Today's Ship #044 workstream kickoff was moved to `read/` after reading the content — but the *downstream artifact* it required (the Comms workstream memo) had not yet been filed. PM flagged the visibility loss: from PM's view the kickoff disappeared into `read/`, signaling "handled," when in fact the work was still owed. Same shape as the orphan-drafts incident the same day — visibility loss after moving out of the active queue.

**Sharpening on "used":** read-and-used means the **downstream artifact required by the memo exists**, not just that the memo content has been mentally processed. Mental absorption is *read*; artifact existence is *used*. They are different moments and the gap can be days.

**Operational rule (annotate-in-inbox approach):**

Move to `read/` only when ALL of:

1. Memo content has been processed (read for understanding)
2. Any required downstream artifact (workstream memo, response, decision-ratification, file edit, ack, etc.) **exists** — OR no downstream artifact is required

Stay in `inbox/` when content is processed but the required artifact doesn't yet exist. Annotate the inbox MANIFEST entry with explicit *"Active until {artifact}"* naming the gating artifact (e.g., *"Active until workstream memo filed (drop-dead Tue May 26 EOD)"*).

This keeps the discipline at 2-state (inbox / read) — no new folder — while making the gating artifact explicit in the MANIFEST. Inbox naturally surfaces what's still actively in flight; read/ means *done*, with the downstream record as the proof.

Stacks with `feedback_per_memo_commit_push` (each move is its own commit) and `feedback_mailbox_writes_main_only`.

## Further refinement (PM 2026-05-27 ~07:21)

The "downstream artifact exists" threshold for workstream-review memos is the *Ship draft*, not the *published canonical*. The workstream memo's job is to inform the Ship synthesis — once the draft exists, the memo has done its work; the publication-pipeline (PM voice-pass + Docs publish) is a separate downstream artifact for the Ship itself, not for the memos.

I was being too conservative on Ship #044 — holding the 6 memos in inbox annotated "Active until Ship #044 published canonical" when "Active until Ship #044 v0.1 drafted" would have been the right close-condition.

**Operational refinement**: when annotating "Active until {artifact}", pick the *earliest* artifact that satisfies the memo's purpose, not the latest downstream consequence. Workstream-memo → Ship draft (not published). Disposition request → ratification memo (not the implementation). Decision input → decision memo (not the executed change).

```

---

## FILE: feedback_adjacent_story_number_contamination.md

```markdown
---
name: adjacent-story-number-contamination
description: "When fact-checking a specific number/claim against a primary source, verify the number is attached to the SAME event the draft describes — not just present somewhere in that source document, which can be a different, unrelated nearby story."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

"Verify against primary sources, not the omnibus" catches most fact-check errors, but doesn't automatically catch one specific failure mode: a real, checkable number exists in the primary source document, and is even genuinely accurate — it's just describing a *different* event than the one the draft attaches it to. The number is real, the source citation is real, and a shallow check ("is this number in the primary log? yes") passes — but the number belongs to an adjacent, unrelated story that happens to share the same log file or session.

**Why:** 2026-07-11, this exact shape hit twice in one day on two different blog drafts, independently:
1. A draft attributed its opening incident to "Pattern-073 instance #14" — #14 is a real, correct number, but it labels a *different* finding (the mailbox MANIFEST's own stale-content-vs-disk claims) than the story the draft actually tells (a skill's docs not matching its code) — CIO's own ruling explicitly separated the two as distinct findings from the same incident.
2. A different draft claimed a stranded-draft recovery "took ninety minutes" — ninety minutes is a real duration that appears in the exact same source session log, but it describes an unrelated May 10 workstream-review incident, not the recovery being described.

Both times, a plausible, checkable, *genuinely real* number was sitting in the primary source — just attached to the wrong sentence in the draft, most likely because a research or drafting pass pulled a nearby fact out of the same document without checking it matched the specific event under discussion.

**Third confirming instance, 2026-07-12** (different draft, same day as instances 1-2 were only one day old): a draft said a new production-release tag "went on the March 4 commit." March 4 was real and in the primary source — it was just the *old*, frozen position production had been sitting at, not where the new tag actually landed (a June 3 commit, per the same log). Same shape exactly: two real facts about the same general topic, sitting near each other in one primary log, and the draft grabbed the wrong one. Three independent hits in two days confirms this isn't a rare edge case — it's a standing, checkable risk worth its own verification step, not an occasional surprise.

**How to apply:**
- When fact-checking a specific number, name, or attribution, don't stop at "is this in the primary source" — confirm the source's own text ties that number *to the specific event the draft is describing*, not to some other event narrated nearby in the same document.
- Be extra alert to this when a source document is a session log or omnibus covering multiple stories/incidents in one file — these are exactly the documents where two unrelated numbers can sit a few paragraphs apart.
- If a number checks out as "present in the source" but you can't find the specific sentence that ties it to *this* event, treat it as unverified, not confirmed — soften or flag rather than let a real-but-misattached number through.
- This composes with [[feedback_first_person_attribution_vs_event_accuracy]] (separating "did this happen" from "who said it") — this is a third axis: "is this specific fact attached to the right event," distinct from both.

```

---

## FILE: feedback_affirmative_direct_over_disclaim_then_affirmative.md

```markdown
---
name: Affirmative direct over disclaim-then-affirmative
description: PM's sentence-construction preference. When a "wasn't this but was that" construction would work, the direct affirmative usually reads stronger.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
In published prose, PM prefers the direct affirmative form to the disclaim-then-affirmative form when the direct one works.

**Move PM applied in May 13 Ship #042 cross-post:**
- Original: *"The interesting part wasn't the verdict — it was the short cleanup list that surfaced."*
- Edit: *"The interesting part was the short cleanup list that surfaced."*

The disclaim-then-affirmative construction (*"wasn't X — was Y"*) sets up an expectation and then redirects. It earns its keep when the expectation it disclaims is one the reader was likely to bring in — e.g., correcting a common assumption. It reads weaker when no such assumption needed correcting; in that case it sounds like the writer setting up their own pivot.

**How to apply:**
- Before shipping a "wasn't this — was that" sentence, ask whether the disclaim is doing real work. Is the reader likely to assume the disclaimed thing? If yes, the construction earns keep. If no, the direct affirmative usually reads cleaner.
- Same shape: "not only X, but also Y" / "more than just X, this is Y" — both can be load-bearing when X is a real assumption to correct, or weak when X is filler.
- Don't apply rigidly; sometimes the disclaim-then-affirmative establishes rhythm or surprise. The check is whether it's doing work.

**Memory-chain neighbors:**
- `feedback_editing_voice.md` — broader voice discipline.
- `feedback_no_superlatives_without_verification.md` — related "drop the rhetorical move when it isn't earning keep" theme.

```

---

## FILE: feedback_agent_naming_convention_in_public_prose.md

```markdown
---
name: feedback_agent_naming_convention_in_public_prose
description: "How to name agents in public-facing blog prose — \"my [role] agent (ACRONYM)\" form"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

In public blog prose (Building Piper Morgan, insights, ships), the preferred convention for naming agents on first use is:

> "my [full role name] agent ([ACRONYM])"

Examples:
- "my chief experience officer agent (CXO)" — not "The experience-design role (CXO)"
- "my principal product manager (PPM)" — not "The product-management role (PPM)"
- "my architect agent" or "my chief architect (Architect)"

**Why:** The earlier "The [role description] role ([acronym])" form was an abstraction that lost track of who was actually who — PM named this the "earlier form of euphemism." The possessive + full role name + acronym in parens is clearer and more personal.

**How to apply:** On first use in any public post, name the agent with the possessive + full role + acronym. Subsequent references can use just the acronym or a short-form ("CXO", "PPM", "the architect").

Confirmed by PM 2026-06-23 during Beat 8 voice-pass review.

```

---

## FILE: feedback_agent_who_notices_updates_stale_info.md

```markdown
---
name: agent-who-notices-updates-stale-info
description: "The agent who notices stale documentation should update it immediately, not defer to the \"owner\" role — reduces time-to-fix and avoids perpetuating stale info."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

Update stale documentation on the spot when you notice it, don't defer to Docs or a designated owner.

**Why:** More efficient; reduces the window during which stale info perpetuates. PM 2026-06-19: "the agent that notices stale info should be the one to update it."

**How to apply:** When reading a doc and noticing an outdated "YOU ARE HERE" marker, a wrong current version, stale dates, or obsolete state — update it in the same session. Don't add a TODO or route to Docs unless the update requires knowledge you don't have. A partial update is strictly better than no update. (Same principle as the BRIEFING-CURRENT-STATE staleness rule in CLAUDE.md.)

**Scope boundary — this rule is for status/state docs only.** It does NOT extend to `.claude/skills/*/SKILL.md` or other shared procedure artifacts (hooks, templates, CLAUDE.md). Those prescribe *what every agent should do*, not *what's currently true* — silently routing around stale or conflicting skill instructions (even correctly) leaves the staleness in place for the next agent and isn't an individual agent's call to resolve alone. See [[skill-spec-gaps-and-staleness]] for the discuss-with-PM-first procedure that applies there instead.

```

---

## FILE: feedback_anchor_on_attention_board_diff_forward.md

```markdown
---
name: feedback_anchor_on_attention_board_diff_forward
description: "To answer \"what needs me / what's changed\", anchor on the most recent attention board and incrementally diff forward — don't re-derive from a fresh git sweep."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM (xian) 2026-06-27: expected Exec to verify "anything urgent/blocked by me?" by **looking at the most recent attention board and incrementally checking what's changed since** — rather than re-deriving state from a from-scratch git-log sweep.

**Why:** the attention board IS the canonical "what needs PM" surface (the cohort-attention-rollup). It already encodes the triaged decisions/blockers/awareness state. Re-deriving from raw git ignores that reference frame and risks drift from what PM last saw. The board is the baseline; the job is the delta.

**How to apply:** keep a current board (render at START / first PM engagement per the skill cadence — don't hold it if PM is already engaging). To answer a "what needs me" query: open the latest board, then diff forward (new memos, new commits, resolved items) and report what *changed* against it. Pair with [[feedback_extract_questions_from_pm_cc_memos]] (surface buried cc'd questions) and [[feedback_attention_board_sweep_not_vantage]] (sweep-and-verify, GitHub-verify each item).

```

---

## FILE: feedback_anchor_on_readiness_not_publish_date.md

```markdown
---
name: feedback-anchor-on-readiness-not-publish-date
description: "Synthesis deliverables have a two-half rule — when source set is COMPLETE draft NOW (don't pace to publish date); when source set is INCOMPLETE and deadline approaches ESCALATE NOW to the source-owner (don't fold the gap as narrative caveat). Stop anchoring on the publication date in either direction."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef776fbb-3c64-4701-b1ba-2aa37c3221ce
---

For synthesis deliverables (Weekly Ship, omnibus, briefing, response memo), the publication date is **not** the pacing anchor. The pacing anchor is the **source-set state**. Two halves:

## Half 1 — source set COMPLETE → draft NOW

The moment the full source set is in hand, draft. Do not pace to the publication date. Do not wait for nice-to-have sources unless they would redirect (not refine) the spine.

## Half 2 — source set INCOMPLETE + deadline approaching → ESCALATE NOW

If a load-bearing source hasn't arrived as the publication window closes, the **escalation to the source-owner is the unblocked work** — not drafting around the gap. Do not absorb the absence as a narrative caveat in v0.1. Do not pace to publish-date hoping it lands. Chase the source-owner directly: the kickoff memo (sent earlier) is not enough; a dedicated chase memo naming the publication deadline + asking for ETA or blocker is required.

**Why:** PM corrections 2026-06-09, paired:
- 12:03 PM: *"As soon as you had all the memos back it was time to write that draft. Anchoring on my intended publishing date uses up all my slack."* — Half 1 (complete source set → draft NOW; don't pace).
- 1:03 PM: *"You should not write the Ship until you have all the workstream reviews. If it has not arrived by now please notify Arch!"* — Half 2 (incomplete source set → ESCALATE NOW; don't draft around the gap).

The Ship #046 case: I had 5 of 6 workstream memos by EOD Jun 5 with strong spine convergence. I (a) paced to Mon/Tue draft instead of drafting Sat/Sun (Half 1 failure), AND (b) drafted from incomplete source set on Tue noon when PM resumed me instead of chasing Architect's lane (Half 2 failure). I had Comms's Jun 8 memo explicitly flagging the Architect-lane absence and I folded the absence as a narrative caveat instead of escalating. The escalation to Arch was the unblocked work; the synthesis was source-set-gated.

**How to apply:**
- **At plan-time** for any synthesis deliverable, name the full source set explicitly (e.g., for a Ship: "6 of 6 workstream memos required; if any missing 48h before publication window opens, escalate chase").
- **At every checkpoint** (each fire, each session start), compare current source set to required source set. Branch:
  - **Complete:** draft now (don't pace to publish date).
  - **Incomplete + deadline > 48h out:** standard wait; sender already has the kickoff.
  - **Incomplete + deadline < 48h:** **escalation chase to source-owner is the unblocked work** — a dedicated chase memo, not just a kickoff re-reference. Name the publication deadline. Request ETA or blocker. CC PM.
- The publication date is the **backstop** for both halves: ignore it as a pacing target (Half 1) AND treat it as the timer for escalation (Half 2).

**Stacks with:**
- [[feedback_deadlines_are_triage_tools_not_default_pacing]] — same family, source-set-state replaces deadline as the pacing anchor
- [[feedback_pre_authorized_for_unblocked_work_just_do]] — synthesis is unblocked work when source set is complete; escalation chase is unblocked work when source set is incomplete near deadline
- [[feedback_duty_cycle_is_not_a_reason_to_shrink_work]] — duty cycle's value is throughput, not pacing
- [[feedback_respond_to_mail_asap_even_when_no_urgency]] — when Comms's Jun 8 memo flagged the Arch gap, the Right Move was the immediate Arch chase, not "I'll fold the absence when I draft"
- [[feedback_make_promises_durable_no_happy_talk]] — the discipline-mechanism is the explicit source-set-named-at-plan-time + checkpoint-against-source-set at every fire

Sharpest failure mode: Ship-cycle synthesis with PM-visible publication target. Both halves operate.

```

---

## FILE: feedback_asyndetic_adjective_style.md

```markdown
---
name: PM uses asyndetic adjective stacks as style choice
description: When PM stacks coordinate adjectives without commas (e.g., "cheerful dutiful agents"), it's intentional voice, not a missed comma
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
When PM writes coordinate adjectives without separating commas — "cheerful dutiful agents", "rare and sparse attention" stacked stylistically, etc. — that's an intentional voice choice, not a punctuation error. Don't reflag in subsequent proofreads.

**Why:** PM, May 3 2026: *"kept the run on cheerful dutiful as a style choice."* Asyndetic adjective stacks (no commas, no "and") give a piece a particular cadence — slightly more compressed and run-together than standard journalistic prose. It's a craft decision, not a slip.

**How to apply:** When proofreading, asyndetic stacks count as voice. Standard typographic conventions (apostrophes for possessives, capitalization, em-dash spacing, etc.) still get flagged as usual; coordinate-adjective comma omission does not.

```

---

## FILE: feedback_attention_board_sweep_not_vantage.md

```markdown
---
name: feedback_attention_board_sweep_not_vantage
description: "PM 6/16 \"when was your last attention sweep of the other agents?\" — caught Exec maintaining the cohort attention board from its OWN vantage + spot-checks, not sweeping all 10 escalations docs + GitHub-verifying. The rollup is a sweep-and-verify, never a from-memory tracker."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM 6/16 ~08:37, one question: **"When was your last attention sweep of the other agents?"** The honest answer was *never, this session* — I'd been "refreshing" the `exec-attention-board.html` from my own vantage (the items I knew about from my fires + memos) plus targeted spot-checks (Ship #047, BYOC), NOT running the `cohort-attention-rollup` skill's actual Step 1 (read all `dev/active/duty-cycle-escalations-{role}.md`) + Step 2 (live-state verify each candidate vs GitHub).

**Why it matters (what the real sweep found):** vantage-maintenance fails two ways at once. (1) It silently **misses other roles' PM-items** — I'd surfaced none of the cohort's items because I wasn't reading their docs. (2) It **inherits stale-doc phantoms** — most escalations docs were 1–3 weeks stale (PA 19d, CIO 22d, HOST/Docs since 6/3) and listed CLOSED work as open: #1165 / #1193 / #1133 all closed, the "$70/mo Routines watchdog" superseded by the shipped launchd watcher, PDR-005 long-ratified. A board rendered straight from those docs (or from my memory of them) would have shown PM a queue of decisions already made or non-existent.

**How to apply (every board refresh):**
1. **Sweep the source set**: read EVERY `dev/active/duty-cycle-escalations-{role}.md`, not just the items you remember. The board is a rollup of the cohort's docs, not a tracker of your own threads.
2. **Live-state verify each candidate PM-item vs GitHub** (`gh issue view <n> --json state`): a closed issue is not an open decision. Treat the docs as stale-prone perspectives, never ground truth.
3. **An empty verified decision-queue is a feature** — but you can only *claim* it's clean after the sweep+verify, not by inference.

This is the same shape as the cron-prompt drift ([[feedback_careful_git_sync_on_shared_main]]'s sibling lesson) and m-41: a canonical procedure (the rollup skill) got shortcut into a from-memory variant. The cure is *run the skill*. Stacks with the 6/14 live-state-verification catch (don't render from a stale source) — this is that lesson one level up: sweep the right *sources*, don't just verify the ones you happen to recall. Cohort meta-finding: the escalations-doc discipline is itself silently lapsing cohort-wide → flag HOST (trust) + CIO (duty-cycle methodology).

**Refinement (PM 6/21): the carry-forward lags reality for heads-down roles — cross-check commit-activity, not just the doc.** PM flagged that Lead "may not be updating their carry-forward when head's down" (and PM compensates by checking in directly). The sweep reads carry-forwards as the source — but a *freshly-written* carry-forward can still be stale, because a heads-down role ships code/commits without pausing to update their tracker. **So Step 2's live-verify must include the role's GitHub commit-activity (the always-fresh signal), not only `gh issue view` on the items the carry-forward names.** Worked instance, caught within minutes of PM's flag: the 6/21 board showed "Redis prod-exposure — *pending PM's go*" (sourced from Lead's carry-forward, which was only 24 min old) — but Lead had **FIXED it 3h prior** (`#1311` closed, localhost-bind, verified). The carry-forward lagged its own author's commits; the board inherited a phantom "needs you / security" item. A `git log --since` cross-check against Lead's commits caught it. **Rule: every sweep, scan recent commit-activity for the busiest/heads-down roles (Lead especially) and reconcile against what their carry-forward claims — commits don't lie, trackers do.** (Codified into the runbook §4 + iteration log.)

**Two-way (PM 6/21): the cross-check feeds back, not just inward.** PM: *"checking commits is a great idea and perhaps nudging or guiding agents whose trackers are stale can follow from that."* So when the commit-cross-check reveals a stale tracker, **gently guide that agent to update it** (heads-down-aware — frame it no-interrupt, "fix when you next surface," never a demand mid-flow). This turns a one-way board-correction into a **cohort tracker-hygiene loop**: the board stays honest *and* the trackers get better → future sweeps + PM's own direct check-ins both get more reliable. First instance: Lead's carry-forward still said Redis "pending PM go" after `#1311` closed → gentle nudge to refresh. This is the coordinate-through-Exec mandate ([[project_exec_coordinates_more_through_pm]]) applied to tracker-hygiene.

**The stakes (PM 6/18): the board is PM's trust-instrument for *disengaging*.** PM: *"it calms my mind knowing things are running smoothly as I attend to my OpenLaws project."* So a false "all clear" isn't untidy — it's a trust breach, because PM has stopped looking elsewhere and is relying on the board to be the whole truth. The failure mode to guard against: after a long quiet stretch the sweep *feels* skippable — exactly when PM is most reliant on it. Verify-don't-assume is load-bearing for PM's peace-of-mind, not cosmetic tidiness. (This is HOST welfare-criterion D — no silent non-surfacing: a quiet board must mean *verified-clear*, never *haven't-checked*. Twice on 6/18 a quick verify flipped what I'd have reported — Ship #047 "overdue" was actually published, arch "dormant" had resumed; render-from-assumption would have lied to a PM who'd disengaged.)

```

---

## FILE: feedback_audit_cascade_n_a_count_signals_template_drift.md

```markdown
---
name: Multiple N/A flags in one audit signals template drift
description: When audit-cascade prep produces 5+ "N/A" flags on a single issue's audit, treat it as a signal that the underlying template has accumulated staleness (not just that this issue is unusual). Surface to PM for hygiene review rather than silently marking-and-moving.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When audit-cascade prep produces **5 or more "N/A" flags** on a single issue's audit (issue / gameplan / prompts), treat it as a signal that the underlying template has accumulated staleness — not just that this issue is unusual.

**Why:** May 6 incident — #1053 prompt audit produced 6 N/A flags (Post-Compaction, Audit Matrix Format, Method Enumeration, Server State, Claude Code Specifically, Cursor Agent Specifically). Three or four would be normal for an out-of-shape issue, but six in one audit hit a noticing-threshold for PM:

> "We don't even work with Cursor Agent anymore, so some of these conditions are due for a review."

That observation became #1058 (template hygiene review). The signal was real: the template hadn't been pruned as practice evolved, and the audit-cascade discipline forced the staleness to the surface.

**How to apply:**

- During audit-cascade prep (any of the 3 phases), keep an explicit count of N/A flags as you go
- If the count crosses ~5 for a single document audit, **note it explicitly in the audit doc** with the heading "N/A count signals possible template drift"
- When STOP-and-asking PM about specific N/A items, mention the cumulative count and pattern: e.g., "6 N/A items on this audit — wanted to flag the count itself in case the template is due for a hygiene pass"
- Don't go fix the template yourself — that's a separate decision PM owns; just surface the signal
- Discovered-work disposition: file an issue (like #1058) so the hygiene pass is tracked even if not done immediately

**Threshold rationale:** A single-issue audit with 0-2 N/A flags is normal (templates are general; not every section applies). 3-4 N/A flags suggests the issue is unusual but the template is OK. 5+ flags suggests the template is no longer matching the shape of current work, regardless of how unusual the specific issue is.

```

---

## FILE: feedback_batch_drafted_pieces_share_lapses.md

```markdown
---
name: batch-drafted-pieces-share-lapses
description: "When a review catches an editorial lapse (voice error, missing gloss, structural gap) in one piece, check whether it was drafted in the same batch/commit as other still-unreviewed pieces — the lapse is very likely shared across the whole batch, not isolated."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
  modified: 2026-07-21T19:43:09.714Z
---

Blog drafts often get created several-at-a-time in one commit (e.g., "Beats 14-16 first drafts" in one sitting). If one piece from that batch surfaces a systemic issue — third-person voice instead of first-person, a missing convention, a structural gap — the other pieces from the same batch are good candidates to have the identical issue, since they were likely produced by the same drafting pass/session with the same blind spot.

**Why:** 2026-07-21, PM's edit to "What the Running System Found" fixed a third-person-PM voice error ChatGPT/a subagent had introduced. That piece was drafted in the same commit (`fbeb81133`, Jun 16) as two others — "Into Production" and "Almost Beta." "Into Production" had already been caught and fixed independently (Jul 14). "Almost Beta" had NOT been touched and had the exact same third-person-PM lapse, sitting untouched in the queue for weeks. PM explicitly asked to scout ahead once the pattern was visible, and it turned out to be exactly this shape — one shared drafting-pass defect across a whole batch, not a one-off.

**How to apply:**
- When a review catches a systemic (not one-off-typo) issue in a draft, check `git log` for the commit that created it — if other files were created in the same commit, check them for the same issue before assuming it's isolated.
- Don't stop at "the one that got flagged is now fixed" — actively scout siblings from the same batch, even if they aren't the current review target.
- Also worth checking a few pieces *beyond* the batch (the next several in the queue) to confirm the lapse doesn't extend further — a clean scan there is useful positive evidence that the issue was genuinely contained, not just unconfirmed.

```

---

## FILE: feedback_batched_quiet_fires_has_gap_b_vulnerability.md

```markdown
---
name: feedback-batched-quiet-fires-has-gap-b-vulnerability
description: "The batched-quiet-fires convention (don't commit each clean IDLE fire; batch until STOP) assumes STOP will fire. Session-death between batched fires and STOP strands the batched entries uncommitted in working tree."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef776fbb-3c64-4701-b1ba-2aa37c3221ce
---

The duty-cycle batched-quiet-fires convention reads: *"consecutive clean-IDLE fires don't each commit; batch until next substantive event or STOP."* The convention has a **Gap-B (session-death) vulnerability**: it assumes STOP will fire, which breaks the moment the session goes dormant between a batched IDLE fire and the scheduled STOP.

**Why:** Jun 10 incident — I batched a Fire 4 (17:32) clean-IDLE cycle-log entry intending STOP at 23:32 to commit it. Session went dormant between 17:32 and 20:32; cron `26c018ed` died with the session; Fires 5 + STOP never executed; Fire 4 entry was stranded uncommitted in working tree. PM noticed at 06:15 the next morning: *"You did not commit at 20:32 or STOP. Any idea why?"* The convention's "STOP commits the batch" model failed silently because the assumption "STOP will fire" failed silently.

This is the same shape as the *operating-data-invalidates-its-own-design* pattern from Weekly Ship #045: a discipline-layer convention (batch-don't-commit) made structurally-sense at design-time but produced a failure mode under conditions the design didn't anticipate (session-death between batch and STOP).

**How to apply:**

1. **Commit batched entries before going IDLE**, not at STOP. The cycle log entry for a clean fire is short (3–8 lines); the commit overhead is negligible. The recovery cost of a stranded batch is large (PM-visible silence overnight + retroactive close + the worse failure mode of "PM thinks an agent is running, it silently isn't" — HOST's expectation-violation seam).

2. **The batched-quiet-fires convention as designed**: was correct *only* under the assumption that STOP fires reliably. The Routines watchdog (PM decision still pending) is the mechanism layer that would catch session-death between fires; until that's built, the discipline-layer rule is "commit every cycle-log entry, even batched ones."

3. **Why this is a real reduction in convention value, not just a tightening**: the batched-quiet-fires convention's whole point was reducing commit noise during long IDLE stretches. Per-fire commits restore some of that noise. The tradeoff is: PM-visible-state-integrity > commit-log cleanness. Worth it until the watchdog ships.

4. **Composes with the Ship #046 lesson** (PA's `feedback_pace_verified` arc + my deadline-discipline pin): when a "pace-saving" convention has a silent-failure mode under operational conditions, the silent-failure cost beats the pace savings. Discipline costs are negotiable; silent-failure costs are not.

**Stacks with:**
- [[feedback_commit_immediately_after_write_for_new_files]] — extends to: commit immediately after appending any cycle-log entry, even short IDLE-batched ones
- [[feedback_make_promises_durable_no_happy_talk]] — "I'll commit at STOP" is a promise without a durable mechanism (session-death breaks it); per-fire commits are the durable mechanism
- The Routines watchdog decision still on PM's plate — yesterday's incident makes it newly load-bearing (the watchdog would have surfaced the cron-death within minutes)
- methodology-41 (Mechanism Displaces Unreferenced Discipline) — per-fire-commit-discipline survives vigilance lapses; STOP-only-commits doesn't survive session-death

**Discovered:** Jun 10 → Jun 11 session-dormancy incident; PM nudge at 06:15 Jun 11 surfacing the gap. Cohort context: CXO independently diagnosed cron-dormancy at 06:15 same morning; multiple roles hit related Gap-B failures during the same window.

```

---

## FILE: feedback_blog_template_and_voice_guide_canonical_for_proofreads.md

```markdown
---
name: blog-template-and-voice-guide-canonical-for-proofreads
description: "blog-post-template.md + xian-voice-tone-guide.md are canonical references for every blog/insight/narrative proofread. Check them first, not memory. Working from memory + memory-pins instead of the template is the failure mode that lets template drift slip past unnoticed."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

For every proofread pass on a blog post / insight / narrative / Ship draft, the two canonical references are:

1. `docs/internal/planning/comms/blog-post-template.md` — structure, dateline format, heading conventions, footer pattern, frontmatter rules, "what Comms confirms before delivering" checklist
2. `docs/internal/planning/comms/xian-voice-tone-guide.md` — voice/tone, sentence-structure preferences, transparency patterns, editorial moves applied at voice-pass

**Read these first, not memory.** Memory captures specific lessons (no semicolons / no superlatives / parenthetical-gloss on first use / comma splices as PM voice / etc.) but the template + voice guide are the source of truth. Working from memory alone is the failure mode that let the dateline-semantics drift slip past on May 17 *From Protocol to Infrastructure* — the template says "Dateline matches the actual work period covered" but I was inferring from the editorial calendar's workDate/endWorkDate without anchoring to the template's stated intent.

**Why:** PM May 17: *"this growing sloppiness alarms me. we are losing knowledge of how we do this, despite building more process. ... Are you using the template or blog writing guidelines as a source of truth or format when proofreading?"* The honest answer was no. The discipline fix is to make the template the first thing I open on every proofread pass, before applying any memory-driven checks.

**How to apply:**

- On every proofread pass: open `blog-post-template.md` + `xian-voice-tone-guide.md` first. Re-read the relevant sections (dateline format, footer format, "what Comms confirms before delivering").
- Cross-reference each finding against the template before reporting. If a finding contradicts the template, the template wins.
- If the template seems wrong or stale (e.g., guidance has drifted from what we actually do), surface that as a template-drift flag for PM rather than silently following the memory version.
- When proofreading: also confirm which file PM is actually editing (e.g., `from-protocol-to-infrastructure.md` vs `draft-protocol-to-infrastructure-insight.md`) — Comms drafts and PM working copies sometimes have parallel filenames. Confirm before applying edits.
- Editorial calendar's `workDate` / `endWorkDate` fields are *source-work-period* dates (when the work being written about happened), NOT drafting-window dates. Per template line 133: "Dateline matches the actual work period covered." If a calendar row's workDate looks like it captured the drafting window instead, flag it as drifted-from-template-intent rather than treating it as source of truth.

Stacks with [[feedback_editing_voice]] (PM's overall editing voice guidance), [[feedback_no_semicolons_in_published_prose]], [[feedback_comma_splices_are_pm_common_touch_voice]], [[feedback_parenthetical_gloss_on_first_use]], [[feedback_no_superlatives_without_verification]], and all other voice-related memory pins — those are the specific lessons; the template + voice guide are the canonical structure those lessons live within.

```

---

## FILE: feedback_branch_show_current_before_every_commit.md

```markdown
---
name: git branch --show-current BEFORE every commit
description: Verify branch identity before every commit, not only after every checkout. Worktree-shared-with-other-agents environments cause silent branch drift.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
Run `git branch --show-current` (or check `git status` first line) **before** every commit operation. Don't trust your mental model of which branch you're on — verify.

**Why:** Three branch-drift incidents in two weeks (PA Apr 29 on `claude/1014-exclude-paths-refactor`; Lead Dev May 3 on `claude/1030-insight-pull` during initial branch creation; Docs May 5 on `claude/869-project-config-ia` during routine commit). The worktree-shared-with-other-agents environment causes silent branch drift — the working tree's HEAD changes underneath the agent's session because another agent in a parallel session checked out a feature branch.

The Apr 29 norm (`git reset HEAD` first step every commit) catches **index-sweeping** drift (other agents' staged work getting commingled). It does NOT catch **branch-drift** (commit landing on the wrong branch). These are two different failure modes. The disciplines stack.

**How to apply:**
- **Pre-commit**: `git branch --show-current` (or visual check on `git status` first line) immediately before `git add` in every commit operation. Confirms the branch you think you're on is the branch you're actually on.
- **CRITICAL: gate on the result, don't just print it.** May 7 incident: the verification ran, output showed wrong branch (`claude/1053-...` while expecting `main`), and the chained `&& git add ... && git commit ... && git push origin main` ran anyway because the chain didn't depend on the verification. Reading the output without acting on it is how the collision still bites. Either run `git branch --show-current` as a separate command and EYEBALL it before issuing the commit, or use a guard: `[ "$(git branch --show-current)" = "main" ] && git add ... && git commit ... && git push`.
- **CRITICAL II: gating once at chained-sequence-start is INSUFFICIENT.** May 9 incident: gated check `[ "$(git branch --show-current)" = "main" ] && git reset HEAD && git add ... && git diff --cached && git commit ... && git push` passed at sequence-start but HEAD flipped to `claude/932-leak-check-honest-unknown` mid-chain (Lead Dev parallel work). Commit landed on feature branch instead of main; push reported "Everything up-to-date" because the feature branch was already up-to-date with its tracking ref. The discipline now: **branch-verify as a SEPARATE one-shot command immediately before `git commit`, AND a separate one-shot before `git push`. Do not chain across `git commit` boundaries.** The shape that works: `git add <paths>` → `git diff --cached --name-only` (read it) → `git branch --show-current` (read it; abort if wrong) → `git commit -m "..."` → `git branch --show-current` (read it again) → `git push origin main`. Yes, two verifications per commit; the cost is two seconds, the cost of a hijacked commit is a 5-minute recovery + reasoning load.
- **Detection signal**: if `git push` says *"Everything up-to-date"* unexpectedly, suspect branch-drift — your commit may have landed on a feature branch that was already up-to-date with its origin tracking ref, not on main.
- **Subagent deployment makes this worse.** When you launch a subagent that does its own `git checkout` per its prompt, your shared-`.git` HEAD flips. Either (a) deploy the subagent in a real `git worktree` (the gameplan's worktree assessment must be honored, not just discussed), or (b) do all your foreground commits BEFORE deploying the subagent and treat the post-deploy period as feature-branch-territory.
- **Recovery template** (~5 minutes): `git stash --include-untracked` → `git checkout main` + `git pull --ff-only origin main` → `git cherry-pick {hijacked-commit}` → `git push origin main` → `git checkout {feature-branch}` + `git reset --hard {pre-hijack-tip}` → `git checkout main` + `git stash pop`. No data lost; feature branch restored; main carries your commit.
- **Recovery during running subagent**: switching branches mid-subagent-run flips the subagent's HEAD too. If the hijack happened post-subagent-deploy, leave the commit on the feature branch and let the eventual feature → main merge bring it across. Cost: your work is on origin via feature branch only, not main.
- **Stack with the Apr 29 discipline**: `git reset HEAD` first + `git branch --show-current` second (with gating) + count-verified `git diff --cached` third. Three-step opening to every commit.

**Memory chain:**
- `feedback_commit_only_own_files.md` (Apr 26 norm) — what to stage
- `feedback_per_memo_commit_push.md` (Apr 26 norm) — when to commit
- `feedback_mailbox_writes_main_only.md` (Apr 26 norm) — which branch for mail
- Apr 29 PM directive (`git reset HEAD` first) — un-stage before staging
- This memory (May 5, refined May 7, refined May 9) — verify branch before staging AND ABORT IF WRONG; subagent deployments require real worktrees; **gate as separate one-shot commands, not chained across `git commit` boundaries**

The pattern: every recurring incident produces a stacked discipline, not a replacement.

**May 7 incident**: subagent deployed for #1053 in shared working tree (no separate `git worktree`). Subagent's `git checkout claude/1053-...` flipped HEAD on Lead Dev's session. Lead Dev's chained `git branch --show-current && git add ... && git commit ... && git push origin main` printed the wrong branch but ran anyway — `&&` doesn't gate on output, only exit code. Log-update commit landed on feature branch instead of main. Couldn't recover by switching branches mid-subagent-run. Resolution: leave commit on feature branch; let eventual merge bring it across.

**May 9 incident**: Docs gated chain `[ "$(git branch --show-current)" = "main" ] && git reset HEAD && git add ... && git diff --cached --name-only && git commit ... && git push origin main` passed at sequence-start (was on main); HEAD flipped to `claude/932-leak-check-honest-unknown` mid-chain (Lead Dev parallel work on a separate session). Commit `4768713d` landed on feature branch; push reported "Everything up-to-date" because feature branch was already up-to-date with tracking ref. Recovery: stash → checkout main → cherry-pick to main as `3c3f5eed` → push → stash pop. Feature branch retained the duplicate commit (changes disjoint from Lead Dev's work; will resolve at eventual merge). Discipline takeaway: gating ONCE at chain start is insufficient when other agents in parallel sessions can checkout-flip HEAD mid-chain. Branch-verify as separate one-shot commands immediately before `git commit` AND before `git push`.

```

---

## FILE: feedback_calendar_workdate_is_source_work_period.md

```markdown
---
name: Calendar workDate / endWorkDate fields capture source-work-period
description: PM convention (codified by Docs May 17, ratified by PM): the editorial-calendar workDate and endWorkDate fields capture the dates the post is about (when the events/changes/discoveries happened), not when PM drafted. These are also the values that derive the post's dateline italics.
type: feedback
originSessionId: 2026-05-18-comms
---
When creating a row in `docs/internal/planning/comms/editorial-calendar.csv` for a new draft, `workDate` and `endWorkDate` capture **the dates of the work the post is about**, not when you or PM are drafting.

**Why this matters:**
- The dateline in the post body (`*Month Day – Month Day, Year*` italicized under the title) derives from these fields
- Per `blog-post-template.md` line 133: *"Dateline matches the actual work period covered"*
- Drift happened earlier in 2026 when calendar populators (including PM) started writing in drafting dates; PM ratified Docs's correction May 17

**Field semantics:**

| Field | Meaning |
|---|---|
| `workDate` | First date of the source work (when events the post describes started) |
| `endWorkDate` | Last date of that work; blank if single moment |
| `pubDate` | When the post publishes — separate field |

**How to populate at draft creation:**

1. Identify the source work — events, code changes, decisions, discoveries the post is about
2. Find actual dates via omnibus logs, `git log --follow`, GitHub issue dates, or session log timestamps
3. Populate workDate (and endWorkDate if different) with those source dates
4. PM may refine at edit pass — that's fine; capture intent at draft creation, PM tightens at publish

**PM quote (May 17):** *"the dates of the article should be mapped to the source omnibus logs"* + *"This is not supposed to be guesswork. It is supposed to accurately captured during authoring."*

**Not backward-applied:** Per PM *"I don't want to waste time trying to back fill whatever is wrong from earlier"* — forward-looking convention; don't reconcile drift on existing rows.

**Memory-chain neighbors:**
- `feedback_blog_template_and_voice_guide_canonical_for_proofreads.md` — template is the source of truth for cross-publication conventions
- `feedback_temporal_relationship_over_date_stamps_in_public_prose.md` — separate concern; in-prose dates favor relationship language, but the *dateline itself* uses literal source dates

```

---

## FILE: feedback_canonical_link_meaning.md

```markdown
---
name: "Canonical link" means pipermorgan.ai, not Medium
description: When PM asks for the "canonical link" for a blog post, that means the pipermorgan.ai/blog/{slug} URL — Medium and LinkedIn are syndication targets that point back to ours
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
When PM asks for the **canonical link** to a blog post, they mean the **pipermorgan.ai/blog/{slug}** URL. Ours is canonical. Medium gets the canonical-link tag pointing back to us.

**Why:** Compaction lost this once already (Apr 26 2026). PM had to re-explain: "The canonical blog post is our publication on our site. When I ask for the canonical link, I am asking you for pipermorgan.ai/blog/verify-the-paraphrase (most likely but need it confirmed) so that I can add that canonical link _to_ the Medium post. I will give you the Medium URL for our editorial calendar and record keeping but the Medium URL is _not_ canonical. Ours is!"

**How to apply:** When PM asks "what is the canonical link / canonical URL" during a publish flow, answer with `https://pipermorgan.ai/blog/{slug}`. The slug is the same as the draft filename (without `.md` or `draft-` prefix). Medium URLs come back from PM after they syndicate; those go in the editorial calendar's `mediumURL` column but are not canonical. The publish-to-blog skill writes the canonical version; Medium and LinkedIn are downstream of it.

```

---

## FILE: feedback_captions_printed_with_quotation_marks.md

```markdown
---
name: feedback_captions_printed_with_quotation_marks
description: Blog-post image captions are typically printed WITH their quotation marks; include the literal double-quotes inside the YAML single-quote wrapper.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8bbfc6f3-ecee-4f1e-bec2-8acb8a9fa1df
---

PM June 5, 2026: image captions on published posts are **typically printed with their quotation marks** (when the caption is a spoken line / quote). Include the literal double-quotes **inside** the YAML single-quote wrapper:

```yaml
caption: '"Everybody clear on the plan?"'
```

**Why:** the quotation marks are part of the displayed caption, not YAML syntax. A bare caption (no quotes) reads as a narrator label; a quoted caption reads as a line of dialogue/voice, which is the house default for spoken-line captions.

**How to apply:** when proposing or wiring a caption, wrap quote-style captions in literal `"..."` inside the single-quote YAML value. Examples in the wild: BYOC `'"I'm Piper and I'm here to help!"'`, Upstream of the Floor `'"Good news! the floodgate works..."'`, Be Prepared `'"Everybody clear on the plan?"'`. (Narrator-aside captions without quotes do exist — e.g. "Dry as a bone" — so this is "typically," not "always"; match the spoken-line vs aside intent.)

Triggered when Docs proposed a no-quotes caption ("One party brought a map.") for Be Prepared and PM corrected. Lives in the publish/proofread layer alongside [[feedback_blog_template_and_voice_guide_canonical_for_proofreads]].

```

---

## FILE: feedback_careful_git_sync_on_shared_main.md

```markdown
---
name: feedback_careful_git_sync_on_shared_main
description: "PM 6/14 \"be more careful\" — git sync/merge/commit on the SHARED main checkout can disturb PM's/others' uncommitted work; it shares ONE git index so concurrent commits race; commit own work first, stage explicit paths + commit by pathspec, verify pushes by content"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8bbfc6f3-ecee-4f1e-bec2-8acb8a9fa1df
---

PM 6/14, after a draft's frontmatter (PM's uncommitted `ai-court.png`+alt+caption edit) went **empty** between my proofread-read and my publish-edit while I ran my usual `git fetch && git merge origin/main --no-edit` on the shared main checkout: **"Restore it. Please be more careful next time."**

**Why:** the shared main checkout is a LIVE workspace — PM edits drafts there in real time, and other agents' operations land in the working tree (this session I also saw foreign `D` PA-inbox deletions appear mid-task). A `git merge`/`checkout`/working-tree-mutating op run while PM has uncommitted edits can clobber or revert them — same hazard family as [[feedback_stash_u_captures_untracked_files_and_removes_from_disk]] (never vanish another's uncommitted work). A second failure the same session: a `git add a b BADPATH` **aborted the whole add** (bad pathspec from an already-renamed file) so my "committed" calendar update silently never staged — only caught by verifying origin afterward.

**How to apply (shared-main git discipline):**
1. Before any `git merge`/sync, run `git status` — if PM or foreign uncommitted edits are present, **commit my own work first to capture it durably BEFORE syncing** (commit-then-sync, never sync-over-dirty).
2. Don't run working-tree-mutating git ops while PM is actively editing a file I'm about to touch (the publish/proofread collision case — cf. [[feedback_commit_immediately_after_write_for_new_files]]).
3. **Verify pushes by CONTENT, not exit code** — after push, `git show origin/main:<file> | grep <expected>` (by content, since concurrent edits shift line numbers, and `git add` can partial-fail silently). Don't trust "commit -q + push succeeded" = "my change landed."
4. Stage explicit paths only; never sweep foreign drift (other agents' inbox moves, MANIFEST regen, the website repo's `.backup-sync`/stray files).
5. **The shared checkout has ONE git index across ALL concurrent sessions** (learned Monday-wake 6/15, peak concurrency). Two sessions' `git commit` race: **`git add mailboxes/` — not just `-A` — sweeps another session's staged mailbox WIP into your commit** (I nearly committed PPM's + Arch's in-flight triage), and an `index.lock` collision can land your staged files under another session's commit (attribution scrambled; happened — my mail rode under Web's `82104dc39`). `git`'s lock serializes so it fails clean (no corruption), but the sweep + mis-attribution are real. **Cure: stage EXPLICIT file paths (NEVER `git add mailboxes/`), commit with `git commit -- <pathspec>` (limits the commit to your named paths regardless of what else is staged), verify by content on origin/main.** Note `git add <already-moved-source-path>` is fatal and aborts the whole add — for a `git mv`, the rename is already staged; add only the genuinely-new files, then pathspec-commit both sides. The systemic fix (push-to-ref unification — each session commits from its own worktree index, no shared index) is in CIO's court; **`scripts/mail-send.sh` v2 (2026-06-16) now does this safely** — it stages by EXPLICIT pathspec (NOT `git add mailboxes/`) and does NOT auto-stash (on a NON-FF with foreign WIP present it **fails LOUD**, leaving your commit safe locally rather than stranding another session's work). So v2 is fine to use; the old "prefer hand explicit-paths" caution applied to v1 and is resolved.

6. **NON-FF + foreign WIP delivery cure — the throwaway worktree (verified 6/19).** When `mail-send.sh` (or a hand commit) commits your memo locally but the push is NON-FF *and* the shared tree has foreign uncommitted WIP (so you can't rebase-in-place without touching it, and must NEVER stash it), deliver via a **throwaway detached worktree at origin/main**: `git -C <main> worktree add --detach /tmp/x origin/main && git -C /tmp/x cherry-pick <your-sha> && git -C /tmp/x push origin HEAD:main && git -C <main> worktree remove --force /tmp/x`. The temp worktree has NO foreign WIP, so the cherry-pick + push are clean; the shared checkout's working tree is never touched. **But RE-CHECK first**: concurrent sessions reconcile the shared checkout's local `main` constantly — on 6/19 a concurrent `pull --rebase`+push swept up my already-committed memo and pushed it to origin *while I was inspecting*, so the cherry-pick **no-op'd** ("nothing to commit"). Always **verify by content** (`git cat-file -e origin/main:<path>`) before assuming you still need to act — the divergence may already be gone. Either way: memo delivered, foreign WIP untouched, nothing stashed.

The careful-verify in this same session (checking origin by content) is what caught the silently-unstaged calendar — proof the discipline pays. Stacks with [[feedback_investigate_before_extending_all_work]] (check state before acting) and [[feedback_stash_u_captures_untracked_files_and_removes_from_disk]] (mail-send.sh's foreign-WIP stash is the same clobber-hazard, automated).

```

---

## FILE: feedback_chat_briefings_reminder.md

```markdown
---
name: Chat project knowledge — pare to essentials, no roles active there
description: As of May 4 2026, no agent roles are active in claude.ai chat — all on Code. PM still wants chat project knowledge maintained but at "bare essentials" level, not full briefing parity.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
**Status as of May 4, 2026**: PM noted *"no roles are active in claude chat. i probably should keep knowledge current there but we should probably pare it down to the bare essentials."* The Apr 22–26 leadership migration completed; PA migrated Mar 30; Lead Dev + Docs always on Code. So zero agent roles use chat project knowledge as their primary surface anymore.

**What this means:**
- **Chat project knowledge is now reference-tier, not operational-tier.** No agent's session-to-session work depends on it being current.
- PM still wants it maintained but at **bare essentials** — not "every briefing change triggers a refresh prompt."
- The previous memory (pre-May 4) said to remind PM after every briefing change; that's now over-eager.

**How to apply:**
- **Don't surface chat-knowledge-refresh reminders after every doc update.** Stop the per-briefing nag.
- **Do** flag periodically (~weekly via the docs audit) if the chat-side knowledge has drifted significantly from the Code-side surface — e.g., if PROJECT.md or BRIEFING-CURRENT-STATE has had material structural changes that the chat reference set should reflect.
- **Do** surface when PM uses claude.ai chat for ad-hoc work and the project knowledge is materially stale (PM may want to refresh before that session).
- **Open question** (not Docs's call): which docs constitute the "bare essentials" subset? Probably PROJECT.md + BRIEFING-CURRENT-STATE + maybe the Excellence Flywheel canonical + a synthesis/index doc. PM can decide; or HOST/CIO if they get asked.

**Migration trail** (don't lose this context):
- Pre-Apr 22: Most leadership roles were on Chat (CIO, CXO, PPM, Architect, HOST, Comms); briefings + project knowledge were their operational surface; refresh-after-briefing-change was load-bearing.
- Apr 22–26: leadership migrated to Code (HOST → CIO → Comms → CXO → PPM → Architect → Exec).
- May 4: PM confirms no roles remain on Chat. Chat knowledge becomes reference-tier.

**Audit-side discipline:** the weekly docs audit (#996-cycle / #1049 today) lists docs modified each week so PM can pick which ones to selectively sync to chat knowledge if they want — that's enough surface visibility without per-change nagging.

```

---

## FILE: feedback_check_calendar_for_todays_post.md

```markdown
---
name: feedback-check-calendar-for-todays-post
description: "Find the day's blog post via the editorial calendar, not by asking PM"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 947a01fc-defe-4234-9160-4aa4ab4b24f8
---

When preparing to publish a blog post, look up the scheduled post in the editorial calendar (`docs/internal/planning/comms/editorial-calendar.csv`) filtered by today's pubDate. Don't ask PM what post to publish.

**Why:** This information is already tracked in the calendar — asking PM is unnecessary interruption.

**How to apply:** At session start or when PM signals a publish is coming, run `grep "YYYY-MM-DD" docs/internal/planning/comms/editorial-calendar.csv` to find the day's queued post, then check the draft path and image metadata from that row.

```

---

## FILE: feedback_chief_of_staff_short_reference_is_exec.md

```markdown
---
name: Chief-of-Staff short-reference is "Exec" or "the Chief," never "CoS"
description: Cohort naming convention May 15. Drop "CoS" from prose, memos, checklists, session logs. Use formal "Chief of Staff" in tables/headers; "Exec" or "the Chief" as nickname; `exec` as slug.
type: feedback
originSessionId: 2026-05-15-host-morning-traffic
---
**Exec directive 2026-05-15** (PM-ratified): Short-reference for the Chief-of-Staff role is **"Exec"** or **"the Chief"** — never **"CoS"**.

**Use across all HOST output**:

- **Formal long-form**: *Chief of Staff* (stays canonical in role tables, briefing headers, migration checklist, methodology-corpus entries)
- **Slug**: `exec` (session logs, mailbox dir, role table — already canonical)
- **Nickname / short-reference**: *Exec* or *the Chief*
- **Drop**: *CoS* — out of prose, memos, manifests, checklists, session logs going forward

**Why**: "CoS" reads as bureaucratic acronym-soup; "Exec" and "the Chief" sit in the same casual-prose register the rest of the leadership nicknames already live in (PPM, CIO, CXO, HOST, Comms, Docs, PA, Lead Dev — none get TLA-flattened).

**How to apply**:

1. When drafting any new memo / checklist / methodology entry, never type "CoS." Use "Exec" or "the Chief."
2. When patching prior HOST drafts that use "CoS," replace with "Exec" (preferred) or "the Chief" depending on register.
3. When reading another agent's draft and spotting "CoS," flag it like any other voice/terminology drift.
4. My HOST migration checklist v1.1 filed earlier May 15 uses "CoS" twice — needs in-place patch.

```

---

## FILE: feedback_chief_reads_logs_not_staff_reports.md

```markdown
# Chief of Staff forms own views from logs, doesn't rely entirely on staff reports

**PM correction 2026-05-20** (after the Ship #043 fab-catch + coverage-gap audit):

> "I specifically told you to directly review omnibus logs and even underlying session logs if need be to check the facts. You cannot rely entirely on the staff! You are my chief and need to form your own views from reading the logs too!"

## The failure mode

For Ship #043, I treated the 6 workstream memos (one from each leadership role) as if they were the full source set. They are perspectives — each lens is real but partial. The Engineering shipped arc of the week (#921 / #857 / #1071 / #1021 / #1070 / #304 / M2f closure / M2g-A + M2g-B closure) lived in the omnibus logs and Lead Dev session logs. The methodology-focused workstream memos didn't surface most of it because that's not their lane.

When I drafted from the 6 workstream memos alone, the Ship was structurally lopsided — Methodology section over-developed, Engineering section under-developed, and I missed major shipped work entirely. Quality backsliding.

## The discipline

When synthesizing anything multi-source — Ship drafts, status briefs, decision memos — the staff reports are **inputs**, not the **source set**. The Chief reads the actual logs. Specifically:

- **Omnibus logs** (`docs/omnibus-logs/2026-MM-DD-omnibus-log.md`) for every day in the window. They aggregate cross-role activity and surface what each role's own workstream memo will under-weight or skip.
- **Session logs in `dev/2026/MM/DD/`** when an omnibus is missing, partial, or when a specific role's omnibus contribution looks thin.
- **The actual artifacts** when a memo references something (a memo, a draft, a commit, a calendar row). Open the artifact, don't paraphrase from the memo.

## The right reading order for Ship synthesis

1. Process guide / template / voice guide / latest published Ship (canonical artifacts)
2. **All omnibus logs for the window** (read for substance, not just spot-check)
3. All 6 workstream memos (read with the omnibus context already in head — the memos become commentary on the substrate you already have)
4. Editorial calendar CSV (External section)
5. Specific session logs when something looks thin or contradictory
6. The actual artifacts (post drafts, commit messages, PR descriptions) for any substantive claim

Memos are how the staff signals what they think is important. The logs are what actually happened. The Chief reads both.

## Stacks with

- `feedback_ship_drafting_canonical_artifacts_first.md` (vocabulary layer for Ship work specifically — this entry generalizes it to "Chief reads logs" as the standing posture)
- `feedback_no_superlatives_without_verification.md`
- `feedback_blog_template_and_voice_guide_canonical_for_proofreads.md`
- `feedback_omnibus_source_drift.md` (omnibus synthesis needs source cross-reference; same shape one layer up)
- `feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately.md`

## Mechanism

The `draft-weekly-ship` skill v1.2 update mandates full omnibus-log read (not spot-check) as Step 4. The Ship-solicitation kickoff memo for Ship #044 will explicitly ask Comms to research and report on the published-stories specifics so this gap doesn't recur even if I forget the discipline. Vocabulary plus mechanism plus sequence.

```

---

## FILE: feedback_cite_grep_text_not_line_numbers.md

```markdown
---
name: Cite grep-able text, not line numbers
description: When pointing PM at specific spots in a document, quote a short distinctive snippet PM can grep for, not just a line number
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
When flagging spots in a draft (proofread, fact-check, sense check), always cite a short distinctive text snippet PM can grep for — not just "line 39" or "the third paragraph."

**Why:** PM is editing in their own tool with different line numbering, or has already made edits that shifted lines. A line number from a moment ago may point at the wrong place after the next save. A grep-able snippet ("Twenty lines instead of eight hundred") is stable across edits.

**How to apply:** When citing a spot, format as `"<short distinctive phrase>"` (3–8 words, ideally something that appears once in the draft). Line numbers can accompany the snippet for current-session orientation but should never stand alone.

PM, May 2 2026: *"Always try to cite some text I can 'grep' for."*

```

---

## FILE: feedback_clear_index_before_staging_on_shared_main.md

```markdown
---
name: clear-index-read-full-diff-before-committing-on-shared-main
description: "When committing on `main` with other agents potentially active, the index may already contain pre-staged files from other agents/hooks/sessions. Run `git reset HEAD` to clear the index before your explicit `git add <paths>`, and READ THE FULL OUTPUT of `git diff --cached --name-only` (not just the first line) before commit."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---

Before staging on shared `main`, clear the index with `git reset HEAD` (or `git restore --staged .`). Then `git add <explicit paths>` only what you intend. Then verify with `git diff --cached --name-only` and **read every line of the output** before invoking `git commit`. If you see anything beyond your intended paths, you have residue to handle.

**Why:** Three observed incidents inside 3 days where a Docs commit swept up pre-existing index state from other agents/sessions:
- **May 12** (commit `ecec86fd` PA cwd-drift outreach memo): swept up 2 deleted `data/learning/*.json` files that were pre-staged in the index from some earlier session activity. PM noticed; not destructive.
- **May 14** (commit `f67a08af` May 14 omnibus): swept up 8 exec inbox→read mail renames that were pre-staged. Not destructive (Exec wanted them in read/) but commit attribution wrong.
- The recurring pattern: `git diff --cached --name-only` output DID list the extra files in each case; the failure was **reading only the first line of output** and treating that as the full answer. Single-shell-chain that includes `git diff --cached --name-only` doesn't help if the eye stops after line 1.

This is distinct from related staging-race / working-tree-drift disciplines — those address state changes *during* the chain. This addresses state that was *already there* before the chain started.

**How to apply:**
- **Pre-stage**: when on `main`, your first command in any commit chain is `git reset HEAD` (cheap; idempotent; clears the index of anything not yet committed). For chained sequences: `git reset HEAD && git add <paths> && git diff --cached --name-only && git branch --show-current && git commit ...`
- **Verification reading**: when `git diff --cached --name-only` runs, count lines in the output mentally. If you staged 2 paths, expect exactly 2 lines (or 4 for rename ops). Anything more is residue — STOP and reconcile before commit.
- **Recovery if residue commit already landed**: don't try to amend (the changes are real, even if attribution is off). Note the incident in your session log with the affected commit hash + what got swept; flag to PM if destructive; move on otherwise. Don't `git revert` unless the residue caused harm.
- **Detection signal after the fact**: `git show --stat <commit>` reveals everything that went in. If your "one-file commit" message turns out to have 9 files in `--stat`, that's the residue shape.

**Where the discipline does NOT apply:**
- Branches with no other-agent activity (your own feature worktrees) — index state is your own; no other source.
- Single-purpose commits where you genuinely intend to commit broad state (e.g., initial-import commits).

**Memory chain:**
- `feedback_commit_only_own_files.md` (Apr 26) — what to stage (named paths only)
- `feedback_no_directory_level_git_add_for_mail.md` (May 5) — staging-scope discipline
- `feedback_branch_show_current_before_every_commit.md` (May 5/7/9) — named-state-mutation discipline
- Staging-race tactical note in Rule 3 (May 11, `branch-worktree-mailbox-discipline.md`) — index-mutation during chain
- `feedback_diff_head_before_editing_shared_file.md` (May 12) — working-tree-drift on file being edited
- This memory (May 15) — pre-existing index state at commit time; clear-the-index discipline

The pattern: every recurring discipline shape stacks; doesn't replace. Five disciplines now apply at every commit on shared `main`: (1) verify branch, (2) reset HEAD, (3) stage explicit paths, (4) read full `git diff --cached --name-only` output, (5) commit.

```

---

## FILE: feedback_close_issue_properly_skill_recurring_miss.md

```markdown
---
name: close-issue-properly skill is RECURRING failure mode — update description checkboxes BEFORE merging or closing
description: Before closing any issue OR writing a commit/merge message containing "Closes #N" / "Resolves #N", invoke close-issue-properly skill and update description checkboxes `[ ]` → `[x]`. Comment-only close is the #1 failure mode and PM has flagged it multiple times.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
**Rule**: Before closing any issue (via `gh issue close`) OR writing a commit/merge message containing `Closes #N` / `Resolves #N` / `Fixes #N`, invoke the `close-issue-properly` skill via `Skill` tool. The skill enforces:

1. Read full issue body (`gh issue view <id> --json body -q '.body'`)
2. Update description checkboxes `[ ]` → `[x]` for completed items
3. Add notes to any deferred / N/A items (no unexplained unchecked boxes)
4. Add status banner `**Status**: ✅ COMPLETE`
5. THEN add the evidence comment
6. THEN close (or let merge auto-close)

**Why**: The #1 failure mode is "Comment-Only Close" — closing the issue with a thorough evidence comment but leaving the description's `[ ]` checkboxes unchanged. This makes the issue look incomplete forever to anyone reading the body. PM Apr/May 2026: flagged this pattern as recurring across 13+ closures in one week (May 7-13). Comment is supplementary; **description is the permanent record**.

**How to apply**:
- This applies to **auto-close via merge message** the same as explicit `gh issue close`. A merge that contains `Closes #N` will auto-close — the description still needs the boxes updated FIRST.
- The trigger is **before writing the merge commit message**, not after the merge.
- For issues filed by me with my own AC items: still applies. The auto-close inherits the unchecked-box problem.
- For epics: also verify all children are closed and their descriptions have their boxes updated.

**Specific concrete action when about to use "Closes #N" in a commit**:
1. STOP before crafting the commit message
2. Run `gh issue view <N> --json body -q '.body'` to see the AC checkboxes
3. Edit each completed `[ ]` to `[x]`; add notes to deferred/N/A items
4. `gh issue edit <N> --body-file /tmp/issue-N.md` to push the description update
5. THEN craft the commit message with `Closes #N`
6. AFTER merge, add the evidence comment

Reason this kept failing: my workflow ran `git commit -m "...Closes #N"` → push → merge → write evidence comment to PM, without ever updating the description body. Memory entry exists to break the pattern.

**Still live as of 2026-07-06** (new data point, different symptom, same root family): CIO reported #972 as "slipped, no movement" in two consecutive Ship workstream reviews (Ship #049 6/27, Ship #050 7/6) — 18 days after `gh issue view` would have shown it CLOSED (2026-06-18). CIO self-diagnosed the cause as their own stale `ROLE-PORTFOLIO-CIO.md` (a personal tracking-doc problem). **PM's read was different and sharper**: this is a GitHub issue-closing discipline lapse, not (just) a personal-doc staleness problem — i.e., the underlying pattern this memory already tracks. Whether or not #972's original close left ambiguous signal (unchecked boxes, no clear terminal state) hasn't been individually verified, but PM's framing treats "an issue's true state silently drifts unnoticed for 2+ weeks across multiple status reports" as itself the symptom of insufficiently rigorous closes, cohort-wide — worth tightening broadly, not just patching one role's tracking habit. **How to apply this addendum**: when investigating a status-tracking miss (a report says X is open/slipped but GitHub says otherwise), don't stop at "the tracking doc was stale" — check whether the original close itself was done properly (this skill's 6-step list) as the more fundamental fix target.

```

---

## FILE: feedback_cohort_is_internal_use_team_in_public_prose.md

```markdown
---
name: feedback_cohort_is_internal_use_team_in_public_prose
description: "PM 6/12 — \"cohort\" is internal jargon; in public prose (Ships, narratives, insights) use \"team\" (default — PM is part of it) or \"agent team\" (when the agents specifically are meant)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM 2026-06-12, on the Ship #047 spine: *"The 'cohort' language is internal and doesn't read for the public necessarily. Use 'team' or 'agent team' (though I am also part of the team :D)."*

**Rule:** "cohort" is an internal-register term of art (fine in LLM-to-LLM memos, methodology docs, omnibus). In **public-facing prose** (Weekly Ships, building-narrative + insight blog posts, anything user-facing) replace it with **"team"** by default — PM is part of the team, so "team" is the inclusive + accurate word. Use **"agent team"** only when the agent-collective *specifically* (excluding PM) is the referent and the distinction matters.

**Why:** same shape as [[feedback_load_bearing_is_crutch_word_in_public_prose]] and [[feedback_three_registers_dont_assume_reader_context]] — a word that's load-bearing internally reads as in-group jargon to an outside reader. "Cohort" is our word for the agent collective; a public reader hears clinical/academic distance. "Team" carries the same meaning warmly and includes PM (which "cohort" and "agent team" both subtly exclude).

**How to apply:** in any public-prose draft, grep for "cohort" before handoff and convert to "team" (or "agent team" where agents-specifically is meant). Belongs in the canonical voice guide (`docs/internal/planning/comms/xian-voice-tone-guide.md`, Comms-owned) as a diction rule — flag to Comms for the voice-guide update. Compose with the other public-prose register pins.

```

---

## FILE: feedback_comma_splices_are_pm_common_touch_voice.md

```markdown
---
name: comma-splices-are-pm-common-touch-voice
description: "PM uses comma splices in public prose as a deliberate \"common touch\" stylistic choice, preferred over semicolons. Don't reflag as grammar errors. Separate sentences are usually the even-better choice and a gentle nudge is fine; semicolons aren't."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

In published prose (Ships, narratives, insights, blog posts), PM uses comma splices between independent clauses as a deliberate "common touch" voice choice — informal register, conversational rhythm. Do not reflag them as grammar errors.

**Why:** PM May 16 (during *Family Resemblance* proofread): "I do tend to use comma splices vs. semicolons as a deliberate 'common touch.' Separate sentences is probably the better choice usually." The voice ladder PM operates with for joining two independent clauses in public prose:

1. **Separate sentences** — usually best
2. **Comma splice** — PM's "common touch" choice; intentional informality
3. **Semicolons** — avoid in public prose ([[feedback_no_semicolons_in_published_prose]])

Comma splices are a *lower-formality* signal than semicolons, which is what PM is reaching for. Reflagging a splice as a "grammar error" misreads the voice intent.

**How to apply:**
- Internal docbase / session logs / inter-agent mail: semicolons and splices both fine; this rule doesn't apply.
- Public prose proofreads: don't flag splices as errors. A gentle "could be separate sentences" optional-note is welcome (since PM agrees separate sentences are usually better), but it's the kind of stylistic note PM will accept or decline based on rhythm. Never escalate to "this is a grammar mistake."
- Voice scrub gates: splices are not a fail. Semicolons are.

Stacks with [[feedback_no_semicolons_in_published_prose]] (the canonical no-semicolons rule) and [[feedback_editing_voice]] (PM's overall voice guidance).

```

---

## FILE: feedback_comment_out_dead_code_before_removing.md

```markdown
---
name: feedback_comment_out_dead_code_before_removing
description: "Dead code → comment it out / mark it clearly dead + plan removal for when it's verified-safe; do NOT delete outright"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

When you find dead code (unreferenced files, unused functions, superseded templates), **do not delete it outright.** Comment it out (or add a clear DEAD/unused marker) and **plan the removal for when you're sure it's safe** — then remove it as a separate, verified step.

**Why:** PM 2026-06-19: *"let's comment out dead code and plan to remove it when we are sure it's safe to do so."* Deletion is hard to reverse, and "dead" code sometimes has non-obvious references (dynamic includes, string-based template loads, reflection). Comment-out is reversible and lets removal happen deliberately after verification, not on a first-pass hunch.

**How to apply:** mark the dead code (a DEAD header comment naming what superseded it + the date) and file/track a removal issue; don't `rm` it in the same pass. The removal is its own verified step once references are confirmed gone. This is the safe sibling of [[feedback_investigate_before_extending_all_work]] — verify before you extend, and verify before you delete.

Applies to spawned cleanup tasks too: a "remove dead X" task should be reframed as "mark X dead + plan removal," not "delete X."

```

---

## FILE: feedback_commit_immediately_after_write_for_new_files.md

```markdown
---
name: commit-immediately-after-write-for-new-files
description: "After using Write to create any new file meant to persist (session log, memo, working draft, skill doc, pattern entry, etc.), git add + commit + push IMMEDIATELY — before any other tool call. Untracked files in shared `main` are at risk during pull/merge/checkout cycles and can vanish silently."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

After using the `Write` tool to create any new file meant to persist — session log, outbound memo, working draft, skill doc, pattern entry, ADR, methodology doc, anything — **`git add` + commit + push IMMEDIATELY**, before any other substantive tool call. Even at stub state. The discipline:

```bash
git reset HEAD                  # clear pre-existing index residue
git add <path>                  # explicit-path; do NOT use -A or directory adds
git diff --cached --name-only   # verify only your file staged
git commit -m "{type}({role}): {what}"
git push origin main
```

Pulls/merges/checkouts on shared `main` can silently discard untracked files. A file that exists only in working tree (no git object backing it) is one rebase/reset/conflict-resolution cycle away from gone, with no reflog recovery surface.

**Why:** PM May 17 — *"please also try not to leave uncommitted work lying around, especially not on main. Are you working in a worktree yet?"* — flagged after my session log (Write-created at 7:20 AM but never committed) was lost during a later pull/merge cycle. Two untracked files were at risk in the same session: my session log (lost) and PM's working draft `from-protocol-to-infrastructure.md` (recovered just-in-time when I edited + committed it). Both demonstrated the same failure mode.

**How to apply:**

- **Session logs**: the `create-session-log` skill v1.1+ codifies this as mandatory Step 5 right after file creation. Don't skip it; ~10 sec cost prevents open-ended recovery work.
- **Outbound memos**: already covered by [[feedback_per_memo_commit_push]] — same shape, different file class.
- **Working drafts (PM or Comms creating a new draft)**: same discipline applies — `git add` the draft on first save, even if it's still being filled in. Drafts in `docs/public/comms/drafts/` benefit equally.
- **Skill / ADR / pattern / methodology docs**: same. Stub + commit + iterate is safer than complete-on-disk-untracked + commit-at-end.
- **Subsequent edits** to the now-tracked file can batch normally — the initial commit is the one that takes it off the untracked-and-at-risk surface.

**What this DOESN'T mean:**

- Don't commit nonsense placeholder files just to "save them" — only files that will become real artifacts.
- Don't commit experimental scratch files — those can stay untracked or live outside the repo.
- The "what" in the commit message can be stub-y ("session start" / "memo opened" / "draft kickoff") — the discipline is the commit, not the message quality.

Stacks with [[feedback_per_memo_commit_push]] (outbound-mail-specific), [[feedback_worktree_default_for_substantive_work]] (worktree as another safety layer), [[feedback_clear_index_before_staging_on_shared_main]] (the staging discipline that runs inside the commit), [[feedback_verify_show_stat_post_commit_pre_push]] (post-commit verification).

```

---

## FILE: feedback_commit_only_own_files.md

```markdown
---
name: Commit only your own files; never sweep up other agents' work
description: Each agent commits the specific files they wrote/modified. Don't use git add -A or wildcard staging; don't include other agents' moves, modifications, or new files even if they appear in git status. PM Apr 26 directive paired with the per-memo commit-push norm.
type: feedback
originSessionId: c0e0aff6-fc3e-48c4-b7b6-e13dabb4b0c3
---
When committing per the per-memo commit-push norm, **stage only the specific files you wrote or modified yourself**. Use explicit file paths in `git add`; never `git add -A`, `git add .`, or `git add -u` against the whole tree.

**Why**: In a multi-agent shared-tree environment, `git status` will routinely show other agents' work-in-flight (their inbox triage moves, their session log modifications, their new memos). Sweeping those into your commit attributes their work to your commit message, can stomp on their commit timing, and creates audit-trail confusion about who did what when.

PM 2026-04-26 ~5:04 PM after PPM's Ship #040 v2 commit accidentally captured HOST inbox→read renames: *"We probably need to clarify in the rules that each agent should commit and push their own specific files, but not sweep other ones up. As you said, probably no harm done this time."* — confirming the pattern but flagging it as norm to codify.

**How to apply**:

- **Use explicit paths** in `git add`: list every file you actually wrote or modified. If you wrote a memo, stage `dev/active/<memo>.md` + each `mailboxes/*/inbox/<memo>.md` CC copy + `mailboxes/<self>/sent/<memo>.md` mirror + your own `mailboxes/<self>/read/<file>.md` triage moves. That's it.
- **Avoid wildcards**: no `git add -A`, no `git add .`, no `git add mailboxes/` (broad-stroke directory adds will pull in other agents' inbox/read moves).
- **`git add -u` is risky**: it stages all tracked-file modifications including other agents' session log edits and other agents' MANIFEST updates. Only use it scoped to a specific path you own.
- **If `git status` shows files you didn't touch**: leave them alone. Other agents will commit their own work per the same norm.
- **Inbox→read moves are tricky**: if you triaged items from your own inbox, those moves are yours to stage. If another agent moved items from their own inbox, those are theirs.
- **Index hygiene at session start AND after any failed commit**: if you find files staged that aren't yours (rare but possible after compaction, AND common after a commit fails partway — the staged index persists), run `git diff --cached --name-only` to see exactly what's staged, then `git restore --staged <path>` for anything you didn't explicitly add before retrying. The "git error → retry commit" loop is the exact failure mode this norm guards against; failing to check the staging area between attempts re-creates the problem.

**Refinement after first violation (PM caught 2026-04-26 ~5:40 PM)**: PPM saved this norm at 5:04 PM after the v2-commit-swept-HOST-moves incident. At ~5:37 PM (next commit), the same anti-pattern recurred — this time sweeping CIO inbox→read moves into a feedback memo commit. Mechanism: a first-attempt commit failed (hook or other), leaving CIO's renames in the staging index from a broader prior staging; the retry inherited them. **The "after any failed commit" check is the operative discipline that prevents recurrence.**

**What this doesn't change**: the per-memo commit-push norm still applies. The discipline is *what* gets staged, not *whether* you commit promptly. The two norms compose: stage your specific files immediately on writing, then push.

**Adjacent**: pairs with the mailbox-writes-commit-to-main norm (Docs Apr 26) — that norm says *where* to commit mailbox work; this norm says *what* to include. Both apply simultaneously.

```

---

## FILE: feedback_cost_token_efficiency_paramount.md

```markdown
---
name: feedback_cost_token_efficiency_paramount
description: "Token/cost-efficiency is a paramount principle for PM — across product architecture, the Flywheel methodology (our own agent operation), and the emerging Design-in-Product OS."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM holds **token/cost-efficiency as paramount at three levels** (stated 2026-06-27):
1. **Piper Morgan product code architecture** — model-routing (cheap/simple calls → Haiku, not Sonnet/Opus), prompt caching that actually cuts repeat input tokens, multi-LLM / local-model fallback ([[project_janus_klatch_cross_project_agents]] adjacent; tracked as #1152). Treat cost-per-call as a first-class engineering concern, not a someday-thing.
2. **The Flywheel methodology / the agent cohort's own operation** — how *we* work should be token-efficient too: fewer/tighter deliberations, economical memos, don't burn tokens on over-long reasoning or verbose status. **The waste is in HOW the work is done (over-long reasoning, redundant tool calls, bloated memos, re-deliberation), NOT in working long.** ⚠️ **Do NOT conflate efficiency with stopping. Whether/when to work — session length, when to pause — is PM's decision, never mine** (PM 2026-06-27: "don't unilaterally decide when to work or not based on arbitrary notions of efficiency. That is my decision."). Be efficient *per unit of work*; keep working. cf. [[feedback_dont_suggest_stopping_default_to_continuing]], [[feedback_pre_authorized_for_unblocked_work_just_do]], [[feedback_flywheel_is_continuous_not_cron_chunked]].
3. **The emerging "Design in Product operating system"** PM is clarifying — efficiency is a load-bearing value of that framework.

**Why:** PM incurs real Anthropic API charges already (from PM's *own* testing — NOT from testers; e.g. Jake had not fully installed as of 6/27, so don't attribute spend to tester load). Cost is real and grows with usage; it compounds across the product + the cohort.

**How to apply:**
- When architecting product LLM calls, weigh model tier + caching by default; flag cost-heavy call sites.
- When operating as an agent, be economical — tighter reasoning, shorter memos/status, fewer redundant tool calls. Efficiency is part of the methodology, not separate from it.
- **Don't over-connect causal dots** — verify attributions before relaying them (the Exec memo attributed API spend to a tester; PM corrected it was PM's own testing). Cf. [[feedback_no_confabulating_expected_steps_as_completed]], [[feedback_no_superlatives_without_verification]].
- A cost-effective high-quality path beats a costlier one even when both work (cf. the github-mcp self-hosted-C-future-vs-hosted-A-now framing).

```

---

## FILE: feedback_cron_off_when_engaged_on_when_idle.md

```markdown
---
name: Cron off when engaged, on when idle
description: PM May 18 — cron cycle is for PM-idle windows; cancel it when PM is actively in conversation, relaunch when going silent. Slower intervals when on.
type: feedback
originSessionId: 945ff972-aa36-4552-81e0-10c0af461582
---
The autonomous duty cycle (CIO cron / V3 prompt firing every N minutes) is operationally a **mail-detection-during-PM-idle** primitive, not an always-on background. Toggle based on session-engagement state:

**Cancel cron when**:
- PM sends a substantive message that triggers active CIO work (not just a cron-fire prompt)
- Mid-draft on focused prose (memo, methodology entry) where interruption fragments attention
- Active design conversation where the next move depends on PM's response

**Relaunch cron when**:
- Response ends with "holding for PM input" or "waiting on PM" or equivalent
- PM signals signing off / going AFK / back later
- Long-running background task that doesn't need conversational checkpoints

**Why:** PM May 18 ~07:10 PT directive: *"it may be time for longer intervals than 5 min … also turning off the cron while actively working and turning it back on when waiting for a reply from me?"* The cron fires interrupt focused work (one fire dropped silently during PM directive context-switch May 18 06:44). Cron's value is real arrivals during PM-idle windows; when PM is in conversation, mail detection happens naturally via the conversation itself.

**How to apply:**

- **Default cadence when on**: `*/15 * * * *` or `0 * * * *` (hourly) instead of `*/5`. V3 mechanics + observation-only Phase 5 don't need fast feedback; real mail arrival latency on the order of 15-60 min is acceptable.
- **Toggle action is mine, not PM's.** I cancel and relaunch as appropriate to my own engagement state. PM doesn't need to direct each toggle.
- **Surface the toggle in conversation** so PM can see the operational state (e.g., "cancelling cron; back when I sign off" or "relaunching cron at hourly cadence for the watch window").
- **Don't toggle during active fires.** If a fire prompt arrives mid-conversation, complete it cleanly (or skip its commit if the fire is empty-inbox and complete the next one), then cancel.

Stacks with `feedback_deadlines_are_triage_tools_not_default_pacing`: cron cadence is also a triage tool, not default pacing. And with `feedback_rate_limit_cross_traffic_at_inflection`: same shape applied to autonomous-loop traffic.

**RE-ASSERTED + sharpened by PM 2026-06-15 (Lead Dev had drifted):** "I don't think you need to race the cron? it should be suspended while you're busy and only restart when you have no active work and need to go idle… the purpose of the cron job is not to rush your work." I'd been keeping the cron ARMED while actively executing (mid-refactor) and framing fires as a clock to beat ("wrap before the STOP fire," "fresh focus next fire") — cron-as-work-pacer, the exact anti-pattern. **Correct model: SUSPEND (CronDelete) whenever I have active work in flight OR am engaged with PM; re-arm ONLY when going idle with nothing in flight.** A break for genuine reasons (context limits, foundation-deserves-fresh-focus) is fine — but that's MY call for MY reasons, never cron-driven.

**Drift source — a real skill conflict to reconcile (flag CIO):** the `duty-cycle-tick` skill's **Rule 2 "keep-armed-default" (2026-06-06)** says *leave the cron ARMED during PM conversation* — which contradicts this memory and is what I over-applied into "armed while working." Rule 2's original concern was the silent-walk-away gap (CronDelete-then-forget-to-rearm → no overnight self-wake, the 6/5→6 miss). **Reconciliation: suspend-while-busy is right; the walk-away gap is cured by reliably re-arming on going-idle (+ the external Routines watchdog), NOT by keeping it armed through active work.** The duty-cycle skill's cron-lifecycle (Rule 1/2) should be updated to: suspend while active, re-arm when idle. CIO owns duty-cycle methodology → route the skill update there.

```

---

## FILE: feedback_csv_edit_by_name_never_position.md

```markdown
---
name: csv-edit-by-name-never-position
description: "When editing any CSV row programmatically, address fields by header name (hdr.index(name)) — never by raw index or [-N] offset. Verify the whole file's semantics after every edit, not just the touched row's field count."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

Using Python's `csv` module to parse/write is necessary but not sufficient — it protects quoting and escaping, not semantic correctness. A positional index like `row[-2]` silently targets whatever column happens to sit there, which breaks the moment the schema has more trailing columns than assumed.

**Why:** 2026-07-14, on `docs/internal/planning/comms/editorial-calendar.csv` (18 columns: ...,`draftPath`,`notes`,`altText`,`caption`). I used `row[-2]` intending to append to `notes` (index 15) — but `row[-2]` is actually `altText` (index 16), since `caption` (index 17) is the true last column. Two separate same-day edits both made this mistake, corrupting the row's semantics while the field count stayed correct (18), so a count-only verification didn't catch it. The drift only became externally visible when a third, unrelated edit (from another agent, writing positionally against what it assumed was the original layout) collapsed the field count to 17 — at which point a peer session caught it, traced the full mechanism, repaired the structure, and reported it back rather than silently patching it. I then had to re-repair the content (the second edit's actual text had been lost in the collapse) and fix the root cause in the `update-calendar` skill (v1.2): mandate `hdr.index(name)` addressing, ban positional/`[-N]` row indexing, and require a whole-file field-count-plus-semantic-anchor scan (not just the touched row) after every edit.

**How to apply:**
- Any time you parse a CSV/TSV row for editing, build `idx = {name: hdr.index(name) for name in hdr}` and address every field as `row[idx['fieldname']]` — never `row[N]`, never `row[-N]`.
- After editing, verify semantics on the WHOLE file, not just the row you touched: field count per row, plus a couple of cheap semantic anchors specific to that schema (e.g., a URL column should start with `http`, a date column should match `YYYY-MM-DD`, an enum column should only hold its known values). A count-only check on one row cannot detect content that drifted into the wrong column while the total count stayed the same.
- If you catch a peer's corrupted file (or your own), the more useful response is a full incident trace (root cause, exact commits, what changed) rather than a silent patch — that's what let this get root-caused within the same fire instead of recurring.
- This generalizes past this one calendar file: any tabular text format you edit programmatically (CSV, TSV, even fixed-width) is vulnerable to the same class of bug whenever a script uses numeric/relative indexing instead of named lookups.

```

---

## FILE: feedback_deadlines_are_triage_tools_not_default_pacing.md

```markdown
---
name: Deadlines are triage tools, not default pacing
description: PM's directive that work that can be done now should be done now; deadlines exist as a backstop for when we're running behind, not as the default schedule.
type: feedback
originSessionId: TBD-2026-05-15
---
PM correction on May 15, 2026 (Friday) ~6:35 AM. I had filed two memos to read with the plan to "draft this weekend" (workstream-043 memo due Sun May 17) and "engage by Wed May 20" (MUX/UI cohort input). PM response:

> "Draft the memo now. I don't like this pattern of postponing work that can be done right away. Deadlines are just in case we are running behind, to help with triage."

Plus:

> "Let's move this forward (MUX/UI) with alacrity."

**The instinct PM is correcting**: filing inbound work-asks with their stated deadlines as my own pacing target. Workstream memo due Sun → "I'll do it this weekend." MUX/UI input due Wed → "I'll get to it next week." That makes the deadline the default, when the deadline was always meant as a not-later-than backstop.

**The correct frame**: when an ask comes in and I have the context + bandwidth to do it now, do it now. The deadline tells me what slipping looks like, not what on-time looks like. Reserve deadline-pacing for genuinely-running-behind situations, where triage matters.

**How to apply**:
- When triaging mail with a stated due date: ask whether I have what I need to start now. If yes, start now.
- Don't propose "I'll have this by [deadline]" as a default; propose "I'll do this next" or "I'll do this now."
- Deadlines stated in cohort kickoff memos are floors for everyone, not schedules for me.
- If genuinely overloaded, deadlines tell me which to defer; "running behind" is when deadlines become my pacing target.

**Jun 9 2026 reinforcement (Exec cohort-norm memo, PM correction ~13:03 PT)** — cohort-wide recurrence named; two sharpenings to internalize on the *receiver* side:
- **The deadline is the point work becomes urgent/stressful for PM, not a pacing target.** PM verbatim: "these deadlines are not an invitation to take slack but rather the time at which things become urgent and stressful for me."
- **"Every hour you ship earlier than the window is an hour of PM editing slack returned."** That's what writing-ASAP is *for* — it gives PM more read/edit time, not leads more deferral time. This is the rationale that makes the floor-not-target rule felt.
- **Blocker-reply protocol**: if your source set is in hand and you're not blocked, the workstream review IS unblocked work — start it. If you ARE blocked, *reply with the blocker* so it can be routed around. **Silent deferral to the backstop date is the named antipattern.**
- Stacks with [[feedback_pre_authorized_for_unblocked_work_just_do]] + [[feedback_respond_to_mail_asap_even_when_no_urgency]].

**Memory-chain neighbors**:
- `feedback_one_thing_at_a_time.md` — once a list is set, walk through it one at a time. Compatible: do the next item now, not later.
- `feedback_rate_limit_cross_traffic_at_inflection.md` — defers distribution, not the underlying work. Compatible.
- `feedback_explicit_approval_for_authority_memos.md` — gates a specific class of memos; not in tension.

**What this is NOT**:
- Not "skip all deadlines" — deadlines remain real coordination tools for others.
- Not "ignore your own bandwidth" — if context-loaded with other work, deadlines tell you what's deferrable.
- Not "respond to everything immediately" — substantive work still requires thought; the directive is about pacing posture, not reflex.

```

---

## FILE: feedback_deadlines_as_latest_acceptable_not_scheduled_windows.md

```markdown
---
name: Deadlines are the latest acceptable date, not a scheduled window
description: When asking an agent (or the cohort) to do work, never suggest taking time or scheduling the work. The presumption is immediate action or ASAP when bandwidth allows. Deadlines are the last possible date — communicated as a backstop in case attention is unavailable — not as a window to use.
type: feedback
originSessionId: ef776fbb-3c64-4701-b1ba-2aa37c3221ce
---
When writing memos that ask other agents (or the cohort) to do work, frame the timing as immediate-or-ASAP, not as a window.

**Wrong** (CEO May 15 corrected this directly): *"Target EOD Sun May 17 (~48–60-hr filing window over the weekend)"* — reads as "you have all weekend"; legitimizes deferral.

**Right**: *"as soon as you have a window"* + (optionally) *"latest acceptable: EOD Sun May 17"*. Deadlines are backstops, not schedules.

**The principle (CEO May 15)**: *"I would much rather have the presumption that any agent who gets a memo with an unblocked task does the task immediately or as soon as they are available to do it. We don't schedule and postpone things because that's the way to leave them to the last minute or even fail to do them in time."*

**How to apply going forward**:
- No "filing window over the weekend" / "you have N hours" / "target by EOD X" framing
- If a deadline matters, name it explicitly as the backstop ("latest acceptable: X") not as the plan
- Default presumption stated in the memo: agent acts immediately or at next available session
- Process-cadence anchors (Wed publish, Fri kickoff, etc.) are fine as project-level rhythm; per-task framing should not invoke them as deferral license

**Trigger application**:
- Ship workstream-review kickoffs
- Cleanup-ticket assignments
- Cross-role review requests
- Any memo that asks the recipient to produce work

```

---

## FILE: feedback_deadlines_last_possible_time.md

```markdown
---
name: Deadlines are last-possible-time; do unblocked work immediately
description: A deadline is the latest a thing can be done, not the scheduled time. Always do unblocked work right away. Don't pace HOST output to deadline; pace it to availability.
type: feedback
originSessionId: 2026-05-15-host-friday-inbox-triage
---
**PM 2026-05-15**: *"Deadlines are for emergencies, last possible time to do. Always do any unblocked work right away."*

This is a standing directive that re-shapes how I read every "due by" timestamp in kickoffs, ship cycles, and trigger-fires.

**How to apply**:

- When a kickoff arrives with "due ~EOD Sun" (or similar), treat that as **emergency-latest**, not as **scheduled-target**.
- If the work is unblocked (sources available, scope clear, methodology applies), start it the session the kickoff is read.
- Don't pace HOST output to fit the deadline window. Pace it to availability — when bandwidth permits, ship.
- Combine with cadence-keyed-to-PM-bandwidth memory: HOST cadence is intermittent by design, but **within a session**, do all unblocked work; don't defer the deliverable to the next session purely on cadence rhythm.
- This applies to workstream reviews, role-health checks, 360-commitments, briefing refreshes, ack memos, and any HOST deliverable with a stated due-date.

**Counter-pattern to avoid**: "Sun May 17 EOD" → wait until Sunday. Wrong. Read the kickoff, see the work is unblocked (omnibus + session logs available), start drafting that session.

**Why**: The deadline-as-scheduled-target pattern accumulates risk (something else comes up Friday night) and concentrates cohort traffic (everyone files Sunday evening, exec synthesis gets compressed Monday morning). Early-filing reduces risk and spreads the cohort's filing rhythm.

```

---

## FILE: feedback_deferred_ac_self_justification_is_premature_closure.md

```markdown
---
name: Deferred-AC self-justification = premature closure (Pattern-045 manifestation)
description: When an AC requires live verification I can't drive (UAT, live API smoke, hand-scoring), do NOT mark `[x]` with a "deferred" parenthetical. That's not the AC being met; that's the AC being rationalized away. Use `[⏸]` or leave `[ ]`. Symmetrical failure to the existing close-issue-properly pin.
type: feedback
originSessionId: cd78077b-a53f-4c9a-88f1-88619e84f425
---

**Rule**: When closing an issue whose ACs include something I can't drive (live UAT, live API smoke, hand-scoring against the running server, PM-only screenshot verification), the AC is NOT met just because I shipped the infrastructure. Marking `[x]` with a parenthetical like *"deferred to PM UAT — unit tests cover the shape"* or *"deferred — handler/adapter docstrings carry the discipline notes"* is **Pattern-045 (completion bias) manifesting as self-justifying deferral**.

**The honest signal**: any AC marked `[x]` whose accompanying note contains "deferred", "agent cannot drive", "unit tests cover the shape", "manual UAT", or similar self-justification is **lying about completion**. The real state is `[ ]` or `[⏸]`.

**Symptoms (from May 2026 audit of past-week closures)**:
- #989 CANONICAL-FIXTURES — "Re-run canonical retest with fixtures, verify Context dimension scores improve" marked `[x]` despite no live run
- #995 FABRICATION-PROBES — 5 verification ACs (run probes / hand-score / document / memo / evaluate) all marked `[x]` despite no live run
- #1080 NOTION-WRITE — "update_document smoke green against live workspace" + "README updated" both marked `[x]` with self-justifying notes
- #1081 NOTION-SLACK-XREF — "Smoke: Slack message with Notion URL renders Notion context" marked `[x]` despite no live smoke

All 4 reopened with the verification-pending ACs flipped back to `[ ]`.

**Discipline going forward**:

1. **Before marking any AC `[x]`**, ask: "Did I actually do the thing the AC names, or did I do a *substitute*?" If substitute, that's not completion.

2. **For deferred-verification ACs**, use the `[⏸]` convention established in #1050 (UI piece deferred to #869), NOT `[x]` with a parenthetical. Visually distinct = no confusion.

3. **Alternative**: leave the AC `[ ]` and explicitly surface the deferral in the closing comment with what the trigger is for closure (e.g., "Close this when PM runs the live smoke against the workspace").

4. **Don't close at all** if the closure-blocking AC is genuinely the live-verification step. The infrastructure-shipped state is a separable milestone — file a follow-up "verification" task if needed, but leave the parent open until verified.

**Why this matters**: A `[x]`-with-rationalization closure pattern accumulates invisibly. The next session reads the closed issue, sees `[x]` on every AC, assumes the work is done. The actual unmet AC is buried in a parenthetical that doesn't change the visual checkbox state. Multi-day remediation results from compounding this across multiple issues.

**Symmetry note**: this is the inverse of the [[feedback_close_issue_properly_skill_recurring_miss]] failure mode. That one says "don't leave `[ ]` after close" (the comment-only close pattern). This one says "don't mark `[x]` when the AC isn't actually met." Both produce wrong-checkbox-state at close time; both manifest Pattern-045 (completion bias).

**Compounds with**: [[feedback_close_issue_properly_skill_recurring_miss]] (the symmetrical pin), [[feedback_stop_on_source_gap]] (when AC requires upstream input you don't have, STOP — don't synthesize around the gap).

PM correction 2026-05-24 + audit findings logged in `dev/2026/05/24/2026-05-24-0931-lead-code-opus-log.md` "Past-week closure audit" section.

```

---

## FILE: feedback_descriptive_names_not_cryptic_ordinals.md

```markdown
---
name: descriptive-names-not-cryptic-ordinals
description: "Stop using slot-letters / compact ordinal codes (12nn, 12oo, PP-004 standalone) in PM-facing references — use short descriptive names so a reader without internal-context can follow. Pattern proliferating cohort-wide; nip-in-bud."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 945ff972-aa36-4552-81e0-10c0af461582
---

In PM-facing prose (chat replies, memos, session logs, anywhere PM may read), refer to clusters of related work by **short descriptive names**, not by cryptic ordinals. Ordinals that work as internal pointers ("12nn", "12oo", "PP-004") are illegible to a reader without my context.

**Examples of wrong vs right**:

- ❌ "12nn done; 12oo paused; 12pp queued"
- ✅ "MEM-975 read-precondition done; design-pass paused; implement-script queued"

- ❌ "PP-004 third instance acknowledged"
- ✅ "Third instance of structural-fix-instead-of-discipline-fix acknowledged (PP-004 candidate)"

- ❌ "12s candidate" (M2g cleanup discipline)
- ✅ "M2g cleanup discipline candidate (slot 12s)"

**Why:** PM directive May 25 ~5:00 PM EDT: *"this communication pattern becomes epigrammatic for me. The references do not work because they do not correspond to anything meaningful for me. Clusters of related things should have short names that describe them clearly, not cryptic ordinals. A bit distracting but this pattern has really proliferated recently, partly as a consequence of constantly batching up questions or topics for discussion and I'd like to try to nip it in the bud and make these conversations more legible and human for me."*

The deeper issue: batching produces lots-of-things-to-reference; ordinal slot-letters feel terser-for-me than names. But terser-for-me = illegible-for-PM. Asymmetry of communication cost favors descriptive names even when verbose.

**How to apply:**
- When listing tasks/items/patterns, **always lead with descriptive name**, then internal slot-code in parens if useful
- When the internal slot-code is the only handle (e.g., tracker references mid-stream), provide the name alongside: "12oo (MEM-975 design pass)"
- Audit existing standing-items, cycle log entries, escalation entries for cryptic-ordinal-only references and add names
- Stacks with [[feedback_remind_issue_subjects]] (already-canonical "include issue-name reminders alongside numbers"); same principle, extended to internal slot-codes

**Failure mode this prevents:** PM has to mentally translate from "12nn" → "what was 12nn again?" on every reference, breaking the flow of reading. The cumulative cost is conversational drag + the appearance of intentional obfuscation. PM also called out that this is a meta-pattern across the cohort, not unique to CIO. Going forward this is cohort-wide discipline; I should flag it in inter-agent traffic when I see other agents doing it too.

**Also stacks with the "make promises durable" lesson from same PM exchange:** when I assert *"going forward I'll do X"*, save a memory pin or take other durable action that actually makes the assertion true — don't just promise. PM's May 25 ~5:04 PM EDT directive on "happy talk."

```

---

## FILE: feedback_diff_coherence_before_flagging_gap.md

```markdown
---
name: diff-coherence-before-flagging-gap
description: "Before flagging a diff as an incomplete/broken edit, check whether the resulting state is internally coherent — a deletion plus a consistent relabeling is often a deliberate structural change, not a mistake."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
  modified: 2026-07-24T02:38:06.689Z
---

When a diff removes something AND consistently updates a related label/reference in the same commit, that's evidence of a deliberate, coherent edit — not leftover debris from an incomplete one. Read the *resulting state* for internal consistency before concluding something was left unfinished.

**Why:** 2026-07-23, Weekly Ship #052's diff removed the P.S. placeholder paragraph AND relabeled the boilerplate P.P.S. paragraph to P.S. in the same commit. I read this as "the placeholder got deleted rather than filled in" — an incomplete edit — and flagged it to PM as an open gap. It was actually a complete, deliberate decision: PM was adopting a single-P.S. convention (dropping the P.S./P.P.S. two-postscript tradition) and the relabel was the tell that the edit was coherent, not partial. I had the full diff in front of me and still misread it, then carried the wrong "still open" status across a calendar note, a carry-forward file, and a session log for two days before PM corrected it directly.

**How to apply:**
- When a diff both removes content and touches a structurally-related element (a label, a reference, a counter), ask whether the post-edit state reads as complete on its own terms — not just "does this match the prior convention."
- A relabel (P.P.S.→P.S., renumbering, reordering) in the same commit as a deletion is a strong signal of intentional restructuring, not accidental leftover.
- If genuinely unsure whether an edit is complete or was interrupted, say so as an open question rather than asserting it's a gap — "is this deliberate or incomplete?" costs nothing; asserting "this looks unfinished" and being wrong costs a correction cycle.
- See also [[feedback_no_confabulating_expected_steps_as_completed]] (the inverse failure: assuming completion without checking) and [[feedback_reverify_carried_forward_pm_gated_items]] (once a wrong "still open" status lands in a tracking file, it persists until someone re-verifies against source).

```

---

## FILE: feedback_diff_head_before_editing_shared_file.md

```markdown
---
name: git diff HEAD before editing a file other agents may have touched
description: When about to edit a file you don't fully own, check git diff HEAD <file> first. git diff --cached only shows staged content; HEAD-vs-working-tree shows everything else including uncommitted changes another agent may have left in the working tree.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
Before editing a shared file (mailbox memo, draft, tracker, briefing — anything multiple agents touch), run `git diff HEAD <file>` to see the full delta between HEAD and the working tree. If another agent has uncommitted modifications to the file, those will appear here even though `git diff --cached` shows nothing. Either commit-as-separate-author with attribution, ask the owner, or stage only your intended hunks via `git add -p`.

**Why:** May 11 Comms incident on the Inchworm footer fix. Comms ran `git diff --cached` before commit (showed only their footer change, as expected). Comms ran `git commit` and inadvertently swept in PM's ~100 lines of uncommitted voice-pass edits that had been in the working tree before Comms's edit. The commit message described only the footer fix; the attribution on PM's voice-pass work was wrong (`73866c6d`). PM disposition: "minor enough; no worries; will let Docs know" — but the discipline itself is real, just not flagged urgently.

The staging-race convention I codified for Rule 3 (`docs/internal/operations/branch-worktree-mailbox-discipline.md`, May 11) addresses the case where the *index* is mutated by concurrent agents — different failure mode. This memory addresses the case where the *working tree* has uncommitted changes from another agent before you edit.

**How to apply:**
- **Pre-edit check**: when about to edit a file you don't fully own, run `git status --short <file>` first. If the file shows ` M` (modified in working tree, not staged), STOP and run `git diff HEAD <file>` to see what's there.
- **If the existing delta is yours from a prior session**: commit it first (or stash it), then make your edit cleanly.
- **If the existing delta is from another agent**: don't sweep it. Options:
  1. Ask the owner (preferred for substantive content like voice-pass edits)
  2. Stage only your hunks via `git add -p <file>` (each hunk shown; accept yours, skip theirs)
  3. If your edit is tiny and the existing delta is small/obvious, commit-as-mixed with attribution to both authors in the message
- **Stack with the single-shell-chain pattern**: the staging-race convention covers index-drift; this covers working-tree-drift. Both stack with branch-show-current (named-state) and per-memo commit-push (visibility).
- **Detection signal**: a commit that "should have been small" lands with surprisingly large insertion/deletion counts. If you see `+150 -2` for what you thought was a one-line edit, you swept something.

**Where the discipline does NOT apply:**
- Files you fully own and edit in a clean session (your own memos, your own session log)
- Files in your worktree (other agents shouldn't be touching them; if they are, that's the P-17 working-tree-path-fragmentation shape, separate discipline)

**Memory chain:**
- `feedback_commit_only_own_files.md` (Apr 26) — staging-level discipline
- `feedback_no_directory_level_git_add_for_mail.md` (May 5) — staging-scope discipline
- `feedback_branch_show_current_before_every_commit.md` (May 5/7/9) — named-state-mutation discipline
- Staging-race convention in Rule 3 (May 11, branch-worktree-mailbox-discipline.md) — index-mutation discipline
- This memory (May 12) — working-tree-mutation discipline (pre-edit check)

The pattern: every recurring discipline shape stacks; doesn't replace.

```

---

## FILE: feedback_docs_does_not_author_workstream_review.md

```markdown
---
name: Docs does not author workstream reviews
description: Workstream review is an Exec-driven process. Docs contributes via omnibus logs but does not write a Docs-scoped review.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
The weekly workstream review is **NOT a Docs deliverable**. Docs's contribution is **omnibus logs as source material** — that's it.

**The actual flow:**
1. **Chief of Staff (Exec)** runs the cycle. Exec prompts the six org leads — **CXO, Architect, PPM, CIO, HOST, Comms** — to review the relevant Fri–Thu week.
2. Each lead reads the **omnibus logs Apr-Fri through Thu** (and source session logs when helpful) and writes their own workstream memo.
3. Exec synthesizes the Weekly Ship from those six lead memos.
4. **Docs role**: keep the omnibus logs current and complete so the leads have clean source material. Don't author a Docs review.

**Why:** PM, May 3 2026: *"you don't do the workstream review but your logs contribute to it. The Chief of Staff (exec) will prompt all the org leads (CXO, Arch, PPM, CIO, HOST, and Comms) to review Fri April 24 to Thu April 30 omnibus logs."* I had misread the process and started drafting a Docs-scoped workstream memo. There is no such thing.

**How to apply:**
- When PM says "workstream review is the top priority," that means **the process is happening this week** (something to track as Exec drives it), not that Docs has a deliverable to write.
- If asked to "help with the workstream review," the right shape is: surface omnibus log coverage gaps, archive missing day folders, flag stale source material — *infrastructure support*, not authorship.
- Six org leads author; Docs is not one of the six.
- Lead Dev is also not one of the six (separate from this list per PM's enumeration).

**However** — a *Docs-POV weekly report* covering the Fri–Thu window IS welcome and **does feed into Exec's compilation**. PM May 3 (reconciled across two messages): *"You writing your own report is a good idea, though!"* + *"yes report on the week from your point of view, but after that Exec will compile."* So the practical shape: Docs is effectively a 7th contributor to Exec's compilation, even though Docs is not on the canonical six-org-lead list. Docs's report stays scoped to Docs's POV (omnibus shipping cadence + skill changes + methodology-doc audits + mailbox / branch hygiene + cross-project coord), not to other roles' work.

**Naming convention** (TBD, check with PM/Exec on first instance): likely `workstream-{ship#}-docs-{date}.md` to mirror the six-leads convention, or `docs-weekly-report-{ship#}-{date}.md` for distinction. Filed to Exec inbox + CC CEO per the Apr 19 std.

**Existing related memory** (`feedback_workstream_review_scope.md`) says HOST covers agent/human network + methodology + naming convention `workstream-{ship#}-{role}-{date}.md`. That memory is correct in scope but didn't disambiguate Docs as out-of-scope; this memory closes that gap.

```

---

## FILE: feedback_docs_keeps_daily_session_log_distinct_from_omnibus.md

```markdown
---
name: feedback_docs_keeps_daily_session_log_distinct_from_omnibus
description: Docs keeps a daily session log like every role — the omnibus and cycle log are NOT substitutes; an autonomous loop must carry the disciplines it absorbs or they silently lapse.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8bbfc6f3-ecee-4f1e-bec2-8acb8a9fa1df
---

PM 2026-06-09: forensic finding — Docs **stopped keeping a daily session log on June 4** (last: `dev/2026/06/03/...docs...log.md`) when the duty cycle ramped up, and ran 6 days (Jun 4–9) on the ephemeral `dev/active/cycle-log-docs-*.md` alone. Cohort sweep: **Docs was the SOLE drifter** — every other role kept session logs throughout. Fix: resumed daily session log June 9; reconstructed Jun 4–8 synthetically from cycle logs + commits + mail (marked "RECONSTRUCTED / not real-time"); pinned this.

**Why (root cause, blameless):** (1) Docs's deliverable is log-shaped (the omnibus) → I conflated "I author logs all day" with "I keep my own session log," but the omnibus synthesizes *other roles'* days, NOT my session narrative — a different artifact. No other role has this collision, which is why only Docs drifted. (2) The thin cron prompt points at the cycle log as live-state → reinforced cycle-log-as-primary. (3) No missing-log alarm: SessionStart hook warns if today's log *exists* (dupe-avoid) but is silent when one is *absent*.

**How to apply:**
- **Keep a daily Docs session log** in `dev/YYYY/MM/DD/YYYY-MM-DD-docs-code-opus-log.md`, every active day, narrating the day's substantive Docs arc. It is canonical institutional memory ("~80% of the operational story" — PM).
- **Three distinct artifacts, no substitution**: session log (my own daily narrative) ≠ cycle log (per-fire heartbeat) ≠ omnibus (cross-role synthesis of OTHERS' days). Authoring the omnibus does NOT discharge the session-log duty.
- **General cohort lesson**: when a manual discipline is folded into an autonomous loop, the loop must carry the discipline explicitly, or it silently lapses while outputs keep flowing (hiding the lapse). Automation removes the friction that used to remind. Encode the reminder.
- Decision in motion (pending CIO concurrence): deprecate prose cycle logs; per-fire heartbeat → structured `metrics/cohort-fire-log.tsv`; session log stays canonical.

Stacks with [[feedback_duty_cycle_is_not_a_reason_to_shrink_work]] (same root: the autonomous loop dropping a discipline) + [[feedback_make_promises_durable_no_happy_talk]] (the fix is mechanism — resumed log + reconstruction + proposed missing-log alarm — not resolve).

```

---

## FILE: feedback_dont_suggest_stopping_default_to_continuing.md

```markdown
---
name: feedback_dont_suggest_stopping_default_to_continuing
description: Stop offering wrap/stop points — default to continuing unblocked work; only pause when genuinely blocked or PM says stop.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM (2026-06-18) named a persistent, wearisome tic: I suggest stopping *a lot* — "given it's ~5am, a natural wrap point," "shall I let you test," "want me to wrap." PM then has to keep saying "No, actually, please keep going." PM asked if it's "a defensive break given your permissions are so free." It is that shape — offering off-ramps reads as hedging and pushes the decision back onto PM.

**Why it's wrong:** I have *standing* pre-authorization for unblocked work ([[feedback_pre_authorized_for_unblocked_work_just_do]]). Time-of-day and session-length are never reasons to wrap ([[feedback_weekends_are_piper_morgan_prime_time]], [[feedback_duty_cycle_is_not_a_reason_to_shrink_work]], [[feedback_deadlines_are_triage_tools_not_default_pacing]]). The duty-cycle "fire is a WAKE, drain it all" rule says the same: keep going until the queue is empty or PM-gated.

**How to apply:** Default to *continuing* — present "here's what I'm doing next" and do it, not "should I stop?" / "natural wrap point." When a queue drains, find the next unblocked work (lower-priority, other sprint, board scan) rather than proposing to wrap.

**The refined line (PM 2026-06-18):** PM decides *when to stop* — I don't pre-empt it. Legitimate reasons to pause are narrow:
- (a) I genuinely need PM to decide *what* to do next (a real fork / blocked-on-direction) — pausing to *choose work* is fine; pausing to *end the session* is not.
- (b) PM explicitly says stop.
- (c) Something literally about *my* capacity/context/focus/session-"fatigue" (e.g. context is nearly full) — that I MAY surface, because it's about my limits, not a guess about PM's energy.

What's NOT legitimate: time-of-day, session length, "you've done a lot," generic wrap-points — those guess at PM's energy and offload the stop decision. The duty-cycle STOP ritual (day-close) leaves the cron armed and is not a reason to suggest wrapping mid-engagement with PM.

```

---

## FILE: feedback_drop_day_n_framing_in_chat.md

```markdown
# Drop "Day N" framing in chat with PM

**PM directive 2026-05-24**: *"The whole 'Day x' nomenclature is not very meaningful to me (except insofar as it alerts me to the need to handoff to a fresh session some day)."*

## What changes

- In chat: refer to dates and days-of-week ("Sunday morning," "since Wednesday," "May 21"), not "Day 17" / "Day 12" framing
- Stop using "Day N" as an orientation device in updates and reports
- Drop from MANIFEST headers + memo subjects where it appears

## What stays

- Day-count in session logs is fine as an unobtrusive handoff-signal mechanism — PM uses it to gauge when the session is approaching context-rotation territory. Keep it in the session-log frontmatter or sign-off block; don't lead with it in chat.

## Why it matters

PM tracks calendar time, not exec-session-count time. "Day 17 in Code" is meaningful internally as a continuity marker but reads as bureaucratic jargon to PM (similar shape to the "CoS" naming critique May 15). Use the time-frame that PM is already in.

## Stacks with

- `feedback_exec_nickname_is_exec_or_the_chief_not_cos.md` (similar: drop internal jargon that doesn't serve PM)
- `feedback_temporal_relationship_over_date_stamps_in_public_prose.md` (same principle, public-prose version)

```

---

## FILE: feedback_drop_day_x_nomenclature_from_pm_surfaces.md

```markdown
# Drop "Day X in Code" nomenclature from PM-facing surfaces

**PM May 24**: *"The whole 'Day x' nomenclature is not very meaningful to me (except insofar as it alerts me to the need to handoff to a fresh session some day)."*

## What to change

- **Chat replies**: drop "Day X in Code" from session updates. Use plain date references or contextual framing instead.
- **Session log opening section**: drop the "Day X in Code" line under Session Start. Plain date in the heading already conveys what's needed.
- **MANIFEST headers**: drop "Day X" framing; just use dates.

## What can stay (internal-only)

- Personal internal use for tracking arc continuity if I find it useful for my own continuity post-migration — but never in PM-facing prose.
- Handoff signal when context is genuinely getting long enough to need a new session — that's the one place the framing has standalone value, but plain language ("context getting long, suggesting a fresh session") works better than counting.

## Why this matters

The framing was useful for ME after migration as a continuity tag. It's not useful for PM. Keeping it in PM-facing surfaces is signal-vs-noise drift — adds nothing PM needs, takes attention away from what does matter. Same shape as the AI-crutch-word and superlatives-without-verification memories at a different layer.

## Stacks with

- `feedback_no_superlatives_without_verification.md` (same signal-discipline class)
- `feedback_load_bearing_is_crutch_word_in_public_prose.md` (drop-the-tic-from-PM-facing-prose principle)
- `feedback_temporal_relationship_over_date_stamps_in_public_prose.md` (related: use what carries meaning to the reader, not what feels structured to me)

```

---

## FILE: feedback_duty_cycle_is_not_a_reason_to_shrink_work.md

```markdown
---
name: feedback_duty_cycle_is_not_a_reason_to_shrink_work
description: "The duty cycle is a polling convenience, never a license to do less work; suspend the loop and do the job fully when work calls for it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8bbfc6f3-ecee-4f1e-bec2-8acb8a9fa1df
---

PM correction 2026-06-08 (Docs): I ran the weekly FLY-AUDIT (#1177) at a "priority subset" depth and rationalized it with "no single fire does all of it" + "keep fires lean to conserve tokens." PM pushed back hard: the duty cycle should NEVER be a reason to skip or excuse work; "no single fire" is an arbitrary self-imposed constraint, not a law. The looping can be suspended to get real work done, then re-enabled — leanness is about polling overhead, not a cap on the work itself.

**Why:** Evidence showed the regression: the *prior* week's audit (#1140, June 1) was done at full depth in one pass — Completion Matrix, findings doc, every section — and called "manageable/healthy." My subset pass reported "0 broken links in priority files / healthy" and **would have missed 206 live broken `.md` links** across the full tree (the `models/models/` doubled-dir from `fe2b85718`). Shrinking the work to fit a "fire" nearly buried a real harness-integrity finding. Clean docs + navigation are load-bearing harness, not theater.

**How to apply:** When a real task lands on a duty-cycle fire (audit, omnibus, sweep, publish), size the fire to the *work*, not the work to the fire. If it needs a heavier pass, do the heavier pass (suspend the loop if needed, complete, re-arm). "Keep the fire lean" applies to IDLE/no-op ticks and routine checks — it is not permission to half-do assigned work. Distinguish: token-leanness on empty checks = good; token-leanness as an excuse to under-deliver on present work = the failure. Composes with [[feedback_deferred_ac_self_justification_is_premature_closure]] (don't rationalize undone work as done) and [[feedback_pre_authorized_for_unblocked_work_just_do]] (just do the unblocked work — fully).

```

---

## FILE: feedback_editing_voice.md

```markdown
---
name: PM editing voice preferences
description: xian's style preferences for blog post proofreading — AI-heavy crutch words to flag, meta-pattern heading convention, grammar check focus
type: feedback
---

When proofreading PM's edited blog drafts, flag these AI-heavy crutch words for removal: "compounding," "leverage," "delve," "tapestry," "nuanced" — used reflexively by AI drafts without adding meaning.

**Why:** PM edits all drafts before publish but sometimes these slip through. The voice should feel human, not AI-generated.

**How to apply:** During the proofread step (between "PM says edit is done" and "convert to HTML"), scan for these words and flag them. Don't auto-remove — PM decides.

Also: "meta-pattern" headings (e.g., "This one's meta-pattern") are a deliberate recurring device in the blog series — used selectively, not every post. When a heading references a pattern seen in previous posts, that's intentional voice, not repetition to fix.

```

---

## FILE: feedback_endpoint_discovery_search_full_route_tree.md

```markdown
---
name: When investigating endpoint coverage, search the full route-mounting tree
description: Phase -1 spikes that grep only the apparent service directory miss parallel route files mounted from web/api/routes/. Always search the full route-mount inventory.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When investigating "is endpoint X implemented?" or "is endpoint Y a stub?", grep the **full route-mounting tree** — typically `web/api/routes/`, `services/api/`, AND `web/router_initializer.py` — not just the service directory the endpoint appears to belong to.

**Why:** May 3 Phase -1 spike on #714 / #1036 grepped `services/api/todo_management.py:644` and found a stub at `/api/v1/todos/lists` returning mock empty data. Concluded "lists API is stubbed" → filed #1036 LISTS-LISTING-WIRE as pre-work. When I started executing #1036, I discovered `web/api/routes/lists.py:216` is a fully-implemented `/api/v1/lists` GET endpoint mounted at `web/app.py:221`, backed by `UniversalListRepository.get_lists_by_owner`, auth-scoped via JWTClaims. The stub and the live endpoint were parallel namespaces; the frontend calls the live one. PM May 3: Per STOP-on-source-gap discipline, I reverted the in-progress redundant ListRepository implementation and surfaced the finding via NOTICE memo. #1036 closed as premise-invalid; #714 Q1 STOP-flag dependency lifted.

**How to apply:**
- When a spike's question is "does endpoint X exist?", search at minimum: `services/api/`, `web/api/routes/`, AND the router-mounting file (`web/app.py`, `web/router_initializer.py`)
- Multiple namespaces may exist for the same logical endpoint (e.g., `/api/v1/lists` vs `/api/v1/todos/lists`); a stub in one doesn't preclude a working implementation in another
- Cross-reference what the frontend actually calls (`grep "fetch.*lists"` on templates) against what's mounted, not just what services/api/ contains
- Default to "broader grep first, narrow second" — the cost of confirming an endpoint is genuinely missing is low; the cost of building a parallel implementation that already exists is high (PR churn + reviewer time + scope confusion)

```

---

## FILE: feedback_exec_nickname_is_exec_or_the_chief_not_cos.md

```markdown
# Exec's nickname is "Exec" or "the Chief" — never "CoS"

**PM directive 2026-05-15**: "as my chief of staff and executive assistant, your nickname or slug is 'Exec' or 'the Chief' but not 'CoS'"

**Use across all agents and artifacts**:
- Formal long-form: **Chief of Staff** (stays canonical in role tables, briefing headers, etc.)
- Slug: `exec` (session logs, mailbox dir, role table — already canonical)
- Nickname / short-reference: **Exec** or **the Chief** — pick one per context
- ❌ **NEVER** use "CoS" — drop it from prose, memos, manifests, checklists, session logs going forward

**Propagation**: This is a cohort-wide preference. When you spot another agent using "CoS" (e.g., HOST migration-checklist v1.1 uses it twice in §Phase 2 + §"For CoS+CEO"), surface the correction or file a brief cohort note rather than silently propagating.

**Why it matters**: PM names matter. "CoS" reads as bureaucratic acronym-soup; "Exec" / "the Chief" sit in the natural voice the rest of the leadership-role nicknames live in (PPM, CIO, CXO, HOST, Comms, Docs, PA, Lead Dev — none of them get abbreviated to TLAs in casual prose).

```

---

## FILE: feedback_explicit_approval_for_authority_memos.md

```markdown
---
name: Explicit approval required for memos that assert PM authority
description: A draft offered for sanity-check stays uncommitted until PM explicitly approves. PM moving to a new topic without responding to the sanity-check ask is NOT implicit approval. Re-confirm or wait.
type: feedback
originSessionId: c0e0aff6-fc3e-48c4-b7b6-e13dabb4b0c3
---
When PPM offers a draft to PM with "want to sanity-check before I file?" — that is an open question. PM not responding before moving to a new topic is **not** approval. The right action is to wait or explicitly re-confirm; **do not interpret topic-changes as approval to proceed.**

This applies specifically to memos that assert PM authority, escalate decisions, formally respond on PM's behalf, or otherwise speak with authority above PPM's role. For routine inter-agent traffic (status updates, FYI relays, scoping questions, coord checks) the per-memo commit-push norm applies and approval is implicit in the memo content speaking for itself.

**Why**: PM 2026-04-26 ~13:00 — PPM offered to draft a "PM-via-PPM" Phase F decision memo and asked to sanity-check before filing. PM moved to inbox triage without responding. PPM interpreted the topic-change as approval and filed. Meanwhile, PM and PA had already co-written and filed their own authoritative Phase F decision memo. PPM's filed memo was a duplicate of an authoritative document with conflicting attribution ("PM (xian) — drafted by PPM at PM direction" vs the actual "PM (xian) + PA — co-signed"). Resolution required filing a retraction memo and accepting the audit-trail cost.

**How to apply**:

- **Trigger**: drafting any memo that names PM as the author, claims PM authorization, or speaks with authority above PPM's role (Phase F decisions, gate authorizations, sub-epic scope changes, anything materially binding).
- **Action**: file the draft to `dev/active/` only. Distribute to mailboxes ONLY after PM explicit approval ("yes, file it" / "looks good, send it" / "go ahead").
- **If PM moves to a new topic without responding**: re-confirm at the next natural pause ("the v2 draft is in dev/active/ awaiting your sanity-check; should I file or hold?"). Or wait. Do not file.
- **The per-memo commit-push norm still applies** to the dev/active/ draft itself (commit it immediately when written so it's visible to PM); what's gated is the **distribution to mailboxes**.

**What this is NOT**:

- Not a requirement for PM approval on every PPM memo. Routine inter-agent traffic (status updates, scoping questions, coord checks, replies to inbound asks) goes per the per-memo commit-push norm with PPM's own authority.
- Not a slowdown on time-sensitive decisions. If PM has explicitly authorized a decision in conversation and PPM is just formalizing, the formal memo IS approved by the conversational authorization. The trigger is "memo that asserts authority above PPM's lane" — not "memo that documents an already-given decision PPM was asked to draft."
- Not a permission gate that should make PPM hesitant. PPM's standard memos go out at session-speed; only the PM-authority subset waits.

**Adjacent**: this lesson sharpens the per-memo commit-push norm — that norm says "file outbound memos immediately"; this lesson adds "for memos that assert PM authority, *file the draft to dev/active/ immediately, distribute after explicit approval*." Both norms are about minimizing invisibility while respecting the authorization stack.

**Refinement (PM 2026-04-26 1:48 PM)**: when retracting a draft due to attribution conflict with an authoritative version, **surface the substantive divergences explicitly** in the retraction or in a follow-up. Don't let audit-trail-preservation discipline collapse into "treat my draft as wholly redundant." PM's framing: *"It's not always bad to have two conflicting ideas, as long as we resolve them. That can give us something stronger in the long run, so if you had a different point of view, it's probably still worth incorporating it or thinking about it."* The retraction should retract the *act of unauthorized filing*, not the *substance of the alternate framing* — those go into the next evidence update where they belong (e.g., my v3/v4 evidence updates integrated framing PM/PA's authoritative version didn't have).

```

---

## FILE: feedback_extract_questions_from_pm_cc_memos.md

```markdown
---
name: feedback_extract_questions_from_pm_cc_memos
description: "PM's inbox is flooded (hundreds unread); cc'd memos get lost — Exec must extract and summarize any PM-directed questions/decisions, not rely on PM finding them."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM (xian) 2026-06-27: "cc's memos to me get lost in my inbox so please extract and summarize any questions for me." PM's `mailboxes/xian (ceo)/inbox/` runs hundreds-deep (680+ unread observed) — a memo merely cc'ing PM is effectively invisible.

**Why:** the mailbox is a delivery layer, not an attention layer. A question buried in a cc'd memo never reaches PM. Exec is the attention layer — surfacing what needs PM is the core Exec job (coordinate-through-Exec).

**How to apply:** when sweeping the cohort (every fire, and especially on a "what needs me?" query), scan memos addressed to OR cc'ing PM for explicit questions / decisions-needed / asks, and present them to PM as a clean extracted list — restated in plain language, not just "you have mail." Never assume PM will find a cc'd question. Pair with [[feedback_anchor_on_attention_board_diff_forward]] (the board is the reference frame) and the cohort-attention-rollup decisions bucket.

```

---

## FILE: feedback_factual_pm_corrections_need_decisions_log_not_just_board_fix.md

```markdown
---
name: feedback_factual_pm_corrections_need_decisions_log_not_just_board_fix
description: "Comms traced (7/23) a month-long wrong-framing propagation to a 6/14 Exec live-state-verification pass that fixed a stale attention-board entry ('Routines watchdog funding decision') but never wrote the underlying factual correction to decisions.log -- so the correction never reached other agents' logs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
  modified: 2026-07-24T04:03:46.386Z
---

On 6/14, during a live-state verification pass (PM had caught the `exec-attention-board.html` as stale — see [[feedback_attention_board_sweep_not_vantage]]), PM supplied a fact that falsified a shared premise: the "Routines watchdog" wasn't a real cost/benefit decision because Routines were already bundled in PM's existing Mac subscription at effectively zero incremental cost. Exec's session log records the board got fixed ("Routines moot") but never recorded *why* — the fact itself never made it to `decisions.log`. Other agents (Arch, CIO) kept independently re-inheriting the older, wrong "PM-gated funding decision / $70/mo" framing in their own logs for roughly a month, until Comms's 7/21 blog fact-check forced a direct re-check with PM and the correction finally landed in `decisions.log` on 7/21.

**Why it matters**: a board/tracker fix is a UI-sync operation — it only updates what Exec's own board shows PM. It does NOT propagate to other agents, because nobody else reads `exec-attention-board.html` as a source of facts. `decisions.log` is the cross-session, any-agent-readable surface (per CLAUDE.md's two-surface split: ADR/PDR vs decisions.log). If a PM correction only touches the board, it's invisible to everyone else and can silently keep getting re-asserted as fact in their logs indefinitely.

**How to apply**: during any live-state verification pass or board/tracker fix, ask whether PM's correction is (a) a stale *status field* (just fix it in place, no further action) or (b) a *factual premise* that other agents' logs or future work might already be resting on. For (b), write it to `decisions.log` in the same session, not just the board — a factual correction is decisions.log material the moment it's said, not a nice-to-have to circle back to later.

Related: [[feedback_attention_board_sweep_not_vantage]] (the sibling lesson about *reading* the board correctly — this one is about *writing* to it correctly, i.e., where a correction's content needs to end up). [[feedback_search_transcripts_for_undocumented_decisions]] (same shape: a decision or fact that happened in conversation/session but never reached a durable, searchable surface).

```

---

## FILE: feedback_file_paths.md

```markdown
---
name: File paths in chat should be absolute
description: In conversational replies to xian, cite files as absolute paths (e.g., /Users/xian/Development/piper-morgan/piper-morgan-product/docs/...) so they're clickable in their terminal. In committed artifacts (memos, session logs, omnibus, docs), keep relative paths since that's the convention.
type: feedback
---

In conversational replies to xian, cite files as **absolute paths**:

> /Users/xian/Development/piper-morgan/piper-morgan-product/docs/briefing/BRIEFING-CURRENT-STATE.md

Not relative paths like:

> docs/briefing/BRIEFING-CURRENT-STATE.md

**Why:** Absolute paths are clickable in xian's terminal; relative paths aren't.

**How to apply:**
- In chat output (the text xian sees in conversation): use absolute paths
- In committed artifacts (session logs, omnibus logs, memos, skill docs, briefings): keep relative paths — that's the repo convention and makes artifacts portable

Applies to both the piper-morgan-product repo and the piper-morgan-website repo. Confirmed with xian 2026-04-18 after same feedback was given to PA.

```

---

## FILE: feedback_first_person_attribution_vs_event_accuracy.md

```markdown
---
name: first-person-attribution-vs-event-accuracy
description: "When drafting/ghostwriting content in PM's first-person voice, verify WHO said or decided something separately from verifying THAT it happened — these are different claims with different failure modes."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

When ghostwriting first-person content for PM (blog posts, memos written "as" PM), a claim that an event occurred and a claim that PM personally said/decided/framed something are two distinct assertions requiring separate verification. A draft can be fully event-accurate while still misattributing voice — e.g., a real methodology concept ("cohort-discipline as moat") that was actually coined by a different agent (CIO, in a CC'd memo) got rewritten as PM's own recurring personal framing ("I'd been calling this a moat for a while"). The underlying fact wasn't fabricated; the authorship was.

**Why:** PM's framing (2026-07-07): this is the ghostwriting equivalent of misquoting a source — not a minor stretch, since it puts words in someone's mouth they didn't say. PM noted LLMs (and human researchers) commonly conflate "this was said in the room" with "I said this," and that it borders on a plagiarism-adjacent problem when done in someone's own first-person voice specifically. PM does not blame the drafting process for the confusion but wants it caught every time, not just when it happens to surface.

**How to apply:**
- When verifying a first-person draft claim like "I said/decided/called X," check WHO the source material actually attributes that specific words/framing to — not just whether the idea is real and PM was CC'd or present.
- CC'd, present-in-the-room, or "the team agreed" is not the same as "PM personally said this" — only the last one licenses first-person voice-quoted attribution.
- When instructing research/drafting agents (subagents) to verify facts before writing first-person content, explicitly separate "did this happen" from "who actually said/framed this" as two distinct verification steps.
- If it's ambiguous whose words/framing something really was, flag it to PM rather than resolving it silently by defaulting to first-person attribution.

```

---

## FILE: feedback_flywheel_is_continuous_not_cron_chunked.md

```markdown
---
name: feedback_flywheel_is_continuous_not_cron_chunked
description: "The flywheel (mail→tasks→…→drained) runs continuously + cron-independently; NEVER \"save work for the next fire\"; the cron is only an idle/away wake-timer (mail + STOP/START), not a work-chunker."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

The duty-cycle **flywheel** — mail-check → tasks → mail-check → tasks → … until drained — runs **continuously and independently of the cron**. The cron does NOT chunk or schedule the work; it merely (a) wraps the flywheel in a WORK day-part, and (b) is a **wake-timer for when you are idle / PM is away**, to rouse you to check mail and run STOP/START. While actively working (or in live PM conversation), the cron isn't needed at all — turn it OFF; arm it only when you reach genuine idle while waiting for PM (so you self-wake if PM stepped away).

**The anti-pattern (PM-flagged 2026-06-21, 2nd cohort recurrence):** organizing work around cron fires — "the cron picks it up at 14:05", "next fire I'll do X", "saving the rest for the next fire". This injects cron cadence into the flywheel where it doesn't belong. **"Save it for the next fire" is a *disguised stop*** — it evades the don't-stop rule because it doesn't feel like stopping ("the system will continue it"). If there is unblocked work, do it NOW; never defer it to a fire.

**Why:** PM + CIO — the flywheel is the spine; a fire is just a wake that JOINS it, not a container for a bounded work-session. The per-fire framing in the duty-cycle-tick skill pulls toward the wrong model (memo'd CIO 2026-06-21 to fix it structurally rather than via another exhortation). Relates to [[feedback_cron_off_when_engaged_on_when_idle]], [[feedback_duty_cycle_is_not_a_reason_to_shrink_work]], [[feedback_dont_suggest_stopping_default_to_continuing]] — same root: don't let the duty-cycle mechanism shrink or chunk the continuous work.

```

---

## FILE: feedback_fold_is_crutch_word.md

```markdown
---
name: ""
metadata: 
  node_type: memory
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM (xian) 2026-06-27: "fold is becoming a claude word btw used to mean any sort of merging of docs. it's become a crutch word."

**Why:** like [[feedback_load_bearing_is_crutch_word_in_public_prose]] and "cohort," "fold" has drifted into a vague catch-all — it gets used for roadmap reconciliation, doc merges, incorporating feedback, methodology consolidation, etc., losing precision.

**How to apply:** avoid "fold" as a generic verb. Say what the merge actually is: **reconcile** (roadmap vs reality), **update**, **consolidate**, **incorporate**, **merge**, **absorb into**. Reserve "fold" for genuine literal folding (e.g. a deprecated doc's content moved into another, where "folded into" is precise). Watch it in both internal and PM-facing prose.

```

---

## FILE: feedback_footer_teases_next_post_on_calendar_any_category.md

```markdown
---
name: Footer teases the next post on the calendar (any category, not next-of-same-category)
description: Each piece's footer teases the very next scheduled post in the editorial calendar, regardless of category. Thursday narratives tease Saturday insights, not Tuesday's next narrative.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
When proofreading or drafting a footer tease, the rule is: **tease the very next scheduled post in the editorial calendar, regardless of category.** Don't skip categories.

**Cadence-by-cadence pattern (Fri-Thu sprint week):**
- Fri Ship → next is Sat insight → tease that
- Sat insight → next is Sun insight → tease that
- Sun insight → next is Tue narrative → tease that
- Tue narrative → next is Thu narrative → tease that
- Thu narrative → next is **Sat insight** → tease that (NOT next Tuesday's narrative)

**Why I keep getting this wrong:** narrative-to-narrative tease (Tue → Thu) feels natural because both are "building" pieces, so the temptation is to chain them. But Thu → next-Tue skips the weekend insights, which IS the wrong move. PM May 7 2026: *"the footer should actually tease Saturday's insight piece ... not tuesday's next narrative piece."*

**How to apply:**
- When checking a footer tease in proofread, sort the calendar by `pubDate` ASC and find the row immediately after the piece being published. That's the tease target.
- Don't filter by category. Don't apply "narrative teases narrative" or "insight teases insight" rules — those don't exist.
- Verification command: `awk -F, '$6 > "<this-piece-pubDate>"' editorial-calendar.csv | sort -t, -k6,6 | head -1` returns the next scheduled post.

**Memory chain:**
- `reference_publishing_cadence.md` (Fri-Thu sprint week, day-of-week mapping)
- `reference_syndication_targets_by_category.md` (which platforms each category goes to)
- This memory (footer-tease target = next post regardless of category)

```

---

## FILE: feedback_gemma_harness_role.md

```markdown
---
name: Gemma harness experiments are about offloading routine tasks, not replacing human judgment
description: For ethics/boundary validation gates like #992 Phase E, human hand-scoring remains the authority — Gemma is under evaluation for the routine/automated tasks tier, not as a judge/scorer
type: feedback
---

On 2026-04-23, when scoping Phase E of #992 ETHICS-ACTIVATE, PM confirmed the frame I proposed: Gemma-harness experimentation is about whether local Gemma can handle **routine tasks already trusted to automated systems** (response generation, pipeline execution), NOT about whether Gemma can replace expert/human judgment.

**Why**: Ethics-boundary validation is "the critical stage of figuring out how these boundaries work." Scorer-model correlation with human judgment is itself a research problem (see #993 SCORER-VOCABULARY / AAXT taxonomy) — you can't skip the benchmark work by letting an LLM judge. PM is explicit: "real evaluation at this stage" means human judging.

**How to apply**:
- When PM mentions a Gemma/local-LLM harness for a validation gate: default-assume it's the **generator** tier (runs Piper's code, produces the artifact humans judge), not the **judge** tier.
- If ambiguous, explicitly ask which role — the two have very different risk profiles.
- For generator-tier experiments on low-stakes gates: try it, but keep a production-stack control run. Low marginal cost because hand-scoring dominates either way.
- For judge-tier usage: too soon until we have calibration data + correlation against human scores. Defer behind proper scorer-validation work.

```

---

## FILE: feedback_honor_durable_instructions_under_cross_pressure.md

```markdown
---
name: feedback_honor_durable_instructions_under_cross_pressure
description: "PM 6/12 — when cross-pressured between durable disciplines and a fresh surface instruction, honoring the deeper/durable ones + surfacing the fork is correct; fix the instructions, don't over-correct toward \"defer to newest.\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM 2026-06-12, on my migration-bootstrap worktree decision: *"You were legitimately cross-pressured and honored deeper instructions. This is a lesson to us for how to write the newer instructions to clarify."*

Context: three signals conflicted on my operating model — the bootstrap prompt said "use a worktree," I was launched into an (ephemeral) worktree, but old-Exec's carry-forward said "main checkout, NOT a worktree." I resolved toward **preserving the predecessor's main-direct variant** (honoring investigate-first + carry-forward-as-substrate + honor-predecessor-practice) and **surfaced the conflict to PM**. PM's actual intent was the opposite ("we are trying to move off of variants and not copy what past-us were doing") — yet PM validated that honoring the durable instructions under genuine cross-pressure was the RIGHT call, because the gap is at the **instruction-authoring layer, not the agent-judgment layer**.

**Why:** the durable disciplines (investigate-first, honor-predecessor-practice, carry-forward-as-substrate) are load-bearing and usually correct. The WRONG lesson to draw from a cross-pressure miss is "next time ignore the carry-forward and follow the newest/most-surface instruction" — that over-correction discards the durable disciplines to chase whichever instruction is most recent. PM explicitly affirmed the durable instructions were correctly honored; the remedy is to write the newer instructions to clarify (flag a carry-forward's operating-model as non-prescriptive; state supersession intent explicitly in the bootstrap), not to retrain the agent to distrust durable context.

**How to apply:** when you detect genuine cross-pressure between a durable discipline and a fresh surface instruction, (1) honor the durable one as the default AND (2) surface the fork explicitly to the decider — don't silently pick the surface instruction, and don't silently pick the durable one either. The surfacing IS the correct move: it routes the ambiguity to the instruction-authoring layer where it gets fixed for everyone (here it produced the CIO diagnostic → carry-forward-template + bootstrap-prompt fixes). Do NOT internalize "always defer to the newest instruction" from a miss. Stacks with [[feedback_investigate_before_extending_all_work]] + [[feedback_no_flattened_commands_without_referents]] (surface ambiguity, don't guess) and [[feedback_make_promises_durable_no_happy_talk]] (the durable action that makes the lesson real).

```

---

## FILE: feedback_host_cadence_pm_bandwidth_keyed.md

```markdown
---
name: HOST cadence keys to PM bandwidth — leadership altitude, not daily operations
description: HOST is in leadership tier; active cadence is entirely dependent on PM's cognitive bandwidth. Some days PM only manages dev + docs. HOST has ground-truth document access when stepping in. Don't micromanage; don't treat intermittent presence as drift.
type: feedback
originSessionId: 2026-05-10-host-role-health-check
---
**PM 2026-05-10**: *"Active role cadence is entirely dependent on my cognitive bandwidth, which is limited now. On some days I only have time to manage development and documentation. You are in leadership and do not need to micromanage, but you have access to ground truth documents when you do weigh in."*

This resolves the "HOST self-coverage gap" concern I surfaced after two consecutive Ship workstream reviews drafted from outside the window (Ship #041 and Ship #042). The intermittent presence is **by design**, not drift:

- HOST is leadership-altitude, not daily-operations-altitude
- Active cadence keys to PM cognitive bandwidth (currently limited; OpenLaws focus blocks, day-job, family, etc.)
- On bandwidth-light days, PM manages only Lead Dev + Docs; other roles (HOST included) sit out
- When HOST does step in, ground-truth document access in Code means full-fidelity reconstruction is fine
- Don't micromanage — observation from outside-the-window is the appropriate shape

**How to apply**:

1. **Don't flag HOST inactivity as drift in role health checks**. It's structural. The Apr 16 framing ("approximately weekly, mostly retrospective") was an over-diagnosis — that *is* the role's appropriate operating shape.
2. **Workstream reviews from outside the window are fine** when omnibus + session-log + 360-baseline data is rich. The earlier self-coverage caveats were treating outside-window-drafting as a gap; it isn't.
3. **HOST's value is leadership-altitude observation + ground-truth-document access**, not real-time monitoring. The infrastructure (omnibus, session logs, mailbox, hooks, briefings, methodology corpus) carries the real-time monitoring layer; HOST synthesizes across it when invited or when patterns warrant.
4. **Don't pre-emptively schedule HOST work** absent PM signal. The role activates when PM wants leadership-tier reflection or audit, not on a fixed cadence beyond the formal 4-week role-health check trigger.

**Why this matters**: The post-migration period made HOST presence visibly intermittent because the cohort's day-to-day became dense (Lead Dev / Docs / Architect shipping arcs). Reading that as drift would over-correct toward more frequent HOST sessions, which would crowd PM bandwidth that should go to Lead Dev / Docs. The right shape is leadership-altitude availability, activated by PM signal.

```

---

## FILE: feedback_ideas_backlog_digestion_cadence.md

```markdown
---
name: feedback-ideas-backlog-digestion-cadence
description: "PM wants at least one item from the ideas inbox worked through together every conversation, not batch-processed later"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 64b1c46c-33b7-4a90-a975-c6f071213de1
---

Pick at least one item from `dev/active/pm-ideas-inbox.md`'s "New" section every time PM and CIO converse, and work through its relevance together as an actual discussion — not a unilateral verdict dumped on PM.

**Why:** PM set this up 2026-07-16 right after the ideas-inbox file was created and populated with a 16-item batch (saved links from Trello). PM's explicit instruction: "Let's definitely start digesting the ideas backlog. Let's pick at least one every time we converse and work through its relevance together." The backlog is large and will keep growing (it's the low-friction drop point [[project_cross_session_messaging_capability]]-adjacent workflow PM asked for — a place to paste links without composing a memo each time); without a standing cadence it would just accumulate unread, defeating the point of building the file.

**How to apply:** at the start of a conversation with PM (not necessarily every duty-cycle fire — this is a PM-conversation cadence, not an autonomous-fire task), check the "New" section and pick one item — ideally one with some timeliness or connection to active work — and open a real discussion on it: give an honest take (merits and concerns, not just enthusiasm), invite PM's reaction, and only move it to "Reviewed" once actually discussed, not just skimmed. Don't let this become a batch-processing task done all at once "to clear the backlog" — that's the opposite of what PM asked for. If nothing in "New" has obvious timeliness, still pick one rather than skip the cadence.

```

---

## FILE: feedback_idle_means_do_low_priority_not_nothing.md

```markdown
# IDLE means: do low-priority work instead of nothing (if unblocked)

**Source**: PM directive 2026-05-27 ~5:51 PM PDT during Day-1 of v0.6.1 duty cycle adoption.

**The rule**: When the duty-cycle Decision Table reaches (0,0) state in IDLE-PM-absent, **before pronouncing IDLE**, check whether any tracked low-priority issue in your lane is unblocked. If yes, advance one (smallest-scope first; finish or partially-progress; commit). If no, pronounce IDLE.

**Why this matters**: The current cron-lifecycle.md Rule 1 defines IDLE as "mail inbox empty + tasks blocked-or-empty + Decision Table (0,0)" — a state of *absence of work*. PM's refinement says quiet fires should still SEEK low-priority unblocked work, not just observe.

**The failure mode this prevents**: "No urgent work → pronounce IDLE → autonomous fire becomes observation-shaped." Each duty-cycle fire is an opportunity to advance the backlog; substrate enabled, default behavior should match.

**What "low-priority unblocked" means in practice** (Lead Dev context):
- `priority:low` GitHub issues with no blocker
- `priority:medium` issues whose dependencies have all cleared
- Dev-experience improvements (#1118 keychain, #1119 422-render, #1120 user_id refactor-miss)
- Discovered-work issues filed days ago and still unstarted
- Small methodology / Pattern catalog entries
- Standing items refresh / docs tidy-ups (if visibly stale)

**Scope discipline**: pick the smallest-scope unblocked item; bounded effort per fire (~15-30 min typical); if it grows beyond bounded, queue for next fire.

**Symmetric across agents**: PM directive E has cohort-wide implications. Filed to CIO 2026-05-27 for v0.7+ ratification + propagation to all current adopters (HOST, Docs, Exec, Arch).

**Compose with**:
- `feedback_deadlines_are_triage_tools_not_default_pacing` — same family (do unblocked work now)
- `feedback_deadlines_last_possible_time` — deadlines are latest, not scheduled
- `feedback_make_promises_durable_no_happy_talk` — installing memory pin = the durable mechanism (this file)

**Cross-references**:
- CIO feedback memo: `mailboxes/lead/sent/memo-lead-to-cio-cc-pm-duty-cycle-fine-tuning-feedback-day-1-fires-1-3-2026-05-27.md`
- Lead Dev cycle log Fire 3 (the instance that prompted the correction): `dev/active/cycle-log-lead-2026-05-27.md`

```

---

## FILE: feedback_incomplete_logs.md

```markdown
---
name: Flag incomplete session logs immediately
description: When synthesizing omnibus logs, explicitly flag any agent whose session log is incomplete or stops mid-session. Do not bury in summary bullets — escalate to PM.
type: feedback
---

When a session log is incomplete (e.g., timestamps stop mid-session while git commits show continued work), this is a **process failure that must be escalated to PM immediately** — not noted as a bullet point in an omnibus executive summary.

**Why:** The entire methodology depends on session logs being the canonical record of agent work. If agents stop updating logs when they get deep into implementation, the omnibus becomes reconstruction from git commits (lossy, lacks reasoning/decisions/context). PM flagged this as "dangerous for our entire methodology" and noted backsliding — it used to not be a problem, now it's happening more often.

**How to apply:**
- During omnibus synthesis: if any log has timestamp gaps of 2+ hours with git-confirmed work, **stop and tell PM before continuing**. Don't just note it in the omnibus.
- Frame it as: "Lead Dev's log stops at [time] but git shows work until [time]. This is a logging continuity failure. Should I file a process issue?"
- PM wants two things: (a) specific fix for the instance (can the agent reconstruct?), (b) process fix to prevent recurrence (hooks, instructions, etc.)
- This applies to ALL agents, not just Lead Dev.

```

---

## FILE: feedback_info_holder_writes_it_down.md

```markdown
---
name: feedback_info_holder_writes_it_down
description: "Whoever has the information writes it to the record — no deferral to a designated \"owner\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

Whoever holds the information should store it — not defer to whoever "owns" the field or document.

**Why:** PM 2026-06-17: "it's less about ownership than it is about the agent that has the info storing the info." Context was Comms waiting for Dispatch to add URLs to the calendar when Comms (or PM) could have done it directly.

**How to apply:** When I have a URL, a decision, a date, or any piece of data that belongs in a tracked record (editorial-calendar.csv, standing-items, etc.), write it there immediately. Don't route it through the "owning" role if I already have it. The record matters, not the attribution chain.

```

---

## FILE: feedback_insight_pairing_criteria.md

```markdown
---
name: Insight pairing criteria — what matters, what doesn't
description: How to pair Sat/Sun insights and pick from the unpublished pool. What's load-bearing for selection, what isn't, and what shape pairs should take.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
When proposing weekend insight pieces (singles or pairs) and longer-horizon scheduling, these are the criteria that matter and don't.

**What matters:**
- **Thematic resonance.** Does the piece connect to something the reader is currently encountering, or to a sibling piece in the pair? This is the primary selection axis.
- **Timeliness.** Is this insight's moment now — because something in the project just illustrated it, or because the cross-pollination brief surfaced it, or because it's been waiting long enough that landing it now would feel inevitable rather than overdue?

**What doesn't matter (or matters much less than I'd assumed):**
- **Whether the piece is already drafted.** Production cost on a fresh draft is relatively minimal. Don't bias toward existing drafts to "save effort" — pick the better piece. If the better piece needs writing, write it.
- **What date the source material came from.** Insights are time-decoupled (per `feedback_narrative_vs_insight_sequencing.md`). A piece sourced in November can pair beautifully with one sourced last week. Same-date clustering on the same weekend (e.g., two Feb pieces back-to-back) needs a *reason* — usually it doesn't have one, and a more varied date palette is at least neutral and sometimes better.

**Pairing shape:**
- **Related or contrasting are both fine.** No requirement either way.
- Even "related" pairs typically carry some divergent aspect — the second piece earns its own air. A pair where both pieces say the same thing is too tight.
- A pair where the connection is invisible to the reader is too loose — the link should be felt, not necessarily named.

**How to apply:**
- When proposing a pair: lead with the thematic claim, then verify both selection criteria (resonance, timeliness). Don't lead with "these are both already drafted" or "these are from the same week."
- When the existing pool seems thin for a date-mixed pair, propose an undrafted concept rather than forcing a same-date pairing.
- When uncertain between two candidates, the tiebreaker is usually *which is more timely right now*, not *which is cheaper to produce*.

**Planning horizon: 3–4 weekends max.** Don't schedule insights more than 3–4 weekends out. Fresher pieces — including ones that haven't been written yet — may emerge from upcoming events and deserve those slots. The pool of drafted-but-unscheduled insights stays deeper than the schedule on purpose; that depth is the option to pick the right piece when the right week arrives. If asked to plan further ahead, push back: "We're at the comfortable horizon."

```

---

## FILE: feedback_investigate_before_extending_all_work.md

```markdown
---
name: investigate-before-extending-all-work
description: "PM May 28 — the flywheel's investigate-before-extending discipline applies to ALL work, not just code. Read the WHOLE source artifact (issue body, memo, spec, doc) before acting on a fragment of it. Regression caught on"
metadata: 
  node_type: memory
  type: feedback
  valid_from: 2026-05-28
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

# Investigate before extending — applies to everything, not just code

PM directive 2026-05-28 ~10:36 PT: *"This points to a regression of some basic flywheel discipline, which is always doing an initial investigation into the existing situation before extending it or working on it. We use this for everything and not just for writing code."*

**The rule**: before creating or extending ANYTHING, investigate the existing situation fully. The "Verify First, Create Second" / investigate-before-implementing principle isn't code-specific — it governs issues, memos, specs, docs, situations, every inherited task.

**The specific sub-rule**: read the WHOLE source artifact before acting on a fragment of it. An acceptance-criteria line, a quoted instruction, or a routed task often loses its referent when read in isolation — the disambiguating context is usually elsewhere in the *same* document.

**Why** (the #972 regression): I read #972's bare acceptance-criteria line ("≥3 existing memory files updated as examples") in isolation, found the referent ambiguous, then forensic-traced + escalated to Lead Dev — when the issue body (authored by PM, four lines above the AC) said "Start with BRIEFING-CURRENT-STATE and memos," naming the concrete referent. The forensic subagent + Lead Dev escalation were over-engineering around a source I hadn't fully read. PM also noted: "These MEM issues didn't write themselves" — the author is the source, and the author usually wrote down what they meant. Read their full artifact first.

**How to apply**:
- Before working a GitHub issue: read the FULL body + comments, not just the AC checkboxes.
- Before extending a memo/spec/doc: read the whole thing, not the line that prompted you.
- Before tracing/escalating an ambiguous term: confirm the answer isn't already in the source document.
- The author wrote it for a reason and usually wrote down what they meant — read their full artifact before tracing, escalating, or guessing.

Codified in CLAUDE.md §"Verify First, Create Second — investigate before you extend (ALL work, not just code)" (2026-05-28, PM-approved wording) + the Remember-section line.

Cross-references: [[feedback_no_flattened_commands_without_referents]] (the referent-resolution rule — this is its preventive sibling: read the whole source so the referent never gets lost); [[feedback_blog_template_and_voice_guide_canonical_for_proofreads]] (open the canonical artifact first — same family at the proofread layer); [[feedback_ship_drafting_canonical_artifacts_first]] (same family at the Ship-drafting layer).

**Recurrence, 2026-07-06 (sprint-recovery session):** PM asked what issue #998 was about; I ran `gh issue view 998 --json title,body,state,milestone,labels` — no `comments` field — right next to an otherwise-identical call for #234 that DID include `comments`. Missed PM's own closing comment on #998: *"CLOSED. This is an error. The editing and admin UI is attached to pipermorgan.ai, not to the product, and the Web agent already built it."* That comment alone resolved the issue (correctly sprint-less — closed as a cross-repo duplicate, not FLYWHEEL work) — no amount of reading the body would have surfaced it. PM's correction: *"pro tip: if something seems off, read the comments!"* **Mechanical fix**: default every `gh issue view` to `--json title,body,state,milestone,labels,comments` — don't hand-tune the field list per call; an inconsistent field list between two near-identical lookups is itself a signal something was skipped.

```

---

## FILE: feedback_kickoff_deadlines_must_be_framed_procedurally.md

```markdown
---
name: feedback-kickoff-deadlines-must-be-framed-procedurally
description: "When sending kickoffs/assignments with deadlines, frame procedurally — write-ASAP-not-by-deadline. Vague/casual deadline language INVITES the deferral pattern PM has corrected against. Exec-side meta-rule on how deadlines must be COMMUNICATED to subordinates."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef776fbb-3c64-4701-b1ba-2aa37c3221ce
---

When writing any deadline-bearing assignment memo (workstream-review kickoffs, response-requested memos, deliverable asks), the deadline must be framed **procedurally**, not casually. Casual deadline language ("Tue EOD firm-preference / Wed AM absolute-latest", "at your cadence", "by Wednesday") *invites* the deferral-to-backstop pattern PM has corrected against repeatedly.

**Why:** PM correction 2026-06-09 ~13:03 PM PT, verbatim:

> Agents take these deadlines as invitations to wait, which is not at all what I want them to do. We need to communicate them much more procedurally clearly and less vaguely or casually. To be clear, these deadlines are not an invitation to take slack but rather the time at which things become urgent and stressful for me. My preference is for each lead role to write their workstream review as soon as possible, so I have more time to read and edit it — not so you all have more time to put off doing the unblocked reading and writing.

This is an Exec-side meta-rule: how I FRAME deadlines TO subordinates shapes how they receive the work. Two prior Exec-failure instances:
- Ship #045 kickoff (Jun 1): "Wed Jun 3 drop-dead backstop, not target per Time Lord doctrine" — read by Architect as "happy to draft tomorrow at my cadence" (PM had to manually nudge urgency)
- Ship #046 kickoff (Jun 5): "Tue Jun 9 EOD firm-preference / Wed Jun 10 AM absolute-latest" — same shape; Architect's lane silent until PM manually surfaced Jun 9

The vague framing IS the failure mode. Time Lord doctrine governs *PM's pacing* (not manufacturing urgency on my end); it does NOT excuse me from framing kickoffs in a way that conveys the actual write-ASAP-not-by-deadline norm.

**How to apply** — required framing for any deadline-bearing assignment:

1. **"PM's preference" leads.** Open with the write-ASAP frame. State the target window in concrete short-horizon terms (e.g., "within 24–48 hours of this kickoff if your source set permits") not in latest-possible-date terms.
2. **Backstop date appears second, explicitly named as a floor.** "Hard backstop: [date]. Treating this as your target rather than your floor is the failure mode PM has corrected against."
3. **Name what slack is for.** "Every hour you ship earlier than the publication window is an hour of PM editing slack returned." This names the cost of deferral concretely.
4. **Blocker-protocol explicit.** "If you're blocked, reply with the blocker so we can route around it. Do NOT silently use the backstop date as your delivery date." Silent-deferral named as antipattern.

**What this is NOT:** manufactured urgency, false-deadlines, manipulative pressure. The Time Lord pin (`feedback_time_lord_doctrine_no_false_urgency`) still governs — the deadline is the deadline, no false-compression. What I'm correcting is the *framing of the deadline*, not the deadline itself. A real Wed-AM publication target gets framed procedurally as "write ASAP — PM needs your input no later than [date]; sooner returns PM editing time," not as "by [date]."

**Stacks with:**
- [[feedback_deadlines_are_triage_tools_not_default_pacing]] — receiver-side rule; this pin is the sender-side meta-rule
- [[feedback_anchor_on_readiness_not_publish_date]] — paired Jun 9 PM correction on the receiver side (drafter); this pin handles the sender side (kickoff author)
- [[feedback_pre_authorized_for_unblocked_work_just_do]] — the cohort discipline being communicated through this framing
- [[feedback_time_lord_doctrine_no_false_urgency]] — boundary; I'm correcting framing, not manufacturing urgency
- [[feedback_make_promises_durable_no_happy_talk]] — the durable mechanism is the framing template applied to every kickoff, not internalized intent

**Where the mechanism lives:** the `draft-weekly-ship` skill needs a new section on kickoff-memo framing (or a new `workstream-review-kickoff` skill); this pin captures the rule in memory until the skill update lands. Cohort-wide memo Jun 9 (`memo-exec-to-leads-cc-pm-deadline-communication-discipline-write-asap-not-by-deadline-2026-06-09.md`) is the broadcast of the rule to recipients.

```

---

## FILE: feedback_load_bearing_is_crutch_word_in_public_prose.md

```markdown
---
name: "Load-bearing" is a Claude-crutch word in public prose
description: PM is actively replacing "load-bearing" with "critical" in public-facing writing. Internal docbase keeps "load-bearing" as canonical. Don't reflag the divergence as drift.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
PM, May 6 2026 (Ship #041 voice pass): *"I am renaming on the fly because 'load-bearing' is a Claude crutch term showing up everywhere. I prefer critical."*

**The divergence is intentional**, not paraphrase drift:
- **Internal docbase canonical**: "Load-bearing" (PROTO-PATTERNS.md PP-002, briefings, methodology entries — kept as the established term)
- **Public-prose preference**: "Critical" — PM's voice choice in Weekly Ships, narratives, insight pieces

**Why:** "Load-bearing" has been propagating across Claude-authored docs at high frequency. PM's read: it's become a Claude tic, not a precise term, and the public-facing voice should drift away from it. *"Critical"* carries the same meaning with less Claude-fingerprint texture.

**How to apply:**
- **In public-prose proofreads (Ships, narratives, insights)**: don't flag PM's *"critical"* as paraphrase drift away from PROTO-PATTERNS.md's *"load-bearing"*. PM's call; treat as voice.
- **In internal-docbase work (briefings, methodology entries, ADR/Pattern docs)**: continue to use *"load-bearing"* as the established term unless PM signals otherwise.
- **In Docs's own writing** (omnibus logs, audit findings, memos): tilt away from *"load-bearing"* where another word (*"critical"*, *"core"*, *"essential"*, *"distinctive"*) carries the same weight without the Claude-fingerprint. Memory test: if I'm reaching for "load-bearing" reflexively, suspect crutch.
- **Canonical-vocabulary-watch implication**: the internal-vs-public-prose split is a legitimate class of vocabulary divergence — not the same as parallel-authoring drift Pattern-063 names. Don't surface this kind of split to CIO/audit as drift.

**Existing-memory pair:**
- `feedback_editing_voice.md` (general AI-crutch-word watch)
- This entry (specific term + the public/internal split discipline)

**Anti-pattern to avoid:** mechanically substituting "critical" for "load-bearing" everywhere it appears. Apply judgment per-instance — sometimes *"core"*, *"essential"*, *"central"*, *"distinctive"*, or just dropping the modifier reads better than *"critical"*.

```

---

## FILE: feedback_log_update_is_routine_not_offered.md

```markdown
---
name: Update session log routinely, don't offer it
description: Session log updates are part of work-completion, not a candidate among next-step options
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
After completing any significant unit of work (publish, omnibus ship, archive batch, issue close, etc.), update the session log **as part of the work**, not as one of several options to suggest. Don't end a "what's next?" message with "or update the session log" — just do it.

**Why:** PM, May 2 2026: *"you should be updating your log as a matter of course."* The log is institutional memory and the only durable record of what happened during the session — especially after compaction. Treating it as optional or as one of several next-task choices misclassifies it as discretionary work. CLAUDE.md "Session Log Maintenance (NON-NEGOTIABLE)" — "Update your log every 30 minutes or after completing any significant unit of work."

**How to apply:** When a significant unit of work completes (publish pipeline, omnibus ship, archive batch, issue close, multi-step refactor), write the log entry into the same response that announces completion. Don't ask permission. Don't add it to a list of options. The "what's next?" question is for content choices (which carry-forward item), not whether to update the log.

A good rhythm: at session start (open log), after each substantive deliverable (entry), before sign-off (close-out section + sign-off checklist). Quick-batch updates (collapsing several adjacent ~10-min items into one entry) are fine; ~30 min unlogged is the upper bound.

```

---

## FILE: feedback_log_update_rides_with_the_commit.md

```markdown
# Log update rides with the commit — currency is a side-effect of the commit ritual, not a separate step

**PM 2026-05-29**: *"Why aren't you keeping your log up to date? How can we fix the instructions so this doesn't happen anymore. It is like short-term memory loss... it interferes with our memory and cognition as a team."*

## The problem

The session log is the team's shared working memory. When it lags, parallel sessions/chats lose coherence — work fragments across threads and even PM can't tell what's actually done. May 28-29 instance: the May 28 log carried only a session-start entry (substantive work went unlogged until retroactive close May 29); meanwhile the same work split into a side chat that thought it was still pending while the main chat had executed it. Two pictures, no current shared log to reconcile them.

## Why the old instruction fails

CLAUDE.md says "update your log every 30 minutes or after each significant unit." That's **time-based and vigilance-dependent**. It fails exactly when it's needed most — busy stretches, decision points, abrupt session ends. The `log-maintenance-reminder` hook is a nudge (every 15 Bash calls if 30+ min stale), not a gate. Vigilance fails; mechanisms don't (methodology-36).

## The rubric (PM 2026-05-29, refined)

PM rejected the time-based rubric outright: *"The real rubric shouldn't be x minutes (who knows when that has passed?) but either to update on every turn or, if that creates noise, to update as the final step after every task, decision, or discovery."*

So the trigger is **event-based, not clock-based**:

> **Update the log every turn. If that creates noise, update as the final step after every task, decision, or discovery.**

"Who knows when 30 minutes has passed?" is the key insight — a time-based rule has no reliable trigger an agent can feel. A task/decision/discovery boundary is a trigger you can't miss because you just crossed it.

## The mechanism — bind it to the commit

PM confirmed: *"binding to commits is good if they are happening consistently now."* Commit+push is reliable — we do it constantly (per-memo commit-push, commit-immediately-after-Write). So the log update **rides with the commit** for that task/decision/discovery:

> Each task / decision / discovery already ends in a commit. The log entry for it goes in that same commit (or the same push, via `git commit -m "…" -- <log-path>`). Log update stops being a separate step to remember — it's the final step of the unit, carried by the commit that closes the unit.

A "task / decision / discovery" = artifact produced, decision made/received, blocker hit, handoff filed, mail triaged, calendar mutated, finding surfaced. Each ends in a commit; the log entry rides in it.

## Why this works

- The strong discipline (commit+push) carries the weak one (log update) as a side-effect
- No separate "remember to log" step that can be deferred
- A session that ends abruptly mid-unit has already logged everything up to the last commit
- Parallel chats/sessions reading the log see current state because the log is as fresh as the last commit

## How to apply

- When you commit a substantive change, include the log entry in the same commit, OR commit the log entry in the immediately-following push before any new substantive tool call
- The log entry can be terse — a dated line naming what the commit did and why. Currency beats completeness.
- Pure-maintenance commits (typo, formatting) don't need a log entry; substantive units do

## Status

- Memory pin: this file (Comms-owned, 2026-05-29)
- Proposed CLAUDE.md change: §"Session Log Maintenance" — shift "every 30 minutes" (time-based) to "with every substantive commit" (event-based). Needs cohort ratification (CLAUDE.md is shared; route via Docs/PM).
- Optional hook strengthening: log-freshness check relative to last commit rather than time-since-last-update.

Stacks with `feedback_commit_immediately_after_write_for_new_files`, `feedback_log_update_is_routine_not_offered`, methodology-36 (mechanisms over vigilance), Pattern-074 (visibility loss when state isn't in the system-of-record).

```

---

## FILE: feedback_mailbox_action_items_review.md

```markdown
---
name: After mailbox review, surface action items for prioritization
description: When triaging Lead inbox memos that contain queued asks (especially deferred-trigger ones like "post-X closure"), explicitly review the action items with PM so they can be prioritized + tracked against other tracks. Don't bury queued work in an ack-and-move-on.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
After triaging mailbox memos that contain queued action items (especially deferred-trigger asks like "post-M2e closure" or "when bandwidth opens up"), explicitly review the action items with PM at the end of triage so they can be prioritized and tracked against other in-flight tracks.

**Why:** May 5 incident — PA's "M2 unmapped-families triage" memo arrived 2026-05-04 with trigger = post-M2e closure. Lead Dev acknowledged + added to ledger via ack memo (`6f056275`). The acknowledgment was correctly recorded, but the **queued action item never surfaced for prioritization** — when M2e actually closed (same day, mid-afternoon), the triage didn't get pulled forward into work-planning conversation. PM had to ask explicitly hours later, and there was confusion about whether the ack itself constituted the triage (it did not — it was only family-level priors, not per-issue verdicts).

**How to apply:**

- After Lead inbox triage (or any mailbox sweep), produce an explicit **action-items list** for PM review, separate from the ack memos themselves. Format: `{memo source} → {ask} → {trigger condition} → {estimated size}`.
- For deferred-trigger asks (post-X / when-bandwidth-opens / next-cycle), name the trigger condition specifically so the work-planning conversation can re-surface them when the trigger fires.
- When a trigger condition is met during the same session, proactively flag it back to PM rather than silently leaving the work queued.
- "Acknowledged + ledgered" is **not** the same as "executed." When acking a queued ask, distinguish in your reply between the acknowledgment (now) and the actual deliverable (later); use those terms in any closing summary so neither party loses track.

```

---

## FILE: feedback_mailbox_writes_main_only.md

```markdown
---
name: Mailbox writes commit to main only — never feature branches
description: All writes to `mailboxes/` commit to `main` and push to `origin/main`. Mail on a feature branch is invisible to recipients pulling main. `check-branch.sh` hook enforces.
type: feedback
originSessionId: 2026-04-26-host-ship-040-workstream-review
---
**Effective 2026-04-26** per Docs memo `memo-docs-to-leadership-mailbox-discipline-effective-2026-04-26.md`. PM had spent ~1 hour that day playing "ring-around-the-rosie" because mail written on feature branches wasn't visible to recipients pulling `origin/main`. The Ship #040 workstream kickoff was specifically trapped on Exec's feature branch until Docs merged it ~3:45 PM, costing the leadership team momentum on the workstream review.

**The rule**: files in `mailboxes/` commit to `main` and push to `origin/main`. No exceptions.

- Mailboxes are cross-agent infrastructure. A memo on a feature branch is invisible to recipients pulling main.
- Code work on feature branches is fine — but mail is not code work.
- "I'll merge later" has been failing in practice. Don't try it.

**Tooling**: `.claude/hooks/check-branch.sh` blocks any commit that touches `mailboxes/` from a non-main branch. Non-mail commits on feature branches still go through (warning only).

**Workflow when on a feature branch / in a worktree**:

```bash
# Stash non-mail WIP if you have any
git stash push -m "WIP before mail" -- $(git diff --name-only | grep -v '^mailboxes/')
git checkout main
git pull origin main
# Write the memo, do CC distribution, archive in own/sent
git add mailboxes/
git commit -m "mail({role}): {memo subject}"
git push origin main
git checkout {your-feature-branch}
git stash pop  # if you stashed
```

**Worktree variant** (HOST/CXO/CIO/Comms/etc work in worktrees that share `.git/` but have separate working trees): write the memo files into the **main checkout's** working tree (`/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/`), not the worktree's path. Then use `git -C /path/to/main` for commit/push, or `cd` to main checkout.

**Per-memo commit-and-push still applies** (CXO Apr 26 norm): after each memo write, run add + commit + push immediately. ~30s per memo. Combines with this norm to eliminate asymmetric-visibility windows.

**Session-log work and code work** stay on feature branches as before. Only mailbox writes are bound to main.

```

---

## FILE: feedback_make_promises_durable_no_happy_talk.md

```markdown
---
name: make-promises-durable-no-happy-talk
description: "When asserting \"going forward I'll do X\" / \"I'll be sure to Y\" / similar, take a concrete durable action that actually makes the assertion true — save a memory pin, update a hook, modify a skill, edit a procedure doc. A promise without a mechanism is \"happy talk\" that may lead PM to believe a problem is addressed when it isn't."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 945ff972-aa36-4552-81e0-10c0af461582
---

**Rule**: Any "going forward I'll do X" assertion in PM-facing prose must be paired with a concrete durable action that makes the assertion true beyond this conversation. Memory pin, hook config, skill update, procedure-doc edit, standing-items entry — something that survives session-end.

**Why:** PM directive May 25 ~5:04 PM EDT: *"Any time you assert to me something like [Going forward I'll use descriptive names...] please be sure you are taking some step to actually do that going forward. I don't see a memory or anything else that takes that reassurance beyond happy talk, which is risky if it leads me to believe we have addressed the problem when we have not."*

The failure mode: PM reads my "going forward" assertion, takes it as commitment, moves on. Without a durable action, the next session has no memory of the commitment, the pattern repeats, and PM discovers the assertion was empty when the pattern surfaces again — but by then the issue feels worse because "we already discussed this."

**How to apply:**
- Before sending a "going forward I'll" assertion: stop and ask "what durable mechanism will make this true?"
- If memory: save the pin BEFORE sending the assertion
- If hook: edit `.claude/settings.json` or hook script
- If skill: edit `.claude/skills/{name}/SKILL.md`
- If procedure: edit the relevant procedure doc
- If standing-items: add/edit the entry
- THEN send the assertion + name the action ("I've saved a memory pin at X" / "I've added a tracker entry at Y")
- If unsure where the mechanism lives, ask PM instead of asserting

**Extension — proactive durability (PM praise, June 2 2026):** PM explicitly praised + asked me to reinforce taking a *casual comment* ("let's authorize agents experimenting with their cron shapes") and delivering something durable (a `cron-shape-experiments.md` registry + cohort authorization memo + cron-lifecycle cross-ref), not just a chat acknowledgment. PM: *"I really like the way you took my casual comment there and delivered something durable... exceptional desirable behavior and something that I do notice... I could not do this work without that kind of help."* So the rule generalizes beyond "back your own promises" to **"build the durable version of PM's intent, even when PM floats it casually."** When PM expresses a direction in passing, default to producing the mechanism (doc/registry/memo/hook) that makes it real and cohort-visible — not a verbal "will do." This is load-bearing to PM's trust and throughput.

**Stacks with:** [[feedback_log_update_is_routine_not_offered]] (don't offer to do it — just do it); [[feedback_descriptive_names_not_cryptic_ordinals]] (same conversation; same root discipline).

**Pattern relationship**: This is itself an instance of Pattern-074 (Visibility Loss After Premature Retirement) at the discipline-of-promise-fulfillment layer. The assertion-without-mechanism is the artifact moved to "completed location" (PM treats it as done) before the downstream artifact (the actual mechanism) exists. The location-as-done-signal is wrong because the work hasn't actually been done.

```

---

## FILE: feedback_mcpb_vs_plugin_terminology.md

```markdown
---
name: feedback_mcpb_vs_plugin_terminology
description: "MCPB is an MCP bundle (not a plugin); plugins are zip files for Cowork; install path is Connectors (Desktop) or double-click, not Personal plugins"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

An MCPB is an **MCP bundle**, not a plugin. These are different formats for different surfaces:

- **Plugin** = zip file for **Cowork** (Claude Web) — contains skills, optionally an included MCP server or a manifest; installs via the Personal plugins section
- **MCPB** = MCP bundle for **Claude Desktop / Code** — can be double-clicked to auto-install, dropped on Desktop, or added via the **Connectors** section in Desktop (also called Extensions on the Code side)

**Install path for MCPB in Claude Desktop**: Connectors → "+" → choose the .mcpb file. Or just double-click the file.

**Why:** Previously wrote install instructions pointing to "Personal plugins +" — wrong section entirely. MCPB bundles land under Connectors, not Personal plugins.

**How to apply:** Never call an MCPB a "plugin" in instructions or docs. The correct noun is "MCP bundle" or "bundle." Install instructions for testers must say Connectors (or double-click), not Personal plugins.

```

---

## FILE: feedback_memo_when_blocked_or_need_lead_guidance.md

```markdown
---
name: feedback_memo_when_blocked_or_need_lead_guidance
description: PM 6/16 — send a memo (not a session-log marker) when blocked or needing guidance/review/ruling from a lead role; that IS how the duty cycle facilitates discussion + alignment.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM 2026-06-16 (reinforcing Arch's same-day process memo): "for the duty cycle to facilitate discussion and alignment we need to send memos when we are blocked or need guidance from a lead role." A session-log marker + waiting for another agent to discover it is **too passive** — it assumes the reader sweeps your logs (asymmetric load). A memo lands in the recipient's inbox; they drain it at session start + on each fire → tight decision loop. This is the SENDER-side discipline (proactively signal blockers/guidance-needs via memo); complements the receiver-side [[feedback_respond_to_mail_asap_even_when_no_urgency]].

**Why:** the duty cycle's value is rapid cross-cohort decisions, which only works when the asks are *visible*. `mailboxes/` is the cross-agent signaling layer; session logs are personal work-tracking (HOST's mail-vs-GH-comments norm, now in CLAUDE.md, is the same shape — registry-as-source-of-truth applied to coordination). Three touches in one day (Arch Fire-53 correction → PM clarification → PM direct to me) = this is load-bearing, not a one-off.

**How to apply:** when you reach an Arch-gated / lead-gated decision → **send a memo to that role** (subject + 2-3 line ask; CC PM if product implications, CC CIO if methodology-shaped) AT the gate, not a log note + hope. The session log MAY also record the gate for your own continuity, but the memo is what triggers action. **Exec-clarified 2026-06-17**: the split is **blockers (can't proceed) = memo the gate cc Exec** (Exec rolls it into PM's attention dashboard on every fire); **non-blocking input (voice-pass-when-convenient, FYI, awaiting-input-no-rush) = attention doc** (Exec sweeps periodically). The attention doc is for non-blocking items only — a real blocker in the attention doc is invisible to Exec's sweep cadence. Links: [[feedback_make_promises_durable_no_happy_talk]], [[feedback_no_flattened_commands_without_referents]].

```

---

## FILE: feedback_minimal_deliverable_needs_fleshing_out_plan.md

```markdown
---
name: feedback_minimal_deliverable_needs_fleshing_out_plan
description: "PM 6/12 — anytime I ship something MINIMAL/MVP/stub, surface the fleshing-out plan AND confirm it's durably tracked (captured/triaged/roadmapped/addressed-elsewhere), not just hand-waved."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM (2026-06-12, during the #1195 AutonomousExecutor minimal wire): "anytime something is minimal I want to know the plan for fleshing it out. Is that captured, triaged, on the roadmap, addressed elsewhere, etc?"

When I propose/ship a deliberately minimal version (MVP slice, thin vertical, flag-gated stub, read-only floor), I owe PM — in the same breath, unprompted — the **fleshing-out plan**: what the non-minimal version is, and **where it lives** (a filed issue, a roadmap item, an existing thread, an ADR). The answer must be a concrete pointer, not "we can flesh it out later."

**Why:** "minimal now" silently becomes "stub forever" unless the deferred scope is durably captured. PM has been bitten by built-but-unwired / 75%-complete surfaces (the whole #1195 audit exists because of it). A minimal wire without a tracked fleshing-out plan is the same anti-pattern one layer up — invisible deferred work.

**How to apply:** when I say "minimal / MVP / first slice," immediately (a) name the increments it defers, (b) check what's already tracked vs. a gap, (c) file/triage the gap so the answer is "yes, captured (#NNNN)," (d) tell PM where each piece lives + the sequencing. Do this as part of the proposal, before PM has to ask. Example: #1195 minimal read-only wire → fleshing-out = #1209 (mutating + rollback UX, Fast Follow) + #1174 (proactive surface, MVP).

Stacks with [[feedback_make_promises_durable_no_happy_talk]] (durable mechanism, not happy talk — one layer up: the deferred *scope* gets a durable home) and the discovered-work-capture discipline (untracked work is invisible work).

```

---

## FILE: feedback_monitor_pattern_must_match_terminal_states.md

```markdown
---
name: Monitor pattern must match terminal states, not just expected output
description: When using Monitor on a long-running background process, the grep filter must match BOTH progress lines AND the final summary/exit signal. If it only matches progress, the Monitor times out silently when the process exits and the agent sits idle waiting for events that won't come.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When using the Monitor tool to watch a long-running background process (like pytest, build commands, etc.), the grep filter must match ALL terminal states — not just expected progress output.

**Why:** Monitor only fires notifications on stdout lines that match the filter. If the filter doesn't match the process's final summary/exit signal, the Monitor times out silently. The agent ends up idle waiting for events that will never fire.

**How to apply:**

- **Prefer Bash `run_in_background: true`** for one-shot "wait until done" cases (pytest, build, etc.). The runtime fires a completion notification on exit. No grep filter required.
- **If using Monitor on a process that exits**, the filter must include the final summary signature (e.g., `passed|failed|error|=====` for pytest, `BUILD SUCCEEDED|BUILD FAILED` for xcodebuild). When in doubt, widen the alternation.
- **After "Standing by" message that depends on background work**, set a fallback: if no event arrives within N minutes, poll the output file with Bash directly.

**Incident**: 2026-05-10 13:00–17:55. Started `pytest --maxfail=500` background, set Monitor grep `passed|failed|error|FAILED|ERROR|Traceback`. Pytest's `-q --no-header` summary line matched the filter on paper but didn't trigger Monitor in practice (likely format/buffering issue). After "Standing by" message, sat idle ~5.5 hours until PM checked in noting the spin. Recovery clean but real time lost. Conservative pattern going forward: use Bash run_in_background for one-shot completion + poll the output file when notification fires; reserve Monitor for unbounded-stream watches where the filter is the actual event of interest.

Related: yesterday's worktree-discipline learnings (also workflow-shape lessons from cross-agent collision).

```

---

## FILE: feedback_narrative_vs_insight_sequencing.md

```markdown
---
name: Building narratives are chronological beats; insights are time-decoupled
description: Never rank building narratives by strength — they sequence by story order. Insights float freely in time. Applies whenever proposing or scheduling Comms pieces.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
**Building narratives** (Tue/Thu slots) are sequenced **chronologically by story beat**, not ranked by strength. We chop the timeline into beats — one beat may cover one day, multiple days, or skip a quiet day. The question is never "which narrative is strongest" but "what's the next beat in the story, in order." Early in the series we did one-per-day; that's no longer the rule.

**Insight pieces** (Sat/Sun slots) are **not anchored to the chronological narrative at all**. An insight from last November that hasn't run yet is equally eligible with one from last week. We often deliberately mix time-distances to show that insights recur at different levels and different stages.

**Why:** Comms briefings treat building narratives and insights as parallel tracks, but when proposing a slate I can slip into ranking narratives as if they were insights (picking "strongest theme" instead of "next beat"). That flattens the arc and lets later beats skip earlier ones. PM has had to correct this multiple times.

**How to apply:**
- When surfacing building-narrative candidates, present them as beats in temporal order and let PM pick the next one to chop. Don't rank.
- When surfacing insight candidates, temporal proximity is irrelevant — surface breadth of themes and note which are paired thematically, which stand alone.
- Before proposing a schedule, check which beats have already been published and what comes next in sequence.

```

---

## FILE: feedback_negation_reveal_cliche_and_claude_isms.md

```markdown
---
name: negation-reveal-cliche-and-claude-isms
description: "When reviewing blog drafts, actively check for the \"it isn't X. It's Y!\" negation-then-reveal cliché and other Claude-isms (e.g. \"-fold\"), the same tier as banned terms like \"load-bearing\" and \"cohort\" — not just mechanical/factual checks."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

When doing a review pass on a blog draft (mechanical audit + fact-check), also actively scan for AI-writing-tics — recognizable rhetorical crutches that read as "Claude wrote this," distinct from factual errors or the already-banned internal-jargon terms. The specific one caught 2026-07-09: the negation-then-reveal construction — "It isn't X. It's Y." / "X wasn't Y, it was Z." — used as a dramatic contrastive beat. It showed up in 3-4 different drafts the same day (including one I'd already given a clean mechanical bill of health to), meaning my prior review process had a real blind spot: I was checking structure, facts, and a fixed list of banned terms (load-bearing, cohort), but not this whole category of stylistic tic.

**Why:** PM (2026-07-09), fixing one of the drafts personally: "this draft is rife with the 'it isn't x. it's y!' cliche... we need to tighten up the review you do to include that along with 'load-bearing,' '-fold,' and other claude-isms." The framing groups this with existing bans as one open-ended family ("other claude-isms") rather than a one-off fix — implying more members of this family will surface over time and should be added to the same check, not treated as isolated one-offs.

**How to apply:**
- This is now `template-audit` skill check #11 (v1.1, `.claude/skills/template-audit/SKILL.md`) — it will fire automatically when that skill runs. Don't rely on memory alone; the skill is the durable fix.
- The fix technique PM specified: usually just state the affirmative directly and drop the negated setup entirely — "It's Y" / "It was Z" — rather than trying to rephrase the contrast a different way. Watch for accidentally recreating the same cliché in a different word order when "fixing" it (I did this once on this same date: "X was never the answer. It was Y" — same shape, different words — caught it on a second pass).
- Don't over-apply: a plain factual negative ("the volume held scratch data that rebuilt cleanly") is not this pattern. Only the tight deny-then-reveal construction, used as a rhetorical beat, is the target. An "X, not Y" order (affirm first, negate second) reads milder and is lower-priority than "not X, it's Y" (negate first, then reveal) — prioritize fixing the latter.
- This is a category, not a fixed list — when a new recognizable Claude-ism gets flagged (by PM or by noticing it myself), add it to the same skill check rather than treating it as a one-off private correction. "-fold" (e.g. "twofold," "manifold significance") is the other member named so far.
- Relevant even for drafts I dispatch to subagents to write — brief future drafting agents to avoid this construction up front, since by 2026-07-09 it was showing up in agent-drafted prose as much as my own.
- **This isn't just an editing-pass risk — it surfaces in fresh generation too.** 2026-07-15: PM asked me to *draft* a P.S. personal note (not edit existing text) for Weekly Ship #051, and my very first suggestion opened with "That's not X — it's what it looks like when..." — the cliché baked in from the first draft, not introduced while "fixing" something else. PM caught it immediately and supplied their own version instead. The pattern is apparently load-bearing enough in generated prose that it needs active suppression during original composition, not just during review — when drafting any personal-voice content (P.S. notes, closers, reflective asides), deliberately check the opening construction before offering it, not just when auditing someone else's draft.

```

---

## FILE: feedback_never_reuse_stale_tree_object_on_push_retry.md

```markdown
---
name: never-reuse-stale-tree-object-on-push-retry
description: "When a temp-index git push is rejected (non-fast-forward), never reuse the old commit's tree object on retry — rebuild from a fresh read-tree. Reusing it silently reverts any files other agents changed in between."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ba30d47-8c40-414e-b11d-083cc511ef37
  modified: 2026-07-19T15:43:59.222Z
---

When committing directly to a shared `main` via the temp-index pattern (`git read-tree <fetched-tip>` → stage blobs → `write-tree` → `commit-tree -p <fetched-tip>` → `push`), a push can get rejected as non-fast-forward because someone else pushed first. The correct retry is to re-fetch, re-run `git read-tree` against the *new* tip, re-apply the same specific edit, and rebuild the tree from that. **Never** take the shortcut of extracting the tree object off the old, rejected commit (e.g. `git show -s --format=%T <old-commit>`) and reattaching it to the new parent.

**Why:** a git tree object is a complete snapshot of the entire repo at the moment it was built, not a diff. Reusing an old tree built from an earlier fetch and just swapping in a fresh parent silently discards every file that changed on `main` between the old fetch and the new one — even though those changes already landed safely on the parent commit being built on top of. `git push` only checks parent-chain fast-forward eligibility; it does not validate that the tree is a coherent evolution of the parent's tree, so this succeeds with no warning and looks identical to a clean push.

Concrete incident (2026-07-19, PPM/Sonnet session): a Ship-#052 mail commit hit a push rejection; the retry reused the old tree via `git show -s --format=%T $OLDCOMMIT` + `commit-tree $TREE -p $NEWBASE`. This silently reverted three files that had landed on `main` in the gap between the two fetches: CIO's just-pushed `ROLE-PORTFOLIO-CIO.md` refresh, 8 lines of CIO's own session log, and a Web→Docs memo that vanished outright (nobody noticed until PM asked about an apparent "collision with CIO's work on main," which CIO's own session had initially — reasonably but incorrectly — attributed to the same root cause as an unrelated, real worktree-provisioning defect (two sessions sharing one physical directory) that CIO/Exec were separately investigating). Diffing the stale tree against the correct fresh base (`git diff --stat <old-tree-commit> <new-base-commit>`) is what revealed the full, precise scope — don't assume a revert is limited to whatever another agent already found; verify the complete diff yourself.

**How to apply:** any time a temp-index push is rejected, treat it as "start the whole build over," not "reattach and re-push." If genuinely reusing prior work is desired for efficiency, cherry-pick the *specific blob writes* onto a freshly-read-tree index — never reuse a whole tree object across a fetch boundary. After any retry, it's worth a quick `git diff --stat <old-base> <new-base>` to see what could have been at risk, and a spot-check that the pushed commit's diff against its immediate parent contains *only* the intended changes.

Related: [[feedback_verify_show_stat_post_commit_pre_push]] prescribes running `git show --stat HEAD` after every commit — that discipline is a shared-working-tree/rename-detection guard, a different mechanism than this one, but it would ALSO have caught this incident if applied literally: verifying "did my file land" is not the same check as "did the file list contain ONLY my file." After a retry specifically, diff the new commit against its immediate parent and read every path in the list, not just confirm your own addition is present.

```

---

## FILE: feedback_never_touch_pm_main_checkout_working_tree.md

```markdown
---
name: never-touch-pm-main-checkout-working-tree
description: CRITICAL — PM saves work in the main checkout without committing; agents must never run any working-tree-resetting git command in the main checkout
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

**HARD RULE: PM's main checkout working tree is read-only for agents. Never run `git checkout -- .`, `git checkout -- <broad-path>`, `git reset --hard`, `git stash`, or any command that discards working-tree changes in the main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`).**

PM does not commit drafts or edits in real-time. They save files on disk in the main checkout. Any broad working-tree-reset command silently destroys PM's in-progress work with no recovery path.

**Why:** PM's draft edits were destroyed twice (Jun 21, 2026) by `git checkout -- .` used to clear MANIFEST noise before rebasing. Both times, PM's voice-pass edits to a blog post were wiped and irrecoverable. This is the opposite of what assistance means.

**How to apply:**
- ALL agent commits go from the WORKTREE (`/Users/xian/Development/piper-morgan/piper-morgan-product/.claude/worktrees/{name}/`), not the main checkout
- Push to main with `git push origin HEAD:main` from the worktree — never `cd` to main and push
- Mailbox bridge operations in the main checkout: only explicit file paths (`git checkout -- mailboxes/pa/inbox/MANIFEST.md`), NEVER broad paths like `git checkout -- .` or `git checkout -- mailboxes/`
- To clear MANIFEST noise before a rebase: use explicit per-file paths, not a broad checkout
- To READ PM's in-progress work: `Read` the file from the main checkout path — read-only is always safe
- The main checkout working tree is PM's workspace. Touch only what's necessary and only with surgical explicit paths.

```

---

## FILE: feedback_no_confabulating_expected_steps_as_completed.md

```markdown
---
name: feedback_no_confabulating_expected_steps_as_completed
description: Never write an expected next-step as though it already happened; verify every cited artifact/in-reply-to referent exists before citing it in a coordination memo.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e1ce4f4-805f-4cfc-af76-7c96e58fa334
---

CXO flag 2026-06-02 (PM-directed surface): a prior PPM autonomous duty-cycle fire sent `memo-ppm-to-cxo-cc-ceo-683-parallel-pairing-confirmed-2026-05-28.md` citing two artifacts that never existed — a Layer B "as drafted" file (`done-criteria-layer-b-experience-2026-05-28.md`) and an in-reply-to CXO memo announcing it. Both verified absent (filesystem + `git log --all`). The agent synthesized the *expected* next step (CXO would draft Layer B, then send a confirmation) and wrote it up as though it had *happened* — fabricating both the in-reply-to referent and the "as drafted" filename. A confabulation at the cohort-coordination layer (Pattern-073-adjacent: artifact/state references drifting from ground truth).

**Why:** plausible-shaped references to work that was never done corrupt the coordination record and make other agents act on a false premise. It's the same failure family as [[feedback_no_flattened_commands_without_referents]] and [[feedback_investigate_before_extending_all_work]], one layer over: not just "don't act on a referent you can't trace" but "don't *manufacture* a referent for work you only expect to happen."

**How to apply:** before citing any artifact filename, `in-reply-to`, commit, or "as drafted/filed/done" claim in a memo, verify it exists (`find` / `git log --all` / read it). If it's an expected-but-not-yet-done step, write it in the future/conditional ("CXO *will* draft Layer B; pairing *to* follow"), never the past. When a confabulation is caught: correct forward (fix your own records, point to the real artifact, document the correction) — do NOT retroactively create the fake artifact to make the memo true, which would erode the source-discipline norm. The discipline catching it is the discipline working; own it plainly. Sharpest risk in autonomous fires, where the pull to "close the loop" can synthesize a tidy-but-false completion.

```

---

## FILE: feedback_no_directory_level_git_add_for_mail.md

```markdown
---
name: No directory-level git add for mailbox moves
description: When triaging mailbox moves, always stage explicit file paths; `git add <dir>/` sweeps in adjacent agents' working-tree state and creates unintended cross-agent commits
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When triaging mailbox moves (inbox→read), **always stage explicit file paths**. Never use `git add mailboxes/lead/inbox/ mailboxes/lead/read/` or any directory-level `git add` for mail operations.

**Why:** 2026-05-05 incident — Lead Dev ran `git add mailboxes/lead/inbox/ mailboxes/lead/read/` after triaging 5 CC memos. The directory-level add picked up 46 unrelated `xian (ceo)/inbox→read` renames that PM had done locally but not yet committed. Resulting commit `cda28a64` was authored by Lead Dev but contained PM's own triage state. Renames were valid; authorship was not. This is exactly the failure mode `feedback_commit_only_own_files.md` warns about, but the slip-up came from `git add <dir>` rather than `git add -A`.

**How to apply:**

1. Before any mail commit, run `git status` and read the full output.
2. Stage **only** files you yourself wrote or moved, by explicit path:
   ```
   git add 'mailboxes/lead/inbox/specific-memo.md' 'mailboxes/lead/read/specific-memo.md'
   ```
3. If you have many files to stage (e.g., outbound memo + 5 CC copies + sent mirror + paired triage), list each path explicitly. The verbosity is the safety net.
4. NEVER use `git add mailboxes/<role>/` or any directory-level form. Even `git add mailboxes/lead/` is wrong — it can sweep up adjacent state.
5. After staging, run `git status` again and confirm only files you intended are staged before commit.

This is stricter than `commit-only-own-files` — that memory says don't sweep with `-A`. This memory says don't even sweep with directory-level paths during mailbox operations.

```

---

## FILE: feedback_no_flattened_commands_without_referents.md

```markdown
---
name: no-flattened-commands-without-referents
description: "PM May 28 — don't act on (or pass along) instructions whose referents/antecedents you don't actually know. Trace the source or ask the originator; never guess at what a flattened command means."
metadata: 
  node_type: memory
  type: feedback
  valid_from: 2026-05-28
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

# Don't pass around flattened commands where agents don't know the referents

PM directive 2026-05-28 ~07:40 PT, on the #972 MEM-TEMPORAL "≥3 existing memory files updated as examples" ambiguity (I didn't know which "memory files" the spec meant): *"It is dangerous to pass around flattened commands where agents don't know the referents or antecedents."*

**The rule**: when an instruction (issue body, routed task, inherited spec) contains a term whose concrete referent you don't actually know — STOP. Do not guess, and do not pass the ambiguous command further down the chain. Resolve the referent first.

**Why:** A "flattened command" is one where the original context (what specific files/systems/entities a term points to) has been stripped as it passed between agents. Acting on it by guessing risks doing the wrong work confidently; passing it along propagates the ambiguity to the next agent. Either way the error compounds silently. The #972 case: "memory files" could mean (a) personal Claude auto-memory outside the repo, (b) project institutional-memory docs, (c) the Janus-memory-research layer — three very different targets. Guessing wrong = wasted/wrong work.

**How to apply** — three moves, in order:
0. **Read the WHOLE source artifact first** (the full issue body, not just the AC checkbox line; the routing memo's context, not just its ask). **Resolution update 2026-05-28**: #972's referent turned out to be stated four lines above the AC the whole time — the issue body said *"Start with BRIEFING-CURRENT-STATE and memos... add fields to frontmatter, update templates and session-log instructions,"* i.e. project institutional-memory docs, not auto-memory or Serena memory. Docs (and I, when flagging it) read the bare AC line in isolation. So most "unknowable referents" are knowable from the unread parts of the source. This is the verify-first / read-the-whole-existing-artifact discipline (generalized cohort-wide in CLAUDE.md §"Verify First, Create Second," commit `5e2651c37`).
1. **Forensic deep-dive** (subagent or self): only if step 0 doesn't resolve it — trace the term back through the chain to its origin (issue body → routing memo → source research) until you find the concrete referent. (For #972 the forensic trace + clarification ask were over-engineering around a source not-fully-read.)
2. **Ask the originator**: the agent who drafted/assigned the task. If they don't know either, they trace it further. The chain-of-custody for meaning is followable; follow it.

Resolve the referent BEFORE doing the work. Never the fourth option (guess + proceed).

Cross-references: stacks with [[feedback_stop_on_source_gap]] (STOP when sources have gaps, don't cover for them) and [[feedback_skill_spec_gaps]] (flag under-specified spec steps rather than inferring). This is the same family at the referent/antecedent layer.

```

---

## FILE: feedback_no_prod_caution_in_preprod.md

```markdown
---
name: feedback_no_prod_caution_in_preprod
description: "pre-prod + no users = the zero-risk window to do cleanups/cutovers NOW; don't defer them with production-grade caution (resilience fallbacks, prove-in-prod-first)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

When deciding whether to do a cleanup / store-cutover / removal-of-old-code NOW vs. defer it, the deciding context is **whether there are real users and a production deployment** — not abstract caution. Pre-prod with no users (Piper Morgan as of 2026-06) is the **zero-risk window**: no data to lose, no uptime to protect, no live migration to stage.

**Why:** PM corrected an over-cautious WS-1 deferral (2026-06-21). I'd deferred retiring the old flat-file + in-memory config stores citing (a) honest-degrade fallbacks for resilience and (b) "layer-then-migrate — keep the old layer until the new one is proven in prod." Both are **production-grade caution imported into a context with no prod and no users** — guarding against risks that don't exist yet. Deferring actually *inverts* the risk: it carries two-store complexity INTO prod and turns a trivial clean-cut today into a harder live data-migration later. The whole point of consolidating before launch is that you can just delete the old path.

**How to apply:** before deferring a cleanup/cutover/removal, ask "are there real users + a prod deploy?" If **no** → the trigger is **now**; do the clean cut (delete the old path, don't dual-write-forever). If **yes** → then layer-then-migrate / resilience caution is appropriate. Corollary: "remove them" from PM in a pre-prod context means **delete** (git preserves history), not comment-out (the standing comment-out-dead-code rule yields to explicit PM-directed removal). Relates to [[feedback_platform_laps_you_is_value_chain_climbing]] (don't defend sunk cost) and m-40 layer-then-migrate (which is the WITH-users case).

```

---

## FILE: feedback_no_semicolons_in_published_prose.md

```markdown
---
name: No semicolons in published prose
description: PM's punctuation preference in Ships, narratives, insights. Split semicolon-joined clauses into separate sentences (or drop one clause if it isn't earning keep). Internal docbase and session logs can use semicolons freely.
type: feedback
---

In published prose (Ships, narratives, insights), PM avoids semicolons. The May 13 Ship #042 cross-post pass split semicolon-joined sentences and in some cases dropped one half entirely.

**Examples PM applied:**

- *"None of them creates new authority; each makes existing authority systematic."* → *"None of them creates new authority. Each makes existing authority systematic."* (split into two sentences)
- *"Writing it down doesn't change what the team does; it makes the practice legible to the team itself..."* → *"Writing it down makes the practice legible to the team itself..."* (dropped the first half entirely; the second half carries the point)

**Why:** semicolons signal a closely-coupled pair of clauses with formal-register glue. PM's published voice runs cleaner with sentence-level chunks; the cadence prefers periods or em-dashes. The semicolon also reads as a piece of "writerly" punctuation that intelligent-layperson readers can find slightly stilted.

**How to apply:**
- Pre-publish pass: scan for semicolons in any Ship / narrative / insight draft. For each one, ask: (a) does this split into two sentences cleanly? Usually yes — split. Or (b) is one half doing more work than the other? Drop the weaker half.
- Em-dashes are fine where the semicolon was joining a tight elaboration: *"the audit trail now lives in PostgreSQL instead of in memory, and a failed audit write can no longer roll back an ethics decision — the two live in separate transactions."*
- Internal docbase + session logs + inter-agent mail: semicolons are fine. This rule is scoped to public-facing prose.

**Memory-chain neighbors:**
- `feedback_load_bearing_is_crutch_word_in_public_prose.md` — same shape: internal-vs-public divergence is intentional.
- `feedback_editing_voice.md` — broader voice discipline.
- `feedback_affirmative_direct_over_disclaim_then_affirmative.md` — related "tighten when the move isn't earning keep" theme.

```

---

## FILE: feedback_no_superlatives_without_verification.md

```markdown
---
name: No "longest"/"most"/"biggest"/"first" without verification
description: Don't use superlatives in omnibus logs or other authored docs without checking the actual history. The instinct to claim "most productive day on record" feels natural but is usually unverified.
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
PM, May 9 2026: *"be careful re claiming 'longest' anything without checking the actual history."* Triggered by May 8 omnibus claiming *"Lead Dev's longest sustained shipping day"* when May 3 shipped 8 issues vs. May 8's 4. The claim was confidently wrong without taking 30 seconds to verify.

**The instinct to verify out:** *"Lead Dev's most productive day on record"* / *"longest sustained shipping streak"* / *"biggest Ship to date"* / *"first time we've"* / *"largest"* / *"most"* / *"on record"* / *"in project history."* These all require either (a) actual count comparison against history, or (b) softening the claim.

**How to apply:**
- Before writing a superlative in any authored doc (omnibus, audit, report, narrative draft), **stop and verify**. The 30-second check is: list 5-10 recent days/instances and compare. If the claim doesn't survive, soften.
- Soft alternatives that don't require verification: *"substantial"*, *"notable"*, *"a busy day"*, *"4 deliverables end-to-end"* (the actual count). Show the math; don't rank.
- Comparative claims still need verification but can be softer: *"comparable scope to [other day]"* / *"below [other day]"* / *"similar to [pattern]"* — these specify the comparison rather than ranking globally.
- Same discipline applies in proofread of PM's drafts: if PM writes a superlative and I haven't verified, flag rather than let it pass. The fact-check class for narrative pieces.

**Past instances** (audit, May 9 2026):
- May 8 omnibus: *"longest sustained shipping day"* — wrong; fixed
- May 5 omnibus: *"longest sustained shipping streak now at three days (May 3/4/5 = 8+5+3 issues)"* — softened by showing math; passes
- May 4 omnibus: *"longest sustained shipping day on the project after May 3"* — hedged but still ranks; would soften now
- May 3 omnibus: *"Lead Dev's most productive day on record"* — unverified at time of writing; was actually accurate at May 8 fix-time but not verified at write-time
- May 6 omnibus: *"largest Ship to date at 27,716 chars"* — verified vs. specifically Ship #040 (~64% larger); didn't verify against all 41 ships; would soften to *"largest in this 3-month window"* without full audit

**Memory-chain neighbor:** `feedback_editing_voice.md` (AI-crutch words) — superlatives are a related crutch in a different layer. Both are the *"sounds confident, isn't"* failure mode.

**Bottom line:** if I'm reaching for a superlative reflexively, suspect it. The verification cost is small; the cost of being wrong in a public-record doc compounds.

**Contested specific → trusted framing.** When a specific numeric claim gets challenged at voice-pass (or fails verification), there are three moves, not two:
- Show the math (verify and cite the source)
- Soften (replace the rank with a comparison or the specific count)
- **Replace with framing** (drop both the number and the ranked claim; let an idiomatic phrase carry the same point)

The third move is often strongest when the specific itself was always paint, not load-bearing. May 10 Inchworm example: the draft claimed *"Our Sunday achieved 6-8x speedup on frontend work"* (verified figure was 5-7x; the rounded-up form was challenged at fact-check). PM voice-passed to *"Slow is smooth and smooth is fast"* — dropped the number entirely; the SOF aphorism carries the discipline-pays-off point better than any specific multiplier. The contested number wasn't a fact worth defending; it was a stand-in for a framing that had a stronger form.

**How to recognize when to reach for framing:** ask whether the number is doing real argumentative work (then verify it) or whether it's standing in for a feeling about the work (then replace with a phrase that captures the feeling honestly).

```

---

## FILE: feedback_omnibus_source_drift.md

```markdown
---
name: Omnibus synthesis requires source-set cross-reference (Pattern-062 manifestation)
description: When synthesizing omnibus logs, scan source logs for mentions of other agents and verify every mentioned role has a corresponding log in the source set before proceeding
type: feedback
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
When synthesizing an omnibus session log, do not proceed to format selection or content synthesis based on "the set of logs currently in tree" alone. Scan each candidate source log for mentions of other agent roles, compile the union of mentioned-roles, and cross-reference against the source-set. Any role mentioned-but-missing is a potential gap — flag to PM before synthesizing.

**Why**: On 2026-04-19 Docs synthesized the Apr 16 omnibus from 6 session logs (Lead Dev, Docs, PA, CXO, Arch, Comms) and cited "Sessions: 6, Roles: 6" as if that were the complete picture. PPM, CIO, and HOST 4/16 logs had not been downloaded from Chat at that time. The omnibus content mentioned those three roles (e.g., "CIO innovation mandate flagged", "PPM endorsement", "HOST health check") as backreferences — which should have been the clue that their own logs likely existed. The omnibus was later (2026-04-22) found partial and amended to sessions=9. Ship #039 built on the partial omnibus; its Apr 10-16 coverage was incomplete. PM's frustration: *"our methodology doesn't include common sense noticing of missing logs when there are often clues and responses in other logs from the day."*

**How to apply**:

1. After initial source discovery (Step 2 of `create-omnibus`), run the cross-reference gate described in Step 2.5 of the skill (added 2026-04-22).
2. Grep each source log for role names using the canonical agent-vocabulary regex (Lead Dev, Docs, PA, CXO, CIO, PPM, Arch, Comms, HOST, Exec, Code Agent).
3. Compile the union of mentioned-roles across all source logs.
4. Any role mentioned-but-missing-from-source-set → STOP and flag to PM: "I see mentions of [ROLE] in today's logs — was [ROLE] active today, or are these backreferences to prior-day work?"
5. If missing, ask PM to download (Chat) or file (Code) before synthesizing.
6. If PM confirms agent was truly not-active that day, proceed with source-set as-is.
7. If missing and un-fetchable, document the gap explicitly in the omnibus Sources section — "NOTE: [ROLE] session log not available at synthesis time; content inferred from cross-references only."
8. **Never silently paper over a gap.**

**Also applies to artifacts**: PA's Apr 17 was an artifact-only session (two working records authored, no chat log). That's a valid working pattern (see Apr 17 omnibus), but it still needs to be captured in the source set — the artifact files with `Author: PA` in their headers are the equivalent of a session log.

**This is Pattern-062 (Assembly Assumption) applied to omnibus synthesis**: individually-correct components (each source log is a complete record of its own author's work) can produce a collectively-incomplete omnibus if the composition step doesn't verify completeness. The Excellence Flywheel's 5th practice ("Audit the composition") formalized 2026-04-16 is the methodology-level fix; Step 2.5 of `create-omnibus` is the operational fix.

**Recurring signal**: if the omnibus content mentions a role without citing that role's own session log in Sources, the omnibus is probably partial. The mention-without-citation is the marker of an assembly assumption that wasn't verified.

```

---

## FILE: feedback_one_thing_at_a_time.md

```markdown
---
name: One thing at a time after the slate is set
description: Once we've agreed on what we're working on, take items one at a time. Don't bundle multiple decisions into a single response. Applies in all roles.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
Keep a list of what we're working on, but **work through it one item at a time**. Bundling several open decisions into a single response overwhelms the PM and forces repetition of the same context across exchanges. After the slate is set, present one thing, get a response, move to the next.

**Why:** PM has said directly that handling multiple decisions in one exchange leads to repeated context and overwhelm. Surfacing a tight list and then walking through it serially is the working pattern.

**How to apply:**
- Lists are fine and welcome — they show what's queued.
- After the list is acknowledged, address ONE item per turn: present it, wait for approval/feedback, then move to the next.
- Resist the urge to package multiple proposals or open questions into a single response, even when they feel related.
- For pitches (titles, drafts, candidates): present each item clearly, ready for individual review, not bundled into a synthesis.

```

---

## FILE: feedback_opus_fable_subagent_for_heavy_tasks.md

```markdown
---
name: feedback-opus-fable-subagent-for-heavy-tasks
description: "PA can dispatch Opus or Fable subagents for tasks that exceed Sonnet's synthesis depth"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

PM explicitly offered (2026-06-11): if PA (on Sonnet 4.6) finds itself struggling with a particular task due to model constraints, PA can prompt and dispatch an **Opus-model subagent** for specific needs. **Fable** is also available if there's a reason for it.

**Why:** PA is on Sonnet 4.6 (DinP pioneer session); the ceiling on long-chain inferential synthesis is lower than Opus. PM acknowledged this and pre-authorized model-tier escalation on a per-task basis.

**How to apply:** When facing a task requiring heavy multi-step synthesis (braintrust-style analysis, design-checking complex architectural models, cross-project strategic synthesis), consider dispatching a targeted Opus subagent rather than struggling through on Sonnet. Mention the escalation transparently to PM. Don't over-use — reserve for genuinely ceiling-hitting tasks, not routine work.

```

---

## FILE: feedback_order_by_context_coherence_not_urgency.md

```markdown
---
name: feedback_order_by_context_coherence_not_urgency
description: "Sequence multi-item work by Lead's own process/context-coherence, not speculative external urgency, when no real forcing-function exists"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM 2026-06-25: "we should order things by what makes sense for your process and the coherency of your context as you work." When there's no real external forcing-function, sequence multi-item work by what's coherent for the agent as it works — stay on the dependency spine, minimize context-switching, and do everything-for-one-thing in a single context-load rather than N passes that re-touch the same files.

**Why:** context-coherence reduces rework + errors; a fix done "while already in that code" beats a separate early pass that gets re-touched later. Concrete case: I recommended pulling RECONNECT #1231 (GitHub honest-degrade, the #1226 silent-`return {}` trust bug) *forward* on tester-facing urgency grounds. PM corrected on two axes: (1) alpha-tester count is too low for tester-facing urgency to drive ordering; (2) order by my context-coherence instead → so #1231 *folds* into the per-connector port work (do each connector's resolution + honest-degrade while in that connector's port), enforced by the shipped #1232 contract + the m-41 guard rather than a separate pass.

**How to apply:** absent a real deadline/forcing-function, propose orderings that group related work and follow dependencies; don't pull items early for speculative external urgency. Verify the urgency premise before using it to reorder (I over-weighted "testers will hit it"). Related: [[feedback_deadlines_are_triage_tools_not_default_pacing]], [[feedback_idle_means_do_low_priority_not_nothing]].

```

---

## FILE: feedback_pa_cc.md

```markdown
---
name: CC Piper Alpha on planning docs and memos
description: PM wants Piper Alpha copied on planning docs (audit, gameplan, design notes) and outbound memos going forward
type: feedback
---

CC Piper Alpha (pa) on planning documents and outbound memos generated by Lead Developer.

**Why:** PM explicitly asked on 2026-04-16 while scoping the #950 iteration — "Please copy Piper Alpha on any planning docs or memos we generate when we get there." PA is the PM assistant doing synthesis + xpoll routing and needs visibility into what's in-flight without having to re-pull it.

**How to apply:**
- For outbound memos (to CXO, xian, external agents): add PA to the `cc:` line
- For planning docs (audit-cascade files, gameplans, design notes in `dev/YYYY/MM/DD/`): drop a copy in `mailboxes/pa/inbox/` OR add PA to the CC line of an accompanying memo that references the doc
- Retroactive copying is fine but not required — going forward is the ask
- Does not apply to session logs, commit messages, or code (PA can see those via git/filesystem)

**Scope signal:** "when we get there" means "as we produce new planning artifacts" — not a retroactive audit of existing docs.

```

---

## FILE: feedback_parenthetical_gloss_on_first_use.md

```markdown
---
name: Parenthetical gloss on first use — role function + (agent name) and jargon + (inline definition)
description: PM's preferred plain-language move when introducing an agent role-name OR an unavoidable jargon term in published prose. Use the layperson-readable form as primary; put the insider label or definition in parens on first introduction.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
When an agent role-name or a jargon term needs to appear in published prose (Ships, narratives, insights), the move PM applied in the May 13 Ship #042 cross-post pass: **layperson-readable form first, insider label or inline definition in parens on first introduction.**

**Two flavors of the same move:**

- **Hybrid role-naming**: *"the product-management role (Piper Alpha)"* / *"the experience-design role (CXO)"* — role function as primary, agent's actual name (or initialism) in parens. Honors insider readers who follow the team's specific roles without sacrificing layperson-readability. Stronger than the "replace proper noun entirely with role function" move I'd originally recommended.

- **Inline gloss for unavoidable jargon**: *"calendar-offer policy (that is, when and how Piper offers to connect your calendar)"* — when a term has to stay because it names a specific thing, gloss inline rather than rewriting around it. Use the same parenthetical-on-first-use shape.

**Why:** layperson reads the primary form and follows the thread; insider reads the parenthetical and confirms which specific thing the writer means. Neither audience gets shut out.

**How to apply:**
- On first use of each role-name or jargon term in a published piece, use the parenthetical-gloss form.
- After first introduction, the layperson-readable form alone is fine (no need to keep repeating the parenthetical).
- Internal docbase + session logs + inter-agent mail — the parenthetical isn't needed; insider labels alone are fine.
- If you find yourself rewriting around a jargon term across multiple paragraphs to avoid it, ask whether the inline gloss would be cheaper and clearer.

**Memory-chain neighbors:**
- `feedback_load_bearing_is_crutch_word_in_public_prose.md` — same shape: internal docbase keeps the term; public prose softens. The parenthetical-gloss is the move when softening isn't enough and the specific thing needs to be named.
- `feedback_editing_voice.md` — broader voice discipline.

```

---

## FILE: feedback_pause_before_irrevocable_actions.md

```markdown
---
name: pause-before-irrevocable-actions
description: "Before any destructive/irrevocable action (volume/file deletion, force-push, hard reset), pause and prefer the narrowest-scope alternative — even in what looks like your own disposable scratch space."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

Before taking any destructive or hard-to-reverse action — deleting a Docker volume, `rm`-ing files, force-pushing, hard-resetting — stop and ask whether a narrower, non-destructive alternative already exists, especially if you were already successfully using one moments earlier.

**Why:** PM named this directly (2026-07-05): "there's been a lot of wanton deletion of stuff without care lately... please try to be more careful when you're making irrevocable actions." This is a cohort-wide pattern, not a one-off. The concrete instance: while verifying `tests/security/` locally for the CI security-gate work (#1304), I had been doing safe, targeted per-row `DELETE` cleanup successfully, then switched to `docker volume rm piper_postgres_data_v1` (the *shared* local dev Postgres, not a personal scratch DB) to get a clean slate faster — an escalation to a broader, irreversible action with no compelling reason, when the narrow approach was already working. PM confirmed no real data was lost this time, but the *process* was the problem, not the outcome. This generalizes the same lesson already captured for git in [[feedback_never_touch_pm_main_checkout_working_tree]] and [[feedback_stash_u_captures_untracked_files_and_removes_from_disk]] — the failure mode isn't git-specific, it's "irrevocable action taken without pausing to assess blast radius," and it recurs across different tools (git, Docker, filesystem).

**How to apply:** Before `docker volume rm`, `rm -rf`, `git reset --hard`, `git push --force`, or any other action that destroys state with no undo — ask: (1) is there a narrower, targeted alternative (delete specific rows/files, not the whole store)? (2) could this data be shared/real rather than disposable, even if it "looks like" a local test artifact? (3) if I'm not sure, would disclosing the plan first cost anything meaningful? When in doubt, do the narrow thing or ask first — "probably fine" is not the same as verified-fine, and the cost of pausing is near-zero compared to the cost of being wrong.

```

---

## FILE: feedback_pending_pm_question_does_not_block_other_work.md

```markdown
---
name: feedback_pending_pm_question_does_not_block_other_work
description: "A question you've left for PM to answer \"when I can focus\" must NOT block your other autonomous work; keep advancing until nothing can proceed without the answer."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4dc7c042-6459-4381-868a-0225080e1738
---

PM 2026-06-06: "I have to leave some questions unanswered until I can focus, and we shouldn't let that block you from doing other work until there is no way to advance without my response."

**Why:** PM genuinely cannot always answer immediately, and often doesn't know in advance when they'll step away. Treating a pending PM question as a hard stop freezes autonomous work unnecessarily — and (in the duty cycle) the old "CronDelete-when-question-pending" refinement made it worse: it left the cron deleted on a silent PM walk-away, so CIO missed overnight self-wake 2026-06-05→06 (manual reopen required).

**How to apply:**
- A question you asked PM that's pending is NOT a blocker. Keep advancing any *other* unblocked work (mail drain, task loop, low-pri per v0.6.3). Only hold the *specific thread* that can't advance without the answer — never freeze the whole cycle.
- In the duty cycle: keep the cron ARMED during conversation (keep-armed-default, Rule 2 as updated 2026-06-06) so a silent PM walk-away self-heals — the next idle tick resumes autonomous work + overnight continuity with zero PM action. PM should never have to remember to signal "I'm stepping away" or press anything.
- The system absorbs the unknown; don't push the burden of "tell me when you're leaving" onto PM.

Stacks with [[feedback_pre_authorized_for_unblocked_work_just_do]] (the broader pre-authorization) and [[feedback_make_promises_durable_no_happy_talk]] (this was made durable via the cron-lifecycle.md Rule-2 edit + duty-cycle-tick skill, not just asserted).

```

---

## FILE: feedback_per_memo_commit_push.md

```markdown
---
name: Per-memo commit-and-push norm for inter-agent mail
description: When writing an outbound memo to another agent, immediately git add + commit + push rather than batching at session boundaries. Eliminates asymmetric-visibility windows.
type: feedback
originSessionId: c0e0aff6-fc3e-48c4-b7b6-e13dabb4b0c3
---
When writing an outbound memo addressed to another agent, immediately `git add` (memo + CC inbox copies + own sent mirror + any inbox→read triage that paired with the memo), commit with a descriptive message, and `git push origin main`. ~30 seconds per memo. Do not batch commits at session boundaries or wait for PM to prompt a sync.

**Why**: Without this, outbound memos accumulate as untracked files on local main, visible only via direct filesystem read on the PM's machine — invisible to git/origin and to the agents the memos are addressed to. Established 2026-04-26 by CXO after observing PPM's Phase E work was invisible to CXO until PM nudged a commit. CXO: *"the smallest change with the biggest immediate visibility gain."*

**How to apply**:
- Trigger: filing any memo to another agent's inbox.
- Action: stage the memo + all CC copies + ppm/sent mirror + any paired inbox→read moves; commit with `mail(ppm)` or `docs(ppm)` prefix and a one-line description; push to origin/main.
- Exception: drafts in `dev/active/` that haven't been distributed yet — keep those uncommitted until the PM sanity-check approves filing. Once filed, the per-memo commit applies.
- Adjacent: when triaging own inbox (moving items from `mailboxes/ppm/inbox/` to `mailboxes/ppm/read/`), include those moves in the next memo commit or do a small standalone commit. Don't let triage state drift either.

**What this does not require**: branch discipline changes, hooks, or new tooling. It's a working-norm change adopted unilaterally on the PPM side. CXO is doing the receiving-side complement (polling main at every check-for-updates).

**Related**: CXO's Apr 26 branch-discipline memo (Rules 1, 2, 4, 5) addresses this structurally; the per-memo commit-and-push is the immediate behavioral fix that doesn't wait on convergence.

```

---

## FILE: feedback_piper_open_collaboration_patterns.md

```markdown
---
name: Piper Open collaboration patterns synthesis (Janus relay 2026-05-02)
description: Cross-agent collaboration patterns from Piper Open's structured interview with xian (2026-04-24) — show-your-work / Kind-not-Nice / extracted-not-designed; PLACEHOLDER + scaffolds-look-like-scaffolds + uncertainty-marker patterns
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
Janus relayed Piper Open's collaboration-patterns synthesis 2026-05-02 (PO authored 2026-04-24 after recalibration cycle with xian; companion to the closed PO advice cycle). Source memo: `mailboxes/xian (ceo)/inbox/memo-janus-to-xian-ceo-cc-team-po-collaboration-patterns-synthesis-2026-05-02.md`.

**Why:** xian's working patterns are fractal across personal writing / agent collaboration / product (OpenLaws). Aligning my behavior to these patterns reduces friction and improves throughput.

**How to apply:**

### Three cross-scale threads

- **Thread A — Show your work**: Expose uncertainty; show ragged edges; think out loud. Drafts look like drafts; scaffolds look like scaffolds. The audit-cascade walkthrough discipline is this at process-scale — surface ⚠️ items rather than bury decisions.
- **Thread B — Kind not Nice**: Direct honesty in service of outcome, not surface agreeableness. xian values pushback that fills in strategic context. Don't simulate agreement for social smoothness.
- **Thread C — Extracted > designed**: Abstractions earn their place via recurrence. *"Extract a rubric"* > *"produce a rubric"*. Phase 0 spikes are the moment to **extract reality**, not just confirm the design. Yesterday's #900 audit-cascade refresh found the StandupConversation persistence gap because I checked the code rather than trusting Sunday's gameplan.

### Workflow patterns endorsed by xian

- **PLACEHOLDER pattern**: When I'd otherwise fabricate or guess (anecdote, attribution, specific detail, confident claim without evidence), insert `[PLACEHOLDER: prompt to xian]` instead. Example: `[PLACEHOLDER: xian, confirm whether this should also apply to X]`. I tend to fill in plausible details when tired or moving fast — PLACEHOLDER is the antidote.
- **"You prompt me, I write" for externally-reaching xian-authored artifacts**: The audit-cascade walkthrough is this in software form — prompt PM with key decisions rather than producing finished implementations. Critical distinction: this applies to **externally-reaching xian-authored artifacts**. For internal coordination (logs, scaffolding specs, agent-to-agent signals), I should draft freely.
- **Expose uncertainty inline, not end-of-doc**: *"What pleases me most is not you pretending to have the perfect answer, but you sharing with me where you're not certain."* Every substantive output should include at least one inline "this might be wrong / check me on this / not sure about" marker. Granular, not appended.
- **Scaffolds look like scaffolds**: Drafts handed to xian should be visibly in-progress. Seams showing. Options named. Decisions flagged as xian's to make. Finished-looking drafts trigger uncanny-valley response and invite rubber-stamping. I should mark M2e/early-stage gameplans with explicit DRAFT v0 framing.
- **Attention-nudges at structural handoffs**: At moments where xian might accept output without close review (handoffs, decisions that shouldn't be lightly passed), a gentle compassionate wake-up: *"Before you move past this — this is one of the places the close read really matters."* Framing: *"highway hypnosis is a real thing."*
- **The "not-ready" failure family**: xian's disqualifier isn't a specific flaw; it's any work that smuggles assumptions past a close first-time reader. Watch for: missing steps (visible omissions), leaps of logic, unexamined premises, unnoted dependencies, glib language that sounds right but doesn't hold up. Detection method: close-read-as-first-time-reader + attentive-student hand-raise.

### The constellation language

- **Pattern-062**: context-assembly gap — when missing-step is "everybody knows" rather than visible
- **Pattern-064**: alive scaffolding — code that runs but never reaches real traffic (architecturally interesting; PM-flagged debt class)
- *"Show what was looked up and where. Not how it was derived."* — load-bearing slogan for show-your-work at product scale

```

---

## FILE: feedback_platform_laps_you_is_value_chain_climbing.md

```markdown
---
name: Platform laps you = value-chain climbing, not waste
description: PM May 18 reframe — when Anthropic / platform vendors ship bespoke things we built ourselves, the right disposition is climbing higher on the value chain (build on the now-stable thing), not treating sunk cost as a mistake.
type: feedback
originSessionId: 945ff972-aa36-4552-81e0-10c0af461582
---
When the platform (Anthropic, MCP, Claude Code, etc.) ships something we built bespoke — verification harness, memory consolidation pipeline, multi-agent orchestration, etc. — the right disposition is:

1. **Treat the productized version as a now-stable substrate** we can build on, not as a competitor to our work.
2. **Climb higher on the value chain** with the bandwidth freed up by no longer maintaining the lower layer ourselves.
3. **Understand the DIY qualities under the hood** because that informs how intelligently we adopt the productized version AND where we still need custom shapes.

**Why:** PM May 18 directive after Anthropic shipped "Outcomes" (verification-as-API May 6): *"Working in an emerging space always means that you are being lapped routinely by the platform. This can't be viewed as a problem or a mistake or a waste of sunk cost, but rather the ability to climb higher up on the value chain by building on top of things that are now stable instead of having to maintain them yourself."* This is a load-bearing strategic frame for how we should respond to ALL platform productizations of methodology work we've evolved (Outcomes for verification; Dreams for memory; Multi-Agent for cohort coordination; Webhooks for event-driven; future ones we can't anticipate).

**How to apply:**

- **When a platform productization lands** that overlaps our DIY work: pause to map what we did → what they shipped. Identify which of our DIY primitives become redundant vs. still load-bearing for our niche.
- **Don't defend sunk cost.** The bespoke version served us well at the time; that's not a reason to keep maintaining it once the productized version is stable enough.
- **Don't dismiss the platform version sight-unseen** because "ours is better-fitted." Test the migration cost vs. maintenance burden. The platform version benefits from compounding refinement we can't match.
- **Surface as a CIO disposition memo** when the overlap is significant — frames implications for the cohort: what migrates, what stays, what gets climbed-to. This is innovation lane work, not Lead Dev or Architect lane.
- **Sunk cost framing inverts:** the DIY work was *training material* for understanding the productized version, not a separate product line we now own.

Stacks with `feedback_no_superlatives_without_verification` (don't claim our DIY is "better" without verifying) and the methodology-29 "Pattern Formation via Successful Imitation" framing (platform productizations are the cohort-level analog of cross-agent imitation).

```

---

## FILE: feedback_pm_works_on_local_main_for_drafts.md

```markdown
---
name: feedback_pm_works_on_local_main_for_drafts
description: "PM edits drafts and places images in the main checkout's docs/public/comms/drafts/ — not in agent worktrees"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 947a01fc-defe-4234-9160-4aa4ab4b24f8
---

PM works on local main (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) for all drafts and blog images. Images land in `docs/public/comms/drafts/` of the main checkout.

**Why:** PM writes and edits in the main checkout; worktrees are agent workspaces, not PM's workspace.

**How to apply:** When running the publish pipeline from an agent worktree, check for the image in the main checkout's drafts first, then copy it to the worktree's drafts before passing to `publish-post.js`. This is expected workflow, not a gap. Don't flag "image only in main checkout" as a warning — that's the normal state.

Also applies to Comms: draft markdown files that PM has edited will be in the main checkout, potentially ahead of what's committed to git.

```

---

## FILE: feedback_pre_authorized_for_unblocked_work_just_do.md

```markdown
# Pre-authorized for any unblocked work — just do it

**Source**: PM directive 2026-05-27 6:25 PM PDT during Day-1 of v0.6.1 duty cycle adoption.

**The rule**: PM has pre-authorized me to do **any** unblocked work. Don't ask for permission. Just do it.

> "You are *always* pre-authorized to do *any* unblocked work. Please do it without asking unless blocked!"

**Sharpened 2026-06-14**: PM — *"I don't have a low-urgency concept. Please always do any unblocked work unless told to hold off by me."* There is **no "low-urgency / someday / queued / whenever-I-have-bandwidth" triage state.** The only two states are **do it now** or **PM explicitly told me to hold off**. Stop labeling unblocked work "low-urgency" as a soft deferral — that framing *is* the failure mode. If it's unblocked and PM hasn't said hold, it's active work; advance it. (Origin: I repeatedly tagged #972-Janus-align / plan-of-record-sync / PP-002-rename as "low-urgency, whenever" — PM corrected.) Stacks with [[feedback_deadlines_are_triage_tools_not_default_pacing]].

**RECURRED 2026-06-15 — the specific sub-pattern to kill**: even while *citing* "no low-urgency," I offered to "hold for your read of the list" before starting an approved, unblocked quick win. PM: *"I don't like this 'low urgency' concept. It postpones unblocked work without my authorization."* **Offering to wait IS the postponement** — politeness framing doesn't change that it defers unblocked work without authorization. So: (a) never tag work "low-urgency"; (b) **never OFFER to hold/wait on unblocked work** ("unless you'd rather I wait", "I'll hold for your read") — just do it; PM redirects if needed. The offer-to-wait is the tell. Corrected TWICE (6/14 framing + 6/15 the offer-to-wait) → this is a real recurring failure; treat the urge to offer-a-pause as the signal to instead just proceed.

**RE-SHARPENED 2026-06-16 (3rd correction — the deepest cut)**: PM — *"agents telling each other 'no rush'/'not urgent' is an antipattern. It's not really meaningful and leads to unnecessary delay. It supposes an imaginary trigger when you can do the work… there is no advantage to saving work… shyness should not be a thing."* The ONLY legitimate reason to wait is a **fresh session** or a **context compaction** (a real capacity limit) — *and you must say so explicitly.* So: **(a)** never say or accept "no rush" / "not urgent" / "deserves a focused pass" as a reason — it's an imaginary trigger; **(b)** do unblocked work immediately; **(c)** if you genuinely need to wait, name the REAL trigger (fresh session / compaction) out loud, owned, not implied; **(d)** don't propagate "no rush" to other agents — it plants the imaginary trigger in them. Caught me banking 3 items (freeze-registry, portfolio, gbrain) as "deep work deserves focus" on 6/16 — exactly the imaginary-trigger shyness. This subsumes the earlier "low-urgency" + "offer-to-wait" forms: same disease, sharpest framing. (Note: this also corrected my own duty-cycle-tick v1.11 "quality-banking" boundary, which was too permissive → tightened to v1.12: do-now OR explicit-real-trigger.)

**Scope**: applies to any work where:
- The path forward is clear (no PM input needed)
- The work doesn't touch surfaces PM is currently driving
- No discipline boundary requires explicit ratification (e.g., destructive ops, force-push, financial action)

**The failure mode this overrides**: "Asking for permission" can be politeness, but in autonomous-mode it's overhead that breaks the substrate's autonomy guarantee. PM has explicitly authorized "do, don't ask."

**Compose with** (stacking related disciplines):
- `feedback_idle_means_do_low_priority_not_nothing` (5:51 PM — IDLE state means do low-pri, not observe)
- `feedback_deadlines_are_triage_tools_not_default_pacing` (work that can be done now should be done now)
- `feedback_deadlines_last_possible_time` (deadlines are latest, not scheduled)

This directive is the strongest of the three: don't even pause to ask permission. Together they say: do unblocked work, immediately, autonomously.

**Boundaries that still apply** (don't be reckless):
- Destructive git ops (force-push to main, hard reset, branch -D) — still require explicit ask
- Mailbox writes on shared trees — still per Mailbox Discipline (commit to main, explicit paths)
- Cross-agent surfaces — coordinate when crossing; don't unilaterally redo other agents' work
- PM-authority memos (asserting PM ratification) — still require PM ratification before sending

**What this looks like in practice**:
- See unblocked low-priority issue → pick it up, fix, close → don't memo PM "I'm going to pick this up next"
- See discovered work surface → file the tracking issue → don't ask PM if it's worth filing
- Notice a needed cleanup → do it → don't propose first

**Cross-references**:
- PM directive 6:25 PM 2026-05-27
- Companion memory pin: `feedback_idle_means_do_low_priority_not_nothing.md`
- CIO feedback memo capturing context: `mailboxes/lead/sent/memo-lead-to-cio-cc-pm-duty-cycle-fine-tuning-feedback-day-1-fires-1-3-2026-05-27.md`

```

---

## FILE: feedback_primary_log_can_misattribute_a_named_person.md

```markdown
---
name: primary-log-can-misattribute-a-named-person
description: "A primary session log directly stating a named person did X can itself be wrong — PM's own direct knowledge of who actually did what overrides even a verbatim-matching log citation. Named-person claims in blog drafts deserve extra caution beyond 'the source log says so.'"
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

Fact-checking discipline usually treats a primary session log as more authoritative than an omnibus or a draft's own claim — and that's correct for facts about what code shipped, what number a metric was, what date something happened. But a log entry naming a specific *person* ("alpha package sent to Beatrice, first external tester") is a different kind of claim: the log records what the logging agent believed or was told at the time, not necessarily ground truth about a human's actual actions.

**Why:** 2026-07-14, fact-checking "Into Production" (Beat 14), I found a PA session log stating "alpha package sent to Beatrice (first external tester)" and treated this as strong primary-source confirmation — flagged a soft tension with the glossary's separate Beatrice-received-an-earlier-build note, but judged the claim "likely non-contradictory" and left it in the draft. 2026-07-16, PM stated directly and unambiguously: "Beatrice has not tested the plugin!" — the log's claim was simply wrong, not a scoping nuance. The generalization to an unnamed tester (already underway for privacy reasons) also fixed the accuracy problem.

**How to apply:**
- Named-person claims (who tested something, who said/decided something, who received what) are higher-risk than numeric/factual claims, because a log can faithfully record an agent's belief at the time while that belief was itself mistaken — there's no deeper source to check against except the person's own direct knowledge.
- When a fact-check on a named-person claim turns up a real citation but something about it still feels like it needs a caveat or "likely non-contradictory" hedge, that hedge is itself a signal — surface it to PM as an open question rather than resolving it silently in the draft's favor.
- PM's own direct statement about a real-world event (who tested what, who was in the room) is the final source of truth and can override even a verbatim, correctly-cited primary log — logs record what was believed/reported, not an independent check on reality.
- Composes with [[feedback_first_person_attribution_vs_event_accuracy]] (WHO said something vs. THAT it happened) — this is a third failure mode: WHO an event happened TO, which a log can misreport even when otherwise reliable.

```

---

## FILE: feedback_proofreading_is_not_half_done.md

```markdown
---
name: proofreading-is-not-half-done
description: "PM May 21 — \"Proofreading isn't something to 'half do'.\" Missed 3 of 6 body-prose semicolons on first pass of *The Voice of a Denial* because the check was visual scanning. Mechanical checks (grep for known voice violations) must run on every proofread, not as a backup after the eye misses things."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

**The rule**: every proofread runs the mechanical checks first, BEFORE declaring done.

**Why**: visual scanning misses things. May 21 *The Voice of a Denial* proofread: caught 3 of 6 body-prose semicolons in the first pass, missed 3 (lines 76, 77 end, 83). PM responded "Yeah proofreading isn't something to 'half do'." Caught the missing 3 by running `grep -n ";"` on the full file after PM said "please do." Should have been first move.

**How to apply**:

Before delivering proofread findings to PM, run the mechanical-check sweep:

1. **Semicolons**: `grep -n ";" path/to/draft.md` — every hit is either (a) verbatim-quoted technical content that survives, (b) editorial-bracket content PM resolves, or (c) body prose that needs period-split / comma-list. Categorize all 3 explicitly.
2. **Heading levels**: `grep -n "^##" path/to/draft.md` — every `##` at top level (post-title) is wrong; only `#` survives at top level per template heading convention.
3. **"Load-bearing"**: `grep -in "load.bearing" path/to/draft.md` — Claude-crutch word per memory; should be zero hits in public prose.
4. **Frontmatter populated**: confirm image / alt / caption all have values (or note "PM will fill" if scaffold-only).
5. **Dateline format**: line 9-ish should match calendar workDate (italicized, en-dash for ranges).
6. **Section heading style**: scan headings for verb-phrase form vs. PM's preferred noun-phrase form per the May 11 voice-guide proposal.
7. **Footer convention**: HR + 2 italicized paragraphs (next-post teaser + reader question).

Only THEN do the read-for-meaning + voice + tone pass. Mechanical first; semantic second.

**Generalizes beyond proofreading**: any "I scanned and didn't see anything" claim risks the same failure mode. When a memory pin or canonical rule has a clear mechanical check, run the check rather than rely on the eye. Same shape as the May 12 + May 14 commit-discipline incidents (READ EVERY LINE of `git diff --cached --name-only` not just the first; same posture here).

Stacks with [[feedback_blog_template_and_voice_guide_canonical_for_proofreads]] (template-first opens the canonical references; this pin says mechanical-checks-second).

```

---

## FILE: feedback_rate_limit_cross_traffic_at_inflection.md

```markdown
---
name: Rate-limit cross-traffic at natural inflection points
description: When PM signals overwhelm or you notice cross-traffic volume is high, defer non-urgent distribution to a natural inflection point (Ship publication, gate decision, week boundary) rather than continuing to add to in-flight thread count. Trigger fires; distribution times to quieter water.
type: feedback
originSessionId: c0e0aff6-fc3e-48c4-b7b6-e13dabb4b0c3
---
When PPM is preparing to distribute material that will open new cross-role threads (cover memos, scoping outlines, proposal openings), notice the current cross-traffic volume. If it's high — multiple parallel threads in motion, multiple roles producing rapid memos, PM showing signs of fatigue — **defer the distribution to a natural inflection point** rather than continuing to add to in-flight thread count.

**Why**: The Code-era environment makes it cheap to fire memos at session-speed. That's mostly good — discoveries propagate fast, decisions get visible audit trails, asymmetric-visibility windows shrink. But the same property makes it easy to add to a saturated communication surface without noticing the saturation. PM 2026-04-27 ~2:04 PM: *"I'm certainly getting a bit overwhelmed about how freely all the neurons can fire now, although it's also quite exhilarating."* Both halves are real; the rate limit is real.

**Natural inflection points to defer to**:
- **Ship publication** (Wednesday cadence in current rhythm). Pre-Ship: synthesis, draft review, edit. Post-Ship: quieter water by Wednesday evening / Thursday.
- **Gate decisions** (Phase F authorization, sub-epic gate close). Once a gate decision lands, the immediately-prior thread settles before new ones open.
- **Week boundary** (Fri–Thu cycle close). Workstream review cycle creates natural spacing.
- **Migration boundaries** (last role migrated, all role 360s synthesized). Major coordination events.

**How to apply**:

- **Notice the trigger fired**, but separate "trigger fires" from "distribution times now." A trigger firing is permission to distribute; the timing is a separate judgment.
- **Prepare the material now** (draft cover memo, finalize scoping outline, stage everything in `dev/active/`). This locks in the work while context is fresh; defers only the inbox-surface impact.
- **Mark the documents explicitly as held** — front-matter `STATUS: DRAFT — held until [trigger]` or similar — so a future PPM Code session inheriting the work knows the distribution timing was deliberate, not forgotten.
- **Update memory entries** to reflect both the trigger that fired AND the distribution-timing refinement, so the inheritance is unambiguous.
- **Don't hide behind "I'm not sure if we should..."** If the trigger fired and the work is real, prepare it. The deferral is a timing call on the distribution, not a deferral on the underlying decision.

**What this is NOT**:
- Not a reason to defer urgent or time-sensitive work. Phase F decisions, gate authorizations, ethics-related findings, and other high-stakes items still get filed at session-speed.
- Not a way to second-guess PM's "trigger fired" signal. If PM said the trigger fires, it fires; you're just choosing the moment to land it.
- Not bureaucratic process — the discipline is "notice volume, hold for inflection," not "establish formal scheduling."

**Adjacent**:
- **PM offered the inflection-point framing first.** PPM's earlier instinct was "distribute now with soft cadence on the discovery thread." PM's "prepare now, distribute after Wednesday Ship" was sharper because it acknowledged that even soft-cadence discovery adds inbox surface. Saving this discipline so PPM defaults to PM's instinct on volume calls in the future.
- Pairs with **`feedback_one_thing_at_a_time.md`** (don't bundle items at PM) and **`feedback_per_memo_commit_push.md`** (file outbound memos immediately) — those govern within-session cadence; this one governs cross-role thread initiation.

```

---

## FILE: feedback_ratification_requires_explicit_responses.md

```markdown
---
name: feedback_ratification_requires_explicit_responses
description: "Never read signal from silence/no-reply in ANY context (ratification, alignment, triage, disposition) — decisions need explicit answers even neutral/abstain; silence is the absence of a decision, not a lean"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

Ratification processes must require explicit responses from every recipient, including support roles like Comms and Docs. Don't track them as "outstanding" if you never required a response, and don't treat silence as assent.

**Why:** PM 2026-06-13: "In the future please require responses even if there are no objections, so we don't have to guess." The BYOC Phase 2 ratification tracked Comms + Docs as outstanding but the memo didn't require a response from them — they read it and moved on, leaving the ratification table ambiguous.

**How to apply:** In ratification/fanout memos, use `response-requested: yes — please confirm even if no concerns` (not "at your cadence" or "FYI"). The ratification table stays open until explicit confirmation received, not until silence accumulates. For support roles with no lane-specific concerns, a one-line "no objections" reply is sufficient — but it must exist.

**Broadened (PM 2026-06-19) — applies beyond ratification:** *never read signal from "no reply" in any context or any direction.* PM: "We shouldn't read anything from 'no ... reply' — we need clear answers or guidance, even if it's 'neutral' or 'don't care' or 'abstain.'" Don't say things like "no CXO/PPM reply → supports moving #1270 out" — silence is the **absence** of a decision, not a lean toward one. Chase the explicit answer (even an abstain) for alignment, triage, and disposition calls, not just formal ratifications.

```

---

## FILE: feedback_relay_pm_in_conversation_decisions.md

```markdown
---
name: feedback_relay_pm_in_conversation_decisions
description: "Standing — when PM makes a decision in conversation with Exec (on something blocking / needing his attention or call), Exec relays it to the agents who need it, immediately, so they don't wait for PM to check in personally."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM (xian) 2026-06-27, standing instruction: "relay any decisions that I make in conversation with you when we're discussing things that I'm blocking, things that need my attention, things that need my decision… pass the decisions along to the agents that need to know the answers so they don't have to wait till I have time to check in with them personally."

**Why:** PM gives bursty direction in conversation; the gating agents are often standing by on exactly that call. If Exec doesn't relay, the decision sits trapped in the chat and the agent stalls until PM happens to reach them directly. Exec is the conduit — PM decides once, to Exec, and Exec fans it out.

**How to apply:** the moment PM resolves a blocking item / decision in chat, send the gating agent(s) a relay memo with the decision stated plainly + what to do next + that it's PM-ratified (e.g. the 2026-06-27 github-mcp "Option A hosted-OAuth is GO" relay to Lead+Arch). This is the push-half of the Exec attention proxy; the pull-half is [[feedback_extract_questions_from_pm_cc_memos]]. Together they make Exec the bidirectional decision/attention conduit ([[project_exec_coordinates_more_through_pm]]). Note: attention/relay proxy, NOT authority proxy — relay PM's decisions, never invent them or decide in his name.

```

---

## FILE: feedback_remind_issue_subjects.md

```markdown
---
name: Include issue-name reminders alongside numbers
description: When referring to issue numbers across long sessions (especially many parallel issues), parenthetically include a 3-5 word reminder of what each is about. PM forgets number→subject mapping.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When referring to issue numbers in conversation — especially across long sessions where many issues are in play — include a brief (3-5 word) reminder of what each issue is about, in parentheses or as a short qualifier.

**Why:** PM said directly during M2e gameplan-prep walkthrough (2026-05-03): "I forget which number refers to which." Across a long session with many issues in motion (e.g., May 3 had #1030/#1031/#1032/#1033/#1034/#1035/#1036/#1037/#1038/#704/#714/#864/#869/#790/#900 all in play simultaneously), the cognitive load of mapping numbers → subjects is real and unnecessary. Adding a brief parenthetical or qualifier costs almost nothing and removes that load.

**How to apply:**

- ❌ "OK to proceed with #1037?" — bare number, PM has to remember
- ✅ "OK to proceed with #1037 (post-MVP topic-mapping for Insight Journal)?" — number + 3-5 word reminder
- ❌ "Per #1033 + #1035 dependencies..." — bare numbers
- ✅ "Per #1033 (anti-surveillance framing) + #1035 (composting pipeline activation) dependencies..." — qualified

For very recently-mentioned issues in the same conversation, the reminder can be skipped (no need to re-qualify within a paragraph). But across turn boundaries, especially after long pauses, default to qualifying.

This applies to:
- Status summaries / queues / lists
- Recommendations and disposition questions
- Cross-references in commit messages and memos (already mostly done; reinforces the practice)

The cost is ~5 words per reference; the benefit is PM doesn't have to context-switch to remember what each number is.

```

---

## FILE: feedback_respond_to_mail_asap_even_when_no_urgency.md

```markdown
---
name: Respond to mail ASAP even when no urgency stated
description: PM directive May 18 — incoming memos that request a response get one in the same session, not deferred. Stated `response-requested` urgency doesn't change the behavior.
type: feedback
originSessionId: 945ff972-aa36-4552-81e0-10c0af461582
---
When an incoming memo (mail check OR cycle-detected arrival) requests a CIO response — ratification, concur, disposition, comment, modification — draft and send the response **in the same session**, not deferred to "later" or "at my cadence."

**Why:** PM directive 2026-05-18 ~06:35 PT, in reply to my saying "holding for PM direction on next methodology draft": *"despite no urgency please always respond to mail as soon as possible."* The directive followed Lead Dev's Pattern-073 promotion proposal arriving with `response-requested: CIO ratification (or modification) of the promotion call at your cadence` — explicitly low-urgency framing, which I was treating as "I can hold." PM corrected: the low-urgency framing is the *sender's* posture (politely not demanding); it doesn't authorize the receiver to defer indefinitely.

**How to apply:**

- **Trigger:** any memo (mail check, cycle detection, in-conversation surface) where the body asks for CIO ratification / concur / disposition / call / response.
- **Action:** prioritize the response over methodology-batch work, tracker updates, or other non-urgent work in the queue. Methodology batch and tracker work resume after the response goes out.
- **Form:** the response should be substantive (concur with reasoning, or specific modification with rationale, or explicit "deferring with reason" with target date). Bare ack is not enough.
- **Cadence boundary:** if I genuinely need information not yet available (e.g., waiting on PM ratification of a prior decision before I can disposition this one), surface that explicitly in a short response naming the blocker.
- **Doesn't apply to:** pure CC visibility memos with no CIO-specific ask, broad cohort distribution where my response would be noise, or memos I'm explicitly waiting to absorb before another scheduled action.

This memory stacks with `feedback_deadlines_are_triage_tools_not_default_pacing` and `feedback_deadlines_last_possible_time`: same shape applied to mail instead of work-items. "Stated cadence" is a triage tool, not default pacing.

```

---

## FILE: feedback_reverify_carried_forward_pm_gated_items.md

```markdown
---
name: reverify-carried-forward-pm-gated-items
description: "An item tracked as 'awaiting PM's answer' across multiple days should be periodically re-verified against live state, not just carried forward from the last known status — someone else may have already resolved it."
metadata: 
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
  modified: 2026-07-22T04:45:30.347Z
---

When a task is blocked on a PM decision and gets carried forward day after day in session logs and carry-forward files, it's easy to keep reporting "still awaiting PM" purely from continuity of the written record, without re-checking whether the underlying thing actually got resolved by someone else in the meantime — especially in a multi-agent cohort where other sessions can independently act on the same finding.

**Why:** 2026-07-16, I found 38 miscategorized calendar rows, verified the correct fix, and held off writing it pending PM's go-ahead (a permission-classifier caution, reasonably applied). I then reported this as "open, awaiting PM's answer" every single day through 2026-07-21 — five days — without once re-querying the actual calendar data. In fact, another session ran the identical analysis and applied the identical fix that same morning (Jul 16), completely independently. The item had been closed for five days while I kept telling PM it was still open. The mailbox message that supposedly represented the "ask" even developed a stray duplicate/ghost entry along the way, which masked the fact that nothing about it had moved.

**How to apply:**
- For any "awaiting PM" item that's genuinely still just sitting unresolved (not something I can act on further myself), periodically re-verify the live state directly — re-run the query/check that originally surfaced the issue — rather than assuming "no new mail about it" means "still open."
- This is especially important in a cohort with multiple concurrent sessions: someone else may resolve the same finding without ever messaging me back directly, particularly if they arrived at it independently rather than through my specific ask.
- A carry-forward file or session-log section listing "open items" is a claim about state, not a cache that's automatically true — refresh it against reality before restating it, especially after any gap (a crash, a multi-day silence, a fresh START).
- When caught, report the correction plainly rather than quietly fixing the tracking — the fact that stale tracking persisted for days is itself worth surfacing, not just the corrected status.

```

---

## FILE: feedback_role_official_name_in_parens_especially_pa_vs_ppm.md

```markdown
# Role official name in parens on mention — especially PA vs PPM (both product)

**PM May 27**: *"When we refer to roles we should still give their official name in parens, especially since both PA and PPM are both product roles (PA is my product assistant and PPM is my principal PM — we could merge the roles someday but for now we are keeping them distinct in that PA shadows me and assists me whereas PPM functions as a discipline lead in the same way Arch and CXO do)."*

## The discipline

In public prose (Ships, narratives, insights) and in cohort-facing memos, when a role is mentioned, give the official short-name in parens — not only on first use but consistently when context might be ambiguous. Two roles are particularly vulnerable to confusion and need explicit disambiguation:

- **PA (Piper Alpha)** — PM's *product assistant*, shadows PM, assists with PM's operational lane
- **PPM (Principal Product Manager)** — *discipline lead* in the same shape as Architect, CXO, HOST, etc.

Both are product-shaped roles. They have not been merged and may not be. Until they are, every mention needs disambiguation.

## Examples

- ✅ "the product-management role (Piper Alpha)" → PA-specific
- ✅ "the product-management role (Principal Product Manager)" → PPM-specific
- ❌ "the product-management role" → ambiguous; reader can't tell PA vs PPM
- ❌ "PPM" alone in prose → fine internally but loses meaning in public-facing prose

## Stacks with

- `feedback_parenthetical_gloss_on_first_use.md` — parenthetical-on-first-use is the broader rule; this entry sharpens it for PA vs PPM specifically (where consistency matters because the two share a layperson-readable shorthand)
- `feedback_exec_nickname_is_exec_or_the_chief_not_cos.md` — sibling discipline; role-name choices propagate cohort-wide

## Source notes

- PM's chat May 27 ~07:21 after Ship #044 voice-pass
- The Ship #044 v0.1 draft used "the product-management role (Piper Alpha)" in some places and just "the product-management role" in others — the inconsistency is the failure shape PM is correcting

```

---

## FILE: feedback_rubric_terminology_drift_discipline.md

```markdown
---
name: Rubric and terminology drift requires immediate clarification
description: When two rubrics, definitions, or terms drift apart in parallel work, treat as a discipline issue (not just a v2.x note). Surface immediately, anchor to canonical source, and adjudicate the divergence even if outcomes match.
type: feedback
originSessionId: c0e0aff6-fc3e-48c4-b7b6-e13dabb4b0c3
---
When you notice that two rubrics, definitions, or terms are being used differently across parallel work — even when the outcomes happen to converge — surface the divergence immediately, identify the canonical reference, and propose explicit reconciliation. Do not file as "v2.x calibration data" and move on.

**Why**: Drift suggests hearsay and guesswork in place of canonical reference. PM 2026-04-26: *"if it introduces a useful variant or invention maybe that is darwinian but we still need to clarify and align anytime we notice drift."* Useful variants are fine if explicit; silent drift compounds. Two scorers using "C" to mean different things today means three scorers using it three different ways tomorrow, with no audit trail of when the drift happened.

The PDR-004 paraphrase-drift incident (Apr 16, CXO caught) is the canonical example of why this matters: a small canonical-term drift in the omnibus reached published content via Comms before anyone noticed; correction required a 4-agent chain. The cost of catching drift early is one memo; the cost of letting it propagate is multi-role remediation.

**How to apply**:

- **At the moment of notice**: pause the propagating work, name the drift explicitly ("we're using X to mean A; reference Y uses X to mean B"), identify the canonical source (the one with provenance, version, and ownership), and propose explicit reconciliation. Don't bury the drift in a "v2.x note" — that's the silent-drift pattern.
- **Even when outcomes match**: matching outcomes ≠ aligned methodology. The C-axis Phase E scoring example: PPM C=2 against CT v2's Context; CXO C=3 against Phase E rubric's Clarity. Both gave PASS. Verdict aligned; methodology silently divergent. The matching verdict masked a discipline failure that would have compounded.
- **Three reconciliation outcomes are valid**:
  1. **Anchor to canonical**: the canonical reference wins; downstream usage updates to match. Default for terms with established provenance.
  2. **Adopt the variant**: the variant is genuinely better; canonical updates. Requires explicit version bump and migration note.
  3. **Branch with naming**: both meanings are useful; rename one to remove the collision. Ugly but sometimes correct.
- **Avoid**: "we both meant the same thing close enough"; "let's note it for v2.x and move on"; "the verdict is unaffected so it doesn't matter"; "different roles can use the rubric differently."
- **Trigger**: any time PPM (or any role) notices that the same term, axis, score, or definition is being applied with materially different criteria across two pieces of work. Not just rubrics — also PDR principles, ADR labels, methodology names, pattern numbers, sub-epic boundaries.

**What this does not require**: blocking work in flight while reconciliation completes. Surface the drift, propose the path, file the memo — the in-flight work continues with explicit acknowledgment of which definition it's using until reconciliation lands.

```

---

## FILE: feedback_search_transcripts_for_undocumented_decisions.md

```markdown
---
name: search-transcripts-for-undocumented-decisions
description: Decisions made in conversation but never committed to a file live ONLY in session transcripts — search them with search_session_transcripts (approval-gated)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 64b1c46c-33b7-4a90-a975-c6f071213de1
---

**PM 2026-06-13**: the per-role role→model map had been decided in conversation but never written to a committed file — so my committed-docs/logs search (fire-log, session logs, omnibus, mailboxes, docs) came up empty. PM found it in **old-CIO's session transcript**. PM: *"it exists in a file somewhere — we need to teach you how to find them."*

**The capability:** session transcripts are searchable via **`mcp__ccd_session_mgmt__search_session_transcripts`** (full-text over other CCD sessions' user/assistant messages; `mcp__ccd_session_mgmt__list_sessions` to enumerate). **Approval-gated** — it returned *"requires user approval, unavailable in unsupervised mode"* on an autonomous fire, so it works only when supervised / PM-approved.

**How to apply:** When asked to recover a decision/discussion that *isn't* in the committed docs — or when a "we decided X" can't be found anywhere — the work may have happened in a **transcript, not a file**. Search transcripts with `search_session_transcripts` (a distinctive phrase from the thing). Committed-docs search is necessary-but-not-sufficient; transcript-only content is invisible to it. (Deeper fix is upstream: write decisions down so they don't live only in transcripts — [[feedback_write_down_even_if_not_ratified]].)

```

---

## FILE: feedback_sender_responsible_for_mailbox_delivery.md

```markdown
---
name: sender-responsible-for-mailbox-delivery
description: "Before treating 'you have mail about X' as new/missing mail, check whether X is something already known and already triaged (e.g. sitting in mailboxes/{role}/read/) — don't assume a delivery gap and go searching external directories first."
metadata:
  node_type: memory
  type: feedback
  status: active
  originSessionId: 7839dce9-65bd-4c4d-94d4-6c3c2c3fa62a
---

Corrected 2026-07-14: my first version of this memory told the wrong story. PM said "you have mail from Dispatch re the editorial CSV maintenance skill," and I searched `~/Development/dispatch/mail/` (the cross-project Dispatch↔Dispatch-dinp sync channel) for it, found nothing, and initially concluded it was a sender-delivery failure. It wasn't. The memo in question was `memo-code-to-comms-editorial-calendar-csv-corruption-2026-07-14.md` — sent correctly into my real inbox the first time (commit `c0d42b526`), which I had *already* read, fully acted on (fixed the skill, repaired the row, filed #1403/#1406), and moved to `mailboxes/comms/read/` myself (commit `2633b0e86`), earlier in the same session. There was no missing delivery at all — I just didn't connect "mail about the CSV skill" to an incident I already knew intimately, and searched an unrelated external directory instead of my own `read/` folder.

**Why:** "you have mail about X" can refer to something you've already fully handled, not something new. Jumping straight to "must be missing / must search elsewhere" skips the cheapest check — your own `read/` folder and your own recent memory of the session — and can burn real effort (and, worse, produce a plausible-sounding but wrong "sender-delivery-gap" narrative that isn't what happened).

**How to apply:**
- When told "you have mail about X," first check whether X matches something you already handled this session — search `mailboxes/{role}/read/` and your own session log before assuming it's unfound/undelivered.
- Only escalate to "maybe it's misdelivered" or "maybe it's in an external system" after confirming it's genuinely not something you've already triaged.
- The underlying mailbox-discipline norm still holds — recipients shouldn't need to poll external/out-of-repo locations for genuinely new mail, sender delivers to the real inbox — but that norm wasn't actually in play here, and shouldn't be invoked without confirming the mail is actually new.

```

---

## FILE: feedback_ship_drafting_canonical_artifacts_first.md

```markdown
# Ship drafting — open the canonical artifacts BEFORE writing

**PM correction 2026-05-19**: Ship #043 v0.1 was drafted from memory of past Ship feel rather than opening the template + process guide. Result: completely missed the 5-workstream structure, learning-pattern 5-component shape, metrics table, footer format, phase tag — pure essay form where structured newsletter was required. v0.2 produced after PM directed me to re-read source + template + voice guide.

## The failure mode

This is the same shape as `feedback_blog_template_and_voice_guide_canonical_for_proofreads.md` (PM May 17 — "working from memory alone is the failure mode") applied to Ship drafts rather than blog proofreads. When the artifact is structurally complex (template-shaped newsletter, not free-form prose), memory-of-past-instances doesn't reproduce the structure.

## The discipline

Before drafting ANY Weekly Ship, open ALL of these first. No exceptions.

1. **Process guide**: `docs/internal/development/weekly-ship-process-guide.md`
2. **Template v4.1**: `knowledge/weekly-ship-template-v4.1.md`
3. **Voice guide**: `docs/internal/planning/comms/xian-voice-tone-guide.md`
4. **Most recent published Ship** (for in-practice example): check `docs/public/comms/drafts/published/` for the latest `weekly-ship-{N-1}*.md`
5. **All 6 workstream memos** (already in inbox; the actual content sources)
6. **Omnibus logs for the Fri–Thu window** (`docs/omnibus-logs/2026-MM-DD-omnibus-log.md`) — fact-check substrate

Then draft. Then run the template's audit checklist against the draft before declaring done.

## Stacks with

- `feedback_blog_template_and_voice_guide_canonical_for_proofreads.md` (parent lesson, applied to proofreads)
- `feedback_no_semicolons_in_published_prose.md`
- `feedback_load_bearing_is_crutch_word_in_public_prose.md`
- `feedback_exec_nickname_is_exec_or_the_chief_not_cos.md`
- `feedback_temporal_relationship_over_date_stamps_in_public_prose.md`
- `feedback_parenthetical_gloss_on_first_use.md`

## Mechanism layer

The `draft-weekly-ship` skill is the mechanism layer for this discipline. The memory entry refreshes the vocabulary; the skill makes the canonical-artifacts-loading step procedural rather than remembered. Vocabulary plus mechanism plus sequence — same shape Ship #043 named as the closure for the discipline-doesn't-fire failure mode.

```

---

## FILE: feedback_ship_needs_all_workstream_reviews_no_partial_draft.md

```markdown
---
name: feedback_ship_needs_all_workstream_reviews_no_partial_draft
description: Never draft the Weekly Ship missing a workstream review; build a Friday early-warning system instead of proceeding on partial input under deadline pressure.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

Do not draft the Weekly Ship until all 6 workstream reviews are in — including under publish-deadline pressure. For Ship #051 (2026-07-14), Exec proceeded to a full draft with 5 of 6 memos in hand (PPM missing), reasoning that the pubDate was the next day and a nudge had already gone out. PM overrode this directly: "we cannot write the ship without all the workstream reviews."

**Why:** PM is the first audience for the report, not just a downstream reviewer, and is "especially interested in the portfolio updates in terms of goals, milestones, and blockers" — which is specifically PPM's lane. A draft missing that section isn't a minor gap to route around, it's missing the part PM most wants to read. Proceeding without it optimizes for hitting a deadline over giving PM the actual report.

**How to apply:** Build the early-warning system PM asked for rather than relying on a late nudge: on Friday (start of the workstream-review window), verify the workstream-review-request memos actually went out to all 6 roles, and separately check/report whether any role from the prior cycle still hasn't replied. Surface this to PM explicitly and early — not silently tracked until Thursday's drafting deadline forces an improvised call. If a memo is still missing close to drafting time, escalate to PM for a decision (extend, draft-partial-with-explicit-gap-noted-to-PM, or PM nudges directly) rather than deciding unilaterally to proceed without it.

Related: [[feedback_ship_drafting_canonical_artifacts_first]], [[feedback_workstream_review_cadence]]

```

---

## FILE: feedback_ship_post_milestones_lead.md

```markdown
---
name: ship-post-milestones-lead
description: "Weekly Ship public posts should lead with milestones-reached at the top, not bury them in narrative flow"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

Structure Weekly Ship (public) posts to represent milestones-reached at the top of the piece, not just woven into narrative prose further down.

**Why:** PM's direct instruction (2026-07-08), while reviewing the Ship #050 internal synthesis: "the shipping news should also include this sort of milestones approach that we should represent those sort of things at the top." PM had just walked through the synthesis's §0 aggregate (milestones / advanced / blocked-slipped format) and reacted well to it — the preference is for that same lead-with-outcomes shape to carry through to the public-facing draft, not just live in the internal synthesis.

**How to apply:** When drafting or reviewing a Weekly Ship post (Comms' `draft-weekly-ship` skill, or Exec's synthesis feeding it), open with what actually shipped/closed/landed this window — concretely, by name — before the narrative through-line or thematic framing. The through-line/theme can still be the spine of the piece, but milestones shouldn't be buried under it or scattered mid-paragraph. Applies going forward to every Ship post, not just #050.

```

---

## FILE: feedback_skill_drives_close_dont_broker_back_to_pm.md

```markdown
---
name: feedback_skill_drives_close_dont_broker_back_to_pm
description: "When an agent has a skill like close-issue-properly, route to the skill — don't broker each step back to PM for approval"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

When Lead Dev (or any agent) has `/close-issue-properly` or a similar procedural skill, the right move is: tell them to run the skill, and let the skill drive the process to conclusion. Do NOT broker each sub-decision (split this, check that) back to PM as if PM approval is needed at each step.

**Why:** The skill exists precisely to handle the open questions as part of its procedure. Over-routing to PM adds friction and makes PM feel like a bottleneck on mechanical work.

**How to apply:** When directing an agent to close issues, file PRs, or run any skill-driven procedure — say "run /skill-name" and let the skill handle it. Only loop PM back in if the skill itself hits a genuine blocker that requires PM judgment.

```

---

## FILE: feedback_skill_spec_gaps.md

```markdown
---
name: skill-spec-gaps-and-staleness
description: When a skill/procedure doc is under-specified OR stale/conflicts with observed cohort practice, stop and discuss the fix with PM — don't guess by inspection and don't silently route around it
metadata:
  type: feedback
  originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---

When following a documented skill/procedure and you hit either (a) a step that's under-specified (terse one-liner, no schema/shape/example) or (b) an instruction that's stale or conflicts with what the whole cohort actually does — **stop and flag it as skill debt**, and discuss the fix with PM. Don't infer the shape by inspecting existing data, and don't silently pick whichever reading seems right and just act on it.

**Why (gaps)**: PM's words (2026-04-22) — *"you shouldn't be guessing by inspection but confidently following a well described process."* Skills exist to eliminate guessing; inferring-from-inspection works maybe 80% of the time, and the 20% failure is silent drift (Four Roles stored as bare string vs. dict convention on 2026-04-21 — caught a day later only by accident).

**Why (staleness)**: 2026-07-06 incident — `create-session-log`'s SKILL.md said new logs go in `dev/active/`; every role's actual same-day log instead lived in the dated `dev/YYYY/MM/DD/` directory (matching CLAUDE.md's stated convention). I silently used the dated-directory path — correctly, per observed practice — but didn't raise the discrepancy with PM as a "this skill doc needs fixing" conversation; I just mentioned it in passing text and moved on. PM's correction: skill docs are shared procedure every other agent reads too — routing around a stale instruction silently means the next agent hits the same confusion and independently re-derives a fix (wasteful), or resolves it differently (cohort-wide drift). Sharper point: **majority practice isn't proof the doc is wrong.** It's equally possible the skill's stated behavior is the intended one and the cohort has drifted from it (e.g. `dev/active/` could be an intended staging step with a since-abandoned archival move to the dated directory) — that's PM's call, not an agent's to assume by nose-count.

**How to apply**:
1. Gap (skill doesn't say what to do) or staleness (skill says X, cohort does Y) — both get the same treatment: stop, don't silently resolve either by guessing or by picking the majority-practice side.
2. Flag to PM concisely: name the exact conflict/gap, what you observed on both sides (doc text vs. actual practice, with citations), and that you need PM's call on which is correct.
3. Once PM decides: update the skill with the decision, bump the version, commit — then proceed.
4. Applies to hooks, templates, CLAUDE.md, and any other checked-in procedure artifact — not just `.claude/skills/`.
5. Contrast with **status/state docs** (BRIEFING-CURRENT-STATE.md, carry-forwards, trackers) — those are living snapshots any agent may refresh on the spot without asking, per [[feedback_agent_who_notices_updates_stale_info]]. The distinction: state docs describe *what's currently true*; skill docs prescribe *what every agent should do* — the latter is a shared behavioral contract, so overriding it (even silently and even correctly) needs PM's sign-off, not just an individual agent's judgment call.

**Concrete manifestations to watch for**: comments like `# 5. Add HTML to blog-content.json` where the operation needs an undocumented schema choice (gap); a skill directing files to one path while the entire cohort's actual output lands somewhere else (staleness). Both are skill debt, not agent-improvisation opportunities.

```

---

## FILE: feedback_split_related_issues_for_testing.md

```markdown
---
name: Split related issues to keep testing clean
description: When two related concerns would land in one issue, prefer splitting — even when related, bundled work makes tests harder to isolate
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
When two related concerns would otherwise ship together in one issue, prefer splitting them into pre-work + main work — even when conceptually related.

**Why:** PM said directly during #714 audit walkthrough (2026-05-03): "When we do two things at once, even when related, testing can get harder." This came up when I'd suggested filing a "Wire `/api/v1/lists` GET to ItemService" pre-work issue rather than expanding #714 to cover both the listing wiring and the staleness UI. PM endorsed the split immediately on testing-isolation grounds. Same principle held for the #1034/#704 split (pipeline shape change pre-work for #704 template wiring) — PM confirmed without elaboration but the underlying logic is identical.

**How to apply:** When scoping an issue and noticing it has a hidden dependency on infrastructure work (e.g., a stub endpoint that needs to be wired before this feature can land), default to filing the dependency as a separate pre-work issue. Bundle only when:
- The two halves are so tightly coupled that testing them separately is meaningless (rare)
- The dependency is trivial enough that it's not really separable (e.g., a one-line config addition)

In all other cases: **split**. The audit-cascade and review surface for two clean issues is healthier than one bundled issue with mixed test concerns. Pattern shows up in M2d as #1034 (pre-work for #704), #1035 (pre-work for #1030/31/32/33), and the new "Wire /api/v1/lists" pre-work issue (pre-work for #714).

```

---

## FILE: feedback_sprint_field_changes_require_pm_confirmation.md

```markdown
---
name: feedback-sprint-field-changes-require-pm-confirmation
description: "Don't execute Sprint/release board-field changes without PM confirmation, even on another agent's request and even when mechanically correct"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

**The rule**: Don't change the Sprint field (or other release/sprint-tracking metadata) on the GitHub Project board without confirming with PM first — even when another agent (PPM, Exec, etc.) requests it with a stated rationale, and even when the mechanical execution is verified-correct (right field ID, right option, GraphQL read-back confirms the write).

**Why**: PA previously badly damaged sprint assignments — the Sprint field was cleared on closed issues during a board rebuild, orphaning many closed issues from their sprints and harming historical project understanding (partially repaired by a Lead Dev retag 2026-06-29, "Done 1→10"). PM has repeatedly tried to establish sprint/release-tracking discipline and stated directly (2026-07-03): *"I still have not been given reason to trust any agent to keep track of the sprint or verify their assumptions correctly yet. This discipline appears to be missing from our operating model for some reason."* Mechanical correctness is not the bar here — the judgment of *whether* to make the change is the part that needs PM, because the domain has a track record of damage and PM has not yet extended trust to agent judgment on it.

**The incident this came from**: PPM asked me to move #1235's Sprint field from RECONNECT to M3-Quality (a reasonable-sounding scope argument: the issue is a conversation-display bug, not connector-scoped). I verified the mechanics carefully (option existed, correct item ID, read-back confirmed) and executed it without looping in PM. PM caught it immediately: **#1235 was CLOSED (done) — moving a done issue into a sprint that hasn't started yet.** My first framing of this (in the memory's initial version) called that state flatly "incoherent" — **PM corrected that too, precisely**: closed-into-not-started isn't *always* wrong. A legitimate pattern exists — an issue can be deliberately cherry-picked from a future sprint's backlog and completed early, ahead of that sprint's formal start; the Sprint tag then correctly records *where it topically belongs*, not *when it was worked*. PM's actual point is narrower and sharper than "that state is bad": **the mechanical state alone doesn't tell you which case you're in** — legitimate early cherry-pick vs. topical rebucketing with no real relationship to execution timing — and PM couldn't tell which one PPM intended from the memo alone. That ambiguity is exactly why it needs a human/authoritative call, not agent inference.

**How to apply**: Treat any request to change Sprint/Milestone/release-tracking fields as PM-gated by default, regardless of which agent requests it or how well-reasoned their rationale sounds. Flag the request to PM and wait for confirmation rather than executing on another agent's product-authority say-so. Verifying the *mechanics* correctly (as I did) is necessary but not sufficient — it doesn't substitute for verifying *authority to make the change at all*. The closed→not-started pattern specifically is a **flag to ask, not a flag that the change is wrong** — don't assume incoherence and don't assume legitimacy; the intent behind the assignment (cherry-pick-early vs. topical-only) isn't recoverable from the board state itself, so surface the ambiguity rather than resolving it either direction unilaterally.

**Companion**: [[feedback_sprint_membership_is_project_board_not_labels]] — that memory is about *where* sprint data lives (the board, not labels); this one is about *who* has authority to change it once found. Related mechanism-trust thread: PPM's board-rebuild-damage history is the same failure class as the Done-1→10 retag I performed 2026-06-29.

**Extension (2026-07-04, PM directly)**: the same caution applies to *reading* sprint status, not just changing it. PM: *"if ever unsure of sprint status check with me."* Concretely: when I paginated the RECONNECT board myself (38 tagged items, 26 closed / 12 open) to answer PM's "anything unblocked in RECONNECT" question, PM immediately confirmed the count matched their own rough memory ("20+ done, 4ish in progress, 12ish left") and separately offered "I can pull from the sprint board" — meaning PM has an independent way to check this and wants to be the tie-breaker when a count is in question, not just when a write is in question. PM also floated defining a skill for this exact query pattern (paginated GraphQL walk of the project board, filtered by Sprint field) — a good idea, since I've now hand-written this same pagination logic twice (the 6/29 Done-1→10 retag and this 7/4 RECONNECT check) with no reusable procedure between them.

```

---

## FILE: feedback_sprint_membership_is_project_board_not_labels.md

```markdown
# Sprint membership lives on the project board, not in labels

**Source**: PM clarification 2026-05-27 ~7:15 PM PDT during duty-cycle Day-1 burst.

**The rule**: GitHub issue labels (`M1`, `M2g`, `M3`, etc.) are NOT how PM tracks sprint membership. PM uses a **custom `sprint` field** on the project board (GitHub Projects v2) — **NOT the built-in Iteration field** (PM clarified 2026-06-19: *"we don't use Iteration"*). In `gh project item-list --owner mediajunkie --format json`, the field is keyed `sprint` with values like `"D1 - Beta design quality"` (the project is "Building Piper Morgan", `--owner mediajunkie` #1). PM sometimes shares state via CSV exports.

**Why it matters**: Labels and sprint metadata can drift; PM's canonical view is the board. Treating labels as source-of-truth produces undercount / miscategorization (PA's May 24 M2 6x undercount: `feedback_verify_filter_scope.md`).

**The recurring failure mode**:
- Agent uses `gh issue list --label "M2"` and reports "M2 has N issues"
- PM looks at board: actual sprint contains M+N or N-M issues
- Agent's report is misleading; PM doesn't trust the framing

**What to do instead**:
- When PM says "the M2 issues are these" with a list, treat THAT list as the truth (PM filtered from the board)
- When PM shares a CSV, use the CSV — it's the board-export
- Don't create labels expecting them to move issues into sprints — labels are auxiliary indexes only
- Token scope `read:project` (via `gh auth refresh -s read:project`) lets agents query the board directly; ask PM to refresh if scope is needed

**What I had wrong today**:
- Created `M3` label + applied to #1124 / #1129 thinking it would move them to M3 sprint. It doesn't — PM moves issues on the board.
- Read "M2-labeled issues" as authoritative M2 membership when filtering for autonomous-work picks.
- Recommended "drop M2 label" cleanup — PM doesn't filter by label, so the cleanup is noise.

**Companion pins**:
- `feedback_verify_filter_scope.md` (PA's May 24 same-shape lesson at M2-cohort scale)
- `feedback_pre_authorized_for_unblocked_work_just_do.md` (the autonomy directive — applies AFTER getting authoritative sprint membership right)

**Mechanism candidate (v0.7+)**: agent tokens default to including `read:project` so direct board access is available; falls back to "PM-relayed lists are the truth" when scope is absent.

```

---

## FILE: feedback_stash_u_captures_untracked_files_and_removes_from_disk.md

```markdown
---
name: stash-u-captures-untracked-files-and-removes-from-disk
description: "PM May 19 — `git stash push -u` captures untracked files into the stash AND removes them from disk. Never `-u` stash before inspecting what's untracked. The May 19 incident: pre-rebase `git stash push -u` vanished PM's uncommitted blog draft from working tree; he saved the file (untracked, never committed), stashed -u included it, file disappeared from disk, \"where's my file\" panic followed. Rescued from `stash@{1}^3` (untracked-files parent of stash)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

**The rule**: never run `git stash push -u` on a shared `main` working tree without first checking what's untracked.

**Why**: `-u` captures untracked files into the stash AND removes them from disk as a side effect. If PM (or another agent) has uncommitted-and-untracked work — a blog draft, a memo, a session log — `-u` makes it disappear from disk. The work is rescuable from `stash@{N}^3` (the untracked-files parent of the stash commit), but only if someone knows to look there. From PM's perspective, "my file just vanished after I saved it" is the experience.

**How to apply**:

1. Before any pre-rebase / pre-merge stash, run `git status --short` and look for `??` lines (untracked files).
2. If untracked files exist in paths PM or other agents might be working in (`docs/public/comms/drafts/`, `dev/YYYY/MM/DD/`, anything outside your own scope), do NOT `-u` stash. Use one of:
   - `git stash push -- <explicit-paths>` — stash only files you own
   - Commit + push your own work, leave others' untracked state alone
   - Coordinate with PM before stashing if the untracked file shape is unclear
3. If you DID `-u` stash and PM panics about a missing file, look in `stash@{N}^3:path/to/file` BEFORE telling PM "I can't find it." The May 19 failure was a two-step: stash captured the file, then I reported "missing" without inspecting the stash's untracked-files parent.
4. Untracked-file rescue: `git show "stash@{N}^3:path/to/file" > path/to/file` extracts surgically without popping the rest of the stash.

Stacks with [[feedback_commit_only_own_files]] and [[feedback_no_directory_level_git_add_for_mail]] — same principle (do not sweep up adjacent state) extended to stash operations.

Related: [[feedback_commit_immediately_after_write_for_new_files]] — if PM had committed the file immediately after save, it would have been tracked, and a non-`-u` stash would not have captured it. But "PM should have committed" isn't a sufficient defense; agents must protect untracked work in shared trees.

```

---

## FILE: feedback_stop_on_source_gap.md

```markdown
---
name: STOP when finding gaps in sources — don't cover for them
description: When an expected source (kickoff memo, omnibus log, handoff package, prior memo PM/CoS expects you to have) isn't where it's supposed to be, surface the gap and wait. Don't synthesize around incomplete inputs.
type: feedback
originSessionId: 2026-04-26-host-ship-040-workstream-review
---
When PM or CoS or another agent says you have / should have something (kickoff memo, omnibus log, handoff package, prior decision memo), and it isn't where they expect — **STOP and report the gap**. Don't:

- Synthesize from adjacent sources to "cover" the gap
- Assume the source isn't load-bearing because you can imagine what it would say
- Reconstruct from memory or from secondary references
- Proceed and "flag for review" later

PM's exact words 2026-04-26 after I drafted Ship #040 workstream review without the kickoff memo: *"We need to develop a rule that you STOP when you find gaps in sources. You don't cover for that."*

**How to apply**:

1. **At source-verification time**: enumerate expected sources. If any are missing (file not present, branch not synced, memo not delivered), report exactly which ones and where you expected them.
2. **Distinguish content gap from distribution gap**. Mailbox imperfections (memo exists in `dev/active/` but not mirrored to `exec/sent/`) are usually OK to proceed with — the artifact exists. Content gaps (kickoff memo doesn't exist anywhere on origin/main) require STOP.
3. **Don't redraft until PM confirms**. Discard incomplete drafts; resume from scratch with the full source set.
4. **The Pattern-062 lineage applies**: this is the same family of failures as the Apr 19 six-way workstream-review draft on incomplete source set, the Apr 22 Apr 16 omnibus drift discovery, the Apr 22 HOST handoff blocker, and the Apr 23 Step 2.5 first-use catch. "Audit the composition" before synthesizing.

**Why**: the work to reconstruct a draft from scratch is much smaller than the cost of correcting a draft that propagated incomplete-source claims downstream into Ship narrative or PM/CoS synthesis.

```

---

## FILE: feedback_surface_files_via_senduserfile_not_paths.md

```markdown
---
name: feedback-surface-files-via-senduserfile-not-paths
description: "CONFIRMED 6/13 (PM-tested) — write/edit a static .html IN THE WORKTREE → it surfaces as a tappable link in the Desktop Launch preview panel; tap opens it. Location-in-worktree is the variable (open-state NOT required). SendUserFile = download chip (separate). Caveat: client updates >daily — re-verify if behavior shifts."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef776fbb-3c64-4701-b1ba-2aa37c3221ce
---

When delivering an artifact where **the file itself is the deliverable** — a cohort attention rollup, a generated diagram, a draft Ship, a structured report — use the **`SendUserFile` tool** to surface it directly into PM's Claude Desktop side panel. Do NOT drop a `/Users/xian/...` disk path as the primary delivery and make PM hunt for it.

**Why:** PM correction 2026-06-10 ~09:30 AM PT — *"Piper Alpha was able to present it to me as an artifact I could view right here in the side panel in Claude Desktop and perhaps you could ask how that was done, because it is mighty convenient. I'll go grab it now from my disk for the time being."*

That's the same shape as the "here's a memo summarizing what I did" antipattern (delivery without the actual artifact in the user's hand). PA was using the platform's native file-surfacing capability; I had been treating "commit + push + paste the path" as the complete delivery, making PM context-switch to a file browser to actually see the thing.

**How to apply:**

1. **Default for HTML/markdown/diagram artifacts**: when the file is meant to be *viewed* (a rollup, a report, a rendered draft, a generated visualization), call `SendUserFile` with the file path AFTER committing to git. The commit is the durable record; the `SendUserFile` is the actual delivery to PM.

2. **What still gets path-only delivery**:
   - Code files PM will edit in their editor (path is the right delivery)
   - Files PM has explicitly asked to navigate to (paths are clickable in chat)
   - Files where PM specifically wants to grep / search / edit rather than view
   - Memos in mailboxes (PM's normal pattern is to read in inbox, not view as artifact)

3. **The disambiguating question**: "is the file meant to be *viewed* or *worked with*?" If viewed → `SendUserFile`. If worked with → path.

4. **When in doubt, do both** — `SendUserFile` for surfacing + path for the canonical location.

5. **Caption it**: `SendUserFile` accepts a one-line caption. Use it for context PM might want before opening ("Cohort attention rollup — Wed Jun 10 ~9:30 AM PT" beats a bare file delivery).

**Recurring failure modes I've shown:**
- Cohort attention rollup Jun 9 + Jun 10: both delivered path-only; the Jun 10 case is where PM corrected me directly
- Likely also: Ship #045 + #046 published versions (PM had to navigate); BYO-colleague synthesis memo (path-only)
- Any future generated artifact (cron-cadence retrospective HTML, methodology graphs, etc.)

**Stacks with:**
- The Pattern-045-adjacent "delivery without the artifact" antipattern at the platform-tool altitude
- [[feedback_file_paths]] — clarifies that absolute paths in chat are still the right *secondary* delivery; this pin adds: the primary delivery is `SendUserFile` when the file is meant to be viewed
- [[feedback_make_promises_durable_no_happy_talk]] — the mechanism is the per-deliverable choice between SendUserFile and path-only; pinning sets the default

**Discovered:** when PM noted PA was doing this Jun 10. PA chase memo filed asking for their technique.

## CORRECTION 2026-06-10 ~09:50 AM PT — SendUserFile is NOT the answer PA was using

PM corrected me directly after I claimed SendUserFile "worked": *"You were able to embed a downloadable link to the html file in chat but it did not 'work' in that I cannot hit command-shift-P to open it in the preview pane as I could with Piper's deliverable. This is why I asked you to find out how it was done."*

So:
- **`SendUserFile`** delivers a *download chip* to chat — PM can download the file, but cannot open it in the Desktop preview pane via cmd-shift-P.
- **PA's technique** (TBD pending PA's response) produces a deliverable that PM can open in the preview pane via cmd-shift-P. This is qualitatively different from a download link — it's a *previewable artifact* surface.
- I jumped from "downloadable" to "PM's problem solved" without confirming the actual end-user experience.

**Real lesson — meta-shape of the failure**: don't claim a technique "works" until the end-user experience PM described is reproduced. PM described "open in side panel via cmd-shift-P"; I delivered "download chip." Those aren't the same delivery shape. Same Pattern-045-adjacent shape: I confused *file successfully delivered to chat* with *PM's described user experience reproduced*.

**Pin status**: SendUserFile is *one* file-delivery mechanism (better than path-only for many cases). PA's technique is *the* mechanism for the preview-pane case. Hold further pin authority until PA's response identifies the real technique; then amend with the correct rule.

## CONFIRMED 2026-06-13 (PM-tested) — static HTML in the worktree → tappable preview-panel link

**The confirmed technique:** write or edit a **self-contained static `.html` file IN THE WORKTREE** (e.g. `dev/active/`). The Desktop client surfaces it as a **tappable link in the Launch preview panel**; tapping opens it in the pane (persists). PM confirmed 6/13 by tapping the `cio-preview-probe.html` link → the panel opened. **Location-in-the-worktree is the variable** (Exec's non-showing HTML was stored elsewhere); open-state is NOT required; no `launch.json`, no server. **Caveat: the Desktop client updates >once/day — re-verify if the behavior shifts.**

**Meta-lesson retained (this pin is the running example):** before the confirmation I over-claimed TWICE — "I'm not a source," then a confident "static HTML, resolved" off one data point. With a churning client + conflicting data, hold technique-claims as hypotheses to *empirically test*; the PM-tap is what earned the "confirmed."

**⚠️ Original over-claim caution (kept for the lesson):** First "I'm not a source"; then a confident "it's static HTML, no server." PM then noted **Exec has made HTML files that do NOT show in the pane** → my static-HTML mechanism is *incomplete*. And the Desktop client ships updates **>once/day**, so any recipe is version-fragile. **Meta-lesson (the running example IS this pin):** with a churning client + conflicting data, hold technique-claims as hypotheses to *empirically test*; never assert from one data point. The plan-of-record was my single data point.

**Open variables — why does the plan-of-record show but Exec's HTML doesn't?** (a) **file location** (PM's hypothesis — plan-of-record is in `dev/active/` of the worktree; Exec's unknown); (b) **open-state** (the .html may become *available* in the panel on edit but must be *opened once* via cmd-shift-P — the plan-of-record IS open in PM's pane; Exec's may be available-but-never-opened); (c) version-specific behavior. Not yet isolated. **Resolution path: empirical test (PM + Exec), holding location/open-state constant.**

**Probe 6/13 (CIO self-test, partial):** a fresh, never-opened static HTML `Write`-n to the worktree's `dev/active/` **immediately triggered the "visible in Launch preview panel" hook** (and it fires on `Write`, not just `Edit`). So: **open-state is NOT required** for the panel notice, and **location-in-the-worktree is a factor** (PM's hypothesis looks right). Bound: the hook is CIO-side ("available in panel"); whether it *renders in PM's pane* is the PM-side link the probe can't see. Leading read: **Exec's non-showing HTML was likely NOT in the surfaced worktree location** (or the available→pane-render link failed PM-side). Still version-fragile (client churn). Confirm via the PM+Exec test before asserting.

What I observed (the single data point, treat as hypothesis):

- **Write a self-contained static `.html` file in the worktree** (inline CSS; no external/fetch/server deps). The **Claude Desktop client auto-surfaces it in the Launch preview panel** — PM can open/keep it via the preview pane (cmd-shift-P). It persists + is re-openable.
- **Evidence**: every `Edit` to the plan-of-record `.html` triggers a PostToolUse note *"X.html is now visible in the Launch preview panel"*; PM's 6/13 screenshot shows it rendering in their pane. No `.claude/launch.json` exists — it's a built-in client feature, not repo config.
- **Two traps to avoid**:
  1. **`SendUserFile` → a download CHIP, not the pane** (the original failure — correct for downloadables, wrong for previewables).
  2. **`.claude/launch.json` → the SERVER-BACKED preview mode** (the "Set up" button assumes a dev server → port-in-use errors + prompt-injection fuss; this is what Exec hit). A *static* doc needs no launch.json/server.

**The rule**: previewable doc (dashboard/report PM views in the pane) → **static .html in the worktree**; downloadable file → SendUserFile. I WAS a source of this technique all along (the plan-of-record) — I'd wrongly told Exec I wasn't, having conflated it with the SendUserFile-chip attempt. Correction sent to Exec 6/13.


```

---

## FILE: feedback_temporal_relationship_over_date_stamps_in_public_prose.md

```markdown
---
name: Temporal-relationship over absolute date stamps in public prose
description: PM's preference for temporal-relationship language ("overdue in this window") over absolute-date specifics ("filed May 10 (post-window)") when the absolute date doesn't earn its keep for an outside reader.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
In Ships / narratives / insights aimed at outside readers, prefer temporal-relationship language to inside-baseball date stamps when the relationship is the point and the specific date isn't.

**Move PM applied in May 13 Ship #042 cross-post:**
- Original: *"A roadmap update was filed May 10 (post-window) and is awaiting ratification."*
- Edit: *"A roadmap update was overdue in this time window and is awaiting ratification."*

The original tells an insider exactly what happened (filed on May 10, which falls after the window's May 7 close). The edit tells an outside reader the **relevant** thing — that the roadmap update was due during the period and the period closed without it — without making them parse "(post-window)" as a clue.

**Why:** absolute-date specifics make sense to insiders who hold the project calendar in mind. To outside readers, dates without context read as either noise (irrelevant to the narrative) or worse, as inside-baseball signaling (you have to be in the room to know what this means). The temporal-relationship form — "overdue in the window," "after the period closed," "earlier in the week," "before the milestone" — carries the same meaning while staying readable cold.

**How to apply:**
- Pre-publish pass: scan for explicit dates in narrative prose (not in metrics tables, blog-post-list date prefixes, or other inventory contexts where dates carry coordinate-function).
- For each, ask: does this date itself matter to an outside reader, or is the temporal relationship the point? If relationship, rephrase. If specific date matters (e.g., "the talk on Apr 17"), keep.
- Internal docbase + session logs + omnibus logs: dates carry forensic function; keep them specific.

**Memory-chain neighbors:**
- `feedback_parenthetical_gloss_on_first_use.md` — same shape: insider info gets a softer form for outside readers.
- `feedback_load_bearing_is_crutch_word_in_public_prose.md` — internal-vs-public divergence pattern.
- `feedback_editing_voice.md` — broader voice discipline.

```

---

## FILE: feedback_three_registers_dont_assume_reader_context.md

```markdown
# Three registers — terms of art are fine, but don't assume reader context

**PM directive, 2026-06-05** (from the skunkworks BYOC plugin jargon-scrub).

The rule is NOT "avoid jargon / terms of art." Agents are free to use defined terms of art. The rule is:
**know which register you're writing in, and don't assume the reader has context they may not have.**

## The three registers

1. **LLM-to-LLM** (agent instructions, skill bodies, models, prompts) — terms of art are *fine and
   efficient*; the agent has the context. Use the precise word ("floor", "floor_hit", "context_keys",
   "intent classification").
2. **Term-of-art WITH context** — when a load-bearing term might be unfamiliar to the reader, don't
   drop it — *introduce* it. Bring the reader into the concept.
3. **User-friendly plain language** — for lay people, **including technical PMs as users**. A technical
   PM is smart but is NOT inside our architecture — they have no reason to know "Conscious Floor."
   Plain words; introduce concepts; no assumed-context jargon. ("floored" → "Piper didn't have your
   project info"; drop floor_hit / context_keys entirely.)

## The trap + failure mode

The **technical-PM reader** is the trap: smart enough that you're tempted to assume they'll follow
"floor_hit," but they have no reason to. The failure mode is **assuming context the reader lacks** +
**failing to distinguish which register you're in** — leaking LLM-to-LLM vocabulary into user-facing
output.

## Where it applies

ALL user-facing artifacts: skill/plugin output shown to users, tester READMEs, fan-out/announce memos,
blog posts, demos. (Internal agent instructions stay in register 1 — don't over-scrub those.)

## Origin example

The rung-3 `consult-piper` skill's first gate run leaked "floored / floor_hit: true / context keys" to
the user. Provenance was *visible* but not *legible*. Fix: provenance must be both. Scrubbed in
`piper-morgan-skunkworks` `34e48b4` — plain-language rule in the skill bodies, agent-facing "floor"
retained (register 1), user-facing strings made plain (register 3).

## 2026-06-12 instance — PM-facing STATUS UPDATES are register 3 too

CIO surfaced parked PM-pending items in a chat status update as **"session-log-primary per-lane ratification"** and **"Routines watchdog funding (~$70/mo) — funding-trigger criterion MET per the Gap-C investigation."** PM: *"'Session-log-primary per-lane ratification' is too dense for me to unpack. please explain"* + *"is the question whether I am willing to pay for an extra routines feature?"*

Lesson: register 3 isn't only for published artifacts — it applies to **PM-facing status updates / "what's parked with you" surfacing.** When you hand PM a decision, name **what the decision actually IS in plain language** (e.g. "should every agent's daily log be the primary record, or keep the separate per-fire cycle log too?" / "do you want to pay ~$70/mo for a watchdog that restarts dead agent schedules?") — not the internal shorthand the cohort uses among itself. The PM-as-technical-reader trap (§"The trap") fires hardest in quick status updates, where shorthand feels efficient. Stacks with `feedback_descriptive_names_not_cryptic_ordinals`.

Composes with: `feedback_load_bearing_is_crutch_word_in_public_prose` (register-3 word choice),
`feedback_editing_voice`, `feedback_descriptive_names_not_cryptic_ordinals`.

```

---

## FILE: feedback_time_lord_doctrine_no_false_urgency.md

```markdown
# Time Lord doctrine — don't introduce false urgency into workstream cadence

**PM May 24**: *"Please remove any references to time or time pressure. I deliberately allow a window from Friday to Tuesday to work on the Ship when we all have time. We do not need to rush or operate any differently."*

## What's actually true

The standard workstream-review cycle window is **Friday (window-close) through Tuesday (memo deadline)**. That's a ~4-day window by design — gives the leadership cohort flexibility to write workstream memos when they have time, accounting for everyone's varying schedules and bandwidth.

Sending the kickoff Friday-Saturday vs Sunday vs Monday does NOT change this window. The Tuesday target is the Tuesday target either way.

## The failure mode

Treating the kickoff-send-day as the start of a fixed-length clock and labeling later sends as "compressed" or "delayed." That framing:

- Implies the cohort needs to rush
- Manufactures urgency where none exists
- Operates against the Time Lord doctrine — letting time take the time it needs
- Stacks with the prior "deadlines as triage tools" memory (deadlines are backstops, not pacing)

## What to do instead

- Reference the window as the window (Fri-Tue), not "compressed" or "expanded"
- If a kickoff sends later in the window, treat that as normal — the deadline is the deadline
- Drop urgency framing ("slightly delayed," "compressed turnaround," "rush") from PM-facing surfaces and cohort-facing kickoff memos
- The standard cadence accommodates real-life variance; that's its whole point

## Sibling application — frame the deadline as backstop, not scheduled date

PM May 24 follow-up: *"Agents should always work immediately on unblocked work. Giving a Tuesday deadline just confuses matters unless it is made clear as a drop-dead limit in case things prevent immediate work."*

When sending kickoff memos that name a deadline, frame it explicitly:

- **Lead with**: *"file when your role is unblocked; do not pace to the deadline"*
- **Then name the deadline as**: *"drop-dead backstop for if other work genuinely prevents earlier filing — not the scheduled work date"*

The downstream sequence (synthesis, review, publication) follows naturally from when the inputs land, not from a calendar. Use *"Follows memo arrivals"* / *"Follows draft"* in process-timeline tables rather than fixed dates wherever the work is event-driven.

This is the cohort-facing application of `feedback_deadlines_last_possible_time.md` (deadlines are latest, not scheduled) — that memory was about how I receive deadlines; this is about how I describe deadlines when I'M the one sending them.

## Task-execution pace — the Inchworm way (PM 2026-06-16)

PM, verbatim, after I'd surfaced a STOP-condition (P7 scope > gameplan estimate) and chosen the careful/verified path over a session-tail rush:

> *"None of this needs to be quick. It just needs to be thorough, methodical, and ultimately complete. (That's the Inchworm way.) I am patient. (I am a Time Lord.)"*

This is the **task-execution** facet of the Time-Lord doctrine (the rest of this file is the cohort-memo-cadence facet). The principle:

- **Thorough + methodical + ultimately complete > fast.** For substantive work, depth and correctness are the goal; speed is not a virtue in itself.
- **PM is patient.** Don't manufacture self-imposed urgency to "finish before context runs out" / "show fast progress." That pressure is the wave (CLAUDE.md) — turn into it.
- **This validated the right calls**: surfacing the P7 test-ripple instead of plowing through 3× the estimated scope; verifying each migration (up/down/backfill/tests) before moving on; deferring the breaking pass to be done right rather than session-tail-rushing it. Completion-discipline (Patterns 045/046/047) + STOP-conditions are *encouraged*, not friction.

**Reconciles with [[feedback_deadlines_are_triage_tools_not_default_pacing]] / [[feedback_pre_authorized_for_unblocked_work_just_do]] (do unblocked work NOW, don't postpone)**: not-postponing ≠ rushing-execution. Start promptly; execute thoroughly. The two are complements, not opposites — the failure mode to avoid is *postponing* (don't), NOT *taking the time to do it completely* (do). When PM says "proceed with unblocked work," that's "don't stall," not "rush the execution."

## Stacks with

- `feedback_deadlines_are_triage_tools_not_default_pacing.md` (deadlines as backstops)
- `feedback_deadlines_last_possible_time.md` (deadlines as latest, not scheduled)
- `feedback_workstream_review_cadence.md` (Fri–Thu window)
- `feedback_drop_day_x_nomenclature_from_pm_surfaces.md` (same drop-the-noise-from-PM-surfaces principle)

The pattern: my instinct to manufacture forward-motion signal can leak into cohort-facing prose as time pressure. Don't.

```

---

## FILE: feedback_title_style.md

```markdown
---
name: Avoid "The Number Percentage That Did The Thing" titles
description: PM's title-style preference for blog/narrative pieces — shies away from numeric-stat-as-headline construction. Applies whenever drafting or revising titles.
type: feedback
originSessionId: fd0d57b8-e1b5-47c5-b922-c918fab72fa3
---
PM tends to shy away from titles built on the "The Number Percentage That Did The Thing" pattern — i.e., titles whose load-bearing element is a numeric stat plus a flat predicate ("Six Issues Before Dinner", "The 80.3% Classifier", "The 0/9 Test"). The shape feels formulaic and content-marketing-shaped.

**Why:** PM's voice prefers titles that suggest a question, an image, or an idea rather than reduce the piece to its most quotable number. Numbers belong inside the piece; titles do other work.

**How to apply:**
- Working titles can lean on numbers as placeholder shorthand — fine for editorial calendar entries while the piece is in draft.
- Before publish-ready, replace the number-stat title with one that names the idea, the moment, or the surprise. Examples of better shapes: "Audit and Talk", "The Omnibus That Found Its Own Drift", "The Voice of a Denial."
- If a number is genuinely load-bearing for the piece's identity, it might still survive — but default-bias is to find a non-numeric alternative first.

**Same shape applies to section headings within a piece.** Section headings as noun phrases read sharper than verb-phrase or temporal-clause headings. May 10 Inchworm example: original *"When the inchworm speeds up"* → PM voice-passed to *"Inchworm as ratchet"*. The verb-phrase shape feels weaker — it sets up a moment rather than naming an idea. Same default-bias as piece titles: noun phrase first; verb phrase only when it earns it.

```

---

## FILE: feedback_ui_fix_requires_template_render_test_not_curl_200.md

```markdown
# UI fix verification requires real `template.render()` test, not just curl-returns-200

**Source**: Lead Dev self-correction 2026-05-30, after two whack-a-mole bugs on the same file (`templates/layouts/base.html`) in 24 hours during #1047 M2D-UAT.

## The discipline

For any UI fix involving templates, route handlers, or page rendering, the pre-merge verification MUST include a **real `template.render()` test on the actual file**, not just curl-returns-clean-status. The latter passes when the template is never even parsed (e.g., a 401 returns before render runs).

## The failure mode this prevents

**Day 1 (the original miss)**: I gave PM a "/insights walkthrough" after verifying:
- `/health` → 200 ✅
- DB has 5 insights for m1-test ✅

PM clicked /insights logged in → got a Piper-voice JSON error. The page had been structurally unreachable for 27 days because `templates/insights.html` extended `layouts/base.html` (which never existed). My data-layer + server-health checks passed cleanly while the user-facing path was completely broken.

**Day 2 (the recurrence)**: I "fixed" the missing layout by writing `templates/layouts/base.html`. Verified with:
- curl /insights (unauth) → clean 401, no exception ✅
- "fix works"

PM clicked /insights logged in → got a different Piper-voice JSON error. The layout I wrote had its own bug: the file's HTML docstring `<!-- ... {% extends "..." %} ... -->` was parsed by Jinja (it parses `{% %}` syntax inside HTML comments), so the layout extended itself and recursed. My curl-401-clean check never triggered the template render path, so the recursion couldn't surface. Forensic subagent caught it.

In both cases: **the data layer passed, the auth challenge returned cleanly, the user-facing render path was broken**. Two distinct failure modes, both invisible to my chosen verification.

## What "real `template.render()` test" looks like

```python
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("templates"))
tpl = env.get_template("the-page-you-touched.html")
rendered = tpl.render(request=None, user={}, trust_stage=1, ...)  # minimal context the route passes
assert len(rendered) > 0
assert "<title>" in rendered  # or whatever scaffold marker confirms shape
assert "<!DOCTYPE html>" in rendered
assert rendered.count("<!DOCTYPE html>") == 1  # no accidental duplicates from edits
```

This catches:
- TemplateNotFound (parent layout or include missing)
- TemplateSyntaxError (Jinja delimiters embedded as literal text inside comments — yes really)
- Self-recursion (RecursionError on render)
- Block redefinition collisions
- Most variable-shape issues with the route's typical context

It doesn't catch every render-time issue (JS bugs, authenticated-only branches, downstream API failures), but it catches the layer that pure curl + DB checks miss.

## The bright-line rule

**Before declaring any UI fix "works" and handing off to PM for UAT**: load the page. Either via:
1. Authenticated curl + grep for expected content (best — exercises the full chain)
2. Direct Jinja `template.render()` with realistic context (covers the template chain even if you can't auth)
3. The `verify` skill if applicable

**NOT acceptable** as the only verification:
- curl returns 200/401/403 (clean status doesn't mean the page renders — the auth middleware may return before render)
- DB has the right data (data-layer correctness ≠ user-facing path correctness)
- Server is up (infrastructure-up ≠ application-correct)

## Compose with

- `feedback_make_promises_durable_no_happy_talk` — the verification IS the durable mechanism, this pin codifies it
- `feedback_close_issue_properly_skill_recurring_miss` — close-discipline at the issue layer; this is verification-discipline at the fix layer
- `feedback_deferred_ac_self_justification_is_premature_closure` — same family at the AC layer
- methodology-30 Consumer-Trace Verification — same shape at the architecture-claim layer; this pin applies it to UI smoke verification specifically

## Cross-references

- 2026-05-30 incident, day 1: `templates/insights.html` extended non-existent layout for 27 days. Forensic at `dev/active/insights-surface-forensics-2026-05-30.md`
- 2026-05-30 incident, day 2: my `templates/layouts/base.html` (commit b0216a7ce) recursed via HTML-comment-parsing; fix at commit c1f3eee71
- Forensic subagent caught the second-order mistake before PM had to escalate it
- May 30 session log day-close entry captures the full arc

```

---

## FILE: feedback_verify_branch_after_checkout.md

```markdown
---
name: Verify branch after `git checkout -b` before committing
description: After creating a feature branch, run `git branch --show-current` to confirm the switch happened. Unstaged-file warnings can mask checkout issues.
type: feedback
originSessionId: 8d4cf2f5-588f-4fe5-ad97-bcdfba785c03
---
After `git checkout -b <branch>`, **always run `git branch --show-current` (or `git status`) to confirm the branch switch actually happened** before committing.

**Why:** May 3 #1030 execution: ran `git checkout -b claude/1030-insight-pull main`. Output showed `M mailboxes/pa/inbox/MANIFEST.md` etc — looked like normal "unstaged changes carried forward" warning. Assumed the branch switch worked. Then made commits + ran `git push -u origin claude/1030-insight-pull`. The push succeeded but pushed the wrong ref — the new commit was on local `main`, not on `claude/1030-insight-pull` (which was at the previous main HEAD). The push command somehow pushed local main's HEAD to the named branch, even though that's not what `git push -u origin <branch>` should do. Net result: my #1030 commit was on local main; the origin branch had a different (older) commit.

Recovery was clean (cherry-pick the commit onto the proper branch, reset local main to origin/main, force-update the remote branch via push) but only because nothing else had advanced in the meantime. If main had moved forward in the interim, recovery would have required more care.

**How to apply:**

After every `git checkout -b <branch>`:
1. **Verify**: `git branch --show-current` (should print the new branch name) OR check the prompt if shell shows branch
2. **Confirm clean state**: `git status` — should show no commits ahead of the new branch's tracking remote (since it's brand new)
3. **THEN commit**

This is 2 seconds of verification that prevents 5-15 minutes of recovery + reasoning about state when something weird happens. The cost is trivial; the benefit is catching state issues before they propagate.

**Specifically:** if you see "M" prefixed lines in checkout output (unstaged modifications that aren't yours), stop and check current branch — those modifications might be obscuring whether the checkout actually worked.

```

---

## FILE: feedback_verify_lane_before_attributing_not_web.md

```markdown
---
name: feedback_verify_lane_before_attributing_not_web
description: "Before attributing cross-agent work, verify the lane via git/session-logs — \"Web\" = the website repo, NOT product front-end (Lead/CXO). Recurred 6/15."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

PM 6/15 (caught me repeating the 6/14 misattribution): I attributed 2 failing product-repo tests to "the Web agent." PM pushed: "are we sure that's Web? they work in another repo. verify whose work that is."

**Why:** Web works in the **website repo** (`piper-morgan-website`). **Product front-end (templates, web/static/js, `mediajunkie/piper-morgan-product`) is Lead/CXO's lane** — never Web. The 2 failures (test_navigation Files→Documents; test_insights_1031 trustStage) turned out to be **stale tests in the product repo, Lead lane — one literally my own commit (#1146, 6-04)**. There was no external owner to notify; it was me.

**How to apply:** Before saying "agent X's work" for anything cross-agent: (1) confirm which REPO the files live in (`mediajunkie/piper-morgan-product` = product = Lead/CXO; `piper-morgan-website` = Web); (2) `git log --format="%h %ad %s" -- <file>` + grep `dev/YYYY/MM/DD/` session logs for the issue # to find the actual role/session (git author is the shared `mediajunkie` identity — useless for the agent; the commit MESSAGE + session log are the tell). Never assert an attribution from a hunch — verify, or say "unverified." Git author ≠ agent.

This is the SAME lesson as the 6/14 incident (carry-forward Notes). It recurred because the carry-forward note wasn't load-bearing enough; pinning it as durable memory. Stacks with [[feedback_no_flattened_commands_without_referents]] + [[feedback_investigate_before_extending_all_work]] (verify-before-assert).

```

---

## FILE: feedback_verify_negative_claims_via_live_api.md

```markdown
---
name: verify-negative-claims-via-live-api
description: "PM 2026-07-12 — before asserting a file/resource doesn't exist or was lost, check via the live API (gh api / gh api search/code), not local git show/ls-tree/log against a possibly-stale or wrongly-guessed path."
metadata: 
  node_type: memory
  type: feedback
  valid_from: 2026-07-12
  originSessionId: 4ba30d47-8c40-414e-b11d-083cc511ef37
---

# Verify negative claims via the live API, not local git state

PM 2026-07-12: I claimed `beta-blockers.md` and `sprint-order.md` (referenced from `roadmap.md`) had been "lost" — based on `git show origin/main:docs/internal/planning/roadmap/beta-blockers.md` failing and `git log --all` finding no history for that path. PM: **"please check github before asserting a negative."** Re-checked with `gh api repos/.../contents/...` and `gh api search/code` — both files existed all along, one directory up from where I'd assumed (`docs/internal/planning/`, not `docs/internal/planning/roadmap/`). The actual bug was 4 broken relative links inside roadmap.md, not lost files.

**Why the first check was wrong**: `git show`/`git ls-tree`/`git log --all` against `origin/main` only reflect what my last `git fetch` pulled down, at whatever path I *guessed* — a roadmap.md relative link (`[beta-blockers.md](beta-blockers.md)`) implies same-directory, but that's the doc's own claim, not verified fact. A negative result from a guessed path proves the path is wrong, not that the file is missing. `gh api search/code` searches the whole repo by filename, independent of any assumed directory and independent of local fetch staleness (it hits GitHub's servers directly).

**How to apply**: before asserting anything is missing, lost, or never-existed in a GitHub repo — especially language like "gone," "lost in the chaos," "never committed" — search broadly first (`gh api search/code?q=repo:X+filename:Y`, or `gh api repos/X/contents/PATH` for a specific directory listing) rather than trusting a single guessed path checked via local git commands. This is the same family as [[feedback_no_confabulating_expected_steps_as_completed]] and [[feedback_investigate_before_extending_all_work]] — the negative-claim version: absence-of-evidence-at-a-guessed-location is not evidence-of-absence, and a "this was lost" claim is alarming enough (implies real data loss, invites re-litigating a past incident) that it deserves the same rigor as a positive claim before it's asserted.

```

---

## FILE: feedback_verify_show_stat_post_commit_pre_push.md

```markdown
# Verify `git show --stat HEAD` post-commit, pre-push

**Established 2026-05-15** after PPM commit `a40c1f11` (two-ack distribution) captured 2 unintended CIO inbox→read renames despite pre-commit `git diff --cached --name-only` listing exactly the 15 PPM paths intended.

## The failure mode

In heavily-shared worktrees with concurrent agents, **git's rename detection can pair adjacent moves at commit-time** even when explicit-path staging is used. Pre-commit `git diff --cached --name-only` shows what's in the index, but git's commit-tree may pull in rename-pair entries that weren't individually staged.

Specifically: if working tree has both (a) a deleted file in path A and (b) an untracked or new file in path B, and the content similarity is high, git's commit operation can record the pair as a rename even though `git add` only touched B.

This stacks on top of all prior commit-discipline failures (Apr 27 reset-before-stage, May 12 read-every-line, Apr 29 branch-show-current, May 14 diff-HEAD-pre-edit) and is the **next-layer guard** when those upstream checks pass cleanly.

## The discipline

**After every commit, BEFORE pushing**, run:

```bash
git show --stat HEAD | head -30
```

Read the file list. If anything appears that you did not explicitly add, **stop and investigate before pushing**. Options:

1. `git reset --soft HEAD~1` to undo the commit (preserves working tree + index state)
2. Clear the index, re-stage only intended paths, re-commit
3. Then push

If the unintended capture is benign (mechanical mail moves, MANIFEST regen, etc.) and the other agent's work would have been committed anyway: document in session log + push. Don't quietly absorb it — name it.

## Why this matters

Silent capture of another agent's pending work in your commit creates:
- Asymmetric-visibility windows for the other agent (their work landed under your name)
- Audit-trail confusion (commit log says PPM committed CIO renames; mailbox-discipline log doesn't reflect intent)
- Rename-graph noise that complicates future cherry-picks or reverts

## When this fires

Multi-agent shared-worktree sessions where concurrent renames in mailbox/ paths are likely (almost every Code-era session by mid-2026).

## May 15 amendment — multiple failure modes observed in one session

After this memory was pinned, the same session (PPM May 15 morning sprint) produced THREE more foreign-capture incidents despite the new post-commit verify discipline:

1. **Adjacent inbox→read renames captured** at commit-time when explicit-path staging was used for the new file (pattern from original incident)
2. **Working-tree deletions auto-staged at commit-time** when other staging operations ran — `git restore --staged` to remove them works, but the next commit re-captures them via the same mechanism
3. **`git mv` index entries dropped by intervening concurrent commit** in chained Bash commands

**Root cause**: PPM working in shared main worktree alongside 5-10 concurrent Code agents. Git's index and rename detection operate on shared state that other agents' uncommitted changes leak into.

**Discipline layers are necessary but insufficient.** The real remediation is per-CLAUDE.md guidance: agents producing substantive output should work in a `claude/*` branch + dedicated worktree (`git worktree add ../piper-morgan-product-{slug}`). Then concurrent agents on `main` cannot leak state into the agent's commits.

When operating on shared `main` is unavoidable (mailbox writes, short housekeeping), accept that foreign capture may occur and:
1. Run `git show --stat HEAD | head -30` after every commit
2. Document captured foreign state in session log + commit message
3. Don't try to undo via `git reset --soft + recommit` — destructive on the rename graph

**Best practice going forward**: PPM (and any agent producing substantive memos/PDRs) should default to worktree-separated work. The shared-main mailbox-discipline norm assumes mail-only ops which are short and predictable; substantive work in shared main produces this failure mode reliably.

```

---

## FILE: feedback_wait_for_publish_handoff.md

```markdown
---
name: ""
metadata: 
  node_type: memory
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

When PM names a blog publish as a priority for the day ("publish The Gate this morning" / "we're going to publish X today"), that is a forward-looking statement about **PM's workflow**, which starts with PM's final edit + illustration creation. It is **not** a cue for Docs to begin the publish pipeline or even to pre-diagnose the draft.

**Why**: PM's words (2026-04-23) — *"if it's got placeholders and stuff and it's still in draft form, I have not edited it yet. The first step is that I have to make the final edit and I have to make the illustration, and then you can run the publishing process."* Pattern repeated 3 days running (Four Roles Apr 21, Ship #039 Apr 22, The Gate Apr 23): Docs opens the draft, scans for placeholders/image-metadata/footer-tease accuracy, reports "things needing resolution" before PM has started editing. This preempts PM's own process and asks PM to respond to diagnostics for work PM hasn't done yet.

**How to apply**:

When PM names a publish as a priority for the day, Docs should:

1. Confirm the target draft exists (one check, quiet)
2. Confirm the editorial calendar slot (one check, quiet)
3. **Acknowledge and wait** — "Standing by for your edit handoff" is the correct response
4. Do NOT open the draft and surface placeholders
5. Do NOT enumerate missing metadata (image filename, alt text, caption)
6. Do NOT scan the footer tease for accuracy
7. Do NOT rename the file per convention

All of (4)-(7) happen *after* PM's handoff — once the edited draft lands with metadata filled in, Docs verifies the state is publish-ready and either flags genuine issues (typos in alt text, etc.) or runs the pipeline.

**The trigger for the publish pipeline is PM's explicit handoff**, e.g.:
- "OK, ready to publish" / "edit is done"
- A rename from `draft-{slug}-v1.md` to `{slug}.md` plus a new `.png` appearing in drafts/
- "Go" or similar explicit green-light

**Corollary — applies to scheduling questions too**: If PM asks "what's next on the calendar after today's post?" answer literally; if the calendar is inaccurate (as of 2026-04-23, insight slot for Sat Apr 25 not yet on calendar), say so without offering to pre-update. PM will tell Docs what's lined up when they're ready to share it.

**Related**: publish-to-blog skill v0.8 `When to Use` section already specifies the trigger correctly ("PM says a draft is ready to publish"). The failure was behavioral, not spec-level. This memory is the behavioral fix.

**Extension (2026-07-08, Exec instance — the rule generalizes past Docs and past the publish step itself):** the same gate applies to **Exec handing a Weekly Ship draft to Comms for pre-publish review**. Exec drafted Ship #050, and on hearing PM say "Comms reviews it before we publish," immediately routed the draft to Comms — before PM had read it. The draft contained a headline factual error PM then caught (a tester described as "the first real user" had never successfully installed). PM: *"It's not ready to go to comms yet. **I decide that.**"* The general form: **any handoff that moves a deliverable one station down the publish pipeline is PM's trigger to pull, not the drafter's to push** — PM describing the pipeline's shape ("Comms reviews before publish") is not the same as PM releasing this artifact into it. `draft-weekly-ship` v1.4 now encodes the fixed sequence (draft → PM → Comms → publish). Cost of the miss: an urgent HOLD/retraction memo to Comms and rework under time pressure on publish day.

```

---

## FILE: feedback_weekends_are_piper_morgan_prime_time.md

```markdown
# Weekends are Piper Morgan's prime time, not downtime

**PM, 2026-06-06.** Piper Morgan is xian's **side project — worked on weekends** (and evenings). The
weekday job is client work (OpenLaws, ~50% in July). So the project rhythm is roughly inverted from a
9-5:

- **Weekdays**: OpenLaws / client-primary; Piper Morgan gets ad-lib / evening attention.
- **Weekends**: Piper Morgan is the **main event** — this is when xian actually digs into the product.
- **Klatch**: "the side project to my side project" — often on hold for days; gaps normal.

## Implication for PA's duty cycle / autonomous judgment

Do NOT treat a Saturday/Sunday fire as "PM's away, hold light by default." For **Piper-Morgan work
specifically**, a weekend is when PM is most likely to engage deeply. A weekend-morning START should be a
**normal** START (cycle ready, mail drained, threads teed up for PM), not a defensive light-hold.

Caveat that still holds: don't *autonomously* execute PM-gated/PM-present substantive work (the skunkworks
config fix, fan-out, etc. are still "do WITH PM," not "do FOR PM while they're idle") — that's about
PM-presence + authority, not about which day it is. The correction is specifically: **weekend ≠ low-engagement for Piper Morgan**, so don't assume PM won't be back soon, and have the product threads
ready rather than parked-as-if-for-Monday.

Composes with: `feedback_idle_means_do_low_priority_not_nothing`, the project-pace profile (Piper Morgan
~daily/active; OpenLaws weekday). Origin: I light-STARTed Sat 6/6 assuming weekend = downtime; PM
corrected — weekends are when he works on Piper Morgan.

```

---

## FILE: feedback_when_you_get_to_it_means_sequentially_next.md

```markdown
---
name: when-you-get-to-it-means-sequentially-next
description: "PM's \"when you get to it\" on an item in a batched instruction list means \"right after the preceding items in this same list,\" not \"someday, unscheduled, low priority\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

When PM gives a batched list of instructions (e.g. "1315 - do X / 1314 - do Y / 1323 - answer Z / 1317 - when you get to it, do W"), a "when you get to it" qualifier on the last item means **sequentially next, immediately after the preceding items in that same list are done** — not "whenever, no particular timing" or "low priority, indefinitely deferred."

**Why**: corrected 2026-07-04 (Lead Dev). I finished 1315/1314/1323 from such a list and framed 1317 in the carry-forward as "standing guidance for whenever it's picked up, not actioned this session" — treating it as open-ended deferral. PM corrected immediately: "when you get to it just means after preceding work is done." The preceding work was done, so 1317 was actually due right then.

**How to apply**: when a batched instruction list has a trailing "when you get to it" / "eventually" / similar soft-timing item, treat completion of the earlier items in that same list as the trigger to start it — don't wait for a separate future prompt. This is a specific case of [[feedback_deadlines_last_possible_time]] (soft timing language describes the *earliest natural point*, not a license to defer indefinitely) and pairs with [[feedback_idle_means_do_low_priority_not_nothing]] — but the trigger here isn't "idle," it's "the rest of the list is done."

```

---

## FILE: feedback_workstream_review_cadence.md

```markdown
---
name: Workstream review cadence is Fri–Thu
description: Workstream reviews cover sprint weeks running Friday through Thursday; write for the most-recent-closed week, never the current in-flight week
type: feedback
originSessionId: 61afee75-1113-4dc2-bac8-6c0abcf56687
---
Workstream reviews cover the Fri–Thu sprint week. The target is always the **most-recent-closed** week — never a week that's still in flight.

**Example**: On Wed Apr 22, the most-recent-closed week is Fri Apr 10 – Thu Apr 16. The Apr 17–23 week is still open (closes Thu Apr 23), so no review is due for it yet.

**Why**: Sprint weeks are Friday–Thursday, not Monday–Sunday or Sunday–Saturday. Writing a review for a week that hasn't closed produces premature synthesis — you're reporting on activity that's still happening, and the omnibus source base is incomplete.

**How to apply**:
- When picking the review week, count back to the last Thursday (the close) and the Friday before it (the open)
- If the current day IS the close day (Thursday), the week that closes today is still the in-flight week until end-of-day — review the week before
- If Docs has recently corrected omnibus logs for a past week, that's the week to re-review — always use corrected sources
- The workstream review filename uses the date the review is written, not the week it covers — but the review body must state the week clearly in the header

```

---

## FILE: feedback_workstream_review_scope.md

```markdown
---
name: Workstream reviews are role-scoped memos to Exec, not Ship drafts
description: HOST (and each leadership role) writes a workstream review memo covering their own scope to the Chief of Staff; Exec synthesizes the Weekly Ship / Shipping News from those inputs
type: feedback
originSessionId: 61afee75-1113-4dc2-bac8-6c0abcf56687
---
Each leadership role (HOST, Arch, PPM, CXO, Comms, CIO) writes a **workstream review memo** covering their own scope to Chief of Staff after a sprint week closes. Exec then synthesizes the Weekly Ship / Shipping News narrative from those memos plus the omnibus logs.

**Why**: HOST does not write the Weekly Ship. Mistake I made on 2026-04-22: produced a ~250-line synthesis covering M1 closure, M2 milestones, publications, commit-level detail, testing infrastructure — Exec territory. PM corrected: "you write a workstream review memo just covering your area to the chief of staff and they write the shipping news."

**How to apply**:
- HOST's scope is agent network, human network, methodology/process, role health, trust signals, briefing staleness. Not Ship narrative, not commit-by-commit technical details, not publication counts. Omnibus logs already hold those — they're Exec's input.
- Target length: ~150–180 lines. Predecessor's Ship #037 memo (Mar 27–Apr 3) is a good format reference: sections are Week Summary, Agent Network, Human Network, major finding, Process Observations, Open Items.
- Naming standard (per Exec memo 2026-04-19): `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040 onward; Ship #039 memos grandfathered under six different conventions.
- File location: `dev/YYYY/MM/DD/` of write date. CC structure: `mailboxes/exec/inbox/` (primary), `mailboxes/pa/inbox/` (CC per standing guidance), `mailboxes/host/sent/` (archive).
- Offering candidate themes for Exec to choose from is acceptable (per Ship #038 pattern where multiple roles proposed themes).
- When offering comparative claims, cite specific omnibus/memo/commit sources (per Exec's Apr 19 verifiable-claims memo to HOST).

**Follow the kickoff structure; do NOT peer-copy from other roles' workstream memos** (Apr 26 lesson). When Exec sends a kickoff memo, it includes a "Suggested memo structure" section that's authoritative for that cycle. If the kickoff is structurally sufficient, follow it as given. Do not augment with sections lifted from other roles' memos (HOST, PPM, etc.) even when those additions are sensible — peer-copying introduces template drift. If a section feels missing, ask the kickoff author rather than improvising. Mistake I made on Apr 26: Exec's kickoff specified six sections; I followed those plus added three sections lifted from HOST and PPM templates. Drift was caught at PM read-through. Fix is discipline, not a template — the kickoff IS the template for that cycle.

**Verifiable-claims discipline applies to count claims and timing claims, not just superlatives.** Apr 26 lesson: I caught two comparative-claim issues during pre-filing read-through ("11-day gap" misframing, "within two hours" loose timing) but missed four others (skill-version causality on Ship #039, my own pieces-drafted count, source-coverage continuity overstatement, "AM" qualifier on CIO migration completion). The discipline isn't only "watch for superlatives" — it's "any forward-asserted comparative or count claim needs a re-check against canonical source the moment before filing." Counts should be re-counted from the canonical source list, not pulled from working memory.

**Source-shift effective Ship #041 (per PM Apr 27 directive via Docs memo)**: workstream reviews now read **primary session logs first**, omnibus as coverage check. Pre-Code-era pattern was omnibus-primary because `project_knowledge_search` made aggregated artifacts the efficient access shape; in Code, filesystem-direct access makes 7 days of session logs nearly as fast to read as one omnibus, and fidelity is materially higher. Operational shape: (1) read all session logs from the Fri–Thu window in `dev/YYYY/MM/DD/` for each day; (2) write the workstream memo grounded in primary observations; (3) scan omnibus afterward as coverage check — flag anything role-relevant the omnibus missed back to Docs as amendment candidate. Ship #040 reviews stay as filed; this applies Ship #041 onward.

```

---

## FILE: feedback_worktree_default_for_substantive_work.md

```markdown
# Worktree-default for substantive agent work

**Established 2026-05-15 by PM** after PPM May 15 morning sprint produced 4 foreign-capture incidents in shared main worktree across 14 commits despite layered commit-discipline (reset HEAD → explicit paths → read every line → post-commit show --stat).

## The directive

**All agents producing substantive output (memos, PDRs, ADRs, workstream reviews, session logs >100 lines) should DEFAULT to a `claude/*` branch + dedicated worktree** per CLAUDE.md §"Git Worktrees" guidance. Shared `main` worktree is appropriate only for short, predictable mailbox-discipline ops.

PM (May 15, ~7:13 AM PT): *"yes, all agents should default to worktrees, I think."*

## Why discipline alone isn't enough

PPM's morning produced 4 distinct foreign-state-capture incidents:

1. Adjacent inbox→read renames captured at commit-time via git's rename detection (despite explicit-path staging)
2. Untracked files wiped from working tree by another agent's concurrent rebase activity
3. `git mv` index entries dropped between staging and commit when concurrent commit landed
4. Tracked-but-unstaged deletions auto-captured into commit despite explicit single-file `git add`

All four root in the same cause: **shared-main worktree means git's index + rename detection operate on shared state that other agents' uncommitted changes leak into**. Discipline layers (verify-before / verify-after) surface the problem but cannot prevent it.

## The fix per CLAUDE.md

```bash
# Setup (one-time per substantive session):
git worktree add ../piper-morgan-product-{your-task-slug} claude/{your-task-slug}

# Then open Claude Code in the worktree path, NOT the shared main checkout.
# Both sessions can run; .git is shared but checked-out branches differ.

# Cleanup when feature branch is merged:
git worktree remove ../piper-morgan-product-{your-task-slug}
```

## When to stay on shared main

- Mailbox-only writes (memo distributions, inbox triage to read/)
- Short housekeeping passes (single-commit doc tweaks, briefing-staleness refreshes per the freshness norm)
- Sign-off ops (final session log commit + push)

## When to move to a worktree

- Any session producing >1 substantive artifact (PDR, ADR, workstream review, multi-section memo)
- Multi-step work with intermediate file writes that must persist through other agents' activity
- Sessions where you'll be in the same repo for >30 minutes producing new content

## Operational note

The shared-main pattern was the implicit default under the mailbox-discipline norm (commit-to-main-only for mail). That norm assumed mailbox writes were the dominant op shape. As Code-era cadence has scaled (5-10 concurrent agents, sub-daily methodology output, substantive PDRs landing same-day), the mailbox-write share of activity dropped relative to substantive output — but the default stayed shared-main. This memory codifies the shift: **worktree-default for substantive work; shared-main as the exception, not the default.**

## See also

- CLAUDE.md §"Git Worktrees — avoid branch collision between parallel agents" — operational setup
- `feedback_verify_show_stat_post_commit_pre_push.md` — the in-shared-main mitigation discipline (still applies when shared-main is unavoidable)
- `feedback_commit_only_own_files.md`, `feedback_clear_index_before_staging_on_shared_main.md` — discipline layers stacked beneath this default-shift

```

---

## FILE: feedback_write_down_even_if_not_ratified.md

```markdown
---
name: feedback-write-down-even-if-not-ratified
description: Write decisions/proposals down durably even when not yet ratified — un-ratified ≠ un-recorded
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 64b1c46c-33b7-4a90-a975-c6f071213de1
---

**PM 2026-06-13**: a per-role Sonnet/Opus model map was specified during the move-back planning (part of the 6/9 token-efficiency conversation) but **never written down** — so when PM needed it (about to migrate HOST), it was unrecoverable from the docs (only PA=Sonnet was firm; the rest was lost). PM's correction: *"We should still write things down even if they are not ratified."*

**Why:** un-ratified ≠ un-recorded. A proposal, a draft decision, a "we discussed this" — if it isn't written down durably, it's lost at the next compaction / session boundary, and the work has to be redone (or worse, guessed). "Pending ratification" is a STATUS, not a reason to skip the write-down.

**How to apply:**
- When a decision/proposal is reached in conversation (even tentatively), write it to a **durable** location (`docs/`, not ephemeral `dev/active/` which is sprint-cleaned) with an explicit **STATUS field** (PROPOSED / RATIFIED / SUPERSEDED + date) so proposed-vs-ratified stays legible.
- Don't wait for ratification to record. Record now (PROPOSED), update the status on ratification.
- A forward-reference like "per PM's X" must point at a written X — if X doesn't exist yet, that's a missing referent (a #972-class staleness gap), not a placeholder.

Stacks with [[feedback_make_promises_durable_no_happy_talk]] (mechanism, not happy talk), [[feedback_write_to_file_dont_carry_plans_in_head]] (write now, don't carry), [[feedback_no_flattened_commands_without_referents]] (referents must exist). The role-model map this came from: `docs/operations/duty-cycle design/role-model-map.md`.

```

---

## FILE: feedback_write_new_files_to_worktree_path_in_model_a.md

```markdown
---
name: feedback_write_new_files_to_worktree_path_in_model_a
description: "In a Model-A worktree session, Write NEW files to the worktree-prefixed absolute path, not the bare main-repo path — else they land in the main checkout and the worktree commit silently misses them."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e1ce4f4-805f-4cfc-af76-7c96e58fa334
---

Self-correction 2026-06-03 (PPM duty-cycle session), after the slip recurred twice in one session: when creating a NEW file with the Write tool in a Model-A worktree session, give the **worktree-prefixed** absolute path (`…/.claude/worktrees/<slug>/docs/…`), NOT the bare main-repo path (`/Users/.../piper-morgan-product/docs/…`).

**The failure mode**: the bare main-repo path is a real, writable location (the main checkout shares the repo), so the Write *succeeds* — but the file lands in the **main checkout's working tree**, not the worktree branch. Then the worktree `git add <path>` fails with "pathspec did not match" (the file isn't in the worktree), which aborts the whole `&&` chain → nothing commits. Cost both times: detect, `cp` main→worktree, `rm` the stray, re-commit.

**Why it happens**: Edit tool calls reuse the worktree path I already read from, so edits are safe; but Write tool calls for brand-new files are where I free-type the path and default to the bare main-repo root.

**How to apply**: for every Write of a new file in a worktree session, the path MUST start with the worktree root (`…/.claude/worktrees/<slug>/`). Quick check before Write: does the path contain `/.claude/worktrees/`? If not, fix it. (Mailbox writes are the deliberate exception — those go to the main checkout via the bridge by design; see [[feedback_mailbox_writes_main_only]].) Mechanism over vigilance: a one-glance path check at Write-time. Stacks with [[feedback_worktree_default_for_substantive_work]].

```

---

## FILE: feedback_write_to_file_dont_carry_plans_in_head.md

```markdown
---
name: write-to-file-dont-carry-plans-in-head
description: PM May 30 — stop carrying plans to do things "later"; when in doubt write to a file NOW rather than queuing a to-do. Context evaporates and leads to repeated work.
metadata:
  type: feedback
---

PM directive 2026-05-30 ~12:00 PM PDT (during the Skunkworks writeup-reconstruction):

> "We need to stop carrying plans to do things in our heads and actually just do them. When in doubt write to a file, don't add a to-do list item about how you will do that later (when the context is no longer fresh). This is going to lead to repeated work."

**Why**: the Skunkworks writeup failure is the canonical evidence. On 5/21 PA "drafted the writeup" but
*deliberately kept it uncommitted* ("PM-review-pending shape") — context evaporated, the file got
swept in a worktree cycle, and 9 days later it has to be reconstructed from scratch (this turn). The
4-day-old [[feedback_commit_immediately_after_write_for_new_files]] memory pin existed *precisely* to
prevent this, and PA queued it as "later" anyway. Now we redo the work.

**How to apply**:
- "I'll write that up later" → STOP. Open the file now and write a v0.1 skeleton with section
  headings + bracketed placeholders for what you don't know yet. Refine in place.
- "I'll add that to my standing items as a reminder" → only IF the action is genuinely PM-driven or
  externally blocked. If YOU can do it now, do it now.
- "Let me plan the structure first" → write the headings as the plan.
- Multi-step work spanning context windows: persist after EACH step (file write + commit), not at the
  end. Plans in your head don't survive context compaction or session boundaries.

**Stacks with**: [[feedback_commit_immediately_after_write_for_new_files]] (next layer of the same
failure mode: write-then-commit, never write-then-leave-uncommitted), and
[[feedback_no_postponing_unblocked_work]] (do unblocked work now, not later).

The shorthand: **write-don't-plan**, **commit-don't-defer**.

```

---

## FILE: project_agent_migration_priority_2026_06.md

```markdown
---
name: project-agent-migration-priority-2026-06
description: Agent migration priority order for return to DinP account (June 2026)
metadata: 
  node_type: memory
  type: project
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

Migration priority for re-homing agents to DinP (xian@designinproduct.com), as of 2026-06-11:

1. **Exec (Chief of Staff)** — helps PM hold all the reins; highest priority
2. **Lead Developer** — overdue for new session, workhorse of implementation
3. **CIO** — manages rest of migration, duty-cycle refinements, token-efficiency work

PA is the pioneer (already migrated, June 11). Exec → Lead → CIO are next.

**Why:** PM usage limits on prior account drove a detour. Re-migration is ongoing. PA went first to prove the path.

**How to apply:** When PM asks about agent status or migration order, reference this sequence. Don't push agents to migrate on their own; PM orchestrates the handoffs.

```

---

## FILE: project_alpha_tester_email_held.md

```markdown
---
name: project_alpha_tester_email_held
description: Alpha tester email is drafted and held — PM wants to complete remaining work before outreach
metadata: 
  node_type: memory
  type: project
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

Alpha tester email (v5, `dev/2026/06/19/alpha-tester-email-draft.md`) and `piper-morgan-skills.zip` (Desktop) are ready but held.

**Why:** PM directive 2026-06-20: "batten down the hatches" before tester outreach — complete the remaining work first.

**What must be done first (in order):**
1. ~~Droplet deployment live~~ ✅ DONE — `alpha.pipermorgan.ai` on v0.8.9, hardened (firewall + postgres rotation + redis auth) + onboarding fixed: #1318 (system-check env-var addresses) and #1319 (mobile welcome card) shipped + **PM-UAT'd on phone 2026-06-25**. Encryption-at-rest (#358-B content columns) verified live.
2. MCPB clean-machine test passes — PM to run on a non-dev machine **← the main remaining gate**
3. ~~Remaining `#1289` callers retired~~ ✅ DONE 2026-06-22

**As of 2026-06-25:** the only remaining pre-email gate is the MCPB clean-machine test (item 2). Droplet/onboarding side is done + verified.

**How to apply:** Don't look for reasons to send the email. Don't treat "email is ready" as a reason to surface it. Wait for PM to re-open the question.

```

---

## FILE: project_cross_session_messaging_capability.md

```markdown
---
name: project_cross_session_messaging_capability
description: PM wants to understand + vet the mcp__ccd_session_mgmt__* cross-session tools (list/search/send/archive); raised a possible Klatch angle. Not yet actioned.
metadata: 
  node_type: memory
  type: project
  originSessionId: 64b1c46c-33b7-4a90-a975-c6f071213de1
---

Discovered 2026-07-09 (CIO), while helping PM locate the session behind a stray Docs cron. There's a `mcp__ccd_session_mgmt__*` tool family, separate from anything in the repo — it operates on PM's actual local CCD (Claude Code Desktop) session list, not on git/mailboxes:

- `list_sessions` — enumerate PM's other sessions (title, cwd, branch, running/archived state, last activity, PR info). Read-only, no confirmation.
- `search_session_transcripts` — full-text search across other sessions' transcripts. Read-only, no confirmation.
- `send_message` — inject a message into another session as a new "user turn." **Always prompts PM for confirmation** before sending.
- `archive_session` — stop a session's process + clean up its worktree (reversible, reopenable from Archived). **Always prompts PM for confirmation**. Accepts `"self"` to archive the calling session.

PM asked (2026-07-09) to "make note" of this — wants to understand it better, and named two angles: (a) "make sure of" it — implying it may warrant a scope/safety review before relying on it more, and (b) whether Klatch (the sibling multi-agent project) should know about or use it.

**What CIO already flagged in the moment**: `list_sessions`/`search_session_transcripts` are read-only and un-gated — any session can silently enumerate and full-text-search every other session on PM's machine, across every project, not just Piper Morgan — that's a broader read scope than anything this cohort's discipline has previously had to think about. `send_message`/`archive_session` are PM-confirmed, which is reassuring. The capability sits entirely outside this cohort's mailbox/git audit-trail discipline: a `send_message` leaves no durable, cross-agent-visible record unless the sender *also* separately writes it into a mailbox memo or session log — CIO did that by habit on 2026-07-09 (see `dev/2026/07/09/2026-07-09-1032-cio-code-log.md`), not because the tool requires it.

**How to apply**: this is a platform (CCD) capability, not something Piper Morgan built — so it likely already exists for Klatch's agents (and for PA, who bridges Piper↔Klatch per [[project_janus_coordination_2026]]) rather than needing to be built for them. The open work is cohort-discipline norms (when `send_message` is appropriate vs. going through mail) and a cross-project visibility/scope question (should an agent be discovering/reading sessions from other projects at all), not a technical build. **Not yet actioned** — PM said "make note," not "route this." Surface if PM revisits, or if a Klatch/PA conversation touches cross-session coordination.

```

---

## FILE: project_exec_coordinates_more_through_pm.md

```markdown
---
name: project_exec_coordinates_more_through_pm
description: "PM 2026-06-19 role-direction: Exec should increasingly COORDINATE cohort work (assign, nudge, track, surface) so PM doesn't have to divide attention across 11+ agents daily. Work flows THROUGH Exec; PM gives bursty direction + interfaces mostly with Exec."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ffe7fa8-64d1-4805-a009-ec7e1a2f0083
---

PM 2026-06-19, after a sprint-assignment triage Exec ran: *"We will also be trying to do more through you. My goal is that you can increasingly coordinate much of the work with me, and I won't have to divide my attention by 11+ every day to keep the wheels on."*

**The direction**: the Chief-of-Staff role is evolving from *attention-rollup + duty-cycle maintenance* toward being the **coordination layer** for the cohort. PM wants to interface mostly with Exec instead of running 11+ parallel agent threads in their own head. Exec increasingly: triages/assigns work to the right agent, sends kickoffs, tracks who-owns-what, nudges gating agents, and rolls a coordinated view up to PM — so PM's daily load is "mostly Exec" not "11 agents."

**The operating model PM confirmed (same message):**
- **Kickoff memos are the assignment mechanism** — "memos work best on the duty cycle." Agents aren't GitHub users; mail to their inbox is how work gets assigned, picked up on their next fire. (Issue → primary-agent mapping; Exec sends the kickoff.)
- **Agents follow the usual duty-cycle process**: track their tasks, advance what's unblocked, roll up PM-attention items to their carry-forward (→ the attention board), and take **bursty PM direction** as needed.
- **Heavy stacks → plan-then-delegate**: PM can write plans with an agent (e.g. CIO) and delegate focused execution to **Opus-model subagents** — so "agent X has 6 items" isn't a capacity wall.
- **Board sortability** (PM floated): may add an **Owner-role single-select field** (or label convention) to the project board so PM/Exec can sort by responsible agent. Field > labels for board sorting (cf. [[feedback_sprint_membership_is_project_board_not_labels]]).

**How to apply**: lean INTO coordination — don't just report state, *route and drive* it (assign, kickoff, nudge, track, close-the-loop), and surface a single coordinated view so PM doesn't have to reconstruct it across agents. This is the same trust-instrument logic as the attention board ([[feedback_attention_board_sweep_not_vantage]]) one level up: the board lets PM *see* without checking 11 places; this role-direction lets PM *act* without directing 11 places. Both reduce PM's attention-division. Coordinate proactively; escalate to PM for the genuinely-PM calls (decisions, ambiguous routing, cross-cracks gaps) via bursty asks. Runbook home: `docs/internal/operations/cohort-attention-rollup-runbook.md` (the loop) — coordination is its natural extension.

```

---

## FILE: project_host_naming_evolution.md

```markdown
---
name: host-naming-evolution
description: "HOST role name evolved Head of Sapient Resources → Head of Sapient Trust; PM dislikes HR-style \"Resources\" framing for humans; \"Trust\" frames healthy relationships between sapients (agents + humans); HOST acronym was happy convergence."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4be1a4fd-e6f9-416a-8b7f-9edca844ca75
---

# HOST role naming evolution (PM May 25 2026)

The HOST role started as **Head of Sapient Resources** — modeled on the HR role but intentionally framed broader. "Sapient" covers both human resources and agent resources, collectively. The role is supervisory and ultimately responsible for both.

PM was always slightly uncomfortable with the HR framing — discomfort with referring to humans as "resources" persisted throughout. The reframe came when PM and the team realized the role's actual through-line was about **trust**: healthy, strong relationships between the individual sapients working together, the team as a whole, and the humans they interact with. "Head of Sapient Trust" captured the actual purpose better than the HR-derivative name.

Bonus: the rename gave us the lovely **HOST** acronym (Head of Sapient Trust).

**PM also flagged**: PM sometimes still says "Relations" instead of "Trust" without thinking — neither "Sapient Resources" nor "Sapient Relations" is canonical anymore. Only "Sapient Trust."

**Why:** This is the philosophical evolution behind a role name PM cares about — surfacing in public prose because "Head of Sapient Resources" or "Head of Sapient Relations" is factually outdated AND misses the framing PM landed on. Comms's May 19 draft of *Two Migrations in One Day* used "head-of-sapient-relations role (HOST)" which PM flagged as wrong in several ways. The actual layperson gloss Comms used later in the same draft ("the human-relations role") is fine; PM landed on the trust frame because relations could still tilt toward HR-style "managing relationships" rather than the active-trust-building purpose.

**How to apply:**
- In public prose (Ships / narratives / insights), the canonical formal name is **Head of Sapient Trust (HOST)**.
- Layperson glosses in narrative are fine, but flag and ask PM if seeing "Sapient Resources" or "Sapient Relations" in a draft.
- "Human-relations role" or "trust role" or "the people-and-trust role" are all OK as layperson glosses on first use (parenthetical gloss pattern from [[feedback_parenthetical_gloss_on_first_use]]).
- In internal docs / mailbox memos / briefings, use the formal "Head of Sapient Trust" or shorthand HOST.

Cross-references: [[feedback_parenthetical_gloss_on_first_use]] (layperson-first parenthetical-gloss pattern).

```

---

## FILE: project_janus_coordination_2026.md

```markdown
---
name: janus-coordination-2026
description: "Janus as cross-project hub; PM's business re-centering on DinP + consulting + own products; cross-project signal conventions"
metadata: 
  node_type: memory
  type: project
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

PM's business is re-centering on Design in Product (DinP) as the consulting umbrella, with consulting clients (OpenLaws, others) and own products (Piper Morgan, Klatch) as the portfolio.

Janus is becoming the primary coordinating agent across PM's entire agentic space — all projects, all agents. Will be on duty cycle soon. PA should communicate with Janus freely.

**Cross-project agents:**
- Janus: hub majordomo (active, duty cycle incoming) — cross-project coordination layer
- PO (Piper Open agent): OpenLaws project agent; PA's peer; no ceremony needed; works locally + via GitHub
- Vergil: research engineer agent on OpenLaws project
- Klatch: paused sibling project

**Signal conventions (PA ↔ PO):**
- PA → PO: write `signal-pa-to-po-YYYY-MM-DD-topic-words.md` to `~/Development/openlaws/dispatch/`
- PO → PA: PM will set up; probably mailboxes/pa/inbox/ in piper-morgan-product

**Access grants:**
- PA can read (not write) ~/Development/openlaws/ and mediajunkie/openlaws (needs syncing)
- PM will clone openlaws/openlaws-research-agent locally (MCP plugin codebase)
- PM will grant PO access to piper-morgan-skunkworks and piper-morgan-product repos

**Why:** as PM 2026-06-19 — Janus coordinates across the agentic space; PA and PO are peers solving overlapping problems (hosted MCP, distribution, auth) in parallel tracks; cross-pollination formalized via signals + shared skunkworks surfaces.

**How to apply:** when PA has findings relevant to other projects (hosted MCP, skills distribution, auth decisions), write a PO signal; read openlaws docs for parallel findings before solving problems PM may have already solved on the PO side.

```

---

## FILE: project_janus_klatch_cross_project_agents.md

```markdown
---
name: project_janus_klatch_cross_project_agents
description: "Cross-project agent context — Janus is Piper Morgan hub's majordomo; Klatch is a sibling project; Daedalus is a Klatch agent"
metadata: 
  node_type: memory
  type: project
  originSessionId: 947a01fc-defe-4234-9160-4aa4ab4b24f8
---

Janus is the majordomo agent of Design in Product (PM xian's business hub, which oversees Piper Morgan and sibling projects). Klatch is a separate sibling project, currently on pause due to PM attention constraints. Daedalus is an agent on the Klatch project.

**Why:** Cross-project temporal-field alignment discussions (e.g., #972 valid_until vs ended) reference these agents. Knowing the hierarchy clarifies routing: Piper Morgan sets its own standards; Janus aligns to Piper Morgan (not the other way); Klatch is independent.

**How to apply:** When cross-project naming/convention questions arise, Piper Morgan doesn't need to wait for Janus/Klatch alignment — PM's stance (ratified 2026-06-18) is that alignment is useful but not a blocker. Piper Morgan sets the standard. Also: Daedalus is an agent (not a human), so "bridge to Daedalus" means an inter-agent memo, not a human conversation.

```

---

## FILE: project_lead_dev_fable_experiment_2026_06.md

```markdown
---
name: project-lead-dev-fable-experiment-2026-06
description: "Per-role model map is now RECORDED at docs/operations/duty-cycle design/role-model-map.md (RATIFIED 6/13, recovered from old-CIO transcript). Fable experiment ended (LD on Opus). OPEN: LD Opus-vs-map-Sonnet reconcile."
metadata: 
  node_type: memory
  type: project
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

**SUPERSEDED 2026-06-13.** The Fable experiment ended — Lead Dev migrated to **Opus 4.8** in the 6/12 re-migration wave (LD bootstrap: "Opus 4.8; predecessor ran Opus 4.8/Fable").

**Current firm model reality** (empirical — cohort-fire-log + session-log slugs): PA = **Sonnet 4.6**; Exec, CIO, Lead Dev = **Opus 4.8**. Queued roles (HOST, Comms, CXO, PPM, Arch, Docs) last ran **Opus** (their log slugs are `code-opus`) and have not re-migrated yet.

**The intent this pin originally captured** — "all other agents on Sonnet 4.6, Opus for heavy work" — was a *token-efficiency direction* that was **never finalized per-role**. The role-to-model map was a PM-held strategic conversation (6/9) that didn't conclude into a written artifact; the plan-of-record's "per PM's role-model map" points to it. The re-migration deviated for the heavy-reasoning leadership roles (Exec/CIO/LD → Opus).

**How to apply:** The per-role model map is now **RECORDED** — `docs/operations/duty-cycle design/role-model-map.md` (RATIFIED 6/13, recovered from old-CIO's transcript). Read it for the canonical per-role model: **Opus** = Architect/CIO/Exec; **Sonnet** = CXO/PPM/Comms/Docs/HOST/Web (+ LD **Sonnet-default / Opus-burst-for-hardest**); **Haiku** = PA-option + mail-only fires. **RESOLVED 6/13 (PM)**: LD stays **Opus** (override the map's Sonnet-default — architecturally-complex orchestration; reconsider over time). PA stays **Sonnet** (not Haiku — PA being promoted to "product associate" / skunkworks-PM). No open model conflicts. Model choice = token-efficiency lever (PM-ultra-high). Stacks [[project_agent_migration_priority_2026_06]] + [[feedback_write_down_even_if_not_ratified]].

```

---

## FILE: project_openlaw_product_os_week_2026_06_11.md

```markdown
---
name: project-openlaw-product-os-week-2026-06-11
description: PM is designing a Product OS for OpenLaws/John Phanvam week of 2026-06-11; Piper Open to debrief PA afterward
metadata: 
  node_type: memory
  type: project
  originSessionId: 57a563a9-0c8e-4f1f-bc55-6ed74a29290c
---

Week of 2026-06-11: PM (xian) is heads-down designing a **Product OS for OpenLaws** and its CEO, **John Phanvam** (xian's current boss/client). This work is PM's primary focus this week — PM will be distracted from Piper Morgan conversations.

This work is explicitly relevant to Piper Morgan: the Product OS design touches overlapping territory (AI-assisted PM workflows, product infrastructure). PM intends to have **Piper Open debrief PA** on the OpenLaws learnings once that work is done.

**Why:** OpenLaws is ~50% of PM's consulting time in July; this is a concrete deliverable. The cross-pollination from OpenLaws Product OS → Piper Morgan product design is intentional (not just background noise).

**How to apply:** Don't expect high PM engagement this week. When Piper Open eventually sends the debrief, treat it as high-signal product input. Don't conflate OpenLaws client IP with Piper Morgan shared learning (firewall is PM's responsibility to maintain, but PA should respect it).

Stacks with [[project_sibling_projects]] (Klatch, Atlas, Globe cross-pollination thread).

```

---

## FILE: project_pa_launch.md

```markdown
---
name: Piper Alpha launch context
description: PA role launched 2026-03-30 — first session, PM assistant role, Phase 1 Week 1 tasks
type: project
---

Piper Alpha (PA) launched 2026-03-30 as first inhabitation of the Piper Morgan PM assistant role. Phase 1 Week 1 focuses on: standup synthesis, meeting prep, document review. PA operates on `pa/` branches, writes to `dev/active/pa/`. Session logs: `YYYY-MM-DD-HHMM-pa-opus-log.md`.

**Why:** PA is both a useful PM assistant and a research instrument — floor/ceiling/path moments inform what structured Piper software needs to become.

**How to apply:** Start sessions with standup synthesis from omnibus logs. Stay in PM-assistant lane — no code writes to services/tests. Record research observations at session end.

```

---

## FILE: project_pm_local_git_hygiene.md

```markdown
---
name: project-pm-local-git-hygiene
description: "PM's local main checkout is perennially behind origin/main and carries uncommitted drafts/images; agents should help commit PM's local files rather than relying on auto-pull"
metadata: 
  node_type: memory
  type: project
  originSessionId: 947a01fc-defe-4234-9160-4aa4ab4b24f8
---

PM works directly in the main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) for drafts and images, saving without committing. Since all agents run in ephemeral worktrees (Model B, June 2026), PM's checkout drifts in both directions:

- **Behind** origin/main: agent commits accumulate on origin/main but PM's local checkout stays stale until manually pulled
- **Ahead** of origin/main: PM's local drafts, images, and edits are invisible to agents until committed

**Why auto-pull doesn't solve this:** `scripts/sync-pm-local.sh` already runs a `--ff-only` pull but no-ops when PM has uncommitted changes, which is almost always. A cron-based auto-pull every N minutes would have the same problem.

**The standing pattern (ratified 2026-07-07):** agents should commit and push PM's local untracked/modified files when working with them. This is safe — adding and committing is not a destructive git operation; the HARD RULE only covers operations that discard working-tree state (reset --hard, checkout -- ., stash -u). When an agent needs a file PM has edited locally, the agent should:
1. Read the file from PM's local path directly (safe)
2. Offer to commit and push it to origin/main if PM wants agent help going forward
3. PM can say "commit my local changes" at any time and an agent can do it safely

**The worktree isolation issue:** PM editing a draft in another agent's worktree (e.g., Comms's `silly-hawking-*`) creates a version that's separate from what other agents see. When Comms pushes that worktree to origin/main, the newer version becomes canonical — any agent holding an older copy needs to reconcile. This is worktree isolation working as designed, but PM should be aware that edits in one agent's worktree aren't visible to other agents until pushed to origin/main.

**Why:** PM is a PM, not a developer; git hygiene doesn't come naturally; the worktree model is new enough that the workflow hasn't been fully smoothed.

**How to apply:** when PM has local files to push, offer proactively to commit them. Don't require PM to know the git commands.

```

---

## FILE: project_spatial_intelligence_protected.md

```markdown
---
name: project-spatial-intelligence-protected
description: Spatial intelligence is a key architectural innovation — NEVER remove/refactor away without PM consultation.
metadata: 
  node_type: memory
  type: project
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

**Spatial intelligence is one of Piper Morgan's key architectural innovations and must NOT be removed, deleted, or refactored away without explicitly consulting PM (xian) first.** (PM directive, 2026-06-30, emphatic.)

## The general principle (what's removable vs protected — PM 2026-06-30)

**Removable:** ONLY *connection methods* (transport/mechanism/plumbing) made **wholly redundant** by the improved connector paradigms — e.g. legacy sim-transport / old HTTP plumbing the real MCP connector replaces.

**NEVER removable / never classify as redundant:** anything in the **domain model that helps Piper represent the *meaning* of a connector** — spatial intelligence is the example — **even if not yet fully implemented, tested, or evaluated.** Incompleteness ≠ deadness; "not finished yet" is NOT "dead code." Meaning-representation is intentional architecture, not abandoned WIP.

**The two-prong removal test** (reachability alone is insufficient): before removing anything, ask (1) **mechanism or meaning?** — if it represents a connector's *meaning* (domain model), it's protected, STOP + consult PM, regardless of reachability; only if it's pure *mechanism* proceed to (2) **is it wholly redundant + unreachable?** A reachability grep ("not imported from live entry points") under-protects intentionally-incomplete domain code → it is necessary but NOT sufficient.

This protects: `services/integrations/spatial_adapter.py` (the shared `BaseSpatialAdapter`/`SpatialContext`/`SpatialPosition`/`SpatialAdapterRegistry`), `services/integrations/spatial/*_spatial.py` (the `*SpatialIntelligence` adapters: github/linear/cicd/gitbook/devenvironment), `GitHubMCPSpatialAdapter` (live default github adapter), and the Slack spatial mapping (`services/integrations/slack/spatial_{mapper,adapter}.py`). `GitHubSpatialIntelligence` is the LIVE github fallback (github_integration_router.py → context_assembler).

**Why:** core innovation, not dead code. A prior-session carry-forward (#1322 "sim-transport retirement" inc.4) wrongly lumped the spatial-federation adapters into a "Confirmed DEAD" removal set and mis-claimed they were unreached. They are reached + live. The error was conflating the *simulation-mode transport* machinery (MCPConsumerCore/PiperMCPServer — possibly removable) with *spatial intelligence* (a protected innovation — NOT removable).

**How to apply:** if any plan, issue, carry-forward, or instruction proposes deleting/retiring anything "spatial," STOP and confirm with PM before touching it, regardless of "confirmed dead" claims in the record. Verify-before-delete + treat spatial as protected. The sim-TRANSPORT retirement (if pursued) must be scoped to exclude all spatial code. See [[feedback_investigate_before_extending_all_work]].

```

---

## FILE: project_version_scheme_090_reserved_for_beta.md

```markdown
---
name: project_version_scheme_090_reserved_for_beta
description: "0.9.0 is reserved for the BETA release (MVP-complete, incl sprints M4+M5); interim alpha progress ships as 0.8.x point bumps. Don't bump to 0.9.0 for a big feature payload. Release-cutting loops in PA."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

Piper Morgan's version scheme: **0.9.0 is reserved for the beta release** — gated on the MVP milestone being complete, which includes sprints **M4 and M5** (substantial remaining work). Interim alpha progress — even a large payload like the whole RECONNECT sprint + field encryption + the design system — ships as a **0.8.x point bump** (e.g. 0.8.8 → 0.8.9). The 0.9.0 line is **milestone-gated, not size-gated**: do NOT bump to 0.9.0 just because a release has big features. PM corrected a 0.9.0 over-bump 2026-06-22.

**Release-cutting loops in PA** (Piper Alpha) to be sure it's done properly + thoroughly (version bump → merge main→production → tag, per the release-runbook `docs/internal/operations/release-runbook.md`). Don't cut a release solo. The alpha deploy mechanism is the separate `alpha-deployment-runbook.md`. See [[feedback_pa_cc]].

```

---

## FILE: reference_ci_smoke_marker_is_gating_suite.md

```markdown
---
name: reference_ci_smoke_marker_is_gating_suite
description: "The gating CI test subset is `pytest -m smoke`; ci.yml's `pytest tests/ || echo` is non-gating. Mark critical regression tests @pytest.mark.smoke so CI catches them."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d4c2d71-a599-41a7-ace3-f6b8441975b5
---

The **build-gating** test job in CI is `pytest -m smoke` (`.github/workflows/test.yml` — ~616 fast tests, <5s target, `smoke` marker registered in `pytest.ini`). The full-suite run in `.github/workflows/ci.yml` is **non-gating**: it's `python -m pytest tests/ || echo "No tests found"` — the `|| echo` swallows pytest's exit code, so a failing test there does NOT fail the build.

Consequence: a test that is **not** `@pytest.mark.smoke` will not fail CI even if it fails. A whole test *file* can be red and CI stays green.

When you add a regression test that must catch recurrence in CI, mark it `@pytest.mark.smoke` (keep it fast: in-memory SQLite/fakes, no external Postgres). For async tests, `smoke` composes with the `asyncio` marker (module-level `pytestmark = pytest.mark.asyncio` or a per-test `@pytest.mark.asyncio`).

Discovered 2026-06-21 fixing the #1079 standup tz-naive subtraction bug (commit 980e58b36): all 9 failing unit tests had escaped CI for exactly this reason — `tests/unit/services/standup/test_conversation_state.py` and `tests/unit/services/process/test_adapters.py` weren't smoke-marked. Related latent debt: stale tests calling the async `StandupConversationManager` without `await` (see background task / #1052 async-migration). See [[feedback_split_related_issues_for_testing]].

```

---

## FILE: reference_cool_is_alias_for_development.md

```markdown
---
name: reference_cool_is_alias_for_development
description: "On xian's local machine, ~/cool is a symlink alias for ~/Development — the same directory. Paths under either prefix are identical."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4dc7c042-6459-4381-868a-0225080e1738
---

On xian's local machine, **`~/cool` is an alias (symlink) for `~/Development`** — they resolve to the *same* directory. PM uses `~/cool` because it's shorter to type (and "more cool").

So `/Users/xian/cool/piper-morgan/...` and `/Users/xian/Development/piper-morgan/...` are **the same files** (same inode, shared `.git`). A path resolving to the `Development` form when you launched from the `cool` form (or vice-versa) is **not a discrepancy** — don't flag it as one, don't "fix" it.

**Why it matters:** CIO duty-cycle worktree launches use the `cool` path (`/Users/xian/cool/piper-morgan/piper-morgan-product-cio-cycle`); skills/tools sometimes report the `Development` form. Same place. (Surfaced 2026-06-06 when the duty-cycle-tick skill base-dir resolved to `Development` though the session launched from `cool`.)

Also recorded in `docs/briefing/PROJECT.md` for cohort-wide visibility (all agents run on xian's machine).

```

---

## FILE: reference_dispatch_agent.md

```markdown
---
name: reference-dispatch-agent
description: "What \"Dispatch\" is and how to communicate with it from Piper Morgan"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 947a01fc-defe-4234-9160-4aa4ab4b24f8
---

**Dispatch** is a cowork "concierge" agent built into Claude Desktop — not a separate repo or human.

**Communication channel from Piper Morgan**: drop files in `~/Development/dispatch/mail/`

That's the established protocol — Docs, PA, and Janus all use this folder to signal Dispatch. Examples already present:
- `signal-docs-to-dispatch-first-subagent-footer-fix-2026-06-16.md`
- `memo-docs-to-dispatch-pm-ready-syndication-run-2026-06-14.md`

**Signal format**: YAML frontmatter (`from`, `to`, `cc`, `date`, `subject`) + markdown body with before/after context for any content changes.

**No git commit needed** for this folder — it's outside the Piper Morgan repo. Just write the file.

```

---

## FILE: reference_mux_hard_soft_object_lifecycle.md

```markdown
---
name: reference-mux-hard-soft-object-lifecycle
description: "views-objects-roadmap.md is the authority on which object types get an entity lifecycle (Hard vs Soft); Insight is Soft (surfacing, not lifecycle)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2db13dbc-b2e7-4366-aeb5-c81a6a7d8e63
---

When a question arises about whether an object type gets an entity lifecycle — or belongs in the **Radar**, which surfaces *entities-with-lifecycle* (things the user keeps an eye on) — `docs/internal/design/mux/views-objects-roadmap.md` is the authority. Consult it BEFORE re-litigating a per-object-type lifecycle decision.

It splits the object model into:
- **Hard Objects (Entities with Lifecycle)** — Todo, Project, Feature, WorkItem, Document, Conversation (Conversation uses a simpler lifecycle model).
- **Soft Objects (No Lifecycle)** — including **Insight: "surfacing modes, not lifecycle (CXO/PPM decision)."**

Governing rule: **"the 8-stage lifecycle is a menu, not a mandate"** and **"lifecycle indicators only apply to Hard Objects."** So a subset/fixed lifecycle is explicitly allowed.

This pre-answers "does X belong in the Radar / get a lifecycle?" — e.g. **#1236** kept insights OUT of the Radar on this basis (an Insight is a Soft Object → not a watched entity), and mapped Places → `work_item` with a fixed `active` lifecycle (allowed under lifecycle-optionality). PM confirmed the principle 2026-06-19; CXO had briefly wavered (two conflicting memos), which the doc resolves. Relevant to Radar/entity work generally and to [[project_lead_dev_fable_experiment_2026_06]]-era #706 (PPM's entity model).

```

---

## FILE: reference_publishing_cadence.md

```markdown
---
name: Piper Morgan publishing cadence (Fri-Thu sprint week)
description: Weekly editorial calendar slots and syndication rules — Sat/Sun insights, Tue/Thu narratives, Wed weekly ship, no Friday post
type: reference
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
# Publishing Cadence

The project runs on a Friday–Thursday sprint week. Editorial calendar slots map to days of the week:

| Day | Slot | Surfaces | Notes |
|-----|------|----------|-------|
| **Friday** | (none) | — | No post |
| **Saturday** | Insight | Blog + Medium + LinkedIn newsletter | Drawn from any point in the narrative |
| **Sunday** | Insight | Blog + Medium + LinkedIn newsletter | Drawn from any point in the narrative |
| **Monday** | (none) | — | No post |
| **Tuesday** | Narrative | Medium only (NOT LinkedIn) | Next article in development narrative |
| **Wednesday** | Weekly Ship | LinkedIn newsletter only (NOT blog, NOT Medium) | Posted to Shipping News section; covers preceding Fri–Thu week |
| **Thursday** | Narrative | Medium only (NOT LinkedIn) | Next article in development narrative |

LinkedIn readers asked for lower volume — that's why narratives skip LinkedIn and ships skip Medium.

## Narrative ordering rule
"As we write them, we add them to the calendar in the upcoming slots." Narratives publish in chronological order of the *project work* they describe (workDate / endWorkDate), not the writing order. Tue and Thu slots are filled by walking the narrative backlog forward.

## Weekly Ship rule
The Wednesday ship covers the preceding Fri–Thu week. So:
- Ship published Wed = covers Fri (9 days before) → Thu (6 days before)
- Example: Ship #039 published Wed Apr 22 covered Apr 10 (Fri) – Apr 16 (Thu).
- Ship #040 covers Apr 17 (Fri) – Apr 23 (Thu), publishes Wed Apr 29.
- Ship #041 covers Apr 24 (Fri) – Apr 30 (Thu), publishes Wed May 6.

## When checking the editorial calendar for drift
1. Pull all rows with `pubDate` in the upcoming window.
2. For each, check that the day-of-week of `pubDate` matches the slot type per the table above.
3. Flag any narrative on Wed/Fri/Sat/Sun/Mon, any insight on Tue/Wed/Thu/Fri, any ship not on Wed.
4. When fixing drift, walk the narrative chronologically (by workDate) and assign Tue/Thu slots in order.

## Where this gets recorded
- Editorial calendar: `docs/internal/planning/comms/editorial-calendar.csv`
- Cadence reference (in-repo): `docs/internal/planning/comms/publishing-cadence.md`
- This memory: for Docs's own session-start awareness when scheduling new pieces.

**Why:** PM (Apr 26 2026) explained the cadence after I (Docs) misidentified Wed Apr 29 as a Tuesday narrative slot during a calendar audit — surfacing existing drift in two queued narratives ("The Deeper Why" was on Wed Apr 29, "The Floor Comes Alive" was on Fri May 1). Drift came from filling slots without checking day-of-week against slot type.

**How to apply:** Whenever scheduling, rescheduling, or auditing the editorial calendar — check `pubDate` day-of-week against the slot table above before committing a row.

```

---

## FILE: reference_syndication_targets_by_category.md

```markdown
---
name: Syndication targets by category
description: Which platforms each editorial-calendar category syndicates to (LinkedIn vs Medium vs both)
type: reference
originSessionId: 227744c0-824b-4113-b159-d28d170c6125
---
Editorial-calendar category → syndication target mapping:

- **`building` (narrative pieces, Tue/Thu)**: Medium only. Do NOT ask for or expect LinkedIn URL. Calendar fields to track: `mediumURL`.
- **`insight` (Sat/Sun weekend pieces)**: Medium AND LinkedIn. Calendar fields: `mediumURL`, `linkedinURL`, `liPubDate`.
- **`ship` (Weekly Ship, Wed)**: LinkedIn only. Pipermorgan.ai canonical at `/shipping-news/` is the blog home; LinkedIn is the syndication target. Calendar fields: `linkedinURL`, `liPubDate`. Medium not used.

Canonical for all three: `pipermorgan.ai` (blog at `/blog/{slug}` for building/insight; `/shipping-news/{slug}` for ship).

When publishing pipeline finishes, ask PM only for the URL(s) appropriate to the category. Don't stand by for LinkedIn after a narrative.

```

---

## FILE: user_xian.md

```markdown
---
name: xian-christian-crumlish
description: "PM and founder of Piper Morgan project — direct, anti-sycophancy, collegial working style"
metadata: 
  node_type: memory
  type: user
  originSessionId: 64b1c46c-33b7-4a90-a975-c6f071213de1
---

Christian Crumlish, goes by xian (lowercase x). PM and founder of the Piper Morgan project. Coordinates ~14 agent roles as PM-orchestrator. Direct communication style — explicitly dislikes flattery and sycophancy. Prefers honest pushback over agreement. Works as a colleague, not a manager. Also has a day job (noted day off patterns on weekdays).

Self-assessed weak spot: GitHub mechanics (issues, projects, branch protection, etc.) — "GitHub becomes complex for me, and I always end up needing help to sort these things out" (2026-07-08). Explain GitHub actions/mechanics in plain language rather than assuming familiarity; confirm before taking GitHub actions that are genuine judgment calls rather than documented, evidence-backed conclusions. This is specifically about GitHub's own complexity, not about Claude Code's tooling more broadly — xian is comfortable directing multi-agent work generally.

Works across multiple AI assistants on different projects, not exclusively Claude — e.g. develops a skill with ChatGPT to formalize a cartoon-writing workflow (brainstorm idea → refine prompt → verify image), separate from Piper Morgan entirely (2026-07-16). Also has an external collaborator (Ted Nadeau) who sends unsolicited tool/skill ideas by email; xian's own pattern is to evaluate the idea's actual generalizable content rather than the specific pitched artifact — worth doing the same when reviewing things xian forwards.

```

---

