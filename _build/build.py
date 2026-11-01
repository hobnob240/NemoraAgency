# Builds the static NEMORA site (GitHub Pages friendly).
# Run from the repo root:  python3 _build/build.py .
# Guides live in _build/guides.json (newest first); the hub, sitemap and schema update themselves.
import sys, os, json
OUT = sys.argv[1]
SITE = 'https://nemora.uk'
EMAIL = 'daniel@nemora.uk'
V = '7'
# Microsoft Clarity project ID. Leave empty to keep it switched off; when set, visitors get a consent banner first (UK GDPR / PECR).
CLARITY_ID = ''
# The NEMORA inbox service (Cloudflare Worker). The contact form sends messages here; if it can't be reached the form falls back to email.
INBOX_URL = 'https://nemora-inbox.demositeforyou.workers.dev'

ICON = {
  'arrow': '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10h11m-4-4 4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  'tick': '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m5 10.5 3 3 7-7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  'mail': '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.5"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  'pin': '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="10" r="2.3" stroke="currentColor" stroke-width="1.5"/></svg>',
  'clock': '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
}

# Packages. Every feature here maps to something already built for a real site (see proof notes).
TIERS = [
  dict(id='starter', name='Starter', price=400, monthly=25, label='One-page website',
       care='Hosting, domain, SSL, security and urgent fixes. Content changes are quoted before we do them.',
       desc='Everything a small business needs on one well-designed page: who you are, what you do and how to get in touch. Ideal if you’re just starting out or simply need to look professional online.',
       feats=['One custom-designed page, built for phones first',
              'Sections for your services, about you, photos and contact details',
              'Click-to-call, email and social media buttons',
              'A contact form that sends enquiries to your email',
              'Your location, the areas you cover and your opening hours',
              'Page titles, descriptions and Google-ready structure',
              'Domain, hosting and SSL set up for you',
              'Two rounds of changes before launch']),
  dict(id='business', name='Business', price=795, monthly=50, label='Multi-page website', popular=True,
       care='Everything in Starter’s plan, plus up to 1 hour of changes every month: new photos, prices and text.',
       desc='A full website with a page for each part of your business, plus your own admin area so you can change prices, text and photos yourself, straight from your phone.',
       feats=['Everything in Starter, plus:',
              'Up to 5 pages, such as home, services, about, gallery and contact',
              'Password-protected admin area to update text, prices and photos from your phone',
              'Quote or enquiry form with a private enquiries inbox',
              'Photo gallery to show off your work',
              'Reviews section featuring your real customer reviews',
              'Service pages written to be found in local Google searches',
              'Help setting up your Google Business Profile']),
  dict(id='premium', name='Premium', price=1600, monthly=70, label='Bookings, events and payments',
       care='Everything in Business’s plan, plus up to 2 hours of changes every month and regular checks that bookings, payments and email alerts are working.',
       desc='For businesses that take bookings, sell tickets or run events: a bigger website with the systems behind it to handle listings, booking requests and card payments.',
       feats=['Everything in Business, plus:',
              'Up to 10 pages',
              'Events, shows or class listings you update from your admin area',
              'Booking request forms with every request saved to your inbox',
              'Card payments or deposits through your own Stripe account (Stripe’s fees apply)',
              'Instant email alerts when a new enquiry or booking comes in',
              'A news or guides section to help you climb Google',
              'Visitor analytics with a cookie consent banner']),
]

ORG = {"@type": "ProfessionalService", "@id": SITE + "/#business", "name": "NEMORA", "url": SITE + "/",
  "description": "Web design studio in Stoke-on-Trent that designs, builds and looks after websites for independent businesses.",
  "logo": SITE + "/assets/logo-320.png", "image": SITE + "/assets/og.png", "email": EMAIL,
  "address": {"@type": "PostalAddress", "addressLocality": "Stoke-on-Trent", "addressRegion": "Staffordshire", "addressCountry": "GB"},
  "areaServed": [{"@type": "City", "name": "Stoke-on-Trent"}, {"@type": "City", "name": "Newcastle-under-Lyme"}, {"@type": "AdministrativeArea", "name": "Staffordshire"}, {"@type": "Country", "name": "United Kingdom"}],
  "priceRange": "££", "knowsAbout": ["Web design", "Website development", "Website hosting", "Local SEO"],
  "makesOffer": [{"@type": "Offer", "name": f"{t['name']} website ({t['label']})", "price": str(t['price']), "priceCurrency": "GBP", "description": t['desc'] + f" Then £{t['monthly']} a month: {t['care']} 12-month minimum term."} for t in TIERS]}
