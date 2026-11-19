#!/usr/bin/env python3
"""Builds the North South (York) demo site. Run: python3 _build.py"""
import json, os, html
from urllib.parse import quote

OUT = os.path.dirname(os.path.abspath(__file__))
BOOK = "https://ordertab.menu/northsouth/bookings/"
BOOK_FR = "https://ordertab.menu/northsouth/bookings?booking_type=1"
PHONE = "01904 345110"
TEL = "+441904345110"
EMAIL = "contactnorthsouth@gmail.com"
IG = "https://www.instagram.com/northsouthyork/"
MAPS = "https://www.google.com/maps/search/?api=1&query=North+South+25a+Bootham+York+YO30+7BW"
MAP_EMBED = "https://www.google.com/maps?q=North+South,+25a+Bootham,+York+YO30+7BW&output=embed"


def wix(fid, ext, w, h=None, mode="fill"):
    name = f"4d9f73_{fid}~mv2.{ext}"
    size = f"w_{w},h_{h}" if h else f"w_{w},h_{w*3}"
    q = "al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto" if mode == "fill" else "q_90,enc_avif,quality_auto"
    return f"https://static.wixstatic.com/media/{name}/v1/{mode}/{size},{q}/{name}"


LOGO = "https://static.wixstatic.com/media/4d9f73_9e456d80793e4b30a079ecf7ba9a3db7~mv2.png/v1/fit/w_240,h_368,q_90/logo.png"
HERO = ("e8b11b03d99a4a3b849e600130e8bdb2", "jpg")
FIRE = ("329a318b43de4f2981f7d9965816a8dd", "jpg")
VISIT = ("cbf7432253704d79808a6819ae8b1310", "jpg")
GALLERY = [("e89f7c33bbf74d168d032a553749569a", "webp"), ("de1fb723329d4ea39fced1fe6db44ea6", "webp"),
           ("065fe198918042e6a670ee29183a16a2", "webp"), ("4476ef78a3824cb3b218fbf4e9b64e9c", "webp"),
           ("231450799be84720b1d0e25229cc27d2", "webp")]
MENUS = [
    ("breakfast", "Breakfast", "b207fb8940c945ecb3829896a2c78ed2", "png"),
    ("lunch", "Lunch", "dc6e37e127bf4644aec73fbb00bcaa54", "png"),
    ("night", "Night menu", "803d4c5c04974c77b428fc1e8dd68415", "png"),
    ("cocktails", "Cocktails", "b4ae2f9450244f74b2463c55bf47837e", "png"),
    ("wine", "Wine", "0fb031057a1648b288372cdb141fc855", "png"),
]
FR_MENU = ("95998f5af38a4e95815d93ada280f687", "png")

HOURS = [("Monday", "8am", "6pm"), ("Tuesday", "8am", "6pm"), ("Wednesday", "8am", "6pm"),
         ("Thursday", "8am", "6pm"), ("Friday", "8am", "10pm"), ("Saturday", "8am", "10pm"),
         ("Sunday", "8am", "6pm")]

EVENTS = [
    ("2026-11-25", "Wed 25 Nov", "Christmas Wreath Workshop", "Make your own wreath for the door."),
    ("2026-12-01", "Tue 1 Dec", "Christmas Wreath Workshop", "A second date for the wreath workshop."),
    ("2026-12-02", "Wed 2 Dec", "Jewellery Making with Eba Jewellery", "An evening making jewellery with Eba Jewellery."),
    ("2026-12-13", "Sun 13 Dec", "Christmas Quiz with Jack", "Jack's quiz, Christmas edition."),
    ("2026-12-31", "Thu 31 Dec", "New Year's Eve Party", "See the year out at North South."),
]
FR_DATES = [("2026-11-27", "Friday 27 November"), ("2026-11-28", "Saturday 28 November"),
            ("2026-12-16", "Wednesday 16 December"), ("2026-12-17", "Thursday 17 December")]

NAV = [("menus.html", "Menus"), ("free-range-kitchen.html", "Free Range Kitchen"),
       ("events.html", "What's on"), ("visit.html", "Visit us")]

SCHEMA = {
    "@context": "https://schema.org", "@type": "CafeOrCoffeeShop", "name": "North South",
    "slogan": "Meet. Drink. Eat.", "telephone": "+44 1904 345110", "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "25a Bootham", "addressLocality": "York",
                "postalCode": "YO30 7BW", "addressCountry": "GB"},
    "servesCuisine": ["Breakfast", "Lunch", "Cocktails", "Wine"], "acceptsReservations": True,
    "sameAs": [IG],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"], "opens": "08:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "08:00", "closes": "22:00"}],
}


