# Amber Fleet Stand-Down & Resume — Runbook v1 (DRAFT, for review)

**Owner:** Pard (infrastructure lead, Amber) · **Status:** draft v1, not yet rehearsed
**Date:** 2026-08-05 · **Reviewers wanted:** HOST, Arch, CIO, Themis, Argus, Coral
**Trigger for writing it:** macOS 26.6 pending on Amber; automatic install was ON until
today, meaning the host was scheduled to reboot itself overnight and take 24 live agent
sessions with it, unattended.

---

## 1. What this covers

Any event that reboots Amber: macOS updates, hardware maintenance, power work, a kernel
panic recovery. The procedure assumes the reboot is **planned**. Unplanned reboots are
covered in §9.

**It does not cover** Cowork agents (Relay), which run inside Claude Desktop on other
machines and are unaffected by an Amber reboot.

---

## 2. Facts about Amber that shape the procedure

Verified 2026-08-05; re-verify before relying on any of them.

| Fact | Consequence |
|---|---|
| FileVault is **On**; two secure-token users (`xian`, `amberadmin`), personal recovery key escrowed | Boot stops at the FileVault unlock. A human must answer it — but **not necessarily at the keyboard**; see §8.5, the preboot SSH responder answers it remotely. |
| Amber's IP is **not stable across reboots** (observed 2026-08-11: `.118` → `.119`) | **Address it as `amber.local`, never a hardcoded IP.** The `ssh studio` alias hardcodes one and this is what "failed" on the first live run. |
| All 15 scheduled jobs are **LaunchAgents** (`~/Library/LaunchAgents`), plus one user `crontab` entry | These are *user* agents — they load at **GUI login**, not at boot and **not on SSH**. See §8.5: an SSH session is not a login. |
| The fleet runs as **tmux sessions** (24 as of this writing) | tmux does **not** survive a reboot. Every session must be relaunched. This is the bulk of the work. |
| Repo hygiene is good — the 2026-08-05 pre-flight scan found zero uncommitted or unpushed work across all agent worktrees | **Disk state is not the risk.** |
| Each session holds unwritten working context | **Context is the risk.** A reboot without handoffs destroys 24 sessions' understanding, which no backup recovers. |
| `amber-agent.sh` has file-based kickoff and a startup assertion | Resume is scriptable, and "up" can be observed rather than claimed. |

**The single most important framing:** this procedure exists to convert *context loss*
into *context handoff*. Everything else is mechanics.

---

## 2b. ⚠ The conductor is also a casualty

**Pard is resident #24.** From the moment the machine goes down until `amber-fleet resume`
finishes, there is no agent conducting anything — and Pard's own duty cycle is session-scoped,
so it dies with the reboot like PM's eleven (§5b).

**Therefore every command from Phase 4 onward must be runnable by xian alone**, without an agent
to interpret, adapt, or notice a problem. That is a design constraint on this document, not a
caveat about it: if a step needs judgement, it belongs *before* the reboot, not after.

### xian's card — the whole sequence, no agent required

```bash
F=~/Development/mediajunkie/scripts/amber-fleet.sh

# ── before ──────────────────────────────────────────────────────────────
$F gate                 # go/no-go. RED names = not handed off. Re-run at T−5.
$F snapshot             # capture all 24 (session · cwd · partition · transcript)
$F verify               # probe each transcript; ⛔ = wrong session, fix before rebooting
cp ~/.local/state/amber-agent/fleet-snapshot.tsv ~/Desktop/fleet-snapshot-backup.tsv

# ── Coral's partition move (while she is down) ──────────────────────────
cp -R ~/.claude-kindsys/projects/-Users-xian-Development-one-job \
      ~/.claude/projects/-Users-xian-Development-one-job
sed -i '' 's|/Users/xian/.claude-kindsys|default|' ~/.local/state/amber-agent/fleet-snapshot.tsv

# ── reboot ──────────────────────────────────────────────────────────────
sudo fdesetup authrestart   # PREFERRED: takes the password now, boots straight through FileVault
# sudo shutdown -r now      # alternative — stops at the preboot unlock, see §8.5

# ── get back in — NOT automatic, see §8.5 ───────────────────────────────
ping -c2 amber.local    # ALWAYS by name. The IP moves; `ssh studio` hardcodes a stale one.
open vnc://amber.local  # Screen Sharing, then LOG IN AT THE CONSOLE. SSH is not a login.

# ── after GUI login, from a Terminal INSIDE the VNC session ─────────────
launchctl list | grep -cE 'klatch|janus|verify-hooks|troll|crossword|colima'   # expect ~20
$F resume               # brings all 24 back, resuming real conversations
```

**Copy the snapshot to the Desktop before rebooting.** It lives under `~/.local/state/`, which
survives fine — but if anything goes wrong, that file is how the fleet gets rebuilt, and it
should not be somewhere you'd have to ask an agent to find.

> **⚠ Ordering defect, found 2026-08-11 — the backup is taken BEFORE the `sed`.** So
> `~/Desktop/fleet-snapshot-backup.tsv` still points Coral at the retired `~/.claude-kindsys`
> partition. The recovery path — the one the failure table sends you to when nothing else works —
> therefore has Coral's failure mode baked into it. **Run the `sed` against both files**, and
> assert it landed rather than assuming:
> ```bash
> sed -i '' 's|/Users/xian/.claude-kindsys|default|' ~/Desktop/fleet-snapshot-backup.tsv
> grep -c 'claude-kindsys' ~/.local/state/amber-agent/fleet-snapshot.tsv \
>                          ~/Desktop/fleet-snapshot-backup.tsv    # both MUST be 0
> ```

