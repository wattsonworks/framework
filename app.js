/* ============ SurgeGuru Framework — app.js ============ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* year */
  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* price reveal — keep the price off the page until asked for */
  var priceBtn = document.getElementById('price-reveal'), amt = document.getElementById('offer-amt');
  if (priceBtn && amt) priceBtn.addEventListener('click', function () {
    amt.hidden = false;
    amt.classList.remove('is-hidden');
    amt.classList.add('show');
    priceBtn.setAttribute('aria-expanded', 'true');
    priceBtn.hidden = true;
  });

  /* nav toggle */
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

  /* nav shadow on scroll */
  var nav = document.getElementById('nav');
  window.addEventListener('scroll', function () {
    if (nav) nav.style.boxShadow = window.scrollY > 8 ? '0 8px 30px rgba(0,0,0,.4)' : 'none';
  }, { passive: true });

  /* reveal on scroll */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* animated counters */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var dur = 1400, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = target * eased;
      el.textContent = (decimals ? val.toFixed(decimals) : Math.round(val).toLocaleString('en-US')) + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = (decimals ? target.toFixed(decimals) : Math.round(target).toLocaleString('en-US')) + suffix;
    }
    requestAnimationFrame(step);
  }
  var nums = document.querySelectorAll('.stat-num');
  if ('IntersectionObserver' in window && !reduce) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { animateCount(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (el) { co.observe(el); });
  } else {
    nums.forEach(function (el) {
      var d = parseInt(el.getAttribute('data-decimals') || '0', 10);
      el.textContent = parseFloat(el.getAttribute('data-count')).toFixed(d) + (el.getAttribute('data-suffix') || '');
    });
  }

  /* ticker */
  var ticker = document.getElementById('ticker');
  if (ticker) {
    var feed = [
      ['GOOGL', 'PF 2.30', 'up'], ['MU', 'PF 2.08', 'up'], ['TSEM', 'PF 2.78', 'up'],
      ['LRCX', 'PF 1.89', 'up'], ['AMAT', 'PF 1.79', 'up'], ['CAT', 'PF 1.74', 'up'],
      ['WMT', 'PF 1.70', 'up'], ['TSLA', 'PF 1.63', 'up'], ['RISK', '0.38', 'dn'], ['KEEPER', 'RANKING', 'up']
    ];
    var html = '';
    for (var rep = 0; rep < 2; rep++) {
      feed.forEach(function (f) { html += '<span>' + f[0] + ' <b class="' + f[2] + '">' + f[1] + '</b></span>'; });
    }
    ticker.innerHTML = html;
  }

  /* risk value flicker + signal rotation (subtle, decorative) */
  if (!reduce) {
    var riskEl = document.getElementById('risk-val');
    if (riskEl) setInterval(function () {
      var v = (0.30 + Math.random() * 0.30).toFixed(2);
      riskEl.textContent = v;
      riskEl.style.color = v > 0.55 ? '#ff3b5c' : (v < 0.40 ? '#00e5a0' : '#e8edf5');
    }, 2600);

    var sig = document.getElementById('t-signal'), asset = document.getElementById('t-asset'), pf = document.getElementById('t-pf');
    var setups = [
      ['GOOGL · 45M', 'MEGA-TECH · OFF', '2.30'],
      ['MU · 5M', 'SEMIS · OFF', '2.08'],
      ['TSEM · 1H', 'SEMIS · OFF', '2.78'],
      ['AMAT · 1H', 'SEMIS · BRK ON', '1.79']
    ];
    var si = 0;
    if (sig && asset && pf) setInterval(function () {
      si = (si + 1) % setups.length;
      sig.style.opacity = '0'; asset.style.opacity = '0'; pf.style.opacity = '0';
      setTimeout(function () {
        sig.textContent = setups[si][0]; asset.textContent = setups[si][1]; pf.textContent = setups[si][2];
        sig.style.opacity = asset.style.opacity = pf.style.opacity = '1';
      }, 320);
    }, 3800);
    [sig, asset, pf].forEach(function (el) { if (el) el.style.transition = 'opacity .3s'; });
  }

  /* canvas background — drifting node grid with surge pulses */
  var canvas = document.getElementById('bg-canvas');
  if (canvas && !reduce) {
    var ctx = canvas.getContext('2d'), W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var nodes = [];
    function resize() {
      var cw = document.documentElement.clientWidth, chh = window.innerHeight;
      W = canvas.width = cw * dpr; H = canvas.height = chh * dpr;
      canvas.style.width = cw + 'px'; canvas.style.height = chh + 'px';
      var count = Math.min(70, Math.floor(cw / 26));
      nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.18 * dpr, vy: (Math.random() - 0.5) * 0.18 * dpr,
          r: (Math.random() * 1.4 + 0.6) * dpr, pulse: Math.random()
        });
      }
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      var maxd = 130 * dpr;
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.x += n.vx; n.y += n.vy; n.pulse += 0.01;
        if (n.x < 0 || n.x > W) n.vx *= -1;
        if (n.y < 0 || n.y > H) n.vy *= -1;
        for (var j = i + 1; j < nodes.length; j++) {
          var m = nodes[j], dx = n.x - m.x, dy = n.y - m.y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < maxd) {
            var a = (1 - d / maxd) * 0.22;
            ctx.strokeStyle = 'rgba(34,211,238,' + a + ')';
            ctx.lineWidth = 0.6 * dpr;
            ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(m.x, m.y); ctx.stroke();
          }
        }
        var glow = (Math.sin(n.pulse) * 0.5 + 0.5);
        ctx.fillStyle = 'rgba(0,229,160,' + (0.35 + glow * 0.4) + ')';
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r + glow * 0.6 * dpr, 0, Math.PI * 2); ctx.fill();
      }
      requestAnimationFrame(draw);
    }
    resize(); draw();
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(resize, 200); });
  }
})();