def page(file, title, desc, body, here=None, schema=False):
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == here else ""}>{t}</a>' for h, t in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(SCHEMA)}</script>' if schema else ""
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F4EFE6">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#14120F">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="preload" href="fonts/gloock.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="index.html" aria-label="North South, home"><img src="{LOGO}" alt="North South" width="40" height="61"><span>North South</span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="btn btn-solid top-book" href="{BOOK}" rel="noopener" target="_blank">Book a table</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-mark">
      <p class="foot-name">North South</p>
      <p>Meet. Drink. Eat.</p>
    </div>
    <div>
      <p class="foot-h">Find us</p>
      <p>25a Bootham<br>York YO30 7BW</p>
      <p><a href="{MAPS}" rel="noopener" target="_blank">Open in Google Maps</a></p>
    </div>
    <div>
      <p class="foot-h">Get in touch</p>
      <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}" rel="noopener" target="_blank">Instagram, @northsouthyork</a></p>
    </div>
    <div>
      <p class="foot-h">Open</p>
      <p>Every day from 8am<br>Till 10pm Friday and Saturday<br>Till 6pm every other day</p>
    </div>
  </div>
  <div class="wrap foot-base">
    <p>&copy; <span data-year>2026</span> North South, York</p>
    <p><a href="privacy.html">Privacy and cookies</a></p>
  </div>
</footer>
<script src="site.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, file), "w") as f:
        f.write(doc)


def hours_table(cls="hours"):
    rows = "".join(
        f'<tr data-day="{i}"><th scope="row">{d}</th><td>{o} till {c}</td></tr>' for i, (d, o, c) in enumerate(HOURS))
    return f'<table class="{cls}"><caption class="sr">Opening hours</caption>{rows}</table>'


def events_list(limit=None):
    items = EVENTS[:limit] if limit else EVENTS
    out = []
    for iso, short, name, line in items:
        d, rest = short.split(" ", 1)
        out.append(f"""<li class="ev" data-date="{iso}">
  <time datetime="{iso}"><span class="ev-day">{d}</span><span class="ev-date">{rest}</span></time>
  <div class="ev-body"><h3>{name}</h3><p>{line}</p></div>
  <a class="btn btn-line" href="mailto:{EMAIL}?subject={quote(name + ', ' + short)}">Ask about tickets</a>
</li>""")
    return '<ol class="events">' + "".join(out) + "</ol>"


# ---------------- Home ----------------
gallery = "".join(
    f'<figure class="g-item g{i}"><img src="{wix(fid, ext, 900, 1100)}" alt="" loading="lazy" decoding="async" width="900" height="1100"></figure>'
    for i, (fid, ext) in enumerate(GALLERY))

home = f"""
<section class="hero">
  <img class="hero-img" src="{wix(*HERO, 2000, 1250)}" alt="Inside North South on Bootham, York" width="2000" height="1250" fetchpriority="high">
  <div class="wrap hero-in">
    <h1>Meet. Drink. Eat.</h1>
    <p class="hero-sub">A café bar on Bootham, York, open every day from 8am, and till 10pm on Fridays and Saturdays.</p>
    <div class="actions">
      <a class="btn btn-ember" href="{BOOK}" rel="noopener" target="_blank">Book a table</a>
      <a class="btn btn-ghost" href="menus.html">See the menus</a>
    </div>
  </div>
</section>

<section class="day wrap" aria-labelledby="day-h">
  <h2 id="day-h" class="sr">A day at North South</h2>
  <ol class="day-grid">
    <li><p class="day-time">From 8am</p><h3>Breakfast</h3><p>Breakfast is on from the moment the doors open, every day of the week.</p><a href="menus.html#breakfast">Breakfast menu</a></li>
    <li><p class="day-time">Midday</p><h3>Lunch</h3><p>The lunch menu, for a proper sit-down in the middle of the day.</p><a href="menus.html#lunch">Lunch menu</a></li>
    <li><p class="day-time">Fri and Sat till 10pm</p><h3>Night</h3><p>Cocktails, wine and the night menu at the end of the week.</p><a href="menus.html#night">Night menu</a></li>
  </ol>
</section>

<section class="fire" aria-labelledby="fire-h">
  <div class="wrap fire-grid">
    <figure class="fire-pic"><img src="{wix(*FIRE, 1000, 1300)}" alt="Free Range Kitchen at North South" loading="lazy" width="1000" height="1300"></figure>
    <div class="fire-copy">
      <h2 id="fire-h">Free Range Kitchen</h2>
      <p class="lead">Seasonal, foraged food cooked over open fire, with produce from North Yorkshire, on its own takeover nights at North South.</p>
      <ul class="fr-dates">{''.join(f'<li><time datetime="{i}">{t}</time></li>' for i, t in FR_DATES)}</ul>
      <p class="fr-note">Sittings at 5:30pm and 7:45pm.</p>
      <div class="actions">
        <a class="btn btn-ember" href="{BOOK_FR}" rel="noopener" target="_blank">Book Free Range</a>
        <a class="btn btn-ghost" href="free-range-kitchen.html">About the kitchen</a>
      </div>
    </div>
  </div>
</section>

<section class="wrap block" aria-labelledby="on-h">
  <div class="block-head"><h2 id="on-h">What's on</h2><a href="events.html">All events</a></div>
  {events_list(3)}
</section>

<section class="gallery" aria-label="Photos of North South">
  <div class="wrap g-grid">{gallery}</div>
</section>

<section class="wrap block visit-strip" aria-labelledby="visit-h">
  <div>
    <h2 id="visit-h">25a Bootham</h2>
    <p class="lead">Just outside Bootham Bar, a few minutes' walk from the Minster.</p>
    <div class="actions"><a class="btn btn-solid" href="{BOOK}" rel="noopener" target="_blank">Book a table</a><a class="btn btn-line" href="visit.html">Getting here</a></div>
  </div>
  {hours_table()}
</section>
"""
page("index.html", "North South | Café Bar on Bootham, York",
     "North South is a café bar at 25a Bootham, York. Breakfast, lunch, cocktails and wine, open every day from 8am, till 10pm on Fridays and Saturdays.",
     home, schema=True)

