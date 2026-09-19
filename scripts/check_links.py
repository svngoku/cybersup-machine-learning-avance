from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json,requests
ROOT=Path(__file__).resolve().parents[1]
refs=json.loads((ROOT/"resources/sources.json").read_text())
def check(item):
    key,r=item
    if not r["url"].startswith("http"):return {"id":key,"status":"local"}
    try:
        response=requests.get(r["url"],timeout=35,headers={"User-Agent":"Mozilla/5.0 Cybersup-course-link-check"},stream=True)
        status=response.status_code;url=response.url;response.close()
        return {"id":key,"status":status,"url":url}
    except requests.RequestException as e:return {"id":key,"status":"error","error":str(e)}
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,refs.items()))
out=ROOT/".build";out.mkdir(exist_ok=True)
(out/"link-check.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
for r in results:print(r)
