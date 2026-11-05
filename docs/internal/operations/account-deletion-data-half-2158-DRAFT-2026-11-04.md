# Account deletion (#2158), the data half — DRAFT 2026-11-04 (Lead; Arch reviews)

**Status:** draft, prep only (Exec 16:34). HOST's request-handling half: `account-deletion-request-handling-2158-host-half-DRAFT-2026-11-04.md`. xian's 10-13 ruling stands: deletion by email within 14 days. Nothing runs against alpha before xian's yes and a real request.

## What a deleted account is, store by store

`scripts/erase_user.py` (#2064, Arch's shape 2026-10-16) is the one payload, and it is read-only by default. Its erase, in order, each outside store before the rows that point at it, idempotent, pre-flighted in a rolled-back transaction first:

1. **Provider grants:** every connector the account has a credential for goes through the app's own `disconnect_connector`, which revokes on the provider's side where the provider supports it and clears the local credential. **GitHub does not revoke at GitHub (#2178, open):** the person's grant stays valid in their GitHub account until they revoke it under Settings → Applications → Authorized OAuth Apps. The reply to the person says so until #2178 lands.
2. **Uploaded files:** every DB-known `uploaded_files.storage_path` through the storage seam, then anything left under `<UPLOAD_DIR>/<user-id>/`.
3. **ChromaDB chunks** of the account's documents (the in-app store, where present).
4. **Postgres**, one transaction in dependency order: conversations and everything hanging off them (`conversation_turns`, memory rows, `session_activity`), `conversations`, `standup_conversations`, `insights`, `ethics_audit_log`, `feedback`, todo items, lists, projects, repositories, knowledge nodes and edges, Slack identities, documents, `secure_credentials`, `user_api_keys`, `audit_logs`, then `users`. Any error rolls the whole transaction back.
5. **Redis** cache keys naming the account or its conversations (TTL caches, best effort).

Never printed: the email or username (sha256 fingerprints only), any row content.

## The soft-delete tables, and whether the script covers them

Two tables carry a soft-delete flag: `conversations` (`archived_at`, `deleted_at`) and `insights` (`is_deleted`; the insights removal soft-deletes, Lead 10-24). **Both are hard-deleted by the erase plan, by owner, whatever the flag says** (`erase_user.py` steps for `conversations` and `insights` select on `user_id`/`owner_id` only). So an emailed deletion handled through the script leaves no soft-deleted rows behind. No other table soft-deletes (grep of `services/database/models.py` for `deleted_at`, `is_deleted`, `archived_at`, `removed_at`: those two tables only).

## What the script does not reach, and what to say about each

- **Fly volume snapshots of `piper-morgan-db`:** daily, **5-day retention** (Fly's default; `alpha-fly-cutover-runbook-2026-09-22.md` records it on this volume; configurable 1 to 60 days, a change applying to new snapshots only). A deleted account survives in snapshots taken before the erase for up to 5 days after it. **N = 5** for HOST's reply ("Backups can hold a copy for up to 5 days, after which it is gone"). A manual snapshot taken for a drill or a cutover keeps for its own retention, so the operator checks `fly volumes snapshots list <vol_id> -a piper-morgan-db` for any snapshot older than the default window before promising the date.
- **GitHub itself:** issues, comments and the OAuth grant Piper made as the person live in GitHub, not in Piper; not ours to delete, said to the person.
- **Email with the person** (the request thread) and **HOST's private roster**: HOST's half.
- **Application logs:** structured logs carry account ids and fingerprints, never emails or content; Fly's log retention is short and not something this seat has measured (unverified).
- **The MCP app's own state:** the MCP app reads the same database through its own process; whether it holds any per-account rows of its own is **unverified** from this seat and is a question for Arch's review.
- **This repository:** rule 8 keeps names out of logs and mail; nothing to purge here by design, and a slip is Exec's to handle, not a deletion step.

## The procedure, data half (xian's hand, the prod-exec shape; HOST hands over the account id only)

1. **Count:** `fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <account-id>"`. Read the verdict line: "would erase cleanly" proceeds; "would refuse at <table>" stops, and the table named is a unit for Lead before anything is erased.
2. **Erase:** `fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <account-id> --erase --confirm <account-id>"`. The same counts print after; every store reads zero.
3. **Re-count by id:** step 1 again; zeros everywhere, or the leftover is named and a rerun finishes it (the script is idempotent).
4. **Record** (HOST's log, counts only): the date of the erase, the stores' before-and-after counts, and **the snapshot horizon = erase date + 5 days** (or the oldest manual snapshot's retention end, if later).
5. **GitHub grant:** until #2178 lands, the reply tells the person to revoke Piper under their GitHub settings.
6. **After the horizon,** optionally: `fly volumes snapshots list <vol_id> -a piper-morgan-db` shows no snapshot older than the horizon; HOST may then tell the person the copy is gone.

## For Arch's review
Whether the MCP app holds per-account rows outside this plan; whether `audit_logs` rows should be kept in anonymised form for the security record rather than deleted (today the plan deletes them by `user_id`); and whether N should name 5 days or "about a week" to the person.
