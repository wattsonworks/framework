/* ============ LIQUIDEX Framework — app.js (institutional) ============ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* year */
  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* mobile nav */
  var toggle = document.getElementById('nav-toggle'), links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* price reveal — keep the price off the page until asked for */
  var priceBtn = document.getElementById('price-reveal'), amt = document.getElementById('offer-amt');
  if (priceBtn && amt) priceBtn.addEventListener('click', function () {
    amt.hidden = false; amt.classList.add('show');
    priceBtn.setAttribute('aria-expanded', 'true'); priceBtn.hidden = true;
  });

  /* reveal on scroll */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* animated counters (.mv) */
  function fmt(val, decimals, suffix) {
    var s = decimals ? val.toFixed(decimals) : Math.round(val).toLocaleString('en-US');
    return s + (suffix || '');
  }
  function animate(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    if (isNaN(target)) return;
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var dur = 1300, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased, decimals, suffix);
      if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target, decimals, suffix);
    }
    requestAnimationFrame(step);
  }
  var nums = document.querySelectorAll('.mv[data-count]');
  if ('IntersectionObserver' in window && !reduce) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { animate(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.5 });
    nums.forEach(function (el) { co.observe(el); });
  }

  /* topbar hairline shadow on scroll */
  var bar = document.querySelector('.topbar');
  window.addEventListener('scroll', function () {
    if (bar) bar.style.borderBottomColor = window.scrollY > 8 ? 'rgba(236,233,225,.18)' : '';
  }, { passive: true });
})();

/* ============ Cross-section table — render / sort / filter ============ */
(function () {
  'use strict';
  var SCAN = window.SCAN;
  var body = document.getElementById('xbody');
  if (!SCAN || !body) return;
  var rows = SCAN.rows.slice();
  var isSafe = function (r) { return r.dd <= 15 && r.pf >= 1.3; };

  var state = { filter: 'all', sortKey: 'pf', sortDir: -1 };

  function pfClass(r) {
    if (r.pf >= 2 && r.dd < 15) return 'pf-star';
    if (r.pf >= 1.5) return 'pf-strong';
    if (r.pf >= 1) return 'pf-ok';
    return 'pf-neg';
  }
  function ddClass(r) { return r.dd <= 12 ? 'ddlow' : (r.dd >= 30 ? 'ddhi' : ''); }
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }

  function confHTML(conf) {
    return conf.map(function (c, i) {
      var cls = i === 0 ? 'cbadge dir' : 'cbadge';
      return '<span class="' + cls + '">' + esc(c) + '</span>';
    }).join('');
  }

  function matches(r) {
    var f = state.filter;
    if (f === 'all') return true;
    if (f === 'safe') return isSafe(r);
    if (f === 'tuned') return r.tuned;
    if (f === 'fade' || f === 'continuation') return r.family === f;
    return r.sector === f;
  }

  function render() {
    var list = rows.filter(matches);
    var k = state.sortKey, dir = state.sortDir;
    list.sort(function (a, b) {
      var av = a[k], bv = b[k];
      if (typeof av === 'string') return av < bv ? -dir : av > bv ? dir : 0;
      return (av - bv) * dir;
    });
    if (!list.length) { body.innerHTML = '<tr><td colspan="11" class="xempty">No instruments in this view.</td></tr>'; return; }
    body.innerHTML = list.map(function (r) {
      var tune = r.tuned
        ? '<span class="tunepill deep" title="Micro-tuned (deep), verified live — PF ' + r.deepPF + ' at ' + r.deepDD + '% drawdown">✓ ' + r.deepPF + ' · ' + r.deepDD + '%</span>'
        : '<span class="tunepill greedy" title="Not micro-tuned yet — greedy pass at default params">✗</span>';
      return '<tr class="' + (r.pf < 1 ? 'row-loss' : '') + (r.tuned ? ' row-tuned' : '') + '">' +
        '<td class="sym">' + esc(r.sym) + '</td>' +
        '<td class="sec">' + esc(r.sectorLabel) + '</td>' +
        '<td><span class="fampill ' + r.family + '">' + esc(r.family) + '</span></td>' +
        '<td class="r base">' + r.base.toFixed(3) + '</td>' +
        '<td class="r pf ' + pfClass(r) + '">' + r.pf.toFixed(3) + '</td>' +
        '<td class="r lift">' + (r.lift != null ? r.lift.toFixed(2) + '×' : '—') + '</td>' +
        '<td class="r dd ' + ddClass(r) + '">' + r.dd.toFixed(1) + '%</td>' +
        '<td class="r win">' + r.win.toFixed(0) + '%</td>' +
        '<td class="r tr">' + r.trades + '</td>' +
        '<td class="tunecell">' + tune + '</td>' +
        '<td class="confcell">' + confHTML(r.conf) + '</td>' +
      '</tr>';
    }).join('');
  }

  function markHeaders() {
    document.querySelectorAll('#xtable thead th[data-sort]').forEach(function (th) {
      th.classList.remove('sorted-asc', 'sorted-desc');
      if (th.getAttribute('data-sort') === state.sortKey)
        th.classList.add(state.sortDir === 1 ? 'sorted-asc' : 'sorted-desc');
    });
  }

  /* sortable headers */
  document.querySelectorAll('#xtable thead th[data-sort]').forEach(function (th) {
    th.addEventListener('click', function () {
      var key = th.getAttribute('data-sort');
      if (state.sortKey === key) { state.sortDir *= -1; }
      else { state.sortKey = key; state.sortDir = (key === 'sym' || key === 'sectorLabel' || key === 'family') ? 1 : -1; }
      markHeaders(); render();
    });
  });

  /* filter chips */
  var chips = document.querySelectorAll('#xfilters .xchip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('on'); });
      chip.classList.add('on');
      state.filter = chip.getAttribute('data-filter');
      render();
    });
  });

  markHeaders();
  render();
})();
