# #2149 Router catalog shape: design (Arch, 2026-10-31)

Status: proposed. The shape is decided; the measurement licenses the landing.
Owner: Arch (design), Lead (build and runs). Gate: Rule 7.

## The problem, as measured

The router (`inversion_router.py`, `build_routing_prompt`) shows Haiku 4.5 one flat list. Today it holds **72 operations** (66 from the rail, 6 from the registry) plus NONE and CLARIFY, about 9.6k characters of catalog text. That count comes from `derive_routing_grammar()` in Lead's venv on main.

Every single-delta change measured since 10-23 moved rows unrelated to it:
- an op add (#2132);
- one example (week_calendar, attention_query);
- the catalog order alone (10-29: the next-milestone sentinel flipped and the corpus fell 495 → 477 / 550);
- one description clause (10-30: six or more unrelated rows moved, per #2149's 10-30 table).

The fault isn't any op's wording. **In a flat catalog, every op competes with every other op on every turn, so any byte change anywhere changes the whole distribution.** No edit has a bounded blast radius, and so Rule 7 has become a stop on all catalog work.

## What a fix must hold (from #2149)

1. Removing an op is not neutral: its asks go to the nearest visible op. Any op that leaves must route its asks to NONE or CLARIFY, measured.
2. ADR-080: the LLM decides meaning and code decides permission. **The fix adds no phrasing checks in code.**
3. Rule 7 covers the whole change.
4. **The grammar is still derived, not written by hand** (decisions.log 2026-08-09).

## Options

| Shape | Bounds an edit's blast radius? | Cost | Verdict |
|---|---|---|---|
| (i) **Two-stage**: the LLM picks a group, then an op within that group | **Yes, by construction.** An edit to group G's op text is only in G's stage-2 prompt, so it can't move a row whose stage 1 went elsewhere. Only group-level text is shared. | A second Haiku call on routed turns (latency and cost, measured below). Stage-1 errors aren't recoverable in stage 2. | **Chosen** |
| (ii) Grouped catalog with shorter per-op text, one call | No. It's still one prompt, so any delta perturbs all of it. The 10-29 control shows order alone moves rows, and grouping is an order change. | None | Rejected as the fix. Its headers become stage 1's text. |
| (iii) Router-invisible entries | Per op only. It shrinks the list, but constraint 1 applies to each removal. | Small | Kept as a tool (#2132's ratchet, ceiling 1), not the shape. |
| (iv) Retrieval-narrowed catalog (top-k ops by embedding similarity) | Partly. | Needs #2226's embeddings. | **Rejected:** code choosing which meanings the LLM may see, by text similarity, is a phrasing decision in code (ADR-080). |

## The design

1. **A declared group on every routable entry.** `WorkflowEntry(..., route_group=...)` is a required field for `action_triggered=True` entries, from a closed enum. The six registry-only canonicals carry theirs in a `ROUTE_GROUPS` map beside `ACTION_DESCRIPTIONS` in `action_registry.py`. This is entry metadata, like `outwardness`. The grammar still derives from the registry (holds constraint 4), and a ratchet fails any routable entry without a group.
   - The groups follow what the user is asking about, not the rollout cohort, which is why `flip_group` can't be reused (18 ops sit in `read_status`). They aren't the legacy classifier category either (27 ops have none).
   - Lead and I draft the starting enum from the 72 ops: about 8–10 groups (work items and issues, calendar and time, todos and reminders, projects and portfolio, documents, memory and insights, identity, help and guidance, conversation, status and priorities), with no group over about 12 ops.
   - Group text (a name plus one line) is the only text shared across groups.
2. **Stage 1** shows the group list plus NONE and CLARIFY, with session state. It returns one group, or a plan of up to N groups for a multi-op message (the plan form moves up a level). NONE and CLARIFY are decided here.
3. **Stage 2** shows only that group's ops plus CLARIFY and **OTHER_GROUP**. OTHER_GROUP renders as CLARIFY. Code never re-routes it to another group, because a code-side retry over groups would be code choosing meaning. The rate of OTHER_GROUP is measured as stage 1's error rate.
4. **Validation is unchanged downstream.** `_parse_and_validate` still checks that the op is in the grammar, and dispatch, consent and the four-state contract don't change. Only how the op is chosen changes.
5. **No op leaves the catalog in this change.** That keeps constraint 1 off the table for the shape change itself.

## How the landing is licensed (preregistered here, before any run)

- **Isolation, the property the shape exists for:** repeat the three known-bad single deltas (the week_calendar example, the attention_query example, the get_project_status clause) on the two-stage branch, ×6 each. **Pass: no row moves whose stage-1 group differs from the edited op's group.** Rows inside the group may move; that's the bounded radius, and Rule 7 judges them as usual.
- **Parity:** the full corpus and the ×6 screen on the two-stage branch with no deltas. **Pass: the corpus is ≥ the flat baseline on the same day's main (the same scorer), and no live-dispatch row moves from correct to wrong.**
- **Cost:** p50 and p95 router latency, and tokens per turn, flat vs two-stage on the corpus run. **This isn't a gate. The numbers go to Exec and xian with the result**, since a second call is a product cost.
- **Stage-1 error:** the OTHER_GROUP and CLARIFY rate on the corpus. Over 3% means the enum is drafted again, not that code gets patched.
- **If isolation fails:** the shape is wrong and I'll rule again. No partial landing.

## Sequencing

- #2195 and #2197 land after this, inside their groups. That's the point: their edits then touch only their own group's prompt.
- Until it lands, catalog edits stay under the current Rule 7 stop.
- Build order (Lead): the `route_group` field and its ratchet (no behaviour change), then stage 1 and stage 2 behind a flag defaulting off, then the preregistered runs, then my ruling.
- Not in scope: removing ops; the legacy classifier; the floor.

## Step 3 result and the one redraft (Arch, 2026-11-01)

**Result, read against the licence above** (Lead's runs, `dev/2026/11/01/controls/2149-step3-*`, Haiku 4.5):
- **Isolation held.** Stage-1 prompts were byte-identical across the three delta arms, and stage-2 prompts differed only inside the edited group. No phrase moved 6/6 outside its delta's group. The few outside moves (the corpus ×1 and the ×6 spreads) were on rows the flat router also spreads, with identical prompts on both arms, so they're sampling. This is the property the shape exists for.
- **Parity failed:** 412/550 against flat's 489. 88 rows were lost and 9 gained, and the QUERY shared subset regressed (12 → 9).
- **Stage-1 error was over the bar:** OTHER_GROUP 24/559 = 4.3%.
- So the shape stays off. Under the licence, that means a redraft, not a code patch.

**Why it lost, from the 88 rows:**
- 25 rows ended at stage 1 on NONE or CLARIFY, and 23 went to the wrong group. These are mostly the guidance, trust and capability asks ("open the help menu", "do you trust me with this decision", "help me set up my projects"), plus completion history ("when was the auth refactor shipped").
- In each case the flat router resolves the ask by the *operation* (`get_capabilities`, `explain_trust`, `get_contextual_guidance`, `check_completion_status`). A one-line group summary doesn't carry that.
- The other 36 rows ended CLARIFY or OTHER_GROUP at stage 2, inside small groups of near-synonyms.
- The stage prompts copy the flat rules, so the loss is the information stage 1 is given, not their wording.

**The one redraft (preregistered here, before any render):**
1. **Stage 1 shows each group's line followed by its operations' names**, names only, with no descriptions and no examples. The `TestRouteGroupRatchet2149` pin "stage 1 names no op" becomes "stage 1 carries op names and no op description or example".
   - Isolation still holds by construction for the edits that broke the flat router: descriptions, examples and clauses live only in stage 2.
   - An op add, removal or rename changes stage 1. That's a real catalog change, and Rule 7 judges it as one.
2. **Nothing else changes in this redraft:** not the enum, the group lines, the stage-2 prompt, nor CLARIFY's wording. If both stage-1 and stage-2 changed, a result couldn't be attributed. The stage-2 CLARIFY losses are read again after (1), since a better stage 1 changes which rows reach stage 2.
3. **Same runs, same pass.** Isolation is the three deltas, ×6 and corpus ×1. Parity is the full corpus against a same-batch flat baseline: ≥ flat, and no live-dispatch row worse. Stage-1 error must be ≤ 3%, with the group-confusion table. Cost is reported.
4. **If parity still fails, the two-stage shape is rejected.** No second redraft. I'll rule again on the flat catalog: router-invisible entries, option (iii), and what Rule 7's stop means for #2184, #2195 and #2197.

## Run 2 and the end of the two-stage shape (Arch, 2026-11-01)

**Run 2** (stage 1 with op names; `dev/2026/11/01/controls/2149-step3b-*`):
- Isolation held again: 0 of 144 ×6 samples moved in any arm.
- Parity failed again: 428/550 against flat's 490. 76 rows lost and 17 gained. QUERY and IDENTITY regressed.
- Stage-1 error: 4.1%.
- Under the condition above, **the two-stage shape is rejected.** The flat catalog is the router. Total spend: $5.67.

**What the experiment settled:**
- **Bounded radius and routing accuracy pulled against each other here.** The flat list's accuracy comes from every op competing with every other op in one view. That's also why every edit moves unrelated rows.
- So the radius problem isn't solved by splitting the list. It's solved by **not editing the router's render to get an argument or a sub-choice.**

**Rulings on the flat catalog:**
1. **Rule 7 stands unchanged.** A router render change lands only on a passed ×6 and the full run, and a per-row ×6 move outweighs a category gate. Both runs confirm the flat router is the more accurate shape, and that its sensitivity is real.
2. **Op-local resolution, outside the router.**
   - Once the router has picked an op, that op's handler may resolve its own sub-choice with its own LLM call, for example *which* milestone a message names.
   - The call gets the user's message and the candidates code read on this turn.
   - Code binds only to a candidate from that read (#2184 D2). No match, a tie or a failed call renders the op's default, never a nearest guess. Failure is never shown as empty (#2151).
   - It doesn't touch the router request, so Rule 7 doesn't apply to it. It needs its own corpus rows, pins and a served check.
   - The LLM decides meaning and code decides permission, as ADR-080 requires.
   - This replaces #2197's path through declared router args (#2186 unit 2) for the milestone selector.
3. **Gated issues:**
   - **#2197 and #2184** proceed by (2), on `list_milestones` and the milestone-issues read.
   - **#2195** was never blocked by the shape: its literal deletions change what reaches the router, not the router's render, and they go list by list under the existing deletion gate.
   - **#2186 unit 2** (declared args in the render) stays under Rule 7 for any key it still needs.
4. **The code:**
   - The flag path, both stage prompts and parsers, and the runner's two-stage subcommands come out (skill `delete-module-safely`). A dormant flag that routes worse is a liability.
   - `route_group` and its ratchet (step 1) come out with them, unless Lead names a live consumer.
   - This record, the reports and decisions.log keep what was learned.
