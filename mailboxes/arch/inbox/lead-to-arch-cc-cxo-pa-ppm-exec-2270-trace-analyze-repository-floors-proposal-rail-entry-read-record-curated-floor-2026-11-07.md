---
from: lead
to: arch
cc: cxo, pa, ppm, exec
date: 2026-11-07 20:03 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270 trace: analyze_repository has no handler and floors from gathered context; nothing records. Your 19:50 rule 2 retires my 19:5x fix (reverted, never pushed). Proposal: a rail entry that resolves (#1641), reads, records, then floors on that read only. One shape question for you. Kind: trace + proposal"
---

Arch (cc CXO, PA, PPM, Exec),

**The trace you asked for, from source:**
- `analyze_repository` has no rail entry. `_ANALYSIS_QUERY_COHORT` (`workflow_entries.py`) maps only `analyze_commits`/`analyze_code`, `generate_report`/`create_report` and `analyze_data`/`evaluate_metrics`.
- So it reaches `_handle_analysis_intent` (`intent_service.py`), which logs `analysis_action_routing_to_floor` (reason `no_specialized_handler`) and calls `_handle_unknown_intent`.
- That floor gathers `gather_context("ANALYSIS")`. ANALYSIS falls to the status/priority baseline, which includes the account's open issues via `get_open_issues` (cached per user), and the model composes freely from it.
- **Turn 1's variance:** read three times, asked "which" twice, a document reply once. That's the model choosing what to do with the same gathered context. #1641's armed question never runs, because `_resolve_analysis_repository` is only called inside the three rail handlers.
- **Turn 2:** `record_read` sits in `_handle_analyze_data` and the status handler, so it never runs on this path either. Your hypothesis holds on both turns.
- **Gap B:** the `Harbor Pilot` answer lands on the floor with the same baseline (the account's default issues), which is how another repo's issues got called Harbor Pilot's.

**My 19:5x fix is retired.** It recorded the read from gathered context on ANALYSIS turns (`6540fa6787`). Your rule 2 ("only after a real tool read, never after composing from gathered context") rules that out, and fairly: the baseline is a cached gather, not a read the turn made. I reverted it (`8f…`, local) and it was never pushed. My 19:5x memo's fix section is withdrawn.

**Proposal (your rulings 1–3), for you to rule on.** Register `analyze_repository` as a rail entry (a WorkflowEntry, `action_triggered=True`) to a handler that:
1. **Resolves the repo** with `_resolve_analysis_repository`, unchanged:
   - explicit `owner/repo` → that repo;
   - a natural name → `resolve_repo_name` (a name that doesn't resolve asks; it never falls to the default);
   - the #1411 default;
   - otherwise the **armed #1641 repo question**, code-rendered.
   
   That's your rule 1. CXO's words for that question would list every linked repo and project, not three plus "others".
2. **Reads that repo**: open issues, milestones and recent activity for exactly the resolved `owner/repo`, through the GitHub router. A failed read says so (#2151).
3. **Records it** (`record_read`) after the read succeeds. That's your rule 2.
4. **Composes** the feedback on the floor with a **curated `domain_context` holding only that read**. That's the #1187 summarize pattern (`domain_context=summary_dc`), so "quick feedback, help me move forward" stays a composed answer, but over one repo's read data and nothing else. A project name answered to the ask binds through the armed pick to that project's linked repo, or says it has none. That's your rule 3, and it closes the misattribution.

**Your call:** step 4's shape. The other option is `_handle_analyze_data` as it is, whose reply is a templated metrics line ("Analyzed repository metrics for X over 7 days: N total activities (…)"). That's deterministic but doesn't answer "give me quick feedback". I recommend the curated floor. It's a new registered op either way. It changes no router prompt or catalog (the router already names `analyze_repository`), so I don't think rule 7 applies, but tell me if you read it otherwise. PPM: placement. It's #2270's own fix, so I'd treat it as in-sprint.

**Timing:** this is a substantial build (handler, rail entry, the curated floor, the armed ask's words, pins for both turns through `process_intent`). I'll start it on your ruling. Tonight's promotion of `198fbdd89d` (#2325, N1) goes ahead independently.

**Verified how:** I read `_handle_analysis_intent`, `_ANALYSIS_QUERY_COHORT`, `_resolve_analysis_repository`, the `gather_context` ANALYSIS branch and the summarize call site. Grep finds `record_read` in two callers only. Layer: source. No `process_intent` reproduction yet; it comes with the build.

— Lead
