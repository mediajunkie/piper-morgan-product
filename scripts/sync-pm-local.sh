#!/usr/bin/env bash
# sync-pm-local.sh v2 — keep PM's local main checkout current after a push (#1368).
#
# Problem: agents push to origin/main from their own ephemeral worktrees all session long, but PM's
# local main checkout (a separate working directory) doesn't auto-update. PM has to remember to `git
# pull` to see current inbox/carry-forward/session-log state — an easy-to-forget manual step.
#
# v1 (2026-07-04) skipped the sync entirely whenever PM's checkout had ANY uncommitted changes — too
# conservative in practice: PM's checkout accumulates agent-generated drift (mailbox MANIFESTs mainly,
# ~70%+ of observed drift per Docs's 2026-07-06 analysis) as a side effect of local hook runs, and that
# alone was enough to block every sync even when PM's actual WIP (prose drafts) was completely
# unaffected. PM's own words (2026-07-04): "It used to be agents helped keep my local main synced for
# me and now I am being told to do it all manually myself, which feels like a regression from
# assistance to homework."
#
# v2 (2026-07-07) replaces the binary guard with a 3-tier path classifier (design: PA proposed, CIO
# reviewed, Docs added the content-heuristic safety refinement, ratified on #1368):
#   Tier 1 — always-safe path match: mailbox MANIFESTs, per-role carry-forward files, session logs.
#            These are derived/regenerable — origin/main's copy is always the canonical one. Cleared
#            unconditionally via a SURGICAL `git checkout origin/main -- <path>` (never a broad
#            checkout/reset — HARD RULE).
#   Tier 2 — content-heuristic path match: decisions.log, editorial-calendar. PM-writable directly
#            (CLAUDE.md's "any agent can append" is a floor, not a ceiling), so path alone isn't
#            sufficient. Cleared ONLY if the local diff from HEAD is whitespace-only, or the file's
#            line count didn't grow (net shrink/no-growth = someone reformatted or trimmed, not added
#            real content). Otherwise held for PM's own review — never guessed away.
#   Tier 3 — everything else (every `??` untracked file, and any modified/deleted path not matching
#            tier 1 or 2): PM's WIP. Never touched, full stop — not cleared, not even read for content.
#
# Per-path exclusion, not whole-sync abort (PM steer, 2026-07-08): a tier-3 hit does NOT block
# clearing the (disjoint) tier-1/2 paths or attempting the pull. Clearing tier-1/2 files can only ever
# touch those exact paths — it structurally cannot reach a tier-3 file. And the final `git pull
# --ff-only` is independently protected by git itself: if the incoming diff ever touched a path that's
# genuinely dirty in the working tree, the fast-forward refuses outright rather than overwriting it.
# So tier-3 presence changes nothing about what's safe — it only changes whether THAT one file gets
# left alone (always) vs. whether the WHOLE sync gets held hostage to an unrelated dirty file (no
# longer, as of v2). Given PM's normal workflow is "prose mid-edit in this checkout," a whole-sync
# abort meant the sync almost never actually ran — this is what makes the fix actually useful daily.
#
# Safety invariants carried over from v1, unchanged:
#   --ff-only : refuses to create a merge commit and refuses outright if a real merge would be needed.
#   Never touches a checkout that isn't on `main`.
#   Silent, non-fatal no-op on any unexpected condition — never blocks or surprises.
#
# Usage:
#   scripts/sync-pm-local.sh              live mode — classifies, clears tier-1/2-eligible drift,
#                                          fast-forwards. Silent no-op on any skip condition.
#   scripts/sync-pm-local.sh --dry-run    read-only preview — classifies and reports what WOULD be
#                                          cleared/held/skipped. Makes no changes. Use this first
#                                          against real drift before trusting live mode (design note
#                                          on #1368: "don't trust the classifier logic on paper alone").
#
# Env override: PM_CHECKOUT (default: the canonical main checkout path)

set -uo pipefail

# Host-aware default (fixed 2026-07-26). The single hard-coded path below was the LAPTOP checkout;
# on Amber it doesn't exist, so this script no-opped for every agent since the migration — and its
# "not a git checkout — skipping" message is easy to read as the *intended* back-off (the
# PM-has-uncommitted-work case) rather than a misconfiguration. That silent no-op is also why the
# shared Amber checkout drifts, which is why duty-cycle-freeze-check.sh reads a stale registry:
# newly-pushed rows stay invisible to the watchdog. Try known checkouts in order, same shape as the
# fix already applied to duty-cycle-freeze-check.sh.
PM_CHECKOUT="${PM_CHECKOUT:-}"
if [ -z "$PM_CHECKOUT" ]; then
  for cand in /Users/xian/Development/piper-morgan-product \
              /Users/xian/Development/piper-morgan/piper-morgan-product; do
    [ -d "$cand/.git" ] && { PM_CHECKOUT="$cand"; break; }
  done
fi
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

# FAIL LOUDLY if no candidate exists — "registry missing" and "all healthy" must never look alike.
[ -n "$PM_CHECKOUT" ] || { echo "sync-pm-local: NO known PM checkout found — this script synced NOTHING. Set PM_CHECKOUT." >&2; exit 3; }
[ -d "$PM_CHECKOUT/.git" ] || { echo "sync-pm-local: $PM_CHECKOUT is not a git checkout — skipping" >&2; exit 0; }

