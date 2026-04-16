# Linter & Pre-Commit Modernization Recommendation

**Author**: code-opus (research agent)
**Date**: 2026-04-16
**Context**: Issue #981 — linter reverted intentional import removals during #971
**Scope**: Research and recommendation only. No code changes made.

---

## Executive Summary

The Python formatting stack is a conventional **black + isort + flake8** trio, plus a large set of **custom project-governance hooks** that do useful work. The thing most likely reverting imports in #981 is **NOT a Python linter** — none of `autoflake`, `ruff`, or `pyupgrade` are configured anywhere in the repo. The most plausible culprit is the **Cursor/VSCode editor running `isort` on save** (the `.vscode/settings.json` has `editor.formatOnSave: true` plus `python.formatting.provider: black`), combined with a Python LSP that re-suggests imports. A secondary candidate is the agent itself re-inserting imports during long edit sessions. Recommended action is small-to-medium: **replace black + isort + flake8 with a single `ruff` hook, keep all the project-governance hooks, and adjust the IDE save behavior**. Mypy is not in the stack and does not need to be added.

---

## 1. Current Stack Inventory

### 1.1 Config sources

| File | Purpose | Status |
|------|---------|--------|
| `.pre-commit-config.yaml` | Pre-commit framework config (167 lines) | Active |
| `pyproject.toml` | Black + isort config (only; no ruff/mypy) | Active |
| `.flake8` | Flake8 config with most F/W rules disabled | Active |
| `.editorconfig` | Whitespace/newline rules | Active |
| `.vscode/settings.json` | `formatOnSave: true`, black as formatter, **pylint enabled** | Active |
| `requirements.txt` | Lists `black==23.12.0`, `pre_commit==4.2.0` (no ruff/autoflake/pyupgrade) | Active |
| `.github/workflows/lint.yml` | CI lint job: black, isort, flake8 | Active |
| `scripts/fix-newlines.sh` | Manual helper to avoid `end-of-file-fixer` failures | Active |
| `setup.cfg`, `mypy.ini`, `ruff.toml`, `.pylintrc` | **Do not exist** | N/A |
| `.git/hooks/*` | **All samples only** — real hooks managed by pre-commit framework | N/A |

### 1.2 Pre-commit hooks (grouped)

#### Python formatting/linting (3rd-party)

| Hook | What it does | Runs in CI? | Notes |
|------|--------------|-------------|-------|
| `isort` (PyCQA/isort 5.13.2) | Sort imports, `--profile black` | Yes (`--check-only`) | **Suspect #1 in #981** |
| `flake8` (pycqa/flake8 7.0.0) | Lint — but F401/F811/F821/F841/E501/etc. are **all disabled** | Yes (but only syntax-level E9/F63/F7/F82) | Nearly toothless |
| `black` (psf/black 24.3.0) | Format, line-length 100 | Yes (`--check`) | No functional issue |

#### Generic hygiene (pre-commit/pre-commit-hooks v4.5.0)

| Hook | What it does |
|------|--------------|
| `trailing-whitespace` | Strip trailing whitespace |
| `end-of-file-fixer` | Ensure final newline |
| `check-yaml` | YAML syntax |
| `check-added-large-files` | Block large binaries |

#### Project-governance (local hooks — custom)

| Hook | Purpose | Evidence used today? |
|------|---------|----------------------|
| `check-windows-filenames` | Block `:<>"|?*` in paths | Yes — still useful for Windows contributors |
| `check-hallucinated-urls` | Block `Codewarrior1988/piper-morgan` (CLAUDE.md mentions) | Yes — agent-specific guardrail |
| `smoke-tests` | Run <1s smoke suite before commit | Yes — catches import breaks |
| `documentation-check` | Runs `.git/hooks/pre-commit.legacy` | Unclear — legacy script |
| `backlog-roadmap-sync` | Reminder when backlog/roadmap docs change | Yes |
| `github-architecture-enforcement` | Runs `tests/test_architecture_enforcement.py` (pytest inside pre-commit) | Yes — but expensive |
| `direct-github-agent-check` | Grep for bypass imports | Redundant with above, but fast |
| `prevent-direct-adapter-imports` | Enforce Calendar/Notion/Slack router pattern | Yes — active contract |
| `validate-numbering` | Consecutive pattern/ADR numbering | Yes (rarely fires, low cost) |
| `check-tmp-work-files` | Prevent lost work in `/tmp` | Yes — agent safety net |
| `check-init-py` | Ensure `__init__.py` under `services/` | Yes — cross-platform stability |
| `check-manual-tests` | Detect misnamed pytest-unsafe scripts | Yes |
| `release-notes-check` (pre-push) | Force release notes on version bump | Yes (release-time only) |
| `api-versioning-check` | Enforce `/api/v1/` prefix | Yes — documented in CLAUDE.md |

