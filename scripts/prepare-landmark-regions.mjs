import fs from 'node:fs/promises';
import {contains,bounds} from '../src/scripts/geometry.ts';
const dir='public/data/',places=JSON.parse(await fs.readFile(dir+'landmarks.json','utf8')),cache=new Map();
async function layer(code){if(cache.has(code))return cache.get(code);let data;try{data=JSON.parse(await fs.readFile(`${dir}admin/CN-${code}.json`,'utf8')).features.map(f=>({...f,bbox:bounds(f.geometry)}))}catch{data=[]}cache.set(code,data);return data}
const match=(features,p)=>features.find(f=>p.lon>=f.bbox[0]&&p.lon<=f.bbox[2]&&p.lat>=f.bbox[1]&&p.lat<=f.bbox[3]&&contains(f.geometry,p.lon,p.lat));
for(const p of places.filter(p=>p.countryCodes.includes('CN'))){let parent=100000,names=[],path=[100000];for(let depth=0;depth<3;depth++){const f=match(await layer(parent),p);if(!f||f.properties.adcode===parent)break;parent=f.properties.adcode;path.push(parent);names.push(f.properties.name);if(depth===1){p.cityCode=parent;p.city=names.at(-1)}if(f.properties.childrenNum===0)break}p.path=path;p.location=['中国',...names].join(' · ');p.facts[1]=['所在区域',p.location]}
await fs.writeFile(dir+'landmarks.json',JSON.stringify(places));const stats=JSON.parse(await fs.readFile(dir+'landmark-coverage.json'));stats.chinaCities=new Set(places.map(p=>p.cityCode).filter(Boolean)).size;await fs.writeFile(dir+'landmark-coverage.json',JSON.stringify(stats,null,2));console.log(stats);
