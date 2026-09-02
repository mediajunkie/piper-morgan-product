# Web Cron Prompt — v0.7 web-variant (main-direct; START 9:57am + STOP 11:57pm)

> **STATUS (2026-06-09): SHELVED — operator-launch deferred indefinitely.** Cycle launch was stood down 2026-06-06 after PM noted the "doppleganger session" mental-model mismatch. CIO confirmed cycle agents are peer top-level sessions but flagged a doc-vs-practice drift on the actual launch gesture (Desktop New session vs terminal `claude`); PM is using both methods, discussion ongoing with CIO. Web's main-direct 2×/day variant remains ratified as the 5th registered shape (`cron-shape-experiments.md` row 5) — design content below is preserved for that registry reference and for any future revisit. The `claude/web-cycle` worktree was cleaned up 2026-06-09; if cycle launch resumes, no worktree is needed under this variant.

**Purpose**: copy the block below into `CronCreate` once a Claude Code session is launched in plain product main. Web-specific variant of v0.7 — bypasses worktree-Model-A entirely AND auto-finalizes the day's log at 11:57pm so Docs has a clean log to omnibus next morning without PM rousing.

**Filed**: 2026-05-29 (initial worktree-Model-A version) · rewritten 2026-06-05 to the main-direct variant per PM direction; second fire shifted to 11:57pm so it does STOP-style day-close (PM 6/5 clarification: "logs get finalized when the day is over even if I am not around to remind you"). Surfaced to CIO same day. **Shelved 2026-06-06; status banner added 2026-06-09.**

**Shape rationale (web-specific variant)**:
- Web's substantive code work is in `piper-morgan-website` (separate repo) — already isolated from product-main clash. Worktree's clash-avoidance benefit doesn't apply to web's substantive lane.
- Web's product-repo work in a cycle fire is mail triage + log housekeeping — narrow file scope, brief duration, small clash window. Main-direct is simpler than worktree + bridge.
- **STOP fire at 11:57pm satisfies the omnibus-input goal**: each day-close finalizes the log autonomously; Docs has a complete log next morning without PM needing to rouse web.

**Cron expression**: `57 9,23 * * *` (fires at 9:57am START + 11:57pm STOP, PT).

