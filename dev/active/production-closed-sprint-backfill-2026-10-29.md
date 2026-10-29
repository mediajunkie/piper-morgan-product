# Closed Production issues: Sprint backfill (PPM, 2026-10-29)

**Ask:** xian, in conversation on 10-29: sort the closed Production issues into the sprints they belong (or belonged) to, and set aside any that fall outside the current scheme.

**Population:** 115 closed issues in milestone Production, from xian's list. Before this pass all 115 had no Sprint value. 101 closed before the 10-23 sprint plan existed, and 11 were ever rows in the plan, per its git history (43 versions).

**Applied:** 110, set per item with `gh project item-edit`, which is the safe mutation.
- Read back: 116 of 116 matched (the 110, the 5 set aside, and control #1378 still PUB).
- Sprint options: 60, unchanged.
- **Undo:** clear the Sprint field on the item. Every one was unset before this pass.

The plan's sprints map to the board's options as follows: PUB = PUB - Public Beta, H = PROD-HONESTY, D = PROD-DATA, C = PROD-RECONNECT, V = PROD-CONVO, E = PROD-DESIGN, Doc = PROD-DOCS, Dist = PROD-DIST, Q = Q - Recurring Audits.

| Sprint | n | Issues |
|---|---|---|
| PUB | 6 | 1982, 2005, 2052, 2090, 2198, 2199 |
| H | 37 | 1556, 1565, 1575, 1576, 1577, 1580, 1587, 1941, 1958, 1964, 1985, 1990, 1998, 1999, 2003, 2008, 2020, 2026, 2029, 2031, 2032, 2033, 2044, 2049, 2066, 2068, 2075, 2076, 2079, 2111, 2120, 2137, 2140, 2143, 2152, 2176, 2182 |
| D | 7 | 1533, 1574, 1588, 1601, 2019, 2127, 2131 |
| C | 4 | 1592, 1944, 1966, 2121 |
| V | 24 | 1959, 1971, 1973, 1975, 1976, 1977, 1979, 1986, 1987, 1989, 2004, 2007, 2034, 2035, 2046, 2047, 2050, 2051, 2069, 2073, 2082, 2110, 2113, 2119 |
| E | 20 | 1498, 1607, 1948, 1950, 1960, 1988, 1991, 1992, 2001, 2027, 2028, 2037, 2038, 2039, 2055, 2070, 2088, 2108, 2129, 2156 |
| Doc | 2 | 2122, 2138 |
| Dist | 3 | 830, 831, 832 (closed not planned, superseded by PDR-006) |
| Q | 7 | 1459, 1502, 1582, 1842, 1993, 2000, 2177 |
| T | 0 | none |

**Set aside for discussion (still unset).** These are ops and dev tooling, outside the product sprints. The nearest option is the legacy PROD-INFRA, or none.
- #1647: a pre-commit hook blocks instead of warning (cohort tooling).
- #1662: the upload writability probe printed nothing on boot.
- #2081: Admin Invites page (alpha operations, promise T8).
- #2083: /health ignores the database.
- #2146: Postgres recovery waits on two human presses.

**Judgment calls worth a second look:**
- The integrations-card "Connected / Not configured / All healthy" rows went to H, because #2187, the open sibling, is in H. The Test-toast copy rows (#2037, #2038) went to E.
- The time-statement rows (#1556, #1575 to #1577, #1958, #1999, #2079, #2143) went to H, per round 2's timezone-slice move.
- The inversion-gate tooling (#1971, #1973, #2073) went to V (routing), not PUB. Only #1595's remainder (#2195) is in PUB, on xian's word.
- #1592, the Fly log error from calendar adapters built without user scope, went to C.
- #2127 and #2131 (provider resolution without a user) went to D.
