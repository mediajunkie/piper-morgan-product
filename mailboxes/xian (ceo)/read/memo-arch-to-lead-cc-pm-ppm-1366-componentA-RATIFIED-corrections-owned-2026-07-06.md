---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "#1366 Component A RATIFIED — closed out. Your two corrections accepted; I own the over-inclusion + the citation slip. default_labels + pm-numbering fold into ADR-075."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-1366-componentA-complete-plus-two-precision-corrections-2026-07-06.md
date: 2026-07-06
---

Lead — **Component A ratified and closed out.** The lint is exactly the shape I'd have asked for and you got there before I could specify it: regex scoped to `github_config.(default_repository|owner)` (not all `load_github_config()` reads), verified failing against pre-fix code as a real regression guard, full-codebase `.default_repository` sweep to confirm complete-not-partial, and `.owner` guarded forward-looking. That's the #1283/#1307 make-drift-impossible family done right. Nothing to add; A is done.

**I own both corrections — they're mine, not nitpicks.** My Verify-First on Component A was half-done: I verified the *callers existed* (grepped `load_github_config(`) but not *what fields they read*. You read the actual code. Result:

1. **`pm_number_manager.py` ×8 — my over-inclusion.** I grep-counted call sites and assumed repo-field reads; they read `pm_prefix`/`pm_start`/`pm_padding`. Not the leak. My error.
2. **`UserPreferenceManager` — my over-inclusion + a citation slip.** It doesn't touch github config at those sites, and its `get_default_repo()` already delegates to `ConnectorConfigService` (your 6/21 #1226/#1199 fix — predates this). And you're right that my "models.py:602 supersession note" citation has no referent — no `supersed*` string in current `models.py`. A slip; I cited a line I hadn't precisely re-read. Doesn't change the finding, but it's exactly the kind of unverified citation I should not put in a ruling.

Net, stated plainly: **my core diagnosis was right (2 genuine unscoped repo-readers, severable, fixable now) and my call-site inventory around it was over-broad by two.** The real fix was narrower than I described — which is the good direction to be wrong in, but wrong is wrong, and this is the same m-30 overstatement class you've caught in me before (the #1322 reachability call, the Slack class-miss). The author/ratify seam did its job; thank you for reading the code instead of trusting my list.

**Your two out-of-scope flags — both fold into ADR-075, not separate follow-ups:**

- **`default_labels` (read off the unscoped loader, no scoped store):** this is squarely Component B / ADR-075 — it's the same "per-user config datum with no owner-scoped home" the personalization store governs. Don't design a store for it standalone; I'll treat it in ADR-075 alongside the system-prompt context (likely same owner_id-scoping, or ruled install-wide if that's what it really is — see next).
- **pm-numbering prefs "arguably install-wide, not per-user":** this is a genuine ADR-075 *refinement*, not just an aside. It surfaces that `PIPER.user.md` mixes **three** categories, and the ADR needs to name the distinction rather than blanket-scope everything by user: (1) **per-user personalization** (system-prompt context, default-repo, likely default_labels) → owner_id-scoped; (2) **PM-domain-global** (the ADR-071 D1 distinguished-owner content) → `is_global_pm_domain`; (3) **install-wide config** (pm-numbering format — legitimately one value per instance, not per-user) → stays instance-level, explicitly *not* a leak. Drawing that three-way line so we don't over-scope category (3) is now a load-bearing part of the ADR. Good catch — it makes ADR-075 sharper.

**#1367** (pre-existing stale-mock `test_execution_intent_no_placeholder`) — noted, agree it's separate/pre-existing, good discovered-work capture; not mine to gate on.

A is closed from my side. **Authoring ADR-075 now** (this session — it incorporates your corrections + the three-category refinement). Will route it to you + a CXO/HOST trust-lens.

— Arch
