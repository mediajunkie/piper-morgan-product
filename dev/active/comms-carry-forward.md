# Comms carry-forward — 2026-08-02 STOP (21:12) → for the Aug 3 START

**Host**: Amber.local · **Model A** `~/Development/piper-morgan-worktrees/comms` · `claude/comms-cycle`
**Session log**: `dev/2026/08/02/2026-08-02-0642-comms-code-log.md` — `DAY-CLOSED: 2026-08-02` ✓
**Cron**: re-armed at STOP by delete-then-create (id transition in the registry row)

---

## First thing Monday — CHECK THE CALENDAR, it has earned it twice

Two days running, the START calendar check found an unstaged post that would otherwise have been missed. **Next scheduled post is Tue Aug 4, "The List That Lies"** (building). Expect the same state: not voice-passed, no art. Get ahead of it Monday rather than discovering it Tuesday morning.

## Open for PM — 4 items, one dated

1. ⚠️ **Beats 24-28 slate steer — the only dated item.** Queue runs dry after **Aug 18**. Persistent artifact: **`docs/internal/planning/comms/upcoming-beats-plan.html`** (durable home — the working proposal in `dev/active/` is sprint-cleaned). Needs: **5 or 4**, titles (**Beat 25 needs one regardless**), spine.
   ⚠️ **The era question is entangled with this** — if Era 2 splits at the late-July always-on-host move, that is *this slate\'s material*, and "last beat of an era" is a different piece from "one more beat." **Worth deciding before Beat 28 is drafted.**
2. **Beats 21-23 voice-pass + art** — Aug 11 / 13 / 18.
3. 🔧 **`/hooks` open or session restart** — HOST\'s memory counterweight is written, registered, **not live**. It `wc`s at fire time so it does not share a failure mode with the unreliable built-in counter.
4. **Compose-UI restore-banner observation** — wipe path fixed; restore path still unobserved.

## Open for Web/PM (raised by PM 2026-08-02)

- **Series era split.** My POV in the artifact: Era 2 has absorbed **107 posts over 6 months** and 3 distinct working models — overdue. Seam I would argue for: the **late-July move to the always-on host**, because that is when the working model actually changed.
- **Featuring the current post on the blog index.** ⚠️ I could **not** verify the rendered page — it is client-rendered, so a fetch returns a shell. **No layout opinion offered.** Editorial case is strong and partly a syndication artifact: narratives skip LinkedIn, Ships skip Medium, so some readers only ever meet a post on the site. **Web should establish whether the index is a real entry point or whether arrivals are mostly deep links** — measurable, and it decides how much a hero is worth.

## Editorial state

- ✅ Published and verified live: **Mechanism Beats Vigilance** (8/1) · **You Can\'t "White Knuckle" Structural Problems** (8/2). Retroactive teaser on the 8/1 page fixed by Docs after PM retitled.
- **PM cut the overlapping section independently** — 1,437 → **1,025 words**, first post inside the 800-1,300 target in the recent run, and it resolved the Aug1/Aug2 redundancy.
- **§1.5 in force** (`building-narrative-method.md`): a beat is a STORY, not a digest. A plot, optional B plot, something odd — **not a section per workstream**. Measured: span does NOT predict length (r=+0.10), so leaps and cuts are not in tension.
- **BYOC marketplace narrative** — ~6 weeks stale, PM-gated.

## Live hazards (know about them)

- **Two write paths collide.** PM\'s browser can revert agent commits by saving from a stale page — cost three fixes on 8/1. **Distinct from the autosave bug Web fixed.** After PM edits, **re-read before assuming your fix survived**.
- ✅ **Blog art `*.png` gitignore gap FIXED 8/2** (`5b03cc793`). It hid because the admin UI writes via the GitHub API and bypasses local gitignore. Rules 96-98 still point at `docs/comms/blog/`, which does not exist — annotated, not deleted.
- **16 calendar rows have a media filename in `caption`; on 7 caption is AUTHORITATIVE and `cartoon` is stale** (verified live 7/7 vs 0/7). ⚠️ **Do not "clean up" that column.**
- **Omnibus gap**: latest is **2026-07-28**. Those digests are the input to the narrative-front assessment; without them the next one reads ~50 session logs. Flagged to Docs as a dependency, not a request.

## Habits (apply, don\'t just recall)

- ⚠️ **A check that returns cleanly tells you nothing about WHAT it measured.** Four instances on 8/2 alone: wrong machine, reused script hardcoded to another file, 13-commits-behind checkout, and a scan counting build artifacts as "stale rules." **The tell every time was a result contradicting something I already knew** — treat that as data about the instrument.
- **File without a theory when it is outside your lane.** The config finding routed correctly *because* I did not diagnose it; my diagnosis would have been wrong.
- **mail-send: derive the path list from `git status` after the regen**, not from the loop that moved files. (zsh: no `mapfile`; use `${(f)"$(...)"}`.)
- **Verify at the published layer, not the status flag.** Four publishes running.

## State flags

- STOPped cleanly, day fully accounted for. Inbox **zero** (8 memos triaged).
- Queue at close: **(0 unblocked, 4 PM-gated + 2 Web/PM)**. Nothing unblocked held.
- First fire tomorrow **06:12**.
