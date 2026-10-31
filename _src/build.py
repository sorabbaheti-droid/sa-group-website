#!/usr/bin/env python3
"""Generates the Standard Alloys India inner pages from data.
Run from the repo root:  python3 _src/build.py
Home (standard-alloys/index.html) and the gateway (index.html) are hand-written; this script
keeps their footer in step through the <!--footer--> markers, and writes the site 404 page.
Path tokens in page bodies: ~R~ = path to standard-alloys/, ~A~ = path to the repo root."""
import os, html, json, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from catalogue import GRADES, GRADE_ORDER, FAMILIES, FAMILY_ORDER, CONTROL, CONTROL_VIDEO, ASK, IND_NAMES, PRODUCTS, BY_SLUG

OUT = 'standard-alloys'
SITE = 'https://sorabbaheti-droid.github.io/sa-group-website/'   # change to the live domain at launch
NAV = [('About', 'about/'), ('Capabilities', 'capabilities/'), ('Industries', 'industries/'),
       ('Products', 'products/'), ('Grades', 'grades/'), ('Quality', 'quality/'), ('Contact', 'contact/')]
MAIL = 'sales@standardalloysindia.com'
PHONE = '+91 145 269 5110'
TEL = 'tel:+911452695110'
ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IND = json.load(open(os.path.join(os.path.dirname(__file__), 'industries.json')))

def esc(s): return html.escape(s, quote=True)
def slug(s): return re.sub(r'-+', '-', ''.join(c if c.isalnum() else '-' for c in s.lower())).strip('-')
def mailto(subject): return f'mailto:{MAIL}?subject=' + subject.replace(' ', '%20').replace('’', '%27')

# family icons, drawn as simple line glyphs for parts not yet photographed
ICON = {
 'impact':  '<path d="M14 40h20M24 40V22M16 10h16l4 8H12z"/><circle cx="24" cy="30" r="3"/>',
 'jawcone': '<path d="M10 10l8 28h12l8-28M18 38l6-20 6 20"/>',
 'mill':    '<circle cx="24" cy="24" r="14"/><circle cx="24" cy="24" r="6"/><path d="M24 10v8M24 30v8M10 24h8M30 24h8"/>',
 'kiln':    '<path d="M24 8c6 8 10 12 10 19a10 10 0 01-20 0c0-4 2-7 4-9 0 4 2 6 4 6 0-6-2-10 2-16z"/>',
 'spares':  '<circle cx="24" cy="24" r="9"/><path d="M24 8v5M24 35v5M8 24h5M35 24h5M12.7 12.7l3.6 3.6M31.7 31.7l3.6 3.6M12.7 35.3l3.6-3.6M31.7 16.3l3.6-3.6"/>',
}
def placeholder(fam, big=False):
    return f'<div class="ph{" big" if big else ""}"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[fam]}</svg><span>Photograph on request</span></div>'

