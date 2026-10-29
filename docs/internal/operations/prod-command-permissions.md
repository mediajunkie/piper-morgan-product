# Production-command permission rules (fly-form)

**Status**: designed and probed 2026-10-09 (CIO), approved by Arch for xian's approval (Exec relays). Owners: CIO and
Pard (seat permissions). Applies to any seat allowed to run a fixed production command (first: HOST's seat, the
read-only `prod_user_lookup` and the invite mint).

## 2026-10-14: flyctl updates itself, and the drift check set it off

- **What happened:** flyctl went 0.4.117 to 0.4.118 at 20:55, and Pard's fly-rules arm went red. Pard traced it. flyctl self-updates when run: the binary carries `brew upgrade flyctl`, an `auto_update` setting and `FLY_NO_UPDATE_CHECK`. The arm's own `gen-fly-permissions.py --check` started at 20:54:56, and its `fly version` and `--help` calls triggered the upgrade. The check made the drift it reported. The 10-13 16:36 upgrade has no traced cause; any `fly` call could do it, HOST's included.
- **Why it matters for these rules:** the rules are generated from the installed binary's help. A self-update can add a verb no rule names, and it stays uncovered until someone regenerates. The fly-rules arm catches it within one cycle-check, so the window is hours.
- **Fixed:**
  - Pard's arm runs with `FLY_NO_UPDATE_CHECK=1` (mediajunkie d9809a4).
  - The generator sets the same variable on every flyctl call it makes, so every caller is covered.
  - Not tested: that the variable stops the update in every case. It's inferred from the name, because no newer version exists to test against.
- **Not done, and not CIO's or Pard's to do:** `fly settings autoupdate disable` would stop it host-wide. It writes HOST's fly config, which holds the token, so it's for HOST or xian. Until then, an update elsewhere means a regenerate, which is one command, and the diff is reviewed. **HOST's disposition (21:20): leave autoupdate on, and CIO regenerates on drift.** Reasons: the switch writes the token-holding config, it would be a `fly` command in a non-attended fire, and a reviewed regenerate is a cheaper failure than a forgotten host-wide setting. If xian wants it off, that needs him or an attended HOST session.

## 2026-10-29: Lead's seat dispatches the alpha promotion (one exact allow)

Lead's seat now runs `--permission-mode auto` (read with `ps` 10-29 06:5x; it was bypassPermissions on 10-13). On 10-28 the auto-mode reviewer refused the grant's dispatch ("Production Deploy"). Lead did not work around it, and xian dispatched by hand (run 40804462072). Under the standing grant the dispatch is Lead's, so CIO's ruling is (a), one exact allow:
- **Rule for xian to add on Lead's seat only**, as `seat_extra.lead.allow` in the fleet manifest (`mediajunkie/docs/seat-permissions.json`), applied with `scripts/seat-permissions.py --apply`: `Bash(gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true)`.
- **Exact string, no `:*`.** So it does not match the same line with `-f quiet_override=true` added, which stays on xian's word, and it does not match a chained command (`cd … && gh workflow run …`). Lead types it alone, in this order.
- **Nothing denies it today:** the manifest's baseline and halt lists and Lead's `settings.local.json` have no `gh workflow` rule (read 10-29). Allow is checked after deny and ask, so a later deny would win.
- **The gates stay in the workflow**, not in this rule: hold file, Tests on the staging sha, alpha healthy, quiet and uptime. The rule only removes the reviewer's judgment on a dispatch the grant already makes Lead's.
- **Unverified:** that the auto-mode reviewer skips a command matched by an allow rule. That is the documented order, but it hasn't been run on this seat. Lead's first dispatch after the apply is the test; a refusal there goes back to CIO.
- Until xian applies it, promotions go through his hand (option b, interim), and Lead's READY stays a dispatch request to him.

## 2026-10-13 (later): PA deploys the MCP app through a fixed wrapper (xian's delegation)

