#!/usr/bin/env python3
"""Generates the Standard Alloys India inner pages from data.
Run from the repo root:  python3 _src/build.py
Home (standard-alloys/index.html) and the gateway (index.html) are hand-written."""
import os, html, json

OUT = 'standard-alloys'
NAV = [('About', 'about/'), ('Capabilities', 'capabilities/'), ('Industries', 'industries/'),
       ('Products', 'products/'), ('Grades', 'grades/'), ('Quality', 'quality/'), ('Contact', 'contact/')]
MAIL = 'sales@standardalloysindia.com'
PHONE = '+91 145 269 5110'
ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def esc(s): return html.escape(s, quote=True)

def page(path, title, desc, active, body, css='', js=''):
    depth = path.count('/') + 1
    r = '../' * depth              # to standard-alloys/
    a = '../' * (depth + 1)        # to repo root (assets)
    ON = ' class="on"'
    nav = ''.join(f'<a href="{r}{h}"{ON if l == active else ""}>{l}</a>' for l, h in NAV)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Standard Alloys India</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}sai.css">
<script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}}}</script>
{('<style>' + css + '</style>') if css else ''}
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<header class="top solid" id="top">
  <div class="wrap">
    <a class="brand" href="{r}"><img src="{a}assets/saipl-logo.png" alt="" width="40" height="36">STANDARD ALLOYS INDIA</a>
    <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav id="nav" aria-label="Main">{nav}<a class="btn" href="{r}contact/#quote">Send a drawing</a></nav>
  </div>
</header>
<main>
{body.replace('{A}', a).replace('{R}', r)}
</main>
<a class="sidetab" href="{r}contact/#quote">Send a drawing</a>
<footer>
  <div class="wrap">
    <span>© 2026 Standard Alloys India Pvt. Ltd. · Steel casting foundry, Ajmer</span>
    <nav aria-label="Footer"><a href="{r}about/">About</a><a href="{r}sustainability/">Sustainability</a><a href="{r}careers/">Careers</a><a href="{r}contact/">Contact</a></nav>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
<script>{COMMON_JS}</script>
{('<script type="module">' + js.replace('{A}', a).replace('{R}', r) + '</script>') if js else ''}
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
document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const t = document.querySelector(a.getAttribute('href')); if (t && lenis) { e.preventDefault(); lenis.scrollTo(t, { offset: -150 }); } }));
const mb = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
mb.addEventListener('click', () => { const o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });
/* videos play only on screen */
if (!LITE) { const io = new IntersectionObserver(es => es.forEach(e => { const v = e.target; if (e.isIntersecting && !reduce) { v.preload = 'auto'; v.play().catch(() => {}); } else v.pause(); }), { rootMargin: '120px' });
  document.querySelectorAll('video').forEach(v => io.observe(v)); }
/* part links pre-fill the quote email */
const mail = document.getElementById('mail');
document.querySelectorAll('[data-part]').forEach(a => a.addEventListener('click', () => { if (mail) mail.href = `mailto:sales@standardalloysindia.com?subject=${encodeURIComponent('Request for quotation: ' + a.dataset.part)}`; }));
/* process line follows the reader */
const steps = [...document.querySelectorAll('.step')], items = [...document.querySelectorAll('.line li:not(.fill)')], fill = document.getElementById('fill');
if (fill) steps.forEach((s, i) => ScrollTrigger.create({ trigger: s, start: 'top 55%', end: 'bottom 55%', onToggle: st => { if (!st.isActive) return;
  items.forEach((li, k) => { li.classList.toggle('done', k < i); li.classList.toggle('now', k === i); });
  fill.style.width = `calc(${i / Math.max(1, items.length - 1)} * (100% - 2 * var(--gut) - 20%))`; } }));
/* cards tilt toward the pointer */
document.querySelectorAll('.part-card, .pgrid a').forEach(c => {
  c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); c.style.transform = `rotateY(${((e.clientX - r.left) / r.width - .5) * 10}deg) rotateX(${-((e.clientY - r.top) / r.height - .5) * 10}deg)`; });
  c.addEventListener('pointerleave', () => c.style.transform = '');
});
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
if (!reduce) {
  gsap.from('.ihero h1 .ln > span', { yPercent: 105, duration: 1.1, ease: 'power4.out', delay: .15 });
  gsap.from('.ihero .crumbs, .ihero p:not(.crumbs)', { y: 18, opacity: 0, duration: .9, ease: 'power3.out', stagger: .1, delay: .35 });
  gsap.to('.ihero video', { yPercent: 12, scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.ihero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.utils.toArray('[data-r]').forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: .8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
  ScrollTrigger.batch('.part-card, .pgrid a', { start: 'top 92%', once: true, onEnter: b => gsap.from(b, { y: 40, rotateX: -8, opacity: 0, duration: .9, ease: 'power3.out', stagger: .06 }) });
} else document.querySelectorAll('[data-r]').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; });
'''

def hero(crumb, h1, lede, video, short=False):
    return f'''<section class="ihero{' short' if short else ''}" aria-labelledby="h1">
  <video src="{{A}}assets/media/{video}.mp4" poster="{{A}}assets/media/{video}.jpg" muted loop playsinline autoplay aria-hidden="true"></video>
  <div class="in wrap">
    <p class="crumbs"><a href="{{R}}">Home</a> / {crumb}</p>
    <h1 id="h1"><span class="ln"><span>{h1}</span></span></h1>
    <p>{lede}</p>
  </div>
