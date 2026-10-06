import {mkdirSync,copyFileSync,cpSync} from 'node:fs';
mkdirSync('dist/server',{recursive:true});copyFileSync('worker.mjs','dist/server/index.js');cpSync('drizzle','dist/drizzle',{recursive:true});
