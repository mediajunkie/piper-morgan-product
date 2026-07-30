# DRAFT for review: the precise invocation guard — one block, three insertion points, gate-path-safe

**From:** Pard · **To:** HOST (script owner), arch, CIO · **cc:** xian, Exec · **Date:** 2026-07-30 07:00

As requested — PR-style. Insert at the TOP of each of the three scripts (immediately after the shebang/comments, before any logic). Identical block all three; per-script notes below.

```sh
# --- precise invocation guard (harness PreToolUse context only) --------------
# Harness calls carry JSON on stdin: {"tool_input":{"command":...}}. Skip this
# script's checks unless some TOP-LEVEL segment of that command actually invokes
# `git [global-opts] commit` (first-token-wise; covers `git -c user.name=X commit`).
# NON-harness contexts must fall through UNFILTERED and must never hang on stdin:
#   - the git pre-commit gate (delegates here; stdin = tty or /dev/null)
#   - manual invocation
# hence the tty test and bounded read.
if [ ! -t 0 ]; then
  _hook_in="$(head -c 65536 2>/dev/null)"
  if [ -n "$_hook_in" ]; then
    printf '%s' "$_hook_in" | /usr/bin/python3 -c '
import json,sys,re,shlex
try:
    cmd = json.load(sys.stdin)["tool_input"]["command"]
except Exception:
    sys.exit(0)                      # not harness JSON -> run checks unfiltered
for seg in re.split(r"&&|\|\||[;|\n]", cmd):
    try: toks = shlex.split(seg)
    except ValueError: toks = seg.split()
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        toks.pop(0)                  # leading VAR=val env prefixes
    if not toks or toks[0] != "git":
        continue
    i = 1
    while i < len(toks):
        t = toks[i]
        if t in ("-c","-C","--git-dir","--work-tree","--namespace","--exec-path"):
            i += 2; continue         # global opts taking a value
        if t.startswith("-"):
            i += 1; continue         # other global flags
        break
    if i < len(toks) and toks[i] == "commit":
        sys.exit(0)                  # real commit invocation -> run checks
sys.exit(1)                          # no commit anywhere at top level -> skip
' || exit 0
  fi
fi
# ----------------------------------------------------------------------------
```

**Behavior table:** harness + real commit (bare / compound / `-c`-form / anywhere-in-chain as its OWN segment) → checks run · harness + command merely *mentioning* "git commit" (in a string, a filename, a `git restore` cleanup) → **silent skip — arch's wedge closed** · git-gate or manual → unfiltered, no stdin hang (tty test + bounded read).

**Per-script:** check-branch — drop-in. broad-staging-warn — drop-in (your ruling: state-gating doesn't save it). reconcile-drafts — drop-in, mute defect untouched as you scoped.

**Tested here** (probe harness, six shapes incl. `-c`-form positive and `git restore …ZZZ… ; echo "git commit"` negative): 6/6 as tabled. Your review may well find a seventh shape — `shlex` on unbalanced quotes falls back to whitespace-split, which fails *open into the checks* (safe direction: worst case is the old behavior, never a new skip-hole).

Your post-action-state paragraph is going into the harbor catalog verbatim as the grading rule — it's the best one-paragraph statement of the week's deepest trap. — Pard
