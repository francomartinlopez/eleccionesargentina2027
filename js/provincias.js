/* Efecto de las elecciones provinciales 2027 sobre el voto de LLA (plan acordado el 19-11-2026, revisado el 20-11-2026).
   Lo usan el bloque del ICG proyectado (#p2027proy) y el de escenarios (#p2027comp), sincronizados.
   Expone window.PROVEF() -> {P, G, B, GS, BS, on} (puntos para LLA: PASO, general con PASO, balotaje,
   general sin PASO, balotaje sin PASO). Datos en datos/provincias.js (window.PROV_DATA).
   Modos: 'no' sin efecto; 'prob' resultado más probable de cada provincia (el acordado); 'esp' efecto esperado
   (cada resultado ponderado por su probabilidad); 'int' interactivo. */
(function () {
  var PD = window.PROV_DATA, R = PD.reglas;
  function dia(s) { var p = s.split('-'); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  PD.provincias.sort(function (a, b) { return dia(a.fecha) - dia(b.fecha); });
  var st = { modo: 'no', sel: {}, ba: PD.ba.esperado, caba: PD.caba.esperado, rap: 'esp', lista: window.innerWidth > 760 };
  var NAC = { P: dia(PD.nacionales.paso), G: dia(PD.nacionales.general), B: dia(PD.nacionales.balotaje) };
  var CBA = PD.provincias.filter(function (p) { return p.n == 'Córdoba'; })[0].padron;
  function peso(p) { return Math.sqrt(p.padron / CBA); }
  /* Reparto de resultados de una provincia: real, elegido a mano o probabilidades. */
  function reparto(p) {
    var o = {};
    if (p.real) { o[p.real.res] = 1; return o; }
    if (st.modo == 'esp') { ['of', 'amb', 'op'].forEach(function (k) { o[k] = (p.prob && p.prob[k] || 0) / 100; }); return o; }
    o[st.modo == 'int' ? (st.sel[p.n] || p.esperado) : p.esperado] = 1; return o;
  }
  function res(p) { if (p.real) return p.real.res; return st.sel[p.n] || p.esperado; }
  /* Resultado real: el margen escala el efecto y, cuando ya hay un ICG de un mes posterior a la elección, vale la mitad. */
  function factorReal(p) {
    if (!p.real) return 1;
    var m = p.real.margen, f = m == null ? 1 : Math.abs(m) > R.margen_alto ? R.f_alto : Math.abs(m) < R.margen_bajo ? R.f_bajo : 1;
    var mes = window.ACTUAL && window.ACTUAL.mes;
    if (mes && mes > p.real.fecha.slice(0, 7)) f *= R.icg_posterior;
    return f;
  }
  function votaron() { return PD.provincias.filter(function (p) { return p.real; }).length; }
  /* Efecto de una provincia con un resultado dado (sin racha ni topes). */
  function efecto(p, r, MAX) {
    var e = p.efecto[r], w = peso(p), v = {}; if (!e) return v;
    if (r == 'of' && p.propio) w = Math.max(w, R.vuelco);
    var dP = dia(p.senal_paso || p.fecha), dG = dia(p.fecha);
    ['P', 'G', 'B'].forEach(function (k, i) {
      if (!(k in MAX)) return;
      var d = k == 'P' ? dP : dG; if (d >= NAC[k]) return;
      var dec = (NAC[k] - d) / 864e5 > R.dias_mitad ? 0.5 : 1;
      v[k] = e[i] * w * MAX[k] * dec;
    });
    return v;
  }
  function calc(sinPaso) {
    var MAX = sinPaso ? R.max_sin : R.max_con, TOPE = sinPaso ? R.tope_sin : R.tope_con, filas = [];
    PD.provincias.forEach(function (p) {
      var rp = reparto(p), fr = factorReal(p), v = {};
      Object.keys(rp).forEach(function (r) { var e = efecto(p, r, MAX); for (var k in e) v[k] = (v[k] || 0) + e[k] * rp[r] * fr; });
      filas.push({ n: p.n, d: dia(p.fecha), v: v, m: {} });
    });
    /* Racha: en un mes, tres o más elecciones con efecto del mismo signo en una instancia, y que sean al menos
       el 75 % de las que mueven esa instancia ese mes: +50 % para esas elecciones, en esa instancia. */
    ['P', 'G', 'B'].forEach(function (k) {
      var g = {};
      filas.forEach(function (f) {
        var x = f.v[k]; if (x == null || Math.abs(x) < R.racha_umbral) return;
        var m = new Date(f.d).getUTCMonth(); (g[m] = g[m] || []).push(f);
      });
      Object.keys(g).forEach(function (m) {
        var pos = g[m].filter(function (f) { return f.v[k] > 0; }), neg = g[m].filter(function (f) { return f.v[k] < 0; });
        [pos, neg].forEach(function (L) { if (L.length >= R.racha_min && L.length >= R.racha_prop * g[m].length) L.forEach(function (f) { f.m[k] = R.racha; }); });
      });
    });
    var t = { P: 0, G: 0, B: 0 };
    filas.forEach(function (f) { for (var k in f.v) t[k] += f.v[k] * (f.m[k] || 1); });
    for (var k in t) if (TOPE[k] != null) t[k] = Math.max(-TOPE[k], Math.min(TOPE[k], t[k]));
    var ba = { P: 0, G: 0, B: 0 }, cb = 0;
    if (PD.ba.real) ba = PD.ba.opciones[PD.ba.real.res];
    else if (st.modo == 'prob') ba = PD.ba.opciones[PD.ba.esperado];
    else if (st.modo == 'esp') Object.keys(PD.ba.prob).forEach(function (o) { var x = PD.ba.opciones[o], q = PD.ba.prob[o] / 100; ba = { P: ba.P + x.P * q, G: ba.G + x.G * q, B: ba.B + x.B * q }; });
    else ba = PD.ba.opciones[st.ba];
    if (PD.caba.real) cb = PD.caba.efecto[PD.caba.real.res] || 0;
    else if (st.modo == 'prob') cb = PD.caba.efecto[PD.caba.esperado] || 0;
    else if (st.modo == 'esp') Object.keys(PD.caba.prob).forEach(function (o) { cb += (PD.caba.efecto[o] || 0) * PD.caba.prob[o] / 100; });
    else cb = PD.caba.efecto[st.caba] || 0;
    t.P += ba.P; t.G += ba.G + cb; t.B += ba.B;
    t.filas = filas;
    return t;
  }
  window.PROVEF = function () {
    if (st.modo == 'no') return { P: 0, G: 0, B: 0, GS: 0, BS: 0, on: false };
    var c = calc(false), s = calc(true);
    return { P: c.P, G: c.G, B: c.B, GS: s.G, BS: s.B, on: true, modo: st.modo };
  };
  /* Totales de un modo dado, sin tocar el estado (para la Metodología y las pruebas). */
  window.PROVTOT = function (modo) { var m = st.modo; st.modo = modo; var r = window.PROVEF(); st.modo = m; return r; };
  window.PROVSTATE = st;
  function f(x) { return (x > 0.04 ? '+' : x < -0.04 ? '−' : '') + Math.abs(x).toFixed(1).replace('.', ','); }
  function f2(x) { return Math.abs(x) < 0.005 ? '0' : (x > 0 ? '+' : '−') + Math.abs(x).toFixed(2).replace('.', ','); }
  var B = 'font:inherit;font-size:13.5px;padding:6px 10px;border:none;cursor:pointer;flex:1 1 auto;min-height:36px';
  var G = 'display:inline-flex;flex-wrap:wrap;border:1px solid var(--strong);border-radius:8px;overflow:hidden;margin:4px 6px 4px 0';
  function grp(attr, ops, cur, lab, full) {
    return '<div role="group" aria-label="' + lab + '" style="' + G + (full ? ';display:flex;margin-right:0' : '') + '">' + ops.map(function (o) {
      var on = o[0] == cur;
      return '<button type="button" ' + attr + ' data-v="' + o[0] + '" aria-pressed="' + on + '" style="' + B + ';background:' + (on ? 'var(--accent)' : 'transparent') + ';color:' + (on ? 'var(--bg)' : 'var(--ink)') + '">' + o[1] + '</button>';
    }).join('') + '</div>';
  }
  var LAB = { of: 'LLA o aliado', amb: 'Oficialismo provincial', op: 'Peronismo' };
  var LAB_LARGO = { of: 'gana LLA o un aliado formal', amb: 'gana el oficialismo provincial, que compite aparte de LLA', op: 'gana el peronismo opositor' };
  var EST = { c: 'confirmada', a: 'anunciada', e: 'estimada' };
  var MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  var MESL = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  function fecha(s) { var d = new Date(dia(s)); return d.getUTCDate() + ' ' + MES[d.getUTCMonth()]; }
  function panel() {
    var h = '<div style="font-size:13px;font-weight:600;color:var(--ink);margin:10px 0 0">Elecciones provinciales 2027</div>' +
      grp('data-pv-modo', [['no', 'Sin efecto electoral provincial'], ['prob', 'Efecto más probable'], ['esp', 'Efecto esperado (con probabilidades)'], ['int', 'Efecto interactivo']], st.modo, 'Efecto de las elecciones provinciales');
    if (st.modo != 'no') {
      var e = window.PROVEF();
      h += '<div style="font-size:13px;color:var(--ink2);margin:4px 0 0;line-height:1.45"><strong style="color:var(--ink)">Ajuste para LLA por las provinciales:</strong> con PASO, PASO ' + f(e.P) + ' · general ' + f(e.G) + ' · balotaje ' + f(e.B) + ' puntos; sin PASO, general ' + f(e.GS) + ' · balotaje ' + f(e.BS) + '. ' +
        (st.modo == 'prob' ? 'Aplica el resultado más probable de cada provincia.' : st.modo == 'esp' ? 'Suma el efecto de cada resultado posible de cada provincia, ponderado por su probabilidad (estimación propia).' : 'Elija el resultado de cada provincia.') + (votaron() ? ' Ya votaron ' + votaron() + ' de ' + PD.provincias.length + ': para ellas se usa el resultado real.' : '') +
        ' <a href="#met-provincias" data-abrir="met-provincias">Detalle y probabilidades en Metodología</a>. Sin PASO nacionales, las alianzas cerrarían cerca del ' + fecha(PD.sin_paso.alianzas) + ', después de Córdoba y Santa Fe: sus resultados pueden cambiar quién se alía con quién, algo que se elige en el <a href="#p2027comp">cuadro de escenarios</a>.</div>';
    }
    if (st.modo == 'int') {
      h += '<div style="margin:8px 0 0;font-size:13px;color:var(--ink2)">Escenarios rápidos</div>' +
        grp('data-pv-rap', [['esp', 'Lo más probable'], ['buen', 'Buen año para LLA'], ['mal', 'Mal año para LLA'], ['cba', 'Córdoba la gana LLA'], ['sf', 'Santa Fe con alianza']], st.rap, 'Escenarios rápidos');
      h += '<div style="margin:6px 0 0;font-size:13px;color:var(--ink2)">Buenos Aires, gobernador (mismo día que la Nación)</div>' +
        (PD.ba.real ? '<div style="font-size:13px"><strong>Votó:</strong> ' + PD.ba.real.texto + '</div>' : grp('data-pv-ba', [['pc', 'Peronismo claro'], ['pa', 'Peronismo ajustado'], ['sa', 'Santilli ajustado'], ['sc', 'Santilli claro']], st.ba, 'Buenos Aires'));
      h += '<div style="margin:6px 0 0;font-size:13px;color:var(--ink2)">Ciudad de Buenos Aires (si vota con la Nación)</div>' +
        (PD.caba.real ? '<div style="font-size:13px"><strong>Votó:</strong> ' + PD.caba.real.texto + '</div>' : grp('data-pv-caba', [['of', 'PRO con LLA'], ['amb', 'PRO sin LLA'], ['op', 'Gana la oposición']], st.caba, 'Ciudad de Buenos Aires'));
      h += '<details class="pvlista"' + (st.lista ? ' open' : '') + ' style="margin:8px 0 0;padding:6px 8px;border:1px solid var(--line);border-radius:8px"><summary style="cursor:pointer;font-size:13.5px;font-weight:600">Cada provincia (' + PD.provincias.length + '), por fecha. El punto marca el resultado más probable.</summary>';
      var mes = -1;
      PD.provincias.forEach(function (p) {
        var r = res(p), m = new Date(dia(p.fecha)).getUTCMonth();
        if (m != mes) { mes = m; h += '<div style="font-size:12.5px;font-weight:600;color:var(--ink2);margin:10px 0 2px;text-transform:uppercase;letter-spacing:.04em">' + MESL[m] + '</div>'; }
        h += '<div style="padding:4px 0 6px;border-bottom:1px solid var(--line)"><div style="font-size:14px"><strong>' + p.n + '</strong> <span style="color:var(--ink2)">' + fecha(p.fecha) + (p.estado != 'c' ? ' · fecha ' + EST[p.estado] : '') + (p.real ? ' · votó: ' + p.real.ganador + ' ' + String(p.real.pct).replace('.', ',') + ' %' : '') + '</span></div>' +
          (p.real ? '<div style="font-size:13px"><strong>' + LAB[r] + ' ✓</strong></div>' : grp('data-pv-prov="' + p.n + '"', ['of', 'amb', 'op'].map(function (k) { return [k, LAB[k] + (p.esperado == k ? ' •' : '')]; }), r, p.n, 1)) + '</div>';
      });
      h += '</details>';
    }
    return h;
  }
  /* Redibuja los paneles conservando el foco del teclado. */
  function pinta() {
    var a = document.activeElement, key = null, idx = -1;
    if (a && a.closest && a.closest('.pv-panel')) {
      var pans = Array.prototype.slice.call(document.querySelectorAll('.pv-panel')); idx = pans.indexOf(a.closest('.pv-panel'));
      key = Array.prototype.slice.call(a.attributes).filter(function (x) { return x.name.indexOf('data-pv') == 0 || x.name == 'data-v'; }).map(function (x) { return '[' + x.name + '="' + x.value.replace(/"/g, '\\"') + '"]'; }).join('');
      if (a.tagName == 'SUMMARY') key = 'details.pvlista>summary';
    }
    document.querySelectorAll('.pv-panel').forEach(function (el) { el.innerHTML = panel(); });
    if (key && idx >= 0) { var t = document.querySelectorAll('.pv-panel')[idx].querySelector(key); if (t) t.focus({ preventScroll: true }); }
    totales();
  }
  function todo() { pinta(); if (window.proyDraw) window.proyDraw(); if (window.compDraw) window.compDraw(); }
  function rapido(k) {
    st.sel = {}; st.ba = PD.ba.esperado; st.caba = PD.caba.esperado; st.rap = k;
    var paso = function (r, d) { var o = ['op', 'amb', 'of'], i = o.indexOf(r) + d; return o[Math.max(0, Math.min(2, i))]; };
    if (k == 'buen' || k == 'mal') {
      PD.provincias.forEach(function (p) { st.sel[p.n] = paso(p.esperado, k == 'buen' ? 1 : -1); });
      st.ba = k == 'buen' ? 'sa' : 'pc'; st.caba = k == 'buen' ? 'of' : 'amb';
    }
    if (k == 'cba') st.sel['Córdoba'] = 'of';
    if (k == 'sf') st.sel['Santa Fe'] = 'of';
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.pv-panel button'); if (!b) return;
    if (b.hasAttribute('data-pv-modo')) { st.modo = b.dataset.v; if (st.modo == 'int' && !Object.keys(st.sel).length) rapido('esp'); }
    else if (b.hasAttribute('data-pv-rap')) rapido(b.dataset.v);
    else if (b.hasAttribute('data-pv-ba')) { st.ba = b.dataset.v; st.rap = null; }
    else if (b.hasAttribute('data-pv-caba')) { st.caba = b.dataset.v; st.rap = null; }
    else if (b.hasAttribute('data-pv-prov')) { st.sel[b.getAttribute('data-pv-prov')] = b.dataset.v; st.rap = null; }
    todo();
  });
  document.addEventListener('toggle', function (ev) { if (ev.target.classList && ev.target.classList.contains('pvlista')) st.lista = ev.target.open; }, true);
  /* Metodología: cuadro, línea de tiempo y totales generados desde los datos */
  function totales() {
    var T = { p: window.PROVTOT('prob'), e: window.PROVTOT('esp') };
    document.querySelectorAll('[data-pvtot]').forEach(function (el) {
      var k = el.getAttribute('data-pvtot'), x = T[k.charAt(0)][k.slice(1)];
      el.textContent = f(x);
    });
  }
  function metodo() {
    var el = document.getElementById('pvMetodo'); if (!el) return;
    var h = '<table class="pvt"><thead><tr><th style="text-align:left">Provincia</th><th>Fecha</th><th>Más probable</th><th>Prob. LLA / prov. / PJ</th><th>Resultado real</th><th>Peso</th><th>Si gana LLA o aliado</th><th>Si gana el oficialismo prov.</th><th>Si gana el peronismo</th><th>Fuente</th></tr></thead><tbody>';
    PD.provincias.forEach(function (p) {
      var cel = ['of', 'amb', 'op'].map(function (r) { var v = efecto(p, r, R.max_con); return ['P', 'G', 'B'].map(function (k) { return k in v ? f2(v[k]) : '—'; }).join(' / '); });
      var pr = p.prob ? p.prob.of + ' / ' + p.prob.amb + ' / ' + p.prob.op + ' %' : '—';
      h += '<tr><td style="text-align:left">' + p.n + '</td><td data-l="Fecha">' + (p.paso_prov ? 'PASO ' + fecha(p.paso_prov) + ' · ' : '') + fecha(p.fecha) + ' <span style="color:var(--ink2)">(' + EST[p.estado] + ')</span></td><td data-l="Más probable">' + {of:'LLA o aliado',amb:'Ofic. provincial',op:'Peronismo'}[p.esperado] + '</td><td data-l="Probabilidad (LLA / prov. / PJ)">' + pr + '</td><td data-l="Resultado real">' + (p.real ? LAB[p.real.res] + ': ' + p.real.ganador + ' ' + String(p.real.pct).replace('.', ',') + ' % (margen ' + String(p.real.margen).replace('.', ',') + ')' : '—') + '</td><td data-l="Peso">' + peso(p).toFixed(2).replace('.', ',') + '</td>' +
        ['Si gana LLA o aliado', 'Si gana el oficialismo provincial', 'Si gana el peronismo'].map(function (l, i) { return '<td data-l="' + l + '">' + cel[i] + '</td>'; }).join('') +
        '<td data-l="Fuente de la fecha">' + (p.fuente ? (p.fuente.url ? '<a href="' + p.fuente.url + '" rel="noopener" title="' + p.fuente.texto.replace(/"/g, '') + '">' + (p.estado == 'c' ? 'decreto' : 'nota') + '</a>' : 'propia') : '—') + '</td></tr>';
    });
    el.innerHTML = h + '</tbody></table><div style="font-size:12.5px;color:var(--ink2);margin-top:4px">Efectos en puntos para LLA en PASO / general / balotaje, con PASO nacionales, sin racha ni topes. Probabilidades: estimación propia, a revisar a medida que haya encuestas y candidaturas.</div>';
    var t = document.getElementById('pvTiempo'); if (!t) return;
    var ev = PD.provincias.map(function (p) { var a = [{ d: p.fecha, t: p.n + (p.estado != 'c' ? ' (' + EST[p.estado] + ')' : ''), c: '' }]; if (p.paso_prov) a.push({ d: p.paso_prov, t: p.n + ', PASO provinciales', c: '' }); return a; }).reduce(function (a, b) { return a.concat(b); }, []);
    ev.push({ d: PD.nacionales.paso, t: 'PASO nacionales (si se hacen). Votan junto con la Nación las PASO de Buenos Aires y la Ciudad, y Santa Cruz', c: 'nac' });
    ev.push({ d: PD.nacionales.general, t: 'General nacional. Votan el mismo día Buenos Aires, la Ciudad, Catamarca y La Rioja', c: 'nac' });
    ev.push({ d: PD.nacionales.balotaje, t: 'Balotaje nacional (si hay)', c: 'nac' });
    ev.push({ d: PD.sin_paso.alianzas, t: 'Sin PASO nacionales: cierre de alianzas (estimado)', c: 'sinp' });
    ev.push({ d: PD.sin_paso.listas, t: 'Sin PASO nacionales: cierre de listas (estimado)', c: 'sinp' });
    ev.sort(function (a, b) { return dia(a.d) - dia(b.d); });
    t.innerHTML = '<ul class="tl">' + ev.map(function (x) { return '<li class="' + x.c + '"><span class="f">' + fecha(x.d) + '</span> ' + x.t + '</li>'; }).join('') + '</ul>';
  }
  function init() { pinta(); metodo(); }
  var prevAct = window.alActualizar; window.alActualizar = function (A) { if (prevAct) prevAct(A); pinta(); };
  if (document.readyState == 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
