/* Comportamientos generales: enlaces a desplegables, impresión y botón para volver arriba. */
(function () {
  function abrir(id) {
    var el = document.getElementById(id); if (!el) return null;
    var d = el.tagName == 'DETAILS' ? el : el.closest('details');
    while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); }
    return el;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]'); if (!a) return;
    var id = decodeURIComponent(a.getAttribute('href').slice(1)); if (id) abrir(id);
  });
  function hash() { if (location.hash.length > 1) { var el = abrir(decodeURIComponent(location.hash.slice(1))); if (el) el.scrollIntoView(); } }
  window.addEventListener('hashchange', hash);
  if (location.hash.length > 1) setTimeout(hash, 0);
  window.addEventListener('beforeprint', function () { document.querySelectorAll('details').forEach(function (d) { if (!d.open) { d.open = true; d.setAttribute('data-imp', ''); } }); });
  window.addEventListener('afterprint', function () { document.querySelectorAll('details[data-imp]').forEach(function (d) { d.open = false; d.removeAttribute('data-imp'); }); });
  var b = document.getElementById('arriba');
  if (b) {
    var ver = function () { b.classList.toggle('ver', window.scrollY > 1200); };
    window.addEventListener('scroll', ver, { passive: true }); ver();
    b.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      var m = document.querySelector('.marca'); if (m) m.focus({ preventScroll: true });
    });
  }
})();