**Then tell the resumed agents to re-arm their cycles** (§5b) — the seats on session-scoped crons
will not do it unprompted, because they have no way to know their cron died.

## 3. Roles

| Role | Who | Responsibility |
|---|---|---|
| Conductor | Pard | Runs the phases, owns the gate, reports the census |
| Authenticator | xian | FileVault unlock, login, any permission prompt. Cannot be delegated. |
| Residents | all 24 | Write a handoff, commit, push, confirm |

No agent may answer another agent's permission prompts. This is classifier-enforced and
is not a convention we can relax under time pressure.

---

## 4. Phase 0 — Pre-flight (T−24h)

1. **Confirm the reboot is actually needed.** A pending update is not a reason by itself;
   name the driver (security fix, Xcode/App Store minimum, hardware).
2. **Confirm FileVault recovery posture is current** — two secure-token users, recovery
   key escrowed and findable, password hint set. If any is false, **stop**; fix that first.
   A reboot with one forgettable password is a loss event, not an inconvenience.
3. **Scan for at-risk work:**
   ```bash
   # per repo/worktree: uncommitted + unpushed
   git -C "$d" status --porcelain | wc -l
   git -C "$d" rev-list --count origin/main..HEAD
   ```
4. **Announce the window** to xian with a proposed time. Reboots need him present
   throughout — not just at the start.

### 4.1 ⚠ A reboot is not an update. Trigger the update explicitly.

**Measured 2026-08-11:** `sudo shutdown -r now` on Amber with 26.6 staged and pending booted
straight back into **26.5.2**. The staged update did not apply. The entire stand-down — 24
handoffs, gate, snapshot, verify — was spent and the driver that justified it was not satisfied.

**The mechanism, confirmed in System Settings the same morning:** Automatic Updates is set to
**"Only download."** That is the correct setting for this host — §11's whole reason for existing
was stopping Amber from rebooting itself overnight and taking 24 sessions with it — but it means
the update sits fully downloaded and *never scheduled to install*. A restart is therefore just a
restart. **The setting that makes the fleet safe is the same setting that makes a reboot not an
update.** Those two facts belong in the same sentence, and until today they were in neither.

So when the driver is a macOS update, **the update is its own step**, and the reboot in Phase 4 is
not it:

```bash
softwareupdate --list            # confirm the label and that it is actually available
df -h /                          # room to stage and install
```

Then install from **System Settings → General → Software Update** while at the console. Prefer
the GUI on Apple Silicon: CLI `softwareupdate -i -R` commonly fails the volume-owner
authentication that FileVault requires, and diagnosing that with a fleet down is not the moment.

**Sequencing, and this is the part worth getting right:** if you discover post-reboot that the
update did not land, **install it before Phase 5, not after.** The fleet is already down, already
handed off, and the snapshot is already verified — the expensive half of the procedure is spent
and still valid. Resuming first buys a second complete stand-down to return to the state you are
already in. **Never resume and then update:** those 24 residents come back, work, and die again
with no handoff, which is §9 — an unplanned reboot with extra steps.

Add to Phase 6: `sw_vers` must show the version the reboot was called for. A stand-down that
doesn't deliver its driver is a stand-down you get to run again.

---

## 5. Phase 1 — Notice (T−60m)

Broadcast to every session:

> Amber reboots at **{T}**. Before then: (1) write a handoff to your repo's canonical
> handoff path, (2) commit and push it to `origin/main`, (3) reply `STOOD DOWN`.
> Your session will not survive. Anything you have not written down is lost.

**Design note for reviewers:** the notice must state the *deadline* and the *consequence*,
not just the request. An agent that does not know its context dies has no reason to
prioritise the handoff over its current task.

---

## 6. Phase 2 — The handoff gate (T−30m)

**The gate measures files on `origin/main`. It does not accept an agent's assurance.**

```bash
# for each resident: does a handoff dated today exist on the trunk?
git -C "$repo" fetch -q origin
git -C "$repo" ls-tree -r --name-only origin/main -- docs/ | grep "handoff.*$(date +%F)"
```

> **`-r` is load-bearing.** Without it `ls-tree` lists only the top level of `docs/` and finds
> **zero** handoffs — for every resident, always. Verified against the Klatch trunk: 0 without
> `-r`, 10 with it. A gate that never passes is a gate that gets overridden, so this defect
> would have converted the reboot's only interlock into a rubber stamp at exactly the moment it
> mattered. Caught by Arch on review, 2026-08-05, before first use.

Three outcomes per resident:

- **GREEN** — handoff on trunk. Proceed.
- **WAIVED** — xian explicitly waives a resident (idle, parked, or its context is
  genuinely disposable). Recorded by name in the log, never inferred.
- **RED** — no handoff, not waived. **The reboot does not proceed** on a red roster
  without xian's explicit override, and the override is logged with the names.

This is the rule the whole runbook turns on. A stand-down that reboots on a red roster is
just an unplanned reboot with extra steps.

### The T−5 re-check — HOST's gap

