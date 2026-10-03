"""C-crawl: UI login as evalc, screenshot every page route, collect console errors / failed requests / dead links; then chat via UI."""
import json, sys, time, re, httpx
from playwright.sync_api import sync_playwright
B="http://127.0.0.1:8001"; OUT=sys.argv[1]; SH=OUT+"/C-screens"
ids=json.load(open(OUT+"/C-api-exercise.json"))["ids"]
PAGES=['/', '/standup', '/personality-preferences', '/learning', '/settings', '/settings/connected-apps', '/account', '/transparency', '/files', '/documents', '/insights', '/settings/integrations', '/settings/llm-keys', '/settings/preferences', '/settings/integrations/notion', '/settings/integrations/github', '/settings/integrations/slack', '/settings/integrations/calendar', '/settings/projects', '/lists', '/todos', '/projects', f"/projects/{ids['project']}", '/work-items', '/settings/privacy', '/settings/advanced', '/debug-markdown','/login','/reset-password','/setup']
res={}; links=set()
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); ctx=br.new_context(viewport={"width":1280,"height":900}); pg=ctx.new_page()
    cur={"c":[],"f":[]}
    pg.on("console", lambda m: cur["c"].append(m.text[:200]) if m.type=="error" else None)
    pg.on("pageerror", lambda e: cur["c"].append("PAGEERROR "+str(e)[:200]))
    pg.on("response", lambda r: cur["f"].append(f"{r.status} {r.request.method} {r.url.replace(B,'')}") if r.status>=400 else None)
    pg.goto(B+"/login"); pg.fill("#username","evalc"); pg.fill("#password","EvalC-pass-2026"); pg.click("#login-button")
    pg.wait_for_url(lambda u: "/login" not in u, timeout=20000); print("logged in ->",pg.url)
    for path in PAGES:
        cur["c"]=[];cur["f"]=[]; t=time.time()
        try:
            r=pg.goto(B+path,timeout=30000)
            try: pg.wait_for_load_state("networkidle",timeout=10000)
            except Exception: pass
            pg.wait_for_timeout(800)
            st=r.status if r else None
            name=re.sub(r'[^a-z0-9]+','_',path.strip('/').lower()) or 'home'
            name=name[:40]
            pg.screenshot(path=f"{SH}/pg_{name}.png",full_page=False)
            txt=pg.inner_text("body")[:20000]
            hrefs=pg.eval_on_selector_all("a[href]","els=>els.map(e=>e.getAttribute('href'))")
            for h in hrefs:
                if h and h.startswith('/') and not h.startswith('//'): links.add(h.split('#')[0])
            res[path]={"status":st,"final_url":pg.url.replace(B,''),"title":pg.title(),"secs":round(time.time()-t,1),
                "console_errors":cur["c"][:10],"failed_requests":sorted(set(cur["f"]))[:15],
                "empty_state_hint":bool(re.search(r"(?i)no (todos|projects|lists|files|documents|insights|items|patterns)|nothing here|get started|empty",txt)),
                "error_text":re.findall(r"(?i)[^.\n]*(?:error|failed|unable|went wrong|not available|couldn't)[^.\n]*",txt)[:5],
                "words":len(txt.split())}
        except Exception as e: res[path]={"exception":str(e)[:300]}
        print(path,res[path].get("status"),len(res[path].get("console_errors",[])),"cerr",len(res[path].get("failed_requests",[])),"fails")
    cookies={c['name']:c['value'] for c in ctx.cookies()}
    # chat via UI
    chat=[]
    pg.goto(B+"/"); pg.wait_for_timeout(2500)
    for msg in ["hello","what can you do?","add a todo: email the design team","show my todos","what time is it?","what should I focus on today?","remind me to call Sam tomorrow at 3pm","what's on my calendar today?","list open issues"]:
        cur["c"]=[];cur["f"]=[]
        before=pg.inner_text("body")
        t=time.time()
        try:
            pg.fill(".chat-input",msg); pg.keyboard.press("Enter")
            with pg.expect_response(lambda r: "/api/v1/intent" in r.url, timeout=90000) as ri: pass
            r=ri.value; body=r.text()[:1500]; st=r.status
        except Exception as e: body=f"EXC {e}"[:300]; st=None
        pg.wait_for_timeout(2500)
        after=pg.inner_text("body")
        new=after[len(before):] if after.startswith(before[:200]) else after[-800:]
        chat.append({"msg":msg,"api_status":st,"secs":round(time.time()-t,1),"api_body":body,"visible_tail":after[-700:],"console":cur["c"][:5],"failed":cur["f"][:5]})
        print("CHAT",msg,st,round(time.time()-t,1))
    pg.screenshot(path=f"{SH}/chat_after.png",full_page=True)
    br.close()
# dead-link check
c=httpx.Client(base_url=B,cookies=cookies,timeout=30,follow_redirects=False)
dl={}
for h in sorted(links):
    try: dl[h]=c.get(h).status_code
    except Exception as e: dl[h]=str(e)[:80]
json.dump({"pages":res,"links":dl,"chat":chat},open(OUT+"/C-crawl.json","w"),indent=1)
print("links",len(dl),{h:s for h,s in dl.items() if s not in (200,)})
