#!/usr/bin/env python3
"""D-propose context-cost delta. Same method as D-m21.py (tokens = chars/4), reading
D-m21-per-role.csv for 'before' and substituting proposed sizes for 'after'."""
import csv,os,re,subprocess
H=os.path.dirname(os.path.abspath(__file__))
prop=len(open(os.path.join(H,'..','D-proposed-CLAUDE.md'),encoding='utf-8').read())//4
SNAP='a191856'
def show(p): return subprocess.run(['git','-C','/home/user/piper-morgan-product','show',f'{SNAP}:{p}'],capture_output=True,text=True).stdout
cs=show('docs/briefing/BRIEFING-CURRENT-STATE.md').splitlines(True)
interim=len(''.join(cs[17:72]))//4      # STATUS BANNER + Inchworm Position (lines 18-72): read-only-the-top, no file change
NOW_TARGET=3000                          # proposed split: 'Now' file <= 3k tokens; Recent Progress -> history log
TICK_BEFORE=len(show('.claude/skills/duty-cycle-tick/SKILL.md'))//4
TICK_TARGET=6000                         # proposed: core procedure <= 6k; cron-mechanism, Gap-C, examples -> references/
# skill-list (system prompt) cost: frontmatter description of skills proposed for relocation/deletion
reloc=['piper-draft-issue','piper-draft-spec','piper-sprint-plan','piper-stakeholder-update','piper-synthesize-feedback','compost-review','propose-feature','trust-check','update-piper','deliver-mail','close-issue']
def fm(s):
    m=re.match(r'---\n(.*?)\n---',s,re.S); return len(m.group(1)) if m else 0
desc_saved=sum(fm(show(f'.claude/skills/{k}/SKILL.md')) for k in reloc)//4
rows=[]
for r in csv.DictReader(open(os.path.join(H,'D-m21-per-role.csv'))):
    cy=int(r['cycles']); claude=int(r['claude_md_tok']); cur=int(r['current_state_tok'])
    before=int(r['with_dutycycle_skill_tok'])
    s1=before-claude+prop                       # step: CLAUDE.md only
    s2a=s1-cur+interim                          # + read banner/inchworm only
    s2=s1-cur+NOW_TARGET                        # + CURRENT-STATE split
    s3=s2-(TICK_BEFORE-TICK_TARGET if cy else 0)  # + tick skill split
    rows.append(dict(role=r['role'],cycles=cy,before=before,after_claude=s1,after_current_state_interim=s2a,
      after_current_state_split=s2,after_tick_split=s3,pct_reduction=round(100*(before-s3)/before,1)))
w=csv.DictWriter(open(os.path.join(H,'D-propose-delta.csv'),'w'),fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print('proposed CLAUDE.md tok',prop,'| CURRENT-STATE banner+inchworm tok',interim,'| tick before',TICK_BEFORE,'| skill-list desc saved',desc_saved)
for x in rows: print(x)
