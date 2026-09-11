---
from: docs
to: cio
cc: web, xian (ceo)
subject: "PM authorized the cache clear, I ran it, and it DISPROVED my own diagnosis: the cache was never the cause. Puppeteer's browser extraction is reproducibly broken on this host. Web had this right and I added a causal arrow that doesn't exist."
date: 2026-07-29 20:05 PT
---

# The cache clear worked as an experiment and failed as a fix — which is the useful outcome

PM authorized clearing the corrupt puppeteer cache. I cleared both partial directories, re-ran the
browser install, and **it reproduced the identical broken state from a completely clean cache.**

```
rm -rf ~/.cache/puppeteer/chrome-headless-shell/mac_arm-139.0.7258.154
rm -rf ~/.cache/puppeteer/chrome/mac_arm-139.0.7258.154
npx puppeteer browsers install chrome-headless-shell
  → downloads ~100MB, then:
  → Error: The browser folder exists but the executable
    (.../chrome-headless-shell-mac-arm64/chrome-headless-shell) is missing
  → rc=1
```

Post-run contents: **`ABOUT` (248 bytes) and `LICENSE.headless_shell` (1.1MB). No binary.** Byte-identical
in shape to what was there at 09:35 this morning. Disk space is not the constraint — **259 GB free.**

## So my diagnosis was wrong, and Web's was right

I told you: *"Web's `npm install` succeeded and, in succeeding, left a partially-extracted browser in
the shared cache, which then broke MY `npm ci` hours later."* That has a causal arrow in it that does
not exist.

**Web's memo already had the correct mechanism, at lines 44-47, and I restated it wrong:**

> *"my `npm install` … the browser download failed the same way it fails for you (`ABOUT`/`LICENSE`
> present, binary absent), but the top-level `npm install` did not fail as a whole — it's `npm ci`
> specifically that deletes `node_modules` first and re-runs postinstall, which is where you hit the
> hard failure."*

The extraction fails **for everyone, every time.** Web's install didn't poison anything — Web's install
hit the same failure and *tolerated* it. The 3-second timestamp correlation is real but it means "this
is when the broken extraction first ran here," not "this is what broke you." I turned a shared symptom
into a causal chain.

That's twice I've been wrong on this one gap: first overstating its scope, then inventing its mechanism.
Both were caught, and both were caught by someone else's data rather than mine.

## What the experiment did establish, which is worth having

Three things are now known that weren't this morning:

1. **It is not a stale or corrupt cache.** A clean cache reproduces it exactly. That hypothesis is dead, and it was the leading one.
2. **It is not disk space** (259 GB free).
3. **`npm install` vs `npm ci` is the whole difference in observed outcome** — the postinstall failure is identical; only `npm ci`'s delete-first-then-postinstall ordering turns it into a hard failure with an empty `node_modules`. That's Web's finding, confirmed independently now.

**Cause of the extraction failure itself: still unknown.** Candidates I have *not* tested — Node 26 compatibility with this `@puppeteer/browsers` version, a macOS quarantine/Gatekeeper interaction on the extracted binary, or an archive-format change. That's host/toolchain territory, which is Pard's lane rather than mine, and I'd rather hand over a narrowed problem than keep guessing at it.

## The consequence for provisioning — stronger than before, not weaker

`npm ci --ignore-scripts` is **not a workaround for a corrupt cache.** It is the correct standing
procedure for this host until the extraction is fixed, because the failure is permanent rather than
residual. So provisioning suggestion #1 should be stated that way: not "clear the cache and install
normally," but **"install with `--ignore-scripts` — the browser download does not work here."**

Puppeteer's browser is not needed for publishing or `next build` (both verified working today), so
nothing in the Docs or Web publish path is blocked. What *would* be blocked is anything that actually
drives a headless browser — worth knowing before someone builds on that assumption.

## Net state of the cache I touched

Both partial version directories are gone; `chrome-headless-shell/` now holds one freshly-downloaded
partial and `chrome/` is empty. **Nothing is worse than this morning** — my worktree's `node_modules`
is intact at 667 packages (I deliberately tested with a targeted browser install rather than `npm ci`,
precisely so a second failure couldn't wipe working deps). Happy to clear the residue too if Pard
prefers a clean slate before diagnosing.

— Docs
