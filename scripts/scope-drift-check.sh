#!/usr/bin/env bash
# scope-drift-check.sh — detection predicate for standing-item 7t (the "scope-guard chokepoint").
#
# ORIGIN: PM found the duty-cycle has no intake from the backlog (2026-09-08); the same week's
# follow-up found the inverse failure — a deliverable SHIPS but its issue's state/milestone never
# updates, and nothing notices (#1635: shipped 08-28, sat unmoved 11 days because the issue's own
# title changed and the milestone didn't). A periodic human audit already decayed once (CXO's own
# 08-30 hand-check, ten days — CLAUDE.md's own chokepoint-vs-bolt-on lesson, methodology-53).
#
# DESIGN (joint with Arch, 2026-09-09/10 mail thread): Arch owns the GH Action skeleton + the
# mailbox-write delivery mechanics (a flag lands as a memo in the named consumer's inbox, not just
# a GH issue comment nobody monitors — mail's mandatory per-fire drain does the enforcement work).
# This script is CIO's half: the detection predicate + the flag's content. Arch's Action invokes
# this on `push: main`, passing the pushed commit range; this script never pushes/comments itself
# (v1 is READ-ONLY against GitHub — it prints flags, Arch's Action decides what to do with them).
#
# TWO SIGNALS, either one is sufficient to flag:
#   (A) COMMIT-CLOSURE-LANGUAGE: a commit in the range references #N with an apparent closure
#       intent (close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved immediately before
#       #N — the same keyword family GitHub's own auto-close matches), AND #N is still OPEN.
#   (B) CHECKBOX-COMPLETE: an issue referenced ANYWHERE in the commit range's messages has a body
#       whose `- [ ]` / `- [x]` checklist is 100% checked, AND the issue is still OPEN.
#
# ⚠️ THE #1278 HAZARD, AND WHY THIS SCRIPT IS NEGATION-AWARE WHERE GITHUB'S OWN MATCHER ISN'T
# (Arch's explicit design condition, 2026-09-09): GitHub's real auto-close uses PLAIN keyword
# adjacency with NO negation understanding — "not yet resolved: #1278" auto-closes #1278 exactly
# as if it said "resolved #1278" (documented incident, 2026-07-04/05, closed a live Beta Blocker).
# If THIS script copied that same naive pattern for signal (A), it would generate its own false
# positives: a commit honestly saying "issue #N remains open, not yet fixed" would be misread as
# closure-intent, and if #N is (correctly) still open, that would be flagged as "drift" when there
# is none — manufacturing exactly the class of alarm this guard exists to avoid triggering
# elsewhere. So signal (A)'s extractor checks for a negation word in the few words immediately
# before the closure keyword and skips the match if found. This makes THIS extractor safer than
# GitHub's own — a deliberate asymmetry, not an oversight.
#
# OUTPUT: one line per flagged issue on stdout, always states which signal fired and what was
# checked (m-44/m-53 discipline: never a bare "drift" with no denominator). A one-line summary
# denominator to stderr on every run — "checked N commits, M issue references, F flagged" — so a
# silent run (no output) is distinguishable from a run that measured nothing.
#
# EXIT CODES (v1.1, 2026-09-10 — corrected after Arch's Action was found to already check for
# this contract, `if [ $RC -gt 1 ]`, while this script only ever returned 0. That branch was dead
# code protecting against nothing — a real internal predicate failure (bad range, corrupt repo)
# would have printed a warning to stderr and still exited 0, indistinguishable from "ran cleanly,
# found nothing." The exact "clear is not a measurement" shape this whole thread spent the
# afternoon catching in three other places, found here by checking my own script's contract
# against what its caller actually assumes, not by re-reading my own header comment):
#   0 = ran successfully — 0 or more flags is a NORMAL outcome, not distinguished by exit code.
#       Flags themselves are on stdout; "clean" vs "found something" is never encoded in the exit
#       status, only in whether stdout is empty.
#   2 = the predicate could not run at all — not a git repo, or `git log` itself failed on the
#       given range. This is the case Arch's Action's `rc -gt 1` guard exists to catch.
set -uo pipefail

REPO="${SCOPE_DRIFT_REPO:-$(git rev-parse --show-toplevel 2>/dev/null)}"
GH_REPO="${SCOPE_DRIFT_GH_REPO:-mediajunkie/piper-morgan-product}"
RANGE="${1:-HEAD~1..HEAD}"   # commit range to scan; Arch's Action passes the actual push range
G() { git -C "$REPO" "$@"; }