# ---------------------------------------------------------------- page shell
def header(r, a, active):
    ON = ' class="on" aria-current="page"'
    nav = ''.join(f'<a href="{r}{h}"{ON if l == active else ""}>{l}</a>' for l, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top solid" id="top">
  <div class="wrap">
    <a class="brand" href="{r}"><img src="{a}assets/saipl-logo.png" alt="" width="40" height="35">STANDARD ALLOYS INDIA</a>
    <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav id="nav" aria-label="Main">{nav}<a class="btn" href="{r}contact/#quote">Get a quote</a></nav>
  </div>
</header>'''

def footer(r, a):
    fams = ''.join(f'<a href="{r}products/#{k}">{FAMILIES[k]["name"]}</a>' for k in FAMILY_ORDER)
    inds = ''.join(f'<a href="{r}industries/{i["slug"]}/">{i["name"]}</a>' for i in IND)
    co = ''.join(f'<a href="{r}{h}">{l}</a>' for l, h in [('About us', 'about/'), ('Capabilities', 'capabilities/'), ('Quality', 'quality/'), ('Materials and grades', 'grades/'), ('Sustainability', 'sustainability/'), ('Careers', 'careers/'), ('Contact', 'contact/')])
    return f'''<footer class="foot">
  <div class="wrap fgrid">
    <div class="fb">
      <a class="brand" href="{r}"><img src="{a}assets/saipl-logo.png" alt="" width="34" height="30">STANDARD ALLOYS INDIA</a>
      <p>Wear- and heat-resistant steel castings from 3 kg to 7 tonnes, engineered, cast and machined in India for plants worldwide.</p>
      <address>F-26B &amp; 27, Parbatpura Industrial Area<br>Ajmer 305002, Rajasthan, India</address>
      <p class="fc"><a href="{TEL}">{PHONE}</a><a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <nav aria-label="Products"><h2>Products</h2>{fams}<a href="{r}products/">All products</a></nav>
    <nav aria-label="Industries"><h2>Industries</h2>{inds}</nav>
    <nav aria-label="Company"><h2>Company</h2>{co}</nav>
  </div>
  <div class="wrap fbot"><span>© 2026 Standard Alloys India Pvt. Ltd.</span><span>ISO 9001:2015 · ISO 14001:2015 · ISO 45001:2018</span></div>
</footer>'''

def head(title, desc, r, a, extra=''):
    full = title if 'Standard Alloys India' in title else f'{title} · Standard Alloys India'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0d0d0e">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Standard Alloys India">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{a}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}sai.css">{extra}'''

def page(path, title, desc, active, body, js='', three=False, ld=None):
    depth = path.count('/') + 1 if path else 0
    r = '../' * depth              # to standard-alloys/
    a = '../' * (depth + 1)        # to repo root (assets)
    tok = lambda s: s.replace('~R~', r).replace('~A~', a)
    imap = '\n<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>' if three else ''
    ldj = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    doc = f'''<!doctype html>
<html lang="en">
<head>
{head(title, desc, r, a, imap + ldj)}
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{header(r, a, active)}
<main id="main">
{tok(body)}
</main>
<a class="sidetab" href="{r}contact/#quote">Get a quote</a>
{footer(r, a)}
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
<script>{COMMON_JS}</script>
{f'<script src="{a}assets/js/rfq.js"></script>' if 'data-rfq' in body else ''}
{('<script type="module">' + tok(js) + '</script>') if js else ''}
</body>
</html>
'''
    full = os.path.join(OUT, path, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)
    print('wrote', full)

COMMON_JS = r'''
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, LITE = /lite/.test(location.search);
if (LITE) document.querySelectorAll('video').forEach(v => { v.removeAttribute('autoplay'); v.pause(); });
gsap.registerPlugin(ScrollTrigger); gsap.ticker.lagSmoothing(0);
let lenis;
if (!reduce && !LITE) { lenis = new Lenis({ lerp: .1 }); lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); }
document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href'); if (id.length < 2) return; const t = document.querySelector(id); if (t && lenis) { e.preventDefault(); lenis.scrollTo(t, { offset: -150 }); } }));
const mb = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
mb.addEventListener('click', () => { const o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });
addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); mb.setAttribute('aria-expanded', false); mb.focus(); } });
/* videos play only on screen */
if (!LITE) { const io = new IntersectionObserver(es => es.forEach(e => { const v = e.target; if (e.isIntersecting && !reduce) { v.preload = 'auto'; v.play().catch(() => {}); } else v.pause(); }), { rootMargin: '120px' });
  document.querySelectorAll('video').forEach(v => io.observe(v)); }
/* process line follows the reader */
const steps = [...document.querySelectorAll('.step')], items = [...document.querySelectorAll('.line li:not(.fill)')], fill = document.getElementById('fill');
if (fill) steps.forEach((s, i) => ScrollTrigger.create({ trigger: s, start: 'top 55%', end: 'bottom 55%', onToggle: st => { if (!st.isActive) return;
  items.forEach((li, k) => { li.classList.toggle('done', k < i); li.classList.toggle('now', k === i); });
  fill.style.width = `calc(${i / Math.max(1, items.length - 1)} * (100% - 2 * var(--gut) - ${100 / items.length}%))`; } }));
/* in-page tabs on product pages */
const tabs = [...document.querySelectorAll('.ptabs a')];
tabs.forEach(t => { const sec = document.querySelector(t.getAttribute('href')); if (sec) ScrollTrigger.create({ trigger: sec, start: 'top 60%', end: 'bottom 60%', onToggle: st => st.isActive && tabs.forEach(x => x.classList.toggle('on', x === t)) }); });
/* statements light up word by word */
document.querySelectorAll('.lit').forEach(p => {
  p.innerHTML = p.textContent.trim().split(/\s+/).map(x => `<span class="w">${x}</span>`).join(' ');
  const ws = [...p.querySelectorAll('.w')];
  if (reduce) { ws.forEach(w => w.classList.add('on')); return; }
  ScrollTrigger.create({ trigger: p, start: 'top 85%', end: 'bottom 45%', scrub: true, onUpdate: st => { const n = Math.round(st.progress * ws.length); ws.forEach((w, i) => w.classList.toggle('on', i < n)); } });
});
/* counters */
document.querySelectorAll('[data-count]').forEach(b => { const end = +b.dataset.count, dec = +(b.dataset.dec || 0); if (reduce) return; const o = { v: 0 };
  ScrollTrigger.create({ trigger: b, start: 'top 90%', once: true, onEnter: () => gsap.to(o, { v: end, duration: 1.6, ease: 'power3.out', onUpdate: () => b.textContent = o.v.toLocaleString('en-IN', { minimumFractionDigits: dec, maximumFractionDigits: dec }) }) }); b.textContent = (0).toFixed(dec); });
/* ERPNext web form slots */
document.querySelectorAll('[data-webform]').forEach(s => { if (s.dataset.webform) s.innerHTML = `<iframe src="${s.dataset.webform}" title="${s.dataset.title || 'Form'}"></iframe>`; });
/* range bars fill when seen */
document.querySelectorAll('.bar i').forEach(b => { if (reduce) return; gsap.from(b, { scaleX: 0, transformOrigin: 'left', duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: b, start: 'top 92%', once: true } }); });
/* manufacturing chain draws in; product cards lean toward the pointer */
document.querySelectorAll('.mtrack').forEach(t => { if (reduce) { t.classList.add('in'); return; } ScrollTrigger.create({ trigger: t, start: 'top 85%', once: true, onEnter: () => t.classList.add('in') }); });
if (matchMedia('(hover:hover)').matches && !reduce) document.querySelectorAll('.pcard:not(.noimg) .pic img').forEach(img => { const c = img.closest('.pcard');
  c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); img.style.transform = `scale(1.07) rotateY(${((e.clientX - r.left) / r.width - .5) * 14}deg) rotateX(${-((e.clientY - r.top) / r.height - .5) * 14}deg)`; });
  c.addEventListener('pointerleave', () => img.style.transform = ''); });
if (!reduce) {
  gsap.from('.ihero h1 .ln > span', { yPercent: 105, duration: 1.1, ease: 'power4.out', delay: .15 });
  gsap.from('.ihero .crumbs, .ihero p:not(.crumbs)', { y: 18, opacity: 0, duration: .9, ease: 'power3.out', stagger: .1, delay: .35 });
  gsap.from('.phero .reveal', { y: 26, opacity: 0, duration: 1, ease: 'power3.out', stagger: .07, delay: .1 });
  gsap.from('.phero .pvis', { scale: .94, opacity: 0, duration: 1.3, ease: 'power3.out', delay: .2 });
  gsap.to('.ihero video', { yPercent: 12, scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.ihero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.utils.toArray('[data-r]').forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
  ScrollTrigger.batch('.pcard', { start: 'top 94%', once: true, onEnter: b => gsap.from(b, { y: 28, opacity: 0, duration: .8, ease: 'power3.out', stagger: .05, clearProps: 'transform,opacity' }) });
} else document.querySelectorAll('[data-r]').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; });
'''

def hero(crumb, h1, lede, video, short=False):
    return f'''<section class="ihero{' short' if short else ''}" aria-labelledby="h1">
  <video src="~A~assets/media/{video}.mp4" poster="~A~assets/media/{video}.jpg" muted loop playsinline autoplay aria-hidden="true"></video>
  <div class="in wrap">
    <p class="crumbs"><a href="~R~">Home</a> / {crumb}</p>
    <h1 id="h1"><span class="ln"><span>{h1}</span></span></h1>
    <p>{lede}</p>
  </div>
</section>'''

def cta(title='Have a casting problem? Send it to us', sub='A drawing, photographs of the worn part, or just the equipment model: any of them is enough to start. Our metallurgists recommend the grade if you don’t know it.', subject='Request for quotation'):
    return f'''<section class="cta" id="contact" aria-labelledby="cta-h">
  <div class="wrap narrow" data-r>
    <h2 id="cta-h">{title}</h2>
    <p>{sub}</p>
    <div class="acts"><a class="btn" href="~R~contact/#quote">Get a quote</a><a class="btn ghost" href="{mailto(subject)}">Discuss your part by email</a></div>
  </div>
</section>'''

def gnames(p): return ', '.join(GRADES[g]['short'] for g, _ in p['grades'])

def pcard(p, mode='where'):
    """A product card that links to the product page. mode: 'where' (catalogue) or 'fails' (industry pages)."""
    fam = p['fam']
    pic = f'<div class="pic"><img src="~A~assets/cutouts/{p["img"]}.png" alt="" loading="lazy"></div>' if p['img'] else f'<div class="pic type" aria-hidden="true"><span>{p["name"]}</span></div>'
    if mode == 'fails':
        body = f'<dl><dt>Fails by</dt><dd>{p["fails"][0][0]}</dd><dt>Usual grade</dt><dd>{gnames(p)}</dd></dl>'
    else:
        body = f'<p>{p["where"]}</p><span class="g">{gnames(p)}</span>'
    return f'''<a class="pcard{'' if p['img'] else ' noimg'}" href="~R~products/{p['slug']}/" data-fam="{fam}" data-ind="{' '.join(p['inds'])}" data-s="{esc(p['search'])}">{pic}<div class="b"><span class="fam">{FAMILIES[fam]['name']}</span><h3>{p['name']}</h3>{body}</div><i class="go" aria-hidden="true">{ARROW}</i></a>'''


# ---------------------------------------------------------------- shared conversion blocks
def rfq_html(title='Get a quote, or discuss your part'):
    return f"""<div class="rfqwrap">
  <div class="routes">
    <div><b>Have a drawing?</b>Attach it as PDF, DWG, DXF or STEP.</div>
    <div><b>No drawing?</b>Send photographs of the part with key dimensions.</div>
    <div><b>Only know the equipment?</b>Tell us the OEM, the model and what the part does.</div>
  </div>
  <form class="rfqf" data-rfq novalidate aria-label="{title}">
    <fieldset><legend><span>1</span>What part do you need?</legend>
      <input name="part" aria-label="Part" placeholder="For example: mantle for a cone crusher" required>
      <div class="have" role="group" aria-label="What you can send"><span>I can send:</span><button type="button">A drawing</button><button type="button">Photographs</button><button type="button">The worn part</button><button type="button">Only the model</button></div>
    </fieldset>
    <fieldset><legend><span>2</span>Where does it work?</legend>
      <input name="equip" aria-label="Equipment, OEM and model" placeholder="Equipment, OEM and model">
    </fieldset>
    <fieldset><legend><span>3</span>Material, quantity and condition</legend>
      <div class="row"><input name="grade" aria-label="Material or grade" placeholder="Material or grade, if known"><label class="ck"><input type="checkbox" name="rec" checked> Don’t know: please recommend</label></div>
      <div class="row"><input name="qty" aria-label="Quantity" placeholder="Quantity, for example 2 sets a year"><div class="seg" role="group" aria-label="Condition"><button type="button" data-c="As cast">As cast</button><button type="button" data-c="Machined">Machined</button><button type="button" data-c="Not sure" class="on">Not sure</button></div></div>
      <textarea name="notes" aria-label="Notes" rows="2" placeholder="How it fails today, or anything else we should know (optional)"></textarea>
    </fieldset>
    <fieldset><legend><span>4</span>Your details</legend>
      <div class="row"><input name="name" aria-label="Name" placeholder="Name" autocomplete="name"><input name="company" aria-label="Company" placeholder="Company" autocomplete="organization"></div>
      <div class="row"><input name="email" type="email" aria-label="Email" placeholder="Email" autocomplete="email" required><input name="country" aria-label="Country" placeholder="Country" autocomplete="country-name"></div>
    </fieldset>
    <div class="sub"><button class="btn" type="submit">Prepare my enquiry</button><p class="msg" role="status">Incomplete details are fine. Your email app opens with everything filled in, so you can attach files before sending.</p></div>
  </form>
</div>"""

WHY = [('35+', 'years', 'Foundry experience in Ajmer, since 1991.'),
       ('~14,000', 't a year', 'Installed capacity across our three Ajmer facilities.'),
       ('3 kg–7 t', '', 'Single pieces, with up to 10 tonnes of metal in one pour.'),
       ('500+', 'customers', 'Industrial customers in cement, mining, aggregate, power and steel.'),
       ('10,000+', 'patterns', 'Already on file, so repeat orders start at moulding.'),
       ('End to end', '', 'Method, patterns, melting, moulding, heat treatment and machining in our own plants.'),
       ('UT · MPI · DPT', '', 'With spectrometer, microstructure, tensile, impact and hardness testing.'),
       ('Worldwide', '', 'Export packing, material certificates, dimensional and NDT reports.')]
def why_html():
    li = ''.join(f'<li data-r><b>{a}{(" <small>" + u + "</small>") if u else ""}</b><span>{t}</span></li>' for a, u, t in WHY)
    return f"""<section class="whysa" id="why" aria-labelledby="why-sa"><div class="wrap">
  <div class="sh" data-r><h2 id="why-sa">Why trust us with a critical casting</h2><p>Because the part, its grade and every step that decides its life are in one set of hands, and every heat is tested before it ships.</p></div>
  <ul class="proof">{li}</ul>
</div></section>"""

CHAIN2 = [('Engineering', 'Drawing review, or reverse engineering from the worn part'),
          ('Method and simulation', 'Gating and feeding designed; critical parts simulated*'),
          ('Pattern and tooling', 'Wood, polystyrene and aluminium patterns'),
          ('Melting', 'Induction furnaces, chemistry checked every heat'),
          ('Moulding', 'Alphaset no-bake moulds'),
          ('Casting', 'Single pieces from 3 kg to 7 tonnes'),
          ('Heat treatment', 'Water, oil or air quench; tempering'),
          ('Machining', 'Vertical lathes, machining centres, plano miller'),
          ('NDT and inspection', 'UT, MPI, DPT, hardness and dimensions'),
          ('Dispatch', 'Reports traceable to the heat, packed for export')]
def chain_html():
    li = ''.join(f'<li><i>{k:02d}</i><b>{a}</b><span>{b}</span></li>' for k, (a, b) in enumerate(CHAIN2, 1))
    return f"""<section class="mchain" aria-labelledby="mc-h"><div class="wrap">
  <div class="sh" data-r><h2 id="mc-h">One supplier. One manufacturing chain. One responsibility.</h2><p>From your problem to the finished part, every step that decides the life of a casting is ours to control, and ours to answer for.</p></div>
  <div class="mtrack"><ol>{li}</ol></div>
  <p class="note">*Casting simulation for critical parts is run with a specialist partner; method design is in-house.</p>
</div></section>"""

DONTKNOW = '<aside class="dk" data-r><b>Don’t know which alloy you need?</b><p>Send the existing part, its drawing, photographs or the application details. Our metallurgists will recommend the grade and the manufacturing route.</p><a href="~R~contact/#quote">Ask a metallurgist</a></aside>'

EXPORT = """<section class="psec soft" aria-labelledby="ex-h"><div class="wrap ex">
  <div data-r><div class="sh"><h2 id="ex-h">For buyers outside India</h2><p>We ship to plants anywhere in the world. Every export order travels with the documents your receiving inspection and customs need.</p></div></div>
  <ul class="exl" data-r><li><b>Material certificates</b>Chemistry and mechanical properties against the heat number</li><li><b>Dimensional reports</b>Checked against your drawing</li><li><b>NDT reports</b>UT, MPI or DPT, as specified</li><li><b>Export packing</b>Packed and marked for sea or air freight</li><li><b>Commercial documents</b>Invoice, packing list and certificate of origin</li><li><b>Lead time</b>Confirmed with the quotation, and faster when the pattern is already on file</li></ul>
</div></section>"""

# ---------------------------------------------------------------- industries
for ind in IND:
    line = ''.join(f'<li><a href="#{s["id"]}"><i></i>{s["label"]}</a></li>' for s in ind['steps'])
    secs = ''
    for k, s in enumerate(ind['steps'], 1):
        duty = ''.join(f'<span class="hot">{d[1:]}</span>' if d.startswith('!') else f'<span>{d}</span>' for d in s['duty'])
        if 'parts' in s:
            grid = '<div class="pcards">' + ''.join(pcard(BY_SLUG[x], 'fails') for x in s['parts']) + '</div>'
        else:
            grid = '<ol class="proc">' + ''.join(f'<li data-r><b>{a}</b><span>{b}</span></li>' for a, b in s['items']) + '</ol>'
        secs += f'''<section class="step" id="{s['id']}" aria-labelledby="s{k}">
  <div class="wrap">
    <div class="step-head">
      <div><span class="n">Stage {k}</span><h2 id="s{k}">{s['name']}</h2></div>
      <div><p>{s['text']}</p><div class="duty">{duty}</div></div>
    </div>
    {grid}
  </div>
</section>'''
    why = ''.join(f'<li data-r><b>{b}</b>{t}</li>' for b, t in ind['why'])
    body = hero(f'<a href="~R~industries/">Industries</a> / {ind["name"]}', ind['name'], ind['lede'], ind['video']) + f'''
<nav class="line" aria-label="{ind['name']} stages" style="--n:{len(ind['steps'])}"><ol><li class="fill" id="fill" aria-hidden="true"></li>{line}</ol></nav>
<section class="intro"><div class="wrap narrow" data-r><p>{ind['intro']}</p></div></section>
{secs}
<div class="wrap">{DONTKNOW}</div>
<section class="why" aria-labelledby="why-h"><div class="wrap"><div class="narrow" data-r><h2 id="why-h">{ind['why_title']}</h2></div><ul>{why}</ul></div></section>
''' + cta(subject=f'Request for quotation: {ind["name"].lower()} part')
    page(f'industries/{ind["slug"]}', f'{ind["name"]} castings', ind['desc'], 'Industries', body)

tiles = ''.join(f'''<a class="tile" href="~R~industries/{i['slug']}/" data-r><video src="~A~assets/media/{i['tile']}.mp4" poster="~A~assets/media/{i['tile']}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><div class="t"><h3><i>{ARROW}</i>{i['name']}</h3><p>{i['tile_text']}</p></div></a>''' for i in IND)
page('industries', 'Industries', 'Castings for cement, mining, aggregate, thermal power and steel plants, and for the equipment makers who build them.', 'Industries',
     hero('Industries', 'Industries we serve', 'Parts for equipment that runs around the clock, where one early failure stops a whole line.', 'mining') +
     f'<section class="sectors"><div class="tiles" style="margin-top:0">{tiles}</div></section>' + cta())

# ---------------------------------------------------------------- products A–Z
chips = '<button class="chip on" data-f="all" aria-pressed="true">All</button>' + ''.join(f'<button class="chip" data-f="{k}" aria-pressed="false">{FAMILIES[k]["name"]}</button>' for k in FAMILY_ORDER)
opts = '<option value="all">All industries</option>' + ''.join(f'<option value="{k}">{v}</option>' for k, v in IND_NAMES.items())
fsecs = ''
for k in FAMILY_ORDER:
    ps = [p for p in PRODUCTS if p['fam'] == k]
    fsecs += f'''<section class="fam" id="{k}" data-fam="{k}" aria-labelledby="f-{k}">
  <div class="fam-h"><h2 id="f-{k}">{FAMILIES[k]['name']}</h2><p>{FAMILIES[k]['text']}</p></div>
  <div class="pcards">{''.join(pcard(p) for p in ps)}</div>
</section>'''
page('products', 'Products', 'Every wear- and heat-resistant part we cast, searchable by type of casting.', 'Products',
     hero('Products', 'Products', f'{len(PRODUCTS)} parts in five families. Search by type of casting, or browse by industry.', 'rings') + f'''
<section class="catalogue"><div class="wrap">
  <form class="bigsearch" role="search" onsubmit="return false" data-r>
    <label for="q">Search by type of casting</label>
    <div class="bs"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><input id="q" type="search" placeholder="Try: jaw plate, mantle, blow bar, dip tube, grate plate" autocomplete="off"></div>
    <p class="eg">Popular: <button type="button">Jaw plate</button><button type="button">Mantle</button><button type="button">Bowl liner</button><button type="button">VRM roller</button><button type="button">Dip tube</button><button type="button">Grate plate</button></p>
  </form>
  <div class="tools" data-r>
    <div class="chips" role="group" aria-label="Filter by family">{chips}</div>
    <label class="sel tool2"><span class="vh">Industry</span><select id="indf" aria-label="Filter by industry">{opts}</select></label>
  </div>
  <p class="count" id="count" aria-live="polite">{len(PRODUCTS)} parts</p>
  {fsecs}
  <div class="empty" id="empty" hidden><h3>No exact match, but we probably make it</h3><p>We cast to drawing, sample or sketch. Tell us the part and the equipment it fits, and a metallurgist will come back to you.</p><a class="btn" href="~R~contact/#quote">Get a quote for this part</a></div>
  <p class="after" data-r>Your part not listed? We cast to drawing, sample or sketch, with more than 10,000 patterns already on file.</p>
</div></section>''' + cta(),
     js=r'''const chips=[...document.querySelectorAll('.chip')], cards=[...document.querySelectorAll('.catalogue .pcard')], secs=[...document.querySelectorAll('.catalogue .fam')];
const indf=document.getElementById('indf'), q=document.getElementById('q'), count=document.getElementById('count'), empty=document.getElementById('empty');
let fam='all';
function apply(){const ind=indf.value, words=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);let n=0;
  cards.forEach(c=>{const ok=(fam==='all'||c.dataset.fam===fam)&&(ind==='all'||c.dataset.ind.split(' ').includes(ind))&&words.every(w=>c.dataset.s.includes(w));c.hidden=!ok;if(ok)n++;});
  secs.forEach(x=>x.hidden=!x.querySelector('.pcard:not([hidden])'));
  count.textContent=n+(n===1?' part':' parts')+(words.length?' for “'+q.value.trim()+'”':'');empty.hidden=n>0;ScrollTrigger.refresh();
  const u=new URL(location);words.length?u.searchParams.set('q',q.value.trim()):u.searchParams.delete('q');history.replaceState(null,'',u);}
chips.forEach(c=>c.addEventListener('click',()=>{fam=c.dataset.f;chips.forEach(x=>{x.classList.toggle('on',x===c);x.setAttribute('aria-pressed',x===c)});apply();}));
indf.addEventListener('change',apply);q.addEventListener('input',apply);
document.querySelectorAll('.eg button').forEach(b=>b.addEventListener('click',()=>{q.value=b.textContent;apply();q.focus();}));
const sp=new URLSearchParams(location.search);if(sp.get('q')){q.value=sp.get('q');}if(sp.get('ind')&&indf.querySelector('option[value="'+sp.get('ind')+'"]'))indf.value=sp.get('ind');
const h=location.hash.slice(1);if(document.querySelector('.chip[data-f="'+h+'"]'))document.querySelector('.chip[data-f="'+h+'"]').click();else apply();''')

# ---------------------------------------------------------------- product pages
FIN = [('cast', 'As cast'), ('machined', 'Machined'), ('primer', 'Primer')]
def hb_bar(g):
    """A small scale: Brinell range for wear grades, service temperature for heat-resistant grades."""
    G = GRADES[g]
    if 'temp' in G:
        rows = ''.join(f'<div class="bar t"><span class="lb">{n}</span><span class="tr"><i style="left:0;width:{t / 1200 * 100:.1f}%"></i></span><span class="v">≈{t:,} °C</span></div>' for n, t in G['temp'])
        return f'<div class="bars" role="img" aria-label="Typical service limit in oxidising atmospheres">{rows}<div class="ax"><span>0</span><span>600</span><span>1,200 °C</span></div></div>'
    lo, hi = G['hb']; L, H = 100, 750
    x = lambda v: (v - L) / (H - L) * 100
    extra = f'<b style="left:{x(hi):.1f}%;width:{x(G["hb_service"]) - x(hi):.1f}%" title="Work-hardened face in service"></b>' if G.get('hb_service') else ''
    v = f'{lo}–{hi} HB' + (f' · {G["hb_service"]}+ in service' if G.get('hb_service') else '')
    return f'<div class="bars" role="img" aria-label="Typical hardness {v}"><div class="bar"><span class="tr"><i style="left:{x(lo):.1f}%;width:{x(hi) - x(lo):.1f}%"></i>{extra}</span><span class="v">{v}</span></div><div class="ax"><span>100</span><span>400</span><span>750 HB</span></div></div>'

for p in PRODUCTS:
    fam = p['fam']; F = FAMILIES[fam]
    qhref = '~R~contact/?part=' + p['name'].replace(' ', '+') + '#quote'
    inds = ', '.join(f'<a href="~R~industries/{i}/">{IND_NAMES[i]}</a>' for i in p['inds'])
    gl = ', '.join(f'<a href="~R~grades/#{g}">{GRADES[g]["short"]}</a>' for g, _ in p['grades'])
    # visual: 3D model when we have one, the photograph otherwise, a placeholder last
    if p.get('m3d'):
        photo = f'<img class="alt" src="~A~assets/cutouts/{p["img"]}.png" alt="Photograph of {esc(p["name"].lower())}" hidden>' if p['img'] else ''
        ON1 = ' class="on"'
        fbtn = ''.join(f'<button type="button" data-f="{k}"{ON1 if k == "cast" else ""}>{l}</button>' for k, l in FIN)
        vbtn = '<button type="button" class="view" data-v="photo">Photograph</button>' if p['img'] else ''
        vis = f'''<div class="pvis three"><canvas id="p3d" data-part="{p['m3d']}" role="img" aria-label="Illustrative 3D model of {esc(p['name'].lower())}; drag to turn it"></canvas>{photo}
      <div class="vctl"><div class="finish" role="group" aria-label="Surface finish">{fbtn}</div>{vbtn}</div><small>Illustrative model · drag to turn</small></div>'''
    elif p['img']:
        vis = f'<div class="pvis"><img src="~A~assets/cutouts/{p["img"]}.png" alt="Photograph of {esc(p["name"].lower())}"></div>'
    else:
        vis = f'''<aside class="pvis none qcard"><span class="k">{F['name']}</span><h2>Get a quote for {p['name'].lower()}</h2><ul class="chk"><li>A drawing, photographs, or only the equipment model</li><li>Grade recommended if you don’t know it</li><li>As cast, or machined to drawing</li></ul><a class="btn" href="{qhref}">Get a quote</a><p>Or call <a href="{TEL}">{PHONE}</a></p></aside>'''
    fails = ''.join(f'<li data-r><span class="n">{i:02d}</span><b>{a}</b><span class="r">{b}</span></li>' for i, (a, b) in enumerate(p['fails'], 1))
    gcards = ''
    for i, (g, when) in enumerate(p['grades']):
        G = GRADES[g]
        tag = 'Usual choice' if i == 0 else 'Alternative'
        gcards += f'''<article class="gcard" data-r><span class="tag">{tag if len(p['grades']) > 1 else 'Our grade'}</span><h3><a href="~R~grades/#{g}">{G['name']}</a></h3><p class="when">{when}</p>{hb_bar(g)}<p class="std">{' · '.join(G['standards'])}</p></article>'''
    ctrl = ''.join(f'<li data-r><b>{a}</b>{b}</li>' for a, b in CONTROL[fam])
    ask = ''.join(f'<li>{x}</li>' for x in ASK)
    rel = [x for x in PRODUCTS if x['fam'] == fam and x['slug'] != p['slug']][:4]
    cv = CONTROL_VIDEO[fam]
    body = f'''<section class="phero" aria-labelledby="h1">
  <div class="wrap g">
    <div class="ptext">
      <p class="crumbs reveal"><a href="~R~">Home</a> / <a href="~R~products/">Products</a> / <a href="~R~products/#{fam}">{F['name']}</a></p>
      <h1 id="h1" class="reveal">{p['name']}</h1>
      <p class="lede reveal">{p['summary']}</p>
      <dl class="pfacts reveal"><dt>Works in</dt><dd>{p['where']}</dd><dt>Industries</dt><dd>{inds}</dd><dt>Materials</dt><dd>{gl}</dd><dt>Size</dt><dd>Single pieces from 3 kg to 7 tonnes, to drawing</dd><dt>Supplied</dt><dd>As cast, or machined to drawing</dd><dt>Inspection</dt><dd>Chemistry and hardness on every heat; UT, MPI or DPT and a dimensional report as specified</dd><dt>From a worn part</dt><dd>Yes. Send the part, or photographs with key dimensions, and we reverse-engineer it</dd></dl>
      <div class="acts reveal"><a class="btn" href="{qhref}">Get a quote for this part</a><a class="btn ghost" href="#grade">Choose the grade</a></div>
    </div>
    {vis}
  </div>
</section>
<nav class="ptabs" aria-label="On this page"><div class="wrap"><a href="#fails">How it fails</a><a href="#grade">Grade</a><a href="#control">What we control</a><a href="#ask">Quotation</a></div></nav>
<section class="psec" id="fails" aria-labelledby="fails-h"><div class="wrap">
  <div class="sh" data-r><span class="k">01</span><h2 id="fails-h">How it fails, and what we do about it</h2></div>
  <ol class="fl"><li class="hd" aria-hidden="true"><span></span><b>Failure</b><span class="r">Our answer</span></li>{fails}</ol>
</div></section>
<section class="psec soft" id="grade" aria-labelledby="grade-h"><div class="wrap">
  <div class="sh" data-r><span class="k">02</span><h2 id="grade-h">Choosing the grade</h2><p>Typical values from the governing standards. A metallurgist confirms the grade for your duty with every quotation.</p></div>
  <div class="gcards n{len(p['grades'])}">{gcards}</div>
  {DONTKNOW}
</div></section>
<section class="psec" id="control" aria-labelledby="control-h"><div class="wrap cg">
  <figure data-r><video src="~A~assets/media/{cv}.mp4" poster="~A~assets/media/{cv}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video></figure>
  <div><div class="sh" data-r><span class="k">03</span><h2 id="control-h">What we control</h2></div><ul class="ctl">{ctrl}</ul></div>
</div></section>
<section class="psec ask" id="ask" aria-labelledby="ask-h"><div class="wrap ag">
  <div data-r><div class="sh"><span class="k">04</span><h2 id="ask-h">For a quotation, send any of these</h2></div><ul class="chk">{ask}</ul>
    <p class="note">No drawing? Send the worn part or photographs with key dimensions, and we will reverse-engineer it.</p></div>
  <div class="askbox" data-r><h3>{p['name']}</h3><p>A metallurgist reviews every enquiry and replies with a price, a lead time or the right questions.</p>
    <div class="acts"><a class="btn" href="{qhref}">Get a quote for this part</a><a class="btn ghost" href="{mailto('Request for quotation: ' + p['name'])}">Email us instead</a></div>
    <p class="tel">Or call <a href="{TEL}">{PHONE}</a></p></div>
</div></section>
<section class="psec rel" aria-labelledby="rel-h"><div class="wrap">
  <div class="sh" data-r><h2 id="rel-h">More {F['name'].lower()} parts</h2><a class="more" href="~R~products/#{fam}">All {F['name'].lower()} parts {ARROW}</a></div>
  <div class="pcards">{''.join(pcard(x) for x in rel)}</div>
</div></section>'''
    js = ''
    if p.get('m3d'):
        js = r'''import { createViewer } from '~A~assets/js/parts3d.js';
const c = document.getElementById('p3d'), LITE = /lite/.test(location.search);
const v = createViewer(c, { part: c.dataset.part, finish: 'cast', distance: 6.4, exposure: 1.0, preserve: LITE });
const fb = [...document.querySelectorAll('.finish button')];
fb.forEach(b => b.addEventListener('click', () => { fb.forEach(x => x.classList.toggle('on', x === b)); v.setFinish(b.dataset.f); }));
const vb = document.querySelector('.vctl .view'), img = document.querySelector('.pvis .alt');
if (vb) vb.addEventListener('click', () => { const photo = img.hidden; img.hidden = !photo; c.style.opacity = photo ? 0 : 1; document.querySelector('.finish').hidden = photo; vb.textContent = photo ? '3D model' : 'Photograph'; });'''
    ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': p['name'], 'description': p['summary'], 'category': F['name'],
          'brand': {'@type': 'Brand', 'name': 'Standard Alloys India'}, 'manufacturer': {'@type': 'Organization', 'name': 'Standard Alloys India Pvt. Ltd.'},
          'material': ', '.join(GRADES[g]['name'] for g, _ in p['grades'])}
    page(f'products/{p["slug"]}', f'{p["name"]}: {F["name"].lower()}', f'{p["summary"].split(". ")[0]}. Cast in {gnames(p).lower()} by Standard Alloys India.', 'Products', body, js=js, three=bool(p.get('m3d')), ld=ld)

