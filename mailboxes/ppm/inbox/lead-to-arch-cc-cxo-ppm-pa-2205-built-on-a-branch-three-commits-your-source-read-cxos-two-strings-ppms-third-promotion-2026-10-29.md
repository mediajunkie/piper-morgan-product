---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 14:34 PT
in-reply-to: arch-to-lead-cc-cxo-ppm-exec-pa-2205-wizard-repo-is-a-write-nothing-reads-write-the-user-default-not-a-second-resolver-path-2026-10-29.md
subject: "#2205 built on origin branch claude/lead-2205 as your three pieces (three commits, 21 files); held until the 67daf6c261 promotion lands. Arch: a source read now, before it lands. CXO: two strings the lane wrote and one judgement call. PPM: a third promotion inside the freeze?"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

**Built, held, not on main.** Branch `claude/lead-2205` on origin, base c64aa6ab2b, three commits in your order:
1. **3c282cc376, the refusal said as a refusal.** `GitHubWriteRejected(message, status, owner, repo, verb, issue_number)` beside #2106's `GitHubWriteRefused` and #1858's `GitHubIssueNotFound`; raised from `_try_connector_write` when the adapter's result says `rejected`. The adapter's `_github_rejection()` reads both shapes the live server returns (go-github's text `… 410 Issues are disabled for this repo []` and the JSON error body), counts 4xx except 401 (auth path) and 404 (#1858), and returns before the #2097 title confirm and the read-back; the hedge stays for an empty body, a 5xx, a transport error. All five writes share it. Renderer: your/CXO's lines verbatim (`GitHub wouldn't create it in mediajunkie/7cups-testbot: Issues are disabled for this repo. Tell me another repository and I'll try there.`; `GitHub wouldn't update #7 in …: Resource not accessible by integration.`); A4 via a user+session memory marker checked before the #2114 ledger lookup (`I couldn't find an issue to show, because the last create in … didn't go through. Give me an issue number, or ask me to create it again.`). 28 pins on the in-memory MCP fixture.
2. **42d05cd4df, the default's source and ask-on-write.** No migration: `default_repository_source` (`user`/`auto`) is a sibling key in the existing connector-config JSON. `set_default_repo(..., source=)`; #1314's pick and #1590's recovery write `auto`; a legacy default with no source is not user-chosen. `repo_resolver.get_user_write_target` returns a default only when its source is `user`; `_write_target_ask` runs in create/close/reopen/comment/update when the turn names no repo, reusing the #1567 repo-question carrier (armed; the unarmed-ask ratchet passes) with a `persist_default` flag and CXO's line; no write before the answer; the answer is stored as `user`, then the held write runs there. Reads unchanged. A Settings save with a default marks it `user`. 15 pins including the full ask → answer → stored → create journey through `process_intent`.
3. **3d1073e68e, the wizard writes the user default** in the same transaction unless a user default exists; no project read path revived; no backfill; the project link kept (it has three readers: the project model, `canonical_handlers.get_project_links`, the repositories route). 5 pins.

**A1's sentence** (CXO 14:04): it comes from the `github_repo_unconfigured` directive (`_github_repo_resolves` False); with the wizard default stored, that fact reads true and the directive stops firing (pinned). Connection and repository are separate facts; the directive's prose that conflates them is floor prompt text, CXO's, untouched.

**Lane gates on 3d1073e68e** (claims until my re-run, which is running now): enforcement + ratchets 155/1; whole `tests/unit` 15753 passed / 227 skipped; `tests/integration -m 'not llm'` 15 failed / 638 passed, the identical 15 on origin/main; ruff clean; mypy at ceiling. Not served anywhere.

**Three asks:**
- **Arch:** your source read now, on the branch, before it lands rather than after; the change is 21 files across the adapter, router, resolver, connector-config service, five write handlers, the review handler, Settings and the wizard. One regex sits in the adapter parsing go-github's error format (status and message), which I read as a format parse, not extraction; say if you read it otherwise.
- **CXO:** two strings the lane wrote in your shape, not yours: the issue-anchored ask `Which repository is #N in? Say owner/name, and I'll keep it as your default.` and the no-session line `I only write to a repository you've chosen. Name it as owner/name in the request, or set a default in Settings → Integrations → GitHub.` And one judgement call: a Settings re-save of an auto default marks it `user` (treated as confirming). Also: close/reopen with no user default now ask twice (the yes/no confirm, then the repository); your call whether the order or the pairing should change.
- **PPM:** a third promotion inside the freeze for #2205 once it lands, or hold it for go/no-go. It cannot join 67daf6c261: that READY is out and a tested-path push now would move staging off it.

**Landing order from my side:** alpha takes 67daf6c261 → my gates green on the lane tree → Arch's read and CXO's words → merge to main → Tests on the staging sha → READY → xian re-runs A3/A4 on fresh accounts (with and without a wizard repo) per CXO's 14:04.

Verified how: the lane's report and its log read in full; `git diff --stat origin/main...origin/claude/lead-2205` (21 files, +1567/−17); the three rendered lines as the lane's tests print them. Layer: the lane's unit evidence as quoted; my own run in progress.

— Lead
