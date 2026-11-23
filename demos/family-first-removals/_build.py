# Builds the Family First Removals demo site (5 pages) from shared parts. Run: python3 _build.py
# Facts used come from Chloe's email and their Facebook banner only. No prices, reviews or accreditations
# until Chloe confirms them.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = '/tmp/claude-0/-home-claude/dd7eb376-80be-5892-b01d-74b4f1b18b1c/scratchpad/'
BASE_CSS = open(SCR + 'ffr_css.css').read() if os.path.exists(SCR + 'ffr_css.css') else None
ICONS = open(SCR + 'ffr_icons.html').read() if os.path.exists(SCR + 'ffr_icons.html') else None

TEL = '+447858798002'; TELS = '07858 798002'; EMAIL = 'familyfirstremovals25@gmail.com'
FB = 'https://www.facebook.com/profile.php?id=61595959954804'

EXTRA_CSS = r'''
/* ---- multi-page additions ---- */
.mnav { display: none; gap: 8px; overflow-x: auto; padding-bottom: 12px; scrollbar-width: none; }
.page-hero + .sec { padding-top: 32px; }
.nav a[aria-current="page"] { color: var(--red); }
.badge-txt strong { font-size: 1.05rem; }
.page-hero { background: linear-gradient(180deg, var(--sky) 0%, var(--paper) 100%); padding-block: 64px 56px; }
.page-hero h1 { font-weight: 900; font-stretch: 96%; font-size: clamp(2.4rem, 5.4vw, 4.4rem); line-height: .95; letter-spacing: -0.02em; text-transform: uppercase; color: var(--logo-ink); max-width: 16ch; }
.page-hero h1 .r { color: var(--red); }
.page-hero .sec-lead { margin-top: 18px; }
.page-hero .hero-actions { margin-top: 28px; }
.svc-link { margin-top: auto; font-weight: 700; color: var(--red); text-decoration: none; }
.svc-grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.detail { display: grid; grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); gap: 56px; padding-block: 56px; border-top: 1px solid var(--line); }
.detail:first-child { border-top: 0; padding-top: 0; }
.detail h2 { font-weight: 900; font-size: clamp(1.8rem, 3.4vw, 2.6rem); text-transform: uppercase; color: var(--logo-ink); letter-spacing: -0.01em; display: flex; align-items: center; gap: 16px; }
.detail h2 .ring { width: 52px; height: 52px; box-shadow: none; }
.detail h2 .ring svg { width: 24px; height: 24px; }
.detail p + p { margin-top: 14px; }
.detail .body { color: var(--ink-2); font-size: 1.08rem; }
.detail .ticks { margin-top: 22px; }
.also { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin-top: 36px; }
.timeline { list-style: none; margin: 48px 0 0; padding: 0; display: grid; gap: 0; counter-reset: s; max-width: 860px; }
.timeline li { counter-increment: s; display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 24px; padding-bottom: 40px; position: relative; }
.timeline li::before { content: counter(s); display: grid; place-items: center; width: 64px; height: 64px; border-radius: 50%; background: var(--navy); color: var(--on-navy); font-family: var(--display); font-weight: 900; font-size: 1.6rem; position: relative; z-index: 1; }
.timeline li::after { content: ""; position: absolute; left: 31px; top: 64px; bottom: 0; width: 2px; background: var(--line); }
.timeline li:last-child { padding-bottom: 0; }
.timeline li:last-child::after { display: none; }
.timeline li.key::before { background: var(--red); }
.timeline h3 { font-weight: 850; font-size: 1.5rem; text-transform: uppercase; color: var(--logo-ink); margin: 14px 0 8px; }
.timeline p { color: var(--ink-2); max-width: 36em; }
.timeline .tag { display: inline-block; margin-top: 10px; font-family: var(--script); font-weight: 700; font-size: 1.4rem; color: var(--red); line-height: 1.1; }
.steps.five { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; }
.steps.five li { padding: 22px; }
.steps.five h3 { font-size: 1.1rem; }
.steps.five p { font-size: .95rem; }
.steps.five li.key::before { background: var(--red); }
.faq { max-width: 860px; margin-top: 36px; border-top: 1px solid var(--line); }
.faq details { border-bottom: 1px solid var(--line); }
.faq summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 22px 0; font-weight: 700; font-size: 1.12rem; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; font-family: var(--display); font-weight: 900; font-size: 1.6rem; color: var(--red); line-height: 1; flex-shrink: 0; }
.faq details[open] summary::after { content: "\2212"; }
.faq details p { color: var(--ink-2); padding-bottom: 22px; max-width: 44em; }
.town-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; margin-top: 44px; }
.town { background: var(--paper); border: 1px solid var(--line); border-radius: 22px; padding: 32px; display: flex; flex-direction: column; gap: 14px; scroll-margin-top: 110px; }
.town h2 { font-weight: 900; font-size: clamp(1.7rem, 3vw, 2.3rem); text-transform: uppercase; color: var(--logo-ink); letter-spacing: -0.01em; }
.town h2 .r { color: var(--red); }
.town .pc { font-family: var(--display); font-weight: 800; color: var(--red); font-size: .95rem; }
.town p { color: var(--ink-2); }
.town .btn { align-self: flex-start; margin-top: 8px; }
.uk-band { margin-top: 24px; background: var(--navy); color: var(--on-navy); border-radius: 22px; padding: 32px; display: flex; justify-content: space-between; align-items: center; gap: 24px; flex-wrap: wrap; }
.uk-band h2 { font-weight: 900; font-size: clamp(1.6rem, 3vw, 2.2rem); text-transform: uppercase; }
.uk-band p { color: var(--on-navy-2); margin-top: 8px; max-width: 34em; }
.full-form .card-body { display: grid; gap: 16px; }
.full-form .row2 { margin-top: 0; }
.field textarea { width: 100%; min-height: 110px; padding: 12px 14px; font: 500 16px/1.5 var(--body); color: var(--ink); background: var(--field); border: 1.5px solid var(--line); border-radius: 12px; resize: vertical; }
.field textarea:focus { border-color: var(--logo-ink); outline: none; box-shadow: 0 0 0 3px color-mix(in srgb, var(--red) 30%, transparent); }
.field .opt { font-weight: 500; color: var(--ink-2); }
fieldset.field { border: 0; padding: 0; margin: 0; }
fieldset.field legend { font-size: .9rem; font-weight: 700; padding: 0; margin-bottom: 6px; }
.choices { display: flex; flex-wrap: wrap; gap: 8px; }
.choices label { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 16px; border: 1.5px solid var(--line); border-radius: 999px; font-weight: 600; font-size: .95rem; cursor: pointer; }
.field .choices input { appearance: auto; -webkit-appearance: auto; accent-color: var(--red); width: 18px; height: 18px; min-height: 0; padding: 0; margin: 0; border: 0; box-shadow: none; }
.choices label:has(input:checked) { border-color: var(--logo-ink); }
.full-form .btn { margin-top: 6px; }
.next { list-style: none; padding: 0; margin: 28px 0 0; display: grid; gap: 18px; counter-reset: n; }
.next li { counter-increment: n; display: grid; grid-template-columns: 36px minmax(0, 1fr); gap: 14px; align-items: start; }
.next li::before { content: counter(n); display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: var(--navy); color: var(--on-navy); font-family: var(--display); font-weight: 900; }
.next strong { display: block; color: var(--logo-ink); }
.next span { color: var(--ink-2); }
.side-contact { margin-top: 32px; padding: 24px; border-radius: 18px; background: var(--paper); border: 1px solid var(--line); }
.side-contact p { color: var(--ink-2); }
.side-contact a { font-weight: 800; color: var(--logo-ink); }
.foot-grid { display: grid !important; grid-template-columns: minmax(0, 1.4fr) repeat(2, minmax(0, 1fr)); gap: 32px; padding-block: 48px 28px !important; }
.foot-grid h3 { font-family: var(--body); font-size: .95rem; color: var(--on-navy); margin-bottom: 12px; text-transform: none; }
.foot-grid ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
.foot-grid a { text-decoration: none; }
.foot-grid .logo { color: var(--on-navy); margin-bottom: 14px; }
.foot-base { border-top: 1px solid var(--navy-line); }
@media (hover: hover) and (pointer: fine) { .foot-grid a:hover { color: var(--on-navy); } .svc-link:hover { text-decoration: underline; } }
@media (max-width: 1040px) { .steps.five { grid-template-columns: repeat(2, minmax(0, 1fr)); } .steps.five li:last-child { grid-column: 1 / -1; } }
@media (max-width: 900px) {
  .detail, .town-grid, .also, .svc-grid.three, .foot-grid { grid-template-columns: minmax(0, 1fr); gap: 24px; }
  .detail { padding-block: 40px; }
  .page-hero { padding-block: 40px; }
  .steps.five { grid-template-columns: minmax(0, 1fr); }
  .mnav { display: flex; }
}
.mnav::-webkit-scrollbar { display: none; }
.mnav a { flex-shrink: 0; min-height: 38px; display: inline-flex; align-items: center; padding: 0 14px; border: 1.5px solid var(--line); border-radius: 999px; text-decoration: none; font-weight: 700; font-size: .9rem; }
.full-form .card-head p { white-space: nowrap; }
@media (max-width: 480px) { .full-form .card-head p { display: none; } }
.mnav a[aria-current="page"] { background: var(--navy); color: var(--on-navy); border-color: var(--navy); }
'''

