# The Un-Modeled-Noun Audit — 2026-09-08

**Dispatched**: Exec, PM-approved 2026-09-08 ("Whenever we find something like this I want to audit
the category of problem it represents to find its hidden cousins in the code" — PM, after catching
#1615 recurring verbatim as #1729 from memory). **Executed**: Arch, same day. **One-time audit, not
a recurring duty** — the durable half is Lead's object-or-none-exists line (Exec's item 1a).

## Hypothesis under test

> A defect recurs across sites when the thing it is about is a noun we use constantly and never
> modeled. With no class to attach to, a fix attaches to a *site* — so N sites means N fixes, by
> construction.

**Verdict: CONFIRMED, with one sharpening.** Three of the six confirmed cousins are not
*un*-modeled but *half*-modeled — a dict-key convention, an enum unused at the failing seam, a
renderer Protocol living in one unrelated corner. Fixes still attached to sites in all three. So
the discriminator is not "does an artifact exist" but **"can the thing be passed, typed, and
enforced across the seam where it fails."** A convention is not a model.

## Denominator (m-44)

- **Issues scanned**: 435 (47 open-MVP + 388 closed since 2026-06-01, deduped; `gh issue list`,
  2026-09-08 ~07:10 PT).
- **Candidate nouns extracted**: 10 considered against the rule "a thing the system produces or
  does, not implementation detail."
- **Checked against the model**: all 10, against `services/domain/models.py` +
  `services/shared_types.py` + targeted greps for partial artifacts (commands and hits quoted in
  the working notes; the partial artifacts are cited per-noun below).
- **Survived the ≥2-patched-sites discriminator**: 6. Dropped: *a reminder-parse* (one site —
  `temporal_utils`, many bugs, one attachment point = a bug cluster, not a cousin), *a session*,
  *an insight*, *a standup* (each modeled or single-site).

## The control case (checked, holds — and produced the audit's best evidence)

