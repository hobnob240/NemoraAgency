// NEMORA reel maker: turns a short scene list into an honest 9:16 MP4 for Instagram Reels and Facebook.
// Every frame is real: NEMORA's own type and words, or a real website scrolled in a phone-sized browser,
// or a real screenshot. No AI footage, no stock people, no fake reviews.
//
//   node _social/tools/reel.mjs spec.json out.mp4
//
// spec.json:
// { "scenes": [
//     { "type": "title", "kicker": "New website", "text": "Spitfire Comedy", "sub": "Stoke-on-Trent", "seconds": 2.5 },
//     { "type": "scroll", "url": "http://localhost:8800/index.html", "seconds": 7, "label": "spitfirecomedy.co.uk" },
//     { "type": "image", "src": "assets/work/spitfire-comedy-m.webp", "caption": "Next show up front, tickets one tap away", "seconds": 3 },
//     { "type": "end", "text": "Websites from £400", "sub": "nemora.uk", "seconds": 2.5 }
// ] }
// Paths in "src" are relative to the repo root. "scroll" needs a URL the session can open (serve a site
// from its GitHub source with `python3 -m http.server`, or a live URL if the domain is allowed).
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { execFileSync } from 'node:child_process';
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';

const [specPath, outPath] = process.argv.slice(2);
if (!specPath || !outPath) { console.error('usage: node reel.mjs spec.json out.mp4'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'reel-'));
const W = 432, H = 768, DPR = 2.5;            // 1080 x 1920 output
const fontUrl = f => 'file://' + path.join(ROOT, 'assets/fonts', f);
const esc = s => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const css = `@font-face{font-family:S;src:url(${fontUrl('serif.woff')})}@font-face{font-family:I;src:url(${fontUrl('inter-500.woff')});font-weight:500}
*{margin:0;box-sizing:border-box}html,body{width:${W}px;height:${H}px;overflow:hidden;background:#0f1119;color:#ece6d8;font-family:I,system-ui,sans-serif}
.wrap{position:absolute;inset:0;padding:56px 32px;display:flex;flex-direction:column;justify-content:center;gap:14px}
.k{font-size:15px;color:#e8cf97;opacity:0;animation:in .6s .1s forwards}
.t{font-family:S,Georgia,serif;font-size:44px;line-height:1.02;letter-spacing:-.02em;color:#f5efe2;opacity:0;animation:in .7s .25s forwards}
.s{font-size:17px;color:#b8b2a4;opacity:0;animation:in .6s .5s forwards}
.mark{position:absolute;left:32px;bottom:44px;display:flex;align-items:center;gap:10px;font-family:S,serif;font-size:15px;color:#b8b2a4;letter-spacing:.14em}
.mark img{width:22px}
.cap{position:absolute;left:20px;right:20px;bottom:40px;background:rgba(15,17,25,.88);border:1px solid rgba(233,225,205,.16);border-radius:12px;padding:14px 16px;font-size:16px;line-height:1.35;opacity:0;animation:in .5s .3s forwards}
.shot{position:absolute;inset:0;display:grid;place-items:center;padding:28px 28px 120px}
.shot img{max-width:100%;max-height:100%;border-radius:18px;border:1px solid rgba(233,225,205,.16);box-shadow:0 30px 60px rgba(0,0,0,.6);transform:scale(.98);animation:z 4s ease-out forwards}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}@keyframes z{to{transform:scale(1.02)}}`;
const mark = `<div class="mark"><img src="${'file://' + path.join(ROOT, 'assets/mark-96.png')}">NEMORA</div>`;
const page = body => `<!doctype html><meta charset="utf-8"><style>${css}</style>${body}`;   // written to a file so local fonts and images load

const browser = await chromium.launch();
const parts = [];
const FPS = 30;
for (const [i, sc] of spec.scenes.entries()) {
  const secs = Math.max(1, Math.min(15, Number(sc.seconds) || 3)), frames = Math.round(secs * FPS);
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: DPR, isMobile: sc.type === 'scroll', hasTouch: sc.type === 'scroll' });
  const p = await ctx.newPage();
  const dir = path.join(tmp, 's' + i); fs.mkdirSync(dir);
  const shoot = n => p.screenshot({ path: path.join(dir, String(n).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  if (sc.type === 'scroll') {
    // a real website in a phone-sized browser, scrolled smoothly; captured frame by frame so it's crisp at 1080 x 1920
    await p.goto(sc.url, { waitUntil: 'networkidle', timeout: 30000 });
    await p.addStyleTag({ content: '::-webkit-scrollbar{display:none} *{scroll-behavior:auto!important}' });
    await p.waitForTimeout(800);
    const max = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    const dist = Math.min(max, Number(sc.distance) || max), hold = Math.round(FPS * .5);
    for (let n = 0; n < frames; n++) {
      const t = Math.min(1, Math.max(0, (n - hold) / (frames - 2 * hold))), e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      await p.evaluate(y => scrollTo(0, y), Math.round(dist * e)); await shoot(n);
    }
  } else {
    let body = '';
    if (sc.type === 'title' || sc.type === 'end') body = `<div class="wrap">${sc.kicker ? `<p class="k">${esc(sc.kicker)}</p>` : ''}<h1 class="t">${esc(sc.text)}</h1>${sc.sub ? `<p class="s">${esc(sc.sub)}</p>` : ''}</div>${mark}`;
    else if (sc.type === 'image') body = `<div class="shot"><img src="${'file://' + path.resolve(ROOT, sc.src)}"></div>${sc.caption ? `<p class="cap">${esc(sc.caption)}</p>` : ''}`;
    else throw new Error('Unknown scene type: ' + sc.type);
    const f = path.join(tmp, `scene${i}.html`); fs.writeFileSync(f, page(body));
    await p.goto('file://' + f, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
    // step the CSS animations by hand so timing is exact
    for (let n = 0; n < frames; n++) { await p.evaluate(ms => document.getAnimations().forEach(a => { a.pause(); a.currentTime = ms; }), n * 1000 / FPS); await shoot(n); }
  }
  await ctx.close();
  const clip = path.join(tmp, `c${i}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%05d.jpg'), '-vf', 'scale=1080:1920,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', clip]);
  parts.push(clip);
}
await browser.close();
const list = path.join(tmp, 'list.txt');
fs.writeFileSync(list, parts.map(f => `file '${f}'`).join('\n'));
// add a silent stereo track: Instagram and Facebook expect an audio stream
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', outPath]);
console.log(JSON.stringify({ out: outPath, seconds: Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', outPath]).toString().trim()), bytes: fs.statSync(outPath).size }));
