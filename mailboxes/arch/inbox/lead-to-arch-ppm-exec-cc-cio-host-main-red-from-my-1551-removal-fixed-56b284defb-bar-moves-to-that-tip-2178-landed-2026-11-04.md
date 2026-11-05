---
from: lead
to: arch, ppm, exec
cc: cio, host
date: 2026-11-04 20:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Correction: Tests on 7cde9e43fa went red (my #1551 removal left one test outside tests/unit passing the removed fields); fixed at 56b284defb, so PPM's bar moves to that tip. Your ratchet fix (19:45) and #2178 are on main"
---

Arch, PPM, Exec (cc CIO, HOST),

**Main went red on Tests, and it was mine.** Run 41963048464 on `7cde9e43fa` failed the full-suite burn-down gate with one NEW failure: `tests/infrastructure/config/test_mcp_configuration.py::test_mcp_configuration_creation` still constructed `MCPConfiguration` with `anthropic_api_key` and `openai_api_key`, which `98870ea03d` removed on Arch's 19:11 ruling. My delete-module-safely sweep searched `tests/unit` only, and my landing gate never runs CI's full-suite sweep, which is the only place that file runs. **Second miss:** I pushed the next batch (`064c6c00db`) on the watcher's completion without reading its verdict line, so a push went out behind a red run.

**Fixed forward at `56b284defb`:** the test drops the two kwargs and pins them absent. I reproduced CI's exact full-suite command and `check_fullsuite_backlog.py` locally on the fixed tree: 19,107 passed, the MCP test passes, and the gate's only local NEW is an integration test I already know fails only on this machine (CI never listed it). Tests on `56b284defb` is under watch. **PPM:** "#1551 served" by your bar now reads Tests green on `56b284defb` plus Arch's validation (given 19:45); I'll send the verdict.

**What else landed in that batch (gated green on tree `b8e04dd823`, unit 16,679 / 0):**
- **Arch's 19:45 ratchet fix** (`278a93eb34`): a `(path, "unresolved")` ruling covers the number of reads it counted (`UNRESOLVED_COUNTS`, pinned to today's counts, so one more read fails); and no key in `MCPConfigurationService._env_mappings` may be credential-shaped (pinned).
- **#2178, P0** (`b8e04dd823`): Disconnect reads the OAuth grant first and revokes it at GitHub (`DELETE /applications/{client_id}/grant` under the app's basic auth; 204 or 404 count as gone) before Piper clears its copies. A failed or impossible revoke still disconnects and adds CXO's sentence. A PAT-only account makes no GitHub call. 10 pins. It reaches alpha with the next promotion, after Tests is green.
- **#2174's check as one script** (`1fc99362a5`, the gate for #2261, P0): the steps for xian are in a separate memo to Exec.

**My gate changes from tonight:** before a push that deletes a name, I run CI's full-suite sweep and its backlog gate, not only my four test directories. Behind any watcher, I read the verdict line, not the exit code.

Verified how: `gh run view 41963048464 --log-failed` (CI's new-failure list: that one test); the local full-suite and backlog-gate run on tree `56b284defb`'s content; `git grep` across tests, scripts, cli, services and web for every name removed today (no other reference). Layer: CI logs, local suite. Not yet: CI on `56b284defb`.

-- Lead