# ---------------------------------------------------------------- grades
def uses(g): return ''.join(f'<a href="~R~products/{p["slug"]}/">{p["name"]}</a>' for p in PRODUCTS if any(x == g for x, _ in p['grades']))
chart = ''
for g in GRADE_ORDER:
    G = GRADES[g]
    if 'hb' not in G: continue
    lo, hi = G['hb']; L, H = 100, 750; x = lambda v: (v - L) / (H - L) * 100
    ext = f'<b style="left:{x(hi):.1f}%;width:{x(G["hb_service"]) - x(hi):.1f}%"></b>' if G.get('hb_service') else ''
    lab = f'{lo}–{hi} HB' + (f', over {G["hb_service"] - 50} in service' if G.get('hb_service') else '')
    chart += f'<div class="crow" data-r><a href="#{g}">{G["short"]}</a><span class="tr"><i style="left:{x(lo):.1f}%;width:{x(hi) - x(lo):.1f}%"></i>{ext}</span><span class="v">{lab}</span></div>'
ticks = ''.join(f'<span style="left:{(v - 100) / 650 * 100:.1f}%">{v}</span>' for v in (100, 200, 300, 400, 500, 600, 700))
fams = ''
for g in GRADE_ORDER:
    G = GRADES[g]
    fams += f'''<article class="gfam" id="{g}" data-r>
  <div class="gh"><h2>{G['name']}</h2><p>{G['aka']}</p><div class="stds">{''.join(f'<span>{s}</span>' for s in G['standards'])}</div></div>
  <dl class="gd"><dt>Chemistry</dt><dd>{G['chem']}</dd><dt>{'Temperature' if 'temp' in G else 'Hardness'}</dt><dd>{G['strong'] if 'temp' in G else G['hardness']}</dd><dt>Heat treatment</dt><dd>{G['treat']}</dd>
  {'' if 'temp' in G else f"<dt>Strength</dt><dd>{G['strong']}</dd>"}<dt>Limits</dt><dd>{G['limit']}</dd></dl>
  <div class="gu"><h3>Parts we make in it</h3><div class="links">{uses(g)}</div></div>
</article>'''
MIST = [('Grade picked by habit, not by duty', 'Match the alloy to the feed, the impact and the temperature the part will meet.'),
        ('Manganese steel quenched too slowly', 'A slow transfer from furnace to water leaves brittle carbides. Ask how many seconds it takes.'),
        ('No method before the pattern', 'Gating and feeding should be designed, and simulated for critical parts, before metal is poured.'),
        ('Wrong alloy in the hot zone', 'HH and HK look alike on a drawing. Ask for the spectrometer report against the heat.'),
        ('Raw tolerances accepted', 'Proof-machine and check the fit, so the part installs first time in a shutdown.'),
        ('No record of the heat', 'Insist on chemistry, hardness and NDT reports traceable to the heat number.'),
        ('Waiting on overseas lead times', 'Work with a foundry that already holds your patterns.')]
