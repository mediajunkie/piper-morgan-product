# Measures (prereg H4 mechanism dates; deliverable items 4 & 8): month-end snapshots via git ls-tree/grep/show (no checkout):
# CLAUDE.md bytes/lines and MoM growth (flag >25%), .claude/skills count (dirs holding SKILL.md) and bytes, .claude/hooks file count,
# docs/briefing bytes, services+web *.py LOC (git grep -c '' on tree). Month-end = last commit on or before month end (snapshot-bounded).
# Plus first-add dates: first mailboxes/ commit, first .claude/skills/duty-cycle-tick commit, each .claude/hooks file first-add.
import csv,re,datetime,calendar
from common import *
def ms(m):
    y,mm=map(int,m.split('-')); e=datetime.datetime(y,mm,calendar.monthrange(y,mm)[1],23,59,59,tzinfo=datetime.timezone.utc)
    return min(e.timestamp(),1791049304)
rows=[];prev=None
for m in months():
    rev=git('rev-list','-1',f'--before={int(ms(m))}',SNAP).strip()
    if not rev: continue
    tree=git('ls-tree','-r','-l',rev).splitlines()
    sizes={};
    for t in tree:
        meta,p=t.split('\t',1); sizes[p]=int(meta.split()[3]) if meta.split()[3]!='-' else 0
    cm=git('show',f'{rev}:CLAUDE.md') if 'CLAUDE.md' in sizes else ''
    cb=sizes.get('CLAUDE.md',0);cl=cm.count('\n')
    sk={p.split('/')[2] for p in sizes if p.startswith('.claude/skills/') and p.endswith('SKILL.md')}
    skb=sum(v for p,v in sizes.items() if p.startswith('.claude/skills/'))
    hk=[p for p in sizes if p.startswith('.claude/hooks/')]
    bb=sum(v for p,v in sizes.items() if p.startswith('docs/briefing/'))
    loc=0
    for l in git('grep','-c','',rev,'--','services/*.py','web/*.py').splitlines():
        loc+=int(l.rsplit(':',1)[1])
    g=(cb/prev-1) if prev else ''
    prev=cb or prev
    rows.append([m,rev[:10],cb,cl,round(g,3) if g!='' else '',int(g>0.25) if g!='' else '',len(sk),skb,len(hk),bb,loc])
with open('m4_snapshots.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['month','rev','claude_md_bytes','claude_md_lines','claude_md_mom_growth','gt25pct','skills_count','skills_bytes','hooks_files','docs_briefing_bytes','services_web_py_loc']);w.writerows(rows)
print(open('m4_snapshots.csv').read())
def first(paths,*extra):
    out=git('log',SNAP,'--reverse','--diff-filter=A','--format=@@%h %ad','--date=short','--name-only','--',*paths).splitlines()
    return out
print('--first mailboxes/ commit:')
o=git('log',SNAP,'--reverse','--format=%h %ad %s','--date=short','--',"mailboxes").splitlines()[:1];print(o)
print('--first duty-cycle-tick:')
print(git('log',SNAP,'--reverse','--format=%h %ad %s','--date=short','--','.claude/skills/duty-cycle-tick').splitlines()[:1])
print('--hooks first-add:')
cur=None;seen={}
for l in git('log',SNAP,'--reverse','--no-renames','--diff-filter=A','--format=@@%h %ad','--date=short','--name-only','--','.claude/hooks').splitlines():
    if l.startswith('@@'):cur=l[2:]
    elif l and l not in seen: seen[l]=cur
with open('m4_hooks_first_add.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['file','first_add_sha_date']);
    for k,v in seen.items(): w.writerow([k,v]);print(k,v)
