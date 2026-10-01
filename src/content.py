"""All site content. Edit text here, then run build.py."""
import json, os, html
E = html.escape
HERE = os.path.dirname(__file__)

SITE_URL = 'https://hudsoncnc.com'
PHONE = '845-384-2994'
PHONE_TEL = '+18453842994'
EMAIL = 'hudsonvalleycnc@gmail.com'
ADDRESS = '30 Crispell Lane, New Paltz, NY 12561'
QUOTE_FORM_URL = 'https://form.jotform.com/262724476586066'  # Jotform quote form, embedded on the live site
PREVIEW = False


def img(name, alt, cls='', full=True, sizes=''):
    extra = f' data-full="img/{name}.jpg"' if full else ''
    return f'<img src="img/{name}-sm.jpg" alt="{E(alt)}" loading="lazy" decoding="async"{extra}{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'


def cta_row(extra=''):
    return f'<div class="hero-actions"><a class="btn" href="contact.html">Request a Quote</a><a class="btn ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a>{extra}</div>'


# ---------------------------------------------------------------- HOME
def home():
    aud = [
        ('contractors.html', 'crates-on-table', 'Plywood parts nested on the router table', 'Contractors & Builders',
         'Panels cut and drilled, carved trim, curved forms and roof details, ready to install.'),
        ('panels.html', 'relief-carving', 'Carved white 3D relief panel', 'Designers & Architects',
         'Wall panels, screens, fixtures and millwork cut to your drawings, in any material we stock.'),
        ('artists.html', 'portrait-engraving', 'Engraved photo portrait on a black panel', 'Artists & Makers',
         'Relief carving, molds, terrain models, props and editions, cut to scale.'),
        ('services.html', 'trail-signs', 'Carved wood trail signs', 'Businesses & Communities',
         'Signs, trail markers, displays, plaques and production runs of your products.'),
    ]
    tiles = ''.join(f'<a class="tile" href="{h}">{img(i, a, full=False)}<h3>{t}</h3><p>{d}</p><span class="more">See how we help &rarr;</span></a>' for h, i, a, t, d in aud)
    feat = [('library-plaque', 'Gardiner Library commemorative brick wall', 'Gardiner Library Brick Project'),
            ('colorcore-sign', 'Two-color HDPE storefront sign on the router', 'Variable Movement sign'),
            ('slat-bench', 'Curved slatted plywood bench', 'Slatted plywood bench'),
            ('weldwood-sign-2', 'Dimensional 100-year anniversary sign', 'DAP Weldwood 100 Years'),
            ('crates-stacked', 'Stacked plywood crates from a production run', 'Plywood crate production run'),
            ('relief-carving-2', 'White 3D relief carving', '3D relief carving')]
    feats = ''.join(f'<figure class="proj">{img(n, a)}<figcaption><h3>{t}</h3></figcaption></figure>' for n, a, t in feat)
    return f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">CNC routing &middot; carving &middot; fabrication</span>
    <h1>From trail signs to commercial builds</h1>
    <p class="lede">Hudson Valley CNC cuts, carves and drills wood, plywood, plastics and composites on a 5&#8242; &times; 10&#8242; industrial router with a 12-tool automatic changer. Send drawings, a sketch or a sample. We&#8217;ll turn it into finished parts, one piece or a thousand.</p>
    {cta_row()}
  </div>
  <figure class="hero-img"><img src="img/machine-full.jpg" alt="Hudson Valley CNC's 5 by 10 foot automatic tool-change CNC router in our shop" width="1200" height="1600"><figcaption>STM1530C &middot; 60&quot; &times; 120&quot; bed &middot; New Paltz, NY</figcaption></figure>
</div></section>

<div class="specs"><div class="wrap">
  <div class="spec"><b>5&#8242; &times; 10&#8242;</b><span>Full sheets, no seams</span></div>
  <div class="spec"><b>12</b><span>Tools on the automatic changer</span></div>
  <div class="spec"><b>24,000</b><span>RPM, 9 kW HSD spindle</span></div>
  <div class="spec"><b>~12&quot;</b><span>Z clearance for thick stock</span></div>
  <div class="spec"><b>4th axis</b><span>Rotary carving for posts &amp; columns</span></div>
</div></div>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Who we work with</span><h2>One shop, a wide range of work</h2>
  <p class="lede">A one-off carved sign and a run of 500 identical parts get the same care. Pick where you fit.</p></div>
  <div class="grid g4">{tiles}</div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How a job runs</span><h2>Drawing to finished part</h2></div>
  <ol class="steps">
    <li><b>Send it over</b><span>DXF, DWG, SVG, PDF, STL, a sketch, a photo, or a sample to match.</span></li>
    <li><b>We program it</b><span>CAD/CAM file prep, nesting to save material, and a quote.</span></li>
    <li><b>Cut &amp; finish</b><span>Routed, drilled and carved, then sanded, sealed or painted if you need it.</span></li>
    <li><b>Pick up or delivery</b><span>Local pickup at the shop or delivery around the Hudson Valley.</span></li>
  </ol>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Recent work</span><h2>Made in the Hudson Valley</h2></div>
  <div class="grid g3">{feats}</div>
  <p style="margin-top:28px"><a href="projects.html"><b>See all projects &rarr;</b></a></p>
