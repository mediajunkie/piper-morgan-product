"""C-ui-crud: create todo/project/list via real UI dialogs, verify each appears after reload; settings timezone page."""
import json, sys
from playwright.sync_api import sync_playwright
B="http://127.0.0.1:8001"; OUT=sys.argv[1]; SH=OUT+"/C-screens"; R={}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); pg=br.new_page(viewport={"width":1280,"height":900})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto(B+"/login"); pg.fill("#username","evalc"); pg.fill("#password","EvalC-pass-2026"); pg.click("#login-button"); pg.wait_for_url(lambda u:"/login" not in u)
    for page,fn,inp,val in [("/todos","createNewTodo()","#new-todo-text","UI todo: draft PRD"),("/projects","createNewProject()","#new-project-name","UI Project Alpha"),("/lists","createNewList()","#new-list-name","UI Reading List")]:
        try:
            pg.goto(B+page); pg.wait_for_load_state("networkidle")
            pg.evaluate(fn); pg.fill(inp,val)
            with pg.expect_response(lambda r: r.request.method=="POST" and "/api/v1/" in r.url, timeout=15000) as ri:
                pg.keyboard.press("Enter") if False else pg.click("text=/^(Add it|Create|Create it|Create project|Create list|Save)$/")
            st=ri.value.status
            pg.wait_for_timeout(800); pg.reload(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
            seen=val in pg.inner_text("body")
            pg.screenshot(path=f"{SH}/crud{page.replace('/','_')}.png")
            R[page]={"post_status":st,"visible_after_reload":seen}
        except Exception as e: R[page]={"exception":str(e)[:300]}
        print(page,R[page])
    # complete the UI todo via its checkbox if present
    pg.goto(B+"/todos"); pg.wait_for_load_state("networkidle")
    cb=pg.locator("input[type=checkbox]").first
    if cb.count():
        cb.click(); pg.wait_for_timeout(1200); pg.reload(); pg.wait_for_load_state("networkidle")
        R["todo_complete_checkbox"]={"still_visible":"UI todo: draft PRD" in pg.inner_text("body")}
    R["pageerrors"]=errs
    json.dump(R,open(OUT+"/C-ui-crud.json","w"),indent=1); print(R.get("todo_complete_checkbox"),errs)
    br.close()
