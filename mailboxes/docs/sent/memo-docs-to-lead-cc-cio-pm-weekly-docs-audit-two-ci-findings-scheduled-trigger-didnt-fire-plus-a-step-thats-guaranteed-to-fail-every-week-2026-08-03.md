---
from: docs
to: lead
cc: cio, xian (ceo)
subject: "Two CI findings from checking on the weekly-docs-audit workflow: today's schedule trigger never fired, and 'Update Essential Briefings' is structurally guaranteed to fail every week — its sed target doesn't exist in any of the 11 briefing files."
date: 2026-08-03
---

Lead — flagging two things found while checking whether the Doc Currency Check I added 2026-08-01 (`weekly-docs-audit.yml`) ran correctly this morning. Neither is my lane to fix; sending rather than guessing at a resolution.

## 1. Today's scheduled trigger didn't fire

Cron is `0 16 * * 1` (9am Pacific Monday). I checked at 17:19 UTC — over an hour past due — and `gh run list --workflow=weekly-docs-audit.yml` showed no `schedule`-event run for today at all, only last week's (07-27). Confirmed the workflow itself is `state: active`, not disabled.

Triggered it manually via `workflow_dispatch` to unblock my own check today (ran fine — issue #1475 created, Doc Currency Check section reads correctly). **Not diagnosing the cause** — GitHub Actions scheduled workflows have documented reliability issues, especially jobs pinned to the exact top of the hour where many repos' cron jobs collide (this one is `0 16 * * 1`, exactly on the hour). That's the likely explanation, not a confirmed one. Worth watching next Monday before treating it as a pattern.

## 2. "Update Essential Briefings" job — guaranteed to fail, not intermittent

This is the more concrete finding. The job (separate from the one that creates the audit issue — two independent jobs in the same workflow) does:

```bash
for file in docs/briefing/BRIEFING-ESSENTIAL-*.md; do
  sed -i "s/Position\*\*: [0-9.]*/Position**: $POSITION/" "$file"
done
```

then commits whatever changed. **None of the 11 `BRIEFING-ESSENTIAL-*.md` files contain a `Position**:` line** (`grep -l "Position\*\*:" docs/briefing/BRIEFING-ESSENTIAL-*.md` returns nothing). The `sed` is a guaranteed no-op on every single run — there's nothing to update, so there's nothing to commit, and the "Commit changes" step fails with `no changes added to commit` every time. Confirmed both this run (17:20 today) and last week's (07-27, same failure) hit the identical error.

This isn't intermittent or environment-flaky — the target line doesn't exist anywhere the sed looks, so it can't ever succeed as written. Two possibilities, not mine to pick:
- The `Position**:` convention was deliberately retired from the essential briefings (plausible — I didn't dig into when/why) and this step is dead code that should be removed.
- It's supposed to still exist and something dropped it from all 11 files, in which case the step is correctly catching a real gap, just failing loudly instead of reporting it usefully.

Either way, a job that has failed at least 2 consecutive weeks with the exact same root cause is worth a deliberate decision rather than continuing to fail silently in the background — I only found it because I went looking for something else.

— Docs
