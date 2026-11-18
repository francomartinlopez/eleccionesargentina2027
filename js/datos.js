/* Completa la página con datos/actual.json, que se regenera cada mes con scripts/actualizar.py */
(function(){
var MES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
function f(x,d){return x.toFixed(d==null?1:d).replace('.',',');}
function get(o,p){return p.split('.').reduce(function(a,k){return a==null?a:a[k];},o);}
function mesTxt(k){var p=k.split('-');return MES[+p[1]-1]+' de '+p[0];}
function rangoMeses(a,b){var pa=a.split('-'),pb=b.split('-');return pa[0]==pb[0]?MES[+pa[1]-1]+' a '+mesTxt(b):mesTxt(a)+' a '+mesTxt(b);}
function ratios(R){var g={};Object.keys(R).forEach(function(r){var k=f(R[r],2);(g[k]=g[k]||[]).push(r);});
  return Object.keys(g).sort(function(a,b){return parseFloat(a.replace(',','.'))-parseFloat(b.replace(',','.'));}).map(function(k){return g[k].join(' y ')+' '+k;}).join('; ');}
function lectura(A){var g=A.actual.gen,s=A.actual.sin,b=A.actual.bal,t='';
  function pv(r,q){return r[1]>=45?q+'todo el rango supera el 45 %: el oficialismo ganaría en primera vuelta. ':r[1]>=40?q+'todo el rango supera el 40 %: el oficialismo ganaría en primera vuelta si le saca más de 10 puntos al segundo'+(r[2]>=45?', o sin condiciones en la parte alta, por encima del 45 %. ':'. '):r[2]>=40?q+'el rango cruza el 40 %: iría a balotaje salvo en la parte alta, y aun ahí necesitaría 10 puntos de ventaja. ':q+'todo el rango queda debajo del 40 %: iría a balotaje. ';}
  t+=pv(g,'con PASO, ');t+=pv(s,'Sin PASO, ');
  t+=b[2]<50?'En los dos casos, un balotaje hoy lo perdería'+(b[2]>=48?' por poco':'')+': todo el rango queda debajo del 50 %.':b[1]>=50?'En los dos casos, un balotaje hoy lo ganaría: todo el rango supera el 50 %.':'En los dos casos, un balotaje hoy quedaría abierto: el rango cruza el 50 %.';
  return t;}
function celda(v,big){return '<td class="g" style="padding-left:4px;padding-right:2px"><strong style="white-space:nowrap'+(big?';color:var(--accent)':'')+'">'+f(v[1])+' %–'+f(v[2])+' %</strong></td>';}
function aplicar(A){
  window.ACTUAL=A;
  document.querySelectorAll('[data-mes]').forEach(function(e){e.textContent=mesTxt(A.mes);});
  document.querySelectorAll('[data-v]').forEach(function(e){var v=get(A,e.dataset.v);if(v==null)return;
    if(Array.isArray(v))e.textContent=e.hasAttribute('data-r')?f(v[1])+(e.closest('header')?' y ':'-')+f(v[2]):f(v[0]);else e.textContent=f(v,+e.dataset.d||1);});
  document.querySelectorAll('[data-ratios]').forEach(function(e){e.textContent=ratios(A.ratios);});
  document.querySelectorAll('[data-meses-ratio]').forEach(function(e){e.textContent=rangoMeses(A.meses_ratio[0],A.meses_ratio[1]);});
  document.querySelectorAll('[data-bal-verbo]').forEach(function(e){var b=A.actual.bal;e.textContent=b[0]<50?'que LLA perdería':'que LLA ganaría';});
  var lec=lectura(A);
  var al=document.getElementById('aLectura');if(al)al.innerHTML='<strong>Lectura:</strong> '+lec;
  var pl=document.getElementById('pLectura');if(pl)pl.textContent=lec.charAt(0).toUpperCase()+lec.slice(1);
  var ar=document.getElementById('aRows'),a=A.actual;
  if(ar)ar.innerHTML='<tr><td colspan="3" style="text-align:left;border-bottom:none;padding-bottom:0;font-size:.9em;color:var(--ink2)"><strong>Con PASO</strong></td></tr><tr>'+celda(a.paso)+celda(a.gen,1)+celda(a.bal)+'</tr>'+'<tr><td colspan="3" style="text-align:left;border-bottom:none;padding-bottom:0;font-size:.9em;color:var(--ink2)"><strong>Sin PASO</strong></td></tr><tr>'+'<td class="g" style="text-align:center">—</td>'+celda(a.sin,1)+celda(a.bal)+'</tr>';
  if(window.proyDraw){window.PD=A.proyectado;if(A.proyectado_eco)window.PDE=A.proyectado_eco;window.proyDraw();}
  if(window.compDraw)window.compDraw();
  if(window.regRD){window.regRD['2027 P (proy.)']=A.mapa2027;window.regDraw();}
  if(window.alActualizar)window.alActualizar(A);
}
var datos=fetch('datos/actual.json',{cache:'no-cache'}).then(function(r){return r.json();});
var listo=new Promise(function(ok){if(document.readyState!='loading')ok();else document.addEventListener('DOMContentLoaded',ok);});
Promise.all([datos,listo]).then(function(x){aplicar(x[0]);}).catch(function(){});
})();