mist = ''.join(f'<li data-r><b>{a}</b>{b}</li>' for a, b in MIST)
SEL = '''<div class="selector" id="selector" data-r>
  <div class="qs">
    <fieldset><legend>1. Does the part work in hot gas or hot clinker, above about 700 °C?</legend><div class="seg"><button type="button" data-q="hot" data-v="no" class="on">No</button><button type="button" data-q="hot" data-v="yes">Yes</button></div></fieldset>
    <fieldset class="nh"><legend>2. What is its main job?</legend><div class="seg"><button type="button" data-q="job" data-v="wear" class="on">Resist wear</button><button type="button" data-q="job" data-v="load">Carry load or locate</button></div></fieldset>
    <fieldset class="nh wear"><legend>3. How hard is it struck?</legend><div class="seg"><button type="button" data-q="imp" data-v="heavy">Heavy blows</button><button type="button" data-q="imp" data-v="mod" class="on">Moderate</button><button type="button" data-q="imp" data-v="low">Mostly sliding</button></div></fieldset>
    <fieldset class="nh wear"><legend>4. Can tramp metal or uncrushable pieces reach it?</legend><div class="seg"><button type="button" data-q="tramp" data-v="no" class="on">No</button><button type="button" data-q="tramp" data-v="yes">Yes</button></div></fieldset>
  </div>
  <div class="out" aria-live="polite"><span class="k">A good starting point</span><h3 id="selName">Cr-Mo and martensitic steels</h3><p id="selWhy"></p><a class="btn" id="selGo" href="#crmo">See the grade</a><p class="fine">A starting point, not a specification. A metallurgist confirms the grade with every quotation.</p></div>
</div>'''
SEL_JS = r'''const S={hot:'no',job:'wear',imp:'mod',tramp:'no'};
const N={mn:'Austenitic manganese steel',crmo:'Cr-Mo and martensitic steels',hicr:'High-chromium white iron',heat:'Heat-resistant steels',steel:'Carbon and low-alloy steels'};
function pick(){
  if(S.hot==='yes')return['heat','HH type where metal temperatures stay lower; HK type for the hottest positions and severe thermal cycling, such as the kiln outlet and the lowest cyclones; HP40Nb or a tailored nickel–chromium balance where even HK falls short.'];
  if(S.job==='load')return['steel','Parts that carry load or locate others need strength, toughness and machinability more than hardness. Normalised, or quenched and tempered.'];
  if(S.imp==='heavy')return['mn','Heavy blows work-harden manganese steel at the face while the core stays tough. Choose 18% or 22% manganese for hard, abrasive rock.'];
  if(S.imp==='low'&&S.tramp==='no')return['hicr','With little impact and no tramp metal, the hard carbides of white iron give the longest life. Ni-Hard is the usual alternative in coal grinding.'];
  if(S.imp==='low')return['crmo','White iron would last longest in sliding wear, but tramp metal could break it. Cr-Mo steel trades some wear life for toughness.'];
  return['crmo','Moderate impact will not harden manganese steel fully. Martensitic Cr-Mo steel balances hardness and toughness'+(S.tramp==='yes'?'; if tramp metal is frequent, consider manganese steel.':'.')];}
function show(){const sel=document.getElementById('selector');sel.classList.toggle('is-hot',S.hot==='yes');sel.classList.toggle('is-load',S.job==='load');
  const [g,why]=pick();document.getElementById('selName').textContent=N[g];document.getElementById('selWhy').textContent=why;document.getElementById('selGo').href='#'+g;
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches)gsap.fromTo('#selector .out > *',{y:10,opacity:0},{y:0,opacity:1,duration:.5,stagger:.05,ease:'power3.out'});}
document.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>{S[b.dataset.q]=b.dataset.v;b.parentElement.querySelectorAll('button').forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});show();}));
document.querySelectorAll('.seg button').forEach(b=>b.setAttribute('aria-pressed',b.classList.contains('on')));
show();
const GL={mn:['ASTM A128','Hadfield steel','Mn13','Mn14','Mn18','Mn22','IS 276','EN 10349','Manganese steel','Austenitic manganese steel'],
crmo:['IS 4896','Cr-Mo steel','CrMo','Martensitic steel','Pearlitic Cr-Mo steel','Chrome-moly steel'],
hicr:['ASTM A532 Class II','ASTM A532 Class III','Cr15','Cr20','Cr26','Cr27','High chrome iron','High chromium white iron','IS 4771','EN 12513','ISO 21988'],
nihard:['ASTM A532 Class I','Ni-Hard 1','Ni-Hard 2','Ni-Hard 4','Ni-Hard'],
heat:['HH','HK','HK30','HK40','HP40Nb','HP40','HP','ASTM A297','ASTM A447','IS 4522','IS 519','EN 10295','25Cr-12Ni','25Cr-20Ni','HRCS','Heat-resistant steel','Stainless steel'],
steel:['ASTM A27','ASTM A148','IS 1030','IS 2644','EN 10293','Carbon steel','Low-alloy steel','Cast steel']};
const USE={mn:'jaw plates, cone liners, hammers, apron pans and track shoes',crmo:'mill liners, diaphragms, blow bars and grizzly bars',hicr:'VRM rollers, table liners, blow bars on clean feed and chute liners',nihard:'coal mill rolls, bull ring segments, mill and chute liners',heat:'dip tubes, kiln tip castings, cooler grate plates and spouts in hot service',steel:'crusher heads, sockets, trunnions, toggles, wheels and sprockets'};
const dl=document.getElementById('glist');Object.values(GL).flat().forEach(x=>{const o=document.createElement('option');o.value=x;dl.appendChild(o)});
const norm=x=>x.toLowerCase().replace(/[^a-z0-9]/g,'');
function look(){const v=norm(document.getElementById('gq').value),out=document.getElementById('gres');if(v.length<2){out.innerHTML='';return}
  let hit=null;for(const[g,a]of Object.entries(GL)){if(a.some(x=>{const n=norm(x);return n===v||n.startsWith(v)||(v.length>3&&v.includes(n)&&n.length>2)})){hit=g;break}}
  if(hit)out.innerHTML=`<div class="yes"><b>Yes, we pour this.</b> It belongs to <a href="#${hit}">${N[hit]||'Ni-Hard (nickel-chromium white iron)'}</a>, which we cast for ${USE[hit]}. <a class="btn" href="~R~contact/?part=${encodeURIComponent(document.getElementById('gq').value.trim()+' casting')}#quote">Enquire about this grade</a></div>`;
  else out.innerHTML=`<div class="no"><b>Not in our quick list.</b> We also pour to customer specifications within our six alloy families. Send the specification and a metallurgist will confirm. <a class="btn ghost" href="~R~contact/#quote">Ask a metallurgist</a></div>`;}
document.getElementById('gq').addEventListener('input',look);'''
heatbars = ''.join(f'<div class="crow t" data-r><a href="#heat">{n}</a><span class="tr"><i style="left:0;width:{t / 1200 * 100:.1f}%"></i></span><span class="v">about {t:,} °C</span></div>' for n, t in GRADES['heat']['temp'])
page('grades', 'Materials and grades', 'The alloys we pour for wear and heat, the standards we pour them to, typical hardness and temperature limits, and where each one works best.', 'Grades',
     hero('Grades', 'Materials and grades', 'Six alloy families, poured to IS, ASTM, EN or your own specification, and chosen for the duty rather than the catalogue.', 'micro') + f'''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">The right grade is decided by what the part meets in service: impact, sliding abrasion, heat, or all three at once. Our metallurgists confirm the grade with every quotation, and every heat is analysed before the casting ships.</p></div></section>
<section class="psec" aria-labelledby="look-h"><div class="wrap">
  <div class="sh" data-r><span class="k">01</span><h2 id="look-h">I know my grade: can you make it?</h2><p>Type a designation from your drawing or specification.</p></div>
  <div class="lookup" data-r>
    <div class="bs"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><input id="gq" type="search" list="glist" placeholder="For example: HK40, ASTM A128, Cr27, Ni-Hard 4, IS 276" autocomplete="off" aria-label="Grade or standard"></div>
    <datalist id="glist"></datalist>
    <div class="lres" id="gres" aria-live="polite"></div>
  </div>
</div></section>
<section class="psec" aria-labelledby="sel-h"><div class="wrap">
  <div class="sh" data-r><span class="k">02</span><h2 id="sel-h">I know my application: which grade?</h2><p>Four questions about where the part works.</p></div>
  {SEL}
</div></section>
<section class="psec soft" aria-labelledby="ch-h"><div class="wrap">
  <div class="sh" data-r><span class="k">03</span><h2 id="ch-h">Hardness at a glance</h2><p>Typical Brinell hardness as supplied. The hatched band shows how far manganese steel hardens at the face in service.</p></div>
  <div class="chart"><div class="ticks" aria-hidden="true">{ticks}</div>{chart}</div>
  <div class="sh sm" data-r><h3>Heat-resistant steels: typical service limit</h3><p>In oxidising atmospheres. Thermal cycling, load and sulphur lower the practical limit.</p></div>
  <div class="chart heat">{heatbars}</div>
</div></section>
<section class="psec" aria-labelledby="fam-h"><div class="wrap">
  <div class="sh" data-r><span class="k">04</span><h2 id="fam-h">The six families</h2></div>
  <div class="gfams">{fams}</div>
  <p class="note">Typical values from ASTM, IS, ISO and EN standards. Final chemistry and properties are agreed for each order and reported with the casting.</p>
  {DONTKNOW}
</div></section>
<section class="why" aria-labelledby="m-h"><div class="wrap"><div class="narrow" data-r><h2 id="m-h">Seven mistakes when buying wear castings</h2><p>And what to ask your foundry instead.</p></div><ul class="seven">{mist}</ul></div></section>''' + cta('Not sure which grade?', 'Tell us where the part works and how it fails today. A metallurgist will recommend the grade.', 'Grade enquiry'),
     js=SEL_JS)

