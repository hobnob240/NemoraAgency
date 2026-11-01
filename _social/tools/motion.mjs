// NEMORA motion reel maker: 1080 x 1920, 30 fps, H.264 + silent AAC.
// Motion follows _social/video-toolkit/skills/remotion/motion-craft.md: words blur in 2 frames apart, arrivals on a
// long ease-out, camera moves ease both ways, exits accelerate, a landed title stays still, read time 0.5 s + 0.3 s a word,
// the last line holds 3 s, and the transitions vary (rise in, push-in, carry across, phone hand-off, colour flood, blur swap).
// Every frame is real: NEMORA's own type and words, or a real screenshot of a site we built. No AI footage or voices.
// "sound_seed" in the spec picks the music bed's key and tempo (defaults to one derived from the file name).
//
//   node _social/tools/motion.mjs spec.json out.mp4            render, with an original background music bed (sound.py)
//   node _social/tools/motion.mjs spec.json out.mp4 --silent   render with a silent track
//   node _social/tools/motion.mjs spec.json out.mp4 --stills   save a still at the busiest moment of each scene, then stop
//
// spec.json: { "scenes": [
//   { "type": "hook", "kicker": "Recent work · Wolverhampton", "text": "A new website for a family decorating business", "accent": ["decorating"] },
//   { "type": "desktop", "src": "assets/work/law-and-son.webp", "focus": [0.76, 0.54], "zoom": 1.9,
//     "captions": ["A confident first impression", "A quote form right at the top"], "accent": ["quote"] },
//   { "type": "phone", "src": "assets/work/law-and-son-m.webp", "scroll": false, "captions": ["Built for phones first"] },
//   { "type": "list", "kicker": "Also built in", "items": ["…", "…"] },
//   { "type": "end", "text": "Websites from £400", "sub": "nemora.uk" } ] }
// src paths are relative to the repo root (or absolute). "focus" is the point of the screenshot to push in on (0-1).
// A phone src may be a tall full-page phone screenshot (any width); with "scroll": true it scrolls through it.
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const { chromium } = createRequire(import.meta.url)('playwright');

