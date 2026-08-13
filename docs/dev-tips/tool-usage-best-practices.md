# Tool Usage Best Practices for Agents

## Write Tool - Ensuring Final Newlines

**Critical**: Always end file content with `\n` to prevent pre-commit hook failures.

### Good Example
```python
content = """def my_function():
    return "value"
"""  # ← Note the final newline after closing quotes
```

### Bad Example
```python
content = """def my_function():
    return "value"
"""  # ← Missing final newline - will cause pre-commit to fail!
```

### Quick Rule
If your content string doesn't explicitly end with `\n`, add it:
```python
# Ensure final newline
if not content.endswith('\n'):
    content += '\n'
```

---

## Edit Tool - Preserving Newlines

When editing files, maintain the existing newline pattern:
- If the file had a final newline, keep it
- Don't accidentally remove it with `old_string` matching

### Example
```python
# Good - preserves final newline
Edit(
    file_path="test.py",
    old_string="def func():\n    pass\n",  # ← includes final newline
    new_string="def func():\n    return True\n"  # ← preserves it
)
```

---

## Commit Workflow

**Standard Process**:
```bash
# 1. Fix newlines FIRST
./scripts/fix-newlines.sh

# 2. Stage changes
git add .

# 3. Commit (should succeed on first try)
git commit -m "message"

# 4. Push
git push origin main
```

**Why This Order**:
- Running `fix-newlines.sh` before staging ensures all files have proper endings
- Pre-commit hooks will then pass on first attempt
- No need for double commits

---

## Pre-Commit Hook Behavior

**Hooks that modify files**:
1. `trim-trailing-whitespace` - Removes trailing spaces
2. `end-of-file-fixer` - Adds final newline if missing

**If they modify files**:
- Commit fails with "files were modified by this hook"
- You must re-stage and commit again
- **This doubles the work!**

**Prevention**:
- Use `.editorconfig` (automatic in most editors)
- Run `./scripts/fix-newlines.sh` before commits
- Ensure Write tool content ends with `\n`

---

## EditorConfig Benefits

The `.editorconfig` file automatically:
- Adds final newlines to all files on save
- Trims trailing whitespace
- Enforces consistent indentation
- Works in Cursor, VS Code, JetBrains, Vim

**Supported editors**:
- **Cursor**: Built-in (no setup needed)
- **VS Code**: Install "EditorConfig" extension
- **JetBrains**: Built-in (no setup needed)
- **Vim/Neovim**: Install `editorconfig-vim` plugin

---

## For Claude Code Agents

### Before Committing Checklist

- [ ] Run `./scripts/fix-newlines.sh`
- [ ] Stage changes with `git add`
- [ ] Commit with descriptive message
- [ ] Verify pre-commit hooks pass on first try
- [ ] Push to remote

### If Pre-Commit Fails Anyway

1. **Don't panic** - just re-stage and commit
2. **Note the issue** - report what hook failed
3. **Check if preventable** - was it a newline issue?
4. **Consider filing an issue or opening a PR** if you discover a new pattern worth documenting

---

## Quick Reference

| Task | Command | Why |
|------|---------|-----|
| Fix newlines | `./scripts/fix-newlines.sh` | Prevent pre-commit failures |
| Check config | `cat .editorconfig` | See automatic editor settings |
| Verify file ending | `hexdump -C file.txt \| tail -1` | Should end with `0a` (newline) |
| Manual fix | `echo "" >> file.txt` | Add newline to single file |

---

**Added**: October 14, 2025
**Updated**: October 14, 2025
**Reason**: Prevent pre-commit hook failures that require double commits
