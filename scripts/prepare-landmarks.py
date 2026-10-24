"""Build a reproducible CC0 city-attraction snapshot from Wikidata SPARQL exports.
Inputs: /private/tmp/mobius-{landmarks,china-landmarks,country-codes}.json.
Keep individual Wikidata item URLs so users can inspect the original claims.
"""
import json,re,collections,datetime
from pathlib import Path
out=Path('public/data')
snapshot=Path('data/landmarks.json')
read=lambda name:json.load(open('/private/tmp/mobius-'+name+'.json'))['results']['bindings']
value=lambda row,key:row.get(key,{}).get('value','')
simplify=lambda text:text.translate(str.maketrans({'遺':'遗','館':'馆','藝':'艺','術':'术','國':'国','園':'园','廣':'广','場':'场','門':'门','樓':'楼','廟':'庙','觀':'观','橋':'桥','聖':'圣','龍':'龙','馬':'马','麗':'丽','雲':'云','巖':'岩','寶':'宝','達':'达','臺':'台','灣':'湾','長':'长','區':'区','峽':'峡','溝':'沟','慶':'庆','漢':'汉','開':'开','興':'兴','會':'会','蘇':'苏','雙':'双','鍾':'钟','鐘':'钟','寧':'宁','實':'实','歷':'历','蘭':'兰','爾':'尔','爲':'为','為':'为','與':'与','於':'于','東':'东','樂':'乐','聲':'声','鐵':'铁','羅':'罗','維':'维','紀':'纪','盧':'卢','礦':'矿','蓋':'盖','殿':'殿','宮':'宫','壽':'寿','壇':'坛','鄉':'乡','圓':'圆','齋':'斋','幣':'币','護':'护','濕':'湿','熱':'热','歡':'欢','義':'义','軍':'军','愛':'爱','絲':'丝','華':'华','濱':'滨','岡':'冈','嶺':'岭','樹':'树','萬':'万','叢':'丛','夢':'梦','蘆':'芦','蓮':'莲','棲':'栖','風':'风','飛':'飞','陳':'陈','張':'张','莊':'庄','陸':'陆','嶽':'岳','遊':'游','裡':'里','貝':'贝','彌':'弥','薩':'萨','德':'德','審':'审'}))
codes={value(r,'country'):value(r,'code') for r in read('country-codes')}
countries={c['alpha2']:c['name'] for c in json.load(open(out/'country-index.json'))}
rows=read('landmarks'); china=read('china-landmarks'); famous=read('famous');
extras=[(name,read(name)) for name in ['china-local','global-museums','global-places']]
baseline={p['id']:p for p in json.load(open(snapshot))} if snapshot.exists() else {}
famous_ids={value(r,'item') for r in famous}
# A city, station or school is not a visitor attraction merely because it has coordinates.
allowed=r'文物保护|文物保護|文化遺產|文化遗产|摩天大樓|摩天大楼|^塔$|^山$|^湖泊$|^石窟$|古桥|古橋|广场|廣場|博物|美術館|美术馆|藝術館|艺术馆|纪念馆|紀念館|公園|公园|花園|花园|園林|园林|植物園|植物园|动物园|動物園|水族|寺廟|寺庙|佛寺|道觀|道观|宫殿|宮殿|皇宮|皇宫|陵墓|陵寝|考古|古遺址|古遗址|遺址|遗址|古城|歷史建築|历史建筑|历史街区|歷史街區|旅遊景|旅游景|風景|风景|自然保護|自然保护|国家森林|國家森林|地質公園|地质公园|世界遗产|世界遺產|教堂|大教堂|清真寺|紀念碑|纪念碑|城堡|museum|gallery|palace|castle|temple|monument|archaeological|botanical|national park|tourist attraction|heritage site|historic building|historic district|zoo|aquarium|pagoda|garden|cave|waterfall|mountain|觀景|观景'
kindmap=[('museum','博物馆与艺术',r'博物|美術|美术|艺术馆|藝術館|museum|gallery'),('nature','山水与自然',r'湖泊|山峰|名山|自然|森林|地質|地质|風景|风景|waterfall|mountain|cave|瀑布|山峰|的山|山(?:$| ·)|^山$|^湖$|^洞穴$|国家公园|國家公園'),('park','公园与花园',r'公園|公园|園林|园林|花園|花园|植物園|植物园|park|garden|zoo|aquarium|水族|动物园|動物園'),('historic','古迹与建筑',r'僧院|修院|遺址|遗址|墓|碑|关隘|牌坊|教堂|寺|道觀|道观|礼拜堂|禮拜堂|祠|城堡|陵|古城|宮|宫|pagoda|cathedral|church|temple|palace|castle|archaeological|historic|tomb|mosque'),('landmark','城市地标',r'.')]
kindmap=[kindmap[0],kindmap[3],kindmap[1],kindmap[2],kindmap[4]]
merged={}
for r,origin in [(r,'world') for r in rows]+[(r,'china') for r in china]+[(r,'famous') for r in famous]+[(r,name) for name,data in extras for r in data]:
 key=value(r,'item').rsplit('/',1)[-1]
 if key not in merged:merged[key]={'row':r,'types':set(),'china':False,'countries':set(),'english':''}
 if value(r,'typeLabel'):merged[key]['types'].add(value(r,'typeLabel'))
 if value(r,'country'):merged[key]['countries'].add(value(r,'country'))
 if value(r,'english'):merged[key]['english']=value(r,'english')
 if not value(merged[key]['row'],'image') and value(r,'image'):merged[key]['row']=r
 # China export omits country because its query fixes P17 to China.
 if origin in ['china','china-local']:merged[key]['china']=True
 if value(r,'country') and not value(merged[key]['row'],'country'):merged[key]['row']=r
