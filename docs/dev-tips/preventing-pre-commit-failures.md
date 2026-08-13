# Preventing Pre-Commit Hook Failures

## Common Issue: End-of-File Newlines

**Problem**: Pre-commit hooks often fail due to missing final newlines, requiring a second commit.

**Solution**: Use `.editorconfig` and helper scripts to prevent this.

---

## Quick Fix (One-Time)

If you have files staged that will fail the hook:

```bash
# Run before committing
./scripts/fix-newlines.sh
git add -u
git commit
```

---

## Permanent Solution: EditorConfig

**File**: `.editorconfig` (already configured in repo)

**What it does**:
- Automatically adds final newline to all files
- Trims trailing whitespace
- Enforces consistent indentation
- Works with most editors (VS Code, Cursor, JetBrains, Vim)

**Supported editors**:
- **Cursor**: Built-in support
- **VS Code**: Install "EditorConfig" extension
- **JetBrains**: Built-in support
- **Vim/Neovim**: Install `editorconfig-vim` plugin

---

## For Claude Code

When using the Write or Edit tools, always ensure files end with a newline:

**Good**:
```python
def my_function():
    return "value"
# ← cursor here, with blank line after
```

**Bad**:
```python
def my_function():
    return "value"# ← no newline after this
```

**Tip**: The Write tool should include `\n` at the very end of content strings.

---

## Pre-Commit Hook Behavior

**Hooks that check**:
1. `trim-trailing-whitespace` - Removes trailing spaces
2. `end-of-file-fixer` - Ensures final newline

**When they run**:
- Before every commit
- Before every push (via pre-push hook)

**If they fix files**:
- Commit will fail with "files were modified by this hook"
- You must stage the changes and commit again
- This doubles the work!

---

## Verification

Check if your editor respects `.editorconfig`:

```bash
# Create test file
echo -n "test" > test.txt

# Open in your editor, save
# Check if newline was added:
hexdump -C test.txt | tail -1
# Should end with "0a" (newline character)

# Clean up
rm test.txt
```

---

## Benefits

✅ Commits succeed on first try
✅ Consistent formatting across contributors
✅ No manual newline management
✅ Works automatically in most editors
✅ Reduces cognitive load

---

**Added**: October 14, 2025
**Reason**: Pre-commit hooks were requiring 2x commits due to missing final newlines