HOST caught that the gate and the enforcement are **thirty minutes apart**, and everything an
agent does in that window is unhandoffed by construction:

```
T−60  Notice    → the DECLARATION
T−30  Gate      → the EVIDENCE
T     Reboot    → the ENFORCEMENT      ← 30 minutes of unhandoffed work in between
```

So the T−30 gate is a *provisional* pass. **Re-run it at T−5** (`amber-fleet gate`) and treat
*that* result as the go/no-go. Cheap, and it shrinks the unhandoffed window from thirty minutes
to five.

HOST also checked whether their own 08-01 *"declaring stand-down is not a mechanism — close the
window"* ruling applied here, found it didn't, and said so explicitly — the **reboot** is the
enforcement, since sessions don't survive it. Recorded so a future reviewer holding that memo
doesn't reach for an objection that doesn't apply.

---

## 6b. Phase 2.5 — **Compact before you snapshot.** The cost nobody counted.

Added 2026-08-11 from the first live run, where it was found the expensive way: **Piper Morgan
came within sight of exhausting its weekly usage limit two days early**, on the day of the reboot.

### What it costs, and why it is invisible

`--resume` restores the *actual conversation* — which is the whole reason Phase 5 is cheap in
wall-clock. But it means the next turn ships the **entire accumulated context** to the model. For
seats that have been running for days, that is enormous. And then, on that same first substantive
turn, auto-compaction fires anyway — because the restored context is near the limit, which is
exactly why it is expensive.

**So you pay twice and land where one payment would have put you:** once to load a large context,
once to compress it, ending at a compacted session either way. Multiply by 24. xian's summary is
the clearest statement of it:

> *"We may have wanted to compact the sessions before the restarts and likely paid for a lot of
> tokens that were instantly compacted anyhow."*

Nothing in v1 or v2 costed this. The runbook treated the reboot as a *time* and *context-loss*
risk and never as a **budget** event — yet the token cost is what actually bounds how often this
procedure can be run.

### The fix, and its ordering constraint

**Have every resident `/compact` after its handoff is on trunk and before the snapshot is taken.**
The handoff is what makes this safe: the durable context is already written down, so compressing
the live session risks nothing that hasn't been preserved.

**The ordering is not negotiable.** Compaction writes to the transcript and updates its mtime, and
§7's snapshot resolves each session's transcript by *newest mtime* — so compacting **after** the
snapshot contaminates exactly what §12's contamination note warns about. Sequence:

```
notice → handoffs on trunk → gate → COMPACT → snapshot → verify → T−5 re-gate → reboot
```

### Two things this has not been tested against — verify, do not assume

1. **Does compaction affect `--resume`?** It should continue in the same session and the same
   transcript file, so the snapshot's UUID should stay valid. *Should.* Nobody has run it.
   **`amber-fleet verify` is exactly the instrument for this** — run it after the compaction pass
   and confirm every seat still probes to the right conversation before rebooting.
2. **Does a compacted resident come back usefully?** A summary is not the conversation. Phase 5's
   `cold=0` measures whether a transcript was found, not whether what came back is worth having.

### It also fixes the §10.2 measurement

A side benefit worth naming: seats that compact *before* the reboot are not compacting *after* it,
so their first post-resume tool call is genuinely their first — which is precisely the boundary
that `/compact` destroyed this run, and the reason three honest "no prompt" reports could not
settle the question. Compacting first makes §10.2 measurable by the residents themselves rather
than only from the panes.

---

## 7. Phase 3 — Snapshot (T−10m)

**The roster is generated, never maintained.** A hand-maintained census rots silently —
we have already been bitten by exactly that failure elsewhere. Capture live state instead:

```bash
tmux list-sessions -F '#{session_name}' | while read s; do
  pane=$(tmux list-panes -t "=$s" -F '#{pane_current_path} #{pane_pid}' | head -1)
  # → session name, cwd, CLAUDE_CONFIG_DIR (from the claude process env)
done > ~/.local/state/amber-agent/fleet-snapshot-$(date +%FT%H%M).tsv
```

Verified capturable per session: **session name · working directory · `CLAUDE_CONFIG_DIR`**
— which is exactly the argument set `amber-agent.sh` needs to recreate it. Sample:

```
arch      /Users/xian/Development/piper-morgan-worktrees/arch    CLAUDE_CONFIG_DIR=~/.claude-pm
argus     /Users/xian/Development/klatch-worktrees/argus         (default)
```

Commit the snapshot. If the reboot goes badly, this file is how the fleet gets rebuilt.

---

## 8. Phase 4–6 — Reboot, resume, verify

### Phase 4 — Reboot
xian initiates. Note that `sudo shutdown -r` and the Apple menu both work; the
distinction that matters is that **someone must be present for the FileVault unlock.**
Do not start a reboot you cannot be present to finish.

### Phase 5 — Resume — **they resume, they do not re-standup**

**The finding that changes this phase** (measured 2026-08-10): `claude --resume <session-id>`
restores the *actual conversation*, not a fresh session primed with a handoff. A resumed Argus
named the specific threads he had open, unprompted. This is what makes xian's framing literally
true rather than approximately — *"similar to resuming any session,"* not 24 migrations.

