# Leg A2 — Implicit Architecture Reverse-Engineered from the Incident Record

*Filed verbatim 2026-08-29. Researcher was FORBIDDEN from reading ADRs/PDRs — architecture derived
purely from what broke. Denominator: 9 incident/forensics docs in full (of 57 ops docs, ~15
incident-shaped), all 274 closed bug-labeled issue titles, 39 open bugs, ~60 keyword-reached issues,
11 issue bodies in depth. Converges independently with Lead's `failure-class-vocabulary.md`
(2026-08-11) and cites it where it names a class.*

---

## Incident cluster map (by incident mass)

| # | Cluster | ~Count | Representative citations |
|---|---|---|---|
| C1 | Intent-routing fragmentation (pre-classifier / LLM classifier / rail / elif / floor disagree) | 30+ | #855 #845 #923 #1411 #1412 #1555 #1677; accretion set #1490/#1521/#1527/#1492/#1529/#1530/#1559/#1579; summarize forensics |
| C2 | Principal dropped / single-tenant residue | 20+ | #696 #697 #1394 #1419(epic) #1466 #1507; principal-dropping-audit |
| C3 | State asserted without reading it (status lies, fabrication, wrong-empty) | 20+ | #784/#781(root) #1513 #1571 #1648 #1655; status-truth-audit |
| C4 | Silent death (broad except → feature becomes its fallback) | 254 counted sites | #158(2025, first naming) #1423 #1573; ratchet ceiling 254 |
| C5 | Fragmented clock | 15+ | #747/#750(half-fix) #1381 #1405 #1556; time-audit |
| C6 | Parallel systems / shipping-dark / dead-code-with-green-tests | 30+ findings | #963 #290 #1432 #342 #1642 #1671; false-trails audit |
| C7 | Conversation-state hijack / turn-stealing | 15+ | #888 #889 #1529 #1617 #1623 #1627 #1650 #1653 |
| C8 | Conversation-history render seam (same symptom, five names) | 12 | #574…#1489; explained by false-trails S1 (three live renderers in one page) |
| C9 | Schema/signature drift across dynamic seams | 25+ | #370 #468 #1548; census B (1,060 mypy errors → ~30 verified defects) |
| C10 | Deploy/host environment & credential resolution | 12+ | #1104 #1400 #1401; ANTHROPIC_* shadowing; Keychain suffix; Amber keychain-absent |
| C11 | Multi-agent process/git substrate | 15+ | sprint-field wipe; auto-close negation; merge-drop 08-08; amber-hooks |

## The implicit-architecture findings (compressed; full reasoning in the report body)

- **C1**: capability = the union of N surface-local opinions; at least FOUR independent routing
  claimants per utterance, nothing forces agreement. The moratorium's reframing of per-phrasing
  fixes as "corpus material, not patch tickets" is the record admitting patching was the wrong
  altitude for ~2 years.
- **C2**: identity is an optional parameter with a silent default at every seam (anonymous,
  'system', env token, global setting) — each default a cross-tenant leak or structural empty-read.
  33 of 49 principal-path test files never pass a non-None user_id: the test suite structurally
  cannot see the class.
- **C3**: status has many read-time consumers and zero write-time authority. The only integration
  that could ever show "connected" was the fake Demo plugin. Both status and time audits
  independently converged on "ONE canonical source" — evidence the architecture lacks authority
  points as a GENERAL property.
- **C4**: resilience implemented as site-local exception swallowing converts failure into false
  data; no type distinction between "source failed" and "source empty." An 8+-month-old class fixed
  site-by-site.
- **C5**: time — supply 0% (no per-user timezone anywhere: 0 of 79 migrations), consumption ~80%
  built → five improvised clocks. **A half-done class fix relocates the incident stream, it doesn't
  stop it** (#747/#750 fixed storage; every 2026 time bug is the deferred half coming due).
- **C6**: creation is cheap; decommissioning has no owner; the mount graph is the real architecture.
  Three conversation renderers reachable in one page (explains C8's five-name longevity — fixes
  landed in dead markup). Liveness determined by an unenforced reachability graph nobody owned until
  Aug 2026.
- **C7**: turn-claiming precedence is emergent from code order, not designed — the same utterance
  contested by greeting patterns, interviews, slot-fillers, fresh classification; first match wins.
- **C9**: contracts between layers exist only at runtime, and the runtime swallows them. One
  mis-annotation on `session_scope()` made mypy blind inside every DB block codebase-wide.
- **C10**: credential/config resolution is a silent-priority fallback chain nobody can see; the
  implicit architecture assumed a laptop (local disk not durable in the hosted world: #1104, #1400,
  #1401).
- **C11**: the multi-agent dev substrate is itself a shared mutable global with advisory-only
  guards; verification-by-config-presence is endemic.

## Load-bearing walls (revealed by breaking distant things) — 9 found

1. `main.py`'s inline chat handler (gutted under a `docs:` commit; severed the only live
   IntentEnricher call).
2. The intent route's 200-with-error-body contract (#385's switch to 422 bypassed every
   friendly-error layer; three "separate" bugs were one wall).
