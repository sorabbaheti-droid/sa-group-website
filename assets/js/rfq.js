// Quote request: works with a drawing, photographs, or only the equipment model.
// Until the ERPNext Web Form is connected, it prepares an email with everything filled in.
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
      location.href = `mailto:${MAIL}?subject=${encodeURIComponent('Request for quotation: ' + v('part'))}&body=${encodeURIComponent(body)}`;
      f.querySelector('.msg').textContent = 'Your email app should now be open with the enquiry filled in. Attach your drawing or photographs and press send. If nothing opened, write to ' + MAIL + '.';
    });
  });
})();