def ld(*items):
    return [{"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "NEMORA", "publisher": {"@id": SITE + "/#business"}, "inLanguage": "en-GB"}, *items]}]
def crumbs(name, page):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": SITE + "/" + page}]}

NAV = [('index.html', 'Home'), ('services.html', 'Services'), ('work.html', 'Work'), ('guides/', 'Guides'), ('about.html', 'About')]

def shell(page, title, desc, body, robots='index, follow', schema=None, og_type='website'):
    nav = ''.join(f'<a href="{h}"{(" aria-current=\"page\"" if h == page or (h == "guides/" and page.startswith("guides/")) else "")}>{l}</a>' for h, l in NAV)
    canonical = SITE + '/' + ('' if page == 'index.html' else page)
    current = lambda h: ' aria-current="page"' if h == page or (h == 'guides/' and page.startswith('guides/')) else ''
    return f'''<!DOCTYPE html>
<html lang="en-GB"{f' data-clarity="{CLARITY_ID}"' if CLARITY_ID else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0f1119">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="NEMORA"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="NEMORA, web design studio in Stoke-on-Trent"><meta property="og:locale" content="en_GB"><meta name="geo.region" content="GB-STE"><meta name="geo.placename" content="Stoke-on-Trent"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/assets/favicon-96.png" type="image/png" sizes="96x96"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/serif.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={V}">
<script>(function(d){{d.classList.add('js');setTimeout(function(){{if(!window.NEMORA)d.classList.remove('js')}},2500)}})(document.documentElement)</script>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in (schema or []))}
<script src="assets/site.js?v={V}" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="NEMORA, home"><img src="assets/logo-h.png" alt="NEMORA" width="416" height="96"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span></button>
    <nav id="nav" class="nav" aria-label="Main">{nav}<a class="btn btn-gold" href="contact.html"{" aria-current=\"page\"" if page == "contact.html" else ""}>Start a project</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><img src="assets/logo-h.png" alt="NEMORA" width="416" height="96" loading="lazy"><p>A two-person web design studio in Stoke-on-Trent, Staffordshire, working with businesses across the UK.</p><p class="backstamp"><img src="assets/mark-96.png" alt="" width="99" height="96" loading="lazy"><span>Made in Stoke-on-Trent<small>Designed, built and looked after by NEMORA</small></span></p></div>
      <div><h2>Studio</h2><ul><li><a href="services.html">Services &amp; pricing</a></li><li><a href="work.html">Work</a></li><li><a href="guides/">Guides</a></li><li><a href="about.html">About</a></li></ul></div>
      <div><h2>Contact</h2><ul><li><a href="contact.html">Start a project</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    </div>
    <div class="foot-base"><span>&copy; <span id="year">2026</span> NEMORA. All rights reserved.</span><span class="foot-links"><a href="privacy.html">Privacy</a>{'<button type="button" class="linklike" data-consent-open>Cookie settings</button>' if CLARITY_ID else ''}</span></div>
  </div>
</footer>
</body>
</html>
'''

def cta(title='Tell us about your business', text='A few lines about what you do and what you need is enough. We reply within one working day with honest advice and clear next steps.'):
    return f'''<section class="cta-band">
  <div class="wrap">
    <img class="mark reveal" src="assets/mark-96.png" alt="" width="99" height="96" loading="lazy">
    <h2 class="reveal">{title}</h2>
    <p class="reveal">{text}</p>
    <div class="cta-row reveal"><a class="btn btn-gold" href="contact.html">Start a project {ICON['arrow']}</a><a class="btn btn-line" href="mailto:{EMAIL}">Email us</a></div>
  </div>
</section>'''

WORK = [
  dict(slug='spitfire-comedy', name='Spitfire Comedy', kind='Entertainment', where='Stoke-on-Trent',
       blurb='Live stand-up comedy nights', url='spitfirecomedy.co.uk', live=True,
       summary='A bold new website for a stand-up comedy club in Stoke-on-Trent, themed around its Spitfire plane logo. The next show sits up front on a “boarding pass”, with tickets one tap away.',
       built=['Upcoming shows with a “boarding pass” card for the next night', 'Pages for the acts, open mic nights, reviews and venue bookings', 'Password-protected admin to update shows and photos', 'Technical search fixes so Google indexes the site properly']),
  dict(slug='spiritual', name='Staffordshire Spiritual Events', kind='Events', where='Stoke-on-Trent',
       blurb='Mediumship evenings across Staffordshire', url='staffordshire-events.co.uk', live=True,
       summary='A website for an events company that runs evenings of mediumship at venues around Stoke-on-Trent. Visitors can see what’s on, where, and what a night involves, then get in touch in a tap.',
       built=['Event listings with venues and dates', 'Pages for the mediums, the evening itself and FAQs', 'Password-protected admin so the owner can update shows and photos from a phone', 'Click-to-call and mobile-first design']),
  dict(slug='law-and-son', name='Law and Son Decorators', kind='Trades', where='Wolverhampton',
       blurb='Painters and decorators', url='law-and-son.demositeforyou.workers.dev',
       summary='A full redesign for a family painting and decorating business: a confident first impression, clear services and a quote form that sits right at the top of the page.',
       built=['Quote request form with a built-in enquiries inbox', 'Admin console to manage enquiries, photos and text', 'A new logo and brand colours', 'Service pages written for local search']),
  dict(slug='book-a-medium-night', name='Book a Medium Night', kind='Platform', where='UK-wide',
       blurb='A marketplace for venues and mediums', url='book-a-medium-night.demositeforyou.workers.dev',
       summary='Our own venture: a two-sided platform that connects pubs, clubs and venues with psychics and mediums. Venues list dates for free; mediums pay an annual membership to find bookings.',
       built=['Venue registration with private edit links', 'Member accounts, a members’ portal and card payments through Stripe', 'Public profiles, “Find a medium” search and an enquiries inbox', 'Admin console, demo mode and UK GDPR tools built in']),
]

def showcase(w, cls='', eager=False):
    lz = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<div class="showcase {cls}">
  <div class="browser"><div class="browser-bar"><i></i><i></i><i></i><span>{w['url']}</span></div><img src="assets/work/{w['slug']}.webp" alt="{w['name']} website on a desktop screen" width="1200" height="750" {lz}></div>
  <div class="phone"><img src="assets/work/{w['slug']}-m.webp" alt="{w['name']} website on a phone" width="360" height="720" {lz}></div>
</div>'''

import re
def absolute(html):
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: f'{m.group(1)}="/{"" if m.group(2) == "index.html" else m.group(2)}"', html)
import re as _re
def _no_heading_stops(html):
    # headings end without a full stop (but keep '...' and question marks)
    return _re.sub(r'(<h[1-3][^>]*>)((?:(?!</h[1-3]>).)*?[^.])\.(</h[1-3]>)', r'\1\2\3', html, flags=_re.S)
def write(name, html):
    path = os.path.join(OUT, name); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(absolute(_no_heading_stops(html)))

def tier_cards(full=True):
    out = []
    for t in TIERS:
        feats = ''.join(f'<li>{ICON["tick"]}<span>{f}</span></li>' if not f.endswith('plus:') else f'<li class="plus">{f}</li>' for f in t['feats'])
        out.append(f'''<article class="tier" id="{t['id']}">
  <p class="tier-name">{t['name']}</p>
  <div class="tier-price"><b>£{t['price']:,}</b><span>to design and build</span></div>
  <p class="tier-monthly"><b>then £{t['monthly']} a month</b> {'<span>' + t['care'] + '</span>' if full else ''}</p>
  <h3>{t['label']}</h3>
  <p class="tier-desc">{t['desc']}</p>
  {f'<ul class="ticks">{feats}</ul>' if full else ''}
  <a class="btn btn-line" href="{'contact.html?package=' + t['id'] if full else 'services.html#' + t['id']}">{'Choose ' + t['name'] if full else 'See what’s included'} {ICON['arrow']}</a>
</article>''')
    return f'<div class="tiers" data-stagger>{"".join(out)}</div>'

def work_cards(items):
    return ''.join(f'''<a class="work-card reveal" href="work.html#{w['slug']}" style="--i:{i}">
        <div class="work-media"><span class="tag">{w['kind']}</span><img src="assets/work/{w['slug']}.webp" alt="Homepage of the {w['name']} website" width="1200" height="750" loading="lazy"></div>
        <div class="work-meta"><div><h3>{w['name']}</h3><p>{w['blurb']}</p></div><span class="where">{w['where']}</span></div></a>''' for i, w in enumerate(items))

# ---------------- home ----------------
def frame(w, eager=False, cls=''):
    lz = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<figure class="frame {cls}"><div class="browser-bar"><i></i><i></i><i></i><span>{w["url"] if w.get("live") else w["name"]}</span></div><img src="assets/work/{w["slug"]}.webp" alt="{w["name"]} website" width="1200" height="750" {lz}></figure>'
feat = WORK[0]
home = f'''<section class="hero2">
  <div class="wrap">
    <div class="hero2-top reveal"><span>Web design studio</span><span>Stoke-on-Trent, Staffordshire</span></div>
    <h1 class="display reveal">Websites that make your business look established</h1>
    <div class="hero2-row reveal">
      <p class="lede">We design, build and look after websites for independent businesses: fast, built for phones, and set up to turn visitors into enquiries.</p>
      <div>
        <div class="cta-row"><a class="btn btn-gold" href="contact.html">Start a project {ICON['arrow']}</a><a class="btn btn-line" href="work.html">See our work</a></div>
        <p class="hero-note">From £400 · live in about two weeks · hosting and changes included</p>
      </div>
    </div>
  </div>
  <div class="wall" aria-label="Recent client websites">
    {frame(WORK[1], True, 'w-left')}{frame(WORK[0], True, 'w-mid')}{frame(WORK[2], False, 'w-right')}
  </div>
</section>

<section class="clients" aria-label="Recent clients">
  <div class="wrap"><span class="muted">Recent work for</span><ul>{''.join(f'<li><a href="work.html#{w["slug"]}">{w["name"]}</a></li>' for w in WORK)}</ul></div>
</section>

<section class="section">
  <div class="wrap feature">
    <a class="feature-media" href="work.html#{feat['slug']}">{frame(feat)}</a>
    <div class="feature-copy">
      <p class="eyebrow">Featured project · {feat['where']}</p>
      <h2>{feat['name']}</h2>
      <p class="lede">{feat['summary']}</p>
      <ul class="built">{''.join(f'<li>{b}</li>' for b in feat['built'])}</ul>
      <a class="link-arrow" href="work.html#{feat['slug']}">See the project {ICON['arrow']}</a>
    </div>
  </div>
  <div class="wrap">
    <div class="work-grid three">{work_cards(WORK[1:])}</div>
  </div>
</section>

<section class="section paper">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">What we do</p><h2>What we build, and what we look after</h2></div><p>You deal with one small team from the first conversation to launch day, and long after.</p></div>
    <div class="rows">
      <div class="row-item"><h3>Business websites</h3><p>Fast, polished sites that explain what you do, show your best work and make it easy to get in touch.</p><span>One page to ten · built for phones · written for local search</span></div>
      <div class="row-item"><h3>Enquiries and bookings</h3><p>Quote forms, enquiry inboxes and booking requests that send real leads to you, not to a spam folder.</p><span>Enquiry inbox · booking requests · Stripe payments</span></div>
      <div class="row-item"><h3>An admin you can use</h3><p>Update photos, prices, events and text from your phone, in a simple, password-protected admin area.</p><span>Photos · prices · events · text</span></div>
      <div class="row-item"><h3>Care every month</h3><p>Changes, urgent fixes, hosting, security and speed, so your site keeps working as hard as you do.</p><span>Domain and hosting · monthly changes · fixes</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">How it works</p><h2>How a project runs, from first chat to launch</h2></div><a class="link-arrow" href="services.html">Services and pricing {ICON['arrow']}</a></div>
    <ol class="steps">
      <li><h3>Talk</h3><p>We learn about your business, your customers and what the website needs to do.</p></li>
      <li><h3>Design</h3><p>We design a site around your brand and show it to you early, so you can shape it.</p></li>
      <li><h3>Build</h3><p>We build it mobile-first and search-ready, with the tools you need behind it.</p></li>
      <li><h3>Launch and look after</h3><p>We put it live on your domain and keep it updated, secure and working every month.</p></li>
    </ol>
  </div>
</section>

<section class="section paper">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Pricing</p><h2>Three packages, with the prices published</h2></div><p>One fixed price to design and build, then a monthly plan for hosting, updates and fixes. <a href="guides/how-much-does-a-website-cost.html">How much should a website cost?</a></p></div>
    {tier_cards(full=False)}
    <p class="tier-foot">12-month minimum term on every plan. Half the setup fee is paid upfront to book your project.</p>
  </div>
</section>

<section class="section local">
  <div class="wrap split">
    <div><p class="eyebrow">Local to you</p><h2>Web design in Stoke-on-Trent and Staffordshire</h2><p class="backstamp"><img src="assets/mark-96.png" alt="" width="99" height="96" loading="lazy"><span>Made in Stoke-on-Trent<small>Designed, built and looked after by NEMORA</small></span></p></div>
    <div>
      <p class="lede">We’re based in Stoke-on-Trent and build websites for businesses across the Potteries, Newcastle-under-Lyme and the rest of Staffordshire, including Spitfire Comedy and Staffordshire Spiritual Events.</p>
      <p class="lede">We work with clients further afield too, like Law and Son Decorators in Wolverhampton: trades, events, venues, salons and new ventures. Everything can be done by phone, email or video call.</p>
      <a class="link-arrow" href="contact.html">Talk to a local web designer {ICON['arrow']}</a>
    </div>
  </div>
</section>
{cta()}'''
write('index.html', shell('index.html', 'Web Design Stoke-on-Trent | NEMORA', 'NEMORA is a web design studio in Stoke-on-Trent, Staffordshire. Mobile-first websites from £400, with hosting and care plans from £25 a month.', home, schema=ld({'@type': 'WebPage', 'url': SITE + '/', 'name': 'Web Design Stoke-on-Trent | NEMORA', 'about': {'@id': SITE + '/#business'}})))

# ---------------- services ----------------
FAQ = [
  ('How long does a website take?', 'Most sites go live within around two weeks once we have your content: your logo, photos and the details you want on the site. Larger builds take longer, and we’ll give you a timeline before we start.'),
  ('What does the monthly fee cover?', 'Every plan covers hosting, your domain, SSL, security and urgent fixes. Business (£50 a month) adds up to 1 hour of changes every month, and Premium (£70 a month) adds up to 2 hours plus regular checks on bookings and payments. On Starter (£25 a month), content changes are quoted before we do them.'),
  ('Do I pay everything upfront?', 'No. Half of your package’s setup fee is paid upfront to book your project, and the rest when your website is ready to go live.'),
  ('Which package do I need?', 'Starter (£400, then £25 a month) suits a business that needs one professional page. Business (£795, then £50 a month) gives you up to five pages and your own admin area to make changes from your phone. Premium (£1,600, then £70 a month) adds events or listings, booking requests and card payments. If you’re unsure, ask and we’ll recommend one honestly.'),
  ('Who owns the domain?', 'We register and manage your domain as part of the plan. If you decide to leave after your minimum term, we can transfer it to you for a fee.'),
  ('Can you redesign my existing website?', 'Yes. We regularly rebuild older or slow websites, keeping what works and fixing what doesn’t.'),
  ('Will it work on phones?', 'Every site is designed for phones first, because that’s where most of your customers will see it.'),
  ('What about bigger projects?', 'Booking systems, member areas and platforms like Book a Medium Night are priced individually. Tell us what you need and we’ll give you a clear quote.'),
]
services = f'''<section class="page-head">
  <div class="wrap"><p class="eyebrow reveal">Services &amp; pricing</p><h1 class="reveal">Website design and pricing for growing businesses.</h1><p class="lede reveal">One small team in Stoke-on-Trent designs, builds, hosts and looks after your website, so you can get on with running your business.</p></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cards" data-stagger>
      <div class="card"><span class="num">01</span><h3>Website design &amp; build</h3><p>A site designed around your brand and your customers.</p><ul><li>From one page up to ten, depending on your package</li><li>Mobile-first, fast-loading design</li><li>Clear calls to action and click-to-call</li><li>Written and structured for local search</li></ul></div>
      <div class="card"><span class="num">02</span><h3>Enquiries &amp; admin</h3><p>The tools behind the scenes that make your site work for you.</p><ul><li>Contact and quote forms</li><li>Enquiry inboxes</li><li>Password-protected admin area</li><li>Update photos and text from your phone</li></ul><a class="link-arrow" href="work.html#law-and-son">Example: Law and Son Decorators {ICON['arrow']}</a></div>
      <div class="card"><span class="num">03</span><h3>Hosting &amp; care</h3><p>We keep your site online, secure and up to date.</p><ul><li>Domain, hosting and SSL managed for you</li><li>A few changes every month</li><li>Urgent fixes when you need them</li><li>Speed and security looked after</li></ul></div>
      <div class="card"><span class="num">04</span><h3>Bigger builds</h3><p>When you need more than a brochure site.</p><ul><li>Booking and membership systems</li><li>Card payments with Stripe</li><li>Directories and marketplaces</li><li>Priced individually</li></ul><a class="link-arrow" href="work.html#book-a-medium-night">Example: Book a Medium Night {ICON['arrow']}</a></div>
    </div>
  </div>
</section>

<section class="section alt" id="pricing">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow reveal">Packages &amp; pricing</p><h2 class="reveal">Choose the website that fits your business.</h2></div><p class="reveal">Three fixed prices for the design and build, so you know exactly what you’re paying before we start.</p></div>
    {tier_cards()}
    <div class="monthly reveal">
      <div><p class="eyebrow">Every monthly plan includes</p><p class="price-sub">12-month minimum term. Half the setup fee is paid upfront to book your project, the rest when your website is ready to go live.</p></div>
      <ul class="ticks">
        <li>{ICON['tick']}<span>Domain, hosting and SSL managed for you</span></li>
        <li>{ICON['tick']}<span>Security and speed looked after</span></li>
        <li>{ICON['tick']}<span>Urgent fixes whenever something stops working</span></li>
        <li>{ICON['tick']}<span>Two rounds of changes before launch, on every package</span></li>
      </ul>
    </div>
    <div class="price-aside three">
      <div class="note-card reveal"><h3>Need something bigger?</h3><p>Member areas, directories and marketplaces like <a href="work.html#book-a-medium-night">Book a Medium Night</a> are quoted individually, based on what you need.</p></div>
      <div class="note-card reveal"><h3>Already have a website?</h3><p>We can redesign it, speed it up and move it onto our hosting with minimal disruption.</p></div>
      <div class="note-card reveal"><h3>Not sure which to pick?</h3><p>Send us a message. We’ll recommend the right package honestly, even if it’s the cheapest one.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow reveal">Questions</p><h2 class="reveal">Questions people ask us</h2></div></div>
    <div class="faq" data-stagger>{''.join(f'<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in FAQ)}</div>
    <p class="faq-more reveal">Comparing quotes? Read <a href="guides/how-much-does-a-website-cost.html">how much a small business website should cost</a>.</p>
  </div>
</section>
{cta()}'''
write('services.html', shell('services.html', 'Website Design Prices & Services | Stoke-on-Trent | NEMORA', 'Website packages at £400, £795 and £1,600, with hosting and care from £25 a month. Web design for businesses in Stoke-on-Trent and Staffordshire.', services, schema=ld(crumbs('Services & pricing', 'services.html'), {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]})))

# ---------------- work ----------------
cases = ''.join(f'''<article class="case{' flip' if i % 2 else ''}" id="{w['slug']}">
  <div class="reveal">{showcase(w)}</div>
  <div class="reveal">
    <p class="kind">{w['kind']} · {w['where']}</p>
    <h2>{w['name']}</h2>
    <p>{w['summary']}</p>
    <dl><dt>What we built</dt><dd>{'<br>'.join(w['built'])}</dd></dl>
    {f'<a class="link-arrow" href="https://{w["url"]}/" target="_blank" rel="noopener">Visit the live site <span class="sr">(opens in a new tab)</span> {ICON["arrow"]}</a>' if w.get('live') else ''}
  </div>
</article>''' for i, w in enumerate(WORK))
work = f'''<section class="page-head">
  <div class="wrap"><p class="eyebrow reveal">Work</p><h1 class="reveal">Recent websites and what each business needed</h1><p class="lede reveal">A selection of recent web design projects, from Stoke-on-Trent to Wolverhampton: what each business needed, and what we built for them.</p></div>
</section>
<section class="section pt-sm"><div class="wrap">{cases}</div></section>
<section class="section alt"><div class="wrap split"><div><p class="eyebrow reveal">Planning your own?</p><h2 class="reveal">See what it costs and what’s included.</h2></div><div class="reveal"><p class="lede">Every project above started with a short conversation. Our pricing is fixed and published, and our guides explain what a good small business website needs.</p><div class="link-stack"><a class="link-arrow" href="services.html">Services &amp; pricing {ICON['arrow']}</a><a class="link-arrow" href="guides/what-should-a-small-business-website-include.html">What should a business website include? {ICON['arrow']}</a></div></div></div></section>
{cta('Want a website like these for your business?')}'''
write('work.html', shell('work.html', 'Web Design Portfolio | Stoke-on-Trent | NEMORA', 'Websites by NEMORA, including Spitfire Comedy and Staffordshire Spiritual Events in Stoke-on-Trent, Law and Son Decorators and Book a Medium Night.', work, schema=ld(crumbs('Work', 'work.html'))))

# ---------------- about ----------------
about = f'''<section class="page-head">
  <div class="wrap"><p class="eyebrow reveal">About</p><h1 class="reveal">Websites for local businesses, built properly.</h1><p class="lede reveal">NEMORA is a small, independent web design studio in Stoke-on-Trent. We design and build every site ourselves, for comedy clubs, event companies, tradespeople and venues, and we look after them once they’re live.</p></div>
</section>
<section class="section">
  <div class="wrap split">
    <div><p class="eyebrow reveal">Why we started</p><h2 class="reveal">Why we started NEMORA</h2></div>
    <div class="reveal">
      <p class="lede">Too many good local businesses are let down by their websites: slow, dated, hard to use on a phone, or impossible to update without ringing someone. Customers notice, and they go elsewhere.</p>
      <p class="lede">We started NEMORA to fix that with sites that look as good as the business really is, a fixed price you can see before you call, and an admin area simple enough to update from your phone.</p>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap split">
    <div><p class="eyebrow reveal">What we’ve built</p><h2 class="reveal">What we’ve built so far</h2></div>
    <div class="reveal">
      <p class="lede">Our recent work includes <a href="work.html#spitfire-comedy">Spitfire Comedy</a>, a stand-up comedy club in Stoke-on-Trent, <a href="work.html#spiritual">Staffordshire Spiritual Events</a>, which runs mediumship evenings across the county, and <a href="work.html#law-and-son">Law and Son Decorators</a> in Wolverhampton.</p>
      <p class="lede">We also run our own platform, <a href="work.html#book-a-medium-night">Book a Medium Night</a>, which connects venues with mediums, takes card payments and handles member accounts. Running a business on our own code keeps us honest about what owners actually need from a website.</p>
      <a class="link-arrow" href="work.html">See all our work {ICON['arrow']}</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow reveal">How we work</p><h2 class="reveal">What you can expect from us.</h2></div><a class="link-arrow reveal" href="services.html">Services &amp; pricing {ICON['arrow']}</a></div>
    <div class="values" data-stagger>
      <div><h3>Clarity</h3><p>Plain English, published prices (packages from £400, with care plans from £25 a month) and honest advice, even when that advice is that you don’t need us.</p></div>
      <div><h3>Craft</h3><p>Fast, accessible and carefully built, designed for phones first, with the small details done properly on every screen size.</p></div>
      <div><h3>Care</h3><p>Your site doesn’t stop at launch. We host it, keep it secure and make your changes, month after month.</p></div>
    </div>
  </div>
</section>
{cta()}'''
write('about.html', shell('about.html', 'About NEMORA | Web Design Studio in Stoke-on-Trent', 'NEMORA is an independent web design studio in Stoke-on-Trent. We design, build and look after websites for local businesses, from comedy clubs to tradespeople.', about, schema=ld(crumbs('About', 'about.html'), {'@type': 'AboutPage', 'url': SITE + '/about.html', 'about': {'@id': SITE + '/#business'}})))

# ---------------- contact ----------------
contact = f'''<section class="page-head">
  <div class="wrap"><p class="eyebrow reveal">Contact</p><h1 class="reveal">Let’s talk about your website.</h1><p class="lede reveal">Tell us a little about your business and what you need. We’ll reply with honest advice and clear next steps.</p></div>
</section>
<section class="section">
  <div class="wrap contact-grid">
    <form class="form reveal" id="contact-form" data-to="{EMAIL}" data-endpoint="{INBOX_URL}" action="mailto:{EMAIL}" method="post" enctype="text/plain" novalidate>
      <div class="hp" aria-hidden="true"><label for="f-website">Leave this empty</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="row2"><div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" autocapitalize="none" spellcheck="false" required></div></div>
      <div class="row2"><div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f-business">Business name <span class="opt">(optional)</span></label><input id="f-business" name="business" type="text" autocomplete="organization"></div></div>
      <div class="field"><label for="f-package">Package</label><select id="f-package" name="package"><option value="">Not sure yet</option>{''.join(f'<option value="{t["id"]}">{t["name"]}: {t["label"]}, £{t["price"]:,}</option>' for t in TIERS)}<option value="bigger">Something bigger (quoted individually)</option></select></div>
      <div class="field"><label for="f-need">What do you need?</label><select id="f-need" name="need" required><option value="">Choose one</option><option>A new website</option><option>A redesign of my current website</option><option>A booking, membership or payment system</option><option>Not sure yet</option></select></div>
      <div class="field"><label for="f-message">Tell us about your business</label><textarea id="f-message" name="message" rows="6" required placeholder="What you do, who your customers are, and anything you like or dislike about your current website."></textarea></div>
      <p class="fine" id="form-fine">Your message comes straight to us. We only use your details to reply. See our <a href="privacy.html">privacy notice</a>.</p>
      <div><button class="btn btn-gold" type="submit" id="form-send">Send enquiry {ICON['arrow']}</button></div>
      <p class="form-msg" id="form-msg" role="status" hidden></p>
    </form>
    <aside class="contact-aside">
      <a class="contact-line reveal" href="mailto:{EMAIL}">{ICON['mail']}<span><small>Email</small><b>{EMAIL}</b></span></a>
      <div class="contact-line reveal">{ICON['pin']}<span><small>Based in</small><b>Stoke-on-Trent, Staffordshire</b></span></div>
      <div class="contact-line reveal">{ICON['clock']}<span><small>Timescales</small><b>Most websites go live in around two weeks</b></span></div>
      <div class="note-card reveal"><h3>What happens next</h3><p>We’ll reply to talk through what you need, then send a clear plan and price. No pressure, and no obligation.</p></div>
    </aside>
  </div>
</section>'''
write('contact.html', shell('contact.html', 'Contact a Web Designer in Stoke-on-Trent | NEMORA', 'Start a website project with NEMORA, a web design studio in Stoke-on-Trent. Tell us about your business and we’ll reply with honest advice and a clear price.', contact, schema=ld(crumbs('Contact', 'contact.html'))))

# ---------------- privacy ----------------
privacy = f'''<section class="page-head"><div class="wrap"><p class="eyebrow">Privacy</p><h1>Privacy notice</h1><p class="lede">How NEMORA handles personal information on this website.</p></div></section>
<section class="section"><div class="wrap prose">
  <p class="muted">Last updated: October 2026</p>
  <h2>Who we are</h2><p>This website is run by NEMORA, a web design studio based in Stoke-on-Trent, Staffordshire. You can contact us about privacy at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>What we collect</h2><p>{'This website only uses analytics if you agree to it (see “Analytics cookies” below).' if CLARITY_ID else 'This website doesn’t use cookies or advertising trackers.'} When you send us a message through the contact form, we receive the details you type in: your name, email address, and, if you choose to give them, your phone number, business name, the package you’re interested in and your message. If the form can’t reach us for any reason, it opens your own email app with your message filled in instead.</p>
  {'<h2>Analytics cookies</h2><p>If you press “Accept” on our cookie banner, we use Microsoft Clarity to understand how visitors use the site (for example where people click and how far they scroll) so we can improve it. Clarity sets cookies and processes usage data, including your IP address, on our behalf; see the <a href="https://privacy.microsoft.com/privacystatement" rel="noopener">Microsoft privacy statement</a>. Our lawful basis is your consent. If you press “Reject” or ignore the banner, Clarity is never loaded. You can change your choice at any time using “Cookie settings” at the bottom of every page.</p>' if CLARITY_ID else ''}
  <p>We use your details only to reply to you and, if you go ahead, to provide our services. Our lawful basis is your request for information and, where relevant, our contract with you. To stop the form being misused, we also keep a scrambled (hashed) version of your internet address for one hour; it can’t be turned back into your address.</p>
  <h2>Visit statistics</h2><p>To see how many people visit and which pages are popular, we keep a simple count of visits. For each page you open we record the page address, the website that linked you here (just its name, for example google.com), whether you’re on a phone, tablet or computer, and the country your connection comes from. To count unique visitors without cookies, your IP address and browser type are combined with a random code that changes every day and turned into a one-way code; your IP address itself is never stored, and the code can’t be traced back to you or linked from one day to the next. No cookies are set and nothing is stored on your device. This runs on Cloudflare, our hosting provider. Our lawful basis is our legitimate interest in understanding how our website is used. Visit statistics are deleted after 13 months. If your browser sends a “Do Not Track” or “Global Privacy Control” signal, we don’t count your visit at all.</p>
  <h2>How long we keep it</h2><p>Messages are deleted automatically after 2 years, or sooner if you ask. If you become a client, we keep business records for as long as the law requires.</p>
  <h2>Who sees it</h2><p>Only us, through a password-protected admin area. Messages are stored securely by Cloudflare, our hosting provider, and our email is provided by Microsoft; both process data on our behalf under data protection agreements, which may involve servers outside the UK with appropriate safeguards. We never sell your information or use it for advertising.</p>
  <h2>Your rights</h2><p>You can ask to see, correct or delete the information we hold about you, or object to how we use it, by emailing us. If you’re unhappy with how we’ve handled your information, you can complain to the Information Commissioner’s Office at <a href="https://ico.org.uk/make-a-complaint/" rel="noopener">ico.org.uk</a>.</p>
</div></section>'''
write('privacy.html', shell('privacy.html', 'Privacy | NEMORA', 'How NEMORA handles personal information on this website.', privacy))

# ---------------- guides ----------------
# Add a new dict to GUIDES (newest first) to publish a new guide; the hub, sitemap and schema update themselves.
GUIDES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guides.json'), encoding='utf-8'))
GUIDES.sort(key=lambda g: g['date'], reverse=True)

def nice_date(d):
    import datetime; x = datetime.date.fromisoformat(d); return f'{x.day} {x.strftime("%B %Y")}'
for g in GUIDES:
    url = f"{SITE}/guides/{g['slug']}.html"
    others = [o for o in GUIDES if o is not g]
    page = f'''<article>
<section class="page-head"><div class="wrap narrow"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/guides/">Guides</a></nav><h1 class="reveal">{g['title']}</h1><p class="lede reveal">{g['intro']}</p><p class="meta reveal">By NEMORA · <time datetime="{g['date']}">{nice_date(g['date'])}</time> · {g['mins']} minute read</p></div></section>
<section class="section pt-sm"><div class="wrap narrow prose">{g['body']}</div></section>
</article>
{('<section class="section alt"><div class="wrap narrow"><p class="eyebrow">Keep reading</p>' + ''.join(f'<a class="guide-card" href="/guides/{o["slug"]}.html"><h3>{o["title"]}</h3><p>{o["desc"]}</p></a>' for o in others[:2]) + '</div></section>') if others else ''}
{cta('Want a website that ticks every box?')}'''
    art = {'@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'datePublished': g['date'], 'dateModified': g['date'], 'inLanguage': 'en-GB', 'mainEntityOfPage': url, 'image': SITE + '/assets/og.png', 'author': {'@id': SITE + '/#business'}, 'publisher': {'@id': SITE + '/#business'}}
    bc = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/guides/"}, {"@type": "ListItem", "position": 3, "name": g['title'], "item": url}]}
    write(f"guides/{g['slug']}.html", shell(f"guides/{g['slug']}.html", f"{g['title']} | NEMORA", g['desc'], page, schema=ld(bc, art), og_type='article'))
hub = f'''<section class="page-head"><div class="wrap"><p class="eyebrow reveal">Guides</p><h1 class="reveal">Straight answers about small business websites.</h1><p class="lede reveal">Practical guides from our studio in Stoke-on-Trent: what websites cost, what they need and how to get more enquiries from yours.</p></div></section>
<section class="section pt-sm"><div class="wrap"><div class="guide-grid" data-stagger>{''.join(f'<a class="guide-card" href="/guides/{g["slug"]}.html"><span class="meta">{nice_date(g["date"])} · {g["mins"]} min read</span><h2>{g["title"]}</h2><p>{g["desc"]}</p><span class="link-arrow">Read the guide {ICON["arrow"]}</span></a>' for g in GUIDES)}</div></div></section>
{cta()}'''
write('guides/index.html', shell('guides/', 'Website Guides for Small Businesses | NEMORA', 'Plain-English website guides for small businesses in Stoke-on-Trent and beyond: what a website costs, what it should include and how to win more enquiries.', hub, schema=ld(crumbs('Guides', 'guides/'), {'@type': 'CollectionPage', 'url': SITE + '/guides/', 'name': 'Guides', 'hasPart': [{'@type': 'Article', 'headline': g['title'], 'url': f"{SITE}/guides/{g['slug']}.html"} for g in GUIDES]})))

# ---------------- 404 ----------------
nf = f'''<section class="page-head no-border"><div class="wrap"><p class="eyebrow">Page not found</p><h1>We couldn’t find that page.</h1><p class="lede">It may have moved. Try one of these instead.</p><div class="cta-row mt"><a class="btn btn-gold" href="index.html">Home</a><a class="btn btn-line" href="work.html">Our work</a><a class="btn btn-line" href="contact.html">Contact</a></div></div></section>'''
nf += f'''<section class="section pt-sm"><div class="wrap"><div class="sec-head"><div><p class="eyebrow">While you’re here</p><h2>Some of our recent work.</h2></div><a class="link-arrow" href="guides/">Read our guides {ICON['arrow']}</a></div><div class="work-grid">{work_cards(WORK[:2])}</div></div></section>'''
write('404.html', shell('404.html', 'Page not found | NEMORA', 'This page could not be found.', nf, robots='noindex'))
print('built')

LASTMOD = {f"guides/{g['slug']}.html": g['date'] for g in GUIDES}
LASTMOD['guides/'] = max([g['date'] for g in GUIDES] + ['2026-10-29'])
PAGES = ['', 'services.html', 'work.html', 'about.html', 'contact.html', 'guides/'] + [f"guides/{g['slug']}.html" for g in GUIDES] + ['privacy.html']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}/{p}</loc><lastmod>{LASTMOD.get(p, "2026-10-29")}</lastmod></url>\n' for p in PAGES) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /social/\n\nSitemap: {SITE}/sitemap.xml\n')
print('sitemap + robots')
