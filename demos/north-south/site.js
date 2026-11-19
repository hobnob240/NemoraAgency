(function () {
  var now = new Date();
  // today's row in the hours table (Monday = 0)
  var d = (now.getDay() + 6) % 7;
  document.querySelectorAll('.hours tr[data-day="' + d + '"]').forEach(function (r) { r.classList.add('is-today'); });

  // hide events that have passed
  var today = now.toISOString().slice(0, 10);
  document.querySelectorAll('.ev[data-date]').forEach(function (e) { if (e.getAttribute('data-date') < today) e.remove(); });
  document.querySelectorAll('.events').forEach(function (l) {
    if (!l.children.length) { var m = l.parentNode.querySelector('.ev-empty'); if (m) m.hidden = false; l.remove(); }
  });
  document.querySelectorAll('.fr-dates li').forEach(function (li) {
    var t = li.querySelector('time'); if (t && t.getAttribute('datetime') < today) li.remove();
  });

  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = now.getFullYear(); });

  // map loads only when asked (Google may set cookies)
  var btn = document.querySelector('[data-load-map]');
  if (btn) btn.addEventListener('click', function () {
    var box = btn.closest('.map');
    var f = document.createElement('iframe');
    f.src = box.getAttribute('data-map');
    f.title = 'Map showing North South, 25a Bootham, York';
    f.loading = 'lazy';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    box.innerHTML = '';
    box.appendChild(f);
  });
})();
