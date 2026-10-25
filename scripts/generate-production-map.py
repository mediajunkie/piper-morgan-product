#!/usr/bin/env python3
"""Generate docs/internal/planning/production-map.html (the living map, round 3).

Usage: python3 scripts/generate-production-map.py [--snapshot PATH] [--previous PATH] [--out PATH]
Inputs: board snapshot TSV, the previous snapshot, the sprint plan doc, promises.yaml.
Nothing on the page is typed by hand except promises.yaml. No network calls.
"""

import argparse
import csv
import glob
import html
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = "docs/internal/planning/production-sprint-proposal-2026-10-23.md"
PROMISES = "docs/internal/product/promises.yaml"
REPO = "https://github.com/mediajunkie/piper-morgan-product/issues/"
ROWS = ["H", "D", "PUB", "C", "V", "E", "T", "Doc", "Dist", "Readiness", "Q"]
PLAN_LETTERS = {"PUB", "H", "D", "C", "V", "E", "T", "Doc", "Dist", "Q"}
READINESS = [2157, 2158, 2159, 2160, 2161, 2162]
EXCLUDED_SPRINTS = {"Fast Follow", "Ongoing", "Dot Releases (Post-MVP)", "Enterprise"}
MOMENTS = [
    ("invited", "invited"),
    ("set-up", "set up"),
    ("first-conversation", "first conversation"),
    ("connect-a-source", "connect a source"),
    ("get-work-done", "ask and get work done"),
    ("something-goes-wrong", "something goes wrong"),
    ("manage-my-data", "manage my data"),
    ("come-back", "come back"),
]
SEAMS = ["resolver", "catalog", "github-identity", "db-durability", "green-ci"]
# Arch, 2026-10-24 19:21: a column is a surface where a different thing serves the step.
# The plugin is a delivery of the MCP endpoint, not a column. chat is out of 1.0 scope (grey).
SURFACES = ["web", "mcp", "chat"]
OUT_OF_SCOPE_SURFACES = {"chat"}
FALLBACK = {
    "PROD-RECONNECT": "C",
    "PROD-DESIGN": "E",
    "PROD-TRUST": "T",
    "PROD-DOCS": "Doc",
    "PROD-DIST": "Dist",
    "PROD-ONBOARD": "Dist",
    "PROD-TECHDEBT": "Q",
    "PROD-INFRA": "Q",
    "PROD-HONESTY": "H",
    "PROD-DATA": "D",
    "PROD-CONVO": "V",
}


def die(msg):
    sys.exit("generate-production-map: ERROR: " + msg)


def need(path, what):
    if not os.path.isfile(path):
        die(f"missing input ({what}): {path}")
    return path


def load_snapshot(path):
    need(path, "snapshot")
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            try:
                n = int(r["issue"])
            except (KeyError, ValueError):
                die(f"bad snapshot row in {path}: {r}")
            r["labels"] = {x for x in (r.get("labels") or "").split(",") if x}
            r["edges"] = {
                int(x) for x in (r.get("blocked_by") or "").split(",") if x.strip().isdigit()
            }
            out[n] = r
    return out


def load_plan(path):
    need(path, "plan doc")
    member, cur = {}, None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^### (\w+):", line)
        if m:
            cur = m.group(1) if m.group(1) in PLAN_LETTERS else None
            continue
        m = re.match(r"^\| #(\d+) \|", line)
        if m and cur:
            member.setdefault(int(m.group(1)), cur)
    return member


def row_of(n, rec, plan):
    """Front-view row for issue n, or None when excluded."""
    if n in READINESS:
        return "Readiness" if rec["milestone"] in ("Production", "MVP") else None
    if rec["milestone"] != "Production" and not (rec["milestone"] == "MVP" and n in plan):
        return None
    sp = rec["sprint"]
    if sp in EXCLUDED_SPRINTS:
        return None
    if n in plan:
        return plan[n]
    if sp.startswith("PUB"):
        return "PUB"
    row = FALLBACK.get(sp.split(" - ")[0].strip())
    if row is None and rec["state"] == "CLOSED":
        return None  # closed and never sprinted: done, not a gap
    return row or "unsprinted"


def classify(snap, plan):
    return {n: r for n, r in ((n, row_of(n, r, plan)) for n, r in snap.items()) if r}


def a(n, snap):
    t = html.escape(snap[n]["title"], quote=True) if n in snap else ""
    return f'<a href="{REPO}{n}" title="{t}">#{n}</a>'


