// Quote request: works with a drawing, photographs, or only the equipment model.
// Until the ERPNext Web Form is connected, it prepares the enquiry and offers Gmail, Outlook, email app or copy.
(function () {
  const MAIL = 'sales@standardalloysindia.com';
  const part = new URLSearchParams(location.search).get('part');
  document.querySelectorAll('[data-rfq]').forEach(f => {
    if (part && f.part) f.part.value = part;
    let cond = 'Not sure';
    f.querySelectorAll('.seg button').forEach(b => {
      b.setAttribute('aria-pressed', b.classList.contains('on'));
      b.addEventListener('click', () => { cond = b.dataset.c; f.querySelectorAll('.seg button').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); }); });
    });
    f.querySelectorAll('.have button').forEach(b => {
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => { const on = !b.classList.contains('on'); b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); });
    });
    const rec = f.querySelector('[name=rec]'), grade = f.querySelector('[name=grade]');
    if (rec && grade) { grade.addEventListener('input', () => { if (grade.value.trim()) rec.checked = false; }); }
    f.addEventListener('submit', e => {
      e.preventDefault();
      let ok = true;
      ['part', 'email'].forEach(n => { const el = f.querySelector(`[name=${n}]`); const bad = !el.value.trim() || (n === 'email' && !/^\S+@\S+\.\S+$/.test(el.value)); el.setAttribute('aria-invalid', bad); if (bad && ok) { el.focus(); ok = false; } });
      if (!ok) { f.querySelector('.msg').textContent = 'Please add the part and an email address. Everything else is optional.'; return; }
      const v = n => (f.querySelector(`[name=${n}]`) || {}).value?.trim() || '';
      const have = [...f.querySelectorAll('.have button.on')].map(b => b.textContent).join(', ') || 'Not stated';
      const body = [
        `Part: ${v('part')}`,
        `What I can send: ${have}`,
        `Equipment, OEM and model: ${v('equip') || 'Not stated'}`,
        `Material or grade: ${v('grade') || 'Not known'}${rec && rec.checked ? ' (please recommend)' : ''}`,
        `Quantity: ${v('qty') || 'Not stated'}`,
        `Condition: ${cond}`,
        `Notes: ${v('notes') || '-'}`,
        '',
        `Name: ${v('name')}`, `Company: ${v('company')}`, `Email: ${v('email')}`, `Country: ${v('country')}`,
        '',
        'Drawing, photographs or other files attached.'
      ].join('\n');
      const sub = 'Request for quotation: ' + v('part'), eS = encodeURIComponent(sub), eB = encodeURIComponent(body);
      let box = f.querySelector('.sendbox');
      if (!box) { box = document.createElement('div'); box.className = 'sendbox'; f.querySelector('.msg').after(box); }
      box.innerHTML = `<p><b>Your enquiry is ready.</b> Send it from your email, then attach your drawing or photographs.</p>
        <div class="sendrow"><a class="btn" target="_blank" rel="noopener" href="https://mail.google.com/mail/?view=cm&fs=1&to=${MAIL}&su=${eS}&body=${eB}">Gmail</a>
        <a class="btn" target="_blank" rel="noopener" href="https://outlook.office.com/mail/deeplink/compose?to=${MAIL}&subject=${eS}&body=${eB}">Outlook</a>
        <a class="btn ghost" href="mailto:${MAIL}?subject=${eS}&body=${eB}">Email app</a>
        <button type="button" class="btn ghost" data-copy>Copy enquiry</button></div>
        <p class="sendalt">Or write to <a href="mailto:${MAIL}">${MAIL}</a> and paste the enquiry.</p>`;
      box.querySelector('[data-copy]').addEventListener('click', ev => {
        const t = `To: ${MAIL}\nSubject: ${sub}\n\n${body}`;
        (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => { ev.target.textContent = 'Copied'; }, () => { const ta = document.createElement('textarea'); ta.value = t; document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove(); ev.target.textContent = 'Copied'; });
      });
      f.querySelector('.msg').textContent = '';
      box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  });
})();
