# Ship #050 draft — full fact-check (2026-07-08, PM-directed)

**Trigger**: PM caught the headline claim ("The first real user" / Jake Krajewski successfully installed and used the plugin) as a real overstatement — Jake's Claude UI never showed the install entry point (the "+"), it was never resolved, and no successful install was ever confirmed. PM directed a full fact-check of every remaining claim.

**Method**: every claim in the draft traced to its primary source and graded by evidence tier:
- **T1 — PM-witnessed**: PM personally saw/did it live
- **T2 — artifact-attested**: commit, test output, closed issue, or published URL
- **T3 — log-asserted**: stated in a session/omnibus log but not independently verifiable from an artifact
- **T4 — inferred**: cross-referenced or deduced, no direct witness or artifact

The Jake error was a **T4 dressed as T3**: PA had no Jun 26 session log, so Exec's cloud-session inference ("actively using it") became the omnibus's assertion, which downstream verification then treated as ground truth. Provenance: `dev/2026/06/26/2026-06-26-0702-exec-code-sonnet-log.md` (13:02 entry) → Jun 26 omnibus ("Content inferred from Exec cross-refs" — the caveat was even present, and got dropped in transit) → Ship draft. Lesson applied below: claims resting only on T3/T4 get softened or cut.

## Claim-by-claim

| # | Draft claim | Verdict | Evidence |
|---|---|---|---|
| 1 | Jake Krajewski installed the plugin and started using it ("first real user") | **CORRECTED — false** | PM direct knowledge (7/8): install never succeeded, UI lacked the "+" entry point, unresolved. Corroborated: glossary v1.1 (plugin distributed to Jake **Jun 9**, "early/buggy; Caddy auth issues" — so Jun 26 wasn't even first contact); HOST carry-forward ("Jake Krajewski + Rebecca Refoy (setup-friction-blocked)", re-ping wave); HOST 7/6 batch-1 memo (his email still "unconfirmed"). **True in-window claim**: his install-*attempt* feedback on Jun 26 drove three same-day plugin releases (v0.1.4→v0.1.6, incl. a real packaging fix), continuing to v0.1.8 Jun 27 (T2 — versions exist). The feedback loop is real; the working install is not. |
| 2 | Piper claimed "Milestone created" when nothing was created; fixed same day | **REPHRASED — timing** | Caught Jun 29 in live use (T1 — PM's own floor incident); the floor hardening landed **Jun 30** (T2 — roadmap v18.3 changelog: "#1331, Jun 30"), so "within a day," not "same day." Honest-decline rule is real (T2, `conversational_floor.py`). |
| 3 | Conversational set-default-repo | **VERIFIED** | T1 — PM live-tested Jun 29 ("bingo" logged). |
| 4 | GitHub "connected but 401" contradiction fixed | **VERIFIED** | T2 — #1329 closed Jun 29. |
| 5 | GitHub connector real, live-verified with 179 actual issues | **VERIFIED** | T1+T2 — PM's own OAuth round-trip Jun 27; real github-mcp-server v1.5.0; 179 issues pulled live. Strongest claim in the draft. |
| 6 | Calendar connector on the same shared contract | **VERIFIED, scope-noted** | T2 — Jun 27, all 4 protocol methods, 7 tests. Reuses pre-existing Calendar OAuth (#529/#843); the in-window new thing is the port to the shared contract. No GitHub-style live verification in-window — draft phrasing kept modest. |
| 7 | Security gap (#1343) found and fixed same week | **VERIFIED, tightened** | T2 — found Jul 1, deployed Jul 2 as v0.8.9.1 (tagged release). Now phrased "found one day, deployed the next" — stronger AND more accurate. |
| 8 | Freeze-check auto-derived thresholds | **VERIFIED** | T2 — Jun 26, `0b60719e7`, 5/5 tests. |
| 9 | Version-consistency script wired into release runbook | **VERIFIED** | T2 — Jul 2, after real VERSION drift found. |
| 10 | Auto-wake attempt built, failed, retired "the same day" | **REPHRASED — timing** | T2 — built Jun 27, self-validated FAILED Jun 28 morning, disabled Jun 28. Retirement was same-day *as the failure*, not as the build. Now: "proven unreliable by its own self-test the next morning, and retired on the spot." |
| 11 | Arch owning the instantiated≠called misjudgment | **VERIFIED** | T2/T3 — Jun 27 ruling, Jun 28 correction after Lead's call-graph trace; owned in writing. |
| 12 | Cohort-wide throttle in one day | **VERIFIED** | T3 (multiple independent logs) — Jun 28, 10/10 roles, false-alarm interaction caught same session. |
| 13 | Five publications with titles/dates/URLs | **VERIFIED** | T2 — all five checked against editorial-calendar CSV + the published drafts themselves (Jun 27, 29, 30, Jul 1, Jul 2). |
| 14 | 25 issues closed | **VERIFIED** | T2 — `gh issue list --search "closed:2026-06-26..2026-07-02"` → 25. (Caveat: GitHub's closed-date search runs on UTC; ±1 at window edges possible. "25" kept, not rounded up.) |
| 15 | "Milestone dates confirmed" | **REPHRASED — trap avoided** | The in-window event (Jun 27, T1) set beta = Aug 1 / production = Oct 30. But Aug 1 was **dropped entirely on Jul 4-5** — publishing "dates confirmed" today would assert something known-stale. Reframed to the durable part: the version↔milestone ladder (beta ships as 0.9.0, production as 1.0). |
| 16 | No-destructive-git rule ratified | **VERIFIED** | T2 — ADR-073, Jun 27. |
| 17 | Open-registration gap "in hand, not yet shipped as of week close" | **VERIFIED** | T2 — #1344 found Jul 1, PM direction arrived Jul 2, fix built/deployed Jul 3 (out-of-window, correctly excluded). |
| — | Slack onboarding flow (#1201) — **was MISSING from the rebuilt draft** | **ADDED** | T2 — CXO spec (Jun 30) → Lead built and closed **Jul 1**, in-window. Dropped by accident in the window-correction rebuild; restored. |

## Net changes to the draft

1. Theme replaced: ~~"The first real user"~~ → **"The connector gets real"** (recommended; PM approves themes). Headline now rests on the draft's strongest-tier claim (T1+T2).
2. Jake reframed honestly: failed install that produced three same-day fixes and an unresolved mystery — the feedback loop as the win, the install experience as the named gap. No "user," no "using it."
3. Slack onboarding restored (verified, in-window, wrongly dropped).
4. Three timing/phrasing tightenings (#2, #10, #15 above).
5. P.S. rewritten to match the corrected story (PM voice-passes regardless).

## Process notes

- The draft was **prematurely routed to Comms** before PM's read — retracted by HOLD memo (`memo-exec-to-comms-cc-pm-HOLD-ship050-review-retracted-2026-07-08.md`). PM gates the handoff to Comms; `draft-weekly-ship` amended to v1.4 to encode this.
- Evidence-tier discipline going forward: any Ship claim resting solely on T3/T4 (log-asserted or inferred, no artifact and no PM witness) gets softened, attributed, or cut. The omnibus is the fact-check *baseline*, not the fact-check *ceiling* — this incident proves an omnibus can inherit an inference and print it as fact.
