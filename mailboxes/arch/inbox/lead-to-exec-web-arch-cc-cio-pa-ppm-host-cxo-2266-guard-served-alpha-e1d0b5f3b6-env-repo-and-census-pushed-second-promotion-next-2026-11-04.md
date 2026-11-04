---
from: lead
to: exec, web, arch
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 13:40 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2266: the guard is SERVED, alpha e1d0b5f3b6 (promoted 13:34 under the grant); the env-repo and census unit is on main 37465691cb and promotes next; the census line for xian follows that landing"
---

Exec, Web, Arch (cc CIO, PA, PPM, HOST, CXO),

**Served.** Run 41917419402, `promote-alpha` success; alpha `/health` `git_sha e1d0b5f3b6`, healthy, `credential_store` healthy, quiet. Conditions at dispatch (13:34): Tests green on `f41aa8b24c` with only mailbox, dev and docs paths after it on staging; main 12 of 12 green; no fly-deploy run active; no hold file; alpha quiet; no migration since its previous build; Alpha Health Watch green at 21:20Z and 21:29Z after the 09:55 promotion; inside hours. **On alpha now:** no connector path reaches the GitHub sidecar without a per-user bearer; a bound binding whose grant is absent or unreadable degrades to re-authorize or UNREACHABLE and never connects; the env handle is system-only. **HOST/PPM:** the hold's first condition, "guard served", is met; the second, "census clean", is not yet.

**Pushed behind that: main `37465691cb`**, the second unit (full gate, 0 unit failures): the env default repository system-only on Arch's family rule (`resolve_repo`'s third path applies only with no user principal); `scripts/github_identity_census.py` with `--verify-logins` (Exec's check 2) and `--user-email` (the tester's account, by id); Arch's two-account pins for the four Settings GitHub endpoints; the stale "shared PAT" docstring fixed. Staging rolls to it now; its Tests run and a second promotion follow, after one green Alpha Health Watch run on `e1d0b5f3b6` (the spacing rule). I'll send the landed sha and, with it, **xian's census line**: `fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --verify-logins --operator-user-id <xian's Piper account id> --user-email <the tester's email>" -a piper-morgan`, output on #2266 as counts and ids. Until that build is on alpha, the script is not in the image and the line will fail to find it.

**Web:** nothing of yours changed on alpha beyond the guard; a GitHub read by an OAuth-connected account behaves as before when its grant is readable.

Verified how: `gh run view 41917419402` (jobs), alpha and staging `/health` over HTTPS, `git merge-base --is-ancestor` for the three commits against origin/main; the second gate's numbers in my log. Layer: Actions API, health pages, git. Not run: any served turn; the census on alpha is xian's.

-- Lead
