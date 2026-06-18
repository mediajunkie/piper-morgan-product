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

### 04:50 — CXO composition memo + #6 "assigned to me" filter shipped (PM "Yes, #6 next")
- **CXO memo delivered** (`6ceab55cb`): Radar swap live + 2 composition calls — #3 home-modules-vs-chat (with PM's principles: cap height/total, modules yield to chat, chat-maximizes-when-active, or move modules to Radar aside) + search-in-Radar scope (placeholder promises "everything", searches only conversations).
- **#6 SHIPPED** (`116012ca2`): Radar work items now scope to **"assigned to me"** when a GitHub handle is configured.
  - `repo_resolver.read_user_github_handle(user_id)`: reads `github_username` from the per-user github_preferences store (alongside the repo binding) → falls back to `PIPER_GITHUB_HANDLE` env → None (None = no filter, opt-in, show-all preserved). Single-bound-user form of #1233; generalizes with no rework.
  - `radar._filter_issues_by_assignee(issues, handle)`: pure, case-insensitive filter on the issue `assignees` logins. `_WorkItemProvider` reads the handle, fetches wider (100) when filtering so assigned issues aren't missed, caps display at 25.
  - TDD: 6 tests (TestWorkItemAssigneeFilter); 29 radar tests green.
- **Server RESTARTED → PID 89762** with `PIPER_GITHUB_HANDLE=mediajunkie` (single-user-beta config; PM's github login per repo owner) so #6 is live + demoable (was PID 67768). health 200. #6 is a Python change → restart required (unlike the swap/#3 which served fresh).
- **Live now for PM**: hard-reload → Radar work items filter to mediajunkie-assigned. **Caveat surfaced to PM**: if few repo issues are assigned to the handle, few/no work-item cards show — that's correct (honest "my plate"), not a bug. PM corrects the handle if m1-test's GitHub is a different login.

### 05:05 — PM "things look good" → closed #1173 + #1239 properly (UAT passed)
PM confirmed the UAT pass + asked what's closeable. Closed-properly (description-first → comment → close):
- **#1173 CLOSED** (DESIGN-FLOOR-C1 chat-page conformance): full-height anchored chat shipped + UAT-confirmed. Registered the ambient-modules-above-chat deviation → composition routed to CXO (not a #1173 gap).
- **#1239 CLOSED** (WorkItemEntitySource): beta deliverable met (single-bound-user→repo + assigned-to-me); 16 ACs checked, the 1 genuine #1233-gate dependency kept `[ ]` with a note (full multi-identity stays separate — no false-done). Updated #1237 umbrella (3 of 4 facets live; People/#1240 PPM-gated).
- **#1225 = closeable but HELD** (PM's call): the collapse/dismiss affordance is done + UAT'd, but #1225 is the natural tracking home while the #3 composition is mid-flight with CXO. Recommended close-with-followups; awaiting PM.
- **Lead D1-unblocked = DRAINED**: remainder gated — CXO (composition + search-scope), PPM (#1270 object-model, #1240 People), design-pass (#1269). Beyond D1: RECONNECT (next sprint) is Arch-ADR-gated. Surfaced to PM for the what's-next call (~5am; cohort memos out; cron 07:17).

### 05:40 — PM behavioral feedback + D1 board review + 3 more closes
- **PM feedback (durable)**: I suggest stopping too much ("natural wrap point") — wearisome. Refined rule: PM decides *when* to stop; legit pauses = (a) need PM to decide *what* next, (b) PM says stop, (c) genuinely *my* capacity/context/focus. Time-of-day/session-length are NOT reasons. → memory `feedback_dont_suggest_stopping_default_to_continuing` + MEMORY.md index.
- **"Board lag" mischaracterization corrected** (PM caught it): closing an issue auto-flips board Status→Done, so there's NO lag — #1236/#1268/#1271 were open because I shipped the work but never *closed the issues*, not because the board was stale. Owned it.
- **D1 board review** (project #1, Sprint="D1 - Beta design quality"): 34 items, 21→24 Done. Pulled all + reconciled vs real GitHub state.
- **Closed properly this turn**: **#1225** (collapse/dismiss, UAT'd) · **#1268** (nav coverage — Lists reachable + CXO IA reconciled; Documents-merge → #1270) · **#1271** (nav.css extraction + 10 one-offs; broader <style>-lint → #1251 item-2).
- **Verify-first PREVENTED 2 over-closes**: **#1236** NOT closeable (its "entity-search subsumes chat-search" AC is unmet — search still conversation-only = the CXO search-scope item) · **#1169** NOT closeable (child **#1149** DEBUG-ROUTE-PROD-EXPOSURE still OPEN — a security verify). #1251 stays open (item-2 CXO).
- **#1269 design-pass kicked off**: memos written to CXO (experience) + PPM (connected-data model), cc PM — committed `b14a15ce3` on the main-checkout local main, but **push to origin is queued behind a multi-agent pile-up** (comms agent's uncommitted cross-pollination brief + a cxo migration-handoff commit on top of mine) — NOT clobbering active work; rides out on next main push / merge-keeper. **Kickoff recorded on #1269 via gh** (visible now regardless).
- **D1 OPEN tail (10)**: CXO-gated — #1236 (search), #1251 (item-2), #1269-experience, + #3 composition · PPM-gated — #1240, #1270, #1269-data · #1257-gated — #1164 · umbrellas — #1090, #1237 · unblocked Lead tail — **#1149** (debug-route prod-exposure, security verify, under #1169) + #1202 (files follow-on, M5-ish).
- **NEXT (unblocked Lead work)**: #1149 (security — verify debug routes aren't prod-exposed; the one open #1169 child).