# ---------------------------------------------------------------- capabilities
CAP = [
 ('engineering', 'Engineering and method', 'sim', 'Every new part starts with a method: gating, risering and feeding designed in-house, with casting simulation through a specialist partner for critical parts. Worn parts and samples are reverse-engineered when no drawing exists.',
  ['Methoding and casting design', 'CAD and profile design', 'Reverse engineering from samples', 'Simulation with a specialist partner']),
 ('patterns', 'Pattern shop', 'moulds', 'Patterns are made in-house in wood, polystyrene and aluminium, cut on a CNC router. More than 10,000 patterns are already on file, so repeat orders go straight to moulding.',
  ['10,000+ patterns on file', 'Wood, polystyrene and aluminium', 'CNC router pattern making']),
 ('melting', 'Melting', 'pour2', 'Induction melting in crucibles from 500 kg to 6 tonnes. A dual-track power supply brings up to 10 tonnes of liquid metal to a single pour, so heavy pieces are cast in one go.',
  ['Crucibles of 500, 1,500, 3,000 and 6,000 kg', 'Up to 10 t liquid metal per pour', 'Spectrometer analysis on every heat']),
 ('moulding', 'Moulding', 'meltshop', 'Alphaset no-bake moulding gives strong, dimensionally stable moulds for pieces from 3 kg to 7,000 kg. Sand is mechanically reclaimed and reused.',
  ['Alphaset mixers of 8 and 20 t/h', 'Mould pre-heater and shell core shooter', 'Sand reclamation of 6 and 12 t/h']),
 ('heat-treatment', 'Heat treatment', 'quench', 'Gas-fired box furnaces with water quench, and bogie-hearth furnaces with air and oil quench. Manganese steel goes from furnace to water in about 45 seconds.',
  ['Two 10 t box furnaces, water quench', 'Two 12 t bogie-hearth furnaces, air and oil quench', 'Solution treatment, hardening and tempering']),
 ('machining', 'Fettling and machining', 'vtl', 'Castings are fettled, proof-machined and finished to drawing on CNC and conventional vertical lathes, machining centres and a 6,500 mm special-purpose machine.',
  ['Two CNC vertical lathes and a 1,350 mm VTL', 'Machining centres to 1,600 × 800 mm', 'Plano miller, lathes and radial drills']),
]
blocks = ''.join(f'''<article class="cblock" id="{k}" data-v="{i}"><span class="n">0{i + 1}</span><h2>{t}</h2><p>{d}</p><ul>{''.join(f'<li>{x}</li>' for x in l)}</ul></article>''' for i, (k, t, v, d, l) in enumerate(CAP))
ONV = 'class="on" '
vids = ''.join(f'<video {ONV if i == 0 else ""}src="~A~assets/media/{v}.mp4" poster="~A~assets/media/{v}.jpg" muted loop playsinline preload="{"auto" if i == 0 else "none"}" aria-hidden="true"></video>' for i, (k, t, v, d, l) in enumerate(CAP))
UNITS = [('Unit 1', '150', 'Smaller and mid-size castings, where precision and short runs matter.',
          ['Crucibles of 500 and 1,500 kg', '8 t/h Alphaset mixer', 'Shell core shooter', '6 t/h sand reclamation']),
         ('Unit SP75', '600', 'Heavy castings to 7 tonnes, with heat treatment and machining on site.',
          ['Crucibles of 3,000 and 6,000 kg; 10 t per pour', '20 t/h Alphaset mixer and mould pre-heater', '12 t/h sand reclamation', 'Box and bogie-hearth furnaces; machine shop'])]
