# Shared helpers for D0 metrics. Snapshot-bounded git access.
import subprocess, datetime, re
REPO='/home/user/piper-morgan-product'; SNAP='a191856164351cf59ba033d7dbc4a34f036c6122'
def git(*a, text=True):
    return subprocess.run(['git','-c','core.quotepath=off','-C',REPO,*a],capture_output=True,text=text,errors='replace').stdout
def stream(*a):
    p=subprocess.Popen(['git','-c','core.quotepath=off','-C',REPO,*a],stdout=subprocess.PIPE,errors='replace',text=True,bufsize=1<<20)
    for l in p.stdout: yield l.rstrip('\n')
    p.wait()
def month(ts): return datetime.datetime.fromtimestamp(int(ts),datetime.timezone.utc).strftime('%Y-%m')
def day(ts): return datetime.datetime.fromtimestamp(int(ts),datetime.timezone.utc).strftime('%Y-%m-%d')
PC_PREFIX=('services/','web/','templates/','alembic/','cli/')
def is_pc(p): return p.startswith(PC_PREFIX) or p=='main.py'
def is_tc(p): return p.startswith('tests/')
COORD=re.compile(r'^(mail|log|hb-last-invoked|hb|stop|heartbeat)(\(|:|\s|$)',re.I)
def coord_class(subj):
    m=COORD.match(subj); return m.group(1).lower() if m else None
def months():
    out=[];y,m=2025,6
    while (y,m)<=(2026,10):
        out.append(f'{y}-{m:02d}'); m+=1
        if m>12:y+=1;m=1
    return out
