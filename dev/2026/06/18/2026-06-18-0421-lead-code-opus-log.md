# Lead Developer — session log 2026-06-18

**Role**: Lead Developer (lead-code-opus) · **Model**: Opus 4.8 · **Worktree**: `interesting-beaver-7ee19c` (branch `claude/interesting-beaver-7ee19c`, ephemeral) · **Server**: PID 67768 (worktree cwd).

**Session start (ad-hoc, 04:21 PT — pre-07:17-START)**: PM engaged at 4:21am with live-test feedback on yesterday's D1 ships (#1173/#1225/#1239/#1254/nav-IA). 6/17 was DAY-CLOSED at 22:21. Resuming for the UAT pass; the 07:17 cron fire will find this log + resume. Prior-day STOP verified (DAY-CLOSED marker present in 6/17 log).

## PM live-test feedback (m1-test account — Stage 3+ AND GitHub-connected → showed everything incl. #1239 "20 open issues")

### 04:25 — #1225 dismiss-flash FIXED (PM finding #4)
PM: "Cards show, can be dismissed, but flash briefly on reload (at least one did)."
- **Root cause**: the async "what i'm seeing" module (places, `data-module-async`) skipped the dismiss-eval at init (signature not ready) → rendered visible → `refreshAsync()` hid it only *after* the /api/v1/places fetch completed → show-then-hide flash on reload. The sync "recently" module applies dismiss at init (no flash) → matches PM's "at least one."
- **Fix** (`web/static/js/home-modules.js`): in `initModule`, for an async module with a stored dismiss signature, add `is-dismissed` immediately (pre-fetch). `refreshAsync()` still re-evaluates against the real content and re-surfaces if it changed. Cuts the flash from "until fetch completes" to "until DOMContentLoaded." (Residual sub-DOMContentLoaded FOUC would need an inline pre-paint script — noted as polish if it still shows.)
- Verified: `test_home_modules_1225.py` + template suite green (JS-runtime behavior → PM reload is the real gate).

### Triage of PM's 7 findings
1. **Nav "Radar" button vs panel "History" header + still needs `?radar=1`** → REAL coherence gap. The #1262 nav-rename got ahead of the `?radar=1` flag graduation. Clean resolution = graduate the flag (Radar entity feed becomes the default panel + rename panel header) = the #1090/#1236 culmination → PM/CXO sign-off (it swaps the conversation-list UX for entity cards). Teed up to PM.
2. **"Lists" (never saw "Collections") + Files/Documents dual** → expected. "Collections" was trust-gated ≥4 so PM never saw it; now ungated + relabeled "Lists." Files/Documents dual = #1270 WIP (CXO decided one "Documents"; route consolidation PPM-gated on object-model). Confirmed WIP.
3. **Chat anchored but fully occluded by modules** → REAL. #1173 full-height chat + the now-visible Stage-3 ambient modules compete for vertical space; modules win, push chat below fold. #1225 collapse/dismiss is the user-side mitigation, but the *default* (expanded) occludes chat. Composition/default-state = CXO call (the deviation #1173 registered). Teed up + interim options offered.
4. **Flash on reload** → FIXED (above).
5. **Empty-state (#1263) needs fresh account** → correct; verified by render test + copy matches CXO. No action.
6. **Lists every GitHub issue** → known #1233 limitation. Beta path is repo-scoped (all open issues), not user-assigned — assignee filtering needs the user→github-identity map (#1233). Noted as a refinement.
7. **Browser zoom (#1254)** → ✅ confirmed working.

- **Account note**: PM on m1-test (Stage 3 + GitHub-connected = ideal test account). The `xian` Stage-3 bump I did earlier was moot; revert on PM's word.
