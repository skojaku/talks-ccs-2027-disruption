import puppeteer from '/opt/homebrew/lib/node_modules/@marp-team/marp-cli/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import fs from 'fs';
const b = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new'});
const p = await b.newPage();
await p.setViewport({width:1280,height:720});
await p.goto('http://localhost:8766/ccs-2027.html');
await new Promise(r=>setTimeout(r,1500));
const out=[];
const N = await p.evaluate(()=>document.querySelectorAll('section[id]').length);
for (let n=1;n<=N;n++){
  const rows = await p.evaluate((n)=>{
    const sec=document.getElementById(String(n));
    const sr=sec.getBoundingClientRect();
    // Marp shows all sections stacked in the svg; compute relative to section box, scaled to 1280 wide
    const k=1280/sr.width;
    const res=[];
    sec.querySelectorAll('[style*="view-transition-name"]').forEach(el=>{
      const m=el.getAttribute('style').match(/view-transition-name:\s*(\w+)/); if(!m) return;
      const r=el.getBoundingClientRect();
      const cls=el.className&&el.className.baseVal===undefined?el.className:'';
      const txt=(el.textContent||'').trim().replace(/\s+/g,' ').slice(0,40);
      const img=el.querySelector('img'); 
      res.push({name:m[1],tag:el.tagName.toLowerCase(),cls,txt,img:img?img.getAttribute('src'):'',
        x:(r.left-sr.left)*k,y:(r.top-sr.top)*k,w:r.width*k,h:r.height*k,abs:(getComputedStyle(el).position==='absolute')});
    });
    return {sr:[sr.left,sr.top,sr.width,sr.height],res};
  }, n);
  out.push(rows);
}
fs.writeFileSync('geo_raw.json',JSON.stringify(out));
console.log(N, out[8].sr, out[8].res.slice(0,3));
await b.close();