</div></section>

<section class="tight" style="background:var(--panel)"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Materials</span><h2>What we cut</h2></div>
  {materials()}
</div></section>

<section><div class="wrap split">
  <div class="media">{img("panel-dados", "Plywood panels with routed dados on the router bed")}</div>
  <div class="copy"><span class="eyebrow">Serving the Hudson Valley</span><h2>Local shop, industrial capacity</h2>
  <p>We&#8217;re on Crispell Lane, between New Paltz and Gardiner, under the Shawangunk Ridge. Homeowners, contractors, architects, sign shops, artists, towns and manufacturers send us work from New Paltz, Gardiner, Highland, Rosendale, Kingston, Poughkeepsie, Newburgh and across Ulster, Dutchess and Orange counties, and down to New York City.</p>
  <ul class="ticks"><li>Pressure rollers flatten warped construction plywood for accurate cuts</li><li>Vacuum hold-down for fast, clean sheet processing</li><li>Hundreds of tools in stock, including PCD diamond tooling</li></ul>
  {cta_row()}</div>
</div></section>'''


def materials():
    m = [('Wood &amp; plywood', 'Hardwoods (oak, walnut, maple, cherry), Baltic birch, cabinet-grade and construction plywood, MDF (standard, moisture-resistant, formaldehyde-free, fire-rated), bamboo plywood.'),
         ('Plastics &amp; acrylics', 'Acrylic, polycarbonate, HDPE and two-color sign HDPE, LDPE, marine board (Polywood), nylon, PVC board.'),
         ('Architectural', 'HPL laminate, phenolic, solid surface, ACM (aluminum composite), aluminum sheet, fiber cement (HardieBoard).'),
         ('Sign &amp; carving', 'HDU and sign foam for carved and dimensional signs, plus carbon fiber for specialty parts.')]
    return '<div class="mat">' + ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in m) + '</div>'


# ---------------------------------------------------------------- SERVICES
def services():
    S = [
        ('arch', 'relief-carving-3', 'Carved white relief panels', 'Architectural &amp; commercial',
         'Feature walls, carved and fluted panels, screens, reception desks, store fixtures and millwork for architects, designers and general contractors.',
         ['Carved, fluted, slotted and acoustic wall panels', 'Decorative screens and room dividers', 'Store fixtures, slat walls and displays', 'Millwork parts, furniture and casework components (we cut the parts; we don&#8217;t build full cabinets)']),
        ('prod', 'crates-on-table', 'Plywood crate parts nested on the router', 'Products &amp; production runs',
         'Repeatable parts for makers and manufacturers. We nest parts tightly to save material and keep programs on file for reorders.',
         ['Product parts and flat-pack kits', 'Prototypes and short runs', 'Batch and repeat production', 'Jigs, fixtures and templates']),
        ('signs', 'trail-signs', 'Carved wood trail signs', 'Signs, trails &amp; community',
         'Carved and routed signs in wood, HDU and two-color HDPE, from single trail markers to full storefront systems.',
         ['Trail markers and park signs', 'Business and storefront signs', 'Dimensional letters and logos', 'Plaques, donor walls and memorials']),
        ('carve', 'relief-carving', '3D relief carving', '3D carving &amp; parametric design',
         '3D relief carving from models or scans, rotary 4th-axis work, and parametric pieces built from CNC-cut profiles.',
         ['3D relief and sculptural carving', 'Parametric wall art and furniture', 'Terrain and topographic models', 'Rotary carving for posts, columns and turned parts']),
        ('slabs', 'slab-flattening', 'Live-edge slab being flattened on the router', 'Slab flattening &amp; wood processing',
         'Big live-edge slabs flattened on the router and cut to a traced outline, for tables, counters and bar tops.',
         ['Slab flattening and surfacing', 'Profile cutting from a traced outline', 'Edge profiles and joinery', 'Inlays and resin pockets']),
        ('cad', 'plywood-nesting', 'Plywood parts nested for cutting', 'Design &amp; CAD support',
         'Send a napkin sketch or a finished shop drawing. We&#8217;ll draw it, fix it for CNC, nest it and tell you what it costs before we cut.',
         ['Vectorizing sketches, photos and logos', 'Converting shop drawings for CNC', 'Nesting to cut material cost', '3D modeling for carving']),
    ]
    rows = ''.join(f'<div class="svc" id="{i}">{img(im, a)}<div class="copy"><h2>{t}</h2><p class="lede">{d}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in li)}</ul></div></div>' for i, im, a, t, d, li in S)
    return f'''
<header class="page-head"><div class="wrap"><span class="eyebrow">Services</span><h1>What we make</h1>
<p class="lede">CNC routing, drilling, carving and engraving for builders, designers, artists and businesses. Every job runs on our 5&#8242; &times; 10&#8242; automatic tool-change router.</p>
<div class="jump">{''.join(f'<a href="#{i}">{t}</a>' for i, _, _, t, _, _ in S)}</div></div></header>
<section class="tight"><div class="wrap">{rows}</div></section>
<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Capabilities</span><h2>The toolbox</h2></div>
  <div class="grid g2">
    <ul class="ticks"><li>CNC routing and 2D profiling</li><li>Drilling, boring and hardware holes</li><li>Nesting and cutting full sheets</li><li>Pocketing, dados and rabbets</li><li>V-carving and engraving</li></ul>
    <ul class="ticks"><li>3D relief carving</li><li>Rotary 4th-axis carving</li><li>Inlays and dimensional letters</li><li>Slab flattening</li><li>Prototypes to production runs</li></ul>
  </div>
