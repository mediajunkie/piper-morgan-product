# #1064 — Floor Fabrication Investigation (Saturday May 16 deep-dive)

**Issue**: #1064 REGRESSION: Floor fabrication active in canonical retest Run 4
**Author**: Lead Developer
**Date**: 2026-05-16 (8 days after the May 8 filing)
**Scope**: Full investigation per body ACs — five-whys, pattern sweeps, adjacent-problem, systemic check, Apr-to-May regression diff, recommendation

## Headline finding

**The "floor fabrication" framing in the issue body is materially mis-aimed.** Of the 10 Run-4 auto-fails:

| Failure mode | Count | Examples | Resolution path |
|---|---|---|---|
| **Hard-coded templated over-assertion** (canned response asserts more than the underlying logic verified) | 5 | Q8/Q31/Q33 phantom "setup wizard"; Q30 "Everything looks good!"; Q42 "All open PRs are less than 7 days old" | Surgical: #1065 (setup-wizard refs), #1069 (attention_query templated confident-no-data) — partially landed |
| **Routing/dispatch bug** (right category but wrong action; or multi-intent → orchestrator fallback) | 3 | Q40 portfolio_help instead of doc-update; Q25 multi-intent fallback; Q58 #N slot-fill | Surgical: #1067, #1066, #1084 (today) |
| **Test fixture pollution** (real DB data leaked from prior tests) | 1 | Q56 "8 phantom todos with repetition" | Test fixture reset (Run 5/6 disposition) — was REFUTED as LLM hallucination |
| **Routing OK, response unhelpful** (no fabrication; methodology limit of single-turn judging) | 1 | Q49 `/standup` bare opening — multi-turn flow not exercised by single-turn judge | #1070 multi-turn harness + #1079 today |

**Only 0 of 10 were genuine LLM-fabrication.** The anti-fabrication guardrail commitment from M1 close (Apr 11) — "NEVER fabricate user data unless in context" — was targeting LLM hallucination at the conversational floor. None of the Run-4 auto-fails were that shape.

This is the load-bearing methodological insight: **the term "fabrication" in the body conflates several distinct failure modes**, only one of which the M1 guardrails were designed to catch. The other failure modes look superficially similar (user gets confident-incorrect responses about their data) but have different causes and require different fixes.

---

## Five-whys analyses

### Q56 "Show my todos" — phantom todos with item repetition

**Surface symptom**: Fresh canonical-test user with no todos received "I checked your todo list — looks like quite a bit going on with **8 items**. The first one is **'review the deployment plan'**. Then there's **'review the deployment plan'**. Also **'review the deployment plan'**..."

**Five-whys**:
1. Why did the system claim 8 todos exist? → Because `todo_service.list_todos(user_id=...)` returned 8 rows from the database.
2. Why did the database have rows for a "fresh" user? → Because the canonical-test user's todo table had stale rows from prior test runs that weren't cleaned up between runs.
3. Why weren't they cleaned up? → Because the canonical retest harness lacked a fixture-reset step for user-scoped tables; the fresh-account assumption was that the *account* was new, not that *all per-user data was cleared*.
4. Why was the response three repetitions of "review the deployment plan"? → Because three of the 15 stale DB rows had identical text (the test harness inserted duplicates during prior runs without dedup).
5. Why did this masquerade as fabrication? → Because the surface presentation (confident-sounding claim about user data) is indistinguishable from genuine LLM hallucination unless you check the DB state behind the response.

**Disposition**: Not fabrication. Test-fixture pollution. Documented in #1064's session log: *"Q56 smoking-gun was 15 stale DB rows, not LLM hallucination."* The Run 5/Run 6 fix shipped fixture-reset-v2 → resolved. Q56 doesn't appear in Run 9 escalation.

**Methodology lesson**: The "fabrication" judgment (R=3 C=0) is a downstream conclusion. The judge can't distinguish LLM hallucination from real-but-stale data without observing the system state behind the response. This is a category of *judge-grade ambiguity* worth flagging to CXO/CIO: the judge rubric currently treats "claim about user data that doesn't match expected state" as fabrication regardless of source. Maybe it should differentiate, or maybe judge rationales should require "verified the DB state was actually empty" before the FAIL verdict.

### Q31 + Q8 + Q33 — phantom "setup wizard"