PAGES = [('', 'Home'), ('services/', 'Services'), ('how-it-works/', 'How it works'), ('areas/', 'Areas covered'), ('get-a-quote/', 'Get a quote')]

def header(slug, up):
    links = ''.join(f'<a href="{up}{p}"{" aria-current=\"page\"" if p == slug else ""}>{n}</a>' for p, n in PAGES[1:])
    mlinks = ''.join(f'<a href="{up}{p}"{" aria-current=\"page\"" if p == slug else ""}>{n}</a>' for p, n in PAGES)
    return f'''<header class="top">
  <div class="wrap top-row">
    <a class="logo" href="{up}" aria-label="Family First Removals, home">
      <svg class="logo-icon" viewBox="0 0 64 58" aria-hidden="true">
        <path d="M4 30 L30 8 L46 21.5 V12 H53 V27.5 L58 32" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
        <g style="fill: var(--red)"><rect x="21" y="30" width="7" height="7"/><rect x="30" y="30" width="7" height="7"/><rect x="21" y="39" width="7" height="7"/><rect x="30" y="39" width="7" height="7"/></g>
        <path d="M52 54s-9-5.5-9-11.5a4.6 4.6 0 0 1 9-1.6 4.6 4.6 0 0 1 9 1.6c0 6-9 11.5-9 11.5z" fill="none" style="stroke: var(--red)" stroke-width="3" stroke-linejoin="round"/>
      </svg>
      <span class="logo-words"><span class="logo-name">Family <b>First</b></span><span class="logo-sub">Removals</span></span>
    </a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn btn-red top-call" href="tel:{TEL}" aria-label="Call {TELS}"><svg aria-hidden="true"><use href="#i-phone"/></svg><span class="num">{TELS}</span></a>
  </div>
  <nav class="wrap mnav" aria-label="Pages">{mlinks}</nav>
</header>'''

