import httpx, json, os, time
B="http://127.0.0.1:8011"
KEY=os.environ.get("PIPER_TEST_ANTHROPIC_API_KEY","")
def mask(s):
    return s.replace(KEY,"[KEY]") if KEY else s
def client(): return httpx.Client(base_url=B, timeout=120)
def mkuser(c,name,tokfile):
    tok=open(tokfile).read().strip()
    r=c.post("/api/v1/setup/create-user",json={"username":name,"email":f"{name}@example.test","password":"Testpass-12345","password_confirm":"Testpass-12345","invite_token":tok})
    return r
def login(c,name):
    return c.post("/api/v1/auth/login",data={"username":name,"password":"Testpass-12345"})
def store(c,key):
    return c.post("/api/v1/keys/store",json={"provider":"anthropic","api_key":key,"validate":False})
N=[0]
def ask(c,msg,log):
    t=time.time()
    r=c.post("/api/v1/intent",json={"message":msg})
    dt=round(time.time()-t,2); N[0]+=1
    try: b=r.json()
    except Exception: b={"raw":r.text[:500]}
    rec={"msg":msg,"status":r.status_code,"secs":dt,"body":json.loads(mask(json.dumps(b)))}
    log.append(rec); return rec