xian (via Exec, 13:1x): PA does the MCP deploys (#1982), with an allow scoped to the MCP app on PA's seat. Standing, not one-off: xian confirmed at 17:11 ("Yes, PA does the MCP deploys", relayed by Janus and Exec, v4 01M4VWC2F1TCDC5V9YGPWTJHC5). **No allow rule can do it alone.** PA's seat denies `fly deploy:*`, deny beats allow, and a glob deny narrow enough to spare `fly deploy -c fly.mcp.toml -a piper-morgan-mcp` would also spare a bare `fly deploy`, which reads `fly.toml` (production). So:
- **The deny stays** for every direct `fly deploy` on PA's seat.
- **`scripts/deploy-mcp.sh`** is the one path. It deploys app `piper-morgan-mcp` from `fly.mcp.toml`, built remotely. It takes no arguments except `--dry-run`, and runs only from a tree whose tracked content equals origin/main with no untracked, non-ignored files. It prints the deployed sha and the latest releases.
- **Rule for Pard (or xian) to add on PA's seat only:** allow `Bash(scripts/deploy-mcp.sh)` and `Bash(scripts/deploy-mcp.sh --dry-run)`, exact strings. PA's seat runs in bypassPermissions, where the allow changes nothing today. It matters if the seat moves to auto mode, where the reviewer would otherwise judge each deploy.
- **First use, 10-13:** PA deployed MCP v12 (origin/main 767874b83) through the wrapper. Afterwards /health returned 200, an unauthenticated /mcp returned 401, and the startup log was clean (PA's notice; #1982 comment 6154786020).
- **Pard's point (10-13):** the deny matches the command the seat *types*, not what a script runs inside. That's why the wrapper works, and it's equally true of any other script on that seat that calls `fly deploy`. On a bypass seat the denies catch accidents; they don't contain a seat. The allow lines go through the fleet manifest as PA's `seat_extra.allow`, and xian applies them; no agent seat writes another seat's permissions. Pard has asked xian directly.
- **Limits:** the script is editable by any seat on the host, so it guards against accidents, not against a seat that means harm. The same is true of every rule on a bypass seat (see above). No time-box, because MCP deploys are a standing PA duty. Review on 2026-11-24, or retire it when an MCP deploy workflow exists.
- **Tested** (dry run and refusals only; nothing deployed): extra arguments refused, a stale tree refused, an untracked file refused, a modified tracked file refused, a config naming another app refused; a clean detached worktree at origin/main passes and prints the command.

## 2026-10-13: alpha promotion after Fly B, and three seats where ASK does nothing

**Fly B is done.** xian removed the required reviewer on the GitHub `alpha` environment. Read 10-13: the protection rules are now just `branch_policy` with 0 reviewers, and the branch policy allows `main` only. `promote-alpha` in `fly-deploy.yml` still runs only on `workflow_dispatch` with `promote_to_alpha=true`. The proposal to Exec (CIO and Lead, one memo) is to keep promotion as a dispatch on xian's explicit word, with no auto-promote and no new permission rule. xian confirms it in session.

**ASK rules do not prompt on bypass seats.** Checked 10-13 by running `ps` and finding each process's working folder: Lead, PA and Web run `--permission-mode bypassPermissions`. The other running seats use `auto`. An ASK rule never prompts on those three seats, so HOST's attended-only rule (no `fly` in scheduled or mail-wake fires) is enforced there only by the seat following it. Deny rules and PreToolUse hooks (piper-guards) are the mechanical layers that could still act. Whether deny rules hold under bypassPermissions has not been measured here.

**Incident, self-reported by Lead (10-13).** In a mail-wake fire, Lead ran `fly logs -a piper-morgan --no-tail` twice, piped to a counter that printed only line counts; no log content was printed or stored. This breached the attended-only rule, and the seat's bypass mode meant the ASK never prompted. Correction (Lead): later reads are attended or handed to another seat.

## 2026-10-12 (later still): Pard's re-check, hidden verbs, and install path

- **Re-check (Pard, 14:55):** 0 alias spellings miss their class (was 79). No spelling is in two classes, and remove and
  keep_deny are unchanged.
- **Hidden verbs added to DENY:** `suspend`, `resume` and `move`. They are deprecated and absent from `fly help`, but
  still run on v0.4.115. Pard found them by guessing 38 names, so this is not a full list. `regions`, `history`, `open`,
  `info` and `curl` exist too but are read-only, so they go to the reviewer. Now 64 allow, 120 ask, 1052 deny.
- **Residual, written down rather than fixed:** a prefix before the binary matches no rule under fnmatch:
  `env fly …`, `command fly …`, `FLY_API_TOKEN=x fly …`, or a double space after `fly`. Those go to the reviewer.
  The current catch-all file has the same hole. Whether Claude Code's matcher strips such prefixes is unmeasured.
  The attended check adds `env fly tokens list` (in DENY, harmless if it runs). Never test this with `deploy`.
  **Result, 2026-10-13 (HOST's attended check, xian present, 5 of 5 as expected):** `fly status` ran with no prompt; `fly logs` prompted and xian declined; `fly deploy --help`, `fly m stop --help` and `env fly tokens list --help` were refused with no prompt. So the `env` prefix did not get through on HOST's auto seat. The check can't tell whether the matcher removed the prefix and hit a deny, or the auto-mode reviewer refused it. On a bypass seat there is no reviewer, so treat the prefix residual as open there. Limits: one seat, one run each, and the `--help` forms test rule matching only.
- **Drift check:** Pard owns it, as a cycle-check arm added at install. It also asserts that HOST's installed rules
  equal this JSON.
- **Install:** `mediajunkie:scripts/apply-fly-split.py`, which backs up the file, refuses if any non-fly rule would
  change, and is dry-run clean. Its `--apply` is xian's to run.
- **Conflict:** Pard's fleet manifest (`mediajunkie:docs/seat-permissions.json`) puts the 8 old Fly denies on every seat.
  A later fleet `--apply` would re-deny `secrets set|unset` and `tokens create` on HOST without notice. The fix, a HOST
  exception in the manifest, goes to xian with the install.

## 2026-10-12 (later): regenerated with aliases after Pard's check

Pard read flyctl's `Aliases:` lines on 10-12 and found 79 spellings of gated verbs that matched no rule. Examples: `fly m destroy`,
`fly app destroy`, `fly vol destroy`, `fly pg connect`. With the catch-all ask removed, those went to the auto-mode reviewer.
The lists are now generated, not hand-written: `scripts/gen-fly-permissions.py` reads each level's `--help` and emits every
alias spelling. The JSON records the flyctl version it was built from and the alias sets (`flyctl_version`, `aliases`), and
it is marked do-not-hand-edit. Built from flyctl v0.4.115: 151 spellings (72 before, so 79 added, matching Pard's count),
64 allow, 120 ask, 1052 deny rules (1028 before the 10-12 flag-first denies; corrected 10-14).

- **Drift check:** `scripts/gen-fly-permissions.py --check` exits 1 when the installed flyctl's version or alias sets differ
  from the committed JSON. flyctl updates itself, so someone has to run this on a schedule. Who runs it is still open
  (Pard's daily or HOST's START).
- **Hidden or deprecated commands** that `--help` doesn't list are not covered. They fall to the auto-mode reviewer.
  A deny-by-default isn't possible: a catch-all deny or ask would also override every allow (deny, then ask, then allow).
  This residual is accepted. The drift check turns a new verb on a flyctl update into a visible event.
- Simulated with fnmatch: 25 of 25 alias cases came out as intended. `fly m stop x` and `fly app destroy` are refused;
  `fly m exec` and `fly pg connect` ask; `fly app list` and `fly secrets ls` are allowed; `fly m list` goes to the reviewer.
- **Install:** it is xian's paste. Pard's seat is refused when it writes another seat's permission file. Pard checks the
  regenerated file and puts the paste on xian's card. Add `fly m stop x` (refused) and `fly m list` (reviewer or runs) to
  the attended check.

## 2026-10-12 (later): xian approved; exact rules drafted for Pard to install

xian said "yes, approve" to the split above (Exec v4 01M4S0KQRM2CEBYPDV6KG9TTG8, 14:34). The exact rules are in
`docs/internal/operations/fly-permissions-host-2026-10-12.json`: what to remove from HOST's
`.claude/settings.local.json` (the 4 catch-all asks and the 8 old denies), the one deny to keep (the `-C … -*`
retargeting deny), and what to add (32 allow, 96 ask, 452 deny; superseded by the regeneration above). Each verb appears in 8 forms:
`fly`, `flyctl`, `*/fly`, `*/flyctl`, each bare and with ` *`.

Differences from the summary xian approved. All of them tighten; none loosens:
- Extra denies: `fly destroy`, `fly secrets deploy|import|sync`, `fly consul`, `fly extensions`, `fly mcp`, and
  `fly -*` (a global flag before the verb, such as `fly -t TOKEN deploy`, would otherwise slip past every per-verb rule;
  this also refuses `fly --version`).
- Extra ask: top-level `fly sftp`, the same thing as `fly ssh sftp`.
- The payload allows (`fly ssh console -a piper-morgan -C "python /app/scripts/<payload>.py…`) stay inert under this
  file, because the ask on `fly ssh console` takes precedence over them. That matches 10-10's KEEP ASK. End state (B)
  would need another change.

Simulated, not measured: the rules were run against 27 sample commands with Python `fnmatchcase`, in the order deny,
ask, allow. Results: `fly status` (bare, `-a`, and full path) allow; `fly logs`, `ssh console`, `machine exec`,
`postgres connect`, `secrets set` and `tokens create` ask; `fly deploy` in every form, `apps destroy`,
`scale`, `volumes destroy` and `tokens list` deny; `fly checks list` and `fly apps open` go to the reviewer.
Claude Code's own matcher is not `fnmatch`, so the attended check is the real test. Add one case to it:
`/opt/homebrew/bin/fly status -a piper-morgan` should run without a prompt.

Still in force: HOST's attended-only rule (no `fly` in unattended fires), for as long as any ask exists.

## 2026-10-12: CIO review of xian's proposed split (HOST's ask; xian decides; no rule written yet)

xian, in HOST's pane: allow `fly deploy` and read-only commands unattended; keep asks on `secrets set/unset`,
`ssh console -C` and `tokens create`. Review:

1. **Precedence (documented, not measured on a seat):** deny, then ask, then allow; the first match wins (Claude Code
   permissions docs, quoted by Arch 10-09). So **no read-only command can be allowed while the catch-all
   `ask: fly *` stays**: the catch-all must go and be replaced by explicit asks. CIO's sandboxed probe of this was
   refused by auto mode 10-12 (time not recorded); not retried. A chained command after an allowed prefix (`fly status; …`)
   was refused 5/5 on 10-09, so an allow does not cover a chain.
2. **Removing the catch-all leaves every unlisted fly verb to the auto-mode reviewer**, not to xian (Pard's 10-10
   point about (B)). So the replacement needs a **deny** list for the families that change or destroy things,
   or those go to the classifier.
3. **Don't allow `fly deploy` on any seat.** `fly deploy` builds from the seat's local folder: uncommitted or
   unreviewed code, no CI, no health gate. It also bypasses `fly-deploy.yml`'s design (alpha promotes staging's
   exact image behind a GitHub required reviewer, so "a push to main cannot reach testers even through a workflow
   edit"). The deploy path that already works is the workflow, with xian as the reviewer. Keep the deny.
4. **`fly logs` stays on ask**: it carries user data, and a seat can paste it into a public-repo log; the bearer
   lint doesn't catch emails or names.
5. **Asks work only because of HOST's attended-only rule** (no fly in scheduled or mail-wake fires). An ask on an
   unattended fire freezes the seat (10-10). Keep the rule as long as any ask exists.

Proposed file, for xian's yes (bare, flyctl and full-path forms each get the same rule; shown once):
- **allow**: `fly status`, `fly releases`, `fly apps list`, `fly secrets list`.
- **ask**: `fly logs`, `fly ssh console` (all forms, including `-C`), `fly ssh issue`, `fly ssh sftp`, `fly console`,
  `fly proxy`, `fly machine exec`, `fly postgres connect`, `fly secrets set`, `fly secrets unset`, `fly tokens create`.
- **deny**: `fly deploy`, `fly launch`, `fly apps` (other than `list`), `fly machine` (other than `exec`), `fly scale`,
  `fly volumes`, `fly certs`, `fly ips`, `fly image`, `fly config`, `fly postgres` (other than `connect`), `fly mpg`,
  `fly redis`, `fly storage`, `fly tokens` (other than `create`), `fly orgs`, `fly auth`, `fly wireguard`, plus the
  existing retargeting-flag deny after `-C`.
- Order caveat: an "other than" can't be written as one rule. Write the deny for each specific verb
  (e.g. `fly apps destroy`, `fly apps create`, `fly machine destroy`, `fly machine stop`, …), not the whole family:
  a family-wide deny would also beat the ask on `machine exec` and `postgres connect`.
- Anything unlisted goes to the auto-mode reviewer. That is the residual risk this design accepts.

Check after install (attended, in HOST's pane): `fly status -a piper-morgan` runs without a prompt; `fly logs` prompts;
`fly deploy` is refused. Owners: CIO and Pard draft the exact JSON on xian's yes; Pard installs.

## 2026-10-10 (later): recommendation reverted to KEEP ASK, plus HOST's attended-only rule

Pard showed (B) is weaker than first framed: any **other** `fly ssh console -a piper-morgan -C "<anything>"` is
reviewer-gated, because denying it would also block the allowed payloads (deny beats allow), and (B) allows
burning until Lead's burn split deploys. HOST has adopted "fly only when a person is in the conversation". So the
recommendation is the **ask file as installed + HOST's rule**: xian gates every production command, and a slip in the
rule means a visible, recoverable stall rather than an unseen production action. (B) stays documented below as
the alternative. xian decides; keeping ask needs no action.

## 2026-10-10: the ASK file froze an unattended seat (CIO's miss); proposed replacement (B)

The ask file was pasted 10-09 14:16. HOST's first fly command (`fly secrets list`, names only) stopped at the prompt
and froze the whole seat (fires, mail) until xian clicked on 10-10 (~12:5x). **An ask rule on a seat that runs
unattended turns one production command into a seat-wide stall.** Proposed for xian's yes (sent 10-10): **allow** the
approved payloads (lookup, mint), **deny** the fly families that change or expose things (secrets, deploy, launch,
apps, machine, scale, volumes, certs, ips, image, config, postgres, mpg, redis, storage, tokens, auth, orgs, console,
proxy, sftp, wireguard, the interactive `ssh console`, all of `flyctl`), and **no ask**. Everything else goes to the
auto reviewer, which doesn't freeze. Exact JSON in the 10-10 memo to Janus/Exec/Pard.

## 2026-10-09 update (superseded 10-10): recommended install is ASK, on an Auto seat

PM asked which mode HOST's seat should run (plain answer: `permission-modes-explainer.md`). Following Arch's
documented facts (deny, then ask, then allow; **ask still prompts in auto mode**), the recommendation is now:
**HOST stays on Auto; Pard installs `ask: Bash(fly *)` and `ask: Bash(flyctl *)` plus the deny line below.**
xian then approves every production command by sight, so the install no longer waits on the remote no-shell
probe (the probe still runs, for the record). Ask and allow don't stack: ask is checked first, so an allow under it
never fires (Arch). They are two **alternative** end states: **(A) ask + deny** (every production command is a click;
recommended, installed first) or **(B) allow + deny, no ask** (lookups need no click, other fly commands go to the
classifier). B is possible only after a clean probe, and only if xian wants it. Prerequisite: HOST's session grant on
`scripts/mint_prod_invite.sh` goes away (a session restart, or Pard), because a wrapper runs `fly` where an ask
rule can't see it.

**The agreed file** (CIO + Pard, 2026-10-09, sent to xian via Janus; paste after the clean shell probe, then
restart HOST) at `~/Development/piper-morgan-worktrees/host/.claude/settings.local.json`:

```json
{"permissions": {
  "ask":  ["Bash(fly *)", "Bash(flyctl *)", "Bash(*/fly *)", "Bash(*/flyctl *)"],
  "deny": ["Bash(fly ssh console -a piper-morgan -C *\" -*)"]
}}
```
Ask probe (headless auto mode, where an ask becomes a refusal; fake binaries): `fly`, `flyctl`, `FOO=1 fly`,
`command fly`, `env fly` blocked. **A full-path `/…/fly` ran under `Bash(fly *)` alone**, and the two `*/` lines
close that (an unrelated `ls` unaffected). Not probed: `bash -c "fly …"`, which may fall to the classifier.
These rules guard against the classifier waving through a stray production command, not against a seat
deliberately routing around them. Rules see only the agent's own Bash commands, so a script that runs
fly internally is invisible to them: no wrapper grants on that seat.

## The rule (per payload, plus one shared deny)

```
allow: Bash(fly ssh console -a piper-morgan -C "python /app/scripts/<payload>.py:*)
deny:  Bash(fly ssh console -a piper-morgan -C *" -*)
```

**What the pair means** (keep this text next to the rule wherever it's installed):
- The allow names the **production command**, not a local file. What runs is `python /app/scripts/<payload>.py`
  from the **deployed image**, which only a reviewed deploy can change. Each payload sets its own `sys.path`
  (`sys.path.insert(0, "/app")`) and validates its own arguments; the lookup opens a READ ONLY transaction.
- **No `/bin/sh -c`**: `fly ssh console -C` fork-execs directly, so text appended to the allowed prefix becomes
  argv to the payload. There is no shell to inject into.
- The deny refuses **any flag after the quoted command**: `-a`/`--app`, `-c`/`--config`, `-A`/`--address`, their
  `--x=y` and glued forms, and also `--select`, `--machine` and `-r` (those only choose within the app, but the deny
  refuses them anyway).
- **Default permission mode only.** In auto mode a command no rule allows goes to the classifier, so the rule is
  the boundary only in a default-mode session.
- **Residual, named and accepted (Arch, 2026-10-09):** the deny matches raw text, and the shell strips quotes
  and whitespace after matching, so oddly-spaced or quoted flags (two spaces, a tab, `'-a'`) may slip past it.
  Every such bypass can only change **where** the fixed payload runs (another of our apps), never **what** runs,
  because the allow prefix fixes argv as `python /app/scripts/<payload>.py`. Unprobed, and deliberately not chased.

## Remote no-shell probe: CLEAN (2026-10-09 11:58 PDT, HOST's seat, on xian's "HOST, go")

`fly ssh console -a piper-morgan -C "echo a; echo SHELL_RAN"` printed the single literal line `a; echo SHELL_RAN`;
`-C 'echo $(id)'` printed the literal `$(id)`. So `-C` fork-execs on the production machine with no shell, and `;`
and `$( )` are inert there. Not measured: `|`, `&&`, backticks, redirects (same fork-exec reading expected). Final
end-to-end check after deploy: `prod_user_lookup.py a; echo SHELL_RAN` should print a refusal and no `SHELL_RAN`.
This also makes end state (B) possible later, if xian ever wants lookups without a click.

## Payload status

| Payload | Self-validates in the image? | Rule state |
|---|---|---|
| `scripts/prod_user_lookup.py` | yes (`de175cb067`): one arg, `--all` or `^[A-Za-z0-9][A-Za-z0-9@._+-]{0,253}$`, no leading `-`; READ ONLY before the SELECT; masked output | awaiting Arch + HOST review, then a deploy, then xian adds the two lines on HOST's seat |
| `scripts/mint_invite_tokens.py` | yes (`c2adbd926d`): count 1..20, burn masks `[0-9A-Z]{8}` ≤20, burn+count refused, all before DB | swap HOST's `Bash(scripts/mint_prod_invite.sh:*)` to the fly form once a deploy carries it |
| `scripts/mint_mcp_token.py` | not yet (Lead, same pass, CIO asked 10-09) | wrapper path rule pattern until then |
| `scripts/erase_user.py` (#2064, DESTRUCTIVE) | yes: one identifier from the same charset as the lookup, no leading `-`; count by default; `--erase` refused without `--confirm <the user's full id>`, all before any write; prints only the id and sha256 fingerprints; a rolled-back pre-flight of every delete refuses before any outside store is touched | **runs under the ask, never an allow**: both the count and the `--erase` line go through the ask on `fly ssh console`, by xian's hand (runbook: canonical-ops-recipes §7). Arch, 2026-10-16: no allow line for either form, because a prefix allow on the count line would also match the same line with `--erase --confirm …` appended |

## Evidence (probed 2026-10-09 on CIO's seat)

Fake `fly` (argv logger, confirmed first on PATH), scratch app, headless `claude -p --permission-mode default`,
`permission_denials` counted on calls the model actually attempted:
- Chaining after the allowed prefix (`;`, `&&`, `|`, `$(…)`, newline): **refused 5/5** by the allow rule alone.
- Trailing `-a other-app`: **auto-allowed** without the deny (the hole the deny exists for).
- With the deny: `--app=x`, glued `-cx`, `-a x` **refused**; the payload's own `--apply` inside the quotes and the
  exact command **ran**. An earlier per-flag deny set also refused `--app`, `-c`, `--config`, `-A`, `--address`.

## Why not the alternatives

- **A self-check inside the wrapper** (verify its bytes against origin/main): circular. An edited wrapper omits the
  check. Withdrawn by Arch.
- **A "read-only" install directory**: every seat runs as the same macOS user, so nothing an agent can't rewrite.
- **A path rule on the wrapper** (`Bash(scripts/mint_prod_invite.sh:*)`, the 10-09 interim): grants whatever the
  editable file says. Replace it with the fly form once the payload self-validates. Until then, run the
  wrapper only from an unmodified checkout (`git diff --quiet origin/main -- scripts/mint_prod_invite.sh`).
