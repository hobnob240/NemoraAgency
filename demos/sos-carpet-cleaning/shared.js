/* SOS Carpet Cleaning demo: shared data between the booking page and the admin. Demo only: stored in this browser. */
window.SOS = (function () {
  var KEY = 'sos-demo-bookings-v1';
  var ITEMS = [
    { id: 'lounge', name: 'Living room carpet', group: 'Carpets', price: 40 },
    { id: 'bedroom', name: 'Bedroom carpet', group: 'Carpets', price: 30 },
    { id: 'stairs', name: 'Stairs and landing', group: 'Carpets', price: 45 },
    { id: 'hall', name: 'Hallway', group: 'Carpets', price: 25 },
    { id: 'sofa3', name: '3-seater sofa', group: 'Sofas and chairs', price: 55 },
    { id: 'sofa2', name: '2-seater sofa', group: 'Sofas and chairs', price: 45 },
    { id: 'chair', name: 'Armchair', group: 'Sofas and chairs', price: 25 },
    { id: 'rug', name: 'Rug', group: 'Rugs', price: 30 }
  ];
  var SLOTS = ['Morning, 8 to 12', 'Afternoon, 12 to 4', 'Evening, 4 to 8'];
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
  function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }
  function add(b) { var l = load(); l.push(b); save(l); }
  function day(offset) { var d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + offset); return d; }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function fmt(isoStr) { var p = isoStr.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2]); return DAYS[d.getDay()] + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()]; }
  function itemsText(items) { return Object.keys(items).filter(function (k) { return items[k] > 0; }).map(function (k) { var it = ITEMS.find(function (x) { return x.id === k; }); var n = it.name.toLowerCase(); return items[k] > 1 ? items[k] + ' x ' + (/s$/.test(n) || / and /.test(n) ? n : n + 's') : n; }).join(', '); }
  function total(items, prices) { return Object.keys(items).reduce(function (s, k) { var it = ITEMS.find(function (x) { return x.id === k; }); return s + (items[k] || 0) * ((prices && prices[k] != null) ? prices[k] : it.price); }, 0); }
  /* a slot is taken if the admin's sample week, or a stored booking, already uses it */
  function taken(dIso, slot) { return load().some(function (b) { return b.date === dIso && b.slot === slot; }) || ((dIso.charCodeAt(9) + slot.length) % 4 === 0); }
  return { ITEMS: ITEMS, SLOTS: SLOTS, load: load, save: save, add: add, day: day, iso: iso, fmt: fmt, itemsText: itemsText, total: total, taken: taken, DAYS: DAYS, MONTHS: MONTHS };
})();