</section>'''

def cta(title='Send the drawing of your next part', sub='A metallurgist reviews every enquiry and replies with a price, a lead time or the right questions.', subject='Request for quotation'):
    return f'''<section class="cta" id="contact" aria-labelledby="cta-h">
  <div class="wrap narrow" data-r>
    <h2 id="cta-h">{title}</h2>
    <p>{sub}</p>
    <a class="btn" id="mail" href="mailto:{MAIL}?subject={subject.replace(' ', '%20')}">Email the drawing</a>
    <a class="btn ghost" href="{{R}}contact/#quote">Use the quote form</a>
  </div>
</section>'''

def card(img, name, fails, grade, labels=('Fails by', 'Usual grade')):
    pic = f'<div class="pic"><img src="{{A}}assets/cutouts/{img}.png" alt="{esc(name)}" loading="lazy"></div>' if img else '<div class="pic none">Photograph to follow</div>'
    return f'''<article class="part-card" id="{slug(name)}">{pic}<div class="body"><h3>{name}</h3><dl><dt>{labels[0]}</dt><dd>{fails}</dd><dt>{labels[1]}</dt><dd>{grade}</dd></dl><a href="#contact" data-part="{esc(name)}">Send this part’s drawing</a></div></article>'''

def slug(s): return ''.join(c if c.isalnum() else '-' for c in s.lower()).strip('-').replace('--', '-')

# ---------------------------------------------------------------- industries
IND = json.load(open(os.path.join(os.path.dirname(__file__), 'industries.json')))
ALL_PARTS = []
for ind in IND:
    line = ''.join(f'<li><a href="#{s["id"]}"><i></i>{s["label"]}</a></li>' for s in ind['steps'])
    secs = ''
    for k, s in enumerate(ind['steps'], 1):
        duty = ''.join(f'<span class="hot">{d[1:]}</span>' if d.startswith('!') else f'<span>{d}</span>' for d in s['duty'])
        cards = ''.join(card(*p, labels=tuple(ind.get('labels', ('Fails by', 'Usual grade')))) for p in s['parts'])
        for p in s['parts']:
            if ind['slug'] == 'equipment-makers' and s['id'] != 'series': continue
            ALL_PARTS.append({'img': p[0], 'name': p[1], 'grade': p[3], 'ind': ind['name'], 'href': f'industries/{ind["slug"]}/#{slug(p[1])}'})
        secs += f'''<section class="step" id="{s['id']}" aria-labelledby="s{k}">
  <div class="wrap">
    <div class="step-head">
      <div><span class="n">Stage {k}</span><h2 id="s{k}">{s['name']}</h2></div>
      <div><p>{s['text']}</p><div class="duty">{duty}</div></div>
    </div>
    <div class="parts">{cards}</div>
  </div>
</section>'''
    why = ''.join(f'<li data-r><b>{b}</b>{t}</li>' for b, t in ind['why'])
    body = hero(f'<a href="{{R}}industries/">Industries</a> / {ind["name"]}', ind['name'], ind['lede'], ind['video']) + f'''
<nav class="line" aria-label="{ind['name']} process steps" style="--n:{len(ind['steps'])}"><ol><li class="fill" id="fill" aria-hidden="true"></li>{line}</ol></nav>
<section class="intro"><div class="wrap narrow" data-r><p>{ind['intro']}</p></div></section>
{secs}
<section class="why" aria-labelledby="why-h"><div class="wrap"><div class="narrow" data-r><h2 id="why-h">{ind['why_title']}</h2></div><ul>{why}</ul></div></section>
''' + cta(subject=f'Request for quotation: {ind["name"].lower()} part')
    page(f'industries/{ind["slug"]}', f'{ind["name"]} castings', ind['desc'], 'Industries', body)

# industries overview
tiles = ''.join(f'''<a class="tile" href="{{R}}industries/{i['slug']}/" data-r><video src="{{A}}assets/media/{i['tile']}.mp4" poster="{{A}}assets/media/{i['tile']}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><div class="t"><h3><i>{ARROW}</i>{i['name']}</h3><p>{i['tile_text']}</p></div></a>''' for i in IND)
page('industries', 'Industries', 'Castings for cement, mining, aggregate, steel and power plants, and for the equipment makers who build them.', 'Industries',
     hero('Industries', 'Industries we serve', 'Parts for equipment that runs around the clock, where one early failure stops a whole line.', 'mining') +
     f'<section class="sectors"><div class="tiles" style="margin-top:0">{tiles}</div></section>' + cta())