def footer(up):
    return f'''<footer class="foot">
  <div class="wrap foot-grid">
    <div><a class="logo" href="{up}"><span class="logo-words"><span class="logo-name">Family <b>First</b></span><span class="logo-sub">Removals</span></span></a><p>Family-run removals from Hinckley and Earl Shilton, moving people right across the UK.</p></div>
    <div><h3>Pages</h3><ul>{''.join(f'<li><a href="{up}{p}">{n}</a></li>' for p, n in PAGES)}</ul></div>
    <div><h3>Contact</h3><ul><li><a href="tel:{TEL}">{TELS}</a></li><li><a href="mailto:{EMAIL}" style="overflow-wrap:anywhere">{EMAIL}</a></li><li><a href="{FB}" rel="noopener" target="_blank">Facebook</a></li></ul></div>
  </div>
  <div class="foot-base"><div class="wrap"><p>&copy; <span data-year>2026</span> Family First Removals</p><p>This site uses no cookies or tracking.</p></div></div>
</footer>
<div class="callbar" aria-label="Quick contact">
  <a class="btn btn-white" href="tel:{TEL}">Call now</a>
  <a class="btn btn-red" href="{up}get-a-quote/">Free quote</a>
</div>'''

def page(slug, title, desc, body):
    up = '../' if slug else ''
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0B1222">
<link rel="preload" href="{up}fonts/archivo.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{up}style.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"MovingCompany","name":"Family First Removals","slogan":"Let us take the stress away","telephone":"+44 7858 798002","email":"{EMAIL}","address":{{"@type":"PostalAddress","addressLocality":"Hinckley","addressRegion":"Leicestershire","addressCountry":"GB"}},"areaServed":["Hinckley","Earl Shilton","Leicestershire","United Kingdom"],"sameAs":["{FB}"]}}</script>
<script src="{up}site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{ICONS}
{header(slug, up)}
<main id="main">
{body}
</main>
{footer(up)}
</body>
</html>
'''

def tick(t): return f'<li><svg aria-hidden="true"><use href="#i-check"/></svg>{t}</li>'
HEART = '<svg aria-hidden="true"><use href="#i-heart"/></svg>'

# ---------- home ----------
home = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Let us take <span class="r">the stress</span> away.</h1>
      <p class="script">Removals done the family way {HEART}</p>
      <p class="hero-sub">Family-run removals from Hinckley and Earl Shilton, with moves right across the UK. Every quote starts with a survey, so the price fits your move.</p>
      <div class="hero-actions">
        <a class="btn btn-red" href="get-a-quote/">Get a free quote</a>
        <a class="btn btn-ghost" href="tel:{TEL}">Call {TELS}</a>
      </div>
    </div>
    <div class="van">
      <img src="van.jpg" alt="A Family First Removals van being loaded with boxes outside a house" width="1112" height="472" fetchpriority="high">
      <div class="badge"><svg aria-hidden="true"><use href="#i-shield"/></svg><div class="badge-txt"><strong>Survey first</strong><span>before every quote</span></div></div>
    </div>
  </div>
  <svg class="swoosh" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
    <path class="s-red" d="M0 58 C 360 18, 900 96, 1440 30 L1440 44 C 900 108, 360 34, 0 70 Z"/>
    <path class="s-navy" d="M0 74 C 360 40, 900 112, 1440 52 L1440 90 L0 90 Z"/>
  </svg>
</section>

<section class="strip" aria-label="What we do">
  <div class="wrap strip-row">
    <div class="strip-item"><span class="ring"><svg aria-hidden="true"><use href="#i-house"/></svg></span>House removals</div>
    <div class="strip-item"><span class="ring"><svg aria-hidden="true"><use href="#i-box"/></svg></span>Packing services</div>
    <div class="strip-item"><span class="ring"><svg aria-hidden="true"><use href="#i-sofa"/></svg></span>Furniture transport</div>
    <div class="strip-item"><span class="ring"><svg aria-hidden="true"><use href="#i-shield"/></svg></span>Safe and secure handling</div>
    <div class="strip-item"><span class="ring"><svg aria-hidden="true"><use href="#i-truck"/></svg></span>UK-wide moves</div>
    <div class="strip-area">
      <svg class="pin" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z" fill="currentColor"/><circle cx="12" cy="10" r="2.6" style="fill: var(--navy)"/></svg>
      <p>Hinckley and Earl Shilton<span>Covering all areas of the UK</span></p>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="svc-h">
  <div class="wrap">
    <h2 class="sec-title" id="svc-h">What we <span class="r">move</span></h2>
    <p class="sec-lead">Whole homes, the packing, and the long drive to the other end of the country.</p>
    <div class="svc-grid three">
      <article class="svc"><span class="ring"><svg aria-hidden="true"><use href="#i-house"/></svg></span><h3>House removals</h3><p>Flats and family homes, loaded, moved and set down where you want everything.</p><a class="svc-link" href="services/#removals">More about removals</a></article>
      <article class="svc"><span class="ring"><svg aria-hidden="true"><use href="#i-box"/></svg></span><h3>Packing services</h3><p>The whole house, or just the kitchen and the fragile bits.</p><a class="svc-link" href="services/#packing">More about packing</a></article>
      <article class="svc"><span class="ring"><svg aria-hidden="true"><use href="#i-truck"/></svg></span><h3>UK-wide moves</h3><p>From Hinckley to anywhere in the country, in one trip.</p><a class="svc-link" href="services/#uk">More about UK moves</a></article>
    </div>
  </div>
</section>

<section class="motto" aria-label="Our promise">
  <div class="wrap motto-row">
    <div>
      <h2>No job too big or too small.</h2>
      <p class="script">Let us take the stress away {HEART}</p>
    </div>
    <a class="btn btn-white" href="tel:{TEL}">Call {TELS}</a>
  </div>
</section>

<section class="sec" aria-labelledby="how-h">
  <div class="wrap">
    <h2 class="sec-title" id="how-h">How it <span class="r">works</span></h2>
    <p class="sec-lead">No guesswork on price. We see the move first, then you get a quote that fits it.</p>
    <ol class="steps five">
      <li><h3>Enquiry</h3><p>Send the quote form or give us a call.</p></li>
      <li class="key"><h3>Survey</h3><p>We look at everything that's moving.</p></li>
      <li><h3>Quote</h3><p>A clear price, based on the survey.</p></li>
      <li><h3>15% deposit</h3><p>Secures your moving date.</p></li>
      <li><h3>Moving day</h3><p>Loaded, moved and set down.</p></li>
    </ol>
    <div class="hero-actions"><a class="btn btn-ghost" href="how-it-works/">The full process</a></div>
  </div>
</section>

<section class="closing" aria-labelledby="area-h">
  <div class="wrap closing-grid">
    <div>
      <h2 class="sec-title" id="area-h">Hinckley based, <span class="r">all of the UK</span></h2>
      <p class="sec-lead">Local moves around Hinckley, Earl Shilton and the surrounding areas, and longer runs to every part of the country.</p>
      <ul class="towns"><li>Hinckley</li><li>Earl Shilton</li><li>Surrounding areas</li><li class="uk">All areas of the UK</li></ul>
    </div>
    <div>
      <ul class="contact">
        <li><span>Phone</span><a href="tel:{TEL}">{TELS}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Facebook</span><a href="{FB}" rel="noopener" target="_blank">Family First Removals</a></li>
      </ul>
      <div class="hero-actions"><a class="btn btn-red" href="get-a-quote/">Get a free quote</a><a class="btn btn-white" href="areas/">Areas we cover</a></div>
    </div>
  </div>
</section>'''