const args = process.argv.slice(2), STILLS = args.includes('--stills');
const [specPath, OUT] = args.filter(a => !a.startsWith('--'));
if (!specPath || !OUT) { console.error('usage: node motion.mjs spec.json out.mp4 [--stills]'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const FPS = 30, W = 1080, H = 1920;
const file = p => 'file://' + (path.isAbsolute(p) ? p : path.join(ROOT, p));
const words = s => String(s).trim().split(/\s+/).length;
const read = s => 0.5 + 0.3 * words(s);
const esc = v => String(v || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const size = p => { const o = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p.replace('file://', '')]).toString().trim().split(','); return { w: +o[0], h: +o[1] }; };

// ---- timeline: each scene gets a length from its read time; neighbours overlap by 0.3 s for the transition ----
const OV = 0.3; let t = 0;
const scenes = spec.scenes.map((s, i) => {
  let d;
  if (s.type === 'hook') d = 0.4 + words(s.text) * 2 / 30 + read(s.text) + 0.3;
  else if (s.type === 'desktop' || s.type === 'phone') d = 0.8 + (s.captions || []).reduce((a, c) => a + read(c) + 0.35, 0) + (s.hold || 0.4);
  else if (s.type === 'list') d = 0.6 + (s.items || []).reduce((a, c) => a + Math.max(1.0, read(c) * 0.75), 0) + 1.4;
  else if (s.type === 'end') d = 3.2;
  else throw new Error('Unknown scene type ' + s.type);
  if (s.seconds) d = s.seconds;
  const sc = { ...s, i, start: i ? t - OV : 0, dur: d + (i ? OV : 0) };
  t = sc.start + sc.dur;
  if (s.src) { sc.url = file(s.src); sc.size = size(sc.url); }
  return sc;
});
const DUR = Math.round(t * FPS) / FPS;
if (DUR < 6 || DUR > 45) console.warn('warning: video is ' + DUR.toFixed(1) + ' s (playbook: 6 to 45 s)');

const wordSpans = (s, accent = []) => esc(s).split(' ').map(w => `<span class="w${accent.some(a => w.replace(/[^\p{L}\p{N}£]/gu, '').toLowerCase() === a.toLowerCase()) ? ' gold' : ''}">${w} </span>`).join('');
const sceneHtml = s => {
  if (s.type === 'hook') return `<section id="s${s.i}" class="sc hook"><p class="kick">${esc(s.kicker)}</p><h1 class="ww">${wordSpans(s.text, s.accent)}</h1></section>`;
  if (s.type === 'desktop') return `<section id="s${s.i}" class="sc"><div class="desk"><img src="${s.url}"></div>${(s.captions || []).map(c => `<p class="cap dcap ww">${wordSpans(c, s.accent)}</p>`).join('')}</section>`;
  if (s.type === 'phone') return `<section id="s${s.i}" class="sc"><div class="phone"><img src="${s.url}"></div>${(s.captions || []).map(c => `<p class="cap pcap ww">${wordSpans(c, s.accent)}</p>`).join('')}</section>`;
  if (s.type === 'list') return `<section id="s${s.i}" class="sc list"><div class="flood"></div><div class="lw"><p class="k">${esc(s.kicker)}</p>${(s.items || []).map(x => `<p class="it">${esc(x)}</p>`).join('')}</div></section>`;
  return `<section id="s${s.i}" class="sc end"><div class="ew"><h1${words(s.text) > 4 ? ' class="long"' : ''}>${esc(s.text)}</h1><p>${esc(s.sub || 'nemora.uk')}</p></div></section>`;
};
const html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:S;src:url(${file('assets/fonts/serif.woff')})}
@font-face{font-family:I;src:url(${file('assets/fonts/inter-500.woff')});font-weight:500}
@font-face{font-family:I;src:url(${file('assets/fonts/inter-600.woff')});font-weight:600}
*{margin:0;box-sizing:border-box}html,body{width:${W}px;height:${H}px;overflow:hidden}
body{background:#0f1119;color:#ece6d8;font-family:I,sans-serif;position:relative}
.sc{position:absolute;inset:0;opacity:0}.w{display:inline-block;white-space:pre}.gold{color:#e8cf97}
.hook .kick{position:absolute;left:80px;top:700px;font-size:38px;font-weight:600}
.hook h1{position:absolute;left:80px;right:80px;top:770px;font-family:S,serif;font-size:100px;line-height:1.04;letter-spacing:-.02em;color:#f5efe2}
.desk{position:absolute;left:40px;top:560px;width:1000px;height:625px;border-radius:28px;overflow:hidden;border:2px solid rgba(233,225,205,.18);box-shadow:0 40px 90px rgba(0,0,0,.55)}
.desk img{width:1000px;height:625px;display:block;transform-origin:0 0;object-fit:cover;object-position:top}
.phone{position:absolute;left:190px;top:130px;width:700px;height:1400px;border-radius:56px;overflow:hidden;border:3px solid rgba(233,225,205,.22);box-shadow:0 50px 100px rgba(0,0,0,.6);background:#fff}
.phone img{width:700px;display:block}
.cap{position:absolute;left:80px;right:80px;font-size:52px;line-height:1.25;color:#f5efe2}.dcap{top:1270px}.pcap{top:1600px;font-size:48px}
.flood{position:absolute;inset:0;background:#e8cf97}
.lw{position:absolute;left:80px;right:80px;top:520px;color:#0f1119}
.lw .k{font-size:38px;font-weight:600;margin-bottom:44px;color:#5b4a26}
.lw .it{font-family:S,serif;font-size:68px;line-height:1.08;letter-spacing:-.015em;margin-bottom:52px;padding-left:44px;position:relative}
.lw .it::before{content:"";position:absolute;left:0;top:.55em;width:24px;height:3px;background:#0f1119}
.end .ew{position:absolute;left:80px;right:80px;top:50%;transform:translateY(-55%)}
.end h1{font-family:S,serif;font-size:124px;line-height:1.02;letter-spacing:-.02em;color:#f5efe2}.end h1.long{font-size:100px}
.end p{font-size:48px;margin-top:40px}
#mark{position:absolute;left:80px;bottom:110px;display:flex;align-items:center;gap:22px;font-family:S,serif;font-size:36px;letter-spacing:.16em;color:#b8b2a4;z-index:50}
#mark img{width:52px}
</style>${scenes.map(sceneHtml).join('')}<div id="mark"><img src="${file('assets/mark-96.png')}">NEMORA</div>
<script>
const S = ${JSON.stringify(scenes.map(s => ({ type: s.type, start: s.start, dur: s.dur, captions: (s.captions || []).length, focus: s.focus, zoom: s.zoom, scroll: !!s.scroll, size: s.size, items: (s.items || []).length })))};
const cl = x => Math.max(0, Math.min(1, x)), p = (t, a, b) => cl((t - a) / (b - a));
const outExp = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const inOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const inPoly = x => x * x * x * x, mix = (a, b, k) => a + (b - a) * k;
const hex = (a, b, k) => { const A = a.match(/\\w\\w/g).map(h => parseInt(h, 16)), B = b.match(/\\w\\w/g).map(h => parseInt(h, 16)); return 'rgb(' + A.map((v, i) => Math.round(mix(v, B[i], k))).join(',') + ')'; };
// words blur in 4-5 frames each, 2 frames apart; the whole line blurs out over 6 frames
function wordsIn(el, t, a, z) { [...el.querySelectorAll('.w')].forEach((w, i) => { const k = outExp(p(t, a + i * 2 / 30, a + i * 2 / 30 + 5 / 30)), o = z == null ? 1 : 1 - p(t, z, z + 6 / 30); w.style.opacity = k * o; w.style.filter = 'blur(' + ((1 - k) * 6 + (1 - o) * 8) + 'px)'; }); }
const readT = el => 0.5 + 0.3 * el.querySelectorAll('.w').length;
window.render = T => {
  let markO = 0;
  S.forEach((s, i) => {
    const el = document.getElementById('s' + i), t = T - s.start, d = s.dur, first = i === 0, last = i === S.length - 1;
    if (t < -0.01 || t > d + 0.01) { el.style.opacity = 0; return; }
    el.style.opacity = 1;
    const enter = first ? 0 : 0.3, exitAt = last ? 1e9 : d - 0.3;
    if (s.type === 'hook') {
      const k = el.querySelector('.kick'), kin = p(t, .1, .5);
      k.style.color = hex('3a3d48', 'e8cf97', kin); k.style.opacity = cl(kin * 3) * (1 - p(t, exitAt, exitAt + .2));
      wordsIn(el.querySelector('h1'), t, .3, exitAt); markO = Math.max(markO, 1 - p(t, exitAt - .2, exitAt + .1));
    }
    if (s.type === 'desktop' || s.type === 'phone') {
      const box = el.querySelector(s.type === 'desktop' ? '.desk' : '.phone'), img = box.querySelector('img');
      const ain = outExp(p(t, enter - .1, enter + .6));
      const out = s.type === 'desktop' ? inOut(p(t, exitAt - .25, exitAt + .3)) : inPoly(p(t, exitAt - .1, exitAt + .3));
      box.style.opacity = cl(ain * 2) * (s.type === 'desktop' ? 1 - out : 1);
      if (s.type === 'desktop') { box.style.transform = 'translateY(' + ((1 - ain) * 900 - out * 260) + 'px) scale(' + mix(1, .6, out) + ')'; box.style.filter = 'blur(' + Math.sin(out * Math.PI) * 6 + 'px)'; }
      else box.style.transform = 'translateY(' + ((1 - ain) * 260 + out * 2000) + 'px) scale(' + mix(1.06, 1, ain) + ')';
      const caps = [...el.querySelectorAll('.cap')]; let c0 = enter + .55;
      caps.forEach((c, j) => { const r = readT(c) + .35, z = j === caps.length - 1 ? exitAt - .25 : c0 + r - .2; wordsIn(c, t, c0, z); c0 += r; });
      if (s.type === 'desktop' && s.focus) {
        // camera push-in on the focus point over the middle of the scene, eased both ways; never shows past the edge
        const Z = s.zoom || 1.8, k = inOut(p(t, enter + 1.2, Math.max(enter + 2.4, exitAt - .9)));
        const z = mix(1, Z, k), fw = 1000, fh = 625;
        let tx = fw / 2 - s.focus[0] * fw * Z, ty = fh / 2 - s.focus[1] * fh * Z;
        tx = Math.min(0, Math.max(fw - fw * Z, tx)); ty = Math.min(0, Math.max(fh - fh * Z, ty));
        img.style.transform = 'translate(' + tx * k + 'px,' + ty * k + 'px) scale(' + z + ')';
      }
      if (s.type === 'phone' && s.scroll) {
        const ih = 700 * s.size.h / s.size.w, k = inOut(p(t, enter + .9, exitAt - .4));
        img.style.transform = 'translateY(' + (-Math.max(0, ih - 1400) * k) + 'px)';
      }
    }
    if (s.type === 'list') {
      el.querySelector('.flood').style.opacity = inOut(p(t, 0, .4)) * (last ? 1 : 1 - inOut(p(t, d - .3, d)));
      const lo = last ? 1 : 1 - p(t, d - .45, d - .3);
      el.querySelector('.k').style.opacity = outExp(p(t, .4, .7)) * lo;
      let a = .55; [...el.querySelectorAll('.it')].forEach(it => { const k = outExp(p(t, a, a + .25)); it.style.opacity = k * lo; it.style.filter = 'blur(' + ((1 - k) * 8 + (1 - lo) * 8) + 'px)'; it.style.transform = 'translateX(' + (1 - k) * 24 + 'px)'; a += Math.max(1.0, readT(it) * 0.75); });
    }
    if (s.type === 'end') {
      const h1 = el.querySelector('h1'), pp = el.querySelector('p'), eh = outExp(p(t, enter, enter + .25)), ep = outExp(p(t, enter + .45, enter + .75));
      h1.style.opacity = eh; h1.style.filter = 'blur(' + (1 - eh) * 8 + 'px)'; pp.style.opacity = ep; pp.style.color = hex('3a3d48', 'e8cf97', ep);
      markO = Math.max(markO, outExp(p(t, enter + .6, enter + .9)));
    }
  });
  document.getElementById('mark').style.opacity = markO;
};
</script>`;

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-'));
const hf = path.join(tmp, 'page.html'); fs.writeFileSync(hf, html);
const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H } });
await pg.goto('file://' + hf, { waitUntil: 'load' }); await pg.evaluate(() => document.fonts.ready);
if (STILLS) {
  // the busiest moment of each scene: everything landed, just before it leaves
  for (const s of scenes) { const at = +(s.start + s.dur - (s.i === scenes.length - 1 ? 0.2 : 0.75)).toFixed(2); await pg.evaluate(x => render(x), at); const f = OUT.replace(/\.mp4$/, `.still-${s.i}-${at}s.jpg`); await pg.screenshot({ path: f, type: 'jpeg', quality: 85 }); console.log(f); }
  await b.close(); process.exit(0);
}
const parts = [];
for (const [i, s] of scenes.entries()) {
  const f0 = Math.round(s.start * FPS), f1 = i === scenes.length - 1 ? Math.round(DUR * FPS) : Math.round(scenes[i + 1].start * FPS);
  const dir = path.join(tmp, 's' + i); fs.mkdirSync(dir);
  for (let f = f0; f < f1; f++) { await pg.evaluate(x => render(x), f / FPS); await pg.screenshot({ path: path.join(dir, String(f - f0).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 }); }
  const part = path.join(tmp, `c${i}.tmp.mp4`), fin = path.join(tmp, `c${i}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%05d.jpg'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS), part]);
  fs.renameSync(part, fin); parts.push(fin); fs.rmSync(dir, { recursive: true });
}
await b.close();
const list = path.join(tmp, 'list.txt'); fs.writeFileSync(list, parts.map(f => `file '${f}'`).join('\n'));
const joined = path.join(tmp, 'joined.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', joined]);
const tmpOut = OUT.replace(/\.mp4$/, '.tmp.mp4');
// background sound: an original music bed made by sound.py (synthesised, no samples or copyrighted music), timed to
// the scene changes and levelled quietly (-20 LUFS) so it sits under the pictures. --silent keeps a silent track instead.
if (args.includes('--silent')) execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', joined, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', '-map', '0:v', '-map', '1:a', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', tmpOut]);
else {
  const wav = path.join(tmp, 'bed.wav'), seed = String(spec.sound_seed ?? [...path.basename(OUT)].reduce((a, c) => a + c.charCodeAt(0), 0));
  execFileSync('python3', [path.join(ROOT, '_social/tools/sound.py'), wav, '--seconds', String(DUR), '--cuts', scenes.slice(1).map(s => (s.start + OV / 2).toFixed(2)).join(','), '--seed', seed]);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', joined, '-i', wav, '-map', '0:v', '-map', '1:a', '-af', 'loudnorm=I=-20:TP=-2:LRA=7', '-ar', '44100', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', tmpOut]);
}
fs.renameSync(tmpOut, OUT); fs.rmSync(tmp, { recursive: true });
console.log(JSON.stringify({ out: OUT, seconds: DUR, bytes: fs.statSync(OUT).size }));
