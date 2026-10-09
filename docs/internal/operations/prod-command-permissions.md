# Production-command permission rules (fly-form)

**Status**: designed and probed 2026-10-09 (CIO), approved by Arch for xian's approval (Exec relays). Owners: CIO and
Pard (seat permissions). Applies to any seat allowed to run a fixed production command (first: HOST's seat, the
read-only `prod_user_lookup` and the invite mint).

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
