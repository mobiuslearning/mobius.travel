import json, pathlib, subprocess, concurrent.futures
root=pathlib.Path(__file__).resolve().parents[1]
specs=[('438','3d085397bf904e649ce97eb6c4bd9c7a','长城 · 局部建筑','摄影测量模型'),('91','535dc96e586f40bd956ea3cbff810055','罗马斗兽场','精细建筑模型'),('252','1eb09052f6cd421caeaa6cb3204cb15d','泰姬陵','精细建筑模型'),('668','be70b89f9c264fc19d63dca2ae78b224','吴哥窟','影像重建模型'),('326','33b7de00da1a4057a637824007ba73ad','佩特拉 · 卡兹尼神殿','激光扫描模型'),('592','d42b4ad2e4fd443e838df1d8df1830d0','婆罗浮屠','精细建筑模型'),('483','a073249838ad419c8beb35ff32bebf3d','奇琴伊察 · 库库尔坎金字塔','摄影测量模型')]
def one(s):
    heritage,uid,title,kind=s;p=pathlib.Path('/private/tmp')/f'mobius-model-{uid}.json'
    if not p.exists():
        r=subprocess.run(['curl','-sSL','--fail','--retry','2','--max-time','45',f'https://api.sketchfab.com/v3/models/{uid}','-o',str(p)],capture_output=True)
    x=json.loads(p.read_text());license=x.get('license') or {}
    return {'heritage':heritage,'uid':uid,'title':title,'kind':kind,'author':x['user'].get('displayName') or x['user']['username'],'authorUrl':x['user']['profileUrl'],'url':x['viewerUrl'],'embed':x['embedUrl'],'license':license.get('label','作者平台展示条款'),'licenseUrl':license.get('url','https://sketchfab.com/terms'),'licenseSlug':license.get('slug','platform'),'faces':x.get('faceCount'),'description':x.get('description','')[:400],'verified':'2026-10-23'}
models=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    jobs={pool.submit(one,s):s for s in specs}
    for j in concurrent.futures.as_completed(jobs):
        try:
            m=j.result();models.append(m);print(m['title'],m['author'],m['license'],flush=True)
        except Exception as e:print('Unavailable',jobs[j][0],str(e)[:100],flush=True)
(root/'public/data/model-registry.json').write_text(json.dumps(models,ensure_ascii=False,separators=(',',':')))