</div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Materials</span><h2>What we cut</h2></div>{materials()}</div></section>'''


# ---------------------------------------------------------------- PANELS
def panels():
    data = json.load(open(os.path.join(HERE, 'panels.json')))
    series = []
    for d in data:
        if d['series'] not in series: series.append(d['series'])
    slug = lambda s: s.lower().replace(' & ', '-').replace(' ', '-')
    out = ''
    for s in series:
        cards = ''.join(f'''<article class="pcard" id="{d['code']}"><img src="img/panels/{d['code']}.jpg" alt="{E(d['name'])} panel pattern" loading="lazy" data-full="img/panels/{d['code']}.jpg">
<span class="code">{d['code']}</span><h3>{E(d['name'])}</h3><p>{E(d['blurb'])}</p><p class="mono" style="font-size:.78rem">{E(d['depth'])}</p>
<a href="contact.html?design={d['code']}">Request this design &rarr;</a></article>''' for d in data if d['series'] == s)
        out += f'<div class="series-head" id="{slug(s)}"><h2>{s}</h2><span class="eyebrow">{sum(1 for d in data if d["series"] == s)} designs</span></div><div class="grid catalog">{cards}</div>'
    other = [('3D word clouds &amp; dimensional signage', 'Stacked 3D letters, logos and lobby signs.', 'weldwood-sign'),
             ('Barn &amp; sliding doors', 'Carved, grooved and patterned door panels.', 'walnut-slab'),
             ('Inlays &amp; engraving', 'Engraved panels, plaques, logos and awards.', 'library-plaque-detail'),
             ('Carved architectural details', 'Dentil molding, corbels, brackets and gable trim.', 'mahogany-strip')]
    ot = ''.join(f'<div class="tile">{img(i, t)}<h3>{t}</h3><p>{d}</p></div>' for t, d, i in other)
    return f'''
<header class="page-head"><div class="wrap"><span class="eyebrow">Panels &amp; products</span><h1>Panel collection</h1>
<p class="lede">{len(data)} carved, fluted, flexible and acoustic panel designs and decorative screens, cut to order in our New Paltz shop. Any design can be scaled, deepened, recolored or run seamlessly across a whole wall. Custom patterns welcome.</p>
<div class="hero-actions"><a class="btn" href="Hudson-Valley-CNC-Panel-Catalog.pdf">Download the catalog (PDF)</a><a class="btn ghost" href="contact.html">Ask about a custom pattern</a></div>
<div class="jump">{''.join(f'<a href="#{slug(s)}">{s}</a>' for s in series)}</div></div></header>
<section class="tight"><div class="wrap">
<div class="table-wrap"><table class="spec-table"><tbody>
<tr><th>Sizes</th><td>4&#8242; &times; 8&#8242; standard, or single panels up to 5&#8242; &times; 10&#8242; with no seams</td></tr>
<tr><th>Thickness</th><td>1/2&quot; to 1-1/2&quot;; most carved designs in 3/4&quot;</td></tr>
<tr><th>Materials</th><td>MDF (standard, moisture-resistant, NAUF, fire-rated), plywood, hardwoods, bamboo ply, PVC, HDU, acrylic, HPL</td></tr>
<tr><th>Finishes</th><td>Raw, primed, painted, stained or clear-coated; screens can be backlit</td></tr>
<tr><th>Flexible &amp; acoustic</th><td>Kerf-cut and tambour panels bend around curves; felt backing for acoustic designs</td></tr>
</tbody></table></div>
{out}
<p class="eyebrow" style="margin-top:32px">Catalog images are digital renderings. Wood grain, color and finish vary. Samples on request.</p>
</div></section>
<section style="background:var(--panel)"><div class="wrap"><div class="sec-head"><span class="eyebrow">More products</span><h2>Beyond panels</h2></div><div class="grid g4">{ot}</div></div></section>'''


# ---------------------------------------------------------------- CONTRACTORS
def contractors():
    ideas = [
        ('Panel cutting &amp; drilling', 'Cut-to-size sheet goods, nested parts, hole patterns and hardware boring, dados and rabbets. Pressure rollers hold warped construction plywood flat. We don&#8217;t build full cabinets, but we&#8217;ll cut and drill any panel you need.'),
        ('Carved architectural details', 'Dentil molding, corbels, brackets, rosettes, cornice and frieze details, and restoration pieces matched from a sample or photo.'),
        ('Decorative roof &amp; exterior trim', 'Gable trim and vergeboards, scroll brackets, gable vents and louvers, rafter tails, finials and cupola parts, in wood, PVC trim board or HDU.'),
        ('Curved forms &amp; templates', 'Curved concrete and landscape forms, stair stringers, rafter and truss templates, routing templates and bending forms.'),
        ('Facade &amp; exterior panels', 'Fiber cement (HardieBoard), ACM and HPL panels cut and drilled for rainscreen and facade systems.'),
        ('Commercial interiors', 'Fluted and 3D wall panels, reception desk parts, store fixtures and slat walls. We&#8217;ve fabricated for retail store projects with Buxus Construction.'),
        ('Signage', 'Job-site signs and permanent signs for finished projects.'),
    ]
    cards = ''.join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in ideas)
    return f'''