#### CI workflows (parallel to pre-commit)

| Workflow | Enforces |
|----------|----------|
| `lint.yml` | black + isort + flake8 check |
| `ci.yml` | Config validation, basic test run |
| `test.yml` | Smoke, full tests, perf regression, coverage gate |
| `architecture-enforcement.yml` | GitHubIntegrationRouter pattern |
| `router-enforcement.yml`, `config-validation.yml`, `link-checker.yml`, etc. | Various governance checks |

### 1.3 IDE layer (the hidden one)

`.vscode/settings.json` sets:
- `editor.formatOnSave: true`
- `editor.defaultFormatter: esbenp.prettier-vscode` *(note: Prettier for default, not Python-aware)*
- `python.formatting.provider: black`
- `python.linting.pylintEnabled: true` *(pylint is NOT in requirements.txt — if enabled, it's user-installed)*

The IDE config implies that **Cursor / VSCode / Windsurf running on a developer machine could be re-applying formatters/linters on save**, independent of the pre-commit framework.

---

## 2. Root Cause of #981

### Mechanism identified: **most likely IDE-level isort-on-save, not pre-commit**

Evidence:

1. **Autoflake is not installed or configured anywhere.** Grepping `autoflake|expand-star|pyupgrade|ruff` across `pyproject.toml`, `.pre-commit-config.yaml`, `requirements.txt`, `.github/workflows/`, `scripts/` — **zero matches**. Autoflake is the #1 usual suspect for this kind of "linter added my imports back" behavior, and it is not present. Hypothesis (a) from the issue is eliminated.

2. **Ruff is not installed or configured anywhere.** Same grep result. `ruff --fix` with `F401` can only *remove* unused imports, not re-add removed ones, so even if present it wouldn't explain the symptom. Hypothesis (c) from the issue is eliminated.

3. **Isort has no `add_imports` directive** in `pyproject.toml`. Stock isort with `--profile black` does **sort and group imports but does not add new ones**. So pre-commit isort cannot re-add imports either.

4. **Flake8 has F401 (imported but unused) disabled** in `.flake8`. Even if flake8 were aggressive, it is not an autofixer — it reports, it does not rewrite. Not the culprit.

5. **Black does not touch import statements.** Not the culprit.

6. **`.vscode/settings.json` has `editor.formatOnSave: true`** combined with black as the Python formatter and **pylint enabled** for linting. VSCode + Cursor Python extensions commonly bundle `isort` organize-imports-on-save and also surface an LSP-level "missing symbol — import `LLMFactory` from `services.llm.adapters`" code action. If the editor has an auto-apply-quickfix-on-save setting (or if the Cursor/Copilot agent is running its own organize-imports), it would re-insert the deleted symbol based on LSP "undefined name" diagnostics. **This is the most plausible mechanism.**

7. **Alternative: agent-level re-insertion.** Long edit sessions where the editing agent re-reads the file, sees references to `LLMFactory` that haven't yet been scrubbed from the body, and "helpfully" restores the import to match. The session log says "had to be retried via subagent delegation" — consistent with an agent-loop problem more than a linter-loop problem, because pre-commit only runs at commit time, not during edit iterations.

### Conclusion

**Primary cause**: IDE format-on-save + Python LSP auto-import-fix, OR agent-loop re-insertion during iterative edits.
**Not caused by**: any configured pre-commit hook or CI linter. The existing Python formatting hooks (isort, flake8, black) **cannot** re-add removed imports with the current configuration.

### What this means for the modernization question

The title of #981 frames this as "linter aggression", but the linter stack is essentially innocent here. The modernization recommendation should therefore focus on:
- **Simplifying the stack** (black + isort + flake8 → ruff) for maintenance reasons, not to fix #981
- **Tightening or documenting IDE save behavior** as the actual remediation for #981
- **Agent workflow guidance** (batch deletion edits before save-triggered reformats)

---

## 3. Keep / Relax / Remove

### 3.1 Python formatting/linting

| Item | Current | Recommendation | Rationale |
|------|---------|----------------|-----------|
| `black` | Active, v24.3.0 | **Replace with ruff format** | ruff format is drop-in black-compatible, ~30x faster, removes one tool |
| `isort` | Active, `--profile black` | **Replace with ruff's `I` rules** | Same behavior, consolidated, can be selectively disabled via `# noqa: I` |
| `flake8` | Active but **almost all rules disabled** (F401, F811, F821, F841, E501, E402, E712, W291, W293 all ignored) | **Replace with ruff (minimal ruleset)** | Current flake8 catches ~nothing beyond syntax. Ruff `E9,F63,F7,F82` matches what CI actually runs. |
| `mypy` | Not installed | **Do not add** | Project is 6000+ tests and shipping. Adding types now is a large retrofit for unclear benefit. |
| `pylint` | Enabled in `.vscode/settings.json` but not in requirements | **Disable in VSCode settings** | Ghost dependency. Either not installed (silent no-op) or installed inconsistently across contributors. |

### 3.2 Pre-commit generic hygiene

| Hook | Recommendation | Rationale |
|------|----------------|-----------|
| `trailing-whitespace` | **Keep** | Cheap, prevents churn |
| `end-of-file-fixer` | **Keep** | `fix-newlines.sh` exists specifically to pre-empt its failures, which is a smell — but the hook itself is fine |
| `check-yaml` | **Keep** | Cheap |
| `check-added-large-files` | **Keep** | Good for preventing accidental DB/binary commits |

### 3.3 Project-governance hooks (local)

**Keep all except review two candidates**:

| Hook | Recommendation | Rationale |
|------|----------------|-----------|
| `documentation-check` (calls `.git/hooks/pre-commit.legacy`) | **Investigate** — what does the legacy script do? Not visible. Consider removing or documenting. | Unknown behavior should be explained or cut |
| `smoke-tests` (<1s claim) | **Keep but verify timing** | If it's actually <1s this is great; if it's drifted to 10s+, it's friction every commit |
| `github-architecture-enforcement` (runs pytest at commit time) | **Keep** — but this overlaps with `direct-github-agent-check` (pure grep). The grep version is 100x faster; the pytest version is the authoritative check. Consider gating pytest to pre-push instead of pre-commit. | Reduces per-commit latency without losing coverage (CI still runs the pytest version via `architecture-enforcement.yml`) |
| `direct-github-agent-check` | **Keep** | Fast grep guard |
| `prevent-direct-adapter-imports` | **Keep** | Active architectural contract |
| `check-windows-filenames`, `check-hallucinated-urls`, `validate-numbering`, `check-tmp-work-files`, `check-init-py`, `check-manual-tests`, `backlog-roadmap-sync`, `release-notes-check`, `api-versioning-check` | **Keep all** | Each targets a specific failure mode the project has hit. Low cost, high specificity. |

### 3.4 IDE / editor config

| Item | Recommendation |
|------|----------------|
| `editor.formatOnSave: true` | **Keep, but document** that Python edits during large refactors should batch save to reduce auto-fix reapplication churn |
| `python.linting.pylintEnabled: true` (pylint not in requirements) | **Set to `false`** — ghost dependency |
| `editor.defaultFormatter: esbenp.prettier-vscode` | Leave (not Python-relevant, applies to JS/MD/YAML) |
| Add: `"editor.codeActionsOnSave": { "source.organizeImports": "never" }` for Python | **Recommend** — prevents the specific class of thrash that caused #981 |

### 3.5 Scripts

| Item | Recommendation |
|------|----------------|
| `scripts/fix-newlines.sh` | **Keep** — but note that its existence signals `end-of-file-fixer` is tripping on files created by scripts/agents that don't respect the editor config. Root-cause fix would be ensuring all file-writing agents terminate with `\n`. Low priority. |

---

## 4. Proposed Modernized Stack

### Python formatting/linting

**Before** (3 tools, 3 configs):
```
black (pyproject.toml [tool.black])
isort (pyproject.toml [tool.isort])
flake8 (.flake8)
```

**After** (1 tool, 1 config):
```
ruff (pyproject.toml [tool.ruff])
  - format  → replaces black
  - rules E9,F63,F7,F82,I  → replaces flake8 (what's actually enforced) + isort
```

Rough config outline (NOT being applied — illustration only):

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
extend-exclude = ["archive", "venv", "data_backup", "uploads", "web/assets"]

[tool.ruff.lint]
select = ["E9", "F63", "F7", "F82", "I"]  # Parity with CI flake8 + isort
ignore = ["F401", "F811", "F821", "F841", "E501", "E402", "E712", "W291", "W293"]

[tool.ruff.lint.isort]
profile = "black"  # Preserve existing import grouping
```

### Pre-commit config diff (conceptual)

**Remove**:
- `isort` hook (PyCQA/isort)
- `flake8` hook (pycqa/flake8)
- `black` hook (psf/black)

**Add**:
- `ruff-pre-commit` with `ruff` (lint) and `ruff-format` (format) hooks

**Keep**: all 16 project-governance hooks, all 4 pre-commit/pre-commit-hooks hygiene hooks.

### CI workflow diff

`.github/workflows/lint.yml`: replace three `pip install black flake8 isort` + three check steps with a single `pip install ruff` + `ruff check --select=E9,F63,F7,F82,I .` + `ruff format --check .`.

### IDE settings diff

`.vscode/settings.json`:
- `python.linting.pylintEnabled: false`
- Add `"[python]": { "editor.codeActionsOnSave": { "source.organizeImports": "never" } }`
- Optionally switch `python.formatting.provider` from `black` to `none` and install the ruff VSCode extension

---

## 5. Migration Risk

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| **Ruff format output differs subtly from black** | Low. Ruff format targets black parity. | Run `ruff format .` once on a branch; if diff is >100 lines, file an issue and investigate. Commit reformat as single "style" commit. |
| **Ruff isort output differs from isort** | Low with `profile = "black"`. | Same — one-shot reformat commit, diff review. |
| **Developer toolchains out of sync** | Medium — contributors may have black/isort/flake8 pinned in IDE | Update `.vscode/settings.json` + post a migration note in `dev/active/`. Ruff has stable VSCode / Cursor extensions. |
| **CI cache invalidation** | Low | `.github/workflows/lint.yml` cache key is keyed on `requirements.txt`; bumping to ruff flushes old cache naturally. |
| **Flake8 was catching something ruff doesn't** | Very low — current flake8 ignores almost every rule. Only E9/F63/F7/F82 are enforced in CI, all of which ruff supports. | Keep the identical rule selection. |
| **Agent / developer muscle memory** | Medium — CLAUDE.md and briefing docs may reference `black` by name | Search briefing docs for "black", "isort", "flake8"; update to reference `ruff` or generic "formatter". Not blocking — existing references still work for historical commits. |
| **Pylint ghost-installation surfaces errors** | Low | Disabling in `.vscode/settings.json` is a no-op for anyone not running pylint, and a quiet-down for anyone who is. |
| **`fix-newlines.sh` no longer needed** | N/A — leave in place, document as optional helper | Don't delete working infrastructure without PM sign-off |

### What will NOT break
- Any test behavior (zero tests touch linter output)
- The 16 custom pre-commit hooks (untouched)
- The 14+ CI workflows beyond `lint.yml` (untouched)
- Release process (untouched)
- Any `# noqa` comments in source — ruff understands them

### What needs PM explicit buy-in
- **One-shot reformat commit** to apply ruff format. Even with profile parity, a few whitespace/blank-line edges may churn. Should land as a single "style: adopt ruff" commit, pinned to a known-clean main, so `git blame` impact is isolated and reviewable.

---

## 6. Effort Estimate

**Small-to-medium.**

| Task | Size |
|------|------|
| Install ruff, write `[tool.ruff]` config | Small (~15 min) |
| Run `ruff format .` + `ruff check --fix`, review diff | Small-medium (~30-60 min — depends on churn) |
| Update `.pre-commit-config.yaml` | Small (~10 min) |
| Update `.github/workflows/lint.yml` | Small (~10 min) |
| Remove `.flake8`, `[tool.black]`, `[tool.isort]` from pyproject.toml | Small (~5 min) |
| Update `.vscode/settings.json` (disable pylint, organizeImports=never) | Small (~5 min) |
| Smoke-test locally: edit a file, save, commit, push — verify no thrash | Small (~15 min) |
| Optional: document ruff in CLAUDE.md / briefing | Small (~15 min) |

**Total**: half-day of Lead Dev time, depending on whether the reformat diff surfaces surprises. Two commits total: (a) "style: adopt ruff — one-shot reformat" and (b) "chore: replace black+isort+flake8 with ruff".

### Not included in this estimate
- **Adding mypy** — not recommended at this time.
- **Fixing #981's actual cause** — that's an IDE settings change + possibly an agent-workflow doc note. Treat as separate ticket; ruff migration does not address it. If the IDE settings diff above is applied at the same time, it costs ~5 minutes extra.

---

## 7. Recommendation Summary

1. **Keep the 16 custom project-governance hooks as-is.** They're doing real work the project has committed to.
2. **Replace black + isort + flake8 with a single ruff hook.** Same behavior, one tool to manage, faster.
3. **Do not add mypy.** Cost/benefit isn't there for a shipping codebase this size without existing type annotations.
4. **For #981 specifically:** disable pylint in `.vscode/settings.json` (ghost dep), and add `"source.organizeImports": "never"` for Python in codeActionsOnSave. This addresses the root cause (IDE auto-import-reapply), which the Python linter stack was falsely accused of.
5. **Treat #981's "linter softening" as a separate, smaller ticket** focused on IDE + agent workflow, not on removing pre-commit rules.

---

## 8. Things I Could Not Explain

- **`.git/hooks/pre-commit.legacy`** — referenced by the `documentation-check` hook but I didn't read its contents. Worth PM or Lead Dev confirming what it does before any cleanup.
- **Why `.vscode/settings.json` enables pylint when pylint is not in `requirements.txt`** — likely historical drift; worth confirming no dev relies on it.
- **Whether any contributor has a private `.vscode/settings.json` with `source.organizeImports: "explicit"` or `"always"`** — that would be the smoking-gun for #981. I cannot see private user-scope VSCode settings.

---

## Appendix: Files Read

- `/Users/xian/Development/piper-morgan/piper-morgan-product/.pre-commit-config.yaml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/pyproject.toml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.flake8`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.editorconfig`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.vscode/settings.json`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.github/workflows/lint.yml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.github/workflows/ci.yml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.github/workflows/test.yml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/.github/workflows/architecture-enforcement.yml`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/requirements.txt`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/scripts/fix-newlines.sh`
- `/Users/xian/Development/piper-morgan/piper-morgan-product/services/domain/llm_domain_service.py` (head)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/dev/active/2026-04-15-0635-lead-code-opus-log.md`
- Commit `620106a8` diff for `services/domain/llm_domain_service.py`
- GitHub issue #981 (via `gh issue view 981`)

## Appendix: Files Confirmed Absent

- `setup.cfg`, `mypy.ini`, `ruff.toml`, `.pylintrc`
- No non-sample entries in `.git/hooks/`
- No `autoflake`, `ruff`, or `pyupgrade` references in any config, requirements, CI workflow, or script
