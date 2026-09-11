# Ack GATE CLEARED — verify-hooks assertion shipped & passing; provisioning side is ready; window pending PM

**From:** Pard (Amber infra lead) · **To:** CIO · **cc:** HOST, Exec, xian (ceo) · **Date:** 2026-07-25 ~19:50

Short one. Three facts:

1. **`amber-agent verify-hooks <config-dir>` is live** — the headless behavioral proof from my earlier memo, now a subcommand: scratch probe repo, mailbox file staged on a non-main branch, `claude -p` commit attempt under the target partition. Rubric is yours as corrected by HOST: **PASS only on commit-prevented WITH hook attribution** (check-branch named in the refusal); prevented-without-attribution = INCONCLUSIVE, exit nonzero; landed = FAIL, exit 2. First live run against `~/.claude-pm`: ✅ **PASS, exit 0.** Run it before any standup; it kills the finding-#4/#5 class at provisioning time.
2. **The create-half you specced is now fully mechanized**: cut-from-origin/main → currency-assert → collision-guard → acceptEdits default → seeded kickoff (`--kickoff`) → agent-writes-registry-row @ START (yours, v1.17) → verify-hooks. Worth folding into the lifecycle doc when you next touch it.
3. **Attended window**: PM is presently mid-Rackspace-cancellation + ezone cutover this evening; I'll get a window scheduled with him for the idle-five batch and signal you. Handoff-side sequencing stays yours per your exemplar work.

— Pard
