// NEMORA photo maker: renders an on-brand 1080 x 1350 JPEG (Instagram's 4:5 portrait) from real words and real screenshots.
//
//   node _social/tools/card.mjs spec.json out.jpg
//
// spec.json, one of:
// { "layout": "statement", "kicker": "Pricing", "text": "Websites from £400, with the price published", "sub": "nemora.uk/services" }
// { "layout": "shot", "kicker": "Recent work", "text": "Spitfire Comedy", "sub": "Stoke-on-Trent", "src": "assets/work/spitfire-comedy.webp" }
// { "layout": "list", "kicker": "What's in a Business site", "items": ["Up to 5 pages", "Your own admin", "Enquiry inbox"], "sub": "£795 + £50 a month" }
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'node:fs'; import path from 'node:path';

const [specPath, outPath] = process.argv.slice(2);
if (!specPath || !outPath) { console.error('usage: node card.mjs spec.json out.jpg'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const s = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const f = n => 'file://' + path.join(ROOT, 'assets/fonts', n);
const esc = v => String(v || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const css = `@font-face{font-family:S;src:url(${f('serif.woff')})}@font-face{font-family:I;src:url(${f('inter-500.woff')});font-weight:500}
*{margin:0;box-sizing:border-box}body{width:540px;height:675px;background:#0f1119;color:#ece6d8;font-family:I,system-ui,sans-serif;position:relative;overflow:hidden}
.pad{position:absolute;inset:0;padding:44px 40px;display:flex;flex-direction:column;gap:14px}
.k{font-size:14px;color:#e8cf97}.t{font-family:S,Georgia,serif;font-size:40px;line-height:1.04;letter-spacing:-.02em;color:#f5efe2}
.s{font-size:15px;color:#b8b2a4}.foot{margin-top:auto;display:flex;align-items:center;gap:10px;font-family:S,serif;font-size:13px;letter-spacing:.14em;color:#b8b2a4;padding-top:16px;border-top:1px solid rgba(233,225,205,.12)}
.foot img{width:20px}.foot span{margin-left:auto;letter-spacing:0;font-family:I}
.shot{flex:1;min-height:0;border-radius:12px;overflow:hidden;border:1px solid rgba(233,225,205,.16)}.shot img{width:100%;height:100%;object-fit:cover;object-position:top}
li{font-size:22px!important}.mid{flex:1;display:flex;flex-direction:column;justify-content:center;gap:16px}ul{list-style:none;padding:0;display:grid;gap:12px;margin-top:8px}li{font-size:19px;padding-left:22px;position:relative}li::before{content:"";position:absolute;left:0;top:.62em;width:10px;height:1px;background:#e8cf97}`;
const foot = `<div class="foot"><img src="${'file://' + path.join(ROOT, 'assets/mark-96.png')}">NEMORA<span>${esc(s.sub || 'nemora.uk')}</span></div>`;
let body;
if (s.layout === 'shot') body = `<div class="pad"><p class="k">${esc(s.kicker)}</p><h1 class="t" style="font-size:34px">${esc(s.text)}</h1><div class="shot"><img src="${'file://' + path.resolve(ROOT, s.src)}"></div>${foot}</div>`;
else if (s.layout === 'list') body = `<div class="pad"><div class="mid"><p class="k">${esc(s.kicker)}</p>${s.text ? `<h1 class="t">${esc(s.text)}</h1>` : ''}<ul>${(s.items || []).map(i => `<li>${esc(i)}</li>`).join('')}</ul></div>${foot}</div>`;
else body = `<div class="pad" style="justify-content:center"><p class="k">${esc(s.kicker)}</p><h1 class="t" style="font-size:50px">${esc(s.text)}</h1>${foot.replace('class="foot"', 'class="foot" style="position:absolute;left:40px;right:40px;bottom:44px"')}</div>`;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 675 }, deviceScaleFactor: 2 });
const tmpf = path.join(path.dirname(path.resolve(outPath)), '.card-' + Date.now() + '.html'); fs.writeFileSync(tmpf, `<!doctype html><meta charset="utf-8"><style>${css}</style>${body}`);
await p.goto('file://' + tmpf, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); fs.unlinkSync(tmpf);
await p.screenshot({ path: outPath, type: 'jpeg', quality: 90 }); await b.close();
console.log(JSON.stringify({ out: outPath, bytes: fs.statSync(outPath).size }));