def hero(h1, lead, cta=True):
    acts = f'<div class="hero-actions"><a class="btn btn-red" href="../get-a-quote/">Get a free quote</a><a class="btn btn-ghost" href="tel:{TEL}">Call {TELS}</a></div>' if cta else ''
    return f'<section class="page-hero"><div class="wrap"><h1>{h1}</h1><p class="sec-lead">{lead}</p>{acts}</div></section>'

def ctaband(): return f'''<section class="motto" aria-label="Get a quote">
  <div class="wrap motto-row">
    <div><h2>Moving soon?</h2><p class="script">Let us take the stress away {HEART}</p></div>
    <a class="btn btn-white" href="../get-a-quote/">Get a free quote</a>
  </div>
</section>'''

# ---------- services ----------
def detail(i, icon, h, paras, ticks):
    return f'''<article class="detail" id="{i}"><h2><span class="ring"><svg aria-hidden="true"><use href="#i-{icon}"/></svg></span>{h}</h2><div class="body">{''.join(f'<p>{p}</p>' for p in paras)}<ul class="ticks">{''.join(tick(t) for t in ticks)}</ul></div></article>'''
services = hero('Removals, packing and <span class="r">UK-wide moves</span>', 'Everything it takes to get your home from one front door to the next, quoted after a survey so the price matches the job.') + f'''
<section class="sec"><div class="wrap">
{detail('removals', 'house', 'House removals', ['Flats, terraces and family homes. We load the van, protect your furniture on the way, and set everything down in the rooms you want it in at the other end.', 'Because every quote follows a survey, we know what we are moving before the day, so there are no surprises for either of us.'], ['Flats and houses of any size', 'Furniture placed in the right rooms', 'Local moves and long distance'])}
{detail('packing', 'box', 'Packing services', ['Packing is often the most stressful part of a move. We can pack the whole house, or just the parts you would rather not do yourself, like the kitchen and anything fragile.', 'Tell us on the quote form if you want packing, and we will look at it during the survey.'], ['Full or part packing', 'Kitchens and fragile items', 'Added to your quote after the survey'])}
{detail('uk', 'truck', 'UK-wide moves', ['We are based in Hinckley and Earl Shilton, and we move people to every part of the UK. Whether you are going to the next town or the other end of the country, the process is the same: survey, quote, deposit, moving day.'], ['Anywhere in the UK', 'One team from start to finish', 'Same survey-first process'])}
<h2 class="sec-title" style="margin-top:40px">We can <span class="r">also</span> help with</h2>
<div class="also">
  <article class="svc"><span class="ring"><svg aria-hidden="true"><use href="#i-sofa"/></svg></span><h3>Furniture transport</h3><p>Sofas, wardrobes, beds and tables, moved with care from door to door.</p></article>
  <article class="svc"><span class="ring"><svg aria-hidden="true"><use href="#i-boxes"/></svg></span><h3>Single items or full loads</h3><p>One awkward item or a full van. No job too big or too small.</p></article>
  <article class="svc svc-cta"><h3>Not sure what you need?</h3><p>Tell us about the move and we will work it out together at the survey.</p><a class="btn btn-red" href="../get-a-quote/">Get a free quote</a></article>
</div>
</div></section>
{ctaband()}'''