<section class="hero dark" style="padding-bottom:clamp(40px,6vw,72px)"><div class="wrap hero-grid">
  <div class="hero-copy"><span class="eyebrow">For contractors &amp; builders</span><h1>Your CNC partner for the job site</h1>
  <p class="lede">Send drawings or a sketch. We cut, drill and carve it accurately on a 5&#8242; &times; 10&#8242; industrial router, so your crew just installs.</p>{cta_row()}</div>
  <figure class="hero-img">{img('curved-forms', 'CNC-cut curved plywood forms for a concrete walkway around a round house')}<figcaption>Curved forms, cut to radius</figcaption></figure>
</div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Ways contractors use us</span><h2>Jobs you can send out</h2></div><div class="grid g3">{cards}</div></div></section>
<section style="background:var(--panel)"><div class="wrap split">
  <div class="media">{img('nested-panels', 'Sheet of nested panels cut on the router')}</div>
  <div class="copy"><span class="eyebrow">Why send out your CNC work</span><h2>Less site time, less waste</h2>
  <ul class="ticks"><li>Repeatable accuracy on every part</li><li>Faster installs and fewer site cuts</li><li>Nested layouts that use less material</li><li>One-offs or full production runs</li><li>Local pickup or Hudson Valley delivery</li></ul></div>
</div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow">How to send us a job</span><h2>What we need</h2></div>
<div class="table-wrap"><table class="spec-table"><tbody>
<tr><th>Files</th><td>DXF, DWG, SVG, PDF, AI, shop drawings, or a photo or sample to match</td></tr>
<tr><th>Material</th><td>Yours or ours: plywood, MDF, PVC trim board, HDU, HPL, ACM, fiber cement and more</td></tr>
<tr><th>Quantity &amp; deadline</th><td>Tell us how many and when you need them; we&#8217;ll confirm a date with the quote</td></tr>
</tbody></table></div><div style="margin-top:28px">{cta_row()}</div></div></section>'''


# ---------------------------------------------------------------- ARTISTS
def artists():
    svc = [('Molds &amp; patterns', 'Masters and plugs for vacuum forming, fiberglass, silicone, resin, concrete and GFRC. Press and hump molds for ceramics. Foam and wax patterns for casting.'),
           ('Relief &amp; 3D sculpture', 'Bas-relief panels and sculptural forms from your 3D model, scan or STL, plus rotary 4th-axis carving.'),
           ('Photo carving &amp; engraving', 'A photograph turned into a carved relief or a V-carved engraving.'),
           ('Stipple &amp; halftone art', 'Images built from thousands of drilled dots of varying size; can be backlit.'),
           ('Layered &amp; multiplane art', 'Stacked wood or acrylic layers that create depth and shadow.'),
           ('Terrain &amp; topo models', 'Stacked or carved 3D maps of mountains, lakes, trails and properties.'),
           ('Lithophanes', 'Thin carved panels in white solid surface or acrylic that reveal a photo when backlit.'),
           ('Printmaking blocks', 'Woodcut and relief-print blocks at any size, stamps and letterpress blocks.'),
           ('Stencils &amp; templates', 'Durable mural stencils and repeatable templates.'),
           ('Inlay &amp; marquetry', 'V-carve inlays, resin pour pockets and mixed-material inlays.'),
           ('Props &amp; scenery', 'Carved foam, PVC and HDU props and set pieces for theater, film, cosplay and events.'),
           ('Panels, frames &amp; exhibition', 'Cradled painting panels, shaped canvases, profiled frames, pedestals and display mounts.'),
           ('Large-scale &amp; public art', 'Installation parts, flat-pack slotted sculptures, armatures and mural substrates.'),
           ('Tools for potters', 'Texture mats, stamps, and slump and hump molds.'),
           ('Instrument parts', 'Guitar bodies, necks, templates and inlays.'),
           ('String art boards', 'Precisely drilled pin patterns at any size.')]
    cards = ''.join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in svc)
    gal = [('relief-carving', '3D relief carving in white HDPE'), ('terrain-model', 'Shawangunk Ridge terrain model'),
           ('layered-portrait', 'Layered portrait artwork'), ('portrait-engraving', 'Engraved photo portrait on black panel'),
           ('prop-shield', 'Carved PVC prop shield'), ('dino-assembled', 'Giant plywood dinosaur kit, assembled')]
    g = ''.join(f'<figure class="proj">{img(n, a)}<figcaption><p>{a}</p></figcaption></figure>' for n, a in gal)
    return f'''