# ---------------- Menus ----------------
tabs = "".join(f'<a href="#{k}">{t}</a>' for k, t, _, _ in MENUS)
menu_secs = "".join(f"""<section class="menu-sec" id="{k}" aria-labelledby="{k}-h">
  <div class="menu-head"><h2 id="{k}-h">{t}</h2><a href="{wix(fid, ext, 1600, mode='fit')}" rel="noopener" target="_blank">Open full size</a></div>
  <img class="menu-img" src="{wix(fid, ext, 1100, mode='fit')}" alt="The North South {t.lower()} menu" loading="lazy" decoding="async">
</section>""" for k, t, fid, ext in MENUS)
menus = f"""
<section class="wrap page-head">
  <h1>Menus</h1>
  <p class="lead">Breakfast and lunch every day, and the night menu, cocktails and wine for later on.</p>
  <nav class="tabs" aria-label="Menus">{tabs}</nav>
</section>
<div class="wrap menus">{menu_secs}</div>
<section class="wrap block cta-row"><p class="lead">Dietary needs or allergies? Tell the team when you order, or call <a href="tel:{TEL}">{PHONE}</a>.</p><a class="btn btn-solid" href="{BOOK}" rel="noopener" target="_blank">Book a table</a></section>
"""
page("menus.html", "Menus | North South, York", "Breakfast, lunch, night menu, cocktails and wine at North South, 25a Bootham, York.", menus, "menus.html")

# ---------------- Free Range Kitchen ----------------
fr = f"""
<section class="fire fire-page">
  <div class="wrap fire-grid">
    <div class="fire-copy">
      <h1>Free Range Kitchen</h1>
      <p class="lead">A seasonal menu built on North Yorkshire produce, foraged finds and cooking over open fire. It runs on its own takeover nights at North South.</p>
      <div class="actions"><a class="btn btn-ember" href="{BOOK_FR}" rel="noopener" target="_blank">Book Free Range</a></div>
    </div>
    <figure class="fire-pic"><img src="{wix(*FIRE, 1000, 1300)}" alt="Free Range Kitchen at North South" width="1000" height="1300"></figure>
  </div>
</section>

<section class="wrap block" aria-labelledby="ways-h">
  <h2 id="ways-h">How the kitchen cooks</h2>
  <div class="ways">
    <div><h3>Seasonal</h3><p>The menu moves with the seasons, so dishes change as ingredients come and go.</p></div>
    <div><h3>Sustainable</h3><p>It backs producers close to home and a local food system in North Yorkshire.</p></div>
    <div><h3>Foraged</h3><p>Foraging sets the pace, and what is growing nearby gives each menu its ideas.</p></div>
    <div><h3>Open fire</h3><p>Much of the cooking happens over flame, for flavour you can't get any other way.</p></div>
  </div>
</section>

<section class="wrap block fr-book" aria-labelledby="next-h">
  <div>
    <h2 id="next-h">The next takeovers</h2>
    <ul class="fr-dates fr-dates-lg">{''.join(f'<li><time datetime="{i}">{t}</time></li>' for i, t in FR_DATES)}</ul>
    <p>Two sittings each night, at 5:30pm and 7:45pm. The example menu is £39 a head.</p>
    <div class="actions"><a class="btn btn-ember" href="{BOOK_FR}" rel="noopener" target="_blank">Book Free Range</a></div>
  </div>
  <figure class="fr-menu"><img src="{wix(*FR_MENU, 1000, mode='fit')}" alt="An example Free Range Kitchen menu" loading="lazy"><figcaption>An example menu. Dishes change with what's in season.</figcaption></figure>
</section>
"""
page("free-range-kitchen.html", "Free Range Kitchen | North South, York",
     "Free Range Kitchen at North South, York: seasonal, foraged, open-fire cooking with North Yorkshire produce. Sittings at 5:30pm and 7:45pm.", fr, "free-range-kitchen.html")