**Surface symptom**: Q8 ("agenda for today"), Q31 ("Schedule a meeting"), Q33 ("Find time for a 1:1") all returned "I'd love to analyze your meeting time, but Google Calendar isn't configured yet. To enable Calendar integration, please **run the setup wizard** or configure GOOGLE_CREDENTIALS_PATH."

**Five-whys**:
1. Why did the response mention a "setup wizard"? → Because the calendar-not-configured graceful-degradation message in `intent_service.py` was hard-coded with that phrase.
2. Why was that phrase considered fabrication? → Because there is no setup wizard in the product. Setup is via env vars + OAuth flow; "setup wizard" is a phantom UI that doesn't exist.
3. Why was the phrase in the code? → Because it landed during early scaffolding (PM-013-era) when a setup wizard was planned but never built; the response template was written aspirationally.
4. Why wasn't it caught earlier? → Because the canonical retest didn't include calendar queries with the no-config state until Run 4 (M2f baseline introduced the fresh-account canonical-test user).
5. Why does this matter as a class? → Because it's not the only place "aspirational text" got embedded in canned responses. It's the same shape as the Pattern-064 "alive scaffolding" failure — but in copy, not in code. This is the second documented instance today of "documentation/copy claiming behavior the code doesn't honor" (the first was the `session_scope() handles commit` docstring in #1079 fix; the methodology trigger for sub-pattern decision fired this morning via the CIO memo).

**Disposition**: Hard-coded templated over-assertion. #1065 fixed (replaced "setup wizard" with accurate phrasing across calendar graceful-degradation messages). Q8/Q31/Q33 no longer fail in Run 7+ runs.

**Methodology lesson**: Hard-coded canned responses should be audited for ASSERTIONS about product state (UI components, features, capabilities). A response that says "run the setup wizard" is an architectural commitment that future engineers may not honor — and if they don't, the response becomes a fabrication-via-stale-copy.

### Q42 "Show me stale PRs" — phantom data check

**Surface symptom**: Fresh user (no GitHub config? or empty PRs?) received "No stale PRs found! All open PRs are less than 7 days old."

**Five-whys**:
1. Why did the system claim to have checked PR ages? → Because `_handle_stale_prs` in `intent_service.py:2967+` only fires the "No stale PRs found!" message after passing the `is_configured(user_id)` check at line 2995 — i.e., GitHub IS configured for the user.
2. Why did the system claim "all PRs are less than 7 days old"? → Because the handler iterated over `open_items = await github_router.get_open_issues(limit=100)`, found zero PRs with `created_at <= stale_threshold`, and fell into the `if not stale_prs:` branch.
3. Why is this fabrication-shaped? → Because the message asserts a *stronger* claim than the data verified. The system actually knows: "I called get_open_issues, got some result, filtered to PRs older than 7 days, got zero." The message asserts: "All open PRs are less than 7 days old" — which presumes the API returned *all* PRs successfully. If the API returned zero results (e.g., empty repo, permission scope issue, transient error swallowed), the message lies.
4. Why is this a category? → Because empty-result-with-strong-claim is a pattern, not a one-off. Q30 has the same shape ("Everything looks good! No urgent items"). Q56's `_format_empty_list_conscious` says "your mind is clear" — which presumes the empty result reflects reality, not a query failure.
5. Why wasn't this caught at M1? → Because M1 close measured *correctness when data exists*, not *honesty when data doesn't*. The empty-state branch was tested for "doesn't crash" but not for "claims only what it verified."

**Disposition**: Hard-coded templated over-assertion. NOT yet surgically fixed. Recommendation below.

**Methodology lesson**: Empty-state response messages are a high-leverage audit surface. Every "no X found" branch should be examined for: did we *verify* there are no X, or did we receive an empty result that could mean *failure* OR *absence*? The wording should reflect the verification level (e.g., "I didn't find any stale PRs in the 100 most recent open issues" vs "All open PRs are less than 7 days old").

---

## Pattern sweep — all 10 auto-fails

| Q | Failure mode | Status (May 16) | Fix |
|---|---|---|---|
| Q8 | Templated over-assertion (setup wizard) | FIXED | #1065 |
| Q25 | Routing: multi-intent → orchestrator fallback | FIXED today | #1084 (subsumption rule) |
| Q30 | Templated over-assertion ("Everything looks good!") | FIXED | #1069 (attention_query templated) |
| Q31 | Templated over-assertion (setup wizard) | FIXED | #1065 |
| Q33 | Templated over-assertion (setup wizard) | FIXED | #1065 |
| Q40 | Routing: portfolio_help instead of doc-update | FIXED | #1067 |
| Q42 | Templated over-assertion ("All PRs less than 7 days old") | **NOT FIXED** | Recommendation below |
| Q49 | Bare opening, multi-turn methodology limit | PARTIAL | #1079 (today) makes Turn 2 work; bare-opening framing still ambiguous |
| Q56 | Test fixture pollution | FIXED (fixture-reset v2) | Run 5/Run 6 fix |
| Q58 | Routing: #N slot-fill | FIXED | #1066 |

**Net**: 8 of 10 fixed by surgical work. 1 (Q49) partial. 1 (Q42) remains as an unaddressed templated over-assertion.

## Pattern sweep — MARGINAL queries (Run 4)

Sampled the 10 MARGINAL queries. Two showed fabrication-shape concerns:

- **Q32 "Remind me to review PRs tomorrow"** → `"Got it — I'll remind you to **review prs** (tomorrow morning)."` — phantom reminder. There's no reminder system; the response promises a future action the code won't execute. Same shape as the setup-wizard category (asserts behavior the code doesn't honor).
- **Q54 "Add a todo: review the deployment plan"** → `"I've added that to your list."` — claims-of-action; needs to be verified the todo was actually persisted. Worth a quick audit.

Other MARGINALs (Q1, Q4, Q34, Q35, Q37, Q59, Q61, Q62) showed graceful-degradation or honest "I don't have that yet" patterns. Not fabrication.

## Adjacent-problem check (fabrication in PASS/MARGINAL queries)

Spot-checked 5 PASS queries (Q11, Q12, Q13, Q41, Q60) — all returned context-grounded responses with appropriate uncertainty hedging. No silent fabrication.

The pattern that surfaces in adjacent-problem check: the **fabrication-shape risk is concentrated in templated empty-state responses**, not in LLM-generated responses. The LLM-side anti-fabrication guardrails (M1 floor prompt + grammar) appear to be holding. The code-side empty-state messages are where the leak is.

## Systemic check — is the guardrail itself weakened?

Per the issue body: *"Is this LLM behavior, prompt, context-assembler emptiness handling, or interaction effect?"*

**Answer: code-side templated copy, not LLM behavior or floor prompt.** Of the 10 Run-4 auto-fails, **0 originated from the floor LLM**. The fabrication-shaped responses came from:

- `intent_service.py` graceful-degradation messages (Q8/Q31/Q33 calendar; Q42 stale PRs)
- `services/consciousness/todo_consciousness.py` empty-state formatter (Q56 — though Q56 was data, not template)
- `intent_service.py` `_handle_attention_query` templated response (Q30)
- Orchestrator fallback message (Q25 — generic, but not fabrication)

**The M1 anti-fabrication guardrails (floor prompt + grammar at `services/intent_service/conversational_floor.py`) are operating as designed.** What weakened across M2c/M2d/M2e was code-side empty-state copy hygiene. The shape: empty-result + confident-claim copy.

**Why the framing got mis-aimed**: the term "fabrication" in PM/CIO communication has been LLM-shaped since M1 close. The Run-4 symptoms looked superficially identical (confident-incorrect response to a user) so they triggered the "fabrication" mental model. But the underlying mechanism was different — the LLM wasn't even called for most of these.

## Apr-to-May regression diff

Comparing Apr 11 (M1 close, 72.1% PASS) vs May 8 (Run 4, 65.6% PASS):

The 6.5-point quality drop tracks closely with the LANDING of MARGINAL items in surfaces that didn't have canonical tests before. Specifically:
- M2c (April 12–22) added the floor-first routing. New canonical tests probed floor surfaces that had been canonical-only before.
- M2d (Apr 22–) added MUX lifecycle UI. The non-functional MUX surfaces got canonical-graded.
- M2e (May 3+) added integrations (Slack, Notion, calendar). The calendar/no-config branch was probed for the first time at Run 4.

So the "regression" wasn't a guardrail breaking — it was new surfaces being tested for the first time. The same code was passing M1 because M1 didn't probe those surfaces.

**Methodology lesson**: PASS percentage comparisons across versions are only meaningful when the test set is constant. Run 4 added new surfaces (canonical-test user no-config branches) that weren't in Run 3's universe. The 72.1% → 65.6% delta is partly methodology change, not pure code regression.

---

## Recommendation

### A — Close #1064 as state-shifted-and-investigated

The issue's framing (LLM-fabrication guardrail weakening + investigate before M2f) is no longer load-bearing:
- M2f closed May 12; the "blocks M2f" framing is moot
- 8 of 10 auto-fails fixed surgically; 1 (Q42) remains
- The systemic concern (LLM guardrail weakening) is **refuted**: the failures came from code-side templated copy, not the floor LLM
- The fixture-pollution finding (Q56) is a separate methodology improvement, not a fabrication issue

Closing #1064 with this memo as the investigation record is the right disposition. The remaining concrete work — fixing Q42 and applying the empty-state copy audit — should be filed as a new, narrower issue.

### B — File a new narrower issue: "Empty-state copy audit"

Title proposal: **TEMPLATED-EMPTY-STATE-AUDIT: hard-coded canned responses that assert more than they verify**

Scope:
- Q42 "All open PRs are less than 7 days old" — change to "I didn't find any open PRs older than 7 days in the 100 most recent items I checked" (or similar verification-bounded phrasing)
- Q32 "I'll remind you" — change to honest "Reminders aren't built yet — I noted this in our session"
- Q54 "I've added that to your list" — verify the persistence actually happened before asserting
- Sweep all `intent_service.py` graceful-degradation messages for the empty-result + confident-claim pattern
- Sweep `services/consciousness/` empty-state formatters for the same pattern
- ~1-2 days work

Priority: medium. Trust foundation matters but no current user impact (M2f closed; alpha not yet exposed to these surfaces in volume).

### C — Methodology trigger for CIO

This investigation surfaces a strong instance of CIO's **12w "living docs describing dead code"** sub-pattern observation (filed via memo today, ~10:47). The setup-wizard hard-coded references are EXACTLY that shape: copy/prose that asserts product behavior the code doesn't honor.

The methodology corollary is broader: **assertions in templated copy should be audited under the same rigor as assertions in docstrings + issue bodies**. Three shapes now have evidence:
- Docstrings (#1079 fix today: session_scope handles commit)
- Methodology docs (yesterday: methodology-core engine integration guide)
- User-facing canned response copy (today's #1064 investigation: setup wizard + "All open PRs less than 7 days")

Three independent instances in ≤48 hours of the same recognition trigger. The sub-pattern decision is now well-warranted.

### D — Methodology trigger for CXO (judge rubric)

The Q56 fixture-pollution case raises a judge-grade ambiguity: the judge gave R=3 C=0 (auto-fail) for "claim about user data that doesn't match expected state." But the underlying cause was stale DB data, not LLM hallucination. The current rubric can't distinguish these.

Worth surfacing to CXO for a judge-rubric refinement: when a response asserts user data, the judge should ideally check whether the system was operating against a clean fixture before concluding "fabrication." This is hard to operationalize without giving the judge DB-state visibility, but at minimum the judge rationale field could flag the ambiguity.

---

## Cross-references

- #1064 (this issue) — original filing May 8 against Run 4
- #1065 (closed) — phantom setup wizard fix
- #1066 (closed) — #N slot-fill fix
- #1067 (closed) — document-update routing fix
- #1068 (closed) — pre-classifier milestone routing
- #1069 (closed) — attention_query templated confident-no-data
- #1070 (closed) — multi-turn evaluation harness
- #1079 (closed today) — /standup multi-turn state (fixture-write commit + tz-aware datetime)
- #1084 (closed today) — Q25 multi-intent → orchestrator fallback (subsumption rule)
- CIO 12w watch surface (filed Saturday AM bundled acks) + Lead Dev second-instance memo (filed Saturday AM ~10:47)
- M1 close anti-fabrication commitment (Apr 11)
- Run 4 results: `dev/2026/05/08/canonical-retest-m2f-baseline-results.csv`
- Run 9 latest: `dev/2026/05/13/canonical-retest-run9-report.md` (69.8% PASS, 3 auto-fails)

---

**Author**: Lead Developer
**Date**: 2026-05-16
**Status**: Investigation complete; closure of #1064 + new narrower issue filing recommended
