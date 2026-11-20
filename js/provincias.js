/* Efecto de las elecciones provinciales 2027 sobre el voto de LLA (plan acordado el 19-11-2026).
   Lo usan el bloque del ICG proyectado (#p2027proy) y el de escenarios (#p2027comp), sincronizados.
   Expone window.PROVEF() -> {P, G, B, GS, BS} (puntos para LLA: PASO, general con PASO, balotaje,
   general sin PASO, balotaje sin PASO). Datos en datos/provincias.js (window.PROV_DATA). */
(function () {
  var PD = window.PROV_DATA;
  PD.provincias.sort(function (a, b) { return a.fecha < b.fecha ? -1 : a.fecha > b.fecha ? 1 : 0; });
  var st = { modo: 'no', sel: {}, ba: PD.ba.esperado, caba: PD.caba.esperado };
  var NAC = { P: new Date(PD.nacionales.paso), G: new Date(PD.nacionales.general), B: new Date(PD.nacionales.balotaje) };
  var CBA = PD.provincias.filter(function (p) { return p.n == 'Córdoba'; })[0].padron;
  function peso(p) { return Math.sqrt(p.padron / CBA); }
  function res(p) { if (p.real) return p.real.res; return st.modo == 'prob' ? p.esperado : (st.sel[p.n] || p.esperado); }
  /* Resultado real: el margen escala el efecto y, cuando ya hay un ICG de un mes posterior a la elección, vale la mitad (el índice ya refleja parte del clima). */
  function factorReal(p) {
    if (!p.real) return 1;
    var m = p.real.margen, f = m == null ? 1 : Math.abs(m) > PD.reglas.margen_alto ? PD.reglas.f_alto : Math.abs(m) < PD.reglas.margen_bajo ? PD.reglas.f_bajo : 1;
    var mes = window.ACTUAL && window.ACTUAL.mes;
    if (mes && mes > p.real.fecha.slice(0, 7)) f *= PD.reglas.icg_posterior;
    return f;
  }
  function votaron() { return PD.provincias.filter(function (p) { return p.real; }).length; }
  function calc(sinPaso) {
    var MAX = sinPaso ? PD.reglas.max_sin : PD.reglas.max_con, TOPE = sinPaso ? PD.reglas.tope_sin : PD.reglas.tope_con;
    var filas = [], grupos = {};
    PD.provincias.forEach(function (p) {
      var r = res(p), e = p.efecto[r]; if (!e) return;
      var w = peso(p); if (r == 'of' && p.propio) w = Math.max(w, PD.reglas.vuelco);
      var dP = new Date(p.senal_paso || p.fecha), dG = new Date(p.fecha), v = {}, fr = factorReal(p);
      ['P', 'G', 'B'].forEach(function (k, i) {
        if (!(k in MAX)) return;
        var d = k == 'P' ? dP : dG; if (d >= NAC[k]) return;
        var dias = (NAC[k] - d) / 864e5, dec = dias > PD.reglas.dias_mitad ? 0.5 : 1;
        v[k] = e[i] * w * MAX[k] * dec * fr;
      });
      var sg = (v.P || 0) + (v.G || 0); sg = sg > 0 ? 1 : sg < 0 ? -1 : 0;
      if (sg) { var key = dG.getMonth() + '_' + sg; (grupos[key] = grupos[key] || []).push(p.n); }
      filas.push({ n: p.n, v: v });
    });
    var racha = {}; Object.keys(grupos).forEach(function (k) { if (grupos[k].length >= 3) grupos[k].forEach(function (n) { racha[n] = 1; }); });
    var t = { P: 0, G: 0, B: 0 };
    filas.forEach(function (f) { var m = racha[f.n] ? PD.reglas.racha : 1; for (var k in f.v) t[k] += f.v[k] * m; });
    for (var k in t) if (TOPE[k] != null) t[k] = Math.max(-TOPE[k], Math.min(TOPE[k], t[k]));
    var bak = PD.ba.real ? PD.ba.real.res : st.ba, cbk = PD.caba.real ? PD.caba.real.res : st.caba;
    var ba = PD.ba.opciones[bak], cb = PD.caba.efecto[cbk] || 0;
    t.P += ba.P; t.G += ba.G + cb; t.B += ba.B;
    return t;
  }
  window.PROVEF = function () {
    if (st.modo == 'no') return { P: 0, G: 0, B: 0, GS: 0, BS: 0, on: false };
    var c = calc(false), s = calc(true);
    return { P: c.P, G: c.G, B: c.B, GS: s.G, BS: s.B, on: true };
  };
  window.PROVSTATE = st;
  function f(x) { return (x > 0.04 ? '+' : x < -0.04 ? '−' : '') + Math.abs(x).toFixed(1).replace('.', ','); }
  var B = 'font:inherit;font-size:13px;padding:6px 10px;border:none;cursor:pointer;flex:1 1 auto';
  var G = 'display:inline-flex;flex-wrap:wrap;border:1px solid var(--strong);border-radius:8px;overflow:hidden;margin:4px 6px 4px 0';
  var BS = 'font:inherit;font-size:12px;padding:4px 7px;border:none;cursor:pointer';
  var GS = 'display:inline-flex;border:1px solid var(--strong);border-radius:6px;overflow:hidden';
  function grp(attr, ops, cur, small) {
    return '<div style="' + (small ? GS : G) + '">' + ops.map(function (o) {
      var on = o[0] == cur;
      return '<button ' + attr + ' data-v="' + o[0] + '" style="' + (small ? BS : B) + ';background:' + (on ? 'var(--accent)' : 'transparent') + ';color:' + (on ? 'var(--bg)' : 'var(--ink)') + '">' + o[1] + '</button>';
    }).join('') + '</div>';
  }
  var LAB = { of: 'Oficial', amb: 'Ambiguo', op: 'Opositor' };
  var MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  function fecha(s) { var d = new Date(s + 'T12:00:00'); return d.getDate() + ' ' + MES[d.getMonth()]; }
  function panel() {
    var h = '<div style="font-size:13px;font-weight:600;color:var(--ink);margin:10px 0 0">Elecciones provinciales 2027</div>' +
      grp('data-pv-modo', [['no', 'Sin efecto electoral provincial'], ['prob', 'Efecto más probable'], ['int', 'Efecto interactivo']], st.modo);
    if (st.modo != 'no') {
      var e = window.PROVEF();
      h += '<div style="font-size:13px;color:var(--ink2);margin:4px 0 0;line-height:1.45"><strong style="color:var(--ink)">Ajuste para LLA por las provinciales:</strong> con PASO, PASO ' + f(e.P) + ' · general ' + f(e.G) + ' · balotaje ' + f(e.B) + ' puntos; sin PASO, general ' + f(e.GS) + ' · balotaje ' + f(e.BS) + '. ' +
        (st.modo == 'prob' ? 'Aplica el resultado más probable de cada provincia.' : 'Elija el resultado de cada provincia.') + (votaron() ? ' Ya votaron ' + votaron() + ' de ' + PD.provincias.length + ': para ellas se usa el resultado real.' : '') + ' Detalle en Metodología.</div>';
    }
    if (st.modo == 'int') {
      h += '<div style="margin:8px 0 0;font-size:13px;color:var(--ink2)">Escenarios rápidos</div>' +
        grp('data-pv-rap', [['esp', 'Lo esperado'], ['buen', 'Buen año para LLA'], ['mal', 'Mal año para LLA'], ['cba', 'Córdoba la gana LLA'], ['sf', 'Santa Fe con alianza']], null);
      h += '<div style="margin:6px 0 0;font-size:13px;color:var(--ink2)">Buenos Aires, gobernador (mismo día que la Nación)</div>' +
        (PD.ba.real ? '<div style="font-size:13px"><strong>Votó:</strong> ' + PD.ba.real.texto + '</div>' : grp('data-pv-ba', [['pc', 'Peronismo claro'], ['pa', 'Peronismo ajustado'], ['sa', 'Santilli ajustado'], ['sc', 'Santilli claro']], st.ba));
      h += '<div style="margin:6px 0 0;font-size:13px;color:var(--ink2)">Ciudad de Buenos Aires (si vota con la Nación)</div>' +
        (PD.caba.real ? '<div style="font-size:13px"><strong>Votó:</strong> ' + PD.caba.real.texto + '</div>' : grp('data-pv-caba', [['of', 'PRO con LLA'], ['amb', 'PRO sin LLA'], ['op', 'Gana la oposición']], st.caba));
      h += '<div style="margin:8px 0 2px;font-size:13px;color:var(--ink2)">Cada provincia, por fecha. El punto marca el resultado más probable.</div><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:4px 14px">';
      PD.provincias.forEach(function (p) {
        var r = res(p);
        h += '<div style="display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:13px;padding:3px 0;border-bottom:1px solid var(--line)"><span>' + p.n + ' <span style="color:var(--ink2)">' + fecha(p.fecha) + (p.real ? ' · votó: ' + p.real.ganador + ' ' + String(p.real.pct).replace('.', ',') + ' %' : '') + '</span></span>' +
          (p.real ? '<strong style="font-size:12px">' + LAB[r] + ' ✓</strong>' : grp('data-pv-prov="' + p.n + '"', ['of', 'amb', 'op'].map(function (k) { return [k, LAB[k] + (p.esperado == k ? ' •' : '')]; }), r, 1)) + '</div>';
      });
      h += '</div>';
    }
    return h;
  }
  function pinta() {
    document.querySelectorAll('.pv-panel').forEach(function (el) { el.innerHTML = panel(); });
  }
  function todo() { pinta(); if (window.proyDraw) window.proyDraw(); if (window.compDraw) window.compDraw(); }
  function rapido(k) {
    st.sel = {}; st.ba = PD.ba.esperado; st.caba = PD.caba.esperado;
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
    else if (b.hasAttribute('data-pv-ba')) st.ba = b.dataset.v;
    else if (b.hasAttribute('data-pv-caba')) st.caba = b.dataset.v;
    else if (b.hasAttribute('data-pv-prov')) st.sel[b.getAttribute('data-pv-prov')] = b.dataset.v;
    todo();
  });
  /* Metodología: cuadros generados desde los datos */
  function metodo() {
    var el = document.getElementById('pvMetodo'); if (!el) return;
    var EST = { c: 'confirmada', a: 'anunciada', e: 'estimada' };
    var h = '<table style="font-size:13px;width:100%;margin-top:6px"><thead><tr><th style="text-align:left">Provincia</th><th>Fecha</th><th>Estado</th><th>Más probable</th><th>Resultado real</th><th>Peso</th><th>Si gana oficial</th><th>Si gana ambiguo</th><th>Si gana opositor</th></tr></thead><tbody>';
    PD.provincias.forEach(function (p) {
      var cel = ['of', 'amb', 'op'].map(function (r) { return unoSolo(p, r); });
      h += '<tr><td style="text-align:left">' + p.n + '</td><td>' + (p.paso_prov ? 'PASO ' + fecha(p.paso_prov) + ' · ' : '') + fecha(p.fecha) + '</td><td>' + EST[p.estado] + '</td><td>' + LAB[p.esperado] + '</td><td>' + (p.real ? LAB[p.real.res] + ': ' + p.real.ganador + ' ' + String(p.real.pct).replace('.', ',') + ' % (margen ' + String(p.real.margen).replace('.', ',') + ')' : '—') + '</td><td>' + peso(p).toFixed(2).replace('.', ',') + '</td>' + cel.map(function (c) { return '<td style="white-space:nowrap">' + c + '</td>'; }).join('') + '</tr>';
    });
    el.innerHTML = h + '</tbody></table><div style="font-size:12px;color:var(--ink2);margin-top:4px">Puntos para LLA en PASO / general / balotaje, con PASO nacionales, sin racha ni topes.</div>';
  }
  function unoSolo(p, r) {
    var e = p.efecto[r], w = peso(p); if (r == 'of' && p.propio) w = Math.max(w, PD.reglas.vuelco);
    var MAX = PD.reglas.max_con, dP = new Date(p.senal_paso || p.fecha), dG = new Date(p.fecha);
    return ['P', 'G', 'B'].map(function (k, i) {
      var d = k == 'P' ? dP : dG; if (d >= NAC[k]) return '—';
      var dec = (NAC[k] - d) / 864e5 > PD.reglas.dias_mitad ? 0.5 : 1, v = e[i] * w * MAX[k] * dec;
      return Math.abs(v) < 0.005 ? '0' : (v > 0 ? '+' : '−') + Math.abs(v).toFixed(2).replace('.', ',');
    }).join(' / ');
  }
  function init() { pinta(); metodo(); }
  var prevAct = window.alActualizar; window.alActualizar = function (A) { if (prevAct) prevAct(A); pinta(); };
  if (document.readyState == 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
