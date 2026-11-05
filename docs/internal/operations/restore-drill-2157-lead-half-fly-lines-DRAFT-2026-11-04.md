# Restore drill (#2157), Lead's half: the ordered `fly` lines for xian — DRAFT 2026-11-04

**Status:** draft, prep only (Exec 16:34). Nothing runs before xian's yes to CIO's five. HOST's half (rules, timing, logging, stop conditions): `restore-drill-2157-runbook-host-half-DRAFT-2026-11-04.md`. Arch's safe form (decisions.log 2026-11-04 16:38): a **new** Postgres app from a snapshot of `piper-morgan-db`, never a machine or volume inside it, never over alpha or staging; no Piper app boots against the copy; proofs print counts, one id and `ok`/`fail`; destroy and read back in the same sitting.

**Flags checked against Fly's own reference** (`docs.fly.io/flyctl/postgres-create`, read 2026-11-04 16:46 PT from this seat, which runs no `fly`): `fly postgres create` takes `--snapshot-id string` ("creates the volume with the contents of the specified snapshot"), `--name`, `--org`, `--region`, `--initial-cluster-size`, `--vm-size`, `--volume-size`, `--flex` (default true), `--password`. Snapshot ids come from `fly volumes snapshots list <volume id>`; a volume made from a snapshot must be at least the original's size; snapshots keep for 5 days by default (1 to 60 configurable; a change applies to new snapshots only). `--fork-from <app>:<volume>` also exists, but it forks the LIVE volume and proves nothing about snapshots, so it is not the drill.

**Every value is filled in except what only xian holds:** his org name (`fly orgs list`), the volume id and snapshot id the reads print, and the drill app's password, which the create prints once. The password is never pasted into mail or a log.

One line at a time, in the HOST conversation. HOST notes the clock at each step.

**Never `fly postgres attach` the drill app to anything** (Arch 18:34): attaching sets `DATABASE_URL` on the target app and restarts it, which would boot Piper against the copy. If a line not in this list seems needed, stop and report.

**Where each line is typed (HOST's handling point, 16:54, agreed):** step B (the create), proof 2's shell-2 line and proof 4 (the decrypt command) carry the copy's password, which Fly prints once; xian runs those two in **his own terminal** and pastes here only what they print: the create's success line without its credentials block, and `ok` or `fail`. Every other line carries no secret and is typed here with the `!` prefix as usual. The password is never pasted anywhere; it dies with the app in step D.

## A. Read what exists (no change)

```
fly volumes list -a piper-morgan-db
```
Note the volume id (`vol_…`) and its size in GB. One volume is expected.

```
fly volumes snapshots list <vol_id> -a piper-morgan-db
```
Note the newest snapshot id (`vs_…`) and its created-at time. **That time is proof 1's "created-from snapshot time".** If the newest is older than a day, say so; the drill still proceeds (it proves the mechanism, not the cadence).

```
fly orgs list
```
Note the org slug that owns `piper-morgan-db`.

## B. Create the copy as a NEW app (the one write)

```
fly postgres create --name piper-morgan-db-drill --org <org-slug> --region sjc --snapshot-id <vs_id> --initial-cluster-size 1 --vm-size shared-cpu-1x --volume-size <size GB, at least the original's>
```
It prints a superuser password and a connection string once. xian keeps them for this sitting only. If the command refuses `--snapshot-id` (the reference lists it, but a flex cluster's behaviour is unverified from here), **stop and report the exact error**; do not fall back to `--fork-from`, which would not be a snapshot restore.

## C. Proofs, in HOST's order

**Proof 1, the copy exists from that snapshot:**
```
fly status -a piper-morgan-db-drill
fly volumes list -a piper-morgan-db-drill
```
A started machine and one volume; HOST pairs the volume's create time with step B's clock and names the snapshot time from step A.

**Proof 2, `alembic current` on the copy matches alpha's.** Alpha's own reading first (a read inside the live container, the prod-exec shape):
```
fly ssh console -a piper-morgan -C "alembic current"
```
Then the copy, from xian's Mac in a checkout of the sha alpha serves (the migration tool only; no Piper app starts). Shell 1, left running:
```
fly proxy 15434:5432 -a piper-morgan-db-drill
```
Shell 2, **in xian's own terminal** (it carries the drill password; Arch 18:34), and it sets `ALEMBIC_DATABASE_URL`, the name `get_sync_migration_url` reads first, so a stray `DATABASE_URL` in his shell cannot point the proof at another database:
```
ALEMBIC_DATABASE_URL="postgres://postgres:<drill-password>@localhost:15434/piper_morgan" venv/bin/alembic current
```
Only the printed revision id is pasted here. The two revision ids must match.

**Proof 3, counts and one id**, on the copy:
```
fly postgres connect -a piper-morgan-db-drill -d piper_morgan
```
then, at the `psql` prompt, exactly these:
```
SELECT count(*) FROM users;
SELECT count(*) FROM conversations;
SELECT count(*) FROM conversation_turns;
SELECT count(*) FROM user_api_keys WHERE is_active;
SELECT id, created_at FROM users ORDER BY created_at LIMIT 1;
\q
```
Then the same five on alpha, for the comparison (reads only; alpha's counts may be higher by what was written after the snapshot):
```
fly postgres connect -a piper-morgan-db -d piper_morgan
```
Only counts, one id and one timestamp are pasted. No other column.

**Proof 4, one stored credential decrypts under the deployment's key.** Run inside alpha's container (it holds `ENCRYPTION_MASTER_KEY`), pointed at the copy over the private network; it prints `ok`, or `fail:<code>`, and nothing else. `--database-url` is required, and the script refuses (`fail:5`) a URL whose host is the container's own live database, so a dropped or mis-quoted flag can never prove alpha instead of the copy (Arch 18:34):
```
fly ssh console -a piper-morgan -C "python /app/scripts/verify_stored_credential_decrypt.py --database-url postgres://postgres:<drill-password>@piper-morgan-db-drill.flycast:5432/piper_morgan"
```
**Precondition:** the script must be in alpha's image (it lands with the next promotion after it reaches main; HOST checks the served sha against the commit before the sitting). `fail:2` means the copy holds no encrypted row (then proof 4 is vacuous, say so); `fail:1` means the key does not open the row (the real finding this drill exists to catch); `fail:3` means the container has no key (stop, that is a separate incident); `fail:4` the copy could not be read (check the private address and the password); `fail:5` the URL pointed at alpha's own database (re-type it).

## D. Cleanup, same sitting

```
fly apps destroy piper-morgan-db-drill --yes
fly apps list
fly volumes list -a piper-morgan-db
```
HOST quotes the last two reads: no `piper-morgan-db-drill` in the app list, and `piper-morgan-db`'s volume list unchanged from step A. The drill is done only then.

## Cost and time
A `shared-cpu-1x` Postgres app for one sitting costs cents. Expect the create to take a few minutes; the proofs under ten; cleanup one.

## Not in this half
The schedule decision (daily snapshots are Fly's default; a longer retention or WAL backups via `--enable-backups` is CIO's call under #2157), and master-key custody (#2157's other half).