G() { git -C "$PM_CHECKOUT" "$@"; }

# Only act if PM's checkout is actually on main — never touch it if PM has switched branches locally.
CUR_BRANCH=$(G rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [ "$CUR_BRANCH" != "main" ]; then
    echo "sync-pm-local: PM checkout is on '$CUR_BRANCH', not main — skipping" >&2
    exit 0
fi

G fetch origin main -q 2>/dev/null || { echo "sync-pm-local: fetch failed — skipping" >&2; exit 0; }

# --- classify every dirty path -----------------------------------------------------------------
is_tier1() {
    case "$1" in
        mailboxes/*/inbox/MANIFEST.md|mailboxes/*/read/MANIFEST.md) return 0 ;;
        dev/active/*-carry-forward.md) return 0 ;;
        dev/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*-log.md) return 0 ;;
        *) return 1 ;;
    esac
}
is_tier2() {
    case "$1" in
        docs/internal/architecture/decisions/decisions.log) return 0 ;;
        docs/internal/planning/comms/editorial-calendar*) return 0 ;;
        *) return 1 ;;
    esac
}

tier1_paths=""; tier2_candidates=""; tier3_hit=0
while IFS= read -r line; do
    [ -z "$line" ] && continue
    status="${line:0:2}"
    path="${line:3}"
    # git quotes a path in porcelain output whenever it contains characters it considers "unusual" —
    # this triggers on parens (independent of core.quotepath), which real paths in this repo hit
    # (e.g. "mailboxes/xian (ceo)/..."). Strip one wrapping pair of double quotes if present, so
    # pattern-matching below sees the real path. Our paths never contain embedded quotes/backslashes,
    # so a plain strip is sufficient — no need for full C-string unescaping.
    plen=${#path}
    if [ "$plen" -ge 2 ] && [ "${path:0:1}" = '"' ] && [ "${path:$((plen-1)):1}" = '"' ]; then
        path="${path:1:$((plen-2))}"
    fi
    # untracked files are always PM's WIP -- `git pull` never touches them anyway, and they're never
    # a candidate for any tier — but they DO still count toward "checkout has real WIP" awareness.
    if [ "$status" = "??" ]; then
        tier3_hit=1
        continue
    fi
    if is_tier1 "$path"; then
        tier1_paths="${tier1_paths}${path}"$'\n'
    elif is_tier2 "$path"; then
        tier2_candidates="${tier2_candidates}${path}"$'\n'
    else
        tier3_hit=1
        echo "sync-pm-local: unknown-path dirty file (PM's likely WIP): $path" >&2
    fi
done <<< "$(G status --porcelain 2>/dev/null)"

if [ "$tier3_hit" -eq 1 ]; then
    echo "sync-pm-local: PM checkout has WIP outside known-safe paths — leaving those alone, proceeding with tier-1/2 paths only" >&2
fi

# --- tier 2: content-heuristic — clear only if whitespace-only diff, or the file didn't grow -----
tier2_clear=""; tier2_hold=""
while IFS= read -r path; do
    [ -z "$path" ] && continue
    if G diff --quiet -w -- "$path" 2>/dev/null; then
        tier2_clear="${tier2_clear}${path}"$'\n'
    else
        read -r added deleted _ <<< "$(G diff --numstat -- "$path" 2>/dev/null)"
        if [ -n "${added:-}" ] && [ -n "${deleted:-}" ] && [ "$added" -le "$deleted" ] 2>/dev/null; then
            tier2_clear="${tier2_clear}${path}"$'\n'
        else
            tier2_hold="${tier2_hold}${path}"$'\n'
        fi
    fi
done <<< "$tier2_candidates"

if [ -n "$tier2_hold" ]; then
    echo "sync-pm-local: content-heuristic path(s) grew with real changes — holding for manual review (not cleared):" >&2
    echo "$tier2_hold" | sed '/^$/d;s/^/sync-pm-local:   /' >&2
fi

clear_list="$(printf '%s%s' "$tier1_paths" "$tier2_clear" | sed '/^$/d')"

if [ "$DRY_RUN" -eq 1 ]; then
    if [ -n "$clear_list" ]; then
        echo "sync-pm-local: DRY RUN — would clear (tier 1 + eligible tier 2):"
        echo "$clear_list" | sed 's/^/sync-pm-local:   /'
    else
        echo "sync-pm-local: DRY RUN — nothing to clear"
    fi
    echo "sync-pm-local: DRY RUN — no changes made; re-run without --dry-run to apply"
    exit 0
fi

# --- live mode: surgically clear, then attempt the fast-forward ---------------------------------
if [ -n "$clear_list" ]; then
    while IFS= read -r path; do
        [ -z "$path" ] && continue
        if G checkout origin/main -- "$path" 2>/dev/null; then
            echo "sync-pm-local: cleared $path (now matches origin/main)"
        else
            echo "sync-pm-local: warning — could not clear $path, left as-is" >&2
        fi
    done <<< "$clear_list"
fi

if G pull origin main --ff-only -q 2>/dev/null; then
    echo "sync-pm-local: PM checkout fast-forwarded to $(G rev-parse --short HEAD)"
else
    echo "sync-pm-local: fast-forward failed (PM checkout may have local commits, or an untiered path is still blocking, or a network issue) — left untouched" >&2
fi
