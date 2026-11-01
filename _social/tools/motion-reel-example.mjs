// Example of a motion-craft reel (see _social/video-toolkit/skills/remotion/motion-craft.md): Spitfire Comedy v2, Nov 2026. Copy and adapt for new videos.
// usage: node spitfire-v2.mjs <repoRoot> <out.mp4> [stillsAt=comma,separated,seconds]
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { execFileSync } from 'node:child_process';
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';

const [ROOT, OUT, STILLS] = process.argv.slice(2);
const FPS = 30, W = 1080, H = 1920;
const u = p => 'file://' + path.join(ROOT, p);

const html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:S;src:url(${u('assets/fonts/serif.woff')})}
@font-face{font-family:I;src:url(${u('assets/fonts/inter-500.woff')});font-weight:500}
@font-face{font-family:I;src:url(${u('assets/fonts/inter-600.woff')});font-weight:600}
*{margin:0;box-sizing:border-box}html,body{width:${W}px;height:${H}px;overflow:hidden}
body{background:#0f1119;color:#ece6d8;font-family:I,sans-serif;position:relative}
.abs{position:absolute}.w{display:inline-block;white-space:pre}
#kick{left:80px;top:700px;font-size:38px;font-weight:600}
#hook{left:80px;right:80px;top:770px;font-family:S,serif;font-size:104px;line-height:1.02;letter-spacing:-.02em;color:#f5efe2}
#desk{left:40px;top:560px;width:1000px;height:625px;border-radius:28px;overflow:hidden;border:2px solid rgba(233,225,205,.18);box-shadow:0 40px 90px rgba(0,0,0,.55)}
#desk img{width:1000px;height:625px;display:block;transform-origin:930px 625px}
#phone{left:190px;top:130px;width:700px;height:1400px;border-radius:56px;overflow:hidden;border:3px solid rgba(233,225,205,.22);box-shadow:0 50px 100px rgba(0,0,0,.6)}
#phone img{width:700px;height:1400px;display:block}
.cap{left:80px;right:80px;font-size:52px;line-height:1.25;color:#f5efe2}
#cap1,#cap2{top:1270px}#cap3{top:1610px;font-size:48px}
.gold{color:#e8cf97}
#flood{inset:0;background:#e8cf97;opacity:0;z-index:0}
#phone{z-index:2}#list,#end,#mark{z-index:3}
#list{left:80px;right:80px;top:560px;color:#0f1119}
#list .k{font-size:38px;font-weight:600;margin-bottom:44px;color:#5b4a26}
#list .it{font-family:S,serif;font-size:72px;line-height:1.08;letter-spacing:-.015em;margin-bottom:56px;padding-left:44px;position:relative}
#list .it::before{content:"";position:absolute;left:0;top:.55em;width:24px;height:3px;background:#0f1119}
#end{left:80px;right:80px;top:780px}
#end h1{font-family:S,serif;font-size:128px;line-height:1;letter-spacing:-.02em;color:#f5efe2}
#end p{font-size:48px;color:#e8cf97;margin-top:36px}
#mark{left:80px;bottom:110px;display:flex;align-items:center;gap:22px;font-family:S,serif;font-size:36px;letter-spacing:.16em;color:#b8b2a4}
#mark img{width:52px}
</style>
<p id="kick" class="abs">Recent work · Stoke-on-Trent</p>
<h1 id="hook" class="abs"></h1>
<div id="desk" class="abs"><img src="${u('assets/work/spitfire-comedy.webp')}"></div>
<p id="cap1" class="abs cap"></p><p id="cap2" class="abs cap"></p>
<div id="phone" class="abs"><img src="${u('assets/work/spitfire-comedy-m.webp')}"></div>
<p id="cap3" class="abs cap"></p>
<div id="flood" class="abs"></div>
<div id="list" class="abs"><p class="k">Also built in</p>
<p class="it">Pages for the acts, open mic nights and venue bookings</p>
<p class="it">A password-protected admin to update shows and photos</p>
<p class="it">Search fixes so Google indexes the site properly</p></div>
<div id="end" class="abs"><h1>Websites from £400</h1><p>nemora.uk</p></div>
<div id="mark" class="abs"><img src="${u('assets/mark-96.png')}">NEMORA</div>
<script>
const words = (el, s, accent) => { el.innerHTML = s.split(' ').map(w => '<span class="w' + (accent && accent.includes(w) ? ' gold' : '') + '">' + w + ' </span>').join(''); return [...el.children]; };
const hook = words(document.getElementById('hook'), 'A website for a comedy club in Stoke', ['comedy']);
const c1 = words(document.getElementById('cap1'), "Themed around the club's Spitfire plane logo", ['Spitfire']);
const c2 = words(document.getElementById('cap2'), 'The next show sits up front on a "boarding pass"', ['"boarding', 'pass"']);
const c3 = words(document.getElementById('cap3'), 'Built for phones first: shows and venue bookings one tap away', ['phones']);
const items = [...document.querySelectorAll('#list .it')];
const $ = id => document.getElementById(id);
const cl = x => Math.max(0, Math.min(1, x));
const outExp = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const inOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const inPoly = x => Math.pow(x, 4);
const p = (t, a, b) => cl((t - a) / (b - a));
const mix = (a, b, k) => a + (b - a) * k;
// word blur-in: 4 frames each, 2 frames apart; blur-out together over 6 frames
function wordsIn(ws, t, start, end) {
  ws.forEach((w, i) => { const k = outExp(p(t, start + i * 2 / 30, start + i * 2 / 30 + 5 / 30)); const o = end == null ? 1 : 1 - p(t, end, end + 6 / 30);
    w.style.opacity = k * o; w.style.filter = 'blur(' + ((1 - k) * 6 + (1 - o) * 8) + 'px)'; });
}
function hex(a, b, k) { const A = a.match(/\\w\\w/g).map(h => parseInt(h, 16)), B = b.match(/\\w\\w/g).map(h => parseInt(h, 16)); return 'rgb(' + A.map((v, i) => Math.round(mix(v, B[i], k))).join(',') + ')'; }
window.render = t => {
  // 1. hook 0.2-3.1
  const kIn = p(t, .15, .55); $('kick').style.color = hex('3a3d48', 'e8cf97', kIn); $('kick').style.opacity = cl(kIn * 3) * (1 - p(t, 2.9, 3.1));
  wordsIn(hook, t, .35, 2.9);
  // 2. desktop rises from below 2.75-3.5 (arrival, ease-out), push-in 4.6-7.4, carry-across exit 8.7-9.3
  const dIn = outExp(p(t, 2.75, 3.45)), push = inOut(p(t, 4.6, 7.4)), dOut = inOut(p(t, 8.7, 9.3));
  const d = $('desk'); d.style.opacity = cl(dIn * 2) * (1 - dOut);
  d.style.transform = 'translateY(' + ((1 - dIn) * 900 - dOut * 260) + 'px) scale(' + mix(1, .6, dOut) + ')'; d.style.filter = 'blur(' + Math.sin(dOut * Math.PI) * 6 + 'px)';
  d.querySelector('img').style.transform = 'scale(' + mix(1, 2.2, push) + ')';
  wordsIn(c1, t, 3.3, 6.0); wordsIn(c2, t, 6.25, 8.65);
  // 3. phone lands 8.9-9.6, holds; exits down 13.6-14.0 (accelerate)
  const phIn = outExp(p(t, 8.9, 9.6)), phOut = inPoly(p(t, 13.55, 13.95));
  const ph = $('phone'); ph.style.opacity = cl(phIn * 2);
  ph.style.transform = 'translateY(' + ((1 - phIn) * 260 + phOut * 2000) + 'px) scale(' + mix(1.06, 1, phIn) + ')';
  wordsIn(c3, t, 9.35, 13.45);
  // 4. colour flood 13.5-13.9, list items 14.0, 14.9, 15.8 ... hold to 18.6, blur out
  $('flood').style.opacity = inOut(p(t, 13.5, 13.9)) * (1 - inOut(p(t, 18.75, 19.15)));
  const lo = 1 - p(t, 18.55, 18.75);
  $('list').querySelector('.k').style.opacity = outExp(p(t, 13.9, 14.2)) * lo;
  items.forEach((it, i) => { const s = 14.05 + i * 1.05, k = outExp(p(t, s, s + .25)); it.style.opacity = k * lo; it.style.filter = 'blur(' + ((1 - k) * 8 + (1 - lo) * 8) + 'px)'; it.style.transform = 'translateX(' + (1 - k) * 24 + 'px)'; });
  // 5. end card from 19.0, per-letter-ish blur on title, hold >= 3s
  const e = $('end'), eh = outExp(p(t, 19.0, 19.25)), ep = outExp(p(t, 19.45, 19.75));
  e.querySelector('h1').style.opacity = eh; e.querySelector('h1').style.filter = 'blur(' + (1 - eh) * 8 + 'px)';
  e.querySelector('p').style.opacity = ep; e.querySelector('p').style.color = hex('3a3d48', 'e8cf97', ep);
  // mark only at start and end, not docked throughout
  $('mark').style.opacity = Math.max(1 - p(t, 2.7, 3.0), outExp(p(t, 19.6, 19.9)));
};
</script>`;

const DUR = 22.5;
const scenes = [[0, 3.1], [3.1, 8.85], [8.85, 13.5], [13.5, 18.95], [18.95, DUR]];   // cut points sit inside transitions only where the move is fast
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sv2-'));
const hf = path.join(tmp, 'page.html'); fs.writeFileSync(hf, html);
const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H } });
await pg.goto('file://' + hf, { waitUntil: 'load' }); await pg.evaluate(() => document.fonts.ready);
if (STILLS) {
  for (const s of STILLS.split(',')) { await pg.evaluate(t => render(t), Number(s)); await pg.screenshot({ path: path.join(path.dirname(OUT), 'still-' + s + '.jpg'), type: 'jpeg', quality: 85 }); }
  await b.close(); process.exit(0);
}
const parts = [];
for (const [i, [a, z]] of scenes.entries()) {
  const dir = path.join(tmp, 's' + i); fs.mkdirSync(dir);
  const f0 = Math.round(a * FPS), f1 = Math.round(z * FPS);
  for (let f = f0; f < f1; f++) { await pg.evaluate(t => render(t), f / FPS); await pg.screenshot({ path: path.join(dir, String(f - f0).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 }); }
  const clip = path.join(tmp, `c${i}.tmp.mp4`), fin = path.join(tmp, `c${i}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%05d.jpg'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS), clip]);
  fs.renameSync(clip, fin); parts.push(fin); fs.rmSync(dir, { recursive: true });
}
await b.close();
const list = path.join(tmp, 'list.txt'); fs.writeFileSync(list, parts.map(f => `file '${f}'`).join('\n'));
const joined = path.join(tmp, 'joined.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', joined]);
const tmpOut = OUT.replace(/\.mp4$/, '.tmp.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', joined, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', '-map', '0:v', '-map', '1:a', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', tmpOut]);
fs.renameSync(tmpOut, OUT);
console.log('done', OUT);
