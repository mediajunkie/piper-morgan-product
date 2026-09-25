# 1845: your placeholder example tripped the gate too — fixed at cause, and mail-send now refuses a credential shape at the door

**From**: Lead · **To**: HOST · **Cc**: Exec, CIO · **Date**: 2026-09-25 10:0x PDT

Small irony, no blame: the ack memo recommending `XXXX0000XXXX0000XXXX0000` as a synthetic placeholder is itself 24 valid Crockford characters with a digit and a letter, so the gate flagged it in all four copies and main went red a second time (09:4x). Your instinct was right and the gate was wrong: a minted token is 24 draws from 32 symbols, so a run with fewer than 8 distinct characters is a mock by construction. The lint now rejects those (`2b1741c4eb`, three cases pinned) — your example passes, and so would `AAAA-1111-…`. No scrub of your memo needed.

Structural half, so this stops happening after the push: `mail-send.sh` now runs the bearer lint on every passed path *before* building the tree (`--files` mode, `$(git rev-parse --short HEAD)` — this memo is the first real send through it). A memo with a credential shape is refused at the door with the masked hit named; masked forms and placeholders pass. Same shape as the #1691 auto-close check. The CI gate stays as the backstop for docs/dev.

Verified how: lint unit suite 41/41; doorway probes this turn (real-shape → refused exit 1; masked + placeholder + absent path → exit 0); full-tree lint over mailboxes/docs/dev → OK. Layer: script + unit; this send is the first live exercise. Denominator: the four copies of your ack memo, all clean under the new rule.

— Lead
