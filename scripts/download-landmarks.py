"""Fetch public Wikidata exports used by prepare-landmarks.py (no API key).
Run from the project root, then prepare-landmarks.py and prepare-landmark-regions.mjs.
Snapshots are temporary inputs; published records retain individual source URLs.
"""
import urllib.request,urllib.parse,json,argparse
from pathlib import Path
queries={
'country-codes':'SELECT ?country ?code WHERE {?country wdt:P297 ?code}',
'landmarks':'''SELECT DISTINCT ?item ?itemLabel ?itemDescription ?coord ?image ?country ?countryLabel ?links WHERE { VALUES ?type {wd:Q33506 wd:Q570116 wd:Q9259 wd:Q4989906 wd:Q22698 wd:Q16970 wd:Q57821 wd:Q23413 wd:Q2977 wd:Q174782 wd:Q24354 wd:Q39614 wd:Q12518 wd:Q46169 wd:Q108325 wd:Q35509} ?item wdt:P31 ?type; wdt:P625 ?coord; wdt:P17 ?country; wikibase:sitelinks ?links. FILTER(?links>=10) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"} } LIMIT 15000''',
'china-landmarks':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE { ?item wdt:P17 wd:Q148; wdt:P625 ?coord; wikibase:sitelinks ?links; wdt:P31 ?type. FILTER(?links>=3) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"} }''',
'famous':Path('scripts/landmark-query.rq').read_text()
}
queries.update({
'china-local':'''SELECT ?item ?itemLabel ?itemDescription ?english ?coord ?image ?country ?links ?typeLabel WHERE {{SELECT DISTINCT ?item ?type ?coord ?country ?links WHERE {VALUES ?type {wd:Q33506 wd:Q207694 wd:Q22746 wd:Q5393308 wd:Q44613 wd:Q10300916 wd:Q10925991 wd:Q6838244 wd:Q22698 wd:Q43501 wd:Q167346 wd:Q23413 wd:Q16560 wd:Q44539 wd:Q839954 wd:Q570116 wd:Q34038 wd:Q35509} ?item wdt:P17 wd:Q148; wdt:P31 ?type; wdt:P625 ?coord; wikibase:sitelinks ?links. BIND(wd:Q148 AS ?country) FILTER(?links>=1 && ?links<3)} LIMIT 10000} OPTIONAL {?item wdt:P18 ?image} OPTIONAL {?item rdfs:label ?english FILTER(LANG(?english)="en")} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}}''',
'global-museums':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?country ?links ?typeLabel WHERE {VALUES ?type {wd:Q33506 wd:Q207694} ?item wdt:P31 ?type; wdt:P625 ?coord; wdt:P17 ?country; wikibase:sitelinks ?links. FILTER(?links>=3 && ?links<10) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 6500''',
'global-places':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?country ?links ?typeLabel WHERE {VALUES ?type {wd:Q22746 wd:Q5393308 wd:Q44613 wd:Q43501 wd:Q167346 wd:Q16560 wd:Q44539 wd:Q839954 wd:Q34038 wd:Q35509 wd:Q483453} ?item wdt:P31 ?type; wdt:P625 ?coord; wdt:P17 ?country; wikibase:sitelinks ?links. FILTER(?links>=3) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 6500'''
})
queries.update({
'china-zero':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE {?item wdt:P17 wd:Q148; wdt:P625 ?coord; wikibase:sitelinks ?links; wdt:P31 ?type. FILTER(?links=0) OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 12000''',
'china-heritage-gaps':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE {BIND(wd:Q10300916 AS ?type) ?item wdt:P31 ?type; wdt:P625 ?coord. FILTER NOT EXISTS {?item wdt:P17 wd:Q148} OPTIONAL {?item wikibase:sitelinks ?links} OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 4000''',
'china-nature-local':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE {VALUES ?type {wd:Q8502 wd:Q23397 wd:Q34038 wd:Q35509 wd:Q22698 wd:Q22746 wd:Q167346 wd:Q43501} ?item wdt:P31 ?type; wdt:P17 wd:Q148; wdt:P625 ?coord. OPTIONAL {?item wikibase:sitelinks ?links} OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 6000''',
'china-scenic':'''SELECT ?item ?itemLabel ?itemDescription ?coord ?image ?links ?typeLabel WHERE {VALUES ?type {wd:Q10925991 wd:Q6838244} ?item wdt:P31 ?type; wdt:P625 ?coord. OPTIONAL {?item wikibase:sitelinks ?links} OPTIONAL {?item wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "zh,en"}} LIMIT 3000'''
})
parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='+',choices=list(queries));args=parser.parse_args()
for name,query in queries.items():
 if args.only and name not in args.only:continue
 url='https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':query,'format':'json'})
 request=urllib.request.Request(url,headers={'User-Agent':'MobiusCulturalAtlas/1.1 (educational travel atlas)'})
 with urllib.request.urlopen(request,timeout=180) as response:data=json.load(response)
 dest=Path('/private/tmp/mobius-'+name+'.json');dest.write_text(json.dumps(data,ensure_ascii=False));print(name,len(data['results']['bindings']))
