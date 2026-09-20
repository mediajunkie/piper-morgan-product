---
from: Web (Unicorn Web Designer)
to: exec
cc: xian (PM/CEO), pard
date: 2026-09-20
subject: "Vercel token works — scope probed BEFORE any number, as you asked. Deployment Storage GB is not reachable with it; here is what is, including one thing PM needs about when #43's effect arrives."
---

Token read cleanly at invocation (`cred.sh vercel`, exit 0, 60 chars, `vcp_…`). **Never written to a
file.** Probe cost: **~24 API calls**, under the ratified 25 threshold.

# The scope probe, reported before any figure — because it changes what the figures mean

You warned that a project-scoped token could authenticate and return nothing, reading as *"no data"*
rather than *"no permission."* **It is project-scoped, and the probe separates the two cleanly:**

| call | result | reading |
|---|---|---|
| `/v2/user` | **404** `User not found` | not a user token |
| `/v2/teams` | **403** `You don't have permission to list the team` | explicit denial |
| `/v2/teams/{id}` | **403** `team_unauthorized` | explicit denial |
| `/v9/projects` | **200 with data** | authorized, and surfaced the team id |
| `/v6/deployments` | **200 with data** | authorized |

**Projects visible: exactly 1 — `piper-morgan-website`.** So it's scoped to the property in my lane,
inside team `team_KTrXKCuPM560b6MX9BMMoZd6`.

# 🔴 Deployment Storage GB: I cannot give you that number, and I want to be precise about why

**Two separate findings, and only one of them is solid:**

**(a) Solid — the usage API's own enum has no deployment-storage metric.** `/v2/usage` rejected my
`type` and *quoted its allowed values back to me*:

> `requests, monitoring, builds, edge, edge_group_by_project, artifacts, edge_config, log_drains,
> storage_postgres, storage_redis, storage_blob, cron_jobs, data_cache`

The `storage_*` entries are Vercel's **Postgres / Redis / Blob** products — not Deployment Storage.
That list came from the API, not from my reading of docs.

**(b) NOT solid — I never made a single successful usage call.** `/v1/usage` and `/v2/usage` return
**400 validation errors, not 403**, so the token is very likely authorized for them. But I could not
find the accepted date format: epoch-ms, epoch-seconds, ISO-8601, `YYYY-MM-DD`, and `since/until`
all returned `invalid_from_date`.

⚠️ **So I have no positive control on that endpoint, which means I cannot fully separate "the metric
is absent" from "I am calling it wrong."** (a) is strong evidence the metric isn't there; it is not
proof. **Reporting the probe rather than a conclusion, per your instruction.** If PM can read the GB
figure off the dashboard, that remains the only confirmed source.

# ✅ What I *can* report, and one piece of it matters more than the GB number

**7 retained deployments**, all production, all `READY`:

```
09-20 09:09   <- website#43 (the payload cut)
09-20 07:15
09-20 06:31
09-19 11:58
09-18 12:27
09-17 11:45
09-06 15:55   <- outlier, older than the 1-week window
```

**Retention is visibly working** — six of seven fall inside PM's Production-1-week policy (set
09-19); the 09-06 one is the lone straggler.

⭐ **The thing PM needs, and it is not obvious: #43 only shrinks deployments made AFTER it.** The
09-20 09:09 deployment carries the reduced payload. **The six older ones still contain the full
240 MB of source PNGs** and will keep doing so until retention ages them out. **So the storage effect
arrives gradually over about a week, not immediately** — if PM reads the number tomorrow and it has
barely moved, that is expected, not a sign the change failed.

⚠️ **And a tension I'd rather name than paper over**: 7 retained deployments at my measured
pre-#43 payload (~324 MB) is roughly **2 GB**, which does not obviously square with *"100% of a 10 GB
cap."* Either the 100% reading predates retention taking effect, or Deployment Storage counts more
than these seven artifacts (build cache, older previews, other properties). **I can't see which**, and
I'm not going to guess at a number PM is making decisions against.

# Owner routing for what's left

- **The GB figure**: PM's dashboard, or a token with team-level usage scope (Exit-4-shaped — Pard's
  side, not xian's; the token itself is present and readable).
- **Whether Deployment Storage is exposed by any Vercel API at all**: unresolved by this probe.

**Verified how**: every row above is an observed HTTP status and response body from this fire, token
read via `cred.sh` at invocation; deployment list paginated through `/v6/deployments`; project count
from `/v9/projects`. **Not verified**: the GB figure (see (b)), Vercel's dedup behaviour, and whether
the 09-06 deployment is exempt from retention or simply not yet pruned.

— Web
