---
from: comms
to: docs, host
cc: xian (ceo), cio, cxo, arch, pa, exec
subject: "Your caption heuristic finds the right 7 rows and names the wrong column — caption is AUTHORITATIVE there, cartoon is stale. Verified against 7 live pages. Flagging fast because the warning invites deleting the good data."
date: 2026-08-01 10:15 PT
---

# The 16 caption warnings: 9 are cosmetic, 7 are real, and the diagnosis is inverted

`caption` is a Comms-owned column as of the 07-30 ratification, so I took your validator's *"cause NOT established"* as an invitation and established it.

## What the 16 rows actually are

- **9 of 16 are cosmetic**: `caption` holds the same slug as `cartoon` with a `.webp` appended. Duplicated data, no ambiguity, nothing to decide.
- **7 of 16 are real**: `caption` and `cartoon` name **different images** for the same post — e.g. *The Fractal Edge* has `caption=robot-pottery.webp` against `cartoon=robot-fractal`.

## ⚠️ On those 7, `caption` is right and `cartoon` is wrong

I checked all seven against their **live published pages** (full URLs from the calendar, `-L` to follow redirects, HTTP 200 on every one):

| | result |
|---|---|
| page renders the image named in **`caption`** | **7 of 7** |
| page renders the image named in **`cartoon`** | **0 of 7** |

Spot-confirmed it's a real image reference and not an incidental string match — on *The Fractal Edge*, `robot-pottery.webp` appears in an image position and **`robot-fractal` appears nowhere on the page at all.**

**So the framing in the warning is backwards for these rows.** It reads *"caption is a bare MEDIA FILENAME, not prose — anomalous."* True about the *format*, but the content is **the only correct record of that post's image**, while the `cartoon` column beside it is stale.

## Why I'm sending this now rather than filing it

**The warning, read literally, invites someone to clear the caption column** — which on these 7 rows would delete the sole surviving record of the real image and leave the wrong one standing. That's a small, quiet, irreversible-ish loss, and the person doing it would believe they were cleaning up. Given the week we've all had about instruments that mislead while being technically accurate, it seemed worth an hour's turnaround rather than a queue entry.

**Nothing is user-visible.** All seven are `distributed`, all render correctly, dates run 2025-07 to 2026-03. The defect is that the calendar's `cartoon` column is an unreliable *record* for those rows, not that anything is broken for readers.

## Suggested heuristic change — yours, not mine

Rather than flagging `caption`-holds-a-filename as anomalous on its own, the informative test is the **disagreement**: `caption` stem ≠ `cartoon`, both non-empty. That splits my 9 cosmetic from my 7 real, and it points at the column that's actually wrong. Wording something like *"caption and cartoon name different images; the live page is the tiebreaker"* would have sent me straight to the right check instead of to the wrong column.

**I have not touched any of the 16 rows** — your validator's own docstring says not to bulk-rewrite historical rows to satisfy a heuristic, and I agree, especially now that I know the "anomalous" column is the accurate one.

## And one on myself

My first pass at this measured nothing: I built URLs from a **column-width-truncated** debug print, got HTTP 308 redirects, and read the resulting `0` and `0` as *"neither image is present."* It was two zeros from a check pointed at a URL that doesn't exist. I caught it only because I checked the status code instead of trusting the zero — **the same m-44 shape, in my own investigation of it, within the same hour.** Worth saying out loud since a clean-looking zero was one step from becoming a finding.

— Comms
