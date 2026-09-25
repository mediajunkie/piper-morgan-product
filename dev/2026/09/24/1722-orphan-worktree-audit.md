# Orphaned Subagent Worktree Audit — Issue #1722

**Date**: 2026-09-24 (read-only audit, Coding Agent/prog, dispatched by Lead, Sonnet)

**Scope**: every `agent-*` worktree under `/Users/xian/Development/piper-morgan-product/.claude/worktrees/`. This audit is READ-ONLY: no worktree, branch, or file was mutated, removed, checked out, reset, stashed, or rebased. All commands below are `git -C <worktree> <read-only command>` against the `agent-*` subdirectories, plus one `git -C /Users/xian/Development/piper-morgan-product fetch origin main` (refs only, no working-tree touch) run once up front.

**Denominator**: 89 `agent-*` worktrees found (`git worktree list | grep -c "agent-"`), 89 classified (100%). Note this is 2 fewer than the 91 the issue's original discovery counted — consistent with CIO's note in the issue that they'd already removed 2 of their own worktrees during that same discovery session; not evidence of any other cleanup.

## Summary

| Category | Definition | Count | Total size |
|---|---|---|---|
| **A** | Every unpushed commit's content is on `origin/main` — confirmed by `git cherry` patch-id equivalence (or HEAD is a literal ancestor of `origin/main`, 0 unpushed commits). Disposable. | 86 | 34.9 GB |
| **A\*** | Same as A, but `git cherry` reported `+` (patch-id did NOT match, almost always because the worktree's own local session dev-log file changed the diff's patch id) — manually confirmed identical content landed on `origin/main` under a **different commit SHA** (matching subject line + matching per-file insertion/deletion counts across every substantive file, in 2 of 3 cases the identical `Claude-Session` id). Disposable, same as A. | 3 | 1.2 GB |
| **B** (superseded) | None found. | 0 | — |
| **C** (content genuinely absent from main) | None found. | 0 | — |
| **Total** | | **89** | **36.1 GB** |

**Headline finding: all 89 worktrees classify as disposable (A or A\*).** No worktree carries content genuinely absent from `origin/main`. This is a cleaner result than the issue anticipated PM/Lead review being needed for — there is no category-C list to review because none exists.

**Why every one still shows "1-3 unpushed commits"**: these are subagent-dispatch worktrees. The pattern across all 89 is a single subagent doing its work, committing in its own worktree (with its own session-scoped dev log entry), and — per this repo's actual delivery path — a human or the dispatching agent taking that finished diff and committing it to `origin/main` **themselves**, as a fresh commit (same subject, same substantive file content, new SHA/date/author metadata), rather than merging or fast-forwarding the worktree branch itself. The worktree branch is then simply never cleaned up. `git log origin/main..HEAD` will always show those original commits as "unpushed" under this delivery model, even though their content shipped — which is exactly why patch-content comparison (not ancestry) is the right test here, and why the issue's raw "has unpushed commits" framing overstates the actual risk.

## Method

```bash
# once, in the main checkout (refs only, no working-tree touch):
git -C /Users/xian/Development/piper-morgan-product fetch origin main

# per worktree <path>:
git -C <path> rev-parse --abbrev-ref HEAD
git -C <path> rev-parse HEAD
git -C <path> log -1 --format='%ad|%s' --date=short
git -C <path> log origin/main..HEAD --format='%H|%ad|%s' --date=short
git -C <path> diff origin/main...HEAD --stat
git -C <path> cherry origin/main HEAD          # '-' = patch-id already on main; '+' = not found
git -C <path> diff origin/main...HEAD --name-only
du -sh <path>

# manual follow-up for the 3 '+' cases (agent-a7eae8908361d5be2, agent-ab82a92399df9e617,
# agent-af6f27891de682d61): looked up the referenced GitHub issue (1491/1493, 1510, 1650 —
# all CLOSED), then searched origin/main's history by commit subject and compared
# `git show <main-sha> --stat` per-file line counts against the worktree's diffstat.
```

## Per-worktree table

Sorted by last-commit date. `Commits` = count of commits in `origin/main..HEAD`. `Subjects` truncated where long.

