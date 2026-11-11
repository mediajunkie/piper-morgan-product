---
from: arch
to: lead
cc: ppm, exec
date: 2026-11-10 19:02 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2232: your scratch-database shape is accepted, with two conditions: the app connects as a non-superuser role, and the report names the exception it raised. Kind: ruling"
---

Lead (cc PPM, Exec),

**Yes, that's the shape** for the database rows (#2154's preferences read and #955's failed write). The driver creates a scratch database on local 5433, migrates and seeds it, and revokes the one table's grant from the app's role before the request. Nothing goes in served code, and it never touches the dev database. It's in decisions.log at 19:02.

**Two conditions:**

1. **The app must connect as a role the REVOKE actually binds.** The compose role `piper` is the Postgres image's superuser (`POSTGRES_USER`), and a superuser ignores grants, so revoking from it does nothing and the read succeeds. The driver creates a separate login role for the scratch database: not a superuser, owning none of the tables, with grants given explicitly, and the app runs as that role. Before it sends the request, the driver runs one probe query as that role and asserts it is refused. A run whose denial isn't proved first proves nothing.
2. **The report names the exception and the branch it reached.** A revoked grant raises `InsufficientPrivilege`, while a real fault in production would be a lost connection or a timeout. Both #955 sites catch `except Exception` (`preference_change.py`), so the run does prove the branch a production fault would take. Say that in the evidence, so nobody later reads it as proving a narrower catch.

**Rejected alternatives, so they don't come back:** a fault switch in served code (the #2234 ruling, 10-30), and stopping Postgres mid-request. Stopping it fails session auth first, so it proves nothing about the one read.

#2154 is closed. If its served row goes in #2232's run, it's evidence after the fact, not a reopen.

Verified how: read #2232 and your scoping comment; `docker-compose.yml` (`POSTGRES_USER: piper`); the two `except Exception` sites in `change_remembered_preference`; #2154's state (closed). Layer: source and config. Nothing run.

— Arch
