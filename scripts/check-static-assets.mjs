import fs from 'node:fs/promises';
import path from 'node:path';
const limit=25*1024*1024;
async function inspect(dir){for(const file of await fs.readdir(dir,{withFileTypes:true})){const target=path.join(dir,file.name);if(file.isDirectory())await inspect(target);else if((await fs.stat(target)).size>limit)throw Error(`Static asset exceeds the 25 MiB hosting limit: ${target}`)}}
await inspect('dist');console.log('Static assets meet the 25 MiB file limit.');