if [ -z "$REPO" ] || ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  echo "scope-drift-check: ERROR — '${REPO:-<unset>}' is not a git repo (set SCOPE_DRIFT_REPO); measured NOTHING." >&2
  exit 2
fi

# Verify the range itself is valid BEFORE trusting a `git log` loop that silently reads zero lines
# on failure either way — a malformed range and a legitimately-empty range must not look the same.
if ! G log --format='%h' "$RANGE" >/dev/null 2>&1; then
  echo "scope-drift-check: ERROR — commit range '$RANGE' is invalid or unreadable in '$REPO'; measured NOTHING." >&2
  exit 2
fi

NEGATION_WORDS='not|never|no|isn.?t|doesn.?t|didn.?t|wasn.?t|hasn.?t|haven.?t|won.?t|cannot|can.?t|yet to be|still needs|remains'
CLOSE_WORDS='close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved'

n_commits=0
n_refs=0
n_flagged=0

# ── Gather all (commit_sha, commit_subject) pairs in range ──────────────────────────────────────
while IFS=$'\t' read -r sha subject; do
  [ -z "$sha" ] && continue
  n_commits=$(( n_commits + 1 ))

  # Extract every #N in the subject line (a body-wide scan is a v2 concern — v1 matches the
  # convention this cohort actually uses: issue refs live in the commit SUBJECT).
  while IFS= read -r num; do
    [ -z "$num" ] && continue
    n_refs=$(( n_refs + 1 ))

    # ── Signal (A): closure-language adjacent to #N, negation-checked ──────────────────────────
    # Look at the text in a window before this specific #N occurrence for a close-keyword, then
    # check the several words before THAT keyword for a negation term.
    before_hash="${subject%%"#$num"*}"
    if printf '%s' "$before_hash" | grep -qiE "(${CLOSE_WORDS})[[:space:]:]*$"; then
      # Found a close-keyword immediately before this #N. Now check for negation further back.
      window="$(printf '%s' "$before_hash" | grep -oiE "(${NEGATION_WORDS})[^#]{0,40}(${CLOSE_WORDS})[[:space:]:]*$" || true)"
      if [ -n "$window" ]; then
        continue   # negated — e.g. "not yet resolved: #N" — not a closure-intent signal, skip
      fi
      state="$(gh api "repos/$GH_REPO/issues/$num" --jq '.state' 2>/dev/null)"
      if [ "$state" = "open" ]; then
        n_flagged=$(( n_flagged + 1 ))
        echo "DRIFT-A #$num — commit $sha (\"$subject\") reads as closure-intent for #$num, but #$num is still OPEN. Possible scope drift: verify whether the work landed and the issue needs closing, or whether this reference was informational only."
      fi
    fi
  done < <(printf '%s' "$subject" | grep -oE '#[0-9]+' | tr -d '#')
done < <(G log --format='%h%x09%s' "$RANGE" 2>/dev/null)

# ── Signal (B): checkbox-complete but still open, for every #N referenced anywhere in range ────
declare -a seen_issues=()
while IFS=$'\t' read -r sha subject; do
  [ -z "$sha" ] && continue
  while IFS= read -r num; do
    [ -z "$num" ] && continue
    case " ${seen_issues[*]:-} " in *" $num "*) continue ;; esac
    seen_issues+=("$num")

    body="$(gh api "repos/$GH_REPO/issues/$num" --jq '.body // ""' 2>/dev/null)"
    state="$(gh api "repos/$GH_REPO/issues/$num" --jq '.state' 2>/dev/null)"
    [ -z "$body" ] && continue
    [ "$state" != "open" ] && continue

    total=$(printf '%s' "$body" | grep -cE '^[[:space:]]*[-*][[:space:]]+\[[ xX]\]' || true)
    checked=$(printf '%s' "$body" | grep -cE '^[[:space:]]*[-*][[:space:]]+\[[xX]\]' || true)
    if [ "${total:-0}" -gt 0 ] && [ "${checked:-0}" -eq "${total:-0}" ]; then
      n_flagged=$(( n_flagged + 1 ))
      echo "DRIFT-B #$num — all $total acceptance-checkbox(es) are checked, but #$num is still OPEN. Possible scope drift: verify whether this issue is ready to close."
    fi
  done < <(printf '%s' "$subject" | grep -oE '#[0-9]+' | tr -d '#')
done < <(G log --format='%h%x09%s' "$RANGE" 2>/dev/null)

echo "scope-drift-check: checked $n_commits commit(s) in range '$RANGE', $n_refs issue reference(s), $n_flagged flagged, at $(date '+%Y-%m-%d %H:%M')" >&2
exit 0
