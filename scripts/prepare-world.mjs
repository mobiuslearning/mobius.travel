import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import iso from 'i18n-iso-countries';
import zh from 'i18n-iso-countries/langs/zh.json' with { type: 'json' };
import en from 'i18n-iso-countries/langs/en.json' with { type: 'json' };
iso.registerLocale(zh);iso.registerLocale(en);
const root=path.resolve(import.meta.dirname,'..');const output=path.join(root,'public/data');const raw='/private/tmp/mobius-geodata';fs.mkdirSync(raw,{recursive:true});
const all=JSON.parse(fs.readFileSync('/private/tmp/mobius-boundaries-catalog.json'));
const candidates=all.map(x=>({iso:x.boundaryISO,level:Number(x.boundaryType.slice(3)),label:x.boundaryCanonical,year:x.boundaryYearRepresented,units:Number(x.admUnitCount),license:x.boundaryLicense,source:x.boundarySource,url:x.simplifiedGeometryGeoJSON.replace('https://github.com/wmgeolab/geoBoundaries/raw/','https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/')}));
const grouped=new Map();for(const c of candidates){const key=c.iso+'-'+c.level;const old=grouped.get(key);const year=v=>Math.max(...(String(v).match(/(?:19|20)\d{2}/g)||[0]).map(Number));if(!old||year(c.year)>year(old.year)||year(c.year)===year(old.year)&&c.units>old.units)grouped.set(key,c)}const catalog=[...grouped.values()];
fs.writeFileSync(path.join(output,'boundary-catalog.json'),JSON.stringify(catalog));
const countries=Object.entries(iso.getAlpha3Codes()).map(([code,alpha2])=>({iso:code,alpha2,name:iso.getName(code,'zh')||code,en:iso.getName(code,'en')||code,numeric:iso.alpha3ToNumeric(code),levels:catalog.filter(x=>x.iso===code&&x.level>0).map(x=>x.level)}));
for(const c of catalog)if(!countries.some(x=>x.iso===c.iso)){const raw=all.find(x=>x.boundaryISO===c.iso);countries.push({iso:c.iso,alpha2:c.iso==='XKX'?'XK':c.iso,name:c.iso==='XKX'?'科索沃':raw.boundaryName,en:raw.boundaryName,numeric:'',levels:catalog.filter(x=>x.iso===c.iso&&x.level>0).map(x=>x.level)})}
fs.writeFileSync(path.join(output,'country-index.json'),JSON.stringify(countries));
let world=JSON.parse(fs.readFileSync(path.join(output,'countries.json')));world.features.forEach(f=>{const c=countries.find(c=>c.numeric===f.id||c.en===f.properties.name);if(c)Object.assign(f.properties,{iso:c.iso,alpha2:c.alpha2,name_zh:c.name})});fs.writeFileSync(path.join(output,'countries.json'),JSON.stringify(world));
const selection={TWN:[1,2],JPN:[1,2],ITA:[2,3,4],USA:[1,2],FRA:[1,2,3],GBR:[1,2,3],IND:[1,2,3],KHM:[1,2,3],JOR:[1,2,3],EGY:[1,2],GRC:[1,2,3],ESP:[1,2,3],PER:[1,2,3],MEX:[1,2],AUS:[1,2],IDN:[1,2,3],THA:[1,2,3],TUR:[1,2]};
const jobs=catalog.filter(c=>selection[c.iso]?.includes(c.level));let idx=0,success=0,failed=[];
const round=v=>Array.isArray(v)?v.map(round):typeof v==='number'?Math.round(v*1e5)/1e5:v;
async function download(c){const dest=path.join(output,'admin',`${c.iso}-${c.level}.json`);if(fs.existsSync(dest)){success++;return}const temp=path.join(raw,`${c.iso}-${c.level}.json`);if(!fs.existsSync(temp)){await new Promise((resolve,reject)=>{const p=spawn('curl',['-sSL','--fail','--retry','2','--max-time','100',c.url,'-o',temp]);let err='';p.stderr.on('data',d=>err+=d);p.on('exit',code=>code===0?resolve():reject(new Error(err)))})}let data=JSON.parse(fs.readFileSync(temp));const features=data.features.map(f=>({type:'Feature',properties:{name:f.properties.shapeName,key:f.properties.shapeID,iso:c.iso,level:c.level,shapeISO:f.properties.shapeISO},geometry:{type:f.geometry.type,coordinates:round(f.geometry.coordinates)}}));fs.writeFileSync(dest,JSON.stringify({type:'FeatureCollection',features}));success++;console.log(`Cached ${c.iso} ADM${c.level}: ${features.length} regions`)}
await Promise.all(Array.from({length:4},async()=>{while(idx<jobs.length){const c=jobs[idx++];try{await download(c)}catch(e){failed.push({iso:c.iso,level:c.level,error:String(e).slice(0,180)});console.log('Download deferred:',c.iso,c.level)}}}));
const coverage={retrieved:'2026-10-23',countries:new Set(catalog.filter(c=>c.level>0).map(c=>c.iso)).size,layers:catalog.filter(c=>c.level>0).length,localLayers:success,localCountries:Object.keys(selection).filter(iso=>fs.existsSync(path.join(output,'admin',`${iso}-${selection[iso][0]}.json`))),failed};
fs.writeFileSync(path.join(output,'world-coverage.json'),JSON.stringify(coverage));console.log(JSON.stringify(coverage));

catalog.forEach(c=>c.local=fs.existsSync(path.join(output,'admin',`${c.iso}-${c.level}.json`)));fs.writeFileSync(path.join(output,'boundary-catalog.json'),JSON.stringify(catalog));
