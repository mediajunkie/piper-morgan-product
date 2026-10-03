#!/usr/bin/env python3
"""M2.1 session-start load per role + M1b.1 shared-vs-role-specific. tokens = chars/4 (UTF-8 chars, not bytes)."""
import os,csv,json
R='/home/user/audit-wt/'   # snapshot a191856
def ch(p):
    p=R+p
    return len(open(p,encoding='utf-8',errors='replace').read()) if os.path.exists(p) else None
HOOK=429   # measured: bash session-start.sh in audit-wt -> 429 bytes; budget in source = 500 chars
roles={ # role: (briefing, cycles?, extra mandated by briefing)
 'Lead Developer':('BRIEFING-ESSENTIAL-LEAD-DEV.md',1,[]),
 'Piper Alpha (PA)':('BRIEFING-piper-alpha.md',1,[]),
 'Chief Architect':('BRIEFING-ESSENTIAL-ARCHITECT.md',1,[]),
 'Chief of Staff (exec)':('BRIEFING-ESSENTIAL-CHIEF-STAFF.md',1,[]),
 'CXO':('BRIEFING-ESSENTIAL-CXO.md',1,[]),
 'CIO':('BRIEFING-ESSENTIAL-CIO.md',1,[]),
 'PPM':('BRIEFING-ESSENTIAL-PPM.md',1,[]),
 'HOST':('BRIEFING-ESSENTIAL-HOST.md',1,[]),
 'Comms':('BRIEFING-ESSENTIAL-COMMS.md',1,['docs/internal/planning/comms/xian-voice-tone-guide.md','docs/internal/planning/comms/publishing-cadence.md','docs/internal/planning/comms/building-narrative-method.md']),
 'Docs':('BRIEFING-ESSENTIAL-DOCS.md',1,['dev/2026/07/29/docs-handoff-2026-07-28.md']),
 'Coding Agent':('BRIEFING-ESSENTIAL-AGENT.md',0,[]),
 'Web':('BRIEFING-ESSENTIAL-WEB.md',1,[]),
 'ETA (dormant)':('BRIEFING-ESSENTIAL-ETA.md',0,[]),
}
common={'CLAUDE.md':ch('CLAUDE.md'),
 'docs/briefing/BRIEFING-CURRENT-STATE.md':ch('docs/briefing/BRIEFING-CURRENT-STATE.md'),
 'docs/briefs/cross-pollination/current.md':ch('docs/briefs/cross-pollination/current.md'),
 'session-start hook output (measured)':HOOK}
ext_skills={'.claude/skills/create-session-log/SKILL.md':ch('.claude/skills/create-session-log/SKILL.md'),
 '.claude/skills/check-mailbox/SKILL.md':ch('.claude/skills/check-mailbox/SKILL.md')}
tick=ch('.claude/skills/duty-cycle-tick/SKILL.md')
skilldesc=14717  # chars of 37 SKILL.md frontmatter blocks (auto-listed in system prompt)
rows=[];loads={}
for r,(b,cy,ex) in roles.items():
    bc=ch('docs/briefing/'+b)
    exc=sum(ch(e) or 0 for e in ex)
    base=sum(common.values())+bc
    ext=base+sum(ext_skills.values())+exc
    full=ext+(tick if cy else 0)
    docs=dict(common);docs['docs/briefing/'+b]=bc
    for e in ex: docs[e]=ch(e)
    loads[r]=dict(docs)
    loads[r].update({k:v for k,v in ext_skills.items()})
    if cy: loads[r]['.claude/skills/duty-cycle-tick/SKILL.md']=tick
    rows.append(dict(role=r,cycles=cy,claude_md_tok=common['CLAUDE.md']//4,briefing_tok=bc//4,current_state_tok=common['docs/briefing/BRIEFING-CURRENT-STATE.md']//4,xpoll_tok=common['docs/briefs/cross-pollination/current.md']//4,hook_tok=HOOK//4,
     base_tok=base//4,base_plus_mandated_extras_and_startup_skills_tok=ext//4,with_dutycycle_skill_tok=full//4,briefing_mandated_extra_tok=exc//4))
w=csv.DictWriter(open('D-m21-per-role.csv','w'),fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# M1b.1 : per doc, roles loading x size, vs total
tot=0;per={}
for r,d in loads.items():
    for k,v in d.items():
        per.setdefault(k,[0,v]);per[k][0]+=1;tot+=v
out=[]
for k,(n,v) in sorted(per.items(),key=lambda x:-x[1][0]*x[1][1]):
    out.append(dict(doc=k,roles_loading=n,tokens=v//4,role_tokens_total=n*v//4,share_of_all_role_load=round(n*v/tot,3)))
w=csv.DictWriter(open('D-m1b1-shared.csv','w'),fieldnames=out[0].keys());w.writeheader();w.writerows(out)
# role-specific share per role (strict base, extended, with-tick): role-specific = docs loaded by exactly 1 role
res=[]
for r,d in loads.items():
    t=sum(d.values()); spec=sum(v for k,v in d.items() if per[k][0]==1)
    base_t=sum(v for k,v in d.items() if k in common or k==('docs/briefing/'+roles[r][0]))
    spec_base=sum(v for k,v in d.items() if (k in ('docs/briefing/'+roles[r][0],) ) and per[k][0]==1)
    res.append(dict(role=r,total_tok=t//4,role_specific_tok=spec//4,role_specific_share=round(spec/t,3),base_total_tok=base_t//4,base_role_specific_share=round(spec_base/base_t,3)))
w=csv.DictWriter(open('D-m1b1-role-specific-share.csv','w'),fieldnames=res[0].keys());w.writeheader();w.writerows(res)
print('skill_frontmatter_tok',skilldesc//4,'tick_tok',tick//4)
for r in rows:print(r)
for r in res:print(r)
for o in out[:8]:print(o)
