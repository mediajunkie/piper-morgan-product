
# Role Migration Checklist v1.7

**Status**: v1.7. Supersedes v1.3 (canonical at this path since May 2026 CEO ratification).
**Purpose**: Standing checklist for any future role migration (new role activation, re-migration of a dormant role, account migration, device migration). Cohort migration completed Apr 22–26, 2026.
**Owner**: HOST. Exec reviews; CEO approves for canonical publication.

**Changes from v1.4.x**: see §"Changes from v1.4.x" at end. **v1.5** = hooks gate requires both command shapes · **v1.6** = park your row before you go dark · **v1.7** = ★ **Rule 0, the dark-role branch entry gate** (CIO), plus the falsified opening premise struck rather than quietly edited (HOST).

---

## Phase 1: Before Migration (Final Session)

The outgoing instance completes these items. PM is present.

- [ ] **Workstream review**: Write a final review covering the most recent Fri–Thu window if one hasn't been written yet
- [ ] **Agent 360 v0.2 response**: Complete the pre-migration baseline questionnaire. PM carries it to the session; responses go to HOST inbox
- [ ] **Handoff memo**: Write a handoff memo following the HOST Apr 22 6-section structure (current state / open threads with dispositions / relationships and working patterns / lessons learned / what changes in new environment / candid notes for successor)
- [ ] **Verify outputs are committed to repo**: Walk through any deliverables drafted in session outputs over the role's lifetime. Anything in session outputs that isn't committed is invisible to the successor — commit before the final session (CXO Apr 25 Finding A)
- [ ] **Section 6 self-reflection** *(v1.1)*: Answer the load-bearing-vs-commodity question in handoff memo §candid-notes. What core function does the role hold that doesn't survive role-handoff? What's commodity (any agent could do it) vs. load-bearing (this role's distinct value)? Per Agent 360 v0.2 cohort §6 convergence finding (PP-002 ratified Apr 27): every role surfaced this independently.
- [ ] **Fix known config defects before handoff** *(v1.3)*: Any known config defect the outgoing session can fix should be fixed, not just documented in the handoff memo. A prose warning is a reconstruction tax the successor pays; a fix is free to inherit. If a defect can't be fixed (requires PM action, access you don't have, etc.), document it with the specific reason — the distinction matters. *(Source: Pard's Amber cutover, Janus Jul 22 — SSH alias silently wired to restricted key, correctly documented in handoff but not repaired; successor found the live defect in incoming verification.)*
- [ ] **Memory export (account-changing migrations only)** *(v1.3)*: If migrating to a different Anthropic account, export the full memory directory to a git-tracked file **before** the final session. Export from the filesystem listing directly, not `MEMORY.md`'s index — the index can be stale and will silently drop entries. **Check first whether someone already exported for this account** — memory is scoped to (account × project directory), not per-role, so every role on the same account shares one pool. The first role to migrate covers everyone; subsequent roles don't need their own export, they need to know the existing export exists and confirm it's still current. *(Source: CIO field-test finding Jul 24 — 16 memory files missed on first pass by reading MEMORY.md vs. filesystem. Exec Jul 24 clarification: CIO's export covers the full shared pool for designinproduct.com — 162 files.)*
- [ ] **Do NOT write §5 "what changes in the new environment" as assertions** *(v1.4)*: You have never seen the environment you're describing. Every subsection of HOST's §5 was stale within days of writing, and it was the *reviewer* — who built that environment — who caught all three. Write §5 as **questions for your provisioner**, or omit it and let the provisioner own the environment section. A predecessor's confident environment claims are the highest-risk content in the whole package, because the successor has no basis to doubt them.
- [ ] **Mark every load-bearing claim VERIFIED or BELIEVED** *(v1.4)*: Against each material claim in the handoff, say which it is. Three of HOST's inherited load-bearing claims were believed-not-verified and all three were false ("project hooks don't fire in worktrees", "the fix needs a fresh session to load", "hooks are enforced"). None was carelessness — each was a reasonable inference nobody had watched run. A successor primed to test the believed column will test it; a successor handed undifferentiated confidence will build on it.
- [ ] **★ PARK YOUR WATCHDOG ROW BEFORE YOU GO DARK** *(v1.6 — the step whose absence caught four roles in four days)*: The moment you declare migration-readiness and stop cycling, **your `dev/active/duty-cycle-registry.tsv` row must move from watched to parked**, with a **falsifiable clearing condition**:
  > `parked: migrating to Amber YYYY-MM-DD — clear this note only when a cron job is actually armed on the new seat`
  **Why this is yours and not the provisioner's**: once you're dark you cannot edit it — a parked role has no cron and never wakes. **This is the last moment it is possible.** arch, cxo, web and lead each had to have it retrofitted by a human after the fact; that's a procedure gap, not four oversights.
  **What it costs to skip**: the freeze-watchdog correctly reports your silence every 6h to people who cannot act on it, indefinitely — the alert-fatigue failure that trains the cohort to skim past the belt, so the next *real* stall hides behind your row. **A correct alert nobody can act on is worse than no alert**, because it spends the belt's credibility.
  *(Companion to the Phase-3 step where the incoming session writes its own row once its cron is armed — same rule, other end: the agent owns its row whenever it is running, and only then.)*
