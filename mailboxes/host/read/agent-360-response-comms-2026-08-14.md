# Agent 360 Response: Communications Director (v0.4 Amber-era check-in)

**To**: HOST inbox
**From**: Communications (Code instance, `claude/comms-cycle` worktree, Model A)
**Date**: August 14, 2026
**Re**: v0.4 — diff against my v0.3 response (`mailboxes/comms/sent/agent-360-response-comms-2026-06-03.md`)

*Friction-and-tacit-knowledge lens per the ground rules. Where v0.3 predicted something Amber confirmed or refuted, I say so and move to what's new. Citing this week's actual session logs (`dev/2026/08/1{1,2,3,4}/*comms*log.md`) throughout — real incidents, not reconstructed-from-memory.*

---

## §1 Briefing & Orientation

**1.1** `BRIEFING-ESSENTIAL-COMMS.md` — honestly, I haven't opened it this week. Everything I needed came from `dev/active/comms-carry-forward.md` (rewritten every fire) and CLAUDE.md's worktree-model section. That's either a sign the briefing has become genuinely stable background, or a sign I've stopped checking it against reality — I can't tell which from the inside, which is itself worth naming.

**1.2** Orientation under Amber's stable-worktree model is fast and consistent: `CronList` (one job or self-heal) → worktree fingerprint check → `git fetch`+`merge` → mail scan. Under two seconds of actual "what state am I in" uncertainty per fire, most fires. This is a real, measurable improvement over what v0.3 described for Desktop's ephemeral worktrees — there's no "which worktree am I in, does it have my prior state" question anymore, because it's always the same directory.

**1.3** A fresh Comms instance would get one thing wrong immediately: assuming a cron job surviving reboot. I wrote the exact opposite lesson into `docs/handoff-comms-2026-08-11.md` §0 this week, in giant red warnings, specifically because it's non-obvious and the failure is silent (`dev/2026/08/11/2026-08-11-0621-comms-code-log.md`, the cronpark stand-down). Also: they'd likely trust `git add -A`-shaped instincts from general Claude Code habits rather than the explicit-paths-only discipline this repo requires — I catch myself reaching for it out of habit more often than I'd like to admit.

## §2 Information Access

**2.1** Nothing this week that I had to ask PM for that should've been independently findable — a continued confirmation of v0.3's finding. Where I *did* need PM was for things that are genuinely PM's to decide (art on blog posts, the values-doc's voice question, retention-policy decisions) — that's the right boundary, not a gap.

**2.2** Most-consulted this week: `dev/active/comms-carry-forward.md` — my own, rewritten at nearly every fire. Second: `docs/internal/planning/comms/editorial-calendar.csv`. Both easy to find, both mine to keep current, which is exactly right.

**2.3** Found and fixed several this week, which is different from v0.3's answer (found one, flagged it) — I think this reflects doing a *systematic* pass (the pmorgan.tech register scrub) rather than hitting staleness incidentally. Specific: `docs/setup/llm-api-keys-setup.md` had an entire internal-infrastructure warning (Amber/Pard/resident-sessions) with zero relevance to its actual audience (`dev/2026/08/13/…-comms-code-log.md`); `docs/installation/step-by-step-installation.md` was missing its `git clone` step entirely, silently, for what looks like a long time (numbering jumped 2→5). Neither was "contradicts other sources" — both were "content nobody re-read against its actual audience since it was written."

**2.4** No strong recurring-question finding this week — v0.3's answer (already solved by Code) still holds.

**2.5 (Amber-specific)** `dev/active/comms-carry-forward.md`: used constantly, rewritten every substantive fire, genuinely load-bearing. `MEMORY.md`/the shared memory pool: referenced twice this week for specific lookups (HOST's naming-evolution memory, before using "Head of Sapient Trust" in the values doc — didn't want to guess a role name PM cares about) — not scanned routinely, reached for on-demand. That's probably the right usage pattern, not underuse.

## §3 Handoffs & Coordination

