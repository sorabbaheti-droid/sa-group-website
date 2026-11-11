// Home page: results appear as the visitor types a casting name.
// Also hands the part photo to the next page so it travels there (view transitions).
(() => {
  const here = document.currentScript.src;
  const DATA = new URL('../parts.json', here), IMG = new URL('../cutouts/', here);

  document.addEventListener('click', e => {
    const l = e.target.closest('a[href*="products/"]'); if (!l) return;
    const im = l.querySelector('img'); if (!im) return;
    document.querySelectorAll('[style*="view-transition-name"]').forEach(x => x.style.viewTransitionName = '');
    im.style.viewTransitionName = 'part';
    try { sessionStorage.setItem('vtPart', '1'); } catch (_) {}
  });

  const form = document.querySelector('.bigsearch.home'); if (!form) return;
  const input = form.querySelector('input[type=search]'), box = form.querySelector('.bs');
  const list = document.createElement('div');
  list.className = 'ta'; list.id = 'ta-list'; list.setAttribute('role', 'listbox'); list.hidden = true;
  box.after(list);
  input.setAttribute('role', 'combobox'); input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-controls', 'ta-list'); input.setAttribute('aria-expanded', 'false'); input.autocomplete = 'off';

  let parts = null, active = -1, rows = [];
  const load = () => parts ? Promise.resolve(parts) : fetch(DATA).then(r => r.json()).then(d => (parts = d)).catch(() => (parts = []));
  const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mark = (name, q) => { const i = name.toLowerCase().indexOf(q); return i < 0 ? esc(name) : esc(name.slice(0, i)) + '<mark>' + esc(name.slice(i, i + q.length)) + '</mark>' + esc(name.slice(i + q.length)); };

  function find(q) {
    const words = q.split(/\s+/).filter(Boolean), out = [];
    for (const p of parts) {
      const name = p.n.toLowerCase();
      if (!words.every(w => p.k.includes(w) || p.k.includes(w.replace(/s$/, '')))) continue;
      out.push([name.startsWith(q) ? 0 : name.includes(q) ? 1 : words.every(w => name.includes(w)) ? 2 : 3, p]);
    }
    return out.sort((a, b) => a[0] - b[0]).slice(0, 6).map(x => x[1]);
  }

  function close() { list.hidden = true; active = -1; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); }
  function setActive(i) {
    rows.forEach((r, k) => r.classList.toggle('on', k === i)); active = i;
    if (i >= 0) { input.setAttribute('aria-activedescendant', rows[i].id); rows[i].scrollIntoView({ block: 'nearest' }); } else input.removeAttribute('aria-activedescendant');
  }
  function render() {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) return close();
    const hits = find(q), all = 'products/?q=' + encodeURIComponent(input.value.trim());
    let h = hits.map((p, i) => `<a role="option" id="ta-${i}" href="products/${p.s}/">${p.i ? `<img src="${IMG}${p.i}.webp" alt="" width="64" height="48">` : '<i aria-hidden="true"></i>'}<span><b>${mark(p.n, q)}</b><small>${esc(p.f)}</small></span></a>`).join('');
    h += hits.length
      ? `<a role="option" id="ta-${hits.length}" class="all" href="${all}">See every match in the catalogue</a>`
      : `<a role="option" id="ta-0" class="all" href="contact/?part=${encodeURIComponent(input.value.trim())}#quote">No match in the catalogue yet. Ask us about this part</a>`;
    list.innerHTML = h; rows = [...list.querySelectorAll('a')]; list.hidden = false; active = -1; input.setAttribute('aria-expanded', 'true');
  }

  input.addEventListener('focus', () => load().then(render), { once: false });
  input.addEventListener('input', () => load().then(render));
  input.addEventListener('keydown', e => {
    if (list.hidden) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive((active + 1) % rows.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active <= 0 ? rows.length - 1 : active - 1); }
    else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); rows[active].click(); }
    else if (e.key === 'Escape') close();
  });
  document.addEventListener('click', e => { if (!form.contains(e.target)) close(); });
})();