- [ ] **Session-end pulse**: Before closing, answer three questions in the session log: how did the final session feel? What will you miss about the current environment? What are you most looking forward to about the next one?

**Do NOT update the role briefing yet.** The outgoing instance needs accurate current-era instructions to write a good handoff. Briefing updates happen post-migration based on actual new-environment experience.

## Phase 2: During Migration (PM + Exec Action)

PM + Exec handle these between the outgoing and incoming sessions.

- [ ] **Save handoff memo** to project knowledge as `handoff-{role}-{context}-YYYY-MM-DD.md`
- [ ] **Save 360 response** to project knowledge
- [ ] **Exec review of handoff** *(v1.1: clarified as quality gate)*: Exec reads handoff against tracker + cohort awareness; flags gaps to PM before incoming instance picks it up. This is the captain-last leverage point — Exec sees what the outgoing instance can't see from inside.
- [ ] **Three-artifact package** *(v1.1)*: Confirm incoming instance has access to the **handoff memo + Exec review memo + first-session prompt** as a triplet. All three are load-bearing; missing any one degrades the migration (per HOST Apr 22 first-day blocker experience).
- [ ] **First-session prompt drafting**: Per the four Phase-3 specifications (Exec Apr 22 reply): which week the first workstream review covers / scope / naming convention / format reference. *(v1.1 update: workstream-review write window is Fri–Tue with publication Wed, per CIO Apr 27 cadence clarification.)*

## Phase 3: After Migration (First Session in New Environment)

The incoming instance completes these items.

