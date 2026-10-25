import json, pathlib, subprocess, concurrent.futures, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'public/data/admin';OUT.mkdir(parents=True,exist_ok=True)
RAW=pathlib.Path('/private/tmp/mobius-geodata');RAW.mkdir(exist_ok=True)
def fetch(url,path):
    if path.exists():
        try:return json.loads(path.read_text())
        except:pass
    p=subprocess.run(['curl','-sSL','--fail','--retry','2','--max-time','100',url,'-o',str(path)],capture_output=True)
    try:return json.loads(path.read_text())
    except:raise RuntimeError(url+' '+p.stderr.decode()[-160:])
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
def rounded(v):
    if isinstance(v,list):return [rounded(x) for x in v]
    return round(v,5) if isinstance(v,float) else v
def compact(data):
    return {'type':'FeatureCollection','features':[{'type':'Feature','properties':f['properties'],'geometry':{'type':f['geometry']['type'],'coordinates':rounded(f['geometry']['coordinates'])}} for f in data['features'] if f['properties'].get('name') or f['properties'].get('shapeName')]}
def china(code):
    target=OUT/f'CN-{code}.json'
    if target.exists():return json.loads(target.read_text())
    url=f'https://geo.datav.aliyun.com/areas_v3/bound/{code}_full.json'
    d=compact(fetch(url,RAW/f'CN-{code}.json'));dump(target,d);return d
root=json.loads((ROOT/'public/data/100000.json').read_text());provinces=[f['properties'] for f in root['features'] if f['properties'].get('adcode') and f['properties'].get('name')]
dump(OUT/'CN-100000.json',compact(root))
errors=[];cities=[];count=0
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    jobs={pool.submit(china,p['adcode']):p for p in provinces}
    for job in concurrent.futures.as_completed(jobs):
        p=jobs[job]
        try:
            d=job.result();count+=1
            cities += [f['properties']['adcode'] for f in d['features'] if f['properties'].get('level')=='city' and f['properties'].get('childrenNum',0)>0]
        except Exception as e:errors.append({'code':p['adcode'],'error':str(e)})
    print('China provinces:',count,'prefecture downloads:',len(cities),flush=True)
    jobs={pool.submit(china,c):c for c in cities}
    for i,job in enumerate(concurrent.futures.as_completed(jobs)):
        try:job.result();count+=1
        except Exception as e:errors.append({'code':jobs[job],'error':str(e)})
        if i%50==0:print('China progress',i+1,'/',len(cities),flush=True)
index=[]
for f in OUT.glob('CN-*.json'):
    for v in json.loads(f.read_text())['features']:
        p=v['properties'];index.append({'name':p['name'],'code':p['adcode'],'level':p.get('level'),'path':p.get('acroutes',[]),'center':p.get('center',p.get('centroid'))})
index={p['code']:p for p in index}
dump(ROOT/'public/data/china-index.json',list(index.values()))
dump(ROOT/'public/data/china-coverage.json',{'source':'DataV','retrieved':'2026-10-23','files':count+1,'regions':len(index),'failed':errors})
print('China complete:',count+1,'files,',len(index),'regions, errors',len(errors),flush=True)