# ---------------------------------------------------------------- products A–Z
fams = sorted({p['ind'] for p in ALL_PARTS}, key=[i['name'] for i in IND].index)
chips = '<button class="chip on" data-f="all">All</button>' + ''.join(f'<button class="chip" data-f="{slug(f)}">{f}</button>' for f in fams)
seen, cards = {}, ''
for p in sorted(ALL_PARTS, key=lambda x: x['name']):
    key = p['name']
    if key in seen: seen[key]['ind'].append(p['ind']); continue
    seen[key] = {**p, 'ind': [p['ind']]}
for p in sorted(seen.values(), key=lambda x: x['name']):
    pic = f'<img src="{{A}}assets/cutouts/{p["img"]}.png" alt="" loading="lazy">' if p['img'] else '<span class="noimg">Photograph to follow</span>'
    cards += f'<a href="{{R}}{p["href"]}" data-f="{" ".join(slug(i) for i in p["ind"])}">{pic}<b>{p["name"]}</b><span>{", ".join(p["ind"])} · {p["grade"]}</span></a>'
page('products', 'Products', 'Every wear- and heat-resistant part we cast, by industry, with the grade we usually use.', 'Products',
     hero('Products', 'Products A to Z', 'Every part we cast, with the industry it serves and the grade we usually start from.', 'rings') + f'''
<section class="products" style="padding-top:clamp(56px,7vw,90px)"><div class="wrap">
  <div class="chips" role="group" aria-label="Filter by industry">{chips}</div>
  <div class="pgrid" id="pgrid">{cards}</div>
  <p class="after" data-r>Your part not listed? We cast to drawing, sample or sketch, with more than 10,000 patterns already on file.</p>
</div></section>''' + cta(),
     css='''.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:40px}
.chip{border:1px solid var(--line);background:#fff;color:var(--ink);font:600 12px/1 var(--font);letter-spacing:.06em;text-transform:uppercase;padding:12px 18px;border-radius:999px;cursor:pointer;transition:background .25s,color .25s,border-color .25s}
.chip:hover{border-color:var(--ink)}.chip.on{background:var(--red);border-color:var(--red);color:#fff}
.pgrid a.out{display:none}.pgrid .noimg{display:grid;place-items:center;color:var(--muted);font-size:13px}''',
     js='''const chips=[...document.querySelectorAll('.chip')], cards=[...document.querySelectorAll('#pgrid a')];
chips.forEach(c=>c.addEventListener('click',()=>{chips.forEach(x=>x.classList.toggle('on',x===c));const f=c.dataset.f;
cards.forEach(a=>{const show=f==='all'||a.dataset.f.split(' ').includes(f);a.classList.toggle('out',!show);if(show&&!matchMedia('(prefers-reduced-motion: reduce)').matches)gsap.fromTo(a,{opacity:0,y:16},{opacity:1,y:0,duration:.5,ease:'power3.out'})});ScrollTrigger.refresh()}));''')

