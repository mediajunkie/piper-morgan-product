## Proposed diff (unified; hunk per finding)
`CLAUDE.md` hunks are verbatim. For skill files I give the line to replace and its replacement, since I read them via reviewers.

```diff
--- CLAUDE.md
@@ line 33 @@
-**Session logs**: `dev/active/YYYY-MM-DD-HHMM-[role-slug]-log.md`
+**Session logs**: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-[role-slug]-code-log.md`
@@ line 77 @@
-ls mailboxes/lead/inbox/
+ls mailboxes/{role}/inbox/
@@ line 161 @@
-(Keychain first, then env var — see `services/config/llm_config_service.py:213`)
+(Keychain first, then env var — see `LLMConfigService.get_api_key` in `services/config/llm_config_service.py`)
@@ line 302-305 @@
-- Call out bad ideas and mistakes - PM depends on this
-- Never "You're absolutely right!" - be honest
-- STOP and ask for clarification rather than assuming
+- Give an honest assessment. Call out bad ideas and mistakes; PM depends on it.
+- STOP and ask for clarification rather than assuming
@@ line 652 @@
-that's the whole point of Model-B + push-to-ref.
+that's the whole point of per-agent worktrees + push-to-ref.
@@ line 742 @@
-See §"Worktree model" near the top of this file for the operative rules and the two Amber gotchas (silent stale-branch provisioning; project hooks possibly not firing).
+See §"Worktree model" near the top of this file for the operative rules and the two Amber gotchas (silent stale-branch provisioning; hooks that were dead from an invalid matcher, now fixed, and advisory only).
@@ line 744 @@
-- Setup + branch-collision context: `docs/internal/operations/git-worktrees-model-a-setup.md`
+- Setup + branch-collision context: `docs/internal/operations/git-worktrees-model-a-setup.md` (its header says "deprecated"; the commands remain valid for Model A)
@@ lines 128, 273, 495, 527 (marker removal, reasons already adjacent) @@
-### BRIEFING-CURRENT-STATE staleness response (MANDATORY when triggered)
+### BRIEFING-CURRENT-STATE staleness response (when triggered)
-### Session Log Maintenance (NON-NEGOTIABLE)
+### Session Log Maintenance
-## Sign-Off Discipline (CRITICAL — read before ending any session)
+## Sign-Off Discipline (read before ending any session)
```

Skill hunks (replace the quoted text at each line):
- `create-session-log:99-100`, `cut-release:173`, `publish-to-blog:517,563`: `git push origin main` → `git push origin HEAD:main`.
- `duty-cycle-tick:34,368`: `…{role}-code-opus-log.md` → `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{role}-code-log.md`.
- `duty-cycle-tick:217`: glob across roles → `git checkout -- mailboxes/{role}/inbox/MANIFEST.md mailboxes/{role}/read/MANIFEST.md`.
- `check-mailbox` after line 52 and 113 (add): "Send the reply and the inbox move with `scripts/mail-send.sh "mail({role}): {subject}" <every changed path>`; don't `git add` or commit mailbox files."
- `check-mailbox:146-147`: replace the `mailboxes/README.md` lines with `mailboxes/DIRECTORY.md`.
- `create-omnibus:268-285`: remove the archive step; add frontmatter `name`/`description` at line 1.
- `cut-release:1` and `narrative-verification:1`: add frontmatter with a one-sentence trigger description.
- `continue-narrative:70`: "cycle log / standing-items" → "your session log (and the standing-items tracker if one exists)".
- `draft-blog-post:159,243,293`: "teases the very next scheduled item…" → "teases the next scheduled non-Ship post; Ships carry no tease."
- `draft-blog-post:207,277,294`: metrics "kept rich in tables" → "bullet list, never a table."
- `draft-weekly-ship:197`: "sentence case for theme" → "title case (template-audit check 2)".
- `update-calendar:261`: "Always set blogURL + blogPath + canonicalSite" → "Always set blogURL + blogPath (leave canonicalSite empty until syndication runs)". `:80`: add `not-syndicated` to the status values.
- `audit-cascade:63`: `.github/ISSUE_TEMPLATE/` → `.github/issue_template/`. `cleanup-dev-active:133`: remove the line. `doc-sync-sweep:135`: remove the line.
- `template-audit:333-355`: add `16. Typographic residue ✓ PASS`.
- `SKILLS.md`: add the 11 missing rows, drop "planned" for `create-omnibus`, update the `duty-cycle-tick` row and the two reference paths.
- `ab-a-isolation:26-34`: stash recipe → `git stash push -u -m aba-<tag>`; capture SHA; restore with `git stash apply <sha>`; never in the shared main checkout.
- `update-current-state:91`: → "Add new entries at the top; don't delete others' entries unless PM or Docs trims them."
- `brief-coding-agent` (add): "State the model tier: set `model` explicitly and note it in your session log beside the dispatch."
- Nested `dev/2025/09/21/CLAUDE.md` and `AGENTS.md`: delete both, or replace with one line: "Archive directory; follow the root CLAUDE.md."

**Verified how:** I did the `CLAUDE.md` checks myself, with reads of the repo paths, greps of the named symbols, `git blame` on the contested lines, and a read of `get_api_key`. I re-ran the reviewers' High findings the same way: blame, path reads, quotes. Denominator: 41 of 41 in-project instruction files, with a spot-check of the reviewers' High findings only, not every Medium or Low one. I did not run the behavioral before-and-after probes (Step 7), so none of the removals is tested. Every file under `~/.claude`, the ancestor directories and any managed policy was unreadable here, so those are unaudited.