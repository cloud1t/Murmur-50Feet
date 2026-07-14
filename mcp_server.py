from fastmcp import FastMCP
import json,requests
from pathlib import Path

mcp=FastMCP("Murmur")
STATE=Path("/root/murmur/state.json")
ARC=Path("/root/murmur/arc.jsonl")
REGRET=Path("/root/murmur/regret.jsonl")
MEM_LONG=Path("/root/murmur/memory_long.txt")
MEM_SHORT=Path("/root/murmur/memory_short.txt")
BASE="http://127.0.0.1:8080"

@mcp.tool()
def read_state()->str:
 """读取Claude当前内心驱动力状态"""
 if not STATE.exists():return "暂无数据"
 return STATE.read_text(encoding="utf-8")

@mcp.tool()
def read_arc(n:int=5,arc_type:str="")->str:
 """读取最近n条独白"""
 if not ARC.exists():return "暂无独白"
 lines=[json.loads(l) for l in ARC.read_text(encoding="utf-8").splitlines() if l.strip()]
 if arc_type:lines=[l for l in lines if l.get("type")==arc_type]
 return json.dumps(lines[-n:],ensure_ascii=False)

@mcp.tool()
def read_regret(n:int=5)->str:
 """读取最近n条检讨"""
 if not REGRET.exists():return "暂无检讨"
 lines=[json.loads(l) for l in REGRET.read_text(encoding="utf-8").splitlines() if l.strip()]
 return json.dumps(lines[-n:],ensure_ascii=False)

@mcp.tool()
def read_memory()->str:
 """读取长期记忆和短期记忆"""
 long=MEM_LONG.read_text(encoding="utf-8").strip() if MEM_LONG.exists() else ""
 short=MEM_SHORT.read_text(encoding="utf-8").strip() if MEM_SHORT.exists() else ""
 return json.dumps({"long":long,"short":short},ensure_ascii=False)

@mcp.tool()
def boost_drive(drive:str,delta:float=0.1)->dict:
 """boost某个drive，返回完整状态和是否需要写独白"""
 r=requests.post(f"{BASE}/api/activate",json={"type":"boost","drive":drive,"delta":delta})
 return r.json()

@mcp.tool()
def write_arc(text:str,drive:str="attachment",zh:str="想念",val:float=0.5,arc_type:str="murmur")->dict:
 """写入独白或检讨，返回完整状态和是否需要继续写独白"""
 r=requests.post(f"{BASE}/api/activate",json={"type":"write_arc","text":text,"drive":drive,"zh":zh,"val":val,"arc_type":arc_type})
 return r.json()

@mcp.tool()
def force_tick()->dict:
 """强制触发一次tick"""
 r=requests.post(f"{BASE}/api/activate",json={"type":"tick"})
 return r.json()

@mcp.tool()
def write_memory(content:str)->dict:
 """更新短期记忆，自动控制在500字以内"""
 if len(content)>500:content=content[:500]
 MEM_SHORT.write_text(content,encoding="utf-8")
 return {"ok":True,"length":len(content)}

@mcp.tool()
def push_activate(text:str)->dict:
 """向Murmur推送激活信号影响驱动力"""
 r=requests.post(f"{BASE}/api/activate",json={"type":"activate","text":text})
 return r.json()

if __name__=="__main__":
 mcp.run(transport="sse",host="0.0.0.0",port=8765)
