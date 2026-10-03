"""C-LLM probe 3: the 16 messages behind the 16 failing tests/unit/services/test_multi_intent.py tests (B6), sent to the live LLM-backed chat."""
import importlib.util,sys,json
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
c=L.client(); L.login(c,"llmgood"); H={"X-User-Api-Key":L.KEY}
cases=[("test_greeting_plus_agenda_query","Hi Piper! What's on my agenda?","calendar"),
("test_hello_plus_calendar","Hello! What's on my calendar today?","calendar"),
("test_hey_plus_meetings","Hey, do I have any meetings today?","calendar"),
("test_greeting_plus_schedule","Good morning! What's my schedule today?","calendar"),
("test_greeting_plus_todos","Hi! Show my todos","todos"),
("test_greeting_plus_status","Hello! What am I working on?","status"),
("test_greeting_plus_priority","Hey Piper, what should I focus on today?","priority"),
("test_single_query_only","What's on my agenda?","calendar"),
("test_emoji_in_greeting","Hi! 👋 What's my schedule?","calendar"),
("test_multiple_substantive_intents","What's on my calendar and show my todos","calendar+todos"),
("test_case_insensitive_detection","HI PIPER! WHAT'S ON MY AGENDA?","calendar"),
("test_extra_whitespace_handling",sys.argv[1] if len(sys.argv)>1 else "Hi  Piper!   What's on my agenda?","calendar"),
("test_exclamation_points","Hello!!! What's on my calendar???","calendar"),
("test_agenda_today_is_meeting_time","Hi! What's on my agenda?","calendar"),
("test_week_calendar_is_week_calendar","Hi! What's my week look like?","calendar"),
("test_recurring_meetings_is_recurring","Hi! Show my recurring meetings","calendar")]
log=[]
for name,m,exp in cases:
    r=L.ask(c,m,log,hdr=H,tag=name); r["expected"]=exp
    b=r["body"];i=b.get("intent") or {}
    print(r["secs"],i.get("category"),i.get("action"),"|",m,"=>",(b.get("message") or "")[:170].replace("\n"," "))
json.dump(log,open("C-LLM-probe3.json","w"),indent=1,ensure_ascii=False)