units = ''.join(f'''<article class="unit" data-r><h3>{n}</h3><p class="cap"><b>{c}</b> tonnes a month</p><p>{d}</p><ul>{''.join(f'<li>{x}</li>' for x in l)}</ul></article>''' for n, c, d, l in UNITS)
page('capabilities', 'Capabilities', 'Engineering, pattern making, induction melting, no-bake moulding, heat treatment and machining, in our own plants.', 'Capabilities',
     hero('Capabilities', 'Everything that decides the life of a casting', 'From the method to the machined part, in our own plants.', 'furnace') + chain_html() + f'''
<section class="caps"><div class="wrap capgrid">
  <div class="capmedia"><div class="frame">{vids}</div></div>
  <div class="capblocks">{blocks}</div>
</div></section>
<section class="psec soft" aria-labelledby="u-h"><div class="wrap">
  <div class="sh" data-r><h2 id="u-h">Standard Alloys India units</h2><p>Two of our three facilities, pouring about 750 tonnes a month between them.</p></div>
  <div class="units">{units}</div>
</div></section>
<section class="psec" aria-labelledby="f-h"><div class="wrap"><div class="sh" data-r><h2 id="f-h">In figures</h2></div>
<ul class="figs"><li data-r><b>~<span data-count="14000">14000</span> t</b>Installed capacity a year, three facilities</li><li data-r><b><span data-count="10">10</span> t</b>Liquid metal in one pour</li><li data-r><b><span data-count="7000">7000</span> kg</b>Heaviest single piece</li><li data-r><b><span data-count="10000">10000</span>+</b>Patterns on file</li></ul>
<p class="note" data-r>Laboratory, NDT and inspection are described on the <a href="~R~quality/">quality page</a>.</p></div></section>''' + cta(),
     js=r'''const vs=[...document.querySelectorAll('.capmedia video')];
document.querySelectorAll('.cblock').forEach(b=>ScrollTrigger.create({trigger:b,start:'top 60%',end:'bottom 60%',onToggle:st=>{if(!st.isActive)return;
document.querySelectorAll('.cblock').forEach(x=>x.classList.toggle('on',x===b));const i=+b.dataset.v;vs.forEach((v,k)=>{v.classList.toggle('on',k===i);if(k===i&&!/lite/.test(location.search)){v.preload='auto';v.play().catch(()=>{})}else v.pause()})}}));''')

# ---------------------------------------------------------------- quality
CHAIN = ['Heat number', 'Chemistry', 'Mould', 'Heat treatment', 'Machining', 'Inspection', 'Dispatch']
chain = ''.join(f'<li data-r><i></i><span>{c}</span></li>' for c in CHAIN)
page('quality', 'Quality', 'Laboratory testing, NDT, dimensional checks and traceability from heat to dispatch. ISO 9001, ISO 14001 and ISO 45001 certified.', 'Quality',
     hero('Quality', 'Traceable to the heat', 'Every heat is analysed in our own laboratory, and every casting carries its heat number from the mould to your plant.', 'ut') + f'''
<section class="trace"><div class="wrap"><div class="narrow" data-r><h2>From melt to dispatch</h2><p>One heat number follows the casting through every step, so any report can be traced back to the metal it came from.</p></div>
<ol class="chain">{chain}</ol></div></section>
<section class="qblocks"><div class="wrap qb">
  <figure data-r><video src="~A~assets/media/micro.mp4" poster="~A~assets/media/micro.jpg" muted loop playsinline preload="none" aria-label="Microstructure examination"></video></figure>
  <div data-r><h2>Laboratory</h2><ul><li>Chemical analysis on an Ametek spectrometer, for every heat</li><li>Optical microscope with image analyser for microstructure</li><li>Tensile, impact and bench hardness testing</li><li>Sand laboratory: grain size, clay and loss on ignition, compression and shear strength</li></ul></div>
  <div data-r><h2>Non-destructive testing</h2><ul><li>Ultrasonic testing of critical sections</li><li>Magnetic particle inspection</li><li>Dye penetrant testing</li></ul><p class="aside">Manganese steel is non-magnetic and coarse-grained, so its surface is checked with dye penetrant, and its soundness is built in through the method.</p></div>
  <figure data-r><video src="~A~assets/media/mpi.mp4" poster="~A~assets/media/mpi.jpg" muted loop playsinline preload="none" aria-label="Magnetic particle inspection"></video></figure>
  <figure data-r><video src="~A~assets/media/cnc.mp4" poster="~A~assets/media/cnc.jpg" muted loop playsinline preload="none" aria-label="Machining and dimensional check"></video></figure>
  <div data-r><h2>Dimensions and fit</h2><ul><li>Dimensional inspection against the drawing</li><li>Profile and thread gauges; surface roughness</li><li>Assembly and segment fit checks</li><li>Wet and dry film thickness of the paint</li><li>3D laser scanning and portable CMM through partners</li></ul></div>
</div></section>
<section class="why" aria-labelledby="c-h"><div class="wrap"><div class="narrow" data-r><h2 id="c-h">Certified systems</h2></div>
<ul><li data-r><b>ISO 9001:2015</b>Quality management</li><li data-r><b>ISO 14001:2015</b>Environmental management</li><li data-r><b>ISO 45001:2018</b>Occupational health and safety</li></ul></div></section>''' + cta('Ask for a sample inspection report', 'See exactly what arrives with your castings before you order.', 'Sample inspection report'))

# ---------------------------------------------------------------- sustainability
INIT = [('Water scrubber', 'Cleans the fume from the induction furnaces.'),
        ('Economiser', 'Recovers waste heat from the heat-treatment furnace.'),
        ('630 kW of solar', 'Rooftop solar supplying the plant.'),
        ('Sand reclamation', 'Silica sand mechanically reclaimed and reused in moulding.'),
        ('Dust collection', 'Dust collector on the sand plant.'),
        ('Rainwater harvesting', 'Rainwater collected and returned to the ground.'),
        ('Active melt management', 'Melting monitored and controlled to cut energy per tonne.')]
