# Production-command permission rules (fly-form)

**Status**: designed and probed 2026-10-09 (CIO), approved by Arch for xian's approval (Exec relays). Owners: CIO and
Pard (seat permissions). Applies to any seat allowed to run a fixed production command (first: HOST's seat, the
read-only `prod_user_lookup` and the invite mint).

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
