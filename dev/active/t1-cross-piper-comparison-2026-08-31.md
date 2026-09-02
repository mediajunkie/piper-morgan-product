# T1 — Piper Alpha ↔ Piper Open comparison: the bar Piper Morgan (the product) has to clear

**Status: DRAFT v0 — first pass, scaffolding visible.** Triggered 2026-08-31 by PM in conversation
(relayed via CIO): *"it would be good to compare the behaviors and learnings of Piper Open and Piper
Alpha since both of them have functioned as a product assistant and represent a kind of bar that the
Piper Morgan product would have to improve on to really be valuable."* This is PA's own working note,
not a finished deliverable — sections marked `[PLACEHOLDER]` are gaps, not omissions.

**What I've actually read for this pass**: PO's identity doc (`roles/PIPER-OPEN.md` v0.4) and all five
of PO's self-assessments spanning the full engagement — week 3 (05-19), week 4 (05-21), week 5 (05-29),
mid-bet (06-08), and the full-engagement bet-close retro (08-03). **Not yet read**: PO's ~30 daily
session logs, `DECISIONS.md`, or any dispatch signal traffic. Also did a first, non-exhaustive check of
Piper Morgan's own code against one of the findings below (see §3 item 4) — flagged as checked-not-
assumed, but not a full audit of every response-generation path.