<header class="page-head"><div class="wrap"><span class="eyebrow">For artists &amp; makers</span><h1>Your vision, cut to scale</h1>
<p class="lede">We help artists, designers and makers turn sketches, digital files and ideas into finished work, from a single piece to a full edition or a large public installation. You stay the author. We&#8217;re the fabricator.</p>{cta_row()}</div></header>
<section class="tight"><div class="wrap"><div class="grid g3">{g}</div></div></section>
<section style="background:var(--panel)"><div class="wrap"><div class="sec-head"><span class="eyebrow">What we make for artists</span><h2>Ways to work with us</h2></div><div class="grid g4">{cards}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow">How we work with artists</span><h2>Test first, then cut</h2></div>
<ol class="steps"><li><b>Share your file</b><span>SVG, DXF, AI, PDF, STL/OBJ, a high-res image, or a sketch on paper.</span></li>
<li><b>Prep &amp; test</b><span>We help with CAD, vectorizing or 3D modeling and cut a sample in your material.</span></li>
<li><b>You approve</b><span>Adjust depth, scale or detail before the final cut.</span></li>
<li><b>Cut &amp; deliver</b><span>Cut, finished to your spec, packed or delivered.</span></li></ol></div></section>'''


# ---------------------------------------------------------------- PROJECTS
PROJECTS = [
    ('community signs', 'Gardiner Library Commemorative Brick Project', 'A live-edge display cut from locally sawn pine, carved and machined to re-mount the library\u2019s original brass donor plaques.', ['library-plaque', 'library-plaque-detail']),
    ('signs', 'Variable Movement storefront sign', 'Multi-panel sign carved from King ColorCore two-color HDPE, with a raised, layered logo panel. Weatherproof and never needs painting.', ['colorcore-sign', 'colorcore-sign-detail']),
    ('signs community', 'Trail and business signs', 'Carved signs for Full Circle Gardiner: The Living Room, Hudson Valley Trailworks, Trailunity and Trailside Lounge.', ['trail-signs']),
    ('signs', 'DAP Weldwood 100 Years', 'Layered dimensional anniversary sign with raised lettering and a framed walnut-look background.', ['weldwood-sign-2', 'weldwood-sign']),
    ('production', 'Plywood crate production run', 'A production run of branded plywood crates: parts nested on full sheets, cut, then assembled.', ['crates-stacked', 'crates-on-table', 'crate-white', 'crate-detail', 'crate-orange']),
    ('contractors', 'Curved forms for a round house', 'CNC-cut curved plywood forms for a concrete walkway around a round home.', ['curved-forms', 'curved-forms-2']),
    ('art carving', '3D relief carving', 'Large relief panels carved from a 3D model in white HDPE.', ['relief-carving-2', 'relief-carving', 'relief-carving-3']),
    ('art carving', 'Shawangunk Ridge terrain model', 'A 3D terrain model of the Shawangunk Ridge.', ['terrain-model']),
    ('furniture', 'Slatted plywood bench', 'A bench built from stacked, curved CNC-cut plywood profiles.', ['slat-bench']),
    ('furniture wood', 'Live-edge walnut slab', 'A walnut slab traced, flattened and cut to its final outline on the router.', ['walnut-slab-layout', 'walnut-slab', 'slab-flattening']),
    ('art', 'Layered portrait', 'Layered, cut-panel portrait artwork.', ['layered-portrait']),
    ('art', 'Engraved photo portrait', 'A photograph engraved into a black panel.', ['portrait-engraving']),
    ('art production', 'Giant plywood dinosaur kits', 'Slot-together dinosaur skeletons cut from plywood sheets.', ['dino-assembled', 'dino-parts']),
    ('art', 'Carved PVC prop shield', 'A cosplay prop carved in PVC with raised relief, then hand-painted.', ['prop-shield']),
    ('production wood', 'Walnut coasters', 'A batch of engraved walnut coasters, nested on one blank.', ['walnut-coasters']),
    ('production', 'Nested parts in production', 'Small parts nested tightly on full sheets for a production order.', ['plaques-production', 'plaques-sheet', 'plaques-routing']),
    ('art production', 'Instrument template', 'A guitar-body template cut from sheet stock.', ['instrument-template']),
    ('signs', 'Engraved plywood sign', 'V-carved lettering in Baltic birch.', ['reload-sign']),
]
CATS = [('all', 'All'), ('signs', 'Signs'), ('community', 'Community'), ('contractors', 'Contractors'), ('production', 'Production'),
        ('art', 'Art'), ('carving', '3D carving'), ('furniture', 'Furniture'), ('wood', 'Wood')]


def projects():
    chips = ''.join(f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in CATS)
    cards = ''
    for cat, t, d, ims in PROJECTS:
        th = ''
        if len(ims) > 1:
            th = '<div class="thumbs">' + ''.join(f'<img src="img/{i}-sm.jpg" data-sm="img/{i}-sm.jpg" data-full="img/{i}.jpg" alt="{E(t)}" loading="lazy">' for i in ims) + '</div>'
        link = next((s for s, v in CASES.items() if v['project'] == t), None)
        h = f'<a href="{link}">{E(t)}</a>' if link else E(t)
        more = f'<a href="{link}"><b>Read the project story &rarr;</b></a>' if link else ''
        cards += f'<article class="proj" data-cat="{cat}">{img(ims[0], t, cls="main")}{th}<span class="tag">{cat.split()[0]}</span><h3>{h}</h3><p>{E(d)}</p>{more}</article>'
    return f'''
