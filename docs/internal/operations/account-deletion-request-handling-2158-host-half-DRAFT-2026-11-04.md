# Account deletion by email (#2158): HOST's half of the procedure (DRAFT)

**Status:** draft, 2026-11-04. The data half (which tables soft-delete, what `scripts/erase_user.py` covers, how long snapshots keep a deleted account) is Lead's, reviewed by Arch. This half is the request handling. xian's 10-13 ruling: deletion by email within 14 days.

## Steps

1. **A request arrives** at the project's address, or reaches xian. xian forwards it to HOST in the HOST conversation. HOST does not read the mailbox for this.
2. **Log it privately.** The requester's name, address and the date go in the private roster only, never in this repo (hard rule 8). The repo log says "a deletion request" and the day.
3. **Start the 14-day clock** on the day of the request. HOST writes the due date in the private roster and an `OWED[key: deletion-<n>; to: host; by: <date>]` marker in the session log without any identity.
4. **Check identity.** The request must come from the address on the account, or xian confirms the person to HOST. If neither, xian asks the person to write from the account address. Nothing is deleted on an unconfirmed request.
5. **Hand the data half to Lead** by mail with only the Piper account id (found from the roster mapping), not a name or address. Lead's data half runs `scripts/erase_user.py` (count first, then `--erase --confirm <id>`, then a re-count) and records the snapshot horizon, the erase date plus 5 days. The two soft-delete tables are hard-deleted by its plan.
6. **Confirm back.** When Lead reports done, HOST tells xian, who replies to the person. Sends are xian's hand.
7. **Say plainly what remains.** Backups: a deleted account can survive in snapshots for their retention (5 days: Fly's default, recorded on this volume; Lead's data half, `account-deletion-data-half-2158-DRAFT-2026-11-04.md`). The reply to the person should say so in a sentence.
8. **Close.** Mark the roster entry, close the `OWED` marker with `OWED-CLOSED[key: ...]`.

## What the person is told (for xian's edit)

> We have deleted your Piper Morgan account and the data in it. Backups can hold a copy for up to 5 days, after which it is gone. If you connected GitHub, Piper's Disconnect does not revoke the grant there, so please also revoke Piper under your GitHub settings, Applications, Authorized OAuth Apps. If you didn't ask for this, write to us right away.

(5 is Lead's figure. The GitHub sentence comes out when #2178 lands. Lead's data half also lists what the purge does not reach: GitHub's own copies, application logs, and the MCP app's state, which is unverified.)

## Not decided here

Whether in-product deletion replaces this later (that stays Production), and whether identity check needs more than the account address.
