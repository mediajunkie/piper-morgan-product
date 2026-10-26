# Root README review, 2026-10-26 (Docs, weekly audit #2180)

Scope: `README.md` (repository view) and `docs/README.md` (pipermorgan homepage).

- "NEW:" claims in `README.md`: `grep -n -i "NEW:"` returns 0 lines.
- Internal links: 0 broken of the `.md` links in `README.md` and in `docs/README.md` (python os.path.exists, relative to each file, checked this fire).
- Version: `docs/README.md` line 7 says v0.8.14.0, `pyproject.toml` says 0.8.14.0. Match.
- Both READMEs last changed 3 weeks ago (`git log -1 --format=%cr`), so no unchanged claim is newer than three weeks.
- Not done: external links not fetched, setup steps and code examples not re-run, capabilities list and roadmap section not compared with the shipped feature set, the alpha guides not read for currency. Reported as unverified rather than checked.