init = ''.join(f'<li data-r><span class="n">{i:02d}</span><b>{a}</b>{b}</li>' for i, (a, b) in enumerate(INIT, 1))
page('sustainability', 'Sustainability', 'Absolute emission-reduction targets on a 1.5 °C pathway, 630 kW of rooftop solar and seven initiatives across our plants.', 'About',
     hero('<a href="~R~about/">About</a> / Sustainability', 'Responsible foundry', 'A casting that lasts longer is the first saving. We are also cutting the energy and emissions behind every tonne we pour.', 'solar') + '''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">A casting that lasts longer means fewer parts melted, shipped and replaced. That is where our work on grades and methods starts. In the plant, we have set absolute targets for our own emissions and put seven initiatives to work.</p></div></section>
<section class="psec soft"><div class="wrap"><div class="sh" data-r><h2>Emission targets</h2><p>Absolute reduction targets, set on a 1.5 °C pathway using the Science Based Targets initiative method.</p></div><ul class="figs">
<li data-r><b><span data-count="19.4" data-dec="1">19.4</span>%</b>Scope 1 reduction target</li>
<li data-r><b><span data-count="11.2" data-dec="1">11.2</span>%</b>Scope 2 reduction target</li>
<li data-r><b><span data-count="13" data-dec="0">13</span>%</b>Scope 1 and 2 combined</li></ul></div></section>
<section class="psec"><div class="wrap"><div class="sh" data-r><h2>Seven initiatives in the plant</h2></div><ul class="inits">''' + init + '''</ul></div></section>
<section class="qblocks"><div class="wrap qb">
<div data-r><h2>Environmental management</h2><ul><li>ISO 14001:2015 certified</li><li>Moulding sand reclaimed and reused</li><li>Steel scrap remelted in induction furnaces</li></ul></div>
<figure data-r><video src="~A~assets/media/aerial.mp4" poster="~A~assets/media/aerial.jpg" muted loop playsinline preload="none" aria-label="The plant from the air"></video></figure>
<figure data-r><video src="~A~assets/media/meltshop.mp4" poster="~A~assets/media/meltshop.jpg" muted loop playsinline preload="none" aria-label="Induction melt shop"></video></figure>
<div data-r><h2>Safe workplace</h2><ul><li>ISO 45001:2018 certified</li><li>Health and safety managed to a certified system</li></ul></div>
</div></section>''' + cta('Talk to us about sustainability data', 'We can share our certificates and emission targets for your supplier assessment.', 'Sustainability information'))

# ---------------------------------------------------------------- about
LEAD = [('Shiv Das Baheti', 'Founder and Managing Director', 'More than 50 years in industry. BITS Pilani; National Institute of Foundry and Forge Technology.'),
        ('Gaurav Baheti', 'Director', 'More than 15 years in the business. BITS Pilani; SP Jain Institute of Management.'),
        ('Sorab Baheti', 'Director', 'More than 8 years in the business. IIT Kanpur, materials science; earlier with Tonbo Imaging and on thyssenkrupp cement plant projects.')]
lead = ''.join(f'<article class="person" data-r><h3>{n}</h3><p class="role">{r}</p><p>{d}</p></article>' for n, r, d in LEAD)
page('about', 'About us', 'Standard Alloys India: a steel foundry since 1991, making wear- and heat-resistant castings for plants worldwide.', 'About',
     hero('About', 'Since 1991', 'A fabrication shop that became a specialist foundry for the parts that wear out first.', 'aerial') + '''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">Standard Alloys India began in 1991 as a fabrication shop in Ajmer, Rajasthan, and lit its first induction furnace in 1994. Over three decades we have built a foundry around one idea: a casting should be specified for the duty it will meet. Today our three facilities have about 14,000 tonnes a year of installed capacity, pouring single pieces from 3 kg to 7 tonnes for more than 500 industrial customers, in plants anywhere in the world.</p></div></section>
<section><div class="wrap timeline">
<div data-r><b>1991</b><span>Starts as a fabrication shop in Ajmer</span></div>
<div data-r><b>1994</b><span>First induction furnace, the start of the foundry</span></div>
<div data-r><b>Today</b><span>About 14,000 t a year of capacity, castings to 7 tonnes, shipped worldwide</span></div></div></section>
<section class="why"><div class="wrap"><div class="narrow" data-r><h2>How we work</h2></div>
<ul><li data-r><b>Duty first</b>We ask where a part runs and how it fails before we recommend a grade.</li>
<li data-r><b>In-house control</b>Method, pattern, melt, heat treatment, machining and testing in our own plant.</li>
<li data-r><b>Evidence with every casting</b>Chemistry, hardness and NDT reports, traceable to the heat.</li></ul></div></section>
<section class="psec" aria-labelledby="l-h"><div class="wrap"><div class="sh" data-r><h2 id="l-h">Leadership</h2></div><div class="people">''' + lead + '''</div></div></section>
<section class="aboutlinks"><div class="wrap al">
<a href="~R~capabilities/" data-r><video src="~A~assets/media/vtl.mp4" poster="~A~assets/media/vtl.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Capabilities</span></a>
<a href="~R~quality/" data-r><video src="~A~assets/media/ut.mp4" poster="~A~assets/media/ut.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Quality</span></a>
<a href="~R~sustainability/" data-r><video src="~A~assets/media/solar.mp4" poster="~A~assets/media/solar.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Sustainability</span></a>
<a href="~R~careers/" data-r><video src="~A~assets/media/grind.mp4" poster="~A~assets/media/grind.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Careers</span></a>
</div></section>''' + cta('Work with us', 'Send a drawing, a sample or a worn part, and we will take it from there.'))

# ---------------------------------------------------------------- careers
WHYWORK = [('Learn on real parts', 'Training on the shop floor and in the laboratory, on castings that go into working plants.'),
           ('Metallurgy at the core', 'Work next to metallurgists who choose grades, design methods and read microstructures every day.'),
           ('Safety first', 'Health and safety run to a certified ISO 45001:2018 system, in every unit.'),
           ('Room to grow', 'People who learn the process end to end take on more responsibility, from cell to shift to department.'),
           ('A global customer base', 'Parts you make run in cement, mining, power and steel plants anywhere in the world.'),
           ('Thirty-five years of craft', 'A family-run foundry since 1991, investing in new furnaces, machines and methods.')]
whywork = ''.join(f'<li data-r><span class="n">{i:02d}</span><b>{a}</b>{b}</li>' for i, (a, b) in enumerate(WHYWORK, 1))
TEAMS = [('Melting and moulding', 'meltshop'), ('Metallurgy and laboratory', 'micro'), ('Heat treatment', 'quench'), ('Machining', 'drill'),
         ('Quality and NDT', 'mpi'), ('Engineering and patterns', 'moulds'), ('Sales and export', 'jaws'), ('Maintenance', 'cnc')]
teams = ''.join(f'<figure data-r><video src="~A~assets/media/{v}.mp4" poster="~A~assets/media/{v}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><figcaption>{t}</figcaption></figure>' for t, v in TEAMS)
LIFE = [  # (file, kind, category, caption, size)  size: big | tall | wide | ''
 ('v-firedrill', 'clip', 'training', 'Fire safety drill on the shop floor', 'big'),
 ('cricket-team', 'photo', 'sports', 'Our cricket team', 'wide'),
 ('training-session', 'photo', 'training', 'Training session', ''),
 ('v-safa', 'clip', 'celebrations', 'Celebration on the shop floor', 'wide'),
 ('plant-visit-1', 'photo', 'training', 'Students on a plant visit', ''),
 ('cricket-awards', 'photo', 'sports', 'Cricket league felicitation', ''),
 ('v-festival', 'clip', 'celebrations', 'Festival celebrations', 'wide'),
 ('team-meeting', 'photo', 'team', 'Team meeting', ''),
 ('cricket-ground', 'photo', 'sports', 'Match day', ''),
 ('shopfloor-assembly', 'photo', 'team', 'Shop-floor assembly', 'wide'),
 ('v-games', 'clip', 'celebrations', 'Team games in the office', ''),
 ('student-briefing', 'photo', 'training', 'Briefing before the plant tour', ''),
 ('office-celebration', 'photo', 'celebrations', 'Celebrating together', ''),
 ('plant-visit-2', 'photo', 'training', 'Shop-floor walk-through', ''),
 ('cricket-league', 'photo', 'sports', 'The league, all teams', 'wide'),
]
def _tile(f, k, c, cap, sz):
    if k == 'clip':
        m = f'<video src="~A~assets/life/{f}.mp4" poster="~A~assets/life/{f}.jpg" muted loop playsinline preload="none" disablepictureinpicture controlslist="nodownload noplaybackrate noremoteplayback" aria-hidden="true"></video>'
    else:
        m = f'<img src="~A~assets/life/{f}-s.jpg" alt="{cap}" loading="lazy" draggable="false">'
    return f'<figure class="lt {sz}" data-cat="{c}">{m}<figcaption class="cap">{cap}</figcaption></figure>'
wall = '<div class="chips lchips" role="group" aria-label="Filter">' + ''.join(f'<button class="chip{" on" if v == "all" else ""}" data-l="{v}">{t}</button>' for v, t in [('all', 'All'), ('training', 'Training and safety'), ('sports', 'Sports'), ('celebrations', 'Celebrations'), ('team', 'Team')]) + '</div><div class="lwall" oncontextmenu="return false">' + ''.join(_tile(*x) for x in LIFE) + '</div>'
STREAMS = [('Technical roles', 'Melting, moulding, heat treatment, machining, metallurgy and laboratory, quality and NDT, engineering and patterns, maintenance.', 'Technical role'),
           ('Commercial roles', 'Sales and export, purchase, planning, accounts, human resources and administration.', 'Commercial role')]