Exec predicted the confirm/offer family — which **got** objects (`SessionSnapshot`, `EffectClass`,
the `_apply_soft_offer` clobber-guard idiom, the #846 arm-site idiom) — should show compounding
rather than repetition. It does, and the evidence is in the issue *titles themselves*: the offer
family's bugs self-locate in their family ("#1623 family, member 2", "#1648's class, one question
earlier", "under #1631's 160 floor", "#1652's clobber guard"). The un-modeled families never cite
each other — #1729 did not cite #1615; PM caught the recurrence **from memory**. A modeled noun
gives a new bug an address; an un-modeled noun makes every discovery a first discovery.

Sharpest single exhibit, from the rendering family itself: #1628 — "degenerate-title guard
(#1622) **covers only the Radar seam**." A fix attached to a site, and the next surface needed the
same fix. That is the hypothesis in one sentence, written by the fix's own follow-up.

## The six confirmed cousins, ranked (sites × surface breadth)

| # | Noun | Patched sites (issues) | Model status today |
|---|------|------------------------|--------------------|
| 1 | **An empty-or-degraded answer** — "none" because verified-empty vs source-FAILED vs never-gathered | **~10**: #1425 (×5 handlers), #1544, #1639 (×2 lanes), #1645 (×2 gaps), #1675, #1570, #1657, #1530 — and **#1717 is the meta-evidence**: "the honest-degrade directives compose additively — five sites now, no aggregation" | **Half-modeled**: `source_failed` is a per-slice *dict-key convention* in `context_assembler.py` — stringly, unaggregated, cannot be typed or enforced |
| 2 | **A rendered deliverable** — markdown/structure becoming display | **6–7**: #1615, #1729 (verbatim recurrence), #1227, #1622, #1628, #1393/#1570 (scaffolding leak ×2) | **Half-modeled in the wrong corner**: `services/mux/moment_ui.py` has `RenderedMoment` + a `MomentRenderer` Protocol — the right *pattern*, wired only to MUX moments; zero coverage of chat/Slack/standup deliverables |
| 3 | **An error surfaced to a user** | **~8**: #1614, #1414, #1404, #1520, #1212, #1159, #1718, #1348 | **Half-modeled at a broken seam**: `web/utils/error_responses.py` has `ErrorCode`; #1614 shows the app-level handler rewrites `detail`→`message` while every consumer reads `detail` — the model exists and the seam un-adopts it |
| 4 | **A decline/refusal** | **~6**: #1605, #1571, #1417, #1426, #1333, #1517, #1293 | **Un-modeled**: no Decline class; #1333 already asked for "a category rule instead of a list" — the noun requesting to become a class. Entangled with *a capability* (#1632's catalog, #1428): a decline is a claim about a capability, and with no capability registry every site invents its own claim |
| 5 | **A user-local time** | **~6 display sites**: #1589, #1405, #1381, #1163, #1150, #1562 (+ the internal naive/aware class #1493/#1491/#1573/#1285, already named as a class by #1493) | **Un-modeled at display**: #1572 (browser-tz, "parse/display in USER time") is the modeling request, open |
| 6 | **A resolved repo target** | **~5**: #1388, #1567, #1641, #1646, #1226/#1199 | **Half-modeled**: `repo_resolver` (#1042) resolves, but the *result* doesn't travel — #1646: "ANALYSIS handlers resolve a repository but `get_recent_activity` never receives it" |

Seeds from the dispatch not surviving as separate rows: *a capability* folded into #4 (same noun,
positive face); Exec's four seeds otherwise all confirmed.

## What modeling would mean, per the top three (design sketches, not commitments)

1. **`GatherOutcome`** — a typed result every context slice returns: value + provenance
   (`fresh | verified_empty | source_failed | not_attempted`) + an aggregation rule (N failed
   slices → one honest sentence, not N caveats — #1717's exact complaint). Note the convergence:
   **CONNECTORS rule 1 class A already ratified this shape at the MCP boundary** (`source_failed`
   as a structured field, probe-tested both vendors). The audit says the same noun exists at every
   internal gather seam. One model, two altitudes.
2. **A deliverable model** — semantic blocks (list, summary, caveat-member per CONNECTORS rule 1B)
   rendered by per-surface renderers (web/Slack/standup). The `MomentRenderer` Protocol is the
   in-repo precedent; the work is promotion, not invention. **This is also the answer to Exec's
   rendering question** (five fixes, five sites): there is no place where markdown becomes display
   — there are N call sites with N inline conversions, and #1628's "covers only the Radar seam" is
   what that costs.
3. **Adopt-the-existing-model fixes** for errors (#3: one seam fix + consumer migration) — cheaper
   than new modeling; the class exists.

## Scope ruling (the dispatch's open question)

**Audit scope was all surfaces** — reading is cheap, and cousins #1, #3, #4 live on both sides of
the freeze line. **Modeling scope should be MCP-path-first**: `GatherOutcome` and the deliverable
model belong where new build is going (the tool layer renders through the same seam — CONNECTORS
rule 1B's member-caveat IS a deliverable-model decision already taken). Web-chat sites join as
*named members of the modeled family* when touched — the freeze governs where fixes ship, not
where classes live. Trigger for the web-chat members: the first post-beta fix that touches one.

## The guard, restated

This audit does not recur. Its durable half is Lead's one-line discipline (a fix states the object
it should have touched, or says none exists — every "none exists" is a self-reporting cousin
candidate). If a quarterly re-run gets proposed, the answer is no — the chokepoint is in the
fix-writing, not in re-reading 435 issues.

**Verified how**: issue corpus via two `gh issue list` queries (counts above, deduped in-session);
model absence/presence via grep of the two canonical model files plus targeted class greps, hits
quoted in the table; control case via title cross-citation reads. Layer: issue text + model source
— NOT runtime behavior; site counts are patched-fix counts from issue records, not a code census.

— Arch, 2026-09-08