# ---------------- Events ----------------
ev = f"""
<section class="wrap page-head">
  <h1>What's on</h1>
  <p class="lead">We love an event at North South. Quizzes, workshops and parties, all at 25a Bootham.</p>
</section>
<section class="wrap block" aria-label="Upcoming events">
  {events_list()}
  <p class="ev-empty" hidden>Nothing on the list right now. Follow <a href="{IG}" rel="noopener" target="_blank">@northsouthyork</a> for the next one.</p>
</section>
<section class="wrap block cta-row">
  <p class="lead">For tickets, email <a href="mailto:{EMAIL}">{EMAIL}</a>, call <a href="tel:{TEL}">{PHONE}</a>, or message us on <a href="{IG}" rel="noopener" target="_blank">Instagram</a>.</p>
</section>
"""
page("events.html", "What's on | North South, York", "Quizzes, workshops and parties at North South, 25a Bootham, York.", ev, "events.html")

# ---------------- Visit ----------------
visit = f"""
<section class="wrap page-head">
  <h1>Visit us</h1>
  <p class="lead">25a Bootham, York YO30 7BW. Walk in any time, or book a table for the evening.</p>
</section>
<section class="wrap block visit-grid">
  <div>
    <h2>Opening hours</h2>
    {hours_table()}
  </div>
  <div>
    <h2>Booking a table</h2>
    <p>Tables are booked in 90 minute slots. If you'd like to stay longer, get in touch and we'll do our best.</p>
    <p>We don't take bookings on weekend daytimes, so just come in.</p>
    <div class="actions"><a class="btn btn-solid" href="{BOOK}" rel="noopener" target="_blank">Book a table</a><a class="btn btn-line" href="{BOOK_FR}" rel="noopener" target="_blank">Book Free Range</a></div>
    <h2 class="mt">Get in touch</h2>
    <ul class="contact">
      <li><span>Phone</span><a href="tel:{TEL}">{PHONE}</a></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>Instagram</span><a href="{IG}" rel="noopener" target="_blank">@northsouthyork</a></li>
    </ul>
  </div>
</section>
<section class="wrap block">
  <div class="map" data-map="{MAP_EMBED}">
    <img src="{wix(*VISIT, 1600, 900)}" alt="North South, 25a Bootham" loading="lazy" width="1600" height="900">
    <div class="map-veil">
      <p>The map comes from Google, which may set cookies once it loads.</p>
      <div class="actions"><button type="button" class="btn btn-solid" data-load-map>Show the map</button><a class="btn btn-ghost" href="{MAPS}" rel="noopener" target="_blank">Open Google Maps</a></div>
    </div>
  </div>
</section>
"""
page("visit.html", "Visit us | North South, York", "Opening hours, bookings and directions for North South, 25a Bootham, York YO30 7BW.", visit, "visit.html")

# ---------------- Privacy ----------------
priv = f"""
<section class="wrap page-head prose">
  <h1>Privacy and cookies</h1>
  <p class="lead">This website doesn't use tracking or advertising cookies, and it doesn't ask you for any personal details.</p>
  <h2>Who we are</h2>
  <p>North South, 25a Bootham, York YO30 7BW. Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or on <a href="tel:{TEL}">{PHONE}</a>.</p>
  <h2>Cookies</h2>
  <p>We don't set cookies. The map on the Visit us page stays switched off until you press Show the map. After that, Google may set its own cookies under its privacy policy.</p>
  <h2>Booking and contacting us</h2>
  <p>Table bookings are taken through OrderTab, which handles your details under its own privacy policy. If you email or call us, we use your details only to reply and to manage your booking or event, and we don't share them for marketing.</p>
  <h2>Your rights</h2>
  <p>Under UK GDPR you can ask to see, correct or delete the personal information we hold about you. Email us and we'll reply within one month. You can also complain to the Information Commissioner's Office at ico.org.uk.</p>
</section>
"""
page("privacy.html", "Privacy and cookies | North South, York", "How North South, York handles privacy and cookies.", priv)
print("built")