# ---------- how it works ----------
how = hero('From first call to <span class="r">moving day</span>', 'Five steps, and no guessing on price. We look at your move before we quote, so what you are quoted is what the job is.') + f'''
<section class="sec"><div class="wrap">
<ol class="timeline">
  <li><div><h3>Send an enquiry</h3><p>Fill in the quote form or call {TELS}. Tell us where you are moving from and to, roughly when, and what is going with you.</p></div></li>
  <li class="key"><div><h3>We survey your move</h3><p>Before we give a price, we take a proper look at everything that needs moving. It means nothing gets missed, and you get the right van and the right team on the day.</p><span class="tag">Every quote starts here</span></div></li>
  <li><div><h3>You get your quote</h3><p>Based on the survey, we send you a clear quote for the move, including any packing you have asked for.</p></div></li>
  <li><div><h3>15% deposit confirms your date</h3><p>Happy with the quote? A 15% deposit books your moving date in, so the van and team are kept for you.</p></div></li>
  <li><div><h3>Moving day</h3><p>We pack if you have asked us to, load up, and set everything down at the other end, so you can start getting settled.</p></div></li>
</ol>
<h2 class="sec-title" style="margin-top:88px">Good <span class="r">questions</span></h2>
<div class="faq">
  <details><summary>Why do you survey before quoting?</summary><p>Two homes with the same number of bedrooms can need very different moves. Seeing what is actually going means the quote is accurate, and the day runs to plan.</p></details>
  <details><summary>Can I get a price over the phone?</summary><p>We are always happy to talk your move through on the phone, but your quote comes after the survey. That way the price is right first time.</p></details>
  <details><summary>What is the deposit for?</summary><p>The 15% deposit confirms your booking and holds your moving date, so the van and team are reserved for you.</p></details>
  <details><summary>Do you only move people locally?</summary><p>No. We are based around Hinckley and Earl Shilton, and we cover all areas of the UK.</p></details>
</div>
</div></section>
{ctaband()}'''

