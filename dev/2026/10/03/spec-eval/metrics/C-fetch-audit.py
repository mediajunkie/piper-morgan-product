"""C-fetch-audit: every literal /api/... URL the UI (templates + static js) calls, checked against live OpenAPI routes."""
import re,glob,json,sys
spec=json.load(open('/tmp/claude-0/-home-user/03717665-1eb6-52ef-ab7b-3677cba046df/scratchpad/openapi.json'))
pats=[re.compile('^'+re.sub(r'\{[^}]+\}','[^/]+',p.rstrip('/'))+'/?$') for p in spec['paths']]
urls={}
for f in glob.glob('templates/**/*.html',recursive=True)+glob.glob('web/static/js/*.js'):
    for u in re.findall(r"""[`'"](/api/[A-Za-z0-9_\-/{}$.]+)""",open(f).read()):
        u=re.sub(r'\$\{[^}]*\}','X',u).split('?')[0]
        urls.setdefault(u,set()).add(f)
miss={u:sorted(fs) for u,fs in urls.items() if not any(p.match(u.rstrip('/')) or p.match(u) for p in pats) and not u.endswith('/')}
print('ui api urls',len(urls),'unmatched',len(miss))
for u,fs in sorted(miss.items()): print(' ',u,fs[:2])
json.dump({"total":len(urls),"unmatched":miss},open(sys.argv[1],'w'),indent=1)
