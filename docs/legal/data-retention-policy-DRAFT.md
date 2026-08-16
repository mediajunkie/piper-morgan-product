# Data Retention & Learning-Scope Policy — Piper Morgan (scaffold)

> ✅ **§3 and §4 RATIFIED 2026-08-15** — retain all by default (no auto-expiry), user-facing
> retention settings scoped to the Enterprise milestone (#1634), not MVP. Still a scaffold for
> §1/§2's exact wording before publication as the live privacy-policy text.
> **Origin**: PM asked Exec for a retention policy draft (2026-08-13), named it HOST's remit (trust/
> safety, not product or design), and gave four framing points to build from — see `mailboxes/host/
> read/brief-exec-to-host-cc-pm-draft-a-retention-policy-your-remit-per-pm-2026-08-13.md` for the full
> handoff. This scaffold follows that framing; the two open questions in it are left open on purpose.
> **Every factual claim below was independently spot-checked against the code before drafting** —
> not just accepted from Exec's brief. See the "What HOST verified" section at the bottom for exactly
> what was re-checked and how.
> **Relationship to the privacy policy**: `docs/legal/privacy-policy-DRAFT.md`'s retention section (🔍
> marker, added 2026-08-13) already states the ground truth this scaffold is built on. Once PM blesses
> a policy here, its content replaces that 🔍 marker with real policy text — this document is upstream
> of that one, not a duplicate of it.

---

## 1. The headline trust property: Piper does not learn across users

**This comes first, deliberately** — PM named this as potentially more load-bearing than the retention
*duration* question below, because it's a claim about *scope* (what Piper does with what it learns),
not just *storage* (how long data sits).

> **What you tell Piper Morgan, and what Piper learns from working with you, stays yours.** Piper does
> not apply what it learns from one user's conversations, working style, or project context to any
> other user's experience — and it does not fold your data into Piper Morgan's own shared or core
> functionality. Your working relationship with Piper is not a training signal for anyone else's.

**Why this is a claim we can make, not just a claim we want to make**: it's structurally enforced on
the live production path, not merely a convention someone could quietly break.

- The two files that implement personalization and learning — `services/personality/repository.py`
  and `services/learning/learning_handler.py` — filter every read and write by `user_id`. This is the
  actual production learning path, confirmed live-called from `services/intent/intent_service.py`.
- **ADR-079** (owner-scoping integrity contract) makes owner-scoping **CI-blocking, not just
  conventional**: `scripts/check_unscoped_reads.py` is wired into the test suite
  (`tests/test_completion_ratchets.py`) as a ratchet — an unscoped read against any owner-bearing table
  fails the build. It generalizes ADR-075, which specifically governs personalization ownership.

**One honest precedent, worth citing rather than hiding**: `#1366` (closed 2026-07-06) was a real
violation of exactly this claim — an unscoped instance-config file leaked one user's personal context
and default GitHub repo to every user on a shared alpha instance. It was fixed within a day (`#1373`),
and ADR-079's CI ratchet now makes that class of bug structurally harder to reintroduce, not just
promised-not-to-recur. **Stating that this happened once, and what changed structurally afterward, is
a stronger trust claim than asserting a purity that was never quite true** — a user who later learns
about #1366 from any other source is better served by having read it here first.

**One loose end, flagged rather than left silent**: dead code (`QueryLearningLoop` /
`PredictiveAssistant`) implements the exact cross-user pooling this policy disclaims. It is unreachable
in production today — test-only entry point, its HTTP routes commented out and marked deprecated — but
it exists in the repo with nothing currently guarding against it being reconnected without review.
Filed as `#1613` so it can't become a silent policy violation later. This belongs in this document's
own methodology, not in user-facing text — it's a note to whoever next touches that code, not a
disclosure the user needs.

## 2. Retention: hosted vs. self-hosted are different claims, not one policy with a footnote

**These are structurally different situations and the policy must say so as two claims, not one policy
with an asterisk** — PM's framing point, and it holds up: when Piper Morgan runs self-hosted, we are
not a party to the retention question at all. There is no "our" data to have a stance on.

### 2a. Hosted (`pipermorgan.ai`)

**Current practice, stated as fact — this is what exists today, not yet what the policy should be:**

No retention or expiry logic exists anywhere in the code for conversation or message data. Verified
across `services/database/`, `services/domain/`, and the product's own background-job scheduler
(`services/scheduler/`, plain asyncio) — the only automated cleanup job anywhere is
`EthicsAuditCleanupJob` (`web/startup.py`, 90-day retention), and it purges only the `ethics_audit_log`
table (decision metadata), not conversations. Combined with `services/database/repositories.py`'s
soft-delete-only behavior and the absence of any account-deletion path in `web/api/routes/`:

> **Today, hosted conversation and message data is retained indefinitely, with no automatic expiry and
> no way for a user to fully remove it themselves.**

**What the policy should say once PM decides the practice**: this scaffold does not pre-decide it. The
honest options are (a) state indefinite retention as the deliberate practice, with a clear reason (see
§3 below for why that's not obviously wrong), or (b) commit to a retention period and build the
enforcement that doesn't currently exist. Whichever PM picks, **the published policy must match
enforced behavior** — the privacy-policy draft is explicit that a stated period we don't enforce is
worse than no stated period, because it converts a gap into a misrepresentation.

### 2b. Self-hosted

When Piper Morgan runs self-hosted, the user (or their organization) holds their own data on their own
infrastructure, with no Piper Morgan-operated service in the retention chain at all. **There is nothing
for this policy to promise or restrict here** — retention is entirely the self-hoster's own decision,
governed by whatever policies they set for their own deployment. The published policy should say this
plainly rather than silently scope everything to the hosted case and let a self-hosted reader assume
it applies to them too.

## 3. RATIFIED 2026-08-15 (PM) — no default retention limit; retain all by default

**Decision: retain all data by default, no automatic expiry.** PM agreed with HOST's independent
reasoning (below), not just the stated lean. This is now the policy, not an open question.

<details><summary>HOST's original reasoning (kept for the record)</summary>

## Open question — should there be a default limit on retention? (PM's lean stated; HOST's read given, not just recorded)

**PM's lean, stated but genuinely open**: no default retention limit. Exec's brief asked HOST to
actually weigh this rather than just record the lean as the answer, so:

**HOST's read: agree with the lean, for a reason worth stating explicitly rather than only deferring to
it.** The product's own privacy-policy draft states persistence as a *core function*, not an incidental
byproduct — "this is what allows it to behave like a colleague rather than a fresh assistant each
session." A default auto-expiry works against that promise: it would ship a product whose pitch is a
persistent working relationship with a default behavior that quietly undoes the relationship over time.
That's not a neutral default; it's a default that fights the thing being sold, and a user who discovers
their context vanished on a schedule they never chose is a worse trust outcome than one who was never
promised a schedule at all.

This does **not** mean retention should be unlimited-and-uncontrollable — see §4. The coherent position
is: **no default expiry, because the default should match the product's core promise; but real
user-facing control over their own retention (§4), because indefinite-by-default should not mean
indefinite-with-no-say.**

</details>

## 4. RATIFIED 2026-08-15 (PM) — retention settings on the roadmap, Enterprise milestone

**Decision: yes, eventually — scoped to the Enterprise milestone, not MVP.** Filed as #1634. Real
new product work (no such control exists in the code today), not a policy-wording change.

<details><summary>Original framing (kept for the record)</summary>

## Open question — should Piper Morgan offer user-facing retention settings? (genuinely undecided, left open)

Undecided per PM's framing, and this scaffold leaves it open rather than pre-deciding it. Worth naming
the connection to §3 explicitly: **if the answer to §3 is "no default limit," the case for §4 becomes
stronger, not weaker** — a product that won't impose a retention limit by default has a better trust
story if it can point to a way for a user to set their own limit. Today, no such control exists in the
code (verified: no retention-preference field or endpoint anywhere in `web/api/routes/` or
`services/database/`) — so if PM decides yes on §4, that is new product work, not a policy-wording
change over existing capability.

</details>

## 5. What HOST verified (spot-check, not a full re-audit)

Exec's brief was already carefully verified with file/line citations, commit hashes, and issue numbers
— re-deriving all of it from scratch would have been redundant effort. HOST spot-checked the three
claims this policy's headline property depends on, independently:

- `docs/internal/architecture/current/adrs/adr-079-owner-scoping-integrity-contract.md` exists.
- `scripts/check_unscoped_reads.py` exists and is invoked from `tests/test_completion_ratchets.py` (two
  call sites, one for unscoped-read count, one for repo-wide count) — confirming "CI-blocking" means
  "wired into the pytest suite as a ratchet test," not merely present in the repo unused.
- `services/personality/repository.py` and `services/learning/learning_handler.py` both filter reads
  and writes by `user_id` throughout — spot-checked directly, not inferred from the file names.
- `#1366` (closed), `#1373` referenced as its fix, and `#1613` (open, filed by Exec 2026-08-13) all
  exist as described via `gh issue view`.

All four checks confirmed Exec's claims as stated. No corrections needed to the ground truth; this
scaffold's job was the policy framing on top of it, per PM's ask.

---

**Next step**: PM review. This is a scaffold to react to, not a locked draft — §3 and §4 in particular
are stated as HOST's read and an open question respectively, not settled positions.