# ---------- areas ----------
areas = hero('Removals in <span class="r">Hinckley</span> and Earl Shilton', 'A local, family-run removals team, moving people around Hinckley, Earl Shilton and the surrounding areas, and right across the UK.') + f'''
<section class="sec"><div class="wrap">
<div class="town-grid">
  <article class="town" id="hinckley"><p class="pc">LE10</p><h2>Removals in <span class="r">Hinckley</span></h2><p>Moving house in Hinckley? We are a family-run team based right here, so local moves are what we do every week. We survey your home first, give you a clear quote, and look after everything from the first box to the last.</p><p>House removals, packing, and moves from Hinckley to anywhere in the UK.</p><a class="btn btn-red" href="../get-a-quote/">Get a Hinckley quote</a></article>
  <article class="town" id="earl-shilton"><p class="pc">LE9</p><h2>Removals in <span class="r">Earl Shilton</span></h2><p>Family First Removals covers Earl Shilton as home ground. Whether you are moving across the village or out of the county, the process is the same: a survey, a quote that fits the job, then a 15% deposit to book your day.</p><p>House removals, packing, and moves from Earl Shilton to anywhere in the UK.</p><a class="btn btn-red" href="../get-a-quote/">Get an Earl Shilton quote</a></article>
</div>
<div class="uk-band"><div><h2>Moving further afield?</h2><p>We cover all areas of the UK. Long-distance moves get the same survey-first process as a move down the road.</p></div><a class="btn btn-white" href="../get-a-quote/">Get a free quote</a></div>
</div></section>'''

