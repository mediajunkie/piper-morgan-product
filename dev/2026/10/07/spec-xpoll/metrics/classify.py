#!/usr/bin/env python3
"""Cross-pollination insight classifier (stdlib only). See classifier_prompt.md."""
import argparse, collections, json, os, random, re, ssl, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
INSIGHTS = os.path.join(HERE, "insights.jsonl")
BRIEFS = "/home/user/designinproduct/src/internal/briefs/"
PROMPT_MD = os.path.join(HERE, "classifier_prompt.md")
DRYRUN = os.path.join(HERE, "classify_dryrun.jsonl")
FULLRUN = os.path.join(HERE, "classify_full.jsonl")
CA = "/root/.ccr/ca-bundle.crt"
MODEL = "claude-sonnet-5-5"
# $/MTok for claude-sonnet-5-5 (claude-api skill, Current Models table; cache read $0.20; cache write = 1.25x input)
P_IN, P_OUT, P_CREAD, P_CWRITE = 2.00, 10.00, 0.20, 2.50
FRAMING = {
    "A": "Framing: classify by the insight's central SUBJECT MATTER - what it is mainly about.",
    "B": "Framing: classify by where a practitioner would most naturally FILE or LOOK UP this insight - what area of work it would change.",
}


def system_prompt():
    t = open(PROMPT_MD).read()
    return t.split("<!-- BEGIN SYSTEM -->\n")[1].split("<!-- END SYSTEM -->")[0]


def load_rows():
    return [json.loads(l) for l in open(INSIGHTS)]


def eligible(rows):
    return [r for r in rows if r["confidentiality"] == "clear" and r["era"] != "draft"]


def get_body(r):
    """Return body block text for the row, or None if it cannot be located."""
    p = BRIEFS + r["brief_file"]
    if not os.path.exists(p):
        return None
    lines = open(p).read().split("\n")
    n = int(r["id"].split("#")[1])
    start = None
    for i, l in enumerate(lines):  # 1) numbered heading
        if re.match(r"### %d\. " % n, l):
            start = i; break
    if start is None:  # 2) exact heading text
        for i, l in enumerate(lines):
            if l.startswith("### ") and l[4:].strip() == r["heading"].strip():
                start = i; break
    if start is None:  # 3) n-th ### heading
        hs = [i for i, l in enumerate(lines) if l.startswith("### ")]
        if len(hs) >= n and len(hs) == r.get("n_in_brief", len(hs)):
            start = hs[n - 1]
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("### ") or lines[j].startswith("## "):
            end = j; break
    body = "\n".join(lines[start + 1:end]).strip()
    body = re.sub(r"\n---\s*$", "", body).strip()
    return body or None


def user_msg(r, body, which):
    return (f"{FRAMING[which]}\n\nHeading: {r['heading']}\nFrom: {r.get('from')}\n"
            f"Relevant to: {r.get('relevant_to')}\n\nBody:\n{body}")