def issue_chip(n, snap):
    r = snap[n]
    if r["state"] != "CLOSED":
        return f'<span class="chip">{a(n, snap)} open</span>'
    if "close:served" in r["labels"]:
        return f'<span class="chip done gn">{a(n, snap)} closed, served</span>'
    if "close:pins-only" in r["labels"]:
        return f'<span class="chip done am">{a(n, snap)} closed, pins only</span>'
    return f'<span class="chip done gy">{a(n, snap)} closed, state unlabelled</span>'


def esc(s):
    return html.escape(str(s))


def pick_snapshots(args):
    snaps = sorted(glob.glob(os.path.join(ROOT, "dev/snapshots/project-board-*.tsv")))
    cur = args.snapshot or (snaps[-1] if snaps else None)
    if not cur:
        die("no dev/snapshots/project-board-*.tsv found")
    prev = args.previous
    if not prev:
        older = [s for s in snaps if os.path.abspath(s) < os.path.abspath(cur)]
        prev = older[-1] if older else None
    return cur, prev


def since_last(cur, prev, plan, rows_c, rows_p):
    if not prev:
        return ["<p>No previous snapshot found; nothing to compare.</p>"], "no previous snapshot"
    pc = {n: r for n, r in prev.items()}
    added = sorted(set(rows_c) - set(rows_p))
    removed = sorted(set(rows_p) - set(rows_c))
    common = sorted(set(rows_c) & set(rows_p))
    moved = [
        n for n in common if rows_c[n] != rows_p[n] or cur[n]["milestone"] != pc[n]["milestone"]
    ]
    closed = [n for n in common if cur[n]["state"] == "CLOSED" and pc[n]["state"] != "CLOSED"]
    key = lambda l: l.split(":")[0] in ("promise", "journey", "seam") and ":" in l
    lab = []
    for n in sorted(set(cur) & set(pc)):
        for l in sorted(cur[n]["labels"] - pc[n]["labels"]):
            if key(l):
                lab.append(f"{a(n, cur)} +{esc(l)}")
        for l in sorted(pc[n]["labels"] - cur[n]["labels"]):
            if key(l):
                lab.append(f"{a(n, cur)} -{esc(l)}")
    ec = {(b, k) for n, r in cur.items() for b in [n] for k in r["edges"]}
    ep = {(b, k) for n, r in pc.items() for b in [n] for k in r["edges"]}
    eadd, erem = sorted(ec - ep), sorted(ep - ec)
    fmt = lambda ns: " ".join(a(n, cur if n in cur else pc) for n in ns) or "none"
    pair = lambda es: ", ".join(f"#{b} &rarr; #{k}" for b, k in es) or "none"
    mv = ", ".join(f"{a(n, cur)} {rows_p[n]}&rarr;{rows_c[n]}" for n in moved[:40]) or "none"
    if len(moved) > 40:
        mv += f" ... (+{len(moved) - 40} more)"
    L = [
        f"<p>Compared with {esc(os.path.basename(prev_path[0]))}. Membership for both uses the plan doc's "
        "table (limit: the plan is today's, so older sprint moves are invisible); issues absent from the plan "
        "use each snapshot's own Sprint value.</p>",
        "<ul>",
        f"<li>Added to scope ({len(added)}): {fmt(added[:60])}{' ...' if len(added) > 60 else ''}</li>",
        f"<li>Removed from scope ({len(removed)}): {fmt(removed[:60])}{' ...' if len(removed) > 60 else ''}</li>",
        f"<li>Moved row or milestone ({len(moved)}): {mv}</li>",
        f"<li>Closed ({len(closed)}): {fmt(closed[:60])}{' ...' if len(closed) > 60 else ''}</li>",
        f"<li>Labels added/removed (promise/journey/seam): {'; '.join(lab) or 'none'}</li>",
        f"<li>Edges added: {pair(eadd)}. Edges removed: {pair(erem)}.</li></ul>",
    ]
    summ = (
        f"vs {os.path.basename(prev_path[0])}: +{len(added)} added, -{len(removed)} removed, "
        f"{len(moved)} moved, {len(closed)} closed, {len(lab)} label changes, "
        f"+{len(eadd)}/-{len(erem)} edges"
    )
    return L, summ