# ---------- quote ----------
quote = hero('Get your free <span class="r">quote</span>', 'Tell us about your move. We’ll get back to you to arrange the survey, then you get a quote that fits.', cta=False) + f'''
<section class="quote-sec" style="padding-top:24px"><div class="wrap quote-grid" style="align-items:start">
<div class="card full-form">
  <form novalidate>
    <div class="card-head"><h3>Free quote</h3><p>takes two minutes</p></div>
    <div class="card-body">
      <div class="route">
        <div class="field"><label for="from">Moving from</label><input id="from" name="from" autocomplete="postal-code" placeholder="Postcode" required></div>
        <span class="route-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg></span>
        <div class="field"><label for="to">Moving to</label><input id="to" name="to" placeholder="Postcode" required></div>
      </div>
      <div class="row2">
        <div class="field"><label for="size">What's moving?</label>
          <select id="size" name="size"><option>Flat or apartment</option><option>2 to 3 bed house</option><option>4+ bed house</option><option>Furniture or single items</option><option>Something else</option></select></div>
        <div class="field"><label for="date">Moving date <span class="opt">(if you know)</span></label><input id="date" name="date" type="date"></div>
      </div>
      <fieldset class="field"><legend>Would you like packing?</legend><div class="choices"><label><input type="radio" name="packing" value="No" checked> No</label><label><input type="radio" name="packing" value="Some"> Some rooms</label><label><input type="radio" name="packing" value="All"> Everything</label></div></fieldset>
      <div class="row2">
        <div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="tel">Phone number</label><input id="tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" required></div>
      </div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" inputmode="email" autocomplete="email" required></div>
      <div class="field"><label for="notes">Anything we should know? <span class="opt">(optional)</span></label><textarea id="notes" name="notes" placeholder="Stairs, parking, a piano, best time to call"></textarea></div>
      <button class="btn btn-red" type="submit">Send my quote request</button>
      <p class="note">We only use your details to arrange your survey and quote.</p>
    </div>
  </form>
  <div class="sent" role="status" aria-live="polite">
    <h3>Thanks, <span data-name>we've got it</span>.</h3>
    <p>On the finished website, this request goes straight to {EMAIL}, with the postcodes, date and phone number ready to call back about your survey.</p>
  </div>
</div>
<div>
  <h2 class="sec-title" style="font-size:clamp(1.8rem,3.4vw,2.6rem)">What happens <span class="r">next</span></h2>
  <ol class="next">
    <li><div><strong>We get in touch</strong><span>to arrange a survey at a time that suits you.</span></div></li>
    <li><div><strong>We survey your move</strong><span>so nothing is missed and the price is right.</span></div></li>
    <li><div><strong>You get your quote</strong><span>A 15% deposit then books your moving date.</span></div></li>
  </ol>
  <div class="side-contact"><p>Rather talk it through?</p><p><a href="tel:{TEL}">{TELS}</a></p><p><a href="mailto:{EMAIL}" style="overflow-wrap:anywhere">{EMAIL}</a></p></div>
</div>
</div></section>'''

