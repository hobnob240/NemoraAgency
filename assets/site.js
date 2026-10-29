// NEMORA — small progressive enhancements. Everything works without JavaScript.
(function () {
  // header: solid background once the page scrolls
  var head = document.querySelector('.site-head');
  var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 8); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  var setMenu = function (open) {
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    nav.classList.toggle('open', open);
    head.classList.toggle('open', open);
  };
  if (btn && nav) {
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); btn.focus(); } });
    window.matchMedia('(min-width: 861px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  // reveal on scroll, once; children of [data-stagger] get a small cascade
  document.querySelectorAll('[data-stagger]').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (el, i) { el.classList.add('reveal'); el.style.setProperty('--i', Math.min(i, 6)); });
  });
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  // contact form: opens the visitor's email app with the details filled in
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('form-msg');
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var v = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ''; };
      var to = form.getAttribute('data-to');
      var subject = 'Website enquiry from ' + v('name') + (v('business') ? ' (' + v('business') + ')' : '');
      var body = [
        'Name: ' + v('name'),
        'Email: ' + v('email'),
        v('phone') ? 'Phone: ' + v('phone') : '',
        v('business') ? 'Business: ' + v('business') : '',
        'Looking for: ' + v('need'),
        '',
        v('message')
      ].filter(function (l, i) { return l !== '' || i === 5; }).join('\n');
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      msg.hidden = false;
      msg.className = 'form-msg';
      msg.textContent = 'Your email app should now open with your message ready to send. If nothing happened, email us directly at ' + to + '.';
    });
  }

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
