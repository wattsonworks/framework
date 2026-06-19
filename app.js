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