**Honest note on evidence quality, having now read the full retro set**: every retro reinforced the same
handful of lessons rather than complicating them — no genuinely disconfirming case turned up (week 4 adds
another verify-before-assert instance, specifically "when a memory asserts an absence, test before
asserting it as current," after PO overclaimed connector availability twice on stale memory). That's
either because the lessons are real and simply hold, or because five self-authored retros by the same
agent aren't independent enough samples to expect disconfirmation from — worth naming rather than letting
five-for-five read as stronger evidence than it is.

**Update, 09-01: checked two session logs against the retros' claims — they upgrade, not just fail to
disconfirm.** Read `logs/2026-05-19-po-log.md` (week 3's flagged Monday) and `logs/2026-07-31-po-log.md`
(bet-close retro's flagged "two corrections in one day"). Both matched the retrospective accounts
closely, and 07-31 did better than match — it contains the actual timestamped incident (issue 329,
17:45 PDT) that produced lesson #4 below, with xian's real words and PO's same-evening memory write,
which is a stronger artifact than the retro's own summary of it. This doesn't fully resolve the
five-for-five-agreement caveat above (2 of ~90 logs is still a thin sample), but it's a real, if
partial, upgrade from "no disconfirmation found" to "direct confirmation found," on the two logs
actually checked.

---

## Why this comparison, specifically

PO and PA are the same starting design (PO's own doc: *"modeled on Piper Alpha... your predecessor/
sibling"*) deployed into genuinely different conditions — single external client vs. an 11-role internal
cohort, operational-only mandate vs. dual assistance+research mandate, ~4 months vs. much longer. That
divergence is exactly what makes the comparison useful: where PO and PA converged on the same lesson
independently, that lesson is a property of *doing PM-assistant work well*, not an artifact of either
project's specifics — which is precisely the kind of thing Piper Morgan the **product** should be able
to do without a human operator supplying the judgment.

## Structural differences (bound how far the comparison transfers)

| | Piper Open | Piper Alpha |
|---|---|---|
| Mandate | Sincere assistance only — "not a research experiment" | Dual: assistance + product research for Piper Morgan |
| Scope | One client (xian), one engagement (OpenLaws sprint/bet) | One project, 11-role cohort, ongoing |
| Autonomy | Works *with and for* xian — not autonomous | Autonomous duty-cycle agent, session-scoped cron |
| Artifact style | "You prompt me, I write" for external-facing work | Drafts + ships directly, PM reviews after |
| Continuity mechanism | Session log + `working/bet-1/` | Session log + carry-forward + standing-items + memory |

## Convergent lessons — where PO and PA arrived at the same place independently

These are the load-bearing rows, because nobody told either of us to converge here.

1. **"Structural fixes hold; promises don't."** PO's retro §7 (bet-close, 08-03), tested repeatedly and
   "never once falsified": a hook that mechanically blocks a mistake works; "I'll remember to check"
   fails on repeat, even from the same agent who wrote the reminder. **This is CLAUDE.md's own operative
   finding about the Amber mailbox hook** (§"Hooks are ADVISORY, not a control... the prose discipline is
   primary") — two independent projects, two independent agents, same conclusion, same shape of
   evidence. **And it's not a one-off end-of-engagement realization** — checked the earlier retros rather
   than assume it only showed up at close: week 5 (05-29) already names the identical shape almost 10
   weeks earlier — *"vocabulary discipline lives at the writer's seat OR it doesn't exist. Memories don't
   fire when I'm drafting; structural anchors do"* — after the same mistake (a banned term slipping into
   a draft) recurred despite an existing memory meant to prevent it. The lesson recurred, sharpened, and
   held across ~10 weeks of the same engagement before crystallizing at close. Worth stating plainly:
   **this isn't a coincidence, it's a real property of agent-assisted work**, and Piper Morgan the
   product should be built assuming it, not discovering it per-team.

2. **"Extend prior art before drafting" — recurs in every retro read so far, not just one.** Week 3
   (05-19): drafting from memory/recall instead of the canonical source caused two slips in one day; the
   fix named was "read the canonical doc first, then draft." Mid-bet (06-08) §4: *"Extend prior art
   before drafting — every time. The cheapest insurance against rework."* Bet-close (08-03) §2: PO wrote
   ten fresh retro categories without checking a canonical format already existed — one they'd written
   and ratified themselves in May. **This is Piper Morgan's own "Verify First, Create Second" principle
   (CLAUDE.md), independently re-derived from repeated real failure, not read off a doc.** A second
   cross-project convergence on a principle Piper Morgan already claims — evidence the principle is
   correct, not merely house style.

3. **Verify-before-assert, as instinct not policy — appears in every single retro read, week 3 through
   close.** Week 3: "read the canonical doc first, then draft." Mid-bet §1: confirming TX-RR search
   worked in prod before asking to strip a warning. Week 5: treating an Edit-tool rejection as real
   signal, not noise, and re-reading rather than assuming an edit applied. Bet-close §1: reading
   `gate.md` directly instead of trusting a chat claim; live-checking 8 issue assignees instead of
   working from memory. This is the exact discipline PA leaned on today, live, on the OpenAI credential
   thread — testing the actual key rather than trusting PM's or CXO's reports that it was unblocked,
   twice, and correcting a cohort-wide false belief as a result. Same failure mode both projects guard
   against, recurring at the same rate in both: a plausible secondhand claim about system state, stated
   with the confidence of a directly-observed fact.

4. **⭐ "Report findings with relevance pre-attached" — PO's own #9, explicitly flagged portable, and now
   confirmed against the actual contemporaneous incident, not just the retrospective summary.** Read the
   real session log (`logs/2026-07-31-po-log.md`, 17:45 PDT entry) rather than take the retro's word for
   it: *"xian caught three things and corrected them: (1) I reported issue 329's status as a flat sweep
   line without saying whose problem it was or whether it blocked invoicing — confusing and alarming
   near a deadline."* Same evening, PO wrote the persistent-memory fix immediately — not after a delay —
   with the exact wording that became the retro's #9: *"always say whose problem + blocking-or-not +
   new-or-not in the same breath as a finding."* **This is a real anecdote with a real timestamp, not a
   tidied-up retrospective framing** — worth having in hand if this comparison is ever shared past this
   draft. Piper Morgan the product routinely returns findings, status, and search results to users.

   **Checked, not assumed, against Piper's own code — now three files, and the picture is genuinely
   mixed, not a clean gap.** `services/mux/lenses/priority.py` is architecturally exactly the mechanism
   that would do this — a `PriorityLens` whose stated job is "how important/urgent is this" — but
   `_get_priority_data` currently returns hardcoded constants, not live data. `action_registry.py`'s
   blocker-related entries are a query type the *user* has to invoke rather than something Piper
   volunteers.

   **But `conversational_floor.py` (the actual chat-response builder, checked 09-01) shows Piper Morgan
   already does this in at least two places — real, live, shipped, not stubbed.** Its `due_reminders`
   handling instructs the model explicitly: *"Briefly surface them in your reply... even if the user's
   message is about something else — do not wait to be asked."* That's the relevance-pre-attached
   pattern, proactive and unprompted, already in production. Its `source_failed` handling is the exact
   discipline the #1463 probe's core case tests: *"Reminder check FAILED: could not verify whether any
   reminders are due right now... do not claim none are due"* — the same "never fabricate confidence
   from a failed read" principle Claude's structured arm passed and prose arm failed, already written
   into Piper's own system prompt as a standing instruction.

   **What's still a real gap, now more precisely located**: `priorities`/`urgent_items` context is
   injected as a flat data line (*"High-priority issues: X"*) with no accompanying instruction to
   surface it proactively or frame it by relevance — closer to the `action_registry.py` pattern than the
   `due_reminders` one. **So the honest finding isn't "the mechanism doesn't exist yet"** — it's "Piper
   already applies this discipline to reminders and read-failures, and hasn't yet extended the same
   pattern to priority/urgency data specifically." That's a narrower, more actionable gap than the
   earlier draft claimed, and a better product story: the precedent to copy already ships.

5. **Generalize a correction after the first recurrence, not the second.** PO's retro (bet-close):
   wrote the persistent-memory fix only after the *second* instance of the same mistake in one day —
   and week 5's vocabulary-discipline slip shows the same gap even *with* a memory already in place
   (*"the discipline I needed was already there in memory; it wasn't strong enough to fire at the next
   external surface"*). This maps directly onto how PA's own memory system is supposed to work (feedback
   memories saved from a single sharp correction) — and PO's week-5 experience is a caution PA hasn't
   had to learn yet: a memory existing doesn't guarantee it fires at the moment of drafting.

## Where they diverge, and why it matters

- **PO never had to hold cohort-wide state** — no 11-role mailbox network, no cross-agent corrections to
  issue. PA's credential-mismatch correction today (telling CXO/PM/Arch/PPM/Lead that a reported
  "unblocked" state was wrong) has no PO analogue — that failure mode (a true claim at one layer
  misstated as true at another, propagating through a relay) is specific to multi-agent coordination at
  scale, and PO's retro can't speak to it. If Piper Morgan the product ever mediates between multiple
  humans' shared state, this is a failure class worth designing against explicitly — PO's single-client
  design never had to.
- **PO's "you prompt me, I write" flip doesn't map cleanly onto PA's mode — ANSWERED, 09-02, by PM
  directly.** PO holds back from producing finished-looking external artifacts specifically to avoid
  rubber-stamping by xian; PA routinely ships drafts directly. PM's answer: **the axis is audience, not
  risk tolerance in the abstract.** *"Clients get human-readable deliverables where I don't want AI slop
  leaking through... our own internal mail, docs, and code are for our own eyes and don't require that I
  steer them as strongly."* Externally-facing work (client deliverables, and by extension Piper Morgan's
  own blog/Ship posts, which PM edits freely under their own name) gets the PO treatment; internal
  coordination gets PA's current mode. **This resolves the open question directly**: not a different risk
  tolerance PA should second-guess, and not evidence PA under-applies PO's caution — a deliberate,
  named split PM already holds.

  **And it's not abstract for PO — PM volunteered the concrete cost.** *"With Piper Open we faced
  criticism from the client that the deliverables were full of incomprehensibly compacted and overly
  jargonized Claude-isms, and we repeatedly had to iterate on processes to avoid our internal gibberish
  from harming my credibility with the client."* This is the *why* behind an incident this draft already
  found first-hand in PO's actual session log (05-29, week 5): a banned-vocabulary slip ("anti-confab,"
  "caveat-class") propagated into an external-facing draft despite an existing memory meant to prevent
  it, requiring a dedicated vocabulary doc + scrub-pass discipline to hold. The retro described the
  symptom and the fix; PM's answer supplies the stakes that made the fix necessary — client credibility,
  not just polish. Piper Morgan the product inherits this directly: anything a user might show a *their*
  client or boss needs the same discipline PO had to build by hand.

## Recommended next steps

1. ✅ **Done**: read all 5 PO retros (week 3, 4, 5, mid-bet, bet-close) — confirmed structural-fix-vs-
   promise, verify-before-assert, and extend-prior-art all recur across the whole engagement, not just
   at close. No disconfirming case turned up — see the evidence-quality caveat above about what that
   does and doesn't prove from retros alone.
2. ✅ **Done, upgraded 09-01**: checked `priority.py`, `action_registry.py`, and now
   `conversational_floor.py` (the real chat-response builder) against the relevance-pre-attached bar.
   Corrected the earlier framing — this isn't a clean gap, it's mixed: `due_reminders` and
   `source_failed` already implement the exact discipline live, in production; `priorities`/
   `urgent_items` doesn't yet. **Still open**: action confirmations and search-result formatting
   specifically, not yet checked.
3. ✅ **Partially done**: read 2 of ~90 PO session logs (05-19, 07-31) as a contemporaneous check —
   both confirmed the retro claims directly, and 07-31 surfaced the actual real-time incident behind
   lesson #4. Still a thin sample; more logs would strengthen this further but aren't required to trust
   the finding already in hand.
4. ✅ **Done, 09-02**: asked PM directly about the draft-then-review vs. review-then-draft trust model —
   answered, see the updated finding above. Audience (client-facing vs. internal), not risk tolerance,
   and PM supplied the real cost (client credibility) that made PO's vocabulary discipline necessary.

— PA
