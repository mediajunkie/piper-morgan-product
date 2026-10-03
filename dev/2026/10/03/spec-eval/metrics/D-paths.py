#!/usr/bin/env python3
"""M2.2 stale-path check. Extract backticked/plain path tokens from CLAUDE.md, docs/briefing/*.md, SKILL.md files, settings; test existence in snapshot a191856 (/home/user/audit-wt)."""
import re,os,glob,csv,sys
R='/home/user/audit-wt/'
files=['CLAUDE.md']+sorted(glob.glob(R+'docs/briefing/*.md'))+sorted(glob.glob(R+'.claude/skills/*/SKILL.md'))
files=[f if f.startswith('/') else R+f for f in files]
pat=re.compile(r'(?<![\w/.:@-])((?:\.claude|docs|dev|scripts|services|web|tests|mailboxes|config|knowledge|alembic|cli|templates|data|tools|shared|main\.py|skunkworks|\.github)(?:/[^\s`\'"<>()\[\]|,;*]*)+)')
rows=[];seen=set()
for f in files:
    rel=f.replace(R,'')
    for i,l in enumerate(open(f,encoding='utf-8',errors='replace'),1):
        for m in pat.finditer(l):
            p=re.sub(r':\d+(-\d+)?$','',m.group(1).rstrip('.:)*_'))
            if re.search(r'[{}$*<>]|YYYY|NNN|\.\.\.|\bXX|\{|role\]|ROLE|\[', p): continue
            if p.endswith('/'): pass
            key=(rel,p)
            if key in seen: continue
            seen.add(key)
            ex=os.path.exists(R+p.rstrip('/')) 
            rows.append((rel,i,p,ex))
w=csv.writer(open('D-paths.csv','w'));w.writerow(['file','line','path','exists']);w.writerows(rows)
tot=len(rows);miss=[r for r in rows if not r[3]]
print('checked',tot,'missing',len(miss))
from collections import Counter
c=Counter(r[0] for r in miss);print(c.most_common(12))
cm=[r for r in miss if r[0]=='CLAUDE.md'];print('CLAUDE.md missing:');[print(r) for r in cm]
print('briefing-only missing (non-skill):',sum(1 for r in miss if r[0].startswith('docs/briefing')))
