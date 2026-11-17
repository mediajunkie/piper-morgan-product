#!/usr/bin/env bash
# guard-browser-launch.sh — PreToolUse (Bash): refuse a Chrome or Chromium launch without --use-mock-keychain.
# Concept: docs/internal/operations/hooks-registry.md (index); see the row for this hook.
#
# xian's rule (2026-11-11): nothing a seat runs reads his login keychain without his permission.
# On 2026-11-15 CIO started the test browser by hand without --use-mock-keychain, so it may have
# made or read one "Safe Storage" item there. xian, 2026-11-17 (via Exec): "ok to leave it. let's
# ensure it doesn't recur, though." This turns the rule into a mechanism for the Bash tool.
#
# Refuses a Bash command that has a Chrome or Chromium program among its words without
# --use-mock-keychain, whatever stands in front of it (nohup, env, timeout, arch, sudo, xargs, an
# unknown wrapper), plus `open -a` and `osascript` naming one, `bash -c`, and a variable set in the
# same command. A short list of commands that only read (ls, strings, grep, ps, codesign, git ...)
# may name the program. Fails closed on an unknown command, open on input it can't parse.
# Heredoc text going to a file is not judged (a log entry may quote a command); one fed to a shell is.
# Does NOT see: a launch from inside a script file or another program (python, node). The browser
# tool's own launches and the seat browser's LaunchAgent pass the flag themselves.
# scripts/browser_keychain_check.py is the after-the-fact check for what this cannot see.
#
# Cost:    one bash `case` per Bash call; Python only when the command mentions chrome/chromium.
# Benefit: none yet: measuring (prevention guard; no catches is the goal).
# Review:  2026-12-17.   Owner: CIO.
# Exit 2 + reason on STDERR (only stderr reaches the agent).
set -u
in="$(cat)"
case "$in" in *[Cc]hrom*) ;; *) exit 0 ;; esac
# Fail OPEN if the logic file is missing or Python errors: a broken guard must not wedge Bash.
here="$(cd "$(dirname "$0")" && pwd)"
[ -f "$here/guard_browser_launch.py" ] || exit 0
printf '%s' "$in" | python3 "$here/guard_browser_launch.py"
rc=$?
[ "$rc" = 2 ] && exit 2
exit 0
