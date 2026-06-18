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

### 04:40 — Radar swap GRADUATED (#1090) + #3 chat-occlusion interim — PM-authorized
PM: "Let's authorize the swap. There are no real users and I have approved the Radar design." + #3 guidance (cap module heights/total, modules yield to chat, or chat maximizes when active; modules may move to the Radar aside; default-collapsed "probably safe too").
- **#1090 SWAP — Radar is now the DEFAULT Layer-2 panel** (`d17ff1cfb`): flipped home.html so `loadRadar()` runs by default (`?radar=0` = escape hatch to the conversation list; loadRadar still falls back to it on error). `renderRadar` already swaps the panel title→"📡 Radar" + hides load-more, so no static header change needed.
  - **Verify-first caught a regression**: the History *list* was click-to-resume-conversation, but `renderRadarCard` built **non-clickable** cards → graduating as-is would lose conversation navigation. **Fixed in the swap**: cards with a ref get `data-entity-type`/`data-ref`/`tabindex`/`.radar-card--clickable`; the delegated click routes by type — **Conversation→resume the chat** (the path the list used), **Work item→open the GitHub issue** (new tab), **Document→/documents**. Enter/Space parity; refless (example) cards stay inert. token_lint PASS; **91 radar/sidebar/modules/route tests green** (updated the gate test default-on; +5 clickable-card tests in TestRadarSurface).
  - **Known follow-up (→CXO)**: search-in-Radar still searches conversations only (placeholder says "search everything"); pre-existing, noted.
- **#3 chat-occlusion interim — modules default COLLAPSED** (`90b237769`): both ambient sections server-render `is-collapsed` + `aria-expanded=false` (server-rendered → no collapse-flash); `home-modules.js` default = collapsed-unless-explicitly-expanded. Chat-first by default; user's explicit expand persists. **Interim only — CXO owns the fuller composition** (PM's principles above). 9 #1225 tests green.
- **Template + inline JS → live on reload; the #4 flash fix (home-modules.js, static) needs a HARD reload** (JS cache). No server restart needed.
- **NEXT**: route #1 (search-in-Radar reconcile) + #3 (composition) to CXO with PM's principles; answer PM's #6 (GitHub-handle config → filter to "assigned to me", a small #1233-lite build). Cron armed `0351e020`; next fire 07:17.