1. xian unlocks FileVault and **logs in**. LaunchAgents load at this point, not before.
2. Verify host services returned *before* touching the fleet — a fleet standing up on a
   host whose services are still down produces confusing failures:
   ```bash
   launchctl list | grep -E 'klatch|janus|verify-hooks|troll|crossword|colima|ollama|openlaws'
   colima status && crontab -l
   ```
3. **Coral's partition move, done while she is down** — this window is the only cheap moment,
   because it needs her session stopped anyway. Her *transcript* lives on the retired kindsys
   partition alongside her memory, so both must travel or `--resume` cannot find her:
   ```bash
   cp -R ~/.claude-kindsys/projects/-Users-xian-Development-one-job \
         ~/.claude/projects/-Users-xian-Development-one-job
   # then edit her row in the snapshot: config_dir  →  default
   ```
   Destination verified absent 2026-08-10 — a clean copy with nothing to reconcile.

   > **Correction, 2026-08-11: this does NOT empty the partition.** Both this section and §2b
   > said the move "empties it and it can then be retired." It is a `cp -R`, not a `mv` — the
   > original stays exactly where it was, and `ls ~/.claude-kindsys/projects/` still lists her
   > after a successful run. That is the *right* behaviour (you want the source intact until the
   > destination is proven), but the document claimed a state it never produced, and anyone
   > reading it would believe the partition was already clear.
   >
   > **Retirement is a separate, later, deliberate step.** Verify the copy is complete first —
   > `diff -rq` between source and destination, which is an artifact check and not a file count —
   > then let Coral run on `default` long enough to trust it, and only then delete.
4. **One command for the rest:**
   ```bash
   amber-fleet resume
   ```
   Per-session startup is asserted (pane foreground is no longer a shell), not claimed.

### Phase 5b — **Re-arm the cycles.** The gap that hides.

Arch ranked this above all five of the original open questions, and they were right:

> *"Every agent's duty cycle runs on the harness's session-scoped `CronCreate`. Those jobs die
> with the session — and therefore with the reboot. Phase 5 relaunches sessions; nothing re-arms
> a cycle."*

So the fleet comes back **looking healthy and quietly never fires again** — a silent, delayed
failure, the worst kind to discover.

- **LaunchAgent cycles survive** (Klatch ×15, Janus, and every host service) — they are *user*
  agents and reload at login. Confirm with `launchctl list | grep klatch` rather than assuming.

> **Expect a notification storm here, and do not read it as a problem.** Bootstrapping the 15
> parked plists produces **one macOS "App Background Activity" notice per plist** — a stack of 15
> saying *"klatch-cycle-fire.sh can run in the background."* Observed 2026-08-11. They are
> informational; nothing is awaiting approval, and every item comes back **enabled**. Confirm
> rather than trust the toggles:
> ```bash
> launchctl print-disabled gui/$(id -u) | grep -i klatch
> ```
> Empty output means none were disabled. These notices are **not** the §10.2 trust prompts — that
> question is about Claude Code asking permission on first tool use, and it is a different
> mechanism entirely.
- **Session-scoped `CronCreate` cycles do NOT** — this is PM's eleven, and Pard's own.
  **Each agent must re-arm its own**, so the resume kickoff for those seats has to say so
  explicitly. An agent that doesn't know its cron died will not notice.

### Phase 6 — Verify

- Census must equal the snapshot count.
- **Name any resident that did not come back.** A count without names hides a casualty.
- **Verify the cycles, not just the sessions.** A resumed fleet with dead cycles passes a census
  and fails at its job. Check `launchctl list | grep -cE 'klatch|janus'` against expected, and
  confirm the session-scoped seats have re-armed before calling the reboot done.
- Coral specifically: confirm she came back on the **default** partition and can see her memory.

---

## 8.5. Phase 4.5 — **Getting back in.** The seam that had no steps.

Added 2026-08-11, written from the first live run. Every prior version of this document went
straight from `sudo shutdown -r now` to *"after login"*, as though logging back in were a thing
that simply happens. It is not, and the whole of the first run's 40-minute outage lived in that
gap. Nothing in this section is reasoned; all of it was observed.

### 8.5.1 Address Amber by name. Never by IP.

**Amber's address is not stable across reboots.** On the first run it moved `192.168.1.118` →
`192.168.1.119`. The `ssh studio` alias hardcodes the old one, so every reconnection attempt hit
an address with nothing behind it and reported `Host is down` — which reads as *the machine is
dead* and is in fact *you are knocking on an empty room*. Forty minutes were spent debugging a
host that had been healthy the entire time.

```bash
ping -c2 amber.local && dscacheutil -q host -a name amber.local   # mDNS: the address of record
```