places=[]
for key,entry in merged.items():
 r=entry['row'];name=value(r,'itemLabel');description=value(r,'itemDescription');types=' · '.join(sorted(entry['types']));is_cn=entry['china'] or value(r,'country').endswith('/Q148');is_famous=value(r,'item') in famous_ids
 if (is_cn or is_famous) and not re.search(allowed,types,re.I) and not (is_famous and re.search(r'觀光塔|观光塔|电视塔|電視塔|鐘樓|钟楼|橋|桥|雕像|塑像|大佛|觀景|观景|shopping|購物|购物|街道|大街|道路|street|通道|門戶|gate|tower|bridge|sculpture|landmark|amusement|entertainment|performing arts|theatre|歌劇院|歌剧院|音乐厅|音樂廳|高層建築|高层建筑|摩天|建築群|建筑群|觀光地|观光地',types,re.I)):continue
 if re.search(r'考古學文化|考古学文化|大學|大学|地级市|地級市|副省级市',types) and not is_famous:continue
 # Foreign export already restricts direct P31 to attraction classes.
 if not name or re.fullmatch(r'Q\d+',name):continue
 match=re.fullmatch(r'Point\((-?[\d.]+) (-?[\d.]+)\)',value(r,'coord'))
 if not match:continue
 lon,lat=map(float,match.groups())
 if abs(lat)>90 or abs(lon)>180:continue
 code='CN' if is_cn else codes.get(value(r,'country'))
 if code not in countries:continue
 text=types+' '+description+' '+name
 subtype,tag,_=next(k for k in kindmap if re.search(k[2],text,re.I))
 image=value(r,'image').replace('http:','https:')
 if image:image+='?width=640'
 country=countries[code];name=simplify(name);description=simplify(description)
 country_codes=sorted(set([code]+[codes.get(c) for c in entry['countries'] if codes.get(c) in countries]))
 places.append(dict(id='wd-'+key,name=name,en=entry['english'] or (name if r['itemLabel'].get('xml:lang')=='en' else ''),location=country,category='nature' if subtype in ['nature','park'] else 'culture',subtype=subtype,tag=tag,image=image or '/images/poi-'+subtype+'.svg',lat=lat,lon=lon,country=country,countryCodes=country_codes,tagline=description or tag,description=description or name+'是'+country+'的'+tag+'类地点。',story='可以从空间布局、周边环境与建筑细节开始探索。百科资料会在打开详情后补充；具体开放安排请以当地官方信息为准。',facts=[['地点类型',tag],['所在国家 / 地区',country],['地理坐标',f'{lat:.5f}, {lon:.5f}']],source=key,sourceType='wikidata',sourceUrl='https://www.wikidata.org/wiki/'+key,sourceLabel='Wikidata 原始条目',designation=simplify(types),model=None,importance=max(180 if is_famous else 0,int(value(r,'links') or 0)),photoCredit='Wikimedia Commons · 作者与许可见原始文件页' if image else '原创分类插画 · 非实景',retrieved='2026-10-24'))
for p in places:
 old=baseline.get(p['id'])
 if old:
  p['importance']=max(old.get('importance',0),p.get('importance',0));p['en']=p['en'] or old.get('en','');p['countryCodes']=sorted(set(old.get('countryCodes',[])+p['countryCodes']))
 baseline[p['id']]=p
places=list(baseline.values());places.sort(key=lambda p:-p['importance'])
snapshot.write_text(json.dumps(places,ensure_ascii=False,separators=(',',':')))
stats=dict(records=len(places),countries=len(set(p['country'] for p in places)),china=sum('CN' in p['countryCodes'] for p in places),categories=dict(collections.Counter(p['subtype'] for p in places)),retrieved='2026-10-24',previousRecords=10933,addedSincePrevious=len(places)-10933,queries=[{'name':n,'rows':len(r),'limit':10000 if n=='china-local' else 6500} for n,r in extras],source='Wikidata',license='CC0',sourceUrl='https://www.wikidata.org/wiki/Wikidata:Licensing')
(out/'landmark-coverage.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps(stats,ensure_ascii=False))
