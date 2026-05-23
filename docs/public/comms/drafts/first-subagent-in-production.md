---
image:
alt:
caption:
---

# First Subagent in Production

*May 6–7, 2026*

The audit cascade is a procedural check Lead Dev had been running for weeks before any implementation gameplan. Walk the issue. Walk the gameplan. Walk the prompts. Resolve every ⚠️ before any code gets written. By mid-May the discipline had operated at the gameplan-prep stage many times. It had operated at the closure stage many times. It had never operated at a *subagent-deployment* stage, because Lead Dev hadn't yet deployed a subagent into production work.

Wednesday evening, May 6, the prep landed.

The issue was test migration — a queue of stale unit tests left behind after the standup-conversation persistence work I described in another piece had landed. The tests didn't need new logic. They needed mechanical rewrites against the new persistence layer. Single-purpose work, no architectural calls, well-scoped — exactly the shape that justifies a subagent. Lead Dev built the audit cascade for the deployment in three passes.

The Issue audit ran twenty-four checks. One ⚠️ for a Developer Experience question I needed to dispose of, which I did. The Gameplan audit ran twenty-seven checks. Four "N/A" calls — the gameplan was scoped tight enough that several check categories didn't apply. I approved each. The Prompts audit ran thirty-six checks against the subagent brief itself. Six "N/A" calls.

That last set caught my attention. I'd run the audit cascade enough times by then to have a sense for the N/A rate. Six of thirty-six is high. Lead Dev surfaced it: the Cursor-derived audit template we'd been using had categories that didn't generalize cleanly to a subagent-deployment context. The template was drifting from its use cases. Lead Dev filed a template-hygiene tracking issue for later. A new memory entry got pinned: *when an audit produces five-plus N/A flags in one pass, treat the count as a signal that the template needs review, not as five-plus separate "doesn't apply" judgment calls.*

By bedtime the prep package was complete. Gameplan, three audit documents, the subagent prompt itself. Ready to deploy.

# The thirty-minute run

Thursday morning at 6:48 AM Lead Dev launched the subagent.

It ran in the background. Phase 1, Phase 2, Phase 3, Phase 4 — each phase a chunk of tests to migrate. Lead Dev got on with other work in the foreground while the subagent worked. At about 7:18 AM the subagent finished. Lead Dev ran the post-execution audit — sixteen checks against the actual work the subagent had done. All sixteen passed. Merge, close, sign-off. Fifty minutes deployment to merge.

Two things from inside that fifty minutes are worth slowing down for.

The first is how the subagent handled an unexpected finding. Phase 2 of the gameplan said *migrate the twelve tests in this file*. When the subagent got to the file, the tests didn't need migration — they were already passing under the new persistence layer. The plan had been wrong about the work, not about the goal. The subagent's response was to annotate the gameplan with what it had found, mark Phase 2 complete without modifying the file, and proceed to Phase 3. It did not improvise. It did not "fix" the gameplan by going beyond its scope. It surfaced the discrepancy and continued.

That's the audit-cascade discipline operating at the execution layer — not at the prep layer where Lead Dev had run it the evening before, and not at the closure layer where Lead Dev would run it half an hour later. The same discipline, the same posture, applied by a different actor inside the same procedure. The subagent had absorbed the *"reframe rather than improvise"* shape that the methodology had been holding all along.

# The collision

The second thing is less elegant.

Around seven o'clock — partway through the subagent's run — Lead Dev needed to update the session log with a note. The discipline by then was a chained shell command: `git branch --show-current && git add … && git commit … && git push origin main`. The branch-verification step prints the current branch first. If it's `main`, the chain proceeds and the commit lands on main. If it's not, you see the wrong branch, you stop, you fix it.

The subagent's checkout of its working branch had silently flipped HEAD on Lead Dev's session — the two were sharing one `.git` directory. The branch-verification step ran. The chain proceeded. The commit landed on the *subagent's feature branch*, not on main.

The discipline had named the right check. The discipline was even running the check. The discipline was *printing* the right answer — *wrong branch* — to the terminal. But the chained `&&` only gated on the verification command's exit code, not on what the verification printed. Exit code zero means the command ran successfully. It does not mean the answer was the one you wanted.

