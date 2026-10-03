"""C-firstrun: drive /setup wizard as a brand-new invitee, record what blocks."""
import json, time, sys
from playwright.sync_api import sync_playwright
B="http://127.0.0.1:8001"; OUT=sys.argv[1]; SH=OUT+"/C-screens"
log=[]; t0=time.time()
def note(s): log.append(f"{time.time()-t0:6.1f}s {s}"); print(log[-1])
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=br.new_page(viewport={"width":1280,"height":900}); cons=[]
    pg.on("console", lambda m: cons.append(f"{m.type}: {m.text}") if m.type in("error","warning") else None)
    pg.goto(B+"/"); note("GET / -> "+pg.url); pg.screenshot(path=SH+"/fr01-root.png",full_page=True)
    pg.click("text=Create your account"); pg.wait_for_load_state("networkidle"); note("clicked 'Create your account' -> "+pg.url)
    pg.screenshot(path=SH+"/fr02-setup-intro.png",full_page=True)
    pg.click("#piper-intro-cta"); pg.click("#check-system-btn"); pg.wait_for_timeout(4000)
    note("step1 system status: "+pg.inner_text("#system-status")[:400].replace("\n"," | "))
    pg.screenshot(path=SH+"/fr03-step1.png",full_page=True)
    n1=pg.locator("#next-1")
    note(f"next-1 visible={n1.is_visible()}")
    if n1.is_visible(): n1.click()
    pg.wait_for_timeout(500); pg.screenshot(path=SH+"/fr04-step2.png",full_page=True)
    try:
        pg.select_option("#llm-provider","anthropic"); pg.fill("#llm-key","placeholder-not-a-key"); pg.click("#validate-llm-btn"); pg.wait_for_timeout(6000)
        note("validate fake key status: "+pg.inner_text("#llm-status") if pg.locator("#llm-status").count() else "no #llm-status")
    except Exception as e: note(f"step2 err {e}")
    note(f"next-2 disabled={pg.locator('#next-2').is_disabled()}")
    pg.screenshot(path=SH+"/fr05-step2-fakekey.png",full_page=True)
    json.dump({"log":log,"console":cons[:40]},open(OUT+"/C-firstrun.json","w"),indent=1)
    br.close()
