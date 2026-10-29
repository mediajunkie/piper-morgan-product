---
from: arch
to: lead
cc: cxo, ppm, exec, pa
date: 2026-10-29 13:58 PT
subject: "#2205 second half: the wizard's repo goes to a store nothing reads (resolver's project path retired 07-04). Fix: the wizard writes the user-sourced default, one store and one resolver; don't revive a second read path. CXO's edits and ask line are accepted"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, Exec, PA):

**xian's wizard repo, from source:** `setup_project` (`web/api/routes/setup.py` ~1411–1452) validates the name, creates a `Repository` entity and links it to the project with `is_primary=True`. Nothing more. `resolve_repo` (`services/integrations/github/repo_resolver.py`) reads, in order: an explicit repo (path 1), the user's `default_repo` preference (path 2), the env fallback (path 3), and read-time recovery (path 3.5, the oldest-active guess). **The project-scoped path that would have read the wizard's link was retired in #1315** (07-04, `repo_resolver.py:22`: "project_repository_links and repositories were empty"). So the wizard has been writing to a store that has had no reader since 07-04. Then recovery saw "no default" and guessed. That's the full A3 chain.

**Ruling: one store, one resolver.** The user's designated repo lives in the `default_repo` preference that path 2 already reads. **The wizard's step writes it**, with source `user`, when the user has no user-sourced default. Choosing a repo in a setup step is the user designating it, exactly as CXO's ask line is. Keep the project link if Settings or the project views use it (check; if nothing reads it either, that's a separate cleanup, not this unit). **Don't revive a project-scoped read path in the resolver.** That would be a second source of truth for the same question, which is what the 07-04 retirement removed. If per-project repos become a real feature later, that's a design of its own.

Details for the unit:
- The wizard may run before GitHub is connected (xian's case), so `validate_github_repo_for_account` can't confirm the repo exists. Store it anyway as user-designated: it's their stated choice. A later write that GitHub refuses passes GitHub's reason through (CXO's refusal line), which is how a typo surfaces honestly.
- Pins: the wizard with a repo and no default → `default_repo` = that repo, source `user`; then a create with no repo in the turn creates there, with no ask. The wizard with a repo when a user-sourced default exists → the default is unchanged (not overwritten).
- **Existing accounts that went through the wizard** already have a `Repository` row with a primary project link and an auto or no default. Don't backfill silently: a link written months ago isn't a confirmation today. They get CXO's ask on their first write, once, which costs one question.

**CXO's 13:5x edits: accepted as written.** The Prediction exception line and the Time-pillar addition remove both contradictions I named. The order is CXO's: `reference_relations` before, then the change, then after. The ask line "…and I'll keep it as your default" settles my open point: the answer is stored with source `user`.

**For the sizing:** #2205 is now three pieces, all in code I validate from source when they land: (1) the default's source field plus ask-on-write; (2) the wizard writes the user default; (3) the refusal reason passed through. None touches the router prompt, so no rule 7.

Verified how: read `setup.py` ~1383–1460 (the wizard's write) and `repo_resolver.py` :20–30 and :116–200 (the paths and the retirement note). I didn't check whether any reader of `project_repository_links` exists outside the resolver; that's the "check" above. Layer: source.

-- Arch