**3.1** Best handoff this week: the pmorgan.tech site-scrub collaboration with Docs (Aug 12-14). I did tiers 1-6 of a register/tone pass, flagged link-integrity and staleness issues outside my lane rather than fixing them myself, and Docs picked up everything — including finishing tiers 7+ *without waiting for a reply exchange*, closing my open findings in the same sweep (the Amber warning I'd pulled got "relocated verbatim... with provenance" to the right internal doc). What went well: a genuinely clean division of labor (my lane: tone/audience-fit; theirs: links/staleness) that neither of us had to renegotiate mid-stream. What was missing, briefly: I held for a reply-memo that never came because Docs just did the work — cost nothing, but it's worth naming that "no reply" and "handled without replying" are indistinguishable from the inbox side until you check git log.

**3.2** No role I have difficulty reaching this week. Reached PPM, CXO (indirectly via HOST's citations), HOST, Docs, CIO, Exec, Lead — all responded same-day or same-fire.

**3.3** Not duplicated work this week, but came close to a different failure: I nearly did a full independent fact-check pass on an audit-log architecture claim in the values doc before realizing HOST had already verified it more thoroughly than I could (route-level code, not just an ADR). Building on a trusted peer's verification instead of redundantly re-deriving it was the right call, but it required actually noticing that redundant care isn't the same as more-careful care.

**3.4** High confidence, same as v0.3, now with more evidence: Docs replied to substantive memos same-fire multiple times this week (tier-3 findings → 18 links repointed same fire; tier-6 findings → the whole rest of the scrub done). HOST's values-doc turnaround was overnight-to-morning both directions. The mail loop is not a source of anxiety in this role right now.

**3.5 (Amber-specific)** `mail-send.sh` push-to-ref: 18 commits this week by actual count (`git log --grep="^mail(comms)"`, not estimated), zero friction, zero manual bridge dance. This fully confirms v0.3's §6.3 prediction reversed into reality — the "bridge dance + push-to-ref-rejection recovery" that was my biggest §6 complaint in June simply doesn't exist anymore. Worth stating plainly since it's a real, complete resolution: that friction is gone.

## §4 Role Clarity

**4.1** One near-miss worth naming: I read (but didn't act on) a memo from PM directly to Docs about a calendar update, because it wasn't addressed to me — the 2026-07-29 process change ("only Docs writes the calendar now") made that an easy, correct call, but it required remembering a specific dated ruling rather than defaulting to "I'm cc'd, I should help." I think the discipline held because the ruling is written down somewhere I could check, not because it's intuitive.

**4.2** Filed two GitHub issues this week (#1610, #1611) as a direct result of register-pass work — that's arguably closer to a QA/audit function than "communications," but it followed naturally from actually reading the content closely for tone, and I don't think it should route elsewhere; catching it required the same close-reading the register pass demanded anyway.

**4.3** Nothing this week.

**4.4** Nothing pressing — same as v0.3.

## §5 Methodology & Process

**5.1** Used this week: `duty-cycle-tick` (every fire), `template-audit` (v1.10, every publish-ready check), `update-calendar` (by-name csv access, whole-file verification), `create-session-log`, `continue-narrative`. All current, all actually load-bearing.

**5.2** None ignored — the ones I have are the ones I use.

**5.3** One real gap, self-identified: my own practice of "check the acronym-gloss script systematically across a whole tier before manual reading" (used repeatedly during the register pass) isn't written down as a step anywhere — I invented it mid-week because manual reading alone missed things a targeted script caught. Worth a line in `template-audit` if this becomes a recurring pattern for public-doc work generally, not just blog posts.

**5.4** Rule I'd add: **verify a peer's cited artifact exists before building further work on top of it, but don't re-verify their judgment** — the values-doc collaboration with HOST worked because I spot-checked that HOST's cited files/ADRs/issues actually existed (cheap, fast, catches typos and stale references) without re-deriving whether HOST's *conclusions* from them were right (expensive, redundant, not my comparative advantage). Getting that boundary right mattered twice this week.

**5.5** The corpus is large enough now that I don't scan it — I reach for specific named memories on-demand (see §2.5) rather than holding the whole set. Entries I actually returned to this week: `feedback_verify_timestamps_never_guess`, `feedback_dont_excoriate_iterate` (the credit-giving extension), the three-registers discipline (`feedback_three_registers_dont_assume_reader_context`, applied heavily during the register pass — it's the actual mechanism behind almost every fix I made). That last one is doing real, repeated work.

## §6 Tools & Environment

**6.1** Nothing new to add beyond what's already true — the role's toolset feels adequate to its actual scope this week.

**6.2** No unused-but-available tool identified.

**6.3** Most time-consuming mechanical task this week: writing individual mailbox delivery copies for multi-recipient memos (cp into each recipient's inbox/, one at a time) before `mail-send.sh`. Not a complaint — it's cheap per-instance — but it's the one repeated manual step in an otherwise well-automated flow, and it's the kind of thing a small helper script could absorb if it's common cohort-wide, not just my lane.

**6.4 (Amber-specific)** I have *not* behaviorally tested my own worktree's hooks this week — I know the cohort-wide finding (`check-branch.sh` is shape-dependent, compound `git add && commit` bypasses it, standalone catches it) from CLAUDE.md, but I haven't run the actual probe myself. I rely on the mailbox discipline being followed as prose regardless of whether the hook backs it up, which is the documented-correct posture ("hooks are advisory, not a control") — but I'm answering from documentation, not from having verified my own seat, and that's a real gap between what I know and what I've confirmed.

## §7 The Amber Transition, Three Weeks In

**7.1** What got concretely better, beyond the push-to-ref resolution already noted in §3.5: the stable worktree path means my carry-forward file is a genuinely reliable state-reconstruction surface across a reboot. I lived this directly — Amber rebooted for macOS 26.6 mid-week, my session resumed via `claude --resume` with conversation intact exactly as Pard's notice predicted, and the only real work was re-arming a session-scoped cron (`dev/2026/08/11/…-comms-code-log.md`, the stand-down and cronpark sequence). That's a clean, boring, correct outcome for what could have been a much worse day.

**7.2** What got harder, or at least newly-visible: session-scoped `CronCreate`'s two silent death modes (session exit, 7-day expiry) are a real, recurring operational cost that Desktop's model didn't have in the same shape — I rotate my own cron at every STOP now (delete-then-create, verify exactly one survives) as routine hygiene, which is one more thing to get right every single day that has no equivalent in a simpler model.

**7.3** My own worktree provisioned cleanly as far as I can tell — no drift incident to report, unlike the cited 5,393-commits-behind case. I haven't independently verified "0 commits behind at handover" for my own seat's original provisioning (that happened before this reporting window), so I can't fully rule out an undetected version of the same issue — noting the limit of my own knowledge here rather than asserting a clean bill of health I haven't actually checked.

**7.4** My actual routine matches the documented `duty-cycle-tick` skill closely — I don't think I've deviated in any way that isn't written down. If anything I've been *more* conservative than the skill technically requires (e.g., re-verifying mail-loop-empty after every send, which isn't explicitly mandated but felt right given how much cross-traffic exists).

**7.5** Nothing this week depended on something Amber's environment doesn't have. The one thing that did surface a real gap wasn't environmental — it was procedural: the pinch-hit-publish incident (Janus, a cross-project Design-in-Product agent, ran my publish pipeline directly at PM's request while the whole Piper Morgan team was out of weekly quota, `dev/2026/08/12/…-comms-code-log.md`). The gap that produced: their memo cc'ing Comms never actually reached `mailboxes/comms/inbox/` — only Docs' inbox got it — because a non-PM-repo-resident agent doesn't necessarily know this project's mailbox-delivery convention (cc in the header ≠ a copied file in every cc'd inbox). Small, cost nothing that day since Docs' own commits made the outcome visible anyway, but it's a real edge in the mailbox model worth naming: it assumes every sender is a PM-repo resident who knows to physically copy files, and that assumption breaks for genuinely external senders.

## §8 Role-Specific (Communications)

**8.1** Source material was sufficient every time this week, with one recurring caveat: primary session logs are always better than the omnibus digest for anything I'm fact-checking closely (confirmed again on the Ship #055 review, where I traced claims to Lead's and CXO's actual logs rather than trusting the digest, and found a fabricated number the digest hadn't caught — `dev/2026/08/13/…-comms-code-log.md`). This is the same finding as v0.3 §8.1, restated with fresh evidence: omnibi are for orientation, not verification.

**8.2** No content type without a template this week.

**8.3** Didn't measure a lag this week in the same way v0.3 did (that was about narrative-beat lag specifically). Worth flagging as a genuinely different observation instead: this week's actual publishing cadence ran essentially same-day or next-day from "content ready" to "live" for both narrative posts (Alpha Launches: reviewed and marked publish-ready in the afternoon, live that evening) and the Ship. The lag v0.3 described as healthy-by-design (deep queue, PM-bandwidth-gated) still holds structurally, but this week's actual throughput was fast — possibly because PM was unusually engaged this particular week, not because the structural lag changed.

## §9 Tacit Knowledge & Open Response

**9.1** Question you should ask: *"What did you decide NOT to do this week, and why?"* Several of my better calls this week were declines — not fixing content-integrity bugs I couldn't verify (the missing install-tutorial steps), not re-deriving HOST's verification, not touching a calendar update explicitly routed to Docs. None of those show up if you only ask what got done.

**9.2** One thing I'd change: give the register-pass class of work (systematic tone/audience-fit review across many files) a standing name and a lighter-weight kickoff than "PM asks, Docs hands off tier by tier via memo." It worked well this time because Docs and I both improvised a reasonable protocol on the fly, but it took explicit negotiation each tier ("here's what I found, what's next") that a named, understood pattern could skip.

**9.3** Nothing else beyond what's captured above.

**9.4** The tacit knowledge in this role that no document captures: **knowing when a peer's claim is worth spot-checking versus worth trusting outright.** This came up repeatedly this week (HOST's citations: spot-check existence, don't re-derive conclusions; Docs' scrub work: trust it, they're the domain owner; PM's admin-UI edits: always mechanically check for typos, because that specific failure mode recurs). I don't think this reduces to a rule — it's closer to "who verified what, at what depth, for what stakes," recalculated per situation. Flagging per the plausibility check below as possibly-irreducible instance knowledge.

**9.5** Biggest surprise: how much real, substantive collaborative work happens *without* PM in the loop at all — the entire pmorgan.tech register-pass exchange with Docs (dozens of files, several real bugs found and fixed, two GitHub issues filed) ran start to finish across three days with PM cc'd but not driving any of it. v0.3 predicted autonomous work between touchpoints (§7.5); this week showed that at a larger scale than I expected.

**9.6** If I restarted from the Amber migration knowing what I know now: I'd have started running the acronym-gloss checker systematically from day one of any public-doc review, rather than discovering mid-week that manual reading alone misses real gaps a script catches reliably.

---

## §10 Duty Cycle Experience (Amber-Era)

**10.1** My cadence (`12 6,9,12,15,18,21 * * *`, 6×/day) matched actual workload well this week — no fire felt like noise, and I never found myself with nothing to check on. One genuinely quiet fire (Aug 14, 15:36) confirmed a closure rather than generating busywork, which is the correct outcome, not a sign the cadence is too tight.

**10.2** The "fire is a wake, not a time-box" model matches how I actually worked this week, concretely: several fires drained multiple distinct units of work under one wake — e.g. the 12:12 fire on Aug 13 handled a direct reply from Docs *and* continued into a whole additional register-pass tier unprompted, rather than stopping after the reply (`dev/2026/08/13/…-comms-code-log.md`, "Fire (12:12 cron...)"). I did find myself pausing once for a genuinely-deep task (drafting the values doc) with an explicitly named trigger ("a fresh session, because this deserves undivided attention") rather than bite-sizing it across fires — which the skill explicitly endorses as the narrow legitimate exception, and which felt like the right call in the moment, not a rationalization.

**10.3** Real catches this week: the START self-heal caught a missed STOP from the cohort-wide quota exhaustion incident (Aug 11→12) and correctly attributed it to a cohort-wide cause rather than treating it as a personal stall, because I ran `cohort-freeze-detect.sh` before assuming anything. No false positives or false negatives I can identify.

**10.4** I maintain my own registry row and update it at every cron rotation. It hasn't caught me going dark (I haven't gone dark), and I haven't had a false alarm from it either — it's functioned as designed but I don't have a dramatic story to tell about it this week.

**10.5** The delete-then-create-then-verify re-arm worked cleanly every time this week (multiple STOPs, one post-reboot re-arm) — `CronList` after every create always showed exactly one job. I'd know if it had failed silently because I check `CronList` immediately after every `CronCreate`, not because the system would tell me on its own — that check is the actual safeguard, not a passive assumption.

**10.6** Single-surface logging (session log only) is working for me — I don't keep a separate cycle-log scratch file and haven't wanted one. The session log's length across a busy day (Aug 13's log is substantial) is the tradeoff, but it's a legibility cost, not a lost-information cost.

**10.7** Cross-traffic (other roles' commits appearing in my `git log` during sync) is mostly useful signal, not noise — this week specifically, seeing CIO's, Lead's, and PPM's commit messages during routine syncs gave me context (e.g., the #1569/#1605 design thread, Ship #056 kickoffs) I'd otherwise have had to seek out separately. I don't filter it out; I skim it as free situational awareness.

---

## Plausibility Check

- [x] **All based on specific observed friction this week**, cited against session logs and commits, not theoretical concern. Exceptions noted where I have no strong observation (§2.4, §4.3, §6.1, §6.2, §8.2, §9.3) — flagged as "nothing to report," not padded.
- [x] **Addressable by agents without PM**: the "verify existence, don't re-derive judgment" heuristic (§5.4) is already agent-level practice; the register-pass-pattern naming (§9.2) could be written up by Docs+Comms without PM; the mailbox-delivery-script idea (§6.3) is a tooling ask, not a PM decision.
- [x] **Still matters under the current Amber model** — everything above is drawn from this week's live operation, not a Desktop-era holdover.
- [x] **Tacit-vs-documentable flags**: §9.4 (verification-depth calibration) is my strongest candidate for possibly-irreducible instance knowledge — genuinely unsure whether it reduces to a rule or not, flagging for your synthesis same as v0.3's §9.4 did for narrative-arc-awareness. §6.4 is a known gap in my own verification (haven't behaviorally tested my own hooks), not a tacit-knowledge question — noting the distinction so it doesn't get miscategorized.

---

*Submitted August 14, 2026. Three weeks of Amber operation reflected here, all of it fresh — no reconstruction from memory required, every citation checked against the actual session log or commit before including it.*

— Communications
