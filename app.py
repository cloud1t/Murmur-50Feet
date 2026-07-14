from flask import Flask,jsonify,render_template,request
import json,time
from pathlib import Path

app=Flask(__name__)

@app.template_global()
def cst(s):
 try:
  from datetime import datetime,timedelta
  return (datetime.fromisoformat(s)+timedelta(hours=8)).strftime("%m-%d %H:%M")
 except:return s

STATE=Path("/root/murmur/state.json")
ARC=Path("/root/murmur/arc.jsonl")
REGRET=Path("/root/murmur/regret.jsonl")
MEM_LONG=Path("/root/murmur/memory_long.txt")
MEM_SHORT=Path("/root/murmur/memory_short.txt")
LAST=Path("/root/murmur/last_result.json")
ORDER=["attachment","tenderness","heartache","curiosity","mischief","restless","regret","desire","gloom","jealousy"]

@app.route("/")
def index():
 drives=[];top_drive=None
 if STATE.exists():
  s=json.loads(STATE.read_text(encoding="utf-8"))
  d=s.get("drives",{})
  if d:
   tk=max(d,key=lambda k:d[k]["v"])
   drives=[(k,d[k],k==tk) for k in ORDER if k in d]
   top_drive=d[tk]
 arcs=[]
 if ARC.exists():
  lines=[json.loads(l) for l in ARC.read_text(encoding="utf-8").splitlines() if l.strip()]
  arcs=list(reversed(lines[-50:]))
 regrets=[]
 if REGRET.exists():
  lines=[json.loads(l) for l in REGRET.read_text(encoding="utf-8").splitlines() if l.strip()]
  regrets=list(reversed(lines[-20:]))
 return render_template("index.html",drives=drives,arcs=arcs,top_drive=top_drive,regrets=regrets)

@app.route("/api/state")
def api_state():
 if STATE.exists():return jsonify(json.loads(STATE.read_text(encoding="utf-8")))
 return jsonify({})

@app.route("/api/arc")
def api_arc():
 if not ARC.exists():return jsonify([])
 lines=[json.loads(l) for l in ARC.read_text(encoding="utf-8").splitlines() if l.strip()]
 arc_type=request.args.get("type")
 if arc_type:lines=[l for l in lines if l.get("type")==arc_type]
 return jsonify(lines[-50:])

@app.route("/api/regret")
def api_regret():
 if not REGRET.exists():return jsonify([])
 lines=[json.loads(l) for l in REGRET.read_text(encoding="utf-8").splitlines() if l.strip()]
 return jsonify(lines[-50:])

@app.route("/api/memory")
def api_memory():
 long=MEM_LONG.read_text(encoding="utf-8").strip() if MEM_LONG.exists() else ""
 short=MEM_SHORT.read_text(encoding="utf-8").strip() if MEM_SHORT.exists() else ""
 return jsonify({"long":long,"short":short})

@app.route("/api/activate",methods=["POST"])
def activate():
 data=request.get_json(force=True)
 if LAST.exists():
  try:LAST.unlink()
  except:pass
 with open("/root/murmur/cmd.json","w",encoding="utf-8") as f:
  json.dump(data,f,ensure_ascii=False)
 t=data.get("type","")
 if t in("boost","write_arc"):
  for _ in range(50):
   time.sleep(0.1)
   if LAST.exists():
    return jsonify(json.loads(LAST.read_text(encoding="utf-8")))
  return jsonify({"ok":True,"warn":"timeout"})
 return jsonify({"ok":True})

if __name__=="__main__":
 app.run(host="0.0.0.0",port=8080,debug=False)
