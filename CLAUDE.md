# Instrucciones para Claude

Sitio estático "Elecciones 2027" de Franco Martín López. Responder en español, sin voseo.

## Revisión mensual (tarea programada)

1. Leer `datos/actual.json`. Si `mes` no cambió desde la última revisión (ver el último commit "Revisión:"), terminar sin cambios.
2. Los números marcados con `data-v`, `data-mes`, `data-ratios` y la "Lectura" se completan solos con JavaScript. Los valores de respaldo del HTML los actualiza `scripts/respaldo.py` (lo corre la acción); no tocarlos a mano.
3. Revisar los textos interpretativos que no se calculan solos y corregirlos si el nuevo mes los vuelve falsos:
   - `index.html`, desplegable "Lecturas": el punto "Contraste con la Tabla A" (compara el 39,0 % del escenario 2027 B con la general sin PASO del índice).
   - `index.html`, bloque proyectado: notas de trayectorias y años de referencia.
   - `index.html`, encabezado: la nota de diferencias entre los dos análisis.
   - El tercer bloque (composición de fuerzas, `#p2027comp`) toma la base de `datos/actual.json` sola; sus diferencias por escenario (`var COMP`, 44 de las Tablas A a L, 80 de la Tabla M, 712 variantes con Kicillof y Massa (`scripts/kicillof_massa.py`) 466 con Bullrich candidata del PRO (`scripts/bullrich.py`) y 240 con Cristina Kirchner candidata, como sensibilidad (`scripts/cristina.py`, marcadas con `cr`, fuera del recuento y de los botones); la hoja "Todas las combinaciones" del Excel la rehace `scripts/excel_km.py`; `scripts/recuento.py` marca los 170 casos del recuento con `"p":1` e imprime sus cifras, y va al final) son fijas y solo cambian si se rehacen las tablas de escenarios.
   - Las cifras de la sección de escenarios (cifras grandes, "Lo más importante", "Recuento de los 170 casos", encabezado y su nota de Metodología) salen de `scripts/recuento.py`, con valores de las tablas: no cambian con el ICG. Si se rehace COMP, correr los scripts en orden (kicillof_massa, cristina, bullrich, recuento, excel_km) y revisar esos textos.
   - Elecciones provinciales 2027 (`datos/provincias.js` + `js/provincias.js`; selector en el bloque proyectado y en el de escenarios, desplegable en Metodología): actualizar fechas y su estado (c confirmada, a anunciada, e estimada) cuando haya anuncios, y cargar el resultado real de cada provincia cuando vote (campo a agregar: `real`). No cambiar pesos ni efectos sin pedido expreso.
   - Las tablas de escenarios (A a M) ya no están en la página: están en `datos/escenarios-2027.xlsx` (valores fijos, no se actualizan con el ICG). Si se rehacen los escenarios, regenerar el Excel.
4. `datos/economia.json` tiene el ajuste por proyección económica (pesimista, central y optimista, por región y mes). Lo recalcula solo la acción "Actualizar series económicas" (día 22 de cada mes): baja las series (`scripts/economia/fuentes.py`), lee el REM del BCRA (`scripts/economia/rem.py` → `datos/rem.json`) y corre `scripts/economia/calcular.py`. Al día siguiente la acción diaria lo aplica al sitio. Si `actualizado` en `datos/economia.json` tiene más de dos meses, la acción está fallando: avisar a Franco.
5. `datos/parametros.json` incluye el ajuste por continuidad del oficialismo (+1 PASO y general, +0,5 balotaje: Milei buscaría un segundo período seguido; base en `datos/base_gobernadores.csv`). No cambiar `datos/parametros.json` ni las tablas de escenarios salvo pedido expreso.
6. Commit "Revisión: ICG de <mes>" y push a `main`.

Si la acción de GitHub falló (no hay mes nuevo varios días después del fin de mes), avisar a Franco: desde la sesión de Claude no se puede descargar de utdt.edu.