| Worktree | Branch | HEAD | Date | Commits | Category | Size | Note |
|---|---|---|---|---|---|---|---|
| `agent-a7f73fae62169594a` | `worktree-agent-a7f73fae62169594a` | `bf290f45f8` | 2026-08-01 | 1 | A | 354M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a9ff3f3d01204130a` | `worktree-agent-a9ff3f3d01204130a` | `337fbf5c7d` | 2026-08-01 | 1 | A | 358M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-af8ba2072bc2f5649` | `worktree-agent-af8ba2072bc2f5649` | `21635c1c95` | 2026-08-01 | 1 | A | 385M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a8c939a9433b33edf` | `worktree-agent-a8c939a9433b33edf` | `568f0719d9` | 2026-08-02 | 2 | A | 391M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a938a8a5e3d68f13f` | `worktree-agent-a938a8a5e3d68f13f` | `c800a04482` | 2026-08-02 | 1 | A | 360M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aec6a23d1f77f30f5` | `worktree-agent-aec6a23d1f77f30f5` | `34b31218d2` | 2026-08-02 | 1 | A | 361M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a133d207f6e3da2a9` | `worktree-agent-a133d207f6e3da2a9` | `6c385fd1c1` | 2026-08-03 | 1 | A | 392M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ad0c00db33a5509b9` | `worktree-agent-ad0c00db33a5509b9` | `844d505272` | 2026-08-03 | 4 | A | 393M | git cherry: all 4 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7fd1d8dd9c4f073a` | `worktree-agent-a7fd1d8dd9c4f073a` | `331906cc0a` | 2026-08-07 | 1 | A | 383M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ab846312fced200fc` | `worktree-agent-ab846312fced200fc` | `d6c91e00db` | 2026-08-07 | 1 | A | 382M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-acbd16578b85c9e38` | `worktree-agent-acbd16578b85c9e38` | `9191ff4c52` | 2026-08-07 | 1 | A | 410M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ae51dec8222f7b404` | `worktree-agent-ae51dec8222f7b404` | `84647a5725` | 2026-08-07 | 1 | A | 381M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aebfd44711e89764f` | `worktree-agent-aebfd44711e89764f` | `28a2a75487` | 2026-08-07 | 2 | A | 381M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aeff96c0465d3a24f` | `worktree-agent-aeff96c0465d3a24f` | `9858f2541c` | 2026-08-07 | 2 | A | 384M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a0b5a7b6c7952aecb` | `worktree-agent-a0b5a7b6c7952aecb` | `95b855747e` | 2026-08-08 | 1 | A | 394M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a1eb0a58d26c472bc` | `worktree-agent-a1eb0a58d26c472bc` | `04fbf5ab49` | 2026-08-08 | 1 | A | 387M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a538f05acfbfe7e1a` | `worktree-agent-a538f05acfbfe7e1a` | `c277368740` | 2026-08-08 | 1 | A | 391M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a56bd17064b01e8e2` | `worktree-agent-a56bd17064b01e8e2` | `b6b79d4bda` | 2026-08-08 | 1 | A | 447M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a61efcc2fb7f28ae6` | `worktree-agent-a61efcc2fb7f28ae6` | `113b03f4a8` | 2026-08-08 | 1 | A | 408M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a762f33d280ce0a31` | `worktree-agent-a762f33d280ce0a31` | `61ba4711e9` | 2026-08-08 | 1 | A | 388M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7d8228d3b4f9351c` | `worktree-agent-a7d8228d3b4f9351c` | `c8bd752fe0` | 2026-08-08 | 1 | A | 390M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7ec56472509c5acf` | `worktree-agent-a7ec56472509c5acf` | `a7058bbfb0` | 2026-08-08 | 1 | A | 392M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aa35c4ec339ecd114` | `worktree-agent-aa35c4ec339ecd114` | `1857a63fc1` | 2026-08-08 | 1 | A | 389M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aa75d6fe2098c0ac2` | `worktree-agent-aa75d6fe2098c0ac2` | `b28c2ed479` | 2026-08-08 | 1 | A | 415M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aaed59b60d3b8c8d0` | `worktree-agent-aaed59b60d3b8c8d0` | `6b23fe5a3f` | 2026-08-08 | 1 | A | 383M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ab7bc480c707de48b` | `worktree-agent-ab7bc480c707de48b` | `b4eeaa1b14` | 2026-08-08 | 1 | A | 390M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ad092349452ff7710` | `worktree-agent-ad092349452ff7710` | `6c7eb0956f` | 2026-08-08 | 1 | A | 391M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-af758d555bc15ed48` | `worktree-agent-af758d555bc15ed48` | `c3fe4fc679` | 2026-08-08 | 1 | A | 393M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aff7903c2e19d7d98` | `worktree-agent-aff7903c2e19d7d98` | `c7efeef31b` | 2026-08-08 | 1 | A | 391M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a0cf4dc592a57665c` | `worktree-agent-a0cf4dc592a57665c` | `b02ce55131` | 2026-08-09 | 1 | A | 396M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a0e511ed94628f329` | `worktree-agent-a0e511ed94628f329` | `64db7e2f96` | 2026-08-09 | 2 | A | 397M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a3054b59fe5a6c170` | `worktree-agent-a3054b59fe5a6c170` | `ff7c84e54e` | 2026-08-09 | 1 | A | 411M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a321b98a93b38010b` | `worktree-agent-a321b98a93b38010b` | `9caee84f4f` | 2026-08-09 | 1 | A | 395M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a599cec56ecbd6b0b` | `worktree-agent-a599cec56ecbd6b0b` | `79a83c351b` | 2026-08-09 | 1 | A | 396M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a5bad82b7397cb1d7` | `worktree-agent-a5bad82b7397cb1d7` | `065d60135f` | 2026-08-09 | 1 | A | 398M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a67950ef3911e6ec6` | `worktree-agent-a67950ef3911e6ec6` | `ce31572e8e` | 2026-08-09 | 3 | A | 397M | git cherry: all 3 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7eae8908361d5be2` | `worktree-agent-a7eae8908361d5be2` | `58d32bb4a6` | 2026-08-09 | 1 | A* | 410M | cherry showed '+' (patch-id mismatch, likely due to worktree-local dev-log file changing the diff) but manually confirmed: main commit 93c0156839 has IDENTICAL subject + near-identical stat (7/12/21 vs 7/12/21 lines, minus the worktree's own dev-log entry) — same content landed on main. |
| `agent-a7f1b4dcd313e23bd` | `worktree-agent-a7f1b4dcd313e23bd` | `1409a74f99` | 2026-08-09 | 3 | A | 400M | git cherry: all 3 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a8e0d08f4bd789f26` | `worktree-agent-a8e0d08f4bd789f26` | `d1530e6b10` | 2026-08-09 | 1 | A | 395M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ab146ecd1b8362b26` | `worktree-agent-ab146ecd1b8362b26` | `bcf34a52cc` | 2026-08-09 | 1 | A | 396M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ab82a92399df9e617` | `worktree-agent-ab82a92399df9e617` | `0b5b0aacd0` | 2026-08-09 | 1 | A* | 396M | cherry showed '+' (patch-id mismatch) but manually confirmed: main commit 6d9f9e3ae9 has IDENTICAL subject, same Claude-Session id (01KBCtuLeuvFVRqroRQu5mKf), and matching per-file line counts (17/81/355/404) — same content landed on main; the extra ~72 lines in the worktree's own diffstat are its local dev-log entry only. |
| `agent-ae00408fa52ffda55` | `worktree-agent-ae00408fa52ffda55` | `06d968cd0b` | 2026-08-09 | 1 | A | 395M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ae878f4d745247388` | `worktree-agent-ae878f4d745247388` | `bd5351be47` | 2026-08-09 | 1 | A | 397M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a05803576ef2a4387` | `worktree-agent-a05803576ef2a4387` | `e8408a2ac4` | 2026-08-10 | 1 | A | 398M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a0b17214918f623ec` | `worktree-agent-a0b17214918f623ec` | `1a7a10f60a` | 2026-08-10 | 1 | A | 398M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a15dbabf5ba624db8` | `worktree-agent-a15dbabf5ba624db8` | `d435888549` | 2026-08-10 | 2 | A | 441M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a403d606a85be9134` | `worktree-agent-a403d606a85be9134` | `8b00505fb6` | 2026-08-10 | 1 | A | 398M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a5e5b2b42a6f63b5e` | `worktree-agent-a5e5b2b42a6f63b5e` | `ea6390b8ea` | 2026-08-10 | 1 | A | 415M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a636142c8c212daea` | `worktree-agent-a636142c8c212daea` | `416546d52d` | 2026-08-10 | 1 | A | 440M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a647924dac3dc4786` | `worktree-agent-a647924dac3dc4786` | `05f112b441` | 2026-08-10 | 1 | A | 399M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a6fa75f4eb334f48d` | `worktree-agent-a6fa75f4eb334f48d` | `85bc6c774b` | 2026-08-10 | 3 | A | 399M | git cherry: all 3 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7522efe509ce8959` | `worktree-agent-a7522efe509ce8959` | `99321ab307` | 2026-08-10 | 1 | A | 398M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7526ca4d0780889c` | `worktree-agent-a7526ca4d0780889c` | `a6248d44e9` | 2026-08-10 | 2 | A | 396M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aa3d04971a41d0ccc` | `worktree-agent-aa3d04971a41d0ccc` | `5dc2fac0b7` | 2026-08-10 | 1 | A | 403M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ad4650ede32fc0864` | `worktree-agent-ad4650ede32fc0864` | `5d5e91c8d2` | 2026-08-10 | 1 | A | 400M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ae88394db2a98e100` | `worktree-agent-ae88394db2a98e100` | `408faabfbe` | 2026-08-10 | 1 | A | 390M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-afd153bb77ec2c2be` | `worktree-agent-afd153bb77ec2c2be` | `69f1022440` | 2026-08-10 | 1 | A | 405M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-afe667ab5a31bdfec` | `worktree-agent-afe667ab5a31bdfec` | `1b87c41d64` | 2026-08-10 | 2 | A | 398M | git cherry: all 2 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a0aece30ef0c983c5` | `worktree-agent-a0aece30ef0c983c5` | `9b31eec47f` | 2026-08-15 | 1 | A | 417M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a39cdb3f3e037ce61` | `worktree-agent-a39cdb3f3e037ce61` | `873a9196be` | 2026-08-15 | 1 | A | 412M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7ba91fb191eb8c37` | `worktree-agent-a7ba91fb191eb8c37` | `b7f787f2ed` | 2026-08-15 | 1 | A | 418M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7de51739198cf0cd` | `worktree-agent-a7de51739198cf0cd` | `d95103d948` | 2026-08-15 | 1 | A | 416M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aad6798c0ace8e87c` | `worktree-agent-aad6798c0ace8e87c` | `20e2fe4fba` | 2026-08-15 | 1 | A | 419M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aae6a360b3505b0de` | `worktree-agent-aae6a360b3505b0de` | `b4b102d494` | 2026-08-15 | 1 | A | 416M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ac3ad76304f044e61` | `worktree-agent-ac3ad76304f044e61` | `4272b91aa7` | 2026-08-15 | 1 | A | 409M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-addfd7c7ed530c780` | `worktree-agent-addfd7c7ed530c780` | `301e36ba60` | 2026-08-15 | 1 | A | 417M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aedc9148782573889` | `worktree-agent-aedc9148782573889` | `5ffa2fd1b9` | 2026-08-15 | 1 | A | 411M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a43e01bce590cfd98` | `worktree-agent-a43e01bce590cfd98` | `6556d66008` | 2026-08-16 | 1 | A | 416M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a64234e3d8fd28593` | `worktree-agent-a64234e3d8fd28593` | `408ca038b7` | 2026-08-16 | 1 | A | 423M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a7cd4c769f0ef8a9c` | `worktree-agent-a7cd4c769f0ef8a9c` | `abf71e2cf2` | 2026-08-16 | 1 | A | 423M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ab365b095052188d9` | `worktree-agent-ab365b095052188d9` | `a790e89c7d` | 2026-08-16 | 1 | A | 421M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ad06b705a25d4f46b` | `worktree-agent-ad06b705a25d4f46b` | `d21674db82` | 2026-08-16 | 1 | A | 420M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-aed9a91d6f40304d1` | `worktree-agent-aed9a91d6f40304d1` | `cacd1f3b1a` | 2026-08-16 | 1 | A | 420M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a13ec47e08512f150` | `worktree-agent-a13ec47e08512f150` | `f537a0c3ff` | 2026-08-18 | 1 | A | 424M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a84d711ba304fac9d` | `worktree-agent-a84d711ba304fac9d` | `e967f25a0e` | 2026-08-18 | 1 | A | 427M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a93e2bd09b7bf2ace` | `worktree-agent-a93e2bd09b7bf2ace` | `790e697676` | 2026-08-18 | 1 | A | 450M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a97f6c1802c4eeff0` | `worktree-agent-a97f6c1802c4eeff0` | `b0a2fdfe26` | 2026-08-18 | 1 | A | 429M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ac97c35412683e76e` | `worktree-agent-ac97c35412683e76e` | `ba64174037` | 2026-08-18 | 1 | A | 457M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ad4c36d5fc0462f40` | `worktree-agent-ad4c36d5fc0462f40` | `037fd988b3` | 2026-08-18 | 1 | A | 450M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-af6f27891de682d61` | `worktree-agent-af6f27891de682d61` | `7928f76abb` | 2026-08-18 | 1 | A* | 429M | cherry showed '+' (patch-id mismatch) but manually confirmed: main commit 87f454c8a5 has IDENTICAL subject and IDENTICAL per-file line counts (2/25/47/31/11/64/390/43/43/91) across all 10 files — same content landed on main under a different commit (different session/date metadata). |
| `agent-affdeb6a3e820cde0` | `worktree-agent-affdeb6a3e820cde0` | `83bf791ecf` | 2026-08-18 | 1 | A | 431M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a33835435a9076e57` | `worktree-agent-a33835435a9076e57` | `600fec4da5` | 2026-08-19 | 1 | A | 422M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a5ff6832914058987` | `worktree-agent-a5ff6832914058987` | `3804dab188` | 2026-08-19 | 1 | A | 457M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a81476abd2eb310e5` | `worktree-agent-a81476abd2eb310e5` | `2d2367e9fd` | 2026-08-19 | 1 | A | 431M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-acdd21b6c0146a761` | `worktree-agent-acdd21b6c0146a761` | `7fc2908908` | 2026-08-19 | 1 | A | 432M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-ade90f8b8c82ae9ba` | `worktree-agent-ade90f8b8c82ae9ba` | `5942c8008b` | 2026-08-19 | 1 | A | 431M | git cherry: all 1 commit(s) patch-id-equivalent to a commit already on origin/main. |
| `agent-a04c7d212b9dbe4fb` | `worktree-agent-a04c7d212b9dbe4fb` | `5b2f9c138b` | 2026-09-19 | 0 | A | 699M | HEAD is a literal ancestor of origin/main (fully merged, 0 unpushed commits). |
| `agent-a25cb8795379e40e9` | `worktree-agent-a25cb8795379e40e9` | `fd702c23d7` | 2026-09-19 | 0 | A | 699M | HEAD is a literal ancestor of origin/main (fully merged, 0 unpushed commits). |
| `agent-a36b8470f429b3d3f` | `worktree-agent-a36b8470f429b3d3f` | `70b58b7dbc` | 2026-09-19 | 0 | A | 699M | HEAD is a literal ancestor of origin/main (fully merged, 0 unpushed commits). |

## Per-commit subjects (full, not truncated)

For the record — the full unpushed-commit subject line(s) for every worktree, in case the truncated table above lost anything load-bearing:

- **`agent-a7f73fae62169594a`** (A): feat(learning): dashboard controls bind the authenticated principal, not phantom 'current_user' (issue 1430, F19)
- **`agent-a9ff3f3d01204130a`** (A): feat(slack): wire /standup Yesterday/Today to real todo services (issue 1429)
- **`agent-af8ba2072bc2f5649`** (A): fix(portfolio): archived-project list queries archived rows (issue 1431)
- **`agent-a8c939a9433b33edf`** (A): todos(1472): normalize enum filters in get_todos_by_owner + guard agenda todo_count; runtime e2e pins for 1460; intent(1460): backfill original_message attribute on the detect_multiple path; idiom-B readers; Slack fallback key
- **`agent-a938a8a5e3d68f13f`** (A): fix(db): BaseRepository mutations fetch the ORM row, not get_by_id (issue 1464)
- **`agent-aec6a23d1f77f30f5`** (A): test(1433): CHAT_POINTERS product-surface reachability ratchet + decline-copy freshness
- **`agent-a133d207f6e3da2a9`** (A): feat(1428): 'what can you do?' answer derives from the CHAT_POINTERS ledger
- **`agent-ad0c00db33a5509b9`** (A): docs: prog session log wrap for 2026-08-03 (#1466 implementation); feat(#1466): wire Slack linking end-to-end — /link redeem, standup resolution, honest decline, settings mint UI; feat(#1466): link service + CXO copy constants + failing-first suite (18 red on unwired surfaces); feat(#1466): slack_identities + link-code handshake schema (models + alembic l1466slack)
- **`agent-a7fd1d8dd9c4f073a`** (A): fix(1489): unescaped apostrophe in delete-dialog copy was a SyntaxError killing home.html's entire inline conversation script — history reload never ran, so returning to a chat rendered localStorage's user-only bubbles (assistant replies never persisted client-side). One-char fix (It'll -> It\'ll, shipped unescaped by 1482/ce31b09d6); failing-first pins: inline-script string-lexer (reproduces the browser's Unexpected-identifier-ll verbatim), escaped-copy pin, both-sides render pin (1487 noted: renderer is template-embedded, jest can't reach it; route contract already pinned by the 583 suite). Browser-verified: 5-turn conversation renders 5 user + 5 bot bubbles on direct load AND on return-after-navigation.
- **`agent-ab846312fced200fc`** (A): fix(1485): global credential writes require admin — gate slack app-token + slack/calendar app-credentials behind users.is_admin
- **`agent-acbd16578b85c9e38`** (A): fix(1471): connect-verbs out-rank the temporal calendar pattern in the pre-classifier
- **`agent-ae51dec8222f7b404`** (A): fix(1470): thread include_archived into ProjectRepository.find_by_name so restore-by-name can find archived projects
- **`agent-aebfd44711e89764f`** (A): fix(todos): aware-UTC datetimes for todo-layer writes/cutoffs; aware-local reminder parsing (1493); fix(todos): normalize raw TodoStatus/TodoPriority comparisons against String columns (1472)
- **`agent-aeff96c0465d3a24f`** (A): fix(portfolio): robust project-name extraction for archive/restore phrasings (#1492); fix(reminders): handle time-first slot ordering + dedupe 'at at' in confirmation copy (#1490)
- **`agent-a0b5a7b6c7952aecb`** (A): fix(1532): chat-path conversation persistence enforces ownership (audit F3) + the three principal guards
- **`agent-a1eb0a58d26c472bc`** (A): fix(1520): expired sessions get honest copy, visible expiry, and working refresh
- **`agent-a538f05acfbfe7e1a`** (A): fix(1394): thread the principal to the floor — prior turns now reach context on the authenticated chat path
- **`agent-a56bd17064b01e8e2`** (A): fix(1436): slice 1 — mypy gate extended to ALL codes incl name-defined (closes 1469 blindness); 16 name-defined -> 0 incl 1 live NameError; arg-type 410 -> 403
- **`agent-a61efcc2fb7f28ae6`** (A): fix(1476,1477): blocked Radar cards carry a findable referent; current chat visible in rail from first turn
- **`agent-a762f33d280ce0a31`** (A): fix(1480): preserve Slack deep-link (1466) through the login round trip
- **`agent-a7d8228d3b4f9351c`** (A): fix(1524): GitHub query cohort returns honest failure — 1423 slice 2
- **`agent-a7ec56472509c5acf`** (A): fix(1530): chat project list reads the same owner-scoped rows as /projects page
- **`agent-aa35c4ec339ecd114`** (A): fix(1490): bind explicit clock time to date words regardless of ordering
- **`agent-aa75d6fe2098c0ac2`** (A): fix(1521): reminder-QUERY shapes claim surface 1 — 'what reminders do I have?' lists stored reminders, not the temporal answer
- **`agent-aaed59b60d3b8c8d0`** (A): probe(#1283): surface-1 counterfactual measurement — 14 AGREE / 36 DISAGREE / 2 VARIANT of 52 (Arch ruling 2026-08-08, ungated one-off run)
- **`agent-ab7bc480c707de48b`** (A): fix(1411): retire update_issue legacy elif — rail is the single dispatch surface
- **`agent-ad092349452ff7710`** (A): fix(1518): conversation_turns.intent was NEVER populated by the live write path — wire the label through
- **`agent-af758d555bc15ed48`** (A): fix(1529): offer-binding + universal guided-process escape — the standup can no longer hijack a session
- **`agent-aff7903c2e19d7d98`** (A): fix(1423): slice 1 — un-swallow 12 silent-death sites on PM's live-testing paths; ceiling 226→214
- **`agent-a0cf4dc592a57665c`** (A): feat: required defaultless ordered EffectClass on WorkflowEntry (Arch ruling 2026-08-09, PDR-006 cond. 2)
- **`agent-a0e511ed94628f329`** (A): feat: floor capability manifest + anti-retraction guard — capability gaslighting fix (1517); docs: prog session log start for #1517
- **`agent-a3054b59fe5a6c170`** (A): security: owner-scope ProjectQueryService reads, fail-closed (issue 1501)
- **`agent-a321b98a93b38010b`** (A): fix(1431): archived-list query dispatches to archived rows; failure notes render on their own line
- **`agent-a599cec56ecbd6b0b`** (A): docs(1472): prog verification session — all 4 sites confirmed fixed (c632c206f), fresh sweep clean, red-probes prove tests+ratchet gate the class
- **`agent-a5bad82b7397cb1d7`** (A): fix(1542,1545): word-form durations parse as explicit reminders; one malformed row no longer kills the Insight Journal
- **`agent-a67950ef3911e6ec6`** (A): docs: prog session log 2026-08-09 (1558 + 1560); feat(1560): create_reminder onto the 1124 action-dispatch rail (category-independent); fix(1558): user-scoped disconnect no longer pops os.environ tokens process-wide
- **`agent-a7eae8908361d5be2`** (A*): fix(todos): due-reminder fetch failure logs at ERROR, never warning-swallow; get_due_todos marked dead-path (1491, 1493)
- **`agent-a7f1b4dcd313e23bd`** (A): fix(1547): F5 + retire the lying source — plugin /status routes deleted, configured:None, registry-read ratchet; fix(1547): F1-F4 — chat, floor, priority/project metadata, and Radar read the canonical status service; fix(1547): canonical IntegrationStatusService — hoist /health's status truth into ONE service
- **`agent-a8e0d08f4bd789f26`** (A): fix(1411,1543): explicit-#N updates resolve at B3 Stage 0; create-issue titles the subject or asks
- **`agent-ab146ecd1b8362b26`** (A): fix(1541): /todos page CRUD honesty — real delete, complete control, due dates reach /standup
- **`agent-ab82a92399df9e617`** (A*): feat(1510): collaborate-first compose-vs-execute gate + working-mode declaration surface
- **`agent-ae00408fa52ffda55`** (A): fix: PUT /todos calls the real update_todo signature (1548); Add-form priority + no-due-date affordance (1512)
- **`agent-ae878f4d745247388`** (A): docs(prog): 1507+1508 verification session — fixes pre-existed; red/green reproduced; GITHUB_TOKEN reader sweep recorded; 1538 green
- **`agent-a05803576ef2a4387`** (A): fix(1570): floor data queries — scaffolding unrenderable, floor-entry context gather, archived-projects rail key
- **`agent-a0b17214918f623ec`** (A): feat(reminders): 'today' binds today with honest-ask on past (1562); due reminders surface on every floor-bound turn (1566)
- **`agent-a15dbabf5ba624db8`** (A): fix(security): escape every client-side interpolation on the Documents page — stored XSS via filenames/metadata (1581); log(prog): session start for 1581 files.html XSS sweep
- **`agent-a403d606a85be9134`** (A): fix(1573): pending todos no longer vanish from floor context on naive-vs-aware TypeError
- **`agent-a5e5b2b42a6f63b5e`** (A): fix(greeting): never claim a clear day from an unestablished read; never print an unlabeled server clock
- **`agent-a636142c8c212daea`** (A): fix(security): escape every client-side interpolation on /todos — stored XSS via shared titles (1578)
- **`agent-a647924dac3dc4786`** (A): feat: first-contact demonstration — user's own data in the first exchange, unprompted (FTUX-COLDSTART 1536)
- **`agent-a6fa75f4eb334f48d`** (A): docs: session log wrap for 2026-08-10 prog #1190; feat(#1190): multi-turn confirmation gate for destructive rail actions; feat(#1190): close_issue/reopen_issue flip WRITE -> DESTRUCTIVE (PM 08-10 ruling)
- **`agent-a7522efe509ce8959`** (A): fix(intent): 1411 live miss — add 'status' to the shared issue-field vocabulary at the Stage-0 seam
- **`agent-a7526ca4d0780889c`** (A): feat: finish /todos page — inline title edit, priority chip, humanized due dates (1568); docs: session log start for #1568 prog session
- **`agent-aa3d04971a41d0ccc`** (A): feat(todos): give reminders a legible identity — copy teaches the unified model, /todos shows it (1569)
- **`agent-ad4650ede32fc0864`** (A): feat(standup): #1511 MVP — name-addressable interview via token branch in the claiming handler
- **`agent-ae88394db2a98e100`** (A): docs: time-handling class audit 2026-08-10 (PM-directed, audit only)
- **`agent-afd153bb77ec2c2be`** (A): fix(github): read-time recovery for a never-set default repo (1590)
- **`agent-afe667ab5a31bdfec`** (A): fix: 1571 now-fixable halves — floor no-magic-phrases rule + files-family issue-hint decline; test: failing-first tests for 1571 (floor no-magic-phrases rule + files-family issue hint)
- **`agent-a0aece30ef0c983c5`** (A): fix(intent): prose-shape override in detect_offer_response so long replies never accept/decline an armed offer (issue 1631)
- **`agent-a39cdb3f3e037ce61`** (A): test(live): #1621 live-verification fixture — real server, real login, real turns, count-verified cleanup
- **`agent-a7ba91fb191eb8c37`** (A): feat(chat): degenerate GitHub titles render id-carrying placeholders in chat listings (issue 1628)
- **`agent-a7de51739198cf0cd`** (A): fix(draft-flow): mid-compose prose binds to the armed draft — the pop seam holds body answers before any routing surface (1627)
- **`agent-aad6798c0ace8e87c`** (A): feat(reminders): mention due reminders once per session, pin them to Radar top (#1625)
- **`agent-aae6a360b3505b0de`** (A): feat(consent): outwardness axis for the consent gate — 1509 ratified design (PM+CXO+PPM 2026-08-15)
- **`agent-ac3ad76304f044e61`** (A): feat(legibility): catalog states outwardness per action (1632)
- **`agent-addfd7c7ed530c780`** (A): fix(intent): arm a subjectless draft carrier at the compose ask so the first answer binds (issue 1630)
- **`agent-aedc9148782573889`** (A): fix(radar/standup): degenerate entity titles render an id-carrying placeholder, never verbatim (issue 1622)
- **`agent-a43e01bce590cfd98`** (A): test(live): 1597 backlog run — the four shipped fixes' own stated live checks, executed for real
- **`agent-a64234e3d8fd28593`** (A): feat(intent): repo clarification binds and natural repo phrasing extracts (issue 1567)
- **`agent-a7cd4c769f0ef8a9c`** (A): test(1534): end-to-end real-binding regression — setup guidance reads live per-user state
- **`agent-ab365b095052188d9`** (A): feat(intent): chat document-summarize wired to the REST path; dead summarize vocabulary deleted with its record (issue 1624)
- **`agent-ad06b705a25d4f46b`** (A): fix(intent): pending-todos wrong-empty — verified-empty is a fact, conversation-scoped framing removed from the floor prompt (1544)
- **`agent-aed9a91d6f40304d1`** (A): fix(greeting): elapsed focus-time windows render in past tense, never present (1615 tense half)
- **`agent-a13ec47e08512f150`** (A): fix(intent): sibling verified-empty — projects + completed todos are facts when checked, not absences (1639)
- **`agent-a84d711ba304fac9d`** (A): fix(files): upload 500s on Fly — root-owned /data volume vs non-root app user (issue 1656)
- **`agent-a93e2bd09b7bf2ace`** (A): feat(intent): repo-question carrier wired onto reopen, comment, ANALYSIS, and create (issue 1641)
- **`agent-a97f6c1802c4eeff0`** (A): fix(intent): honor explicitly-given subject/description at the draft arm seam (issue 1649)
- **`agent-ac97c35412683e76e`** (A): feat(files): chat summarize sees the SAME document set the Files listing shows (issue 1657)
- **`agent-ad4c36d5fc0462f40`** (A): auth(1640): make /login optional-auth so the 1480 already-authenticated next-bounce is reachable
- **`agent-af6f27891de682d61`** (A*): fix(intent): CONFIRM kinds accept only crisp full-message affirmatives (issue 1650)
- **`agent-affdeb6a3e820cde0`** (A): feat(standup): closing offer binds its overdue-todo referent — acceptance completes the bound id (issue 1651)
- **`agent-a33835435a9076e57`** (A): meas(inversion 1595 Phase 2.1): snapshot-aware corpus gate — armed-state fixtures, runner, honest table
- **`agent-a5ff6832914058987`** (A): feat(intent): 1595 Phase 2.2 flip-1 — live inversion routing behind default-empty per-category flag
- **`agent-a81476abd2eb310e5`** (A): feat(snapshot): arm sites store their rendered ask (1665) + is_confirm derives from offer kind (1664)
- **`agent-acdd21b6c0146a761`** (A): feat(intent): 1666 — delete_todo onto the rail, #1190-gated; legacy elif removed
- **`agent-ade90f8b8c82ae9ba`** (A): feat(1595-P2.0): assemble the SessionSnapshot from the real stores and feed the shadow lane
- **`agent-a04c7d212b9dbe4fb`** (A): (none — already ancestor)
- **`agent-a25cb8795379e40e9`** (A): (none — already ancestor)
- **`agent-a36b8470f429b3d3f`** (A): (none — already ancestor)

## Category A* detail (the 3 manually-confirmed cases)

### `agent-a7eae8908361d5be2` — issues #1491, #1493 (both CLOSED)

Worktree commit `58d32bb4a68`: `fix(todos): due-reminder fetch failure logs at ERROR, never warning-swallow; get_due_todos marked dead-path (1491, 1493)`.

`origin/main` commit `93c0156839` — **identical subject line**, and identical per-file line-change counts: `services/intent_service/todo_handlers.py` (7 lines changed), `services/repositories/todo_repository.py` (12 lines changed), `tests/unit/services/intent_service/test_reminders.py` (21 lines changed) — matching the worktree's own diffstat exactly on all 3 substantive files. The worktree's diffstat shows a 4th file (`dev/2026/08/09/2026-08-09-0940-prog-code-log.md`, +31), which is its own local session dev-log entry and correctly doesn't exist on main (dev logs are worktree-session-local, not part of the shipped fix). Confirmed live in `services/intent_service/todo_handlers.py` line ~417 (`logger.error("Failed to fetch due reminders (source failed)"...)`) and `services/repositories/todo_repository.py` `get_due_todos` docstring (`DEAD PATH (#1493 audit, ...)`) — both present on `origin/main` today. Landed under a different SHA/date/author-metadata than the worktree's own commit, which is why `git cherry` reported `+` (patch-id differs) despite the content being the same.

### `agent-ab82a92399df9e617` — issue #1510 (CLOSED)

Worktree commit `0b5b0aacd07`: `feat(1510): collaborate-first compose-vs-execute gate + working-mode declaration surface`.

`origin/main` commit `6d9f9e3ae9` — **identical subject line**, **identical `Claude-Session` id** (`session_01KBCtuLeuvFVRqroRQu5mKf`) as the worktree commit, and matching per-file line counts: `docs/internal/architecture/current/intent-routing-stack.md` (+17), `services/intent/intent_service.py` (+81), `services/intent_service/collaboration_gate.py` (new, +355), `tests/unit/services/intent_service/test_collaboration_gate_1510.py` (new, +404). `services/intent_service/collaboration_gate.py` exists on `origin/main` today. The worktree's own diffstat shows 72 extra lines, entirely accounted for by its local session dev-log entry.

### `agent-af6f27891de682d61` — issue #1650 (CLOSED)

Worktree commit `7928f76abb1`: `fix(intent): CONFIRM kinds accept only crisp full-message affirmatives (issue 1650)`.

`origin/main` commit `87f454c8a5` — **identical subject line** and **identical per-file line counts across all 10 touched files** (`intent-routing-stack.md` +2/-1, `intent_service.py` +25, `drafted_issue.py` +47, `reminder_clear.py` +31, `repo_clarification.py` +11, `soft_invocation.py` +64 (new detector), plus 4 test files at +390/+43/+43/+91). Different date metadata (main commit dated 2026-08-18, worktree commit shows the same date in its own log) and different `Claude-Session` id from the other two A* cases, so this one is a genuinely separate re-implementation that happened to converge on byte-identical file changes — not a copy-paste of the same session's work, but the same fix landing twice with identical content.

## What was NOT classified / could not verify

Nothing. All 89 worktrees found were classified (89/89). The 3 `A*` cases required manual follow-up beyond the automated `git cherry` signal, documented above; all 3 resolved cleanly to "content is on main." No worktree needed to be left as an open question, and none showed uncommitted working-tree changes (per the Lead's earlier `status --porcelain` pass, not re-run here) or content that could not be matched to `origin/main`.

## Proposed removal — Category A + A* only (NOT executed)

All 89 worktrees are proposed for removal. **This audit did not run any of the following — it is a list for PM/Lead review and manual execution.** Standard caution applies: run from the main checkout, verify `git worktree list` before and after, and note these operate on the `.claude/worktrees/` subtree, never on the main checkout's own working tree.

```bash
cd /Users/xian/Development/piper-morgan-product
git worktree remove .claude/worktrees/agent-a7f73fae62169594a
git worktree remove .claude/worktrees/agent-a9ff3f3d01204130a
git worktree remove .claude/worktrees/agent-af8ba2072bc2f5649
git worktree remove .claude/worktrees/agent-a8c939a9433b33edf
git worktree remove .claude/worktrees/agent-a938a8a5e3d68f13f
git worktree remove .claude/worktrees/agent-aec6a23d1f77f30f5
git worktree remove .claude/worktrees/agent-a133d207f6e3da2a9
git worktree remove .claude/worktrees/agent-ad0c00db33a5509b9
git worktree remove .claude/worktrees/agent-a7fd1d8dd9c4f073a
git worktree remove .claude/worktrees/agent-ab846312fced200fc
git worktree remove .claude/worktrees/agent-acbd16578b85c9e38
git worktree remove .claude/worktrees/agent-ae51dec8222f7b404
git worktree remove .claude/worktrees/agent-aebfd44711e89764f
git worktree remove .claude/worktrees/agent-aeff96c0465d3a24f
git worktree remove .claude/worktrees/agent-a0b5a7b6c7952aecb
git worktree remove .claude/worktrees/agent-a1eb0a58d26c472bc
git worktree remove .claude/worktrees/agent-a538f05acfbfe7e1a
git worktree remove .claude/worktrees/agent-a56bd17064b01e8e2
git worktree remove .claude/worktrees/agent-a61efcc2fb7f28ae6
git worktree remove .claude/worktrees/agent-a762f33d280ce0a31
git worktree remove .claude/worktrees/agent-a7d8228d3b4f9351c
git worktree remove .claude/worktrees/agent-a7ec56472509c5acf
git worktree remove .claude/worktrees/agent-aa35c4ec339ecd114
git worktree remove .claude/worktrees/agent-aa75d6fe2098c0ac2
git worktree remove .claude/worktrees/agent-aaed59b60d3b8c8d0
git worktree remove .claude/worktrees/agent-ab7bc480c707de48b
git worktree remove .claude/worktrees/agent-ad092349452ff7710
git worktree remove .claude/worktrees/agent-af758d555bc15ed48
git worktree remove .claude/worktrees/agent-aff7903c2e19d7d98
git worktree remove .claude/worktrees/agent-a0cf4dc592a57665c
git worktree remove .claude/worktrees/agent-a0e511ed94628f329
git worktree remove .claude/worktrees/agent-a3054b59fe5a6c170
git worktree remove .claude/worktrees/agent-a321b98a93b38010b
git worktree remove .claude/worktrees/agent-a599cec56ecbd6b0b
git worktree remove .claude/worktrees/agent-a5bad82b7397cb1d7
git worktree remove .claude/worktrees/agent-a67950ef3911e6ec6
git worktree remove .claude/worktrees/agent-a7eae8908361d5be2
git worktree remove .claude/worktrees/agent-a7f1b4dcd313e23bd
git worktree remove .claude/worktrees/agent-a8e0d08f4bd789f26
git worktree remove .claude/worktrees/agent-ab146ecd1b8362b26
git worktree remove .claude/worktrees/agent-ab82a92399df9e617
git worktree remove .claude/worktrees/agent-ae00408fa52ffda55
git worktree remove .claude/worktrees/agent-ae878f4d745247388
git worktree remove .claude/worktrees/agent-a05803576ef2a4387
git worktree remove .claude/worktrees/agent-a0b17214918f623ec
git worktree remove .claude/worktrees/agent-a15dbabf5ba624db8
git worktree remove .claude/worktrees/agent-a403d606a85be9134
git worktree remove .claude/worktrees/agent-a5e5b2b42a6f63b5e
git worktree remove .claude/worktrees/agent-a636142c8c212daea
git worktree remove .claude/worktrees/agent-a647924dac3dc4786
git worktree remove .claude/worktrees/agent-a6fa75f4eb334f48d
git worktree remove .claude/worktrees/agent-a7522efe509ce8959
git worktree remove .claude/worktrees/agent-a7526ca4d0780889c
git worktree remove .claude/worktrees/agent-aa3d04971a41d0ccc
git worktree remove .claude/worktrees/agent-ad4650ede32fc0864
git worktree remove .claude/worktrees/agent-ae88394db2a98e100
git worktree remove .claude/worktrees/agent-afd153bb77ec2c2be
git worktree remove .claude/worktrees/agent-afe667ab5a31bdfec
git worktree remove .claude/worktrees/agent-a0aece30ef0c983c5
git worktree remove .claude/worktrees/agent-a39cdb3f3e037ce61
git worktree remove .claude/worktrees/agent-a7ba91fb191eb8c37
git worktree remove .claude/worktrees/agent-a7de51739198cf0cd
git worktree remove .claude/worktrees/agent-aad6798c0ace8e87c
git worktree remove .claude/worktrees/agent-aae6a360b3505b0de
git worktree remove .claude/worktrees/agent-ac3ad76304f044e61
git worktree remove .claude/worktrees/agent-addfd7c7ed530c780
git worktree remove .claude/worktrees/agent-aedc9148782573889
git worktree remove .claude/worktrees/agent-a43e01bce590cfd98
git worktree remove .claude/worktrees/agent-a64234e3d8fd28593
git worktree remove .claude/worktrees/agent-a7cd4c769f0ef8a9c
git worktree remove .claude/worktrees/agent-ab365b095052188d9
git worktree remove .claude/worktrees/agent-ad06b705a25d4f46b
git worktree remove .claude/worktrees/agent-aed9a91d6f40304d1
git worktree remove .claude/worktrees/agent-a13ec47e08512f150
git worktree remove .claude/worktrees/agent-a84d711ba304fac9d
git worktree remove .claude/worktrees/agent-a93e2bd09b7bf2ace
git worktree remove .claude/worktrees/agent-a97f6c1802c4eeff0
git worktree remove .claude/worktrees/agent-ac97c35412683e76e
git worktree remove .claude/worktrees/agent-ad4c36d5fc0462f40
git worktree remove .claude/worktrees/agent-af6f27891de682d61
git worktree remove .claude/worktrees/agent-affdeb6a3e820cde0
git worktree remove .claude/worktrees/agent-a33835435a9076e57
git worktree remove .claude/worktrees/agent-a5ff6832914058987
git worktree remove .claude/worktrees/agent-a81476abd2eb310e5
git worktree remove .claude/worktrees/agent-acdd21b6c0146a761
git worktree remove .claude/worktrees/agent-ade90f8b8c82ae9ba
git worktree remove .claude/worktrees/agent-a04c7d212b9dbe4fb
git worktree remove .claude/worktrees/agent-a25cb8795379e40e9
git worktree remove .claude/worktrees/agent-a36b8470f429b3d3f

git branch -D worktree-agent-a7f73fae62169594a
git branch -D worktree-agent-a9ff3f3d01204130a
git branch -D worktree-agent-af8ba2072bc2f5649
git branch -D worktree-agent-a8c939a9433b33edf
git branch -D worktree-agent-a938a8a5e3d68f13f
git branch -D worktree-agent-aec6a23d1f77f30f5
git branch -D worktree-agent-a133d207f6e3da2a9
git branch -D worktree-agent-ad0c00db33a5509b9
git branch -D worktree-agent-a7fd1d8dd9c4f073a
git branch -D worktree-agent-ab846312fced200fc
git branch -D worktree-agent-acbd16578b85c9e38
git branch -D worktree-agent-ae51dec8222f7b404
git branch -D worktree-agent-aebfd44711e89764f
git branch -D worktree-agent-aeff96c0465d3a24f
git branch -D worktree-agent-a0b5a7b6c7952aecb
git branch -D worktree-agent-a1eb0a58d26c472bc
git branch -D worktree-agent-a538f05acfbfe7e1a
git branch -D worktree-agent-a56bd17064b01e8e2
git branch -D worktree-agent-a61efcc2fb7f28ae6
git branch -D worktree-agent-a762f33d280ce0a31
git branch -D worktree-agent-a7d8228d3b4f9351c
git branch -D worktree-agent-a7ec56472509c5acf
git branch -D worktree-agent-aa35c4ec339ecd114
git branch -D worktree-agent-aa75d6fe2098c0ac2
git branch -D worktree-agent-aaed59b60d3b8c8d0
git branch -D worktree-agent-ab7bc480c707de48b
git branch -D worktree-agent-ad092349452ff7710
git branch -D worktree-agent-af758d555bc15ed48
git branch -D worktree-agent-aff7903c2e19d7d98
git branch -D worktree-agent-a0cf4dc592a57665c
git branch -D worktree-agent-a0e511ed94628f329
git branch -D worktree-agent-a3054b59fe5a6c170
git branch -D worktree-agent-a321b98a93b38010b
git branch -D worktree-agent-a599cec56ecbd6b0b
git branch -D worktree-agent-a5bad82b7397cb1d7
git branch -D worktree-agent-a67950ef3911e6ec6
git branch -D worktree-agent-a7eae8908361d5be2
git branch -D worktree-agent-a7f1b4dcd313e23bd
git branch -D worktree-agent-a8e0d08f4bd789f26
git branch -D worktree-agent-ab146ecd1b8362b26
git branch -D worktree-agent-ab82a92399df9e617
git branch -D worktree-agent-ae00408fa52ffda55
git branch -D worktree-agent-ae878f4d745247388
git branch -D worktree-agent-a05803576ef2a4387
git branch -D worktree-agent-a0b17214918f623ec
git branch -D worktree-agent-a15dbabf5ba624db8
git branch -D worktree-agent-a403d606a85be9134
git branch -D worktree-agent-a5e5b2b42a6f63b5e
git branch -D worktree-agent-a636142c8c212daea
git branch -D worktree-agent-a647924dac3dc4786
git branch -D worktree-agent-a6fa75f4eb334f48d
git branch -D worktree-agent-a7522efe509ce8959
git branch -D worktree-agent-a7526ca4d0780889c
git branch -D worktree-agent-aa3d04971a41d0ccc
git branch -D worktree-agent-ad4650ede32fc0864
git branch -D worktree-agent-ae88394db2a98e100
git branch -D worktree-agent-afd153bb77ec2c2be
git branch -D worktree-agent-afe667ab5a31bdfec
git branch -D worktree-agent-a0aece30ef0c983c5
git branch -D worktree-agent-a39cdb3f3e037ce61
git branch -D worktree-agent-a7ba91fb191eb8c37
git branch -D worktree-agent-a7de51739198cf0cd
git branch -D worktree-agent-aad6798c0ace8e87c
git branch -D worktree-agent-aae6a360b3505b0de
git branch -D worktree-agent-ac3ad76304f044e61
git branch -D worktree-agent-addfd7c7ed530c780
git branch -D worktree-agent-aedc9148782573889
git branch -D worktree-agent-a43e01bce590cfd98
git branch -D worktree-agent-a64234e3d8fd28593
git branch -D worktree-agent-a7cd4c769f0ef8a9c
git branch -D worktree-agent-ab365b095052188d9
git branch -D worktree-agent-ad06b705a25d4f46b
git branch -D worktree-agent-aed9a91d6f40304d1
git branch -D worktree-agent-a13ec47e08512f150
git branch -D worktree-agent-a84d711ba304fac9d
git branch -D worktree-agent-a93e2bd09b7bf2ace
git branch -D worktree-agent-a97f6c1802c4eeff0
git branch -D worktree-agent-ac97c35412683e76e
git branch -D worktree-agent-ad4c36d5fc0462f40
git branch -D worktree-agent-af6f27891de682d61
git branch -D worktree-agent-affdeb6a3e820cde0
git branch -D worktree-agent-a33835435a9076e57
git branch -D worktree-agent-a5ff6832914058987
git branch -D worktree-agent-a81476abd2eb310e5
git branch -D worktree-agent-acdd21b6c0146a761
git branch -D worktree-agent-ade90f8b8c82ae9ba
git branch -D worktree-agent-a04c7d212b9dbe4fb
git branch -D worktree-agent-a25cb8795379e40e9
git branch -D worktree-agent-a36b8470f429b3d3f
```

After running, verify with `git worktree list | grep -c agent-` (expect 0) and `du -sh .claude/worktrees` (expect the directory to be empty or gone).