3. An orphan classifier file as SOLE carrier of ratified taxonomy (#1432 deleted it correctly and
   the ruling vanished; re-land used a pre-ruling snapshot).
4. Unowned conversations as a test-suite assumption (#1532's correct security fix made every e2e
   suite one-shot).
5. `plugin.is_configured()` (#784 changed its failure mode; six user-facing surfaces became
   structural liars for months).
6. `session_scope()`'s return annotation (three lines of typing blinded static analysis
   codebase-wide).
7. `pytest.ini` addopts (passing `-o addopts=…` silently drops archive ignores).
8. The working tree as inter-agent shared state (merge-drop: scope-perfect command, wrong
   direction).
9. The #262 preferences column never migrated — three services leaned on an unbuilt wall for 5
   months (personality dead product-wide, swallow masking the AttributeError throughout).

## Local patches to class-level problems (the trail table, compressed)

UTC-leak (2 fixes → audit finds 27 of 50 render sites wrong) · user_id gates (4 instance fixes →
#1419 epic + AST guards) · principal defaults (6 fixes over 6 months) · naive/aware TypeError
(fixed; same error one function over still live) · reminder-phrasing regex accretion (8 issues →
moratorium + Inversion) · silent-death (2025→per-site; ratchet holds line, doesn't drain) ·
fabricated confirmations (#1544 fixed twice, #1648 twice, #1655 finally names the mechanism) ·
raw-error-to-user (#875 — the POSITIVE example of escalating to the class).

**Observable trajectory**: 2025–early-2026 = point patches; from ~Jul 2026 the response shifts to
census → freeze → ratchet → canonical-service. That shift is the implicit architecture's most
important recent change and lives entirely in process artifacts, not diagrams.

## Never-breaks analysis (silence ≠ health)

- **Genuinely robust (traffic + full-denominator audit both exist)**: Postgres/UTC storage (after
  the #747/#750 class fix — the ONE place fix-the-class demonstrably ended the incident stream);
  `mail-send.sh` push-to-ref.
- **Unobserved, not robust**: knowledge graph (fails on every todo creation, swallowed; every KG
  route 500s via DI misconstruction), ChromaDB/Redis (zero functional incidents = zero observation),
  auth/JWT core (quiet, but a missing `await` silently fell back to a non-scoped key on a live
  path).
- **Unused/gated, not robust**: spatial intelligence (#342: production calling 4 nonexistent
  methods; 12 never-defined methods in notion_spatial) — despite being memory-pinned as "protected
  architectural innovation." The protection is reputational.
- **Robust-by-ratchet**: the workflow-dispatcher rail — the constrained, registry-visible part of
  routing is the quiet part. Consistent with the Inversion bet.

## Contradictions reported (not resolved)

1. Is phrasing-dependent routing an LLM problem? Failure-class 8 says no (dual implementation);
   #1467/#1677 document genuine classifier non-determinism. Both live; no doc apportions the stream.
2. #1489 titled "REGRESSION" but the same symptom exists in the alpha era — five breakages of one
   architectural fact (three live renderers) treated as separate events; nothing links them.
3. Spatial intelligence: memory pin says "protected innovation"; incident record says partly phantom.
   Both stand.
4. `staging_health.py`: CLAUDE.md presents as deliberate live exception; false-trails found it
   imported by nothing, 404ing.
5. Amber hooks property (a) deliberately open.
6. Summarize corpus row expects SYNTHESIS while the ratified design makes floor-routing correct —
   corpus and product ruling disagree.

## The report's one-paragraph synthesis (verbatim)

The incident record describes a system whose real architecture is: *N independent local opinions
where the documented architecture claims one authority* — for routing (C1), identity (C2), status
(C3), time (C5), capability inventory (#923), and even its own liveness graph (C6) — with a runtime
that converts every disagreement into silence rather than error (C4), and a test layer that
historically shared the same blind spots as the code (mocked signatures, anonymous principals,
shared session_ids). The load-bearing walls are almost all *implicit contracts nobody wrote down*:
an error-shape, an annotation, a hardcoded return, a file that happened to be the sole carrier of a
ruling. The 2026-Q3 shift from point-patching to census/ratchet/canonical-source (visible in five
audits and the failure-class vocabulary) is the record's own admission of this, and the Inversion
(#1595) plus the three "ONE canonical X" proposals are the first fixes aimed at the class of classes
rather than any instance.
