#!/usr/bin/env python3
"""Hudson Valley CNC static site builder.
Edit content in src/content.py, then run: python3 build.py
Output: dist/ (the live website) and preview/ (Claude artifact preview variant)."""
import json, os, shutil, html, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800'
         '&family=IBM+Plex+Mono:wght@400;500;600&family=Instrument+Sans:wght@400;500;600;700&display=swap">')

NAV = [('index.html', 'Home'), ('services.html', 'Services'), ('panels.html', 'Panels'),
       ('contractors.html', 'Contractors'), ('brands.html', 'Brands'), ('artists.html', 'Artists'),
       ('projects.html', 'Projects'), ('about.html', 'About')]


def schema():
    import json as _j
    d = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": C.SITE_URL + "/#business",
         "name": "Hudson Valley CNC", "url": C.SITE_URL + "/", "telephone": "+1-845-384-2994", "email": C.EMAIL,
         "image": C.SITE_URL + "/img/machine-full.jpg", "logo": C.SITE_URL + "/img/logo/logo-ridgeline.png",
         "description": "CNC routing, carving and fabrication shop: signs, carved and acoustic wall panels, architectural details, contractor panel cutting, art fabrication and production runs on a 5x10 automatic tool-change router.",
         "address": {"@type": "PostalAddress", "streetAddress": "30 Crispell Lane", "addressLocality": "New Paltz", "addressRegion": "NY", "postalCode": "12561", "addressCountry": "US"},
         "areaServed": ["New Paltz", "Gardiner", "Kingston", "Poughkeepsie", "Newburgh", "Highland", "Rosendale", "Ulster County", "Dutchess County", "Orange County", "Hudson Valley", "New York City"],
         "knowsAbout": ["CNC routing", "CNC carving", "sign making", "wall panels", "acoustic panels", "architectural millwork", "plywood cutting", "HDPE signs", "3D relief carving"],
         "parentOrganization": {"@type": "Organization", "name": "Clean Air Yurts and Woodworks LLC"}}
    return '<script type="application/ld+json">' + _j.dumps(d) + '</script>'


def head(page, title, desc):
    return f'''<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{C.SITE_URL}/img/machine-full.jpg"><meta property="og:type" content="website">
<link rel="canonical" href="{C.SITE_URL}/{'' if page == 'index.html' else page}">
<meta property="og:url" content="{C.SITE_URL}/{'' if page == 'index.html' else page}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml"><link rel="icon" href="img/logo/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="img/logo/favicon-180.png">
{schema() if page == 'index.html' else ''}
{FONTS}
<link rel="stylesheet" href="assets/style.css">'''


BRAND_MARK = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'brand-mark.svgfrag')).read()


def header(page):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if h == page else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
  <a class="brand" href="index.html">{BRAND_MARK}<b>Hudson Valley CNC</b><span>New Paltz, NY</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="contact.html">Request a Quote</a></nav>
</div></header>'''


def footer():
    return f'''<section class="cta tight"><div class="wrap">
  <h2>Have drawings, a sketch, or just an idea?</h2>
  <div class="hero-actions"><a class="btn" href="contact.html">Request a Quote</a><a class="phone" href="tel:{C.PHONE_TEL}">{C.PHONE}</a></div>
</div></section>
<footer class="site-foot"><div class="wrap">
  <div class="cols">
    <div><img class="foot-badge" src="img/logo/badge.svg" alt="Hudson Valley CNC badge" width="120" height="120"><h4>Hudson Valley CNC</h4><p>Industrial CNC routing, carving and fabrication on a 5&#8242; &times; 10&#8242; automatic tool-change router. Serving the Hudson Valley, the Catskills and the NYC region.</p></div>
    <div><h4>Visit / Call</h4><ul><li>{C.ADDRESS}</li><li><a href="tel:{C.PHONE_TEL}">{C.PHONE}</a></li>{f'<li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>' if C.EMAIL else ''}<li>By appointment</li></ul></div>
    <div><h4>Explore</h4><ul><li><a href="services.html">Services</a></li><li><a href="brands.html">Displays &amp; demos for brands</a></li><li><a href="panels.html">Panel catalog</a></li><li><a href="projects.html">Projects</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Request a quote</a></li></ul></div>
  </div>
  <div class="fine">&copy; Hudson Valley CNC, a dba of Clean Air Yurts and Woodworks LLC &middot; New Paltz, New York</div>
</div></footer>
<script src="assets/main.js"></script>'''


def page(name, title, desc, body, preview=False):
    h = head(name, title, desc)
    b = header(name) + f'\n<main id="main">\n{body}\n</main>\n' + footer()
    if preview and name == 'index.html':
        return h + '\n' + b  # artifact wraps the entry page in its own skeleton
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{h}\n</head>\n<body>\n{b}\n</body>\n</html>\n')


def build(out, preview=False):
    C.PREVIEW = preview
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(out)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(out, 'assets'))
    shutil.copytree(os.path.join(ROOT, 'img'), os.path.join(out, 'img'))
    for f in ('Hudson-Valley-CNC-Panel-Catalog.pdf', 'CNAME', 'robots.txt', '.nojekyll'):
        if os.path.exists(os.path.join(ROOT, f)): shutil.copy(os.path.join(ROOT, f), out)
    for name, (title, desc, body_fn) in C.PAGES.items():
        body = body_fn()
        open(os.path.join(out, name), 'w').write(page(name, title, desc, body, preview))
    # sitemap
    urls = ''.join(f'<url><loc>{C.SITE_URL}/{"" if n == "index.html" else n}</loc></url>' for n in C.PAGES)
    open(os.path.join(out, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')


if __name__ == '__main__':
    build(DIST)
    build(os.path.join(ROOT, 'preview'), preview=True)
    print('built', len(C.PAGES), 'pages')
