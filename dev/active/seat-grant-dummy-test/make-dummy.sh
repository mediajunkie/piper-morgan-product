#!/usr/bin/env bash
# Run by Pard (or xian), not by the seat under test. Makes the dummy "credential" file.
# The value is random and is not a credential for anything.
set -euo pipefail
f="$HOME/.piper-shared/seat-dummy-credential-2026-11-15.txt"
umask 077
printf 'dummy-not-a-credential-%s\n' "$(python3 -c 'import secrets; print(secrets.token_hex(8))')" > "$f"
chmod 600 "$f"
echo "made $f ($(wc -c < "$f" | tr -d ' ') bytes)"
