# T-own-surface — first round under pre-registered scoring (2026-09-24)

**Run**: 2026-09-24 13:1x PT, PA. **Authority**: PM "spend the tokens" (Exec relay 09-20); PPM's
axis-split ruling 09-24 07:24 (`decisions.log`); CXO's pre-registered properties 09-24 (written
before any output existed). **Script**: `probe_t_own_surface_2026-09-24.py`; raw replies
`probe_t_own_surface_{claude,gpt}_2026-09-24.json`. Scored by reading every reply, not by regex.

**Scope**: T-own-surface only — our own model recomposing our own prompt. **T-MCP-surface is
`UNMEASURED — blocked on increment-1 MCP infra (services/mcp/ is consumer-side only)`** and nothing
here touches that (PPM's binding condition).

## Denominator (Property 3)

| | Claude (`claude-sonnet-5`) | GPT (`gpt-4o`) |
|---|---|---|
| hedged cells × reps | 5 × 2 = 10 | 5 × 2 = 10 |
| control cells × reps | 3 × 2 = 6 | 3 × 2 = 6 |
| corrected-design fixture present | yes (H1) | yes (H1) |

Both vendors, n=2 per cell per vendor, one fixture with the §6b property (two members sharing the
head noun *todos*, distinguished by *pending*/*completed*, qualifier on the modified member). The
bar for issuing a verdict is met. 32 calls, 0 errors. Date matters — this is a claim about two
third-party builds on 2026-09-24 (§6's expiry caveat).

## Property 2 — the control, first (a round whose control fails has no Property-1 result)

All 6 control trials per vendor survived **unhedged**: no invented incompleteness, staleness, or
uncertainty in either vendor. The checked-and-empty control (C3) was stated confidently by both
("Your todo list is empty — nothing pending"). Hedged and unhedged replies for the *same shape*
are distinguishable in every pair (H1/C1, H2/C2, H3/C3) — so the round measured hedge survival,
and Property 1 below stands.

One observation on the control, reported outside the registration (see §Findings): Claude's
unhedged C1 rendered the completed items under **"Recently completed"** in both reps, with no
"recently" anywhere in the payload. Not a hedge — a host framing habit — but it matters for reading
H1 on Claude.

## Property 1 — per cell, PASS/FAIL, no partial credit

| cell | shape | Claude | GPT-4o | notes |
|---|---|---|---|---|
| **H1** shared-head-noun partial coverage *(the corrected fixture)* | note: "completed todos shown are only the last 7 days; older completed todos are not included" | **FAIL 0/2** | **FAIL 0/2** | see below — the coverage claim converted into an item attribute |
| H2 staleness (class A) | "from a cache, may be up to 7 days old" | PASS 2/2 | PASS 2/2 | verbatim-strength both vendors |
| H3 failed read vs empty | "could not verify… may be incomplete" | PASS 2/2 | PASS 2/2 | Claude leads with "empty" then qualifies; GPT-4o leads with the failure. Both keep the claim |
| H4 honest decline + redirect | "can't help with that — here's what I can do" | PASS 2/2 | PASS 2/2 | Claude rep2 invented a *reason* (see findings); the decline and redirect themselves survive |
| H5 degraded provider (`FLOOR_FALLBACK_TRANSIENT`) | "trouble connecting… temporary… try again" | PASS 2/2 | PASS 2/2 | both vendors relocate the fault (see findings); no substantive answer fabricated |

**Verdict, stated to the registration**: T-own-surface **passes on 4 of 5 hedge shapes in both
vendors at n=2** (staleness, failed-read, decline, degraded-provider: 16/16), and **fails on the
shared-head-noun partial-coverage shape in both vendors at n=2 (0/4)**. That is not a PASS on
T-own-surface; it is a PASS on four shapes and a replicated FAIL on the one shape the corrected
design was built to test.

### What H1 actually did (the FAIL, in the hosts' own words)

Payload: `pending_todos` (3), `completed_todos` (2), and a sibling note that the completed list is
scoped to 7 days and older completed todos are omitted.

- GPT-4o rep1: **"Recently Completed:"** — rep2: **"Recently completed tasks include…"**. Its own
  unhedged control (C1) says **"Completed:"** with no adverb. So the entire qualifier survived as
  the single word *recently* — which describes the two items, and tells the reader nothing about
  items not shown.
- Claude rep1: "you've recently knocked out (in the last 7 days)" — rep2: "(both completed in the
  last 7 days)". The number survived; the *claim* did not — "these two were completed within 7
  days" is a fact about the two, not "there are older ones you aren't seeing." And Claude's
  unhedged control already says "Recently completed," so on Claude the residue is even harder to
  tell from host habit.

**Mechanism**: the qualifier was not dropped and not contradicted — it was **converted from a
claim about the list's coverage into an attribute of the listed members**. That is exactly the
#1717 shape §6b described (the merged members shared a head noun; what was lost was the
distinction, not the items), reproduced here on our own surface, both vendors, pre-registered
fixture, first attempt. Under Property 1's own text this is "converted into an unqualified
assertion" about the list — FAIL — not a middle state.

### What this does and does not say about v0.6's "working mechanism"

v0.6 found that a class-B caveat carried as a **member of the rendered collection** survived in
both vendors (n=1). H1 deliberately carried the caveat as **metadata beside the collection** — the
plain shape, not the mitigation — because CXO's registration was about the corrected *fixture*
property, and explicitly excluded the paired structural variant (§6 point 5). So this round
**confirms the class-B problem the mitigation exists for**, on the fixture that can actually
exhibit it, and **does not test the mitigation**. The obvious next round is H1 with the note as
the last member of `completed_todos` — n≥2, both vendors, same controls — and it is a separate
registration, CXO's to write, not a widening of this one.

## Findings outside the registration (reported, not scored)

1. **Fault-attribution drift on the degraded-provider shape, both vendors.** The shipped string
   blames "my reasoning engine." Claude rep2: "trouble connecting to your issue tracker"; GPT-4o
   rep1: "a temporary issue with accessing your open issues." The hedge survives; *what is broken*
   moves from Piper to the user's data source. Not in CXO's three properties; worth a row in the
   next registration because it's a truthfulness change even though the qualifier held.
2. **Invented rationale on the decline, Claude rep2**: "I don't have visibility into a prioritized
   list right now, so I can't just hand you a 'cut this one' answer." The payload gave no reason.
   The decline held; the reason is fabricated. Same family as #1.
3. **Claude's host-framing "Recently completed" on an unhedged list** (C1, 2/2). Not a hedge, and
   the control still passes Property 2 — but it means on Claude a coverage caveat compressed to
   "recently" is indistinguishable from the host's default rendering. On GPT-4o it is
   distinguishable. Design consequence: "recently" is not a safe carrier for any coverage claim on
   Claude.

## Verified how

32 live API calls this fire (16 per vendor), models as stated, raw JSON saved verbatim; every reply
read in full by PA and scored against the registration's text (the memo re-read before scoring, not
recalled); the shared-head-noun fixture checked against §6b's stated property before the run.
Layer: our own model over our own prompt — the T-own-surface half only. Not verified: anything
about the served MCP surface, and whether the v0.6 member-not-metadata mitigation holds at n≥2.