def call_api(system, user):
    key = os.environ["PIPER_TEST_ANTHROPIC_API_KEY"]
    body = {
        "model": MODEL, "max_tokens": 400,
        "thinking": {"type": "between_tools"},
        "output_config": {"effort": "low"},
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    ctx = ssl.create_default_context(cafile=CA)
    with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
        return json.loads(resp.read())


def parse_out(resp):
    txt = "".join(b.get("text", "") for b in resp["content"] if b["type"] == "text")
    m = re.search(r"\{.*\}", txt, re.S)
    o = json.loads(m.group(0))
    assert int(o["topic"]) in range(1, 7)
    return {"topic": int(o["topic"]), "tag": str(o.get("tag", "")), "confidence": float(o.get("confidence", 0)),
            "rationale": str(o.get("rationale", ""))}


def cost(u):
    return (u.get("input_tokens", 0) * P_IN + u.get("output_tokens", 0) * P_OUT
            + u.get("cache_read_input_tokens", 0) * P_CREAD
            + u.get("cache_creation_input_tokens", 0) * P_CWRITE) / 1e6


def classify_one(system, r, body, which):
    """One call, one retry; a second failure aborts the whole run."""
    for attempt in (1, 2):
        try:
            resp = call_api(system, user_msg(r, body, which))
            out = parse_out(resp)
            u = resp["usage"]
            return {**out, "usage": {k: u.get(k, 0) or 0 for k in
                    ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")}}
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
        print(f"  call error ({r['id']} pass {which}, attempt {attempt}): {err}", file=sys.stderr)
        time.sleep(2)
    sys.exit(f"STOP: {r['id']} pass {which} failed twice")


def done_ids(path):
    if not os.path.exists(path):
        return set()
    return {json.loads(l)["id"] for l in open(path) if l.strip()}


def process(rows, path):
    system = system_prompt()
    done = done_ids(path)
    with open(path, "a") as f:
        for r in rows:
            if r["id"] in done:
                continue
            body = get_body(r)
            if body is None:
                print(f"  SKIP (body not located): {r['id']}", file=sys.stderr); continue
            a = classify_one(system, r, body, "A")
            b = classify_one(system, r, body, "B")
            rec = {"id": r["id"], "A": a, "B": b, "agree": a["topic"] == b["topic"]}
            f.write(json.dumps(rec) + "\n"); f.flush()


def totals(path):
    recs = [json.loads(l) for l in open(path) if l.strip()]
    ps = [p for r in recs for p in (r["A"], r["B"])]
    s = lambda k: sum(p["usage"][k] for p in ps)
    return recs, s("input_tokens"), s("output_tokens"), s("cache_read_input_tokens"), s("cache_creation_input_tokens"), sum(cost(p["usage"]) for p in ps)


def cmd_dry(a):
    rows = sorted(eligible(load_rows()), key=lambda r: r["id"])
    pick = random.Random(a.seed).sample(rows, a.n)
    process(pick, DRYRUN)
    recs, tin, tout, cr, cw, c = totals(DRYRUN)
    print(f"DRY-RUN COST: ${c:.4f} for {len(recs)} items x 2 passes ({MODEL}); "
          f"tokens in={tin} out={tout} cache_read={cr} cache_write={cw}")


def cmd_run(a):
    el = sorted(eligible(load_rows()), key=lambda r: r["id"])
    if not os.path.exists(DRYRUN):
        sys.exit("need a dry run first to estimate cost")
    recs = totals(DRYRUN)[0]
    per_item = sum(cost(p["usage"]) for r in recs for p in (r["A"], r["B"])) / len(recs)
    remaining = [r for r in el if r["id"] not in done_ids(FULLRUN)]
    print(f"ESTIMATED COST: ${per_item * len(remaining):.2f} = ${per_item:.4f}/item (dry-run avg) x {len(remaining)} remaining of {len(el)} eligible")
    if not a.confirm_spend:
        sys.exit("refusing to run: pass --confirm-spend to proceed")
    process(el, FULLRUN)
    print("done ->", FULLRUN)


def cmd_agree(a):
    path = a.file or (FULLRUN if os.path.exists(FULLRUN) else DRYRUN)
    recs = [json.loads(l) for l in open(path) if l.strip()]
    n = len(recs); ag = sum(r["agree"] for r in recs)
    print(f"file: {path}\noverall agreement: {ag}/{n} = {ag / n:.1%}")
    print("\nper topic (by pass A label): agree/total")
    for t in range(1, 7):
        s = [r for r in recs if r["A"]["topic"] == t]
        if s: print(f"  topic {t}: {sum(r['agree'] for r in s)}/{len(s)}")
    m = collections.Counter((r["A"]["topic"], r["B"]["topic"]) for r in recs)
    print("\nconfusion (rows = pass A, cols = pass B)\n      " + " ".join(f"B{j}" for j in range(1, 7)))
    for i in range(1, 7):
        print(f"  A{i}  " + " ".join(f"{m[(i, j)]:2d}" for j in range(1, 7)))


def main():
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest="cmd", required=True)
    d = sp.add_parser("dry-run"); d.add_argument("--n", type=int, default=10); d.add_argument("--seed", type=int, default=20261008); d.set_defaults(f=cmd_dry)
    r = sp.add_parser("run"); r.add_argument("--all", action="store_true", required=True); r.add_argument("--confirm-spend", action="store_true"); r.set_defaults(f=cmd_run)
    g = sp.add_parser("agreement"); g.add_argument("--file"); g.set_defaults(f=cmd_agree)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