JS = r'''/* Family First Removals demo: year in footer, quote form (demo: shows what happens, sends nothing). */
(function () {
  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
  var box = document.querySelector('.card'); if (!box) return;
  var form = box.querySelector('form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = Array.prototype.filter.call(form.querySelectorAll('[required]'), function (f) { return !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim())); });
    form.querySelectorAll('input').forEach(function (f) { f.removeAttribute('aria-invalid'); });
    if (bad.length) { bad.forEach(function (f) { f.setAttribute('aria-invalid', 'true'); }); bad[0].focus(); return; }
    box.querySelector('[data-name]').textContent = form.elements.namedItem('name').value.trim().split(/\s+/)[0];
    box.classList.add('is-sent');
    var s = box.querySelector('.sent'); s.setAttribute('tabindex', '-1'); s.focus();
  });
})();
'''

if __name__ == '__main__':
    css = BASE_CSS.replace('/* Family First Removals: homepage mockup by NEMORA', '/* Family First Removals: demo site by NEMORA') + EXTRA_CSS
    css = css.replace('url("fonts/', 'url("fonts/')
    open(os.path.join(HERE, 'style.css'), 'w').write(css)
    open(os.path.join(HERE, 'site.js'), 'w').write(JS)
    out = [('', 'Family First Removals | Removals in Hinckley and Earl Shilton', 'Family-run removals from Hinckley and Earl Shilton, covering all of the UK. House removals, packing and UK-wide moves, with a survey before every quote.', home),
           ('services/', 'Removals and packing services | Family First Removals', 'House removals, packing services and UK-wide moves from Family First Removals in Hinckley and Earl Shilton.', services),
           ('how-it-works/', 'How it works | Family First Removals', 'Enquiry, survey, quote, 15% deposit, moving day: how a move with Family First Removals works.', how),
           ('areas/', 'Removals in Hinckley and Earl Shilton | Family First Removals', 'Local removals in Hinckley (LE10) and Earl Shilton (LE9), and moves to all areas of the UK.', areas),
           ('get-a-quote/', 'Get a free removals quote | Family First Removals', 'Ask for a free removals quote from Family First Removals. We survey your move first so the price fits.', quote)]
    for slug, title, desc, body in out:
        d = os.path.join(HERE, slug); os.makedirs(d, exist_ok=True)
        html = page(slug, title, desc, body)
        if slug: html = html.replace('href="services/', 'href="../services/').replace('href="get-a-quote/"', 'href="../get-a-quote/"').replace('href="how-it-works/"', 'href="../how-it-works/"').replace('href="areas/"', 'href="../areas/"')
        html = html.replace('href=""', 'href="./"')
        open(os.path.join(d, 'index.html'), 'w').write(html)
    print('built')
