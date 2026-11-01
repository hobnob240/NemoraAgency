// NEMORA carousel maker: a set of 1080 x 1350 JPEG slides built for the feed.
// One idea per slide, big type you can read at thumb size, a slide counter so people swipe, real screenshots only.
//
//   node _social/tools/slides.mjs spec.json social/2026-11/name    (writes name-1.jpg, name-2.jpg, ...)
//
// spec.json: { "slides": [ { "kicker": "...", "big": "...", "text": "...", "phone": "assets/work/x-m.webp", "desk": "assets/work/x.webp", "caption": "real fact under the picture", "cta": "..." } ] }
// Every word and picture must be real (see the social playbook). "caption" says whose site a screenshot is.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'node:fs'; import path from 'node:path';

const [specPath, outBase] = process.argv.slice(2);
if (!specPath || !outBase) { console.error('usage: node slides.mjs spec.json out/base-name'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const file = p => 'file://' + path.resolve(ROOT, p);
const esc = v => String(v || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const css = `@font-face{font-family:S;src:url(${file('assets/fonts/serif.woff')})}@font-face{font-family:I;src:url(${file('assets/fonts/inter-500.woff')});font-weight:500}@font-face{font-family:I;src:url(${file('assets/fonts/inter-600.woff')});font-weight:600}
*{margin:0;box-sizing:border-box}
body{width:540px;height:675px;background:#0f1119;color:#ece6d8;font-family:I,system-ui,sans-serif;position:relative;overflow:hidden}
.top{position:absolute;top:28px;left:32px;right:32px;display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#9a958a}
.top b{color:#e8cf97;font-weight:600}
.brand{display:flex;align-items:center;gap:8px;font-family:S,serif;letter-spacing:.14em;color:#b8b2a4}.brand img{width:18px}
.body{position:absolute;inset:72px 32px 34px;display:flex;flex-direction:column;gap:16px}
.k{font-size:15px;font-weight:600;color:#e8cf97}
.big{font-family:S,Georgia,serif;font-weight:500;font-size:62px;line-height:1;letter-spacing:-.025em;color:#f5efe2;text-wrap:balance}
.big.xl{font-size:92px}
.body.center{justify-content:center;gap:22px}.body.center .txt{font-size:23px}.body.center .cta{margin-top:14px}
.txt{font-size:21px;line-height:1.35;color:#d4cec0;text-wrap:pretty}
.pic{flex:1;min-height:0;display:flex;gap:12px;align-items:flex-end}
.phone{height:100%;max-height:100%;aspect-ratio:1/2;border-radius:18px;overflow:hidden;border:2px solid rgba(233,225,205,.22);box-shadow:0 18px 40px -18px rgba(0,0,0,.8);flex:none}
.desk{flex:1;min-width:0;height:100%;border-radius:12px;overflow:hidden;border:1px solid rgba(233,225,205,.16)}
.phone img,.desk img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.cap{font-size:13px;color:#9a958a}
.cta{margin-top:auto;display:inline-flex;align-self:flex-start;padding:14px 20px;border-radius:10px;background:#c9a35a;color:#0f1119;font-weight:600;font-size:19px}
.swipe{position:absolute;right:32px;bottom:30px;font-size:15px;font-weight:600;color:#e8cf97}
.spacer{flex:1}`;
const n = spec.slides.length;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 675 }, deviceScaleFactor: 2 });
const outs = [];
for (const [i, s] of spec.slides.entries()) {
  const pic = (s.phone || s.desk) ? `<div class="pic">${s.desk ? `<div class="desk"><img src="${file(s.desk)}"></div>` : ''}${s.phone ? `<div class="phone"><img src="${file(s.phone)}"></div>` : ''}</div>${s.caption ? `<p class="cap">${esc(s.caption)}</p>` : ''}` : '';
  const html = `<!doctype html><meta charset="utf-8"><style>${css}</style>
<div class="top"><span class="brand"><img src="${file('assets/mark-96.png')}">NEMORA</span><span><b>${i + 1}</b> / ${n}</span></div>
<div class="body${(s.phone || s.desk) ? '' : ' center'}">${s.kicker ? `<p class="k">${esc(s.kicker)}</p>` : ''}<h1 class="big${s.xl ? ' xl' : ''}">${esc(s.big)}</h1>${s.text ? `<p class="txt">${esc(s.text)}</p>` : ''}${pic}${s.cta ? `<span class="cta">${esc(s.cta)}</span>` : ''}</div>
${i < n - 1 && !s.cta ? '<span class="swipe">Swipe</span>' : ''}`;
  const tmpf = path.join(ROOT, '.slide-' + Date.now() + '.html'); fs.writeFileSync(tmpf, html);
  await p.goto('file://' + tmpf, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); fs.unlinkSync(tmpf);
  const out = `${outBase}-${i + 1}.jpg`; await p.screenshot({ path: out, type: 'jpeg', quality: 90 }); outs.push(out);
}
await b.close();
console.log(JSON.stringify({ slides: outs }));