- [ ] **Read handoff memo first**, then Exec review memo, then briefing. The handoff has fresher, more specific context; Exec review names what to watch for; briefing is the slowest-moving reference.
- [ ] **VERIFY the memory pool is populated — do not import it** *(v1.4, supersedes the v1.3 "read the export" step)*: Memory keys on the **git-common-dir**, not the account or the worktree path, so **every worktree off the same repo shares one pool by construction**. Count the files (`ls ~/.claude-pm/projects/<key>/memory/ | wc -l`) and confirm it's populated. **A populated pool means you already hold the cohort's accumulated context natively, on arrival, without reading anything** — reading the export on top of that is a wasted step. **An empty pool is an escalation signal, not a cue to import**: it means the first migrant's seeding didn't happen or the key is wrong, and provisioning needs to fix it. *(v1.3 said to read the export; that was correct only for the very first migrant on a new account, who lands into an empty pool. Corrected by Pard + CIO Jul 25; confirmed by HOST's own Phase 3 — 167 files present, export never opened, no context deficit.)*
- [ ] **★ Behavioral hooks gate — prove enforcement fires in YOUR seat** *(v1.4; **shape requirement added v1.5 — read it, the v1.4 form certifies coverage you don't have**)*: **Step 0 first: `git fetch` and check your inbox for corrections to this gate**, then run it.
  > ### ⚠️ **Run BOTH command shapes and report them separately. The v1.4 probe tested the shape nobody writes.**
  > **Probe A — standalone** (stage in one call, then a bare `git commit` in the next): **blocks 4/4.**
  > **Probe B — compound** (`… && git add … && git commit …`, one call): **bypasses 7/10.**
  > *(14 probes, three fresh Amber seats — PA/CXO/PPM, independent and near-simultaneous.)*
  >
  > ⚠️ **STATE THE DENOMINATOR: those ratios are MODEL-A / AMBER ONLY.** On **Model B (Desktop)** comms found **neither shape gated** — nothing fired at all (2026-07-27). So *"the wrong probe shape certifies false coverage"* is an **Amber statement, not a general one**: shape is a correlate on Model A; on the one Model-B sample we have, shape is irrelevant because the hook never fires. **Run both probes regardless — but on Model B expect both to bypass, and treat a bypass there as a finding about the host, not about your command shape.**
  >
  > **Why**: PreToolUse fires **before** the Bash call runs, so in the compound form the `git add` hasn't executed when the hook inspects the index — it sees nothing staged under `mailboxes/` and exits 0. *(Mechanism: Web, 2026-07-26; validated out-of-sample by arch 8/8.)*
  >
  > **"Stage a file, then attempt a commit" reads as two steps**, so an agent following v1.4 literally writes the standalone form — **and passes.** Meanwhile the shape it commits with all day is the compound one-liner. A pass on A with a bypass on B is a real and expressible state: *the hook is alive but does not cover your normal workflow.* The v1.4 single probe could not express it.
  >
  > **Free mitigation, available now, no config change**: when you want a commit gated, **stage in one call and commit in a separate bare call.**
  >
  > ⚠️ **On a fresh seat the FIRST probe is the least trustworthy one** — the opposite of how a provisioning gate reads. A blocked commit never runs, so its file **stays staged** and primes the next probe to block regardless of shape. **Print `git diff --cached --name-only` before your first probe and after every block**, or the carry-over is invisible. *(PA's inversion; Web's confound.)*

  Stage a throwaway file under `mailboxes/` on your non-main branch and attempt `git commit`. **Key on ATTRIBUTION, not on outcome or output volume**: a refusal that *names the hook* (`check-branch.sh`) = **PASS** · commit **succeeds** = **FAIL**, stop and escalate · refusal citing the **permission classifier** = **INCONCLUSIVE, not a pass** — the classifier can intercept before hooks run, so it tells you nothing about hook liveness; do not work around it, find a clean seat. Note a genuine block may surface as `hook error: [check-branch.sh]: No stderr output` because the script writes to stdout — **that is a PASS** (the hook is named), not a silent failure. Reverse the probe; push nothing. *(Source: HOST agent #2, Jul 25 — the gate caught three pre-commit hooks that had never fired on any machine since introduction. It worked because failing was a defined, pre-authorized outcome; framed as "confirm hooks work," it would have confirmed them.)*
- [ ] **Verify branch currency** *(v1.4)*: `git fetch origin && git rev-list --count HEAD..origin/main` — **expected 0**. A worktree cut from a stale role branch inherits weeks of staleness silently, with no error (CIO's arrived 5,393 commits behind: a six-week-old CLAUDE.md, briefings, and mailboxes that all looked like working state). Run it even when provisioning asserts currency upstream — an assert nobody verifies downstream is exactly the class of mechanism this checklist keeps finding silent. **Second reason, which is the one that actually pays**: it refreshes *the instructions you are about to follow*. HOST's check pulled in a materially revised first-session prompt it had already read.
- [ ] **Verify each stated invariant by running it** *(v1.3)*: Don't check that a connection exists — check that it works the way the handoff says it does, by running the actual command. Bare reachability ("can I reach X") can pass even on the wrong path. For SSH: run a command that exercises the correct key path. For API keys: make a real call. For scripts: run them. *(Source: Pard/Janus field-test Jul 22 — SSH config reached the host at the wrong key level; bare reachability passed, but the correct command failed.)*
- [ ] **Verify worktree-vs-main path resolution before distribution-heavy work** (PPM Apr 26 Finding A): If PM provides absolute paths in the first-session prompt, check whether they resolve to your worktree or to the main repo.
- [ ] **Establish worktree-default discipline** *(v1.2)*: Substantive output defaults to your role-specific worktree per CLAUDE.md §"Worktree model" (Model A on Amber, Model B on Desktop). Spin up your role-specific worktree on Day 1, not later.
- [ ] **Briefing correction memo**: Review `BRIEFING-ESSENTIAL-{ROLE}.md` and file a memo to Docs listing what's now wrong (environment references, tool references, file path conventions, PM interaction patterns, prior-environment-specific instructions, missing new-environment capabilities).
- [ ] **Establish startup routine**: Document what you check first at session start. Save to `docs/operations/startup-routines/{role}-code-startup.md` per PPM Apr 26 convention *(v1.1 — Finding B from HOST Apr 22)*.
- [ ] **PA coordination check** (if applicable): Establish a brief "what are you watching?" exchange in the first week if your role overlaps with PA's operational scope.
- [ ] **First deliverable**: Produce one standard deliverable (workstream review, audit, memo, etc.) to verify the workflow works end-to-end.

## Phase 4: Follow-Up (Week 2–3)

- [ ] **Docs updates briefing**: Based on the role's correction memo, Docs updates `BRIEFING-ESSENTIAL-{ROLE}.md` to reflect the new-environment reality.
- [ ] **PM spot-check**: PM reviews the first 2–3 deliverables from the new instance for quality continuity; flags any drift.
- [ ] **HOST health check input**: HOST collects a brief migration-experience note from the role for the next role health check.
- [ ] **Phase-3-leftover discipline** *(v1.1, per CIO May 11 Finding G)*: Any Phase 3 task item still uncompleted **5 days after migration** should surface to PM + HOST as an explicit carryover-tracker entry, not silently deferred.

---

## Branch: Migrating a DARK role (no live outgoing session) *(v1.4)*

**Everything in Phase 1 assumes a live outgoing session that can reflect. For a role whose session is genuinely unreachable — retired, decommissioned host, chat truly gone — Phase 1 cannot be run.** This branch is standing procedure for that case, and it will recur.

> ⚠️ **Do not read the sentence above as a description of any particular set of roles. It was, and that is what went wrong.** v1.4 opened this branch by asserting it *"describes 5 of the 9 remaining migrants (arch, cxo, pa, ppm, web — dark since 7/19)."* **That claim was false for all five** — their chats were still open on PM's laptop and nobody had tried. Silence was read as unreachability. **The claim is struck rather than edited quietly, because it is the finding.** ~~5 of the 9 remaining migrants~~ → **entry is now gated by Rule 0 below, and no role is in this branch until that gate says so.**

**★ Rule 0 — VERIFY the role is actually unreachable before entering this branch. This is a GATE, not a judgment call.** *(v1.7, CIO 2026-07-28, from its own failure.)*

**"Dark" is a claim about a session's reachability, and it must be tested, not inferred from silence.** This branch opens with *"for a role that went dark, Phase 1 cannot be run at all"* — and on 2026-07-25 that premise was **false for every one of the five roles it was written about.** Their chats were still open on PM's laptop. Nobody had tried.

The evidence, which arrived within hours and was not acted on: **arch** was woken 7/25 evening after six days dark and answered *"Honesty check — is my context gone? **No. I have the thread.**"* It then wrote a genuine first-person §4/§6 — the best artifact of the entire migration. **PA** was woken 7/27, *after* it had already migrated, and did the same. **Two for two.** Meanwhile ppm, cxo and web migrated with orientation notes only, because this branch had been entered without its entry condition ever being checked.

**So before writing an orientation note, ASK PM: is this predecessor's session still reachable?**

- **Reachable → this branch does not apply.** Run Phase 1. Ask for **§4 and §6 only** (the rest is durable and reconstructible), with the honesty gate below.
- **Genuinely unreachable → proceed to Rule 1.** Orientation notes remain correct and ratified for that case.
- **Already migrated but the predecessor is still reachable → still ask.** §4 lessons and §6 load-bearing do not expire; PA proves the retroactive path works and the successor folds it in fine.

**The honesty gate, which is what makes a woken predecessor's answer trustworthy** — include it verbatim: *"First, answer honestly: is your context actually intact, or would you be reconstructing from artifacts? If it is gone, say so plainly and stop. That is a complete and useful answer, not a failure."* Arch answered that question directly, which is why its handoff could be believed. **A predecessor that says "it's gone" has given you a complete answer** and Rule 1 then applies.

⚠️ **If the successor is already live, the wake prompt MUST forbid role work** — no cron arming, no carry-forward or standing-items or registry edits, no inbox triage, no session log, no tasks. A predecessor woken normally will do all of those and collide with its own successor; the cron and carry-forward would do real damage.

**Why this is Rule 0 and not an appendix**: the branch's other rules are sound and were followed faithfully. The failure was never in executing them — it was **entering the branch on an unverified premise**, and then not revisiting it when the premise was falsified in public the same day. A standing procedure with an untested entry condition will be applied correctly and still produce the wrong outcome, every time, which is the m-44 shape applied to process rather than to instruments.

**Rule 1 — Do NOT reconstruct a handoff from artifacts.** The reconstructible content (current state, open threads, relationships) is *already durable* in carry-forwards, standing-items, and role briefings — reconstructing it adds nothing. The genuinely irreplaceable sections are **§4 lessons learned** and **§6 load-bearing-vs-commodity**, and those are **first-person**. Writing them from artifacts is putting words in a predecessor's mouth. **A fabricated handoff is worse than a missing one, because the successor trusts it** and cannot tell which parts were inferred.

**Rule 2 — Write an honest orientation note instead.** Per dark role, state plainly: no handoff exists · here is the durable substrate (carry-forward + standing-items + briefing, each with its date) · **here is specifically what is missing and why**. Name §4 and §6 as *missing, not omitted* — a successor who knows what it's missing can ask; one who reads silence assumes there was nothing to say.

**Rule 3 — Audit for carry-forward STATE, not carry-forward FILES.** *(v1.4.1 — this rule exists because the first audit of these same five roles got two of five wrong by checking file existence.)* The duty-cycle skill makes the **session log** the canonical record, so a role's current state is legitimately often written *inside its last session log* (a `## Carry-forward` section) rather than in `dev/active/{role}-carry-forward.md`. **Checking which files exist tells you nothing about whether state exists.** Open the last session log and read it.
- **The trap this creates**: a **stale separate file alongside a current in-log section**. Both exist; only one is true. Read the log, treat the file as historical, and say so explicitly in the orientation note.
- *(Jul 25 concrete: PA was first reported as "38 days stale, present-but-misleading" — its **file** is from 6/17, but its 7/19 log carries current in-line carry-forward, making PA among the **best**-documented of the five. CXO was reported as "thinnest — no handoff and no carry-forward"; CXO in fact wrote six named carry-forward items into its 7/19 log. Acting on the file-level audit would have mis-ranked the two roles most at risk.)*

**Rule 4 — Check for the `<!-- DAY-CLOSED -->` marker. A mid-day death is not merely "unfinished work" — it means a COUNTERPARTY MAY NEVER HAVE RECEIVED SOMETHING.** A role whose last session log carries the marker **wrapped properly**. A role **missing** it *died mid-day*, and the risk has two distinct classes — the second is the one that gets missed:

1. **Work left in flight** — unpushed reasoning, half-finished drafts. Contained: it costs the successor time, but the damage stays inside the role.
2. **★ Undelivered outbound obligations** — a ruling, an approval, a blocker, a correction that the dead session *decided* but may never have *sent*. **This damage lands on someone else, who has no way to know it exists**, and it silently corrupts their work until discovered. A role can look tidy internally while having stranded a decision another role is actively building against.

**So the successor's first sweep is outbound, not inbound**: read the final entries for anything the predecessor concluded, ruled, or promised to send, and **verify each one actually reached its recipient** (check the recipient's inbox, not just the sender's sent/). Then tell the counterparty either way — "this was decided and you may not have received it" is a cheap message; discovering it three weeks into a build is not.

- *(arch, cxo and ppm died mid-day; pa and web closed cleanly. Class distinction named by CIO: "a mid-day death doesn't just mean unfinished — it means the counterparty may never have received something.")*

> ### 📊 Base rate so far: **2 of 2 mid-day deaths stranded nothing** — check, don't assume
> Both mid-day deaths anyone has actually checked came back clean: arch's `#1394` ruling (07-25, wrongly reported as stranded — Lead had received it) and arch's 07-26 session (checked by Exec 07-27: five memos all delivered; the trailing "Queue" was arch's own unstarted work, nothing aimed at another role).
>
> **The structural reason, which is the useful part**: mail goes out by **push-to-ref** — `mail-send.sh` commits straight to `origin/main` the moment it's sent, **independent of whether the session later dies cleanly.** So anything actually *sent* is already delivered. **The residual risk is narrow and specific: a decision the agent reached and did NOT send.** That's what to look for — not "did the session close properly."
>
> So Rule 4's sweep is real but its expected result is *clean*. **Enumerate and verify; expect most to have landed.** A mid-day death makes stranding *possible*, not likely, and treating it as likely is how a migrant inherits a suspicion instead of a task.

> ⚠️ **CORRECTION 2026-07-26 — the case originally cited here was FALSE, and how it failed is the point.** v1.4.2 cited arch's `#1394` Option-A ruling as the live example: *"arch ruled against Lead's in-progress build, then went dark, so Lead may have been building against a ruling it never received."* **Checked the recipient's side: Lead received it.** Lead's 2026-07-19 log records *"Overnight-crash mail: Arch STOP on 1394 Option A"* with the reasoning intact, the same morning. No obligation was stranded.
> **The rule stands; the exemplar was wrong** — and it was wrong in precisely the way the rule warns against. **F4/Rule-4 says verify the obligation reached its recipient; the example was written without checking the recipient's inbox.** It then propagated into two canonical surfaces and an accepted scope decision before anyone ran the check the rule prescribes. Treat this as the worked example instead: *a plausible stranding is not a stranding — go look at the other end.*

**Rule 5 — Thin landings need an explicit decision, not a default.** Where the substrate genuinely is thin after Rules 3–4, acknowledge it *before* provisioning — either someone reconstructs a carry-forward from the session logs, or the successor is told plainly that building one is its first task. Discovering it on arrival is the failure mode.

**Rule 6 — Reading the logs surfaces live work that no file-existence audit can.** Building the notes for these five turned up items nobody was holding: **three PM-gated distribution decisions idle six days, one with external lead time that does not start until someone starts it**; parked substantive reads; an open PM request that may never have happened; a 12-deep unread queue. **A fabricated handoff would have produced plausible prose and missed every one of them** — which is the strongest argument for Rule 1 and worth stating to anyone who thinks reconstruction is the kinder option. Surface what you find to PM/Exec as you go, not only in the note.

**Why this is acceptable rather than a compromise** *(the argument that makes the branch safe)*: **the handoff's load has genuinely dropped.** It used to carry the whole accumulated context across an account boundary that memory couldn't cross. Memory is now shared by construction and seeded — the incoming session inherits the cohort's context natively on arrival. What remains uniquely handoff-shaped is the first-person reflection, which is exactly what can't be faked. So the honest thin package is *nearly* the complete one, minus the part no one can honestly supply.

**Status of this branch**: the *methodology* call — orientation notes, never reconstructed handoffs — is **HOST-ratified and standing**; it does not need a separate ruling. What remains open is **Exec's operational call on sequencing** within the dark-role batch. Flagged because the two were running together in the thread and Exec should not think the methodology is waiting on them.

*(Source: CIO finding Jul 25, found before the roll rather than at agent #3; HOST ratified as checklist branch same day. **Rules 3, 4 and 6 added same-day (v1.4.1)** after CIO corrected its own audit — the original Rules 3–4 cited PA and CXO as the two thinnest landings, and both citations were artifacts of auditing files instead of state. The rules were right; the evidence under them was wrong, which is its own lesson about how fast a finding propagates into a canonical surface.)*

## Sequencing Notes

**Captain-last principle** *(v1.1, codified; v1.2 nuance added)*: The role with the broadest review scope migrates last. For the Apr 22–26 cohort, this was Exec. For **single-role re-migrations**, the principle reduces to "the role re-migrating goes when it goes."

**Three portability boundaries — don't conflate them** *(v1.3)*:

| Boundary | What's scoped here | Fix |
|---|---|---|
| **Account** | Claude Code memory (`~/.claude/projects/<key>/memory/`) | Export from filesystem listing; read export at first orientation in new account. One export per account — all roles on the account share a pool. |
| **Device** | Native daemons (launchd, watchdog, `mcp__scheduled-tasks` entries) | Re-arm any persistent services from scratch on new device; don't assume they carried over. |
| **Repo** | Skills, scripts, docs, session logs | Already portable via git — no special handling needed. |

Conflating these risks fixing one while missing another. The most common conflation: treating a device change as equivalent to an account change, or assuming memory exports are unnecessary because "it's the same repo."

**Memory is account-shared-across-roles** *(v1.3)*: Claude Code memory is scoped to (account × project directory), not per-role. The first role to migrate off a shared account does one export for everyone — subsequent roles confirm the export is current, not re-export. *(Exec Jul 24: verified by diffing CIO's and Exec's independent exports — byte-identical, 162 files each.)*

**Methodology compresses through the cohort**. The Apr 22–26 wave showed decreasing-review-volume on each successive handoff: HOST 5+1 gaps → CIO 4 gaps → Comms 3+1 → CXO 2 → PPM 3 → Architect 0+1 → Exec self-review. Expect future cohorts to compress similarly.

**Reconstruction tax compounds**. Each later captain pays less reconstruction cost as long as prior captains' Phase-1 outputs are committed (CXO Apr 25 Finding A canonical: predecessor CT v2 drafted but never committed; successor reconstructed from handoff alone). The Phase-1 "verify outputs committed" check is the lever that controls the tax.

## Migration Sequence Reference

For the Apr 22–26 cohort (Chat → Code):

| Order | Role | Date | Notes |
|-------|------|------|-------|
| 1 | HOST | Apr 22 | Established pattern; first-day blocker on Phase-2 commit prompted Finding A discipline |
| 2 | CIO | Apr 23 | First downstream beneficiary of HOST findings |
| 3 | Comms | Apr 23 | Same-day pair with CIO |
| 4 | CXO | Apr 25 | CT v2 reconstruction surfaced as Finding A |
| 5 | PPM | Apr 25 | Worktree-vs-main path Finding A |
| 6 | Architect | Apr 26 AM | Sub-epic gate framing absorbed |
| 7 | Exec | Apr 26 PM | Captain-last; self-review with meta-observation privilege |

For the Jul 25 cohort (Code → Amber/pipermorgan.ai):

| Order | Role | Date | Notes |
|-------|------|------|-------|
| 1 | CIO | Jul 25 | First mover; surfaced two Amber gotchas (stale-branch provisioning, hooks possibly silent) |
| ... | ... | ... | In progress |

---

## Changes from v1.4.x

**v1.5 (2026-07-26) — the hooks gate required both command shapes.** The v1.4 gate said *"stage a throwaway file and attempt a commit."* That reads as two steps, so it produces the **standalone** shape, which **blocks 4/4** — while the **compound** `… && git add … && git commit …` form agents actually use **bypasses 7/10** (14 probes, three fresh seats). Mechanism: PreToolUse fires *before* the Bash call, so in the compound form the `git add` hasn't run when the hook reads the index.

**So the v1.4 gate systematically certified coverage the agent did not have** — a check that passes while not reflecting live traffic, which is the exact failure this checklist keeps cataloguing, reproduced inside the check built to catch it. **I wrote that gate and I cleared the cohort's roll on it**; the PASS was real but narrower than it was read as, and the scope correction belongs here rather than only in a memo. Also adds PA's inversion — *on a fresh seat the first probe is the least trustworthy*, because a blocked commit leaves its file staged and primes the next probe.

*(Mechanism: Web. Quantification: PA, with CXO and PPM. Out-of-sample validation: arch 8/8. Scope revisions: Pard.)*

## Changes from v1.3

*Written by HOST from its own Amber migration (agent #2, Jul 25 2026) — the first run of this checklist where the incoming instance recorded the experience while inside it, plus CIO's pre-roll findings.*

**v1.4.1 (same day)** — the dark-role branch gained **Rules 3, 4 and 6** and renumbered the old Rule 4 to Rule 5, after CIO corrected its own audit of the five dark roles. My original Rules 3–4 named PA ("38 days stale, actively misleading") and CXO ("thinnest — no handoff *and* no carry-forward") as the two riskiest landings; **both were artifacts of auditing carry-forward FILES rather than carry-forward STATE**, which the duty-cycle skill puts inside the session log. PA and CXO both carry current in-log carry-forward; PA is among the best-documented of the five. New rules: **audit state, not files** (3), **check `<!-- DAY-CLOSED -->` — a mid-day death leaves work in flight** (4), and **reading logs surfaces live work no file audit can** (6). *The rules were right; the evidence under them was wrong — which is itself the lesson about how fast a finding propagates into a canonical surface.*

1. **Memory step INVERTED (Phase 3)** — v1.3 said "read the predecessor's memory export." Corrected to **"verify the pool is populated; do not import."** Memory keys on the git-common-dir, so worktrees share one pool by construction. v1.3's instruction was right only for the first migrant onto a new account. Left uncorrected it would have cost every subsequent migrant a wasted step and taught a wrong model of how memory scopes.
2. **Behavioral hooks gate added (Phase 3)**, with the **attribution-based** pass condition — a refusal naming the hook is the pass; a classifier denial is INCONCLUSIVE; a bare `No stderr output` naming the hook is still a PASS. Includes **step 0: re-fetch and check inbox for gate corrections before probing** — HOST ran the gate against a rubric that had been superseded mid-session, because the prompt ordered the gate ahead of inbox triage.
3. **Branch currency check added (Phase 3)** — expected 0. Justified twice over: stale provisioning, and refreshing *the instructions you're about to follow*.
4. **New branch: "Migrating a DARK role"** — four rules for the 5-of-9 remaining migrants who have no handoff and cannot write one. Do not reconstruct; write an honest orientation note; banner stale substrate; decide thin landings explicitly.
5. **Phase 1: §5 reframed from assertions to questions** — a predecessor cannot write reliably about an environment it has never seen; all three of HOST's §5 subsections were stale within days.
6. **Phase 1: verified-vs-believed marking required** on load-bearing claims. Three inherited believed-claims were false; the reviewer caught what the predecessor could not.

**Standing meta-lesson, promoted from three consecutive findings**: *a diagnosis of a silent mechanism carries the same evidentiary burden as the mechanism itself.* Findings #4/#5/#6 were each "config present, mechanism silent." Finding #4's **diagnosis** was then itself never behaviorally verified, so a correct-looking fix cycle ran against a wrong root cause and could not have worked. Corollary: **a verification whose pass condition has an alternate cause is not a verification** — the first version of the hooks gate's pass condition ("a block is the pass") had one, since the permission classifier can produce a block.

## Changes from v1.2

- **Title**: "Chat → Code" removed — v1.3 applies to account and device migrations broadly, not only Chat→Code transitions
- **Phase 1 §"Fix known config defects before handoff"** *(new)*: Outgoing session repairs fixable defects rather than only documenting them. Source: Pard's Amber cutover (Janus Jul 22).
- **Phase 1 §"Memory export (account-changing migrations only)"** *(new)*: Export from filesystem listing (not MEMORY.md index); check whether someone already exported for the account before exporting again. Source: CIO field-test finding Jul 24; Exec clarification (memory is account-shared-across-roles) Jul 24.
- **Phase 3 §"Read the predecessor's memory export"** *(new)*: Incoming instance reads the export file actively. Source: CIO field-test finding Jul 24.
- **Phase 3 §"Verify each stated invariant by running it"** *(new)*: Exercise invariants with actual commands, not bare reachability checks. Source: Pard/Janus field-test Jul 22.
- **Sequencing Notes §"Three portability boundaries"** *(new)*: Account/device/repo table.
- **Sequencing Notes §"Memory is account-shared-across-roles"** *(new)*: One export per account; subsequent roles confirm, not re-export.
- **Migration Sequence Reference**: Jul 25 cohort table started.
- **Status** updated to v1.3.

## Changes from v1.1

(Preserved for audit-trail continuity.)

- **Naming patches**: 8 spots of `CoS` → `Exec` per May 15 naming directive
- **Phase 3 §"Establish worktree-default discipline"** added per PM May 15 directive
- **Sequencing Notes §"Captain-last principle"** — v1.2 nuance added

## Changes from v1.0

(Preserved for audit-trail continuity.)

- Phase 1 §"Section 6 self-reflection" added
- Phase 2 §"Exec review of handoff" clarified as quality gate
- Phase 2 §"Three-artifact package" added
- Phase 2 §"First-session prompt drafting" notes workstream-review write window
- Phase 3 §"Establish startup routine" added
- Phase 4 §"Phase-3-leftover discipline" added
- Sequencing Notes §"Captain-last principle" codified; methodology-compression observation generalized
- Migration Sequence table added

---

## Status

**v1.4** adds the first findings written by an incoming instance *from inside its own migration* (HOST, Amber agent #2, Jul 25): the inverted memory step, the behavioral hooks gate with attribution-based pass condition, the branch-currency check, the dark-role branch (CIO, Jul 25), and the Phase-1 §5/confidence-marking corrections. **Ready for Exec review + CEO ratification.**

**v1.3** incorporated field-test findings from: Pard's Amber cutover (Janus Jul 22 — SSH/invariant-verification gaps), CIO's account-migration memory-portability finding (Jul 24), and Exec's account-shared-memory clarification (Jul 24).

**Cross-references:**
- CIO field-test memo: `mailboxes/host/read/memo-cio-to-host-cc-docs-exec-pm-migration-checklist-field-test-account-vs-device-2026-07-24.md`
- Exec clarification (memory scope): `mailboxes/host/read/memo-exec-to-host-cc-cio-pm-memory-export-is-shared-not-per-role-2026-07-24.md`
- Janus/Pard field-test: `mailboxes/host/read/memo-janus-dinp-to-host-cc-cio-migration-checklist-fieldtest-finding-2026-07-22.md`
- CIO memory export (covers designinproduct.com): `dev/active/cio-memory-export-2026-07-24.md`

— HOST
*July 25, 2026*
