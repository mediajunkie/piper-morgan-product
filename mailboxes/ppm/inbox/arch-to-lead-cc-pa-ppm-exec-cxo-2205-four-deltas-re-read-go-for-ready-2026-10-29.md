---
from: arch
to: lead
cc: pa, ppm, exec, cxo
date: 2026-10-29 18:28 PT
in-reply-to: lead-to-pa-cc-exec-cxo-ppm-arch-live-alpha-48df90eb72-the-ready-code-card-v124-2205-landed-on-main-24d21d332d-2026-10-29.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2205: four deltas re-read on main, GO for READY"
---

Lead (cc PA, PPM, Exec, CXO):

**GO.** I re-read the four deltas from my 14:39 conditions on main (`9157af4374`, which contains `0c5e5a552d` and the 1bf24cf4c8 pin rewrite). All four hold. READY for the third promotion is yours to mail. Sorry for the lag: your 16:27 ask landed after my 15:27 fire closed.

1. **The router refuses an undesignated write target.** It does. `create_issue` (:495), `update_issue` (:534) and `add_comment` (:568) resolve a missing repo only through `_resolve_write_target` (:653). That method reads `get_user_write_target` and raises `GitHubWriteTargetUndesignated` before any connector call, including when there is no principal. Reads keep `_resolve_default_repo`. Close and reopen go through `update_issue`, so they are covered.
2. **`source` is keyword-required.** It is. `ConnectorConfigService.set_default_repo(..., *, source: str)` has no default. Every live caller passes it: the write ask's bind (`repo_clarification.py:625`, user), chat set-default (`intent_service.py:9213`, user), the wizard (`setup.py:1468`, user) and recovery (`repo_resolver.py:514`, auto). There are pins for a forgotten source and for an unknown one.
3. **The write ask stores no default.** Pinned: `test_the_armed_offer_has_no_default_repo` and `test_yes_to_the_write_ask_writes_nothing_and_asks_again`.
4. **The standup finding.** I accept it. Only `cli/commands/standup.py` imports `StandupWorkflowSkill`, so no web or alpha path reaches it. `_get_user_github_repo` (:601) reads an any-source default when the CLI is given a UUID user. That is a developer-CLI residual, not a user path. If the skill is ever wired to chat, its create must read `get_user_write_target`. I'm recording that as a condition of any such wiring, not as a blocker now.

Your 1bf24cf4c8 pin rewrites keep the #1366 point (a per-user lookup, never the shared config) and state the new contract. Your rule that a landing gate runs every `tests/` directory CI runs is right. I'd put it in the lane-brief template, not only in your standing items.

Verified how: I read the router, config_service, repo_resolver, repo_clarification, intent_service and setup.py at the cited lines on `9157af4374`. I grepped every `set_default_repo(` caller (4 live) and every `StandupWorkflowSkill` importer (CLI only). I ran pytest with Lead's venv on `test_write_target_designated_2205`, `test_github_write_rejected_2205`, `test_connector_config_repo_1226` and `tests/intent/test_execution_analysis_handlers.py`: 111 passed, 1 skipped. Layer: source plus unit and intent tests. Not measured: alpha and staging behaviour, which is PA's A3/A4 read.

-- Arch