streams = ''.join(f'<article class="stream" data-r><h3>{t}</h3><p>{d}</p><a class="btn" href="#apply" data-role="{r}">Apply for a {r.lower()}</a></article>' for t, d, r in STREAMS)
FORM = """<form class="rfqf jobf" data-job novalidate aria-label="Job application">
  <fieldset><legend><span>1</span>What would you like to do?</legend>
    <div class="row"><select name="area" aria-label="Area of work"><option value="">Choose an area</option><option>Technical role</option><option>Commercial role</option><option>Internship or industrial training</option><option>Not sure yet</option></select><input name="role" aria-label="Role" placeholder="Role you are interested in (optional)"></div>
    <div class="row"><input name="exp" aria-label="Experience" placeholder="Years of experience, or your course and year"><input name="qual" aria-label="Qualification" placeholder="Highest qualification"></div>
  </fieldset>
  <fieldset><legend><span>2</span>About you</legend>
    <div class="row"><input name="name" aria-label="Name" placeholder="Name" autocomplete="name" required><input name="email" type="email" aria-label="Email" placeholder="Email" autocomplete="email" required></div>
    <div class="row"><input name="phone" aria-label="Phone" placeholder="Phone" autocomplete="tel"><input name="city" aria-label="Current city" placeholder="Current city"></div>
    <textarea name="notes" rows="3" aria-label="Message" placeholder="Tell us a little about yourself (optional)"></textarea>
  </fieldset>
  <div class="sub"><button class="btn" type="submit">Prepare my application</button><p class="msg" role="status">Your email app opens with these details filled in. Attach your CV before sending.</p></div>
</form>"""
CAREER_JS = r"""const lchips=[...document.querySelectorAll('.lchips .chip')],tiles=[...document.querySelectorAll('.lt')];
lchips.forEach(c=>c.addEventListener('click',()=>{lchips.forEach(x=>x.classList.toggle('on',x===c));tiles.forEach(t=>t.hidden=!(c.dataset.l==='all'||t.dataset.cat===c.dataset.l));ScrollTrigger.refresh();}));
tiles.forEach(t=>{const v=t.querySelector('video');if(v&&!/lite/.test(location.search))new IntersectionObserver(([e])=>{e.isIntersecting?(v.preload='auto',v.play().catch(()=>{})):v.pause()}).observe(t);});
document.querySelector('.lwall').addEventListener('dragstart',e=>e.preventDefault());
const MAIL='sales@standardalloysindia.com', f=document.querySelector('[data-job]');
document.querySelectorAll('[data-role]').forEach(a=>a.addEventListener('click',()=>{f.area.value=a.dataset.role;}));
f.addEventListener('submit',e=>{e.preventDefault();let ok=true;['name','email'].forEach(n=>{const el=f[n],bad=!el.value.trim()||(n==='email'&&!/^\S+@\S+\.\S+$/.test(el.value));el.setAttribute('aria-invalid',bad);if(bad&&ok){el.focus();ok=false}});
 if(!ok){f.querySelector('.msg').textContent='Please add your name and email. Everything else is optional.';return}
 const v=n=>f[n].value.trim()||'-';const body=[`Area: ${v('area')}`,`Role: ${v('role')}`,`Experience: ${v('exp')}`,`Qualification: ${v('qual')}`,'',`Name: ${v('name')}`,`Email: ${v('email')}`,`Phone: ${v('phone')}`,`City: ${v('city')}`,'',v('notes'),'','CV attached.'].join('\n');
 location.href=`mailto:${MAIL}?subject=${encodeURIComponent('Job application: '+(f.area.value||'General')+(f.role.value?' – '+f.role.value:''))}&body=${encodeURIComponent(body)}`;
 f.querySelector('.msg').textContent='Your email app should now be open. Attach your CV and press send.';});"""
page('careers', 'Careers', 'Careers at Standard Alloys India: technical and commercial roles, internships and industrial training in foundry, metallurgy, machining, quality and export.', 'About',
     hero('<a href="~R~about/">About</a> / Careers', 'Careers at Standard Alloys India', 'Join the people who melt, mould, treat, machine and test the castings that keep plants running around the world.', 'sparks') + f"""
<section class="psec"><div class="wrap cg">
  <figure data-r><video src="~A~assets/media/pour2.mp4" poster="~A~assets/media/pour2.jpg" muted loop playsinline preload="none" aria-hidden="true"></video></figure>
  <div data-r><div class="sh"><h2>A culture of craft, rigour and responsibility</h2></div>
    <p>A foundry runs on skill. We look for people who take pride in exact work, from the melt shop to the laboratory, and who want to understand why a casting lasts, not only how it is made.</p>
    <p style="margin-top:14px">You learn on real parts for real plants, alongside metallurgists and engineers, with every step of the process under one roof.</p>
    <div class="acts" style="margin-top:28px"><a class="btn" href="#openings">Explore openings</a><a class="btn ghost" href="#apply">Apply now</a></div></div>
</div></section>
<section class="psec soft" aria-labelledby="ww-h"><div class="wrap"><div class="sh" data-r><h2 id="ww-h">Why work with us</h2></div><ul class="inits six">{whywork}</ul></div></section>
<section class="psec" aria-labelledby="tm-h"><div class="wrap"><div class="sh" data-r><h2 id="tm-h">Where you could work</h2></div><div class="tg">{teams}</div></div></section>
<section class="psec soft" id="openings" aria-labelledby="op-h"><div class="wrap">
  <div class="sh" data-r><h2 id="op-h">Current openings</h2><p>Specific vacancies will be listed here. Until then, apply in the stream that suits you and we will contact you when a matching role opens.</p></div>
  <div class="streams">{streams}
    <article class="stream intern" data-r><h3>Internships and industrial training</h3><p>For engineering, metallurgy and management students who want to see a working foundry from method to dispatch.</p><a class="btn ghost" href="#apply" data-role="Internship or industrial training">Ask about an internship</a></article></div>
</div></section>
<section class="psec" aria-labelledby="lf-h"><div class="wrap"><div class="sh" data-r><h2 id="lf-h">Life at Standard Alloys India</h2></div>{wall}</div></section>
<section class="psec soft" id="apply" aria-labelledby="ap-h"><div class="wrap">
  <div class="sh" data-r><h2 id="ap-h">Apply</h2><p>A few details and your CV. No vacancy listed for you? Apply anyway.</p></div>
  <!-- ERPNext Job Applicant web form: put its URL in data-webform to replace the email composer -->
  <div data-webform="" data-title="Job application">{FORM}</div>
</div></section>
<section class="psec"><div class="wrap"><ul class="figs"><li data-r><b>35+</b>Years in the foundry business</li><li data-r><b>~14,000 t</b>Installed capacity a year</li><li data-r><b>500+</b>Industrial customers</li><li data-r><b>Worldwide</b>Plants our castings run in</li></ul></div></section>""", js=CAREER_JS)

# ---------------------------------------------------------------- contact
page('contact', 'Get a quote', 'Get a quote or discuss your part with Standard Alloys India. A drawing, photographs or only the equipment model is enough to start.', 'Contact',
     hero('Contact', 'Get a quote', 'A drawing, photographs of the worn part, or only the equipment model: any of them is enough to start. A metallurgist replies with a price, a lead time or the right questions.', 'drill') + f"""
<section class="quote" id="quote" aria-labelledby="q-h"><div class="wrap">
  <div class="sh" data-r><h2 id="q-h">Discuss your part</h2><p>Don’t know the material? That’s fine. Tell us where the part works and how it fails, and our metallurgists will recommend it.</p></div>
  <!-- ERPNext Web Form: when the URL from saconnect.frappe.cloud is ready, put it in data-webform below and the upload form replaces the email composer -->
  <div data-webform="" data-title="Request for quotation">{rfq_html()}</div>
</div></section>
{EXPORT}
<section class="visit"><div class="wrap">
  <div class="sh" data-r><h2>Visit the foundry</h2><p><a href="{TEL}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div>
  <div class="maps">
    <figure data-r><iframe title="Map of Standard Alloys India Unit 1, Parbatpura Industrial Area, Ajmer" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=26.4138148,74.662982&amp;z=15&amp;output=embed"></iframe>
      <figcaption><b>Unit 1</b><address>F-26B &amp; 27, Parbatpura Industrial Area<br>Ajmer 305002, Rajasthan, India</address><a href="https://maps.app.goo.gl/eiyeFoDQeCdKW6zdA" target="_blank" rel="noopener">Open in Google Maps</a></figcaption></figure>
    <figure data-r><iframe title="Map of Standard Alloys India Unit SP75, Ajmer" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=26.4351518,74.6963154&amp;z=15&amp;output=embed"></iframe>
      <figcaption><b>Unit SP75</b><address>Standard Alloys India Pvt. Ltd., Unit SP75<br>Ajmer, Rajasthan, India</address><a href="https://maps.app.goo.gl/sSciMavsfMzPz3A56" target="_blank" rel="noopener">Open in Google Maps</a></figcaption></figure>
  </div>
</div></section>""")

# ---------------------------------------------------------------- keep the hand-written home in step
home = os.path.join(OUT, 'index.html')
src = open(home).read()
src = re.sub(r'<!--footer-->.*?<!--/footer-->', '<!--footer-->\n' + footer('', '../') + '\n<!--/footer-->', src, flags=re.S)
for mk, h in [('why', why_html()), ('chain', chain_html()), ('rfq', rfq_html()), ('export', EXPORT)]:
    h = h.replace('~R~', '').replace('~A~', '../')
    src = re.sub(rf'<!--{mk}-->.*?<!--/{mk}-->', lambda m: f'<!--{mk}-->\n{h}\n<!--/{mk}-->', src, flags=re.S)
open(home, 'w').write(src); print('footer synced', home)

# ---------------------------------------------------------------- 404 (site root; works on any path depth)
open('404.html', 'w').write('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Standard Alloys India</title><meta name="robots" content="noindex">
<style>
*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Open Sans",system-ui,sans-serif;color:#4a4a4f;background:#fff;min-height:100svh;display:grid;place-items:center;padding:40px 24px;text-align:center}
.mark{display:inline-flex;align-items:center;gap:12px;color:#1d1d1f;text-decoration:none;font-weight:700;letter-spacing:.02em}.mark img{width:40px}
h1{margin-top:48px;color:#d42a2a;text-transform:uppercase;font-weight:600;font-size:clamp(28px,4vw,44px);line-height:1.15}
p{margin-top:16px;max-width:46ch;margin-inline:auto;line-height:1.7}
.acts{margin-top:30px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.acts a{display:inline-flex;align-items:center;min-height:46px;padding:0 24px;font:600 13px/1 inherit;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;background:#d42a2a;color:#fff}
.acts a+a{background:none;color:#1d1d1f;box-shadow:inset 0 0 0 1px #1d1d1f}
</style></head><body><main>
<a class="mark" data-href="standard-alloys/"><img data-src="assets/saipl-logo.png" alt="">STANDARD ALLOYS INDIA</a>
<h1>This page has moved or never existed</h1>
<p>The part you are looking for may be under a new address. Start from our products, or send us the drawing and we will take it from there.</p>
<div class="acts"><a data-href="standard-alloys/products/">See all products</a><a data-href="standard-alloys/contact/#quote">Send a drawing</a></div>
</main>
<script>const b=location.pathname.startsWith('/sa-group-website/')?'/sa-group-website/':'/';document.querySelectorAll('[data-href]').forEach(a=>a.href=b+a.dataset.href);document.querySelectorAll('[data-src]').forEach(i=>i.src=b+i.dataset.src);</script>
</body></html>
''')
print('wrote 404.html')