prev_path = [None]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot")
    ap.add_argument("--previous")
    ap.add_argument("--out")
    args = ap.parse_args()
    cpath, ppath = pick_snapshots(args)
    prev_path[0] = ppath
    out = args.out or os.path.join(ROOT, "docs/internal/planning/production-map.html")
    cur = load_snapshot(cpath)
    prev = load_snapshot(ppath) if ppath else None
    plan = load_plan(os.path.join(ROOT, PLAN))
    ppath_y = need(os.path.join(ROOT, PROMISES), "promises.yaml")
    raw = open(ppath_y, encoding="utf-8").read()
    draft = bool(re.search(r"DRAFT v\d", raw)) and "NOT RATIFIED" in raw
    pdata = yaml.safe_load(raw)
    promises = [(grp, p) for grp in ("essence", "terms", "readiness") for p in pdata.get(grp, [])]

    rc = classify(cur, plan)
    rp = classify(prev, plan) if prev else {}
    date = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(cpath))
    date = date.group(1) if date else "unknown"
    state = lambda n: cur[n]["state"]
    is_open = lambda n: state(n) != "CLOSED"

    # promise labels
    by_label = {}
    for n, r in cur.items():
        for l in r["labels"]:
            by_label.setdefault(l, []).append(n)
    pstat = []
    for grp, p in promises:
        iss = sorted(by_label.get("promise:" + p["id"], []))
        gbt = "gate-by-test" in (p.get("note") or "") or p["id"].startswith("E7")
        if not iss:
            cls = "grey" if gbt else "red"
        elif any(is_open(n) for n in iss):
            cls = "red"
        else:
            cls = "green" if all("close:served" in cur[n]["labels"] for n in iss) else "amber"
        pstat.append((grp, p, iss, cls, gbt and not iss))
    g1 = [x for x in pstat if str(x[1]["gate"]) == "1.0"]
    n_ok = sum(1 for x in g1 if x[2] and x[3] in ("green", "amber"))
    n_served = sum(1 for x in g1 if x[2] and x[3] == "green")
    q_open = sum(1 for n, r in rc.items() if r == "Q" and is_open(n))

    P = []
    w = P.append
    w(f"<h1>Production map</h1><p>Snapshot {esc(date)}. Generated; do not edit.</p>")
    w(
        f'<div class="head"><div class="big">{n_ok} of {len(g1)} 1.0 promises have a closed issue, {n_served} of them served</div>'
        f"<div>Health lane (Q): {q_open} open &middot; main CI: see scripts/main-ci-status.sh</div></div>"
    )
    if draft:
        w('<p class="amber">promises.yaml is DRAFT v0, unratified: wording may change.</p>')

    sl, summ = (
        since_last(cur, prev, plan, rc, rp)
        if prev
        else (["<p>No previous snapshot found.</p>"], "no previous snapshot")
    )
    w("<h2>Since last</h2>" + "".join(sl))

    # front view
    w(
        "<h2>Front view</h2><p>Rows in closing order. Red = backward edge (blocked by an issue in a later row) or unsprinted. "
        "Readiness lists #2157 to #2162 (the plan doc files them under D; shown once, here).</p>"
    )
    order = {r: i for i, r in enumerate(ROWS)}
    back = []
    w('<div class="scroll"><table><tr><th>Row</th><th>Open</th><th>Closed</th><th>Issues</th></tr>')
    for r in ROWS + ["unsprinted"]:
        ns = sorted(n for n, x in rc.items() if x == r)
        if r == "unsprinted" and not ns:
            continue
        o = sum(1 for n in ns if is_open(n))
        cells = []
        for n in ns:
            bad = [
                b
                for b in sorted(cur[n]["edges"])
                if rc.get(b) in order and r in order and order[rc[b]] > order[r]
            ]
            if bad and is_open(n):
                back.extend((n, b) for b in bad)
                cells.append(
                    f'<span class="red">{a(n, cur)} blocked by {", ".join("#%d" % b for b in bad)} (later row)</span>'
                )
            else:
                cells.append(f'<span class="{"" if is_open(n) else "done"}">{a(n, cur)}</span>')
        cls = "red" if r == "unsprinted" else ""
        w(
            f'<tr class="{cls}"><td>{esc(r)}</td><td>{o}</td><td>{len(ns) - o}</td><td class="iss">{" ".join(cells) or "-"}</td></tr>'
        )
    w("</table></div>")
    w(
        "<p>Struck-through numbers are closed. D is one row (the isolation slice is not separable yet).</p>"
    )

    # promise view
    w(
        "<h2>Promise view</h2><p>Labels (<code>promise:&lt;id&gt;</code>) are not applied yet, so nearly every promise is red. "
        "That is correct today.</p>"
    )
    w(
        '<div class="scroll"><table><tr><th>Promise</th><th>Wording</th><th>Gate</th><th>Issues</th></tr>'
    )
    for grp, p, iss, cls, gbt in pstat:
        txt = (
            "gate-by-test"
            if gbt
            else (" ".join(issue_chip(n, cur) for n in iss) or "no labelled issue")
        )
        w(
            f'<tr class="{cls}"><td>{esc(p["id"])}</td><td>{esc(p["wording"])}</td><td>{esc(p["gate"])}</td><td>{txt}</td></tr>'
        )
    w("</table></div>")

    # readiness
    w(
        "<h2>Readiness view</h2><p>#2157 to #2161 are Terms-backed (gate public beta). #2162 is staging, non-gating.</p>"
    )
    w("<table><tr><th>Issue</th><th>Gate</th><th>State</th></tr>")
    for n in READINESS:
        g = "non-gating" if n == 2162 else "public beta"
        if n in cur:
            w(
                f'<tr class="{"red" if is_open(n) else "green"}"><td>{a(n, cur)} {esc(cur[n]["title"][:70])}</td><td>{g}</td><td>{state(n)}</td></tr>'
            )
        else:
            w(f'<tr class="red"><td>#{n}</td><td>{g}</td><td>not in snapshot</td></tr>')
    w("</table>")

    # dependency
    w("<h2>Dependency view</h2>")
    w("<table><tr><th>Seam</th><th>Issues</th></tr>")
    for s in sorted(set(SEAMS) | {l[5:] for l in by_label if l.startswith("seam:")}):
        iss = sorted(by_label.get("seam:" + s, []))
        if iss:
            w(f'<tr><td>{esc(s)}</td><td>{" ".join(a(n, cur) for n in iss)}</td></tr>')
        else:
            w(f'<tr class="red"><td>{esc(s)}</td><td>empty seam</td></tr>')
    w("</table>")
    edges = sorted((n, b) for n in rc for b in cur[n]["edges"] if b in rc)
    if edges:
        w("<p>Edges among Production issues (blocked &rarr; blocker):</p><ul>")
        for n, b in edges:
            bk = order.get(rc[b], 0) > order.get(rc[n], 0)
            w(
                f'<li class="{"red" if bk else ""}">{a(n, cur)} &rarr; {a(b, cur)}{" (backward)" if bk else ""}</li>'
            )
        w("</ul>")
    else:
        w("<p>No blocked-by edges among Production issues yet.</p>")

    # journey grid
    w(
        "<h2>Journey grid</h2><p>Moment list: CXO draft, unratified. Surface columns (Arch, 10-24): web "
        "(Piper's own web app), mcp (the hosted MCP endpoint, including the Claude plugin, which delivers it), "
        "chat (Slack and similar platforms, not in 1.0, so grey, never red). Labels: surface:web, surface:mcp, "
        "surface:chat. Without a surface label an issue sits under &quot;unassigned surface&quot;.</p>"
    )
    w(
        '<div class="scroll"><table><tr><th>Moment</th>'
        + "".join(f"<th>{s}</th>" for s in SURFACES)
        + "<th>unassigned surface</th></tr>"
    )
    known = {m for m, _ in MOMENTS}
    extra = sorted({l[8:] for l in by_label if l.startswith("journey:")} - known)
    for slug, name in MOMENTS + [(e, e) for e in extra]:
        iss = sorted(by_label.get("journey:" + slug, []))
        if not iss:
            w(
                f"<tr><td>{esc(name)}</td>"
                + "".join(
                    '<td class="gy">not in 1.0</td>'
                    if s in OUT_OF_SCOPE_SURFACES
                    else '<td class="red">no issue</td>'
                    for s in SURFACES
                )
                + '<td class="red">no issue</td></tr>'
            )
            continue
        cols = {s: [] for s in SURFACES + ["u"]}
        for n in iss:
            hit = [
                s
                for s in SURFACES
                if "surface:" + s.lower() in {x.lower() for x in cur[n]["labels"]}
            ]
            for s in hit or ["u"]:
                cols[s].append(issue_chip(n, cur))
        w(
            f"<tr><td>{esc(name)}</td>"
            + "".join(
                f'<td class="gy">{" ".join(cols[s]) or "not in 1.0"}</td>'
                if s in OUT_OF_SCOPE_SURFACES
                else (
                    f"<td>{' '.join(cols[s])}</td>"
                    if cols[s] or s == "u"
                    else '<td class="red">no issue</td>'
                )
                for s in SURFACES + ["u"]
            )
            + "</tr>"
        )
    w("</table></div>")

    cmd = "python3 scripts/generate-production-map.py" + (
        f" --snapshot {os.path.relpath(cpath, ROOT)}" if args.snapshot else ""
    )
    w(
        f"<h2>Footer</h2><p>Generated by <code>{esc(cmd)}</code>.<br>Inputs: {esc(os.path.relpath(cpath, ROOT))}; "
        f"{esc(os.path.relpath(ppath, ROOT)) if ppath else 'no previous snapshot'}; {PLAN}; {PROMISES}.<br>"
        "Nothing on this page is typed by hand except promises.yaml.<br>"
        "Edge rule (Arch, 2026-10-24): an edge means \"must close before\", nothing weaker; whoever adds one "
        "says why in a comment on the blocked issue; a backward edge is drawn red, never hidden; Arch reviews "
        "the edges each Friday. Close states: <code>close:served</code> (a quoted served row on the close) or "
        "<code>close:pins-only</code> (failure branches pinned, not servable); unlabelled closes show grey.</p>"
    )

    css = (
        "body{font:15px/1.45 system-ui,sans-serif;margin:0 auto;max-width:1000px;padding:0 16px 40px;background:#fff;color:#1a1a1a}"
        "a{color:#0a58ca}table{border-collapse:collapse;width:100%;margin:8px 0}th,td{border:1px solid #bbb;padding:4px 6px;text-align:left;vertical-align:top}"
        ".scroll{overflow-x:auto}.big{font-size:1.4em;font-weight:700}.head{padding:8px 0}"
        ".red,tr.red td{background:#fbd5d5;color:#5a0000}.red a{color:#7a0000}tr.green td{background:#d4edda;color:#0b3d17}tr.grey td{background:#e4e4e4}tr.amber td,.am{background:#ffe9a8;color:#4a3800}.gn{background:#d4edda;color:#0b3d17}.gy{background:#e4e4e4;color:#333}.chip{margin-right:6px;white-space:nowrap}"
        ".done a{text-decoration:line-through;color:#777}.amber{background:#fff0c2;color:#4a3800;padding:6px}.iss{line-height:1.8}.iss span{margin-right:6px;white-space:nowrap}"
        "@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}a{color:#7db3ff}th,td{border-color:#444}"
        ".red,tr.red td{background:#5a1c1c;color:#ffd6d6}.red a{color:#ffb0b0}tr.green td{background:#1d4a2a;color:#d6f5de}tr.grey td,.gy{background:#333;color:#ddd}tr.amber td,.am{background:#5a4a10;color:#ffeab0}.gn{background:#1d4a2a;color:#d6f5de}"
        ".done a{color:#888}.amber{background:#4a3d12;color:#ffeab0}}"
    )
    doc = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Production map {esc(date)}</title><style>{css}</style></head><body>\n"
        + "\n".join(P)
        + "\n</body></html>\n"
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)

    # stdout summary
    print(f"wrote {out}")
    print("rows:", {r: sum(1 for x in rc.values() if x == r) for r in ROWS + ["unsprinted"]})
    print(
        f"promises: {len(pstat)} total, {sum(1 for x in pstat if x[3] == 'red')} red, {sum(1 for x in pstat if x[3] == 'grey')} grey; headline {n_ok} of {len(g1)}"
    )
    print(f"backward edges: {len(back)}")
    print("unsprinted:", sorted(n for n, x in rc.items() if x == "unsprinted"))
    print("since last:", summ)
    miss = sorted(n for n in plan if n not in cur)
    print("plan rows not in snapshot:", miss)
    print(
        "plan rows excluded by milestone:",
        sorted((n, cur[n]["milestone"]) for n in plan if n in cur and n not in rc),
    )
    print(
        "open Production issues not in plan or unsprinted fallback:",
        sum(
            1
            for n, r in cur.items()
            if r["milestone"] == "Production" and is_open(n) and n not in plan
        ),
    )


if __name__ == "__main__":
    main()
