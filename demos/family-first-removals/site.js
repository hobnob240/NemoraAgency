/* Family First Removals demo: year in footer, quote form (demo: shows what happens, sends nothing). */
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