<header class="page-head"><div class="wrap"><span class="eyebrow">Projects</span><h1>Recent work</h1>
<p class="lede">Real jobs from the shop, from one-off signs to production runs. Tap a photo to enlarge it.</p></div></header>
<section class="tight"><div class="wrap">
<div class="filters" data-filter-group="#proj-grid" role="group" aria-label="Filter projects">{chips}</div>
<div class="grid g3" id="proj-grid">{cards}</div></div></section>'''



# ---------------------------------------------------------------- CASE STUDY PAGES
CASES = {
 'full-circle-gardiner-signs.html': dict(
   project='Trail and business signs',
   title='Signs for Full Circle Gardiner',
   eyebrow='Project &middot; Signs &middot; Gardiner, NY',
   seo_title='Carved Signs for Full Circle Gardiner & The Living Room | Hudson Valley CNC',
   seo_desc='Hudson Valley CNC made the carved signs for Full Circle Gardiner, The Living Room, Hudson Valley Trailworks, Trailunity and Trailside Lounge at 297 Bruynswick Rd, Gardiner, NY.',
   lede='Carved signs for Full Circle, the community hub at 297 Bruynswick Road in Gardiner: The Living Room, Hudson Valley Trailworks, Trailunity and Trailside Lounge.',
   hero='trail-signs',
   body="""<p>Full Circle is a community gathering place in Gardiner, home to The Living Room music and events space, Gardiner Bakehouse, Benton Beer Garden, Daisy&#8217;s Ice Cream and the trails and natural playgrounds of Hudson Valley Trailworks. It&#8217;s run with a simple idea: help neighbors become neighbors again.</p>
<p>We made the signs that tie the place together: the sign for The Living Room, plus the signs for Hudson Valley Trailworks, Trailunity and Trailside Lounge. Each one is carved on our CNC router, so the lettering and logos come out crisp and every sign in the set matches.</p>
<p>Signs like these are a good example of what a small CNC shop can do for a local business: take an existing logo, turn it into a carved, dimensional sign, and make matching pieces for every space on a property so it reads as one place.</p>""",
   facts=[('Client', 'Full Circle Gardiner (Full Circle Commons)'), ('Location', '297 Bruynswick Rd, Gardiner, NY 12525'),
          ('Signs', 'The Living Room, Hudson Valley Trailworks, Trailunity, Trailside Lounge'), ('Process', 'CNC-carved lettering and logos')],
   gallery=['trail-signs'],
   links=[('Visit Full Circle Gardiner', 'https://www.fcgardiner.com/'), ('The Living Room events', 'https://www.fcgardiner.com/the-living-room'), ('Full Circle on Instagram', 'https://www.instagram.com/fullcirclegardiner/')],
   note='More photos of the installed signs coming soon.'),
 'gardiner-library-brick-project.html': dict(
   project='Gardiner Library Commemorative Brick Project',
   title='Gardiner Library Commemorative Brick Project',
   eyebrow='Project &middot; Community &middot; Gardiner, NY',
   seo_title='Gardiner Library Commemorative Brick Wall | Live-Edge Pine Donor Display | Hudson Valley CNC',
   seo_desc='A live-edge pine donor wall for the Gardiner Library, cut from local timber and CNC-machined to re-mount the original engraved brass commemorative brick plaques.',
   lede='A new home for the library&#8217;s commemorative brick plaques: a live-edge display cut from locally sawn pine and laid out to re-mount every original brass plaque.',
   hero='library-plaque',
   body="""<p>The Gardiner Library&#8217;s Commemorative Brick Project honors hundreds of donors, families and local businesses, each with an engraved brass plaque. The plaques needed a new, permanent home where people could read them again.</p>
<p>We built the display from <strong>locally cut live-edge pine</strong>, keeping the natural edge of the slab as the border. On the CNC router we carved the &#8220;Gardiner Library &middot; Commemorative Brick Project&#8221; title and laid out a precise grid so each <strong>original brass plaque re-mounts</strong> in an even, readable layout. The lettering is finished in gold to match the brass.</p>
<p>It now hangs at the library entrance, carved with &#8220;Made in Gardiner by Hudson Valley CNC&#8221; in the corner.</p>""",
   facts=[('Client', 'Gardiner Library'), ('Material', 'Locally cut live-edge pine'), ('Work', 'CNC-carved, gilded lettering; layout designed to re-mount the original brass plaques'),
          ('Where to see it', 'Gardiner Library entrance, Gardiner, NY')],
   gallery=['library-plaque', 'library-plaque-detail'],
   links=[],
   note=''),
}


def case_page(slug):
    c = CASES[slug]
    facts = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in c['facts'])
    gal = ''.join(f'<figure class="proj">{img(g, c["title"])}</figure>' for g in c['gallery'])
    links = ''.join(f'<a class="btn ghost" href="{u}" rel="noopener" target="_blank">{t}</a>' for t, u in c['links'])
    note = f'<p class="notice">{c["note"]}</p>' if c['note'] else ''
    return f"""
<header class="page-head"><div class="wrap"><span class="eyebrow">{c['eyebrow']}</span><h1>{c['title']}</h1><p class="lede">{c['lede']}</p></div></header>
<section class="tight"><div class="wrap split" style="align-items:start">
  <div class="copy">{c['body']}<div class="table-wrap"><table class="spec-table"><tbody>{facts}</tbody></table></div>
  {f'<div class="hero-actions">{links}</div>' if links else ''}{note}</div>
  <div class="media"><figure class="hero-img">{img(c['hero'], c['title'])}</figure></div>
</div></section>
{f'<section class="tight" style="background:var(--panel)"><div class="wrap"><div class="grid g2">{gal}</div></div></section>' if len(c['gallery']) > 1 else ''}
<section class="tight"><div class="wrap"><p><a href="projects.html"><b>&larr; All projects</b></a></p>
<div style="margin-top:20px">{cta_row()}</div></div></section>"""


# ---------------------------------------------------------------- ABOUT
def about():
    return f'''