# ---------------------------------------------------------------- grades
GR = [
 ('Austenitic manganese steel', 'ASTM A128, IS 276', 'About 200 HB as cast; hardens in service under impact', 'Jaw plates, concaves, mantles, hammers, crusher liners'),
 ('High chromium white iron', 'ASTM A532 Class II and III', 'Typically 550 to 700 HB after heat treatment', 'VRM rollers and table liners, blow bars on soft feed, chute liners'),
 ('Ni-Hard', 'ASTM A532 Class I', 'Typically 550 to 650 HB', 'Mill liners, coal mill parts, pump and chute wear parts'),
 ('Cr-Mo steel', 'To customer or internal specification', 'Typically 300 to 550 HB, set by heat treatment', 'Ball mill liners, diaphragms, blow bars and grates in mixed duty'),
 ('Heat-resistant Cr-Ni steel', 'ASTM A297 (HH, HK and related types)', 'Chosen for strength and scaling resistance at temperature', 'Dip tubes, kiln tip castings, cooler grate plates, furnace castings'),
 ('Carbon and low alloy steel', 'ASTM A27, A148, IS 1030', 'Typically 150 to 300 HB', 'Structural, conveying and machined parts that must weld'),
]
rows = ''.join(f'<tr data-r><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in GR)
MIST = [('Grade picked by habit, not by duty', 'Match the alloy to the feed, impact and temperature the part will meet.'),
        ('Manganese steel quenched too slowly', 'Water quench fast from the furnace, or the steel embrittles and cracks.'),
        ('No method design before pouring', 'Simulate the casting method to keep shrinkage out of critical sections.'),
        ('Wrong alloy for the hot zone', 'Verify Cr-Ni chemistry on a spectrometer before the part ships.'),
        ('Raw tolerances accepted', 'Proof-machine and check fit-up so the part installs first time.'),
        ('No record of the heat', 'Insist on chemistry, hardness and NDT reports traceable to the heat.'),
        ('Waiting on overseas lead times', 'Work with a foundry that already holds your patterns.')]
mist = ''.join(f'<li data-r><b>{a}</b>{b}</li>' for a, b in MIST)
page('grades', 'Materials and grades', 'The alloys we pour for wear and heat, the standards we pour them to, and where each one works best.', 'Grades',
     hero('Grades', 'Materials and grades', 'Six alloy families, poured to IS, ASTM or your own specification, and chosen for the duty, not the catalogue.', 'micro') + f'''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">The right grade is decided by what the part meets in service: impact, sliding abrasion, heat or all three. Our metallurgists confirm the grade with every quotation, and every heat is tested before the casting ships.</p></div></section>
<section class="gradetab"><div class="wrap">
  <div class="tscroll"><table><thead><tr><th scope="col">Alloy family</th><th scope="col">Standards</th><th scope="col">Typical hardness or limit</th><th scope="col">Where it works</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note">Typical values. Final chemistry and properties are confirmed for each order and reported with the casting.</p>
</div></section>
<section class="why" aria-labelledby="m-h"><div class="wrap"><div class="narrow" data-r><h2 id="m-h">Seven mistakes when buying wear castings</h2><p>And what to ask your foundry instead.</p></div><ul class="seven">{mist}</ul></div></section>''' + cta('Not sure which grade?', 'Tell us where the part works and how it fails today. A metallurgist will recommend the grade.', 'Grade enquiry'),
     css='''.gradetab{padding:24px 0 clamp(72px,9vw,120px)}
.tscroll{overflow-x:auto;border:1px solid var(--line)}
.gradetab table{width:100%;border-collapse:collapse;min-width:820px;font-size:15px}
.gradetab th,.gradetab td{text-align:left;vertical-align:top;padding:20px 22px;border-bottom:1px solid var(--line)}
.gradetab thead th{background:var(--soft);font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.gradetab tbody th{color:var(--red);font-weight:600;text-transform:uppercase;font-size:14px;letter-spacing:.02em;width:22%}
.gradetab tbody tr{transition:background .25s}.gradetab tbody tr:hover{background:#fcfcfd}
.gradetab .note{margin-top:14px;font-size:13px;color:var(--muted)}
.seven{counter-reset:m}.seven li{counter-increment:m}.seven li b::before{content:counter(m) ". ";color:var(--red)}''')

# ---------------------------------------------------------------- capabilities
CAP = [
 ('engineering', 'Engineering and method', 'sim', 'Every new part starts with a method: gating, risering and feeding simulated before a pattern is made. Worn parts and samples can be reverse-engineered when no drawing exists.', ['Casting simulation', 'Reverse engineering from samples', 'Drawing review and design for casting']),
 ('patterns', 'Pattern shop', 'moulds', 'Patterns are made in-house in wood, polystyrene and metal. More than 10,000 patterns are already on file, so repeat orders go straight to moulding.', ['10,000+ patterns on file', 'Wood, polystyrene and metal patterns', 'Pattern maintenance and modification']),
 ('melting', 'Melting', 'pour2', 'Induction melting in crucibles of up to 6 tonnes, with up to 10 tonnes of liquid metal in a single pour, so heavy single pieces are cast in one go.', ['Induction furnaces, crucibles to 6 t', 'Up to 10 t liquid metal per pour', 'Spectrometer check before tapping']),
 ('moulding', 'Moulding', 'meltshop', 'No-bake Alphaset moulding gives strong, dimensionally stable moulds for pieces from 3 kg to 7,000 kg.', ['Alphaset no-bake process', 'Single pieces 3 kg to 7,000 kg', 'Sand reclamation']),
 ('heat-treatment', 'Heat treatment', 'quench', 'Box and bogie-hearth furnaces up to 12 tonnes, with water and oil quench. Manganese steel goes from furnace to water in about 45 seconds.', ['Furnaces to 12 t', 'Water and oil quench', 'Solution annealing, hardening, tempering']),
 ('machining', 'Machining', 'vtl', 'CNC and conventional vertical turret lathes, vertical machining centres, a plano miller and a special-purpose machine finish parts to drawing.', ['Turning up to 6,500 mm diameter', 'VTL, VMC and plano milling', 'Assembly fit-up checks']),
]
blocks = ''.join(f'''<article class="cblock" id="{k}" data-v="{i}"><span class="n">0{i + 1}</span><h2>{t}</h2><p>{d}</p><ul>{''.join(f'<li>{x}</li>' for x in l)}</ul></article>''' for i, (k, t, v, d, l) in enumerate(CAP))
ONV = 'class="on" '
vids = ''.join(f'<video {ONV if i == 0 else ""}src="{{A}}assets/media/{v}.mp4" poster="{{A}}assets/media/{v}.jpg" muted loop playsinline preload="{"auto" if i == 0 else "none"}" aria-hidden="true"></video>' for i, (k, t, v, d, l) in enumerate(CAP))
page('capabilities', 'Capabilities', 'Engineering, pattern making, melting, moulding, heat treatment and machining, all under one roof in Ajmer.', 'Capabilities',
     hero('Capabilities', 'Everything under one roof', 'From the method to the machined part, nothing that decides the life of a casting leaves our control.', 'furnace') + f'''
<section class="caps"><div class="wrap capgrid">
  <div class="capmedia"><div class="frame">{vids}</div></div>
  <div class="capblocks">{blocks}</div>
</div></section>
<section class="why" aria-labelledby="f-h"><div class="wrap"><div class="narrow" data-r><h2 id="f-h">In figures</h2></div>
<ul class="figs"><li data-r><b><span data-count="7000">7000</span> kg</b>Heaviest single piece</li><li data-r><b><span data-count="6500">6500</span> mm</b>Largest machined diameter</li><li data-r><b><span data-count="10000">10000</span>+</b>Patterns on file</li></ul></div></section>''' + cta(),
     css='''.caps{padding:clamp(72px,9vw,120px) 0}
.capgrid{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:56px;align-items:start}
.capmedia{position:sticky;top:120px}
.capmedia .frame{position:relative;aspect-ratio:4/3.4;overflow:hidden;border-radius:16px;background:var(--black)}
.capmedia video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity .8s,transform 1.4s var(--ease)}
.capmedia video.on{opacity:1;transform:scale(1)}
.cblock{min-height:70svh;display:flex;flex-direction:column;justify-content:center;padding:24px 0;opacity:.28;transition:opacity .5s}
.cblock.on{opacity:1}
.cblock .n{font-size:13px;font-weight:600;color:var(--red);letter-spacing:.1em}
.cblock h2{text-align:left;margin-top:6px}
.cblock ul{list-style:none;margin-top:18px;display:grid;gap:8px}
.cblock li{padding-left:22px;position:relative;color:var(--ink);font-size:15px}
.cblock li::before{content:"";position:absolute;left:0;top:.75em;width:10px;height:2px;background:var(--red)}
.figs{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.figs b{font-size:clamp(32px,3.4vw,48px)!important;font-weight:300;color:var(--ink);letter-spacing:-.02em;text-transform:none!important}
@media (max-width:980px){.capgrid{grid-template-columns:1fr}.capmedia{top:84px;z-index:2}.cblock{min-height:0;opacity:1;padding:40px 0}.figs{grid-template-columns:1fr!important}}''',
     js='''const vs=[...document.querySelectorAll('.capmedia video')];
document.querySelectorAll('.cblock').forEach(b=>ScrollTrigger.create({trigger:b,start:'top 60%',end:'bottom 60%',onToggle:st=>{if(!st.isActive)return;
document.querySelectorAll('.cblock').forEach(x=>x.classList.toggle('on',x===b));const i=+b.dataset.v;vs.forEach((v,k)=>{v.classList.toggle('on',k===i);if(k===i&&!/lite/.test(location.search)){v.preload='auto';v.play().catch(()=>{})}else v.pause()})}}));''')

# ---------------------------------------------------------------- quality
CHAIN = ['Heat number', 'Chemistry', 'Mould', 'Heat treatment', 'Machining', 'Inspection', 'Dispatch']
chain = ''.join(f'<li data-r><i></i><span>{c}</span></li>' for c in CHAIN)
page('quality', 'Quality', 'Laboratory testing, NDT, dimensional checks and full traceability from heat to dispatch. ISO 9001, 14001 and 45001 certified.', 'Quality',
     hero('Quality', 'Traceable to the heat', 'Every heat is tested in our own laboratory, and every casting carries its heat number from the mould to your plant.', 'ut') + f'''
<section class="trace"><div class="wrap"><div class="narrow" data-r><h2>From melt to dispatch</h2><p>One heat number follows the casting through every step, so any report can be traced back to the metal it came from.</p></div>
<ol class="chain">{chain}</ol></div></section>
<section class="qblocks"><div class="wrap qb">
  <figure data-r><video src="{{A}}assets/media/micro.mp4" poster="{{A}}assets/media/micro.jpg" muted loop playsinline preload="none" aria-label="Microstructure examination"></video></figure>
  <div data-r><h2>Laboratory</h2><ul><li>Chemical analysis by spectrometer, before tapping and on the casting</li><li>Hardness testing</li><li>Tensile and impact testing</li><li>Microstructure examination</li></ul></div>
  <div data-r><h2>Non-destructive testing</h2><ul><li>Ultrasonic testing on critical sections</li><li>Magnetic particle inspection</li><li>Dye penetrant testing</li></ul></div>
  <figure data-r><video src="{{A}}assets/media/mpi.mp4" poster="{{A}}assets/media/mpi.jpg" muted loop playsinline preload="none" aria-label="Magnetic particle inspection"></video></figure>
  <figure data-r><video src="{{A}}assets/media/cnc.mp4" poster="{{A}}assets/media/cnc.jpg" muted loop playsinline preload="none" aria-label="Machining and dimensional check"></video></figure>
  <div data-r><h2>Dimensions and fit</h2><ul><li>Dimensional inspection against drawing</li><li>Assembly fit-up checks</li><li>Paint thickness before dispatch</li></ul></div>
</div></section>
<section class="why" aria-labelledby="c-h"><div class="wrap"><div class="narrow" data-r><h2 id="c-h">Certified systems</h2></div>
<ul><li data-r><b>ISO 9001:2015</b>Quality management</li><li data-r><b>ISO 14001:2015</b>Environmental management</li><li data-r><b>ISO 45001:2018</b>Occupational health and safety</li></ul></div></section>''' + cta('Ask for a sample inspection report', 'See exactly what arrives with your castings before you order.', 'Sample inspection report'),
     css='''.trace{padding:clamp(72px,9vw,120px) 0 40px}
.chain{list-style:none;margin-top:56px;display:grid;grid-template-columns:repeat(7,minmax(0,1fr));position:relative}
.chain::before{content:"";position:absolute;left:7%;right:7%;top:11px;height:2px;background:var(--red)}
.chain li{display:grid;justify-items:center;gap:12px;text-align:center;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:var(--ink);position:relative}
.chain i{width:24px;height:24px;border-radius:50%;background:#fff;border:2px solid var(--red);display:grid;place-items:center}
.chain i::after{content:"";width:8px;height:8px;border-radius:50%;background:var(--red)}
.qblocks{padding:40px 0 clamp(72px,9vw,120px)}
.qb{display:grid;grid-template-columns:1fr 1fr;gap:40px 56px;align-items:center}
.qb figure{aspect-ratio:16/10;overflow:hidden;border-radius:14px;background:var(--black)}
.qb video{width:100%;height:100%;object-fit:cover}
.qb h2{text-align:left}
.qb ul{list-style:none;margin-top:16px;display:grid;gap:8px}
.qb li{padding-left:22px;position:relative;color:var(--ink)}
.qb li::before{content:"";position:absolute;left:0;top:.8em;width:10px;height:2px;background:var(--red)}
@media (max-width:980px){.chain{grid-template-columns:repeat(4,minmax(0,1fr));row-gap:28px}.chain::before{display:none}.qb{grid-template-columns:1fr}}''')

# ---------------------------------------------------------------- sustainability
page('sustainability', 'Sustainability', 'Science-based emission targets, 630 kW of rooftop solar and ISO 14001 environmental management at our Ajmer foundry.', 'About',
     hero('<a href="{R}about/">About</a> / Sustainability', 'Responsible foundry', 'Steel that lasts longer is the first saving. We are also cutting the energy and emissions behind every tonne we pour.', 'solar') + '''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">A casting that lasts longer means fewer parts melted, shipped and replaced. That is where our work on grades and methods starts. In the plant, we have set science-based targets for our own emissions and put solar on our roofs.</p></div></section>
<section class="why"><div class="wrap"><ul class="figs">
<li data-r><b><span data-count="19.4" data-dec="1">19.4</span>%</b>Scope 1 emissions reduction target, set to SBTi criteria</li>
<li data-r><b><span data-count="11.2" data-dec="1">11.2</span>%</b>Scope 2 emissions reduction target, set to SBTi criteria</li>
<li data-r><b><span data-count="630">630</span> kW</b>Rooftop solar installed at the plant</li></ul></div></section>
<section class="qblocks"><div class="wrap qb">
<div data-r><h2>Environmental management</h2><ul><li>ISO 14001:2015 certified</li><li>Moulding sand reclaimed and reused</li><li>Steel scrap remelted in induction furnaces</li></ul></div>
<figure data-r><video src="{A}assets/media/aerial.mp4" poster="{A}assets/media/aerial.jpg" muted loop playsinline preload="none" aria-label="The plant from the air"></video></figure>
<figure data-r><video src="{A}assets/media/meltshop.mp4" poster="{A}assets/media/meltshop.jpg" muted loop playsinline preload="none" aria-label="Induction melt shop"></video></figure>
<div data-r><h2>Safe workplace</h2><ul><li>ISO 45001:2018 certified</li><li>Health and safety managed to a certified system</li></ul></div>
</div></section>''' + cta('Talk to us about sustainability data', 'We can share our certificates and emission targets for your supplier assessment.', 'Sustainability information'),
     css='''.figs{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.figs b{font-size:clamp(32px,3.4vw,48px)!important;font-weight:300;color:var(--ink);letter-spacing:-.02em;text-transform:none!important}
.qblocks{padding:clamp(72px,9vw,120px) 0}.qb{display:grid;grid-template-columns:1fr 1fr;gap:40px 56px;align-items:center}
.qb figure{aspect-ratio:16/10;overflow:hidden;border-radius:14px;background:var(--black)}.qb video{width:100%;height:100%;object-fit:cover}
.qb h2{text-align:left}.qb ul{list-style:none;margin-top:16px;display:grid;gap:8px}.qb li{padding-left:22px;position:relative;color:var(--ink)}
.qb li::before{content:"";position:absolute;left:0;top:.8em;width:10px;height:2px;background:var(--red)}
@media (max-width:980px){.figs{grid-template-columns:1fr!important}.qb{grid-template-columns:1fr}}''')

# ---------------------------------------------------------------- about
page('about', 'About us', 'Standard Alloys India: a steel casting foundry in Ajmer since 1991, making wear- and heat-resistant castings for plants worldwide.', 'About',
     hero('About', 'Since 1991', 'A fabrication shop in Ajmer that became a specialist foundry for the parts that wear out first.', 'aerial') + '''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">Standard Alloys India began in 1991 as a fabrication shop in Ajmer, Rajasthan, and lit its first induction furnace in 1994. Over three decades we have built a foundry around one idea: a casting should be specified for the duty it will meet. Today we cast single pieces from 3 kg to 7 tonnes and ship them to plants anywhere in the world.</p></div></section>
<section><div class="wrap timeline">
<div data-r><b>1991</b><span>Starts as a fabrication shop in Ajmer</span></div>
<div data-r><b>1994</b><span>First induction furnace, the start of the foundry</span></div>
<div data-r><b>Today</b><span>Castings to 7 tonnes, machined to 6,500 mm, shipped worldwide</span></div></div></section>
<section class="why"><div class="wrap"><div class="narrow" data-r><h2>How we work</h2></div>
<ul><li data-r><b>Duty first</b>We ask where a part runs and how it fails before we recommend a grade.</li>
<li data-r><b>In-house control</b>Method, pattern, melt, heat treatment, machining and testing under one roof.</li>
<li data-r><b>Evidence with every casting</b>Chemistry, hardness and NDT reports, traceable to the heat.</li></ul></div></section>
<section class="aboutlinks"><div class="wrap al">
<a href="{R}capabilities/" data-r><video src="{A}assets/media/vtl.mp4" poster="{A}assets/media/vtl.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Capabilities</span></a>
<a href="{R}quality/" data-r><video src="{A}assets/media/ut.mp4" poster="{A}assets/media/ut.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Quality</span></a>
<a href="{R}sustainability/" data-r><video src="{A}assets/media/solar.mp4" poster="{A}assets/media/solar.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Sustainability</span></a>
<a href="{R}careers/" data-r><video src="{A}assets/media/grind.mp4" poster="{A}assets/media/grind.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><span>Careers</span></a>
</div></section>''' + cta('Work with us', 'Send a drawing, a sample or a worn part, and we will take it from there.'),
     css='''.timeline{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;padding:24px 0 72px}
.timeline b{display:block;font-size:clamp(40px,4vw,56px);font-weight:400;color:#d6d6da;line-height:1}
.timeline span{display:block;margin-top:10px;font-weight:600;color:var(--ink);font-size:15px;max-width:26ch}
.aboutlinks{padding:clamp(72px,9vw,120px) 0 0}
.al{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.al a{position:relative;aspect-ratio:3/4;overflow:hidden;border-radius:14px;color:#fff;text-decoration:none;background:var(--black)}
.al video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.al a::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(0,0,0,.7))}
.al span{position:absolute;z-index:1;left:20px;bottom:18px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.al a:hover video{transform:scale(1.06)}
@media (max-width:980px){.timeline{grid-template-columns:1fr}.al{grid-template-columns:1fr 1fr}}''')

# ---------------------------------------------------------------- careers
TEAMS = [('Melting and moulding', 'meltshop'), ('Metallurgy and laboratory', 'micro'), ('Heat treatment', 'quench'), ('Machining', 'drill'),
         ('Quality and NDT', 'mpi'), ('Engineering and design', 'sim'), ('Sales and export', 'jaws'), ('Maintenance', 'cnc')]
teams = ''.join(f'<figure data-r><video src="{{A}}assets/media/{v}.mp4" poster="{{A}}assets/media/{v}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video><figcaption>{t}</figcaption></figure>' for t, v in TEAMS)
page('careers', 'Careers', 'Careers at Standard Alloys India: foundry, metallurgy, machining, quality, engineering and export roles in Ajmer.', 'About',
     hero('<a href="{R}about/">About</a> / Careers', 'Make castings that matter', 'Join the people who melt, mould, treat, machine and test parts that keep plants running.', 'sparks') + f'''
<section class="intro"><div class="wrap narrow" data-r><p class="lit">A foundry runs on skill. We look for people who take pride in exact work, from the melt shop to the laboratory, and we train them on real parts for real plants.</p></div></section>
<section class="teams"><div class="wrap"><div class="narrow" data-r><h2>Where you could work</h2></div><div class="tg">{teams}</div></div></section>
<section class="quote" id="quote"><div class="wrap"><div class="narrow" data-r><h2>Current openings</h2><p>Openings and the application form appear here.</p></div>
<div class="rfq" data-webform="" data-title="Job application" style="margin-top:40px"><div><h3>Apply or send your CV</h3><p>The online application form will appear here. Until then, write to us with the role you are interested in.</p><div class="acts"><a class="btn" href="mailto:{MAIL}?subject=Career%20enquiry">Email your CV</a></div></div></div></div></section>''',
     css='''.teams{padding:24px 0 clamp(72px,9vw,120px)}
.tg{margin-top:44px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.tg figure{position:relative;aspect-ratio:1/1;overflow:hidden;border-radius:14px;background:var(--black)}
.tg video{width:100%;height:100%;object-fit:cover;filter:grayscale(.6);transition:filter .6s,transform 1.2s var(--ease)}
.tg figure:hover video{filter:none;transform:scale(1.05)}
.tg figure::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.7))}
.tg figcaption{position:absolute;z-index:1;left:18px;right:18px;bottom:16px;color:#fff;font-weight:600;font-size:14px;text-transform:uppercase;letter-spacing:.04em}
@media (max-width:980px){.tg{grid-template-columns:1fr 1fr}}''')

# ---------------------------------------------------------------- contact
page('contact', 'Contact and request a quote', 'Send a drawing for a quotation, or contact Standard Alloys India in Ajmer, India.', 'Contact',
     hero('Contact', 'Send us your drawing', 'A metallurgist reviews every enquiry and replies with a price, a lead time or the right questions.', 'drill') + f'''
<section class="quote" id="quote"><div class="wrap qgrid">
  <div data-r>
    <h2 style="text-align:left">What to include</h2>
    <ul style="margin-top:18px"><li>Drawing as PDF, DWG, DXF or STEP</li><li>Grade, or how and where the part is used</li><li>Quantity and annual volume</li><li>As cast or machined</li></ul>
    <p class="note">No drawing? Send the worn part or photographs with key dimensions, and we will reverse-engineer it.</p>
  </div>
  <!-- ERPNext Web Form slot: put the Web Form URL from saconnect.frappe.cloud in data-webform -->
  <div class="rfq" data-webform="" data-title="Request for quotation" data-r><div><h3>Request for quotation</h3><p>The online upload form will appear here. Until then, email the drawing to our sales desk.</p>
    <div class="acts"><a class="btn" id="mail" href="mailto:{MAIL}?subject=Request%20for%20quotation">Email the drawing</a><a class="btn ghost" href="tel:+911452695110">Call {PHONE}</a></div></div></div>
</div></section>
<section class="visit"><div class="wrap vg">
  <div data-r><h2 style="text-align:left">Visit the foundry</h2>
    <address><b>Standard Alloys India Pvt. Ltd.</b><br>F-26B &amp; 27, Parbatpura Industrial Area<br>Ajmer 305002, Rajasthan, India</address>
    <p><a href="tel:+911452695110">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
  <iframe data-r title="Map of Standard Alloys India, Parbatpura Industrial Area, Ajmer" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Parbatpura%20Industrial%20Area%2C%20Ajmer%20305002&amp;z=14&amp;output=embed"></iframe>
</div></section>''',
     css='''.visit{padding:0 0 clamp(72px,9vw,120px)}
.vg{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:48px;align-items:center}
.vg address{font-style:normal;margin-top:18px;color:var(--ink);line-height:1.8}.vg b{font-weight:600}
.vg p{margin-top:14px}.vg a{color:var(--red);text-decoration:none}.vg a:hover{text-decoration:underline}
.vg iframe{width:100%;aspect-ratio:16/10;border:0;border-radius:14px;filter:grayscale(.3)}
@media (max-width:980px){.vg{grid-template-columns:1fr}}''')
