"""A-secretscan: focused regex secret scan. Masks values (first4...last4). Never prints full secrets.
Usage: python A-secretscan.py tree <dir>        # working tree
       python A-secretscan.py history <repo> <rev>  # all blobs reachable in history (git log -p added lines)"""
import re, sys, os, subprocess, collections
PATS = {
 "anthropic_key": r"sk-ant-(?:api|admin)\d{2}-[A-Za-z0-9_\-]{80,}",
 "openai_key": r"sk-(?:proj-)?[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}|sk-proj-[A-Za-z0-9_\-]{40,}",
 "github_pat": r"gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,}",
 "slack_token": r"xox[baprs]-[0-9]{6,}-[0-9A-Za-z\-]{10,}",
 "slack_webhook": r"hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]{20,}",
 "aws_akid": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
 "google_api_key": r"\bAIza[0-9A-Za-z_\-]{35}\b",
 "google_oauth_secret": r"GOCSPX-[A-Za-z0-9_\-]{20,}",
 "notion_token": r"\b(?:secret_[A-Za-z0-9]{43}|ntn_[A-Za-z0-9]{40,})\b",
 "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----",
 "jwt": r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}",
 "pg_url_with_pw": r"postgres(?:ql)?(?:\+\w+)?://[^:\s/'\"]+:[^@\s'\"$\{]{4,}@",
 "stripe": r"\b[sr]k_live_[A-Za-z0-9]{20,}",
 "generic_assign": r"(?i)\b(?:api[_-]?key|secret[_-]?key|client[_-]?secret|password|passwd|auth[_-]?token|jwt[_-]?secret)\b\s*[:=]\s*[\"']([A-Za-z0-9_\-+/=!@#%^&*.]{12,})[\"']",
}
CRE = {k: re.compile(v) for k, v in PATS.items()}
PLACEHOLDER = re.compile(r"(?i)(x{4,}|your[_-]|example|placeholder|changeme|dummy|fake|test|sample|<|\.\.\.|redacted|\*\*\*|1234|abcd|secret_here|replace)")
def mask(s): s = s.strip(); return s[:4] + "…" + s[-4:] if len(s) > 10 else "****"
def scan_line(line):
    out = []
    for k, r in CRE.items():
        for m in r.finditer(line):
            val = m.group(1) if (k == "generic_assign" and m.groups()) else m.group(0)
            ph = bool(PLACEHOLDER.search(val)) or (k == "pg_url_with_pw" and re.search(r"(?i)piper|postgres:postgres|password|user:pass", val))
            out.append((k, mask(val), ph))
    return out
res = collections.Counter(); loc = collections.defaultdict(set)
mode = sys.argv[1]
if mode == "tree":
    root = sys.argv[2]
    for dp, dn, fs in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__", "venv", ".venv")]
        for f in fs:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 3_000_000: continue
                for i, line in enumerate(open(p, errors="ignore"), 1):
                    for k, mv, ph in scan_line(line):
                        tag = (k, "placeholder/test-like" if ph else "LIKELY-REAL")
                        res[tag] += 1; loc[tag].add(f"{os.path.relpath(p, root)}:{i} [{mv}]")
            except Exception: pass
else:
    repo, rev = sys.argv[2], sys.argv[3]
    proc = subprocess.Popen(["git", "-C", repo, "log", rev, "-p", "--no-color", "--unified=0", "--format=COMMIT %h", "--no-renames"],
                            stdout=subprocess.PIPE, text=True, errors="ignore")
    commit = path = None
    for line in proc.stdout:
        if line.startswith("COMMIT "): commit = line.split()[1]; continue
        if line.startswith("+++ b/"): path = line[6:].strip(); continue
        if not line.startswith("+") or line.startswith("+++"): continue
        for k, mv, ph in scan_line(line):
            tag = (k, "placeholder/test-like" if ph else "LIKELY-REAL")
            res[tag] += 1; loc[tag].add(f"{commit} {path} [{mv}]")
for tag, n in sorted(res.items()):
    print(tag, n, "distinct-locations:", len(loc[tag]))
    if tag[1] == "LIKELY-REAL":
        for l in sorted(loc[tag])[:15]: print("    ", l[:200])