<header class="page-head"><div class="wrap"><span class="eyebrow">About</span><h1>A fabrication shop in the Hudson Valley</h1>
<p class="lede">Hudson Valley CNC is a CNC routing and fabrication shop outside New Paltz, New York. We work with homeowners, small businesses, towns, contractors, architects, artists and manufacturers across the Hudson Valley and beyond.</p></div></header>
<section><div class="wrap split">
  <div class="copy"><h2>Built for real production</h2>
  <p>Our shop runs an industrial automatic tool-change router with a full 5&#8242; &times; 10&#8242; vacuum table. It swaps between 12 tools on its own mid-job, so parts that need drilling, pocketing, carving and profiling come off the table in one setup.</p>
  <p>That means consistent parts, fast turnaround, and the capacity for both a single carved sign and a run of hundreds.</p></div>
  <div class="media">{img('tool-rack', 'Gantry and 12-tool linear tool changer on our router')}</div>
</div></section>
<section class="dark"><div class="wrap split rev">
  <div class="media">{img('spindle-closeup', 'Spindle and dust shoe cutting a part')}</div>
  <div class="copy"><span class="eyebrow">Our machine</span><h2>STM1530C ATC router</h2>
  <div class="table-wrap"><table class="spec-table"><tbody>
  <tr><th>Cutting area</th><td>60&quot; &times; 120&quot; (1500 &times; 3000 mm)</td></tr>
  <tr><th>Z clearance</th><td>About 11.8&quot; (300 mm) of travel</td></tr>
  <tr><th>Spindle</th><td>9 kW (12 HP) HSD air-cooled, up to 24,000 RPM, ER32</td></tr>
  <tr><th>Tool changer</th><td>12-position linear automatic</td></tr>
  <tr><th>Hold-down</th><td>Full vacuum table plus pressure rollers for warped sheet goods</td></tr>
  <tr><th>Drives</th><td>Servo motors with reducers; rapids to about 50 m/min</td></tr>
  <tr><th>Extras</th><td>Stand-alone rotary 4th axis; PCD diamond tooling</td></tr>
  </tbody></table></div></div>
</div></section>
<section><div class="wrap split">
  <div class="copy"><h2>Our commitments</h2><ul class="ticks"><li>Clear quotes before we cut</li><li>Honest turnaround dates</li><li>Test cuts for anything new or delicate</li><li>Programs kept on file for fast reorders</li></ul>{cta_row()}</div>
  <div class="media">{img('machine-cutting', 'The router cutting a job in the shop')}</div>
</div></section>'''


# ---------------------------------------------------------------- FAQ
FAQ = [('What files do you accept?', 'DXF, DWG, SVG, AI and PDF for 2D work, and STL or OBJ for 3D carving. A sketch, photo or sample to match works too. We can draw it up.'),
       ('Can you help with design?', 'Yes. We can turn a sketch into a cut file, adjust your drawings for CNC, or design from scratch.'),
       ('What&#8217;s the largest piece you can cut?', 'Sheets up to 5&#8242; &times; 10&#8242; in one piece, and material up to about 8&quot;&ndash;12&quot; thick depending on the part.'),
       ('What materials do you cut?', 'Wood and plywood, MDF, plastics (acrylic, polycarbonate, HDPE, PVC and more), HPL, phenolic, solid surface, ACM, aluminum, fiber cement, sign foam and HDU.'),
       ('Do you do one-offs or only production?', 'Both: single pieces, prototypes and full production runs.'),
       ('Can I supply my own material?', 'Yes, or we can source it for you.'),
       ('How long does a job take?', 'It depends on the size of the job and our schedule. Tell us your deadline and we&#8217;ll give you a date with your quote.'),
       ('Do you paint, finish or install?', 'We can prime, paint and clear-coat many pieces, and can help arrange installation. Ask with your quote.'),
       ('Do you deliver?', 'Local pickup at our New Paltz shop, or delivery around the Hudson Valley.'),
       ('Do you build cabinets?', 'We don&#8217;t build full cabinets, but we&#8217;ll cut and drill any panels you need.'),
       ('How do I get a quote?', f'Use the <a href="contact.html">quote form</a> or call {PHONE}. Include drawings or photos, material, quantity and deadline.')]


def faq():
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''<header class="page-head"><div class="wrap"><span class="eyebrow">FAQ</span><h1>Common questions</h1></div></header>
<section class="tight"><div class="wrap" style="max-width:860px">{items}</div></section>'''


