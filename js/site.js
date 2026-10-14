/* Menu toggle, and the market tape on the front page: three synthetic markets
   that receive the same shock, drawn once from a seeded random walk. */
(function () {
  'use strict';

  var btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var canvas = document.getElementById('tape');
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext('2d');

  // ---- the three worlds ---------------------------------------------------
  var N = 600, SHOCK = 280, THROTTLE = SHOCK + 25;
  var END = { quiet: 1.0110, herd: 0.9002, throttle: 0.9367 };

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function gaussian(rand) {
    var u = 0, v = 0;
    while (u === 0) u = rand();
    while (v === 0) v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  var rand = mulberry32(20260908), noise = [], extra = [], i;
  for (i = 0; i < N; i++) { noise.push(gaussian(rand)); extra.push(gaussian(rand)); }

  function envelopeHerd(t) {
    var s = t - SHOCK;
    if (s < 0) return 0;
    var fall = -0.115 * (1 - Math.exp(-s / 38));
    var wave = 0.028 * Math.sin(s / 21) * Math.exp(-s / 150);
    return fall + wave + 0.015 * (1 - Math.exp(-s / 160));
  }
  var series = { quiet: [], herd: [], throttle: [] };
  var p = 1, pH = 1, pT = 1, rH = 0, rT = 0, eT0 = 0, t;
  for (t = 0; t < N; t++) {
    var base = 0.0011 * noise[t] - 0.03 * (p - 1);
    p *= 1 + base; series.quiet.push(p);
    if (t < SHOCK) { series.herd.push(p); series.throttle.push(p); pH = p; pT = p; continue; }
    // herd: the same innovations, amplified, with momentum, around a cascade envelope
    var eH = envelopeHerd(t);
    rH = 0.0022 * extra[t] + 0.35 * rH;
    pH = series.quiet[t] * (1 + eH) * (1 + rH * 0.6);
    series.herd.push(pH);
    // throttle: follows the herd until the rule engages, then the cascade is damped
    if (t < THROTTLE) { series.throttle.push(pH); eT0 = eH; continue; }
    var u = (t - THROTTLE) / 70;
    var eT = eT0 + (-0.062 - eT0) * (1 - Math.exp(-u));
    rT = 0.0014 * extra[t] + 0.12 * rT;
    pT = series.quiet[t] * (1 + eT) * (1 + rT * 0.6);
    series.throttle.push(pT);
  }
  // pin the closing values with a smooth correction from the shock onwards
  function pin(arr, target, from) {
    var d = target - arr[N - 1], span = N - 1 - from, k;
    for (k = from; k < N; k++) { var x = (k - from) / span, s = x * x * (3 - 2 * x); arr[k] += d * s; }
  }
  pin(series.quiet, END.quiet, 0); pin(series.herd, END.herd, SHOCK); pin(series.throttle, END.throttle, THROTTLE);

  // ---- drawing -----------------------------------------------------------
  var COL = { quiet: '#c7cfdc', herd: '#ff6b6b', throttle: '#6cb5ff', amber: '#f2b32a', grid: 'rgba(148,163,196,.11)', grid2: 'rgba(148,163,196,.22)', text: '#5d6a80', text2: '#97a3b8', ink: '#10161f', ink3: '#161e2a' };
  var Y0 = 0.80, Y1 = 1.10, PAD = { l: 0, r: 76, t: 36, b: 34 };
  var W = 0, H = 0, dpr = 1;

  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var rect = canvas.getBoundingClientRect();
    W = Math.max(320, Math.round(rect.width)); H = Math.max(240, Math.round(rect.height));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function X(k) { return PAD.l + (W - PAD.l - PAD.r) * k / (N - 1); }
  function Y(v) { return PAD.t + (H - PAD.t - PAD.b) * (Y1 - v) / (Y1 - Y0); }

  function chip(x, y, name, value, color, align) {
    ctx.font = '500 11px "JetBrains Mono", ui-monospace, Menlo, monospace';
    var txt = value.toFixed(4), w1 = ctx.measureText(name).width + 14, w2 = ctx.measureText(txt).width + 14, h = 20;
    var x0 = align === 'left' ? x : x - w1 - w2;
    y = Math.max(PAD.t + h / 2, Math.min(H - PAD.b - h / 2, y));
    ctx.fillStyle = COL.ink3; ctx.fillRect(x0, y - h / 2, w1, h);
    ctx.fillStyle = color; ctx.fillRect(x0 + w1, y - h / 2, w2, h);
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#e4e9f2'; ctx.fillText(name, x0 + 7, y + 0.5);
    ctx.fillStyle = '#0b0f16'; ctx.fillText(txt, x0 + w1 + 7, y + 0.5);
  }

  function draw(progress) {
    ctx.clearRect(0, 0, W, H);
    var k = Math.max(1, Math.min(N - 1, Math.floor(progress * (N - 1))));
    // grid
    ctx.lineWidth = 1; ctx.strokeStyle = COL.grid; ctx.fillStyle = COL.text;
    ctx.font = '400 11px "JetBrains Mono", ui-monospace, Menlo, monospace'; ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    var v;
    for (v = Y0; v <= Y1 + 1e-9; v += 0.05) {
      var y = Math.round(Y(v)) + 0.5;
      ctx.beginPath(); ctx.moveTo(PAD.l, y); ctx.lineTo(W - PAD.r, y); ctx.stroke();
      ctx.fillText(v.toFixed(4), W - PAD.r + 10, y);
    }
    ctx.textAlign = 'center';
    var s;
    for (s = 0; s <= N; s += 100) {
      var x = Math.round(X(Math.min(s, N - 1))) + 0.5;
      ctx.beginPath(); ctx.moveTo(x, PAD.t); ctx.lineTo(x, H - PAD.b); ctx.stroke();
      if (s > 0 && s < N) ctx.fillText(String(s), x, H - PAD.b + 16);
    }
    ctx.textAlign = 'left';
    if (W > 640) ctx.fillText('step', PAD.l + 8, H - PAD.b + 16);
    // the shock
    if (k >= SHOCK) {
      var xs = Math.round(X(SHOCK)) + 0.5;
      ctx.save(); ctx.setLineDash([3, 4]); ctx.strokeStyle = COL.amber; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(xs, PAD.t); ctx.lineTo(xs, H - PAD.b); ctx.stroke(); ctx.restore();
      ctx.fillStyle = COL.amber; ctx.font = '700 11px "JetBrains Mono", ui-monospace, Menlo, monospace';
      ctx.fillText('shock', xs + 8, PAD.t - 14);
      ctx.fillRect(xs - 3, Y(series.quiet[SHOCK]) - 3, 6, 6);
    }
    // series
    var order = ['quiet', 'throttle', 'herd'], widths = { quiet: 1.25, throttle: 1.6, herd: 1.6 };
    order.forEach(function (name) {
      var arr = series[name], j;
      ctx.strokeStyle = COL[name]; ctx.lineWidth = widths[name]; ctx.lineJoin = 'round';
      ctx.beginPath(); ctx.moveTo(X(0), Y(arr[0]));
      for (j = 1; j <= k; j++) ctx.lineTo(X(j), Y(arr[j]));
      ctx.stroke();
    });
    // the cursor while the tape is still being written
    if (k < N - 1) {
      var xc = Math.round(X(k)) + 0.5;
      ctx.strokeStyle = COL.grid2; ctx.beginPath(); ctx.moveTo(xc, PAD.t); ctx.lineTo(xc, H - PAD.b); ctx.stroke();
    }
    // chips with the current values, kept apart
    var items = order.map(function (name) { return { name: name, v: series[name][k], y: Y(series[name][k]), c: COL[name] }; });
    items.sort(function (a, b) { return a.y - b.y; });
    var m;
    for (m = 1; m < items.length; m++) if (items[m].y - items[m - 1].y < 24) items[m].y = items[m - 1].y + 24;
    var xe = Math.min(X(k) + 12, W - PAD.r - 2);
    items.forEach(function (it) { chip(xe, it.y, it.name, it.v, it.c, k < N - 1 && xe + 150 < W - PAD.r ? 'left' : 'right'); });
  }

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var start = null, DURATION = 6500, DELAY = 300, progress = 0;
  // the quiet stretch before the shock is written quickly, the cascade slowly
  var SPLIT = 0.22, SHARE = SHOCK / (N - 1);
  function ease(x) {
    if (x < SPLIT) { var a = x / SPLIT; return SHARE * a * (2 - a); }
    var b = (x - SPLIT) / (1 - SPLIT); return SHARE + (1 - SHARE) * (1 - Math.pow(1 - b, 2.2));
  }
  function frame(now) {
    if (start === null) start = now;
    var x = Math.min(1, Math.max(0, (now - start - DELAY) / DURATION));
    progress = ease(x);
    draw(progress);
    if (x < 1) requestAnimationFrame(frame);
  }
  size();
  if (reduced) { progress = 1; draw(1); } else requestAnimationFrame(frame);
  var pending = null;
  window.addEventListener('resize', function () {
    if (pending) cancelAnimationFrame(pending);
    pending = requestAnimationFrame(function () { size(); draw(progress); });
  });
})();
