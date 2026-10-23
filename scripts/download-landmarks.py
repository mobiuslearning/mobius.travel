"""Fetch public Wikidata exports used by prepare-landmarks.py (no API key).
Run from the project root, then prepare-landmarks.py and prepare-landmark-regions.mjs.
Snapshots are temporary inputs; published records retain individual source URLs.
"""
import urllib.request,urllib.parse,json
from pathlib import Path
queries={
'country-codes':'SELECT ?country ?code WHERE {?country wdt:P297 ?code}',
'landmarks':'''SELECT DISTINCT ?item ?itemLabel ?itemDescription ?coord ?image ?country ?countryLabel ?links WHERE { VALUES ?type {wd:Q33506 wd:Q570116 wd:Q9259 wd:Q4989906 wd:Q22698 wd:Q16970 wd:Q57821 wd:Q23413 wd:Q2977 wd:Q174782 wd:Q24354 wd:Q39614 wd:Q12518 wd:Q46169 wd:Q108325 wd:Q35509} ?item wdt:P31 ?type; wdt:P625 ?coord; wdt:P17 ?country; wikibase:sitelinks ?links. FILTER(?links>=10) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"} } LIMIT 15000''',
'china-landmarks':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE { ?item wdt:P17 wd:Q148; wdt:P625 ?coord; wikibase:sitelinks ?links; wdt:P31 ?type. FILTER(?links>=3) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"} }''',
'famous':Path('scripts/landmark-query.rq').read_text()
}
for name,query in queries.items():
 url='https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':query,'format':'json'})
 request=urllib.request.Request(url,headers={'User-Agent':'MobiusCulturalAtlas/1.1 (educational travel atlas)'})
 with urllib.request.urlopen(request,timeout=180) as response:data=json.load(response)
 dest=Path('/private/tmp/mobius-'+name+'.json');dest.write_text(json.dumps(data,ensure_ascii=False));print(name,len(data['results']['bindings']))
