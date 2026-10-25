import json,re,html,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
source=pathlib.Path('/private/tmp/mobius-unesco-selected.json')
rows=json.loads(source.read_text())
index=json.loads((ROOT/'public/data/country-index.json').read_text());countries={r['alpha2']:r for r in index}
clean=lambda s:re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',s or ''))).strip()
def listish(v):
    if not v:return []
    if isinstance(v,list):return v
    try:return json.loads(v)
    except:return [v]
aliases={'Cultural Landscape of Honghe Hani Rice Terraces':'红河哈尼梯田文化景观','Kulangsu, a Historic International Settlement':'鼓浪屿：历史国际社区','Qinghai Hoh Xil':'青海可可西里',"Silk Roads: the Routes Network of Chang'an-Tianshan Corridor":'丝绸之路：长安—天山廊道的路网','The Grand Canal':'大运河','Xinjiang Tianshan':'新疆天山','Fujisan, sacred place and source of artistic inspiration':'富士山：信仰的对象与艺术的源泉','Ogasawara Islands':'小笠原群岛','Sacred Island of Okinoshima and Associated Sites in the Munakata Region':'神宿之岛冲之岛及宗像相关遗产群','Tomioka Silk Mill and Related Sites':'富冈制丝厂和相关遗址','The Architectural Work of Le Corbusier, an Outstanding Contribution to the Modern Movement':'勒·柯布西耶的建筑作品：对现代主义运动的杰出贡献'}
places=[];missing=[]
for r in rows:
    c=r.get('geo_point_2d');components=listish(r.get('components_list'));points=[[p['longitude'],p['latitude']] for p in components if p.get('longitude') is not None and p.get('latitude') is not None]
    if not c or not (-90<=c.get('lat',100)<=90) or not(-180<=c.get('lon',200)<=180):missing.append(r['id_no']);c={'lat':None,'lon':None}
    codes=listish(r['iso_codes']);names=[countries.get(code,{}).get('name',code) for code in codes];category='nature' if r['category']=='Natural' else 'mixed' if r['category']=='Mixed' else 'culture'
    desc=clean(r.get('short_description_zh')) or clean(r.get('short_description_en'))
    places.append({'id':'unesco-'+r['id_no'],'name':aliases.get(clean(r['name_en'])) or clean(r['name_zh']) or clean(r['name_en']),'en':clean(r['name_en']),'location':' / '.join(names) or 'UNESCO 特殊列名区域','country':names[0] if names else '', 'countryCodes':codes,'category':category,'tag':{'nature':'世界自然遗产','mixed':'世界双重遗产','culture':'世界文化遗产'}[category],'image':r.get('main_image_url') or '/images/heritage-placeholder.svg','lat':c['lat'],'lon':c['lon'],'components':points or ([[c['lon'],c['lat']]] if c['lon'] is not None else []),'tagline':clean(r['name_en']),'description':desc,'story':'这是一处由多个组成部分共同构成的系列遗产；地图将优先显示位于当前行政区域内的组成部分。' if len(points)>1 else '沿着地图走近遗产地，了解它与所在地的山水、建筑和文化之间的关系。更多保护信息、价值说明与组成部分，请阅读 UNESCO 原始档案。','facts':[['遗产类型',{'nature':'自然遗产','mixed':'文化与自然遗产','culture':'文化遗产'}[category]],['列入名录',str(r['date_inscribed'])+' 年'],['入选标准',r.get('criteria_txt') or '见原始档案']],'source':r['id_no'],'model':None,'photoCredit':' · '.join(filter(None,[r.get('main_image_author'),r.get('main_image_copyright')])),'descriptionLanguage':'zh' if clean(r.get('short_description_zh')) else 'en','region':r['region'],'attribution':'UNESCO World Heritage Centre · CC BY-SA IGO 3.0（文字）；影像版权归署名者。','retrieved':'2026-10-23'})
places.sort(key=lambda p:(p['country'],p['name']))
(ROOT/'public/data/heritage.json').write_text(json.dumps(places,ensure_ascii=False,separators=(',',':')))
meta={'retrieved':'2026-10-23','source':'UNESCO DataHub whc001','url':'https://data.unesco.org/explore/dataset/whc001/','records':len(rows),'mapped':len(places)-len(missing),'missingCoordinates':missing,'countries':len(set(c for p in places for c in p['countryCodes'])),'categories':dict(collections.Counter(p['category'] for p in places)),'coordinatesNote':'系列与跨国遗产优先使用各组成部分坐标；国家级统计按所有缔约国计数。'}
(ROOT/'public/data/heritage-coverage.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')))
print(meta)