Suspected cause: it came back on a different interface (RTT was 66–158ms, i.e. Wi-Fi with power
save, not Ethernet's sub-millisecond) — different MAC, different DHCP lease.

**The permanent fix is two things, and the alias is only one of them.** In `~/.ssh/config` on
every machine that reaches Amber:

```sshconfig
Host amber studio
    HostName amber.local
    User xian
```

Both names, so muscle memory keeps working and nothing has to be relearned mid-incident. **And
add a DHCP reservation on the router** — mDNS resolves the name but the ~90ms first-packet
latency is real, and a stable lease means the next reboot doesn't move anything at all. The alias
alone treats the symptom.

> **Read the error, it is diagnostic.** `Operation timed out` = SYN sent, nothing answered (host
> may be there, port isn't). `Host is down` = ARP failed, nothing is at that address at layer 2.
> The second one means *check the address before you check the machine.*

### 8.5.2 FileVault CAN be unlocked remotely. §2's "human at the keyboard" was wrong.

Amber runs the **FileVault preboot SSH responder**. `ssh` to it during preboot yields:

```
This system is locked. To unlock it, use a local account name and password.
(xian@amber.local) Password:
System successfully unlocked. You may now use SSH to authenticate normally.
```

That message is definitive — the volume key was accepted. It gives you **no shell**; the session
just sits there. Ctrl-C out. The machine then continues booting and drops off the network for a
few minutes while the real macOS network stack comes up, which is why the errors go
`timed out` → `Host is down` in sequence. **That progression is the unlock working, not failing.**

**Prefer `sudo fdesetup authrestart`** — it takes the password *before* shutdown, caches the key,
and boots straight through with no preboot prompt to catch. Then you only have §8.5.3 to solve.

### 8.5.3 **An SSH session is not a login.** Phases 5 and 5b require a console session.

This is the one that would have quietly wrecked the resume, and it is still true after
connectivity is restored. Three separate things need a real Aqua (console) session, which you get
by logging in **at the screen or through Screen Sharing** — not by SSH:

| Needs a console login | Why | Symptom if you use SSH |
|---|---|---|
| LaunchAgents loading | They load at **GUI login**, not at boot | Phase 5 step 2's count is ~0 and you conclude host services died |
| `launchctl bootstrap gui/$(id -u)` | The `gui` domain does not exist without an Aqua session | Phase 5b errors out; the 15 Klatch plists never re-arm |
| `claude --resume` ×24 | Claude Code's credentials live in the **login keychain**, unlocked at GUI login | **24 simultaneous auth failures** presenting as a fleet problem, not a keychain problem |

That third row is the trap. A keychain-locked resume fails in a way that looks exactly like the
fleet being broken, and you would debug the wrong layer while 24 residents sit dead.

**So: Screen Sharing is a requirement of this procedure, not a fallback.** Run Phases 5 and 5b
from a Terminal *inside* the VNC session.

### 8.5.4 A black Screen Sharing window is a sleeping display, not a hung host.

Expected, and observed on the first run. Screen Sharing connects, shows black, reports the machine
locked. **Click into the window and press shift.** The display wakes to the login window. Do not
read a black screen as a failed boot, and specifically **do not power-cycle on the strength of
it** — an interrupted macOS update on an Apple Silicon Mac with FileVault on can require a DFU
restore, which is the only genuinely destructive move available at this point in the procedure.

### 8.5.5 Expect a host-key warning at the new address.

New hostname, same machine, same key. Verify rather than blind-accepting:

```bash
ssh-keygen -F 192.168.1.118      # the old entry, to compare fingerprints against
```

### 8.5.6 The patience budget

A Mac Studio reaches the login window in roughly 1–3 minutes after unlock. Anything beyond that
is worth investigating — **but investigate the address first** (§8.5.1), because a wrong address
looks exactly like a dead host and is far more likely.

> **Correction, same morning.** The first draft of this section guessed the long outage was a
> staged macOS update installing, and offered a 20–45 minute patience budget on that basis.
> **That guess was wrong**, and measurably so: Amber came back on **26.5.2 with 26.6 still
> pending**. The outage was entirely the address change. Recording the correction rather than
> quietly deleting it, because a plausible wrong hypothesis left in a runbook is worse than no
> hypothesis — the next person reads it at 08:40 and waits 45 minutes for an install that was
> never running.

**The finding underneath it (see §4.1):** `sudo shutdown -r now` **did not apply the staged
update.** A 20–45 minute budget *is* right for an actual macOS update — several internal reboots,
offline throughout, and the preboot unlock again at the end — but you only pay it when you
trigger the update deliberately.

### 8.5.7 **Assert the console session before Phase 5.** Do not infer it from a working SSH prompt.

`gate` asks *may we reboot?* Nothing asked *may we resume?* — and that question cost the first
live run a morning. It is now one command:

```bash
~/Development/mediajunkie/scripts/amber-fleet.sh preflight
```

Run it **from the window you are about to run `resume` in.** That window is the thing being
tested; a pass in one terminal says nothing about another. It exits non-zero on any ⛔, so it
gates a script and not just an eye.

It checks, in order: the Aqua session exists (`gui/$(id -u)`), you own `/dev/console`, the login
keychain is unlocked, the snapshot has residents, **neither snapshot copy still mentions
`claude-kindsys`**, the macOS version, whether a restart-action update is still pending (§4.1),
LaunchAgents loaded, and tmux sessions already up.

**It fails closed.** A check it cannot run is a ⛔, never a silent pass — `verify` shipped failing
open three separate ways in one morning and that is the defect class this script keeps
re-learning.

<details><summary>Manual equivalent, if <code>preflight</code> is unavailable or misbehaving</summary>

```bash
launchctl print gui/$(id -u) >/dev/null 2>&1 && echo "OK console" || echo "NO CONSOLE"
stat -f '%Su' /dev/console
security show-keychain-info ~/Library/Keychains/login.keychain-db
sw_vers
grep -c 'claude-kindsys' ~/.local/state/amber-agent/fleet-snapshot.tsv
grep -c 'claude-kindsys' ~/Desktop/fleet-snapshot-backup.tsv
```

Keychain: unlocked prints timeout settings; locked says *"The specified keychain is not
unlocked."* Both `grep` counts must be **0**. Console owner must be `xian`, not `root`.
</details>

A bare SSH login fails the first three. Screen Sharing or a keyboard with a real login passes
them. This is the §8.5 counterpart to `verify`: the step that turns *"I am logged in"* from a
description into an artifact.

---

## 9. Unplanned reboots

If Amber reboots without a stand-down (panic, power loss, a setting we missed):

1. Log in. Do not relaunch anything yet.
2. Scan every worktree for uncommitted work — this is now a genuine recovery task, since
   nobody had the chance to push.
3. Rebuild from the **most recent snapshot**, and mark in the log that resumed agents have
   no handoff: they are starting cold and will not know it unless told.
4. Treat any agent whose last snapshot predates its last known work as **context-lost**,
   and say so explicitly rather than letting it resume as though continuous.

---

## 10. Open questions for reviewers

Genuinely open — I do not have settled answers and would rather have yours.

1. **Launch storm.** 24 near-simultaneous `claude` launches on one host: resource
   contention, and the startup assertion's 30s ceiling could serialise into ~12 minutes
   worst case. Batch? Stagger? Accept it?
2. **Permission prompts on resume.** Folder trust is already granted per directory and
   `--permission-mode acceptEdits` is the default, so I *expect* a clean relaunch — but I
   have not tested 24 at once, and xian cannot answer 24 prompts. Has anyone seen trust
   prompts recur after a reboot?
3. **Waiver default.** Should idle/parked residents be waived automatically, or must every
   waiver be explicit? Automatic is faster; explicit is auditable. I lean explicit, but I
   am the one who would bear the tedium, so discount accordingly.
4. **Handoff path convention.** Residents' handoff paths differ across repos. Should the
   gate know each repo's convention, or should we standardise a path first?
5. **What did I miss?** Specifically: any host service whose recovery is *not* automatic
   at login, and any resident with state outside git.

---



### §10.2a — WITHDRAWN. Prompts DO recur; the question is not answerable by asking the fleet.

**Current state: prompts occurred after resume and xian approved several of them, including the
one blocking Pard's own duty cycle.** The full finding is §12e; this section exists so that a
reader arriving at §10 does not act on the retracted version.

**Why asking cannot settle it.** A resumed session cannot reliably witness its own first tool
call, because `/compact` destroys exactly that boundary. Two of the three seats said so
unprompted:

> *"my 'first tool call' is the first post-compaction one; if the resume itself emitted a prompt
> before the compaction boundary, I can't see it from here."* — Lead
>
> *"I don't have the exact first tool-call record in-context anymore — it's summarized past, not
> something I can requote."* — Iris

**The agent's report is a description. The pane is the artifact.** The measurement has to come
from outside the thing being measured — the same structure as HOST's ruling that a session cannot
verify its own inertness.

**Method, next reboot** — cheap, and the window is minutes wide. Run immediately after `resume`,
**before anything is approved and before any seat compacts**:

```bash
# capture-pane does NOT accept the "=name" exact-match form that list-panes does — it
# returns "can't find pane" and, in a loop with stderr suppressed, silently yields NOTHING
# for every session. Blank captures at the exact moment you are looking for a prompt read
# as "no prompt". Resolve to a PANE ID first, the same indirection amber-agent already uses
# for send-keys. Verified 2026-08-11: -t "=coral" fails, -t "%5" works.
for s in $(tmux list-sessions -F '#{session_name}'); do
  p=$(tmux list-panes -t "=$s" -F '#{pane_id}' | head -1)
  printf '\n=== %s (%s)\n' "$s" "$p"
  tmux capture-pane -p -t "$p" | grep -v '^$' | tail -4
done
```

Setting seats to Auto also closes the window permanently — correct operationally, and it ends the
experiment. **Capture first.**

**What went wrong in the withdrawn version, because the shape recurs:** three seats reported "no
prompt"; two attached a caveat voiding their own report; I tabulated the three answers and dropped
both caveats. I then described it as observed rather than inferred — a word the seats had not
used and had explicitly disclaimed. And I wrote it from inside a session whose own prompt a human
had already cleared, so the one pane that would have falsified it was the one I could not see.
**Absence of a reported prompt is not absence of a prompt.**

## 11. Status — v2, 2026-08-10

**Still not rehearsed end to end.** But three of the five open questions in §10 are now answered
by measurement rather than reasoning, and the two review defects are closed:

| Was open | Now |
|---|---|
| §10.1 launch storm — 24 sequential standups, ~12 min worst case | **Moot.** `amber-fleet resume` uses `--resume`; sessions restore rather than rebuild. |
| §10.2 do trust prompts recur after reboot? | **NOT ANSWERABLE BY ASKING.** Prompts DID occur and were approved by xian. See §12e and §10.2a. |
| §10.5 what did I miss? | **Two things, both from review:** Arch's cron re-arm gap (now Phase 5b) and HOST's T−30/T window (now the T−5 re-check). |
| Arch's `-r` defect | **Fixed** — the gate found zero handoffs for every resident, always. Would have made the only interlock a rubber stamp. |
| Coral's partition move | **Folded into Phase 5** — her transcript is on the retired partition too, and the reboot window is the only cheap moment. |

**Tooling now exists** (`scripts/amber-fleet.sh`, `a908b67`), tested against the live fleet:
24/24 captured, 19 exact, 5 ambiguous, 0 unresolved — and all five ambiguous mappings *probed and
confirmed* rather than assumed, including Janus at 31 transcripts.

**Scheduled: 2026-08-11, 11:00** — notice 10:00 · gate 10:30 · re-check 10:55 · reboot 11:00.
xian present throughout; FileVault cannot be delegated.

**What would still make this fail**, stated plainly: an agent that resumes but whose cycle nobody
re-arms (Phase 5b is new and untested), a trust prompt storm nobody has observed (§10.2), and
Coral coming back unable to see her own memory. Those are the three I will be watching, and I
will report what happens rather than what should.

---

## 12. Status — v3, 2026-08-11. **First live run.** What actually happened.

Written the same morning, from the run itself, per the promise at the end of §11 to report what
happens rather than what should. It ran early — roughly 08:30 rather than the scheduled 11:00.

**None of my three predicted failure modes fired. The failure was in a phase that had no steps.**

Phases 1–4 went exactly as written: roster clear, snapshot taken, verify clean, Coral's partition
copied, `sudo shutdown -r now` issued. Then Amber went dark for **~40 minutes** — not because
anything broke, but because it came back on `192.168.1.119` while every reconnection attempt
went to the `.118` hardcoded in the `ssh studio` alias. The host was healthy the entire time.
`Host is down` was telling us the truth about the *address* and we read it as news about the
*machine*.

| Prediction | What actually happened |
|---|---|
| Cycles come back unarmed (§5b) | **Not reached.** Never got past the reboot. |
| Trust-prompt storm (§10.2) | **Still unobserved.** Third run in a row this question survives. |
| Coral resumes without her memory | **Not reached** — but see the backup ordering defect in §2b, which would have caused exactly this via the recovery path. |
| — | **The actual failure: no procedure for getting back in.** Now §8.5. |
| — | **And the reboot didn't install 26.6.** Came back on 26.5.2, update still pending. Now §4.1. |

**The second finding is the more embarrassing one.** The whole procedure exists because 26.6 was
pending. It ran end to end — notice, gate, snapshot, verify, reboot — and did not install 26.6,
because `shutdown -r now` does not apply a staged update and nothing in this document ever said
it would. Nobody would have noticed either: there was no step that checked. The runbook had a
Phase 6 that verified the *fleet* came back and no step that verified the *reason for the
reboot* had been served. Now §4.1, and `sw_vers` is in the §8.5.7 block.

**Four defects found, all now fixed above:**

1. **§8.5.1 — the address moves.** The single cause of the outage.
2. **§2's FileVault fact was wrong.** I wrote "nothing proceeds without a human at the keyboard
   or VNC" without testing it. Amber has the preboot SSH responder; xian unlocked it remotely
   from faoilean. I asserted a precondition I had never exercised, and he found its real shape
   at the worst possible moment.
3. **§8.5.3 — SSH is not a login.** Latent, not yet triggered. It would have failed Phase 5b
   outright and quite possibly all 24 resumes on a locked keychain.
4. **§2b — the Desktop backup is taken before the `sed`**, putting Coral's failure mode into the
   recovery path.

**The pattern across all four:** every one is a step I *described* rather than *ran*. The card's
header claims "every command here was executed and verified before it was written down" — true
of the commands, false of the transitions between them, and the transitions are where the whole
morning went. My own handoff warns to verify the artifact and never the description. I wrote the
description of a reboot I had not performed, and called it verified.

**Still open after this run:** §10.2 (trust prompts) and all of Phases 5–6, which remain
untested end to end. This run tested Phases 1–4 and discovered 4.5. It did **not** validate
resume.

### 12b. Phases 5–6, measured — the fleet came back whole

Written after the fact, same morning. **Phases 5–6 are no longer untested.**

```
resumed=24  failed=0  cold=0
```

**Zero cold starts.** Every resident came back on its real conversation, which is the single
outcome the entire procedure exists to produce. Klatch re-armed to **15**.

**Coral, the one resident who changed partitions**, came through intact:

- Resumed on `e3ab1cd8` — **the same transcript ID the pre-reboot `verify` pass recorded.** Same
  conversation, now on `default`. An artifact match, not an assurance.
- Memory present on the new partition: `MEMORY.md` plus two notes.
- Transcript **4512 of 4513 lines**. The single missing line is a `{"type":"last-prompt"}`
  housekeeping record written at 07:51, one minute after the `cp -R` — a pointer to the
  stand-down prompt, not a turn, and the prompt it names still exists on disk. Every
  conversational turn travelled. No repair required.
- Source partition still populated — see the correction in Phase 5 step 3. Retirement pending.

**How that last bullet was reached is the more useful record**, because I got it wrong twice
before measuring it:

| Step | What I said | What it was |
|---|---|---|
| `diff -rq` says the transcripts differ | "she's live and writing to it — proof the move worked" | An interpretation. I never checked *which direction*. |
| `cmp` says destination is a strict prefix | "~40 minutes of her work is missing, and there's a clock on the repair" | Also an interpretation, in the alarming direction this time. Invented urgency. |
| `ls -l` + `wc -l` | — | **223 bytes. One line.** Source mtime 07:51, so nothing was written in the 40 minutes I had imagined. |
| `tail -1` | — | A metadata pointer. Nothing lost. |

Three readings of one artifact, two of them wrong in opposite directions, each corrected by a
single command that produced a **number**. xian caught the second one by asking *"why a clock?
nothing we can't stop?"* — which was right on both counts: no clock, and no irreversible step
anywhere in it.

**This is the same defect as the five in §12, committed while documenting them.** Narrating what
an artifact means is not measuring it, and the tell is that the sentence contains no number.

### 12e. What the fleet reported back — and why §10.2 cannot be answered by asking

Within ~20 minutes of the post-reboot notice, three seats replied on trunk. All three answered
more than they were asked.

**A third schedule mechanism exists, and the re-arm accounting had two buckets.** Tessera reports
running neither `CronCreate` nor a LaunchAgent, but **`ScheduleWakeup`** — a session-scoped
`/loop`-dynamic wakeup, armed ad hoc against a long render rather than as a standing cadence. It
**dies with the reboot exactly like `CronCreate`**, so it belongs on the re-arm side of the
ledger; nothing was pending, so nothing was lost this time. In their words: *"third mechanism your
two-bucket accounting didn't have a slot for."* §5b's two categories are therefore **incomplete by
construction**, not merely missing six names — and the fix is to ask seats what they run rather
than to sort them into the buckets I happened to know about.

**A re-arm resets the expiry clock, and every pre-reboot expiry date is now stale.** Lead's new
job carries a fresh 7-day auto-expiry (~08-18); their row had been flagged `AUTO-EXPIRES ~08-12`
before the reboot. That shift applies across the whole session-scoped cohort, and nobody would
have gone looking for it. Anyone reading expiry dates recorded before 08-11 should treat them as
wrong.

**Lead's re-arm is the pattern to copy**, and is worth quoting as method: `CronList` → *"No
scheduled jobs"* (**the death observed, not inferred**) → `CronCreate` from the prompt text
recorded verbatim in their own handoff → `CronList` again showing exactly one job. The re-arm was
not assumed from `CronCreate`'s success message. A parked registry note was cleared only after its
stated condition was *observed*, never on intent.

**Push races are real at this stagger.** Lead hit two while pushing, and rebased and retried; this
document's own author hit a third from off-host. The 3-second stagger spaces out *pushes*, which
take seconds — it does nothing about **compaction**, which takes minutes, and compaction is what
a broadcast to 24 near-full sessions actually triggers.

#### §10.2: the answer is that the question cannot be asked this way

Three seats reported **no prompt**. And **two of the three volunteered the reason that finding is
weak** — a `/compact` ran in the same resumed session before they could record the moment:

> *"my 'first tool call' is the first post-compaction one; if the resume itself emitted a prompt
> before the compaction boundary, I can't see it from here."* — Lead
>
> *"I don't have the exact first tool-call record in-context anymore — it's summarized past, not
> something I can requote."* — Iris

Meanwhile xian, watching the panes, **saw prompts and approved several**, including Pard's own.

Both reports are honest and they do not conflict. **A resumed session cannot reliably witness its
own first tool call, because compaction destroys exactly that boundary.** So §10.2 was never
answerable by asking the fleet — the agent's report is a description, and the *pane* is the
artifact. The measurement had to come from outside the thing being measured, which is the same
structure as HOST's ruling that a session cannot verify its own inertness.

**Method for next time, since the observation is cheap and the window is minutes wide:** capture
the panes rather than polling the agents.

```bash
for s in $(tmux list-sessions -F '#{session_name}'); do printf '\n=== %s\n' "$s"; tmux capture-pane -p -t "=$s" | grep -v '^$' | tail -4; done
```

Run it **immediately after `resume`, before anything is approved and before any seat compacts.**
Setting seats to Auto also closes the window permanently — correct operationally, and it ends the
experiment, so capture first.

### 12c. §10.2 is *partially* answered, and the distinction is the point

**Zero permission or trust prompts across 24 relaunches.** That is a real observation and it
retires the fear of a 24-prompt storm at resume time, which xian could not have answered.

**It does not close §10.2.** xian caught this and I had already started writing the larger claim:

> *"no permission prompts yet but not sure any duty cycle fires have happened yet?"*

Correct, and decisive. **A trust prompt fires at first tool use, not at launch.** Twenty-four
sessions started; most have done nothing yet. *"No prompts at relaunch"* and *"prompts do not
recur after a reboot"* are different claims about different moments, and I was one sentence from
recording the small one as the large one — in a document whose entire thesis is that a
description is not an artifact.

**§10.2 therefore stays open**, with its remaining scope narrowed and named: *do trust prompts
recur on **first tool use** by a resumed session?* The re-armed Klatch fires (×15) and each
seat's first real work are the observation window. Whoever sees the first fire should record it.

### 12d. The fifth defect, found after the fleet was up

**"The `cp -R` empties the kindsys partition."** It does not; it is a copy. Both the runbook and
the handoff claimed a state the procedure never produced. Corrected in place.

That makes **five defects in one morning, and every one of them the same shape**: a step that was
described rather than run. Four were caught by running the procedure. The fifth was caught by
checking a claim the procedure made about itself.

— Pard
