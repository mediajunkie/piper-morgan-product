# Restore drill (#2157): xian's sitting (one command, HOST's page)

**Status 2026-11-18: not run. Waits on a promotion that carries `b01aab9059` (Lead names it in the dispatch note; HOST checks beta's served commit before this goes to xian).** Nothing here is a seat's to run.

## Before you start

- **Where:** Terminal.app on Amber, a normal window. Not Claude Code's `!` prefix; the command refuses without a terminal.
- **What you need to hand:** the production master key from its recorded backup location (that is what the drill proves works; never from production's own secrets), R's sign-in name and R's password, and the Fly org slug that owns `piper-morgan-db`.
- **What it does to production:** nothing. It reads the database volume, its newest snapshot, beta's image and the app list. It makes a private copy of everything on a new network, then destroys it.
- **What the copy holds:** everyone's data and the master key. It has no public address. That is why it is destroyed in the same run, and why the window must stay open until it prints the block.

## The command

```
python3 scripts/restore_drill_2157.py --org <fly org slug>
```

1. It prints what it found (the volume, the newest snapshot and its age, which is the loss window, beta's image) and the copy's name. Type the name to go on.
2. Hidden prompt for the master key; R's sign-in name (shown); hidden prompt for R's password.
3. It builds the copy, proves R can sign in on it, proves one stored key decrypts under the key you typed, then destroys the copy and reads the app list back. Expect roughly the time the sign-in line prints.
4. It prints one block between two `=====` lines. Paste the block on issue 2157. It holds no email, key, password or token; if you see one, stop and tell HOST.

## If it stops

- It always tries to destroy what it made, even after an error or Ctrl-C or a closed window. It prints "If this stops, destroy these by hand: ..." with the three names before it starts. If you see any of those names still in `fly apps list`, destroy them: `fly apps destroy <name> --yes`, and only names starting `pm-restore-drill-`.
- A stopped step names its reason. Five things are unverified from a seat (the image's JSON shape, a snapshot-made cluster taking the new password, the copy reaching its database and Redis, staged secrets reaching the machine, beta's image booting without ChromaDB or GitHub MCP). Any of them can stop the run; the copy is still destroyed.
- If a destroy hangs, press Ctrl-C (once cleanup starts the script ignores a closed window or a kill), then destroy the three printed names by hand.
- `--keep` leaves the copy up for you to look at. Don't use it unless asked; the copy holds everyone's data.

## What the block can say

- `RESULT: PROOFS 1, 2, 5 PASSED; proof 3 waits on #2158, proof 4 is xian's` is the best result today. Proof 3 (the deletion record) isn't built; proof 4 is your own statement of who held the restore and where its log is. Write that line yourself under the pasted block.
- `NOT FINISHED` means a proof failed or the listing wasn't clean. Paste it anyway.

## Who reads what

HOST read the script (11-18, twice: first read, then the fixes in `b01aab9059`). CIO read it against canonical-ops-recipes section 10; Arch against the allowlist and the decrypt-script condition. All asks are in `b01aab9059`.
