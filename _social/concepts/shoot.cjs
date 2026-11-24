// Concept screenshots: a demo with every real detail swapped for an obvious stand-in, reviews removed, "Concept design" badge.
const { chromium } = require('playwright');
const [,, slug, mapJson, out] = process.argv;
const map = JSON.parse(mapJson);
(async () => {
  const b = await chromium.launch();
  const prep = async (p, mobile) => {
    await p.goto(`http://localhost:8799/${slug}/`, { waitUntil: 'networkidle' });
    await p.evaluate(({ map, mobile }) => {
      // remove anything quoting a real customer
      document.querySelectorAll('section, blockquote, figure, li, article').forEach(el => {
        if (/[“”]/.test(el.textContent) && !el.querySelector('h1')) {
          const sec = el.closest('section') || el; if (!sec.querySelector('h1')) sec.remove(); else el.remove();
        }
      });
      for (const sel of (map.__remove || [])) document.querySelectorAll(sel).forEach(e => e.remove());
      const pairs = Object.entries(map).filter(([k]) => k !== '__remove').sort((a, b) => b[0].length - a[0].length);
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) { let t = n.nodeValue; for (const [k, v] of pairs) t = t.replace(new RegExp(k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![a-z])', 'g'), v); n.nodeValue = t; }
      document.querySelectorAll('a[href^="tel:"],a[href^="mailto:"]').forEach(a => a.setAttribute('href', '#'));
      const tag = document.createElement('div');
      tag.textContent = 'Concept design by NEMORA';
      tag.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:9999;font:600 13px/1 system-ui,sans-serif;background:#111;color:#fff;padding:8px 12px;border-radius:6px;opacity:.92';
      document.body.appendChild(tag);
          if (mobile) { tag.remove(); document.querySelectorAll('body *').forEach(e => { const pos = getComputedStyle(e).position; if (pos === 'fixed') e.style.display = 'none'; if (pos === 'sticky') e.style.position = 'relative'; }); }
    }, { map, mobile });
    await p.waitForTimeout(400);
  };
  const d = await b.newPage({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
  await prep(d); await d.screenshot({ path: `${out}/${slug}-desk.png` });
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  await prep(m, true);
  const h = await m.evaluate(() => Math.min(document.body.scrollHeight, 844 * 5));
  await m.screenshot({ path: `${out}/${slug}-m.png`, clip: { x: 0, y: 0, width: 390, height: h }, fullPage: true });
  const left = await m.evaluate(() => (document.body.innerText.match(/MJ|Matt|Stu\b|S\.T\.|Right Removals|07572|07538|07904|Uttoxeter|Gnosall|“/g) || []).join(','));
  console.log(slug, 'leftover:', left || 'none');
  await b.close();
})();