# ---------------------------------------------------------------- CONTACT
TYPES = ['Wall / 3D panels', 'Acoustic panels', 'Flexible panels', 'Decorative screens', 'Signage / 3D letters', 'Architectural details',
         'Contractor / construction', 'Artist / art fabrication', 'Displays / fixtures', 'Production run', 'Other']


def contact():
    if QUOTE_FORM_URL and not PREVIEW:
        form = f'<iframe src="{QUOTE_FORM_URL}" title="Request a quote form" style="width:100%;min-height:1400px;border:0"></iframe>'
    else:
        opts = ''.join(f'<option>{t}</option>' for t in TYPES)
        form = f'''<form class="form" id="quote" action="#" method="post">
<label>Name<input id="q-name" name="name" required autocomplete="name"></label>
<label>Email<input id="q-email" name="email" type="email" required autocomplete="email"></label>
<label>Phone<input id="q-phone" name="phone" type="tel" autocomplete="tel"></label>
<label>Company <small>(optional)</small><input id="q-company" name="company" autocomplete="organization"></label>
<label>Project type<select id="q-type" name="type">{opts}</select></label>
<label>Catalog design code <small>(optional)</small><input id="q-design" name="design" placeholder="e.g. HV-W01"></label>
<label>Material<input id="q-material" name="material"></label>
<label>Quantity &amp; size<input id="q-qty" name="quantity"></label>
<label class="full">Describe your project<textarea id="q-desc" name="description" required></textarea></label>
<label class="full">Drawings or photos <small>(DXF, DWG, SVG, AI, PDF, STL, JPG)</small><input id="q-files" name="files" type="file" multiple></label>
<div class="full"><button class="btn" type="submit">Send my request</button></div>
<p class="full notice" id="q-msg" hidden>Preview only: on the live site this is the Jotform quote form, and submissions are emailed to you. Call {PHONE} with questions.</p>
</form>
<script>document.getElementById('quote').addEventListener('submit',function(e){{e.preventDefault();document.getElementById('q-msg').hidden=false;}});</script>'''
    return f'''<header class="page-head"><div class="wrap"><span class="eyebrow">Contact</span><h1>Request a quote</h1>
<p class="lede">Tell us what you&#8217;re making. Include drawings or photos, the material, how many and when you need them. We usually reply within 1&ndash;2 business days.</p></div></header>
<section class="tight"><div class="wrap split" style="align-items:start">
  <div>{form}</div>
  <div class="copy"><h2>Shop</h2>
  <div class="table-wrap"><table class="spec-table"><tbody>
  <tr><th>Phone</th><td><a href="tel:{PHONE_TEL}">{PHONE}</a></td></tr>
  {f'<tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>' if EMAIL else ''}
  <tr><th>Address</th><td>{ADDRESS}<br>Visits by appointment</td></tr>
  <tr><th>Service area</th><td>Hudson Valley, Catskills and the NYC region; shipping for flat-pack parts</td></tr>
  </tbody></table></div>
  {img('gantry-detail', 'Router gantry and tool changer')}</div>
</div></section>'''


PAGES = {
    'index.html': ('Hudson Valley CNC | CNC Routing & Fabrication in New Paltz, NY', 'Industrial CNC routing, carving and fabrication in the Hudson Valley: signs, wall panels, architectural details, art fabrication and production runs on a 5x10 ATC router.', home),
    'services.html': ('Services | Hudson Valley CNC', 'CNC routing, drilling, 3D carving, slab flattening, signs, architectural panels and production runs in New Paltz, NY.', services),
    'panels.html': ('Panel Collection | Hudson Valley CNC', 'Carved, fluted, flexible and acoustic wall panels and decorative screens, cut to order in the Hudson Valley.', panels),
    'contractors.html': ('For Contractors | Hudson Valley CNC', 'CNC panel cutting and drilling, carved trim, curved forms and exterior details for contractors and builders.', contractors),
    'artists.html': ('For Artists | Hudson Valley CNC', 'CNC fabrication for artists: relief carving, molds, terrain models, props, stipple art, lithophanes and editions.', artists),
    'projects.html': ('Projects | Hudson Valley CNC', 'Signs, panels, furniture, art and production runs made at Hudson Valley CNC in New Paltz, NY.', projects),
    'about.html': ('About | Hudson Valley CNC', 'About Hudson Valley CNC and our STM1530C automatic tool-change CNC router.', about),
    'faq.html': ('FAQ | Hudson Valley CNC', 'Answers about files, materials, sizes, turnaround and quotes.', faq),
    'contact.html': ('Request a Quote | Hudson Valley CNC', 'Request a CNC fabrication quote from Hudson Valley CNC. Call 845-384-2994.', contact),
}

for _slug, _c in CASES.items():
    PAGES[_slug] = (_c['seo_title'], _c['seo_desc'], (lambda s=_slug: case_page(s)))