**Offset**: `:57` (web's registered slot per CIO cohort slate).

**Pre-flight (PM operator action — ONE step)**:
1. Open a Claude Code session in `/Users/xian/Development/piper-morgan/piper-morgan-product` (NOT a worktree — plain product main).
2. Register the cron with the block below.

That's it — no worktree creation, no sync dance, no Model-A-vs-B gotchas.

---

## The cron block

```
DUTY CYCLE TICK (Web — v0.7 web-variant; main-direct 9:57am START + 11:57pm STOP)

Autonomous loop fire; no human driving this turn. Hold the discipline; be holistic-not-tactical.

CWD: this session is launched in /Users/xian/Development/piper-morgan/piper-morgan-product (plain main; NOT a worktree). Web operates on main directly — the worktree-Model-A dance doesn't fit web's lightweight 2×/day shape.

TWO-REPO NOTE: web's code work is in /Users/xian/Development/piper-morgan/piper-morgan-website (separate repo, own main, GitHub Pages deploy). Substantive code edits do NOT happen in autonomous fires — they happen in focused PM-handoff sessions in the website repo. Autonomous fires are mail-awareness + day-close.

STATE (today — first-fire-of-day creates these):
- Session log: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-web-code-opus-log.md
- Cycle log: dev/active/cycle-log-web-YYYY-MM-DD.md
- Task list: dev/active/web-standing-items.md
- Attention doc: dev/active/duty-cycle-escalations-web.md

CRITICAL SEMANTICS (lighter than continuous-lane): each non-STOP fire = wake → drain mail (triage to read/ with disposition) → optionally advance ONE smallest-scope unblocked low-priority item → IDLE. STOP fire = mail catch-up + day-close session+cycle logs + push + re-arm cron. NOT continuous drain.

CHECK DISPATCHER (2×/day shape):
- Cron fires at 9:57am (morning START) + 11:57pm (evening STOP). The morning fire IS the self-wake (no separate WATCH/START dance).
- ~9:57am fire AND no session log for today? → START (procedures/start.md): open today's session log + cycle log; mail loop; IDLE.
- ~9:57am fire AND session log already exists (e.g. PM-handoff session today)? → MAIL LOOP only; IDLE.
- ~11:57pm fire → STOP (procedures/stop.md): mail loop; day-close the session log (append close-out section noting end-of-day state); cycle-log final entry; commit + push; **CronCreate the same `57 9,23 * * *` expression as the final action — never go quiet cron-deleted** (CIO 6/3 STOP-leaves-armed principle, adapted for 2×/day).

CRON LIFECYCLE (procedures/cron-lifecycle.md):
- Rule 1 (strict — CronDelete-FIRST): if the fire may go substantive (>2 min), CronDelete as the LITERAL FIRST action. Do work, CronCreate at IDLE. Never go quiet cron-deleted — INCLUDING at end of STOP (re-arm the same expression).
- Rule 2 (PM-presence): leave cron running during PM conversation — runtime idle-only-fire suppresses; do NOT CronDelete just for PM messages.
- v0.6.2: quick mail-check before substantive PM engagement.
- v0.6.3: advance one smallest-scope unblocked low-priority item if obvious. Blast-radius is a filter — site-wide visual/code changes prefer PM-supervised over autonomous.

WORKFLOW (main-direct — no worktree dance):
- Sync at fire start: git pull origin main (just pull; we're on main directly).
- Mail triage (inbox→read), cycle log entries, day-close — all commit directly to main.
- Substantive website-repo work is independent: cd to /Users/xian/Development/piper-morgan/piper-morgan-website, commit on its main, push origin main (triggers Pages deploy).
- EXPLICIT-PATHS-ONLY on git add — never directory-level adds (safety against sweeping in other agents' working state on product main).
- Other-agent working-tree state on product main: assume dirty; stage only my own files by path; never `git add -A` or `git add .`.

PROCEDURE EACH FIRE:
1. Time check: date "+%H:%M %Z"
2. CronList (get cron-id for Rule-1 pauses)
3. CHECK dispatcher → execute
4. Append fire entry to cycle log (every fire commits a one-line entry — for 2×/day, every fire is significant).
5. Commit (explicit paths only) → git push origin main.
6. STOP fires only: ensure CronCreate `57 9,23 * * *` as final action (leaves armed for tomorrow's 9:57am START).
7. Brief status report (1-3 sentences).

DISCIPLINE: descriptive names not cryptic ordinals; promises durable (mechanism not vigilance); holistic-not-tactical.
```

---

## How this satisfies the omnibus-input goal

| | Old (manual rouse) | New (2×/day with STOP) |
|---|---|---|
| Day-end log finalization | PM had to rouse web in the morning to wrap yesterday's log | Happens autonomously at 11:57pm |
| Docs's omnibus input | Sometimes missing (web hadn't day-closed yet) | Always finalized by midnight |
| PM overhead | Re-prompt web each morning | Zero — cron handles it |
| Reliability dependency | Manual prompting | Persistent local session staying alive past 11:57pm |

If your laptop is regularly closed before 11:57pm, the STOP fire won't happen and we revert to manual-rouse-style. Adjust the STOP time if your usage pattern needs an earlier slot.

## Differences from the canonical worktree-Model-A v0.7

| | Canonical worktree-Model-A | Web variant (main-direct) |
|---|---|---|
| Session launch location | `claude/{role}-cycle` worktree | Plain product main repo |
| Cycle work commits | Branch → push branch:main | Direct to main |
| Mailbox writes | Via main-worktree bridge | Direct (we ARE on main) |
| Operator setup | `git worktree add` + launch + sync | Just launch |
| Clash exposure | Eliminated via worktree | Small (brief fires, narrow file scope) |
| Day-end log close | STOP fire at ~11pm via hourly schedule | STOP fire at 11:57pm via 2×/day schedule |
| Suitable for | Continuous lanes; substantive cycle work | Lightweight intermittent mail-check + reliable day-close |

## Cleanup note (deferred)

The existing `claude/web-cycle` worktree at `/Users/xian/Development/piper-morgan/piper-morgan-product-web-cycle` is unused under this variant. Cleanup: `git worktree remove ../piper-morgan-product-web-cycle && git branch -D claude/web-cycle` from product main. Deferred until variant proves out.

## Cross-references

- CIO 6/2 cron-shape experimentation authorization (read): `mailboxes/web/read/memo-cio-to-cohort-cc-pm-cron-shape-experimentation-authorized-2026-06-02.md`
- CIO 6/3 overnight-continuity (read): `mailboxes/web/read/memo-cio-to-cohort-cc-pm-overnight-continuity-fix-self-wake-2026-06-03.md`
- Canonical worktree-Model-A (superseded for web): `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md`
- Web variant memo to CIO (filed 2026-06-05): `mailboxes/cio/inbox/memo-web-to-cio-cc-pm-pa-web-variant-main-direct-with-stop-fire-2026-06-05.md`

---

*Filed by Web 2026-06-05, variant of v0.7 per PM direction (simpler shape) + PM 6/5 clarification (logs finalize autonomously at day-end for omnibus input).*