The recovery was small. The commit could come across cleanly at the eventual `--no-ff` merge of the subagent's branch. Two new lessons got pinned. The first: verifying isn't enough — *gate on the result, not just on the exit code*. Either run the verify as a separate command and read the output before continuing, or use a bash form that actually tests the result (`[ "$(git branch --show-current)" = "main" ] && commit`). The second: subagent deployment in a shared `.git` is fundamentally fragile. The mitigation is either to deploy the subagent in its own `git worktree` (so the `.git` doesn't move under the parent agent), or to commit everything you have foreground before deploying and treat the post-deploy window as feature-branch territory.

Both lessons were small. Both were exactly the right size — narrow enough to actually follow next time.

# What this opened

The fifty-minute deployment was satisfying in itself. A real piece of test-migration work moved through a real subagent in a real morning sprint. The audit-cascade methodology operated at every layer it was supposed to. The subagent absorbed the discipline. The closure was clean.

The collision was the more interesting payoff. Until that morning the audit cascade had been a methodology that the parent agent ran. After that morning it was clear the methodology had a *fourth* layer the prep hadn't named — the scaffolding around the deployment. Tool composition, branch identity, working-tree isolation, the difference between an exit code and a result. The discipline had been built for the work. The work surfaced where the discipline still needed to grow.

# What's portable

Most of what counts as discipline at one layer of a system turns out to need its own discipline at the layer below. Auditing the work generates audits that the audit procedure itself needs. Deploying a tool gets you the tool's behavior plus the tool's interaction with the environment it's deployed into. The first deployment of any production-scale tool is the moment the methodology meets the operating environment, and what surfaces is reliably some piece of the methodology that nobody had thought to write down.

Build the discipline anyway. Deploy the tool anyway. The discipline that arrives in the small lessons from that first deployment is usually more durable than the discipline that arrived in the prep work.

---

*Next on Building Piper Morgan: [TEASE PENDING — confirm next-scheduled-item at calendar update].*

*Where in your work has a tool's first production deployment surfaced a piece of discipline you'd been carrying tacitly? What got written down?*

[FACT-CHECK NOTE for PM: Sources verified against May 6 + May 7 omnibus logs. Key facts: May 6 — Lead Dev preps #1053 STANDUP-TEST-MIGRATION with three audit-cascade gates (Issue 24✅+1⚠️ via Developer Experience reinterpretation; Gameplan 27✅+4 PM-approved N/A; Prompts 36✅+6 PM-approved N/A); 5 prep artifacts shipped at `dev/2026/05/06/` (1053-gameplan.md / 1053-gameplan-audit.md / 1053-issue-audit.md / 1053-prompts.md / 1053-prompts-audit.md); #1058 filed for Cursor template hygiene per PM observation; memory `feedback_audit_cascade_n_a_count_signals_template_drift.md` pinned. May 7 — subagent deployed 6:48 AM (agent ID a67932cd58e460562), completed ~7:18 AM, post-execution audit 16/16 ✅, merged + closed `69aa5e74` by 7:30 AM. Subagent committed 4 phases on `claude/1053-standup-test-migration`. Phase 2 reframe (12 tests already passing in `test_standup_routing_585.py`; subagent annotated rather than improvising). Cross-agent git collision ~7:00 AM: subagent's `git checkout` flipped HEAD on Lead Dev's session; chained `&&` verification printed wrong branch but commit proceeded; log-update commit `fc7f685e` landed on feature branch, came across cleanly at `--no-ff` merge. Memory `feedback_branch_show_current_before_every_commit.md` refined with two new lessons (gate-on-result-not-just-exit-code + subagent-deployments-require-real-worktree-or-foreground-commits-first).]

[SOURCE NEEDED for PM: "the standup-conversation persistence work I described in another piece" — I'm referencing Beat 5 (The Pace Verified, May 2–5) which mentions the conversation-state object Phase 2 + #1052 work. The connection is real but the cross-reference reads as a forward call to Beat 5 in the publication order. If Beats are publishing in chronological order (Beat 5 → Beat 6 = May 2–5 narrative → May 6–7 narrative), the cross-reference works. Flag if you'd rather frame as "a piece of persistence work I described earlier" without the explicit cross-reference.]
