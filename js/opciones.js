/* Opciones del cuadro de escenarios que se aplican sobre el escenario elegido, en el navegador:
   outsider con lista propia, vice de Milei, candidato de cada fuerza (con afinidad en los frentes)
   y lo confirmado (datos/confirmados.js). Valores en datos/opciones.js. Ver Metodología. */
(function () {
  var O = window.OPC, CF = (window.CONF && window.CONF.datos) || {};
  if (!O) return;
  var PZ = {'LLA': 'lla', 'PRO': 'pro', 'Centro (UCR y gobernadores)': 'ce', 'centro': 'ce', 'Centro': 'ce', 'CC': 'cc',
    'Peronismo federal': 'pf', 'peronismo federal': 'pf', 'Kirchnerismo': 'k', 'Cristina': 'cr', 'Kicillof': 'kic',
    'K duro': 'kd', 'Massa': 'mas', 'Izquierda': 'iz'};
  var TR = {lla: [.85, 0, .15], pro: [.75, .05, .2], ce: [.45, .2, .35], pf: [.35, .4, .25], cc: [.25, .3, .45], iz: [0, .35, .65],
    k: [.05, .4, .55], cr: [.05, .4, .55], kic: [.05, .4, .55], kd: [.05, .4, .55], mas: [.3, .45, .25], otro: [.3, .3, .4]};
  var FUERZAS = ['pro', 'ce', 'cc', 'pf', 'kf'];
  var NOMB = {pro: 'PRO', ce: 'centro', cc: 'CC', pf: 'peronismo federal', kf: 'frente kirchnerista'};
  function piezas(n) { if (n == 'Peronismo unido') return ['k', 'pf']; return n.split(' + ').map(function (x) { return PZ[x] || 'otro'; }); }
  function fam(p) { return (p == 'k' || p == 'cr' || p == 'kic' || p == 'kd' || p == 'mas') ? 'kf' : p; }
  function coincide(p, key) { if (key == 'per') return fam(p) == 'kf' || p == 'pf'; return fam(p) == key || p == key; }
  function f1(x) { return x.toFixed(1).replace('.', ','); }

  var DEF = {out: [], vice: 'otro', paso: 'sin', cand: {}};
  var S = {out: [], vice: 'otro', paso: 'sin', cand: {}};
  function conf() {
    S.out = CF.out ? [].concat(CF.out.v) : []; S.vice = CF.vice ? CF.vice.v : DEF.vice; S.paso = CF.paso ? CF.paso.v : DEF.paso; S.cand = {};
    FUERZAS.forEach(function (k) { if (CF['cand.' + k]) S.cand[k] = CF['cand.' + k].v; });
  }
  conf();

  function listas(c) {
    var L = [{n: c.f, of: 1, G: c.G.ll, P: c.P.ll, g0: c.G.ll, r: 0, pz: {}}];
    c.O.forEach(function (x) { L.push({n: x[0], G: x[2], P: x[1], g0: x[2], r: x[3], pz: {}}); });
    L.forEach(function (l) { var p = piezas(l.n); p.forEach(function (k) { l.pz[k] = (l.pz[k] || 0) + l.G / p.length; }); });
    return L;
  }
  function principal(l) { var m = null; for (var p in l.pz) if (!m || l.pz[p] > l.pz[m]) m = p; return m || 'otro'; }
  function quitar(X, key, m, tgt) {
    var src = [], tot = 0, res = [];
    X.L.forEach(function (l, i) { if (i === tgt) return; for (var p in l.pz) if (l.pz[p] > 0 && coincide(p, key)) { src.push([i, p]); tot += l.pz[p]; } });
    if (!tot || m <= 0) return res;
    src.forEach(function (s) { var l = X.L[s[0]], v = l.pz[s[1]], a = Math.min(m * v / tot, v * .95); l.pz[s[1]] -= a; l.G -= a; res.push([s[1], a]); });
    return res;
  }
  function dar(X, i, p, m) { var l = X.L[i]; l.pz[p] = (l.pz[p] || 0) + m; l.G += m; }
  function sacar(X, i, m) { var l = X.L[i], q = Math.min(m, l.G * .95), k = l.G ? q / l.G : 0; for (var p in l.pz) l.pz[p] *= (1 - k); l.G -= q; return q; }
  function aOtras(X, m, src, p) {
    var tot = 0; X.L.forEach(function (l, i) { if (i !== src) tot += l.G; });
    X.L.forEach(function (l, i) { if (i !== src && tot) dar(X, i, p, m * l.G / tot); });
  }
  function repartir(X, m, dest, src, p) {
    for (var key in dest) {
      var w = dest[key] * m, hay = [];
      X.L.forEach(function (l, i) { if (i === src) return; if (l.out == key) hay.push([i, l.G]); else for (var q in l.pz) if (coincide(q, key)) { hay.push([i, l.G]); break; } });
      var tot = hay.reduce(function (s, h) { return s + h[1]; }, 0);
      if (!tot) { X.ext -= w; continue; }
      hay.forEach(function (h) { dar(X, h[0], p, w * h[1] / tot); });
    }
  }
  function abst(spec) { return typeof spec.ab == 'number' ? spec.ab : (O.abst[spec.ab] || 0); }
  function efecto(X, i, spec) {
    var e = O.escala[spec.e] || 0, a = abst(spec), l = X.L[i], p = principal(l);
    if (e > 0) {
      for (var key in (spec.de || {})) quitar(X, key, e * (1 - a) * spec.de[key], i).forEach(function (r) { dar(X, i, r[0], r[1]); });
      dar(X, i, p, e * a); X.ext += e * a;
    } else if (e < 0) {
      var m = sacar(X, i, -e), ab = m * a; X.ext -= ab;
      if (spec.a) repartir(X, m - ab, spec.a, i, p); else aOtras(X, m - ab, i, p);
    }
  }
  function distancia(a, b) { var k = [a, b].sort().join('-'); return O.distancia[k] || O.distancia_otra; }
  function afinidad(X, i, spec, orig) {
    if (!spec.org) return;
    var l = X.L[i];
    Object.keys(l.pz).forEach(function (p) {
      var fp = fam(p);
      if (orig.indexOf(fp) < 0 || FUERZAS.indexOf(fp) < 0 || spec.org.indexOf(fp) >= 0 || !(l.pz[p] > 0)) return;
      var r = 0; spec.org.forEach(function (o) { r = Math.max(r, O.retiene[distancia(o, fp)]); });
      var loss = l.pz[p] * (1 - r); l.pz[p] -= loss; l.G -= loss;
      var t = fp == 'pf' ? [.58, 0, .42] : (TR[p] || TR.otro);
      dar(X, 0, p, loss * t[0]); X.ext -= loss * t[2];
      var j = -1; (O.cercana[fp] || []).some(function (q) { X.L.some(function (m, k) { if (k && k !== i && m.pz[q] > 0) { j = k; return true; } }); return j >= 0; });
      if (j >= 0) dar(X, j, p, loss * t[1]); else X.ext -= loss * t[1];
    });
  }
  function balotaje(L) {
    var ll = L[0].G, riv = null;
    L.forEach(function (l, i) { if (i && (!riv || l.G > riv.G)) riv = l; });
    if (!riv) return 100;
    var a = ll, b = riv.G;
    L.forEach(function (l, i) { if (!i || l === riv) return; for (var p in l.pz) { var t = TR[p] || TR.otro; a += l.pz[p] * t[0]; b += l.pz[p] * t[1]; } });
    return 100 * a / (a + b);
  }
  function fuerzasDe(l) { var r = []; for (var p in l.pz) { var f = fam(p); if (FUERZAS.indexOf(f) >= 0 && r.indexOf(f) < 0) r.push(f); } return r; }
  function outsiders() { return O.outsiders.filter(function (x) { return S.out.indexOf(x.k) >= 0; }); }
  function esOut(n) { return outsiders().some(function (x) { return x.n == n; }); }
  // Opciones de candidato de una lista: unión de los nombres de sus fuerzas, sin repetir (efecto mayor).
  var BU = 'lla';
  function buPRO(l) { return BU == 'pro' && fuerzasDe(l).indexOf('pro') >= 0; }
  function opciones(l, interna) {
    var r = [], vistos = {};
    if (!interna && buPRO(l)) return r;
    fuerzasDe(l).forEach(function (f) {
      (O.candidatos[f] || []).forEach(function (c) {
        if (!!c.paso != !!interna) return;
        var e = O.escala[c.e];
        if (vistos[c.n] != null) { var prev = r[vistos[c.n]]; if (e > O.escala[prev.e]) r[vistos[c.n]] = c; return; }
        vistos[c.n] = r.length; r.push(c);
      });
    });
    return r.map(function (c) { return {c: c, no: esOut(c.n) || (interna && S.paso != 'con')}; });
  }
  function elegido(l, interna) {
    var ops = opciones(l, interna), fs = fuerzasDe(l), sel = null;
    var claves = interna ? ['kf'] : fs.filter(function (f) { return f != 'kf'; }).concat(fs.indexOf('kf') >= 0 ? ['kfc'] : []);
    claves.some(function (f) { var n = S.cand[f]; if (!n) return false; ops.some(function (o) { if (o.c.n == n && !o.no) { sel = o.c; return true; } }); return !!sel; });
    return sel;
  }
  function vice(stMain) {
    var v = null; O.vice.forEach(function (x) { if (x.k == S.vice) v = x; });
    if (v && v.k == 'bullrich' && stMain.bu == 'pro') return null;
    return v && v.e ? v : null;
  }

  function aplicar(c, stMain) {
    BU = stMain.bu;
    var X = {L: listas(c), ext: 0}, txt = [], L0 = listas(c), vi = vice(stMain), hay = false;
    outsiders().forEach(function (on) {
      var v = on.v * O.afirm, a = abst(on), idx = X.L.push({n: on.n + ' (outsider)', G: 0, P: 0, g0: 0, r: 0, pz: {}, out: on.k}) - 1;
      for (var key in on.de) quitar(X, key, v * (1 - a) * on.de[key], idx).forEach(function (r) { dar(X, idx, r[0], r[1]); });
      var l = X.L[idx], tot = l.G;
      if (tot) for (var p in l.pz) l.pz[p] += v * a * l.pz[p] / tot; else l.pz.otro = v * a;
      l.G += v * a; X.ext += v * a; hay = true;
      txt.push('outsider ' + on.n + ' (' + f1(v) + ' % de los votos afirmativos)');
    });
    var nL = X.L.length, internas = [];
    for (var i = 1; i < nL; i++) {
      if (X.L[i].out) continue;
      var cd = elegido(L0[i], false);
      if (cd) { afinidad(X, i, cd, fuerzasDe(L0[i])); efecto(X, i, cd); hay = true; txt.push(X.L[i].n + ': ' + cd.n); }
      var it = S.paso == 'con' ? elegido(L0[i], true) : null;
      if (it) { internas.push([i, it]); hay = true; txt.push(X.L[i].n + ': ' + it.n + ' como rival interno en la PASO'); }
    }
    if (vi) { efecto(X, 0, vi); hay = true; txt.push('vice de Milei: ' + vi.n); }
    if (!hay) return null;
    var g0 = 0, p0 = 0; L0.forEach(function (l) { g0 += l.G; p0 += l.P; });
    var k = g0 / (g0 + X.ext);
    X.L.forEach(function (l) { l.G *= k; for (var p in l.pz) l.pz[p] *= k; });
    // PASO: cada lista cambia en la misma proporción que en la general; el outsider, con su valor de la general.
    X.L.forEach(function (l) { l.P = l.g0 > 0 ? l.P * l.G / l.g0 : l.G; });
    var extP = 0;
    internas.forEach(function (t) {
      var i = t[0], s = t[1], e = O.escala[s.e] || 0, a = abst(s), lst = X.L[i];
      for (var key in (s.de || {})) {
        var src = [], tt = 0;
        X.L.forEach(function (m, j) { if (j === i) return; for (var p in m.pz) if (coincide(p, key)) { src.push(m); tt += m.P; break; } });
        src.forEach(function (m) { var q = Math.min(e * (1 - a) * s.de[key] * m.P / tt, m.P * .95); m.P -= q; lst.P += q; });
      }
      lst.P += e * a; extP += e * a;
    });
    var sp = 0; X.L.forEach(function (l) { sp += l.P; });
    X.L.forEach(function (l) { l.P *= p0 / sp; });
    var dB = balotaje(X.L) - balotaje(L0);
    return {dG: X.L[0].G - c.G.ll, dP: X.L[0].P - c.P.ll, dB: dB, L: X.L, ext: X.ext * 100 / g0, extP: sp - p0, txt: txt};
  }

  // ---------- Interfaz ----------
  var BST = 'font:inherit;font-size:13px;padding:6px 10px;border:none;cursor:pointer;flex:1 1 auto';
  var GST = 'display:inline-flex;flex-wrap:wrap;border:1px solid var(--strong);border-radius:8px;overflow:hidden;margin:4px 6px 4px 0';
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function boton(g, v, t, on, no, cf, extra) {
    return '<button type="button" data-g="' + g + '" data-v="' + esc(v) + '"' + (extra || '') + (no ? ' disabled' : '') + (cf ? ' data-conf="" title="Confirmado: ' + esc(cf.fuente) + '"' : '') +
      ' aria-pressed="' + (on ? 'true' : 'false') + '" style="' + BST + ';background:' + (on ? 'var(--accent)' : 'transparent') + ';color:' + (on ? 'var(--bg)' : 'var(--ink)') + (no ? ';opacity:.45;cursor:not-allowed' : '') + '">' + t + '</button>';
  }
  function cfDe(clave, v) { var d = CF[clave]; return d && d.v == v ? d : null; }
  function init() {
    var box = document.getElementById('cOpc'); if (!box) return;
    box.innerHTML =
      '<div style="font-size:13px;font-weight:600;color:var(--ink);margin:14px 0 0">PASO</div><div id="o_paso"></div>' +
      '<div style="font-size:13px;color:var(--ink2);margin:0 0 4px">Decide qué candidatos de interna se pueden elegir. El cuadro muestra igual los resultados con y sin PASO.</div>' +
      '<details class="opc" id="o_dOut"><summary></summary><div style="font-size:13px;color:var(--ink2);margin:6px 0 2px">Se pueden elegir varios; cada uno compite con lista propia. Valor inicial de encuestas, llevado a votos afirmativos; sale de las fuerzas indicadas en Metodología.</div><div id="o_out"></div></details>' +
      '<details class="opc" id="o_dVice"><summary></summary><div id="o_vice"></div></details>' +
      '<details class="opc" id="o_dCand"><summary></summary><div style="font-size:13px;color:var(--ink2);margin:6px 0 2px">Frente a un candidato genérico de esa fuerza. Si el frente une fuerzas, el candidato de una puede hacer perder votos de la otra (afinidad, ver Metodología).</div><div id="o_cand"></div></details>' +
      '<div style="margin:6px 0 0"><button type="button" id="o_conf" style="' + BST + ';border:1px solid var(--strong);border-radius:8px;background:transparent;color:var(--ink)">Volver a lo confirmado</button> <span style="font-size:13px;color:var(--ink2)">✓ = confirmado (lanzamiento, inscripción o ley). Ajuste aproximado sobre el escenario elegido; ver <a href="#met-opciones">Metodología</a>.</span></div>';
    box.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b || b.disabled) return;
      if (b.id == 'o_conf') { conf(); if (window.compConf) window.compConf(); return; }
      var g = b.dataset.g, v = b.dataset.v;
      if (g == 'paso') S.paso = v; else if (g == 'out') { if (v == 'no') S.out = []; else { var i = S.out.indexOf(v); if (i >= 0) S.out.splice(i, 1); else S.out.push(v); } } else if (g == 'vice') S.vice = v;
      else if (g == 'cand') { b.dataset.f.split(',').forEach(function (f) { if (v) S.cand[f] = v; else delete S.cand[f]; }); }
      else if (g == 'int') { if (v) S.cand.kf = v; else delete S.cand.kf; }
      if (window.compDraw) window.compDraw();
    });
  }
  function render(c, stMain) {
    BU = stMain.bu;
    if (!document.getElementById('o_paso')) return;
    document.getElementById('o_paso').innerHTML = '<div style="' + GST + '">' + boton('paso', 'sin', 'Sin PASO', S.paso == 'sin', false, cfDe('paso', 'sin')) + boton('paso', 'con', 'Con PASO', S.paso == 'con', false, cfDe('paso', 'con')) + '</div>';
    var os = outsiders();
    document.querySelector('#o_dOut summary').innerHTML = 'Outsiders: <strong>' + (os.length ? os.map(function (o) { return o.n + ' (' + f1(o.v) + ')'; }).join(', ') : 'ninguno') + '</strong>';
    var h = boton('out', 'no', 'Ninguno', !os.length, false, null);
    O.outsiders.forEach(function (o) { var cf = CF.out && [].concat(CF.out.v).indexOf(o.k) >= 0 ? CF.out : null; h += boton('out', o.k, o.n + ' (' + f1(o.v) + (o.est ? ', estimado' : '') + ')', S.out.indexOf(o.k) >= 0, false, cf); });
    document.getElementById('o_out').innerHTML = '<div style="' + GST + '">' + h + '</div>';
    var vi = vice(stMain), vn = 'Otro';
    O.vice.forEach(function (x) { if (x.k == S.vice && (x.k != 'bullrich' || stMain.bu != 'pro')) vn = x.n; });
    document.querySelector('#o_dVice summary').innerHTML = 'Vice de Milei: <strong>' + vn + '</strong>';
    h = '';
    O.vice.forEach(function (x) { var no = x.k == 'bullrich' && stMain.bu == 'pro'; h += boton('vice', x.k, x.n + (x.d ? ' (' + x.d + ')' : ''), vn == x.n, no, cfDe('vice', x.k)); });
    document.getElementById('o_vice').innerHTML = '<div style="' + GST + '">' + h + '</div>' + (stMain.bu == 'pro' ? '<div style="font-size:13px;color:var(--ink2)">Bullrich es candidata del PRO: no puede ser la vice.</div>' : '');
    var L = listas(c), filas = '', res = [];
    var conLLA = fuerzasDe(L[0]);
    if (conLLA.length) filas += '<div style="font-size:13px;color:var(--ink2);margin:6px 0 0">' + conLLA.map(function (f) { return NOMB[f]; }).join(', ') + ': ' + (conLLA.length > 1 ? 'van' : 'va') + ' con LLA (candidato: Milei).</div>';
    for (var i = 1; i < L.length; i++) {
      var l = L[i], fs = fuerzasDe(l);
      if (buPRO(l)) filas += '<div style="font-size:13px;color:var(--ink2);margin:6px 0 0">' + esc(l.n) + ': la candidata es Bullrich.</div>';
      [false, true].forEach(function (interna) {
        var ops = opciones(l, interna); if (!ops.length) return;
        if (interna && S.paso != 'con') { filas += '<div style="font-size:13px;color:var(--ink2);margin:6px 0 0">' + esc(l.n) + ', rival interno en la PASO: solo con PASO.</div>'; return; }
        var sel = elegido(l, interna), claves = interna ? 'kf' : fs.filter(function (f) { return f != 'kf'; }).concat(fs.indexOf('kf') >= 0 ? ['kfc'] : []).join(',');
        var g = interna ? 'int' : 'cand', b = boton(g, '', interna ? 'Ninguno' : 'Genérico', !sel, false, null, ' data-f="' + claves + '"');
        ops.forEach(function (o) {
          var cf = null; fs.forEach(function (f) { cf = cf || cfDe('cand.' + (interna ? 'kf' : f), o.c.n); });
          b += boton(g, o.c.n, o.c.n, sel && sel.n == o.c.n, o.no, cf, ' data-f="' + claves + '"');
        });
        filas += '<div style="font-size:13px;font-weight:600;color:var(--ink);margin:8px 0 0">' + esc(l.n) + (interna ? ', rival interno en la PASO' : '') + '</div><div style="' + GST + '">' + b + '</div>';
        if (sel) res.push(sel.n);
      });
    }
    document.getElementById('o_cand').innerHTML = filas;
    document.querySelector('#o_dCand summary').innerHTML = 'Candidato de cada fuerza: <strong>' + (res.length ? res.join(', ') : 'genérico') + '</strong>';
  }
  window.OPCION = {aplicar: aplicar, render: render, init: init, CF: CF, S: S};
})();
