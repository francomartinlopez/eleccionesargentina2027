# Instrucciones para Claude

Sitio estático "Elecciones 2027" de Franco Martín López. Responder en español, sin voseo.

## Revisión mensual (tarea programada)

1. Leer `datos/actual.json`. Si `mes` no cambió desde la última revisión (ver el último commit "Revisión:"), terminar sin cambios.
2. Los números marcados con `data-v`, `data-mes`, `data-ratios` y la "Lectura" se completan solos con JavaScript. Los valores de respaldo del HTML los actualiza `scripts/respaldo.py` (lo corre la acción); no tocarlos a mano.
3. Revisar los textos interpretativos que no se calculan solos y corregirlos si el nuevo mes los vuelve falsos:
   - Ya se completan solos (no tocarlos): el mes (`data-mes`), el mes del REM (`data-rem`), la fecha de actualización (`data-actualizado`), el verbo del balotaje del encabezado (`data-bal-verbo`), la lectura de la general en "Contraste con la Tabla A" (`data-pvgen`), la tendencia del ICG en "Qué implica para 2027" (`data-tend`) y los totales del efecto provincial en Metodología (`data-pvtot`).
   - `index.html`, desplegable "Lecturas": el punto "Contraste con la Tabla A" (compara el 39,0 % del escenario 2027 B con la general sin PASO del índice): revisar que la comparación siga siendo cierta.
   - `index.html`, desplegable "Por qué el índice acertó o falló" → "Qué implica para 2027": las frases sobre oficialismo unido y desgaste.
   - `index.html`, bloque proyectado: notas de trayectorias y años de referencia.
   - `index.html`, encabezado: la nota de diferencias entre los dos análisis.
   - El tercer bloque (composición de fuerzas, `#p2027comp`) toma la base de `datos/actual.json` sola; sus diferencias por escenario (`var COMP` en `datos/comp.js`, 44 de las Tablas A a L, 80 de la Tabla M, 712 variantes con Kicillof y Massa (`scripts/kicillof_massa.py`) 466 con Bullrich candidata del PRO (`scripts/bullrich.py`) y 240 con Cristina Kirchner candidata, como sensibilidad (`scripts/cristina.py`, marcadas con `cr`, fuera del recuento y de los botones); la hoja "Todas las combinaciones" del Excel la rehace `scripts/excel_km.py`; `scripts/recuento.py` marca los 170 casos del recuento con `"p":1` e imprime sus cifras, y va al final) son fijas y solo cambian si se rehacen las tablas de escenarios.
   - Las cifras de la sección de escenarios (cifras grandes, "Lo más importante", "Recuento de los 170 casos", encabezado y su nota de Metodología) salen de `scripts/recuento.py`, con valores de las tablas: no cambian con el ICG. Si se rehace COMP, correr los scripts en orden (kicillof_massa, cristina, bullrich, recuento, excel_km), revisar esos textos y correr `scripts/verificar.py`, que compara las cifras citadas en la página con las de `datos/comp.js`.
   - Elecciones provinciales 2027 (`datos/provincias.js` + `js/provincias.js`): ver la sección "Revisión semanal de provincias". No cambiar pesos, efectos, probabilidades (`prob`) ni el resultado esperado sin pedido expreso.
   - Las tablas de escenarios (A a M) ya no están en la página: están en `datos/escenarios-2027.xlsx` (valores fijos, no se actualizan con el ICG). Si se rehacen los escenarios, regenerar el Excel.
4. `datos/economia.json` tiene el ajuste por proyección económica (pesimista, central y optimista, por región y mes). Lo recalcula solo la acción "Actualizar series económicas" (día 22 de cada mes): baja las series (`scripts/economia/fuentes.py`), lee el REM del BCRA (`scripts/economia/rem.py` → `datos/rem.json`) y corre `scripts/economia/calcular.py`. Al día siguiente la acción diaria lo aplica al sitio. Si `actualizado` en `datos/economia.json` tiene más de dos meses, la acción está fallando: avisar a Franco.
5. `datos/parametros.json` incluye el ajuste por continuidad del oficialismo (+1 PASO y general, +0,5 balotaje: Milei buscaría un segundo período seguido; base en `datos/base_gobernadores.csv`). No cambiar `datos/parametros.json` ni las tablas de escenarios salvo pedido expreso.
6. Correr `python scripts/verificar.py` (también lo corren las acciones). Commit "Revisión: ICG de <mes>" y push a `main`.

Si la acción de GitHub falló (no hay mes nuevo varios días después del fin de mes), avisar a Franco: desde la sesión de Claude no se puede descargar de utdt.edu.

## Revisión semanal de provincias (tarea programada, los lunes)

1. Fechas: buscar anuncios nuevos de fecha de elección provincial 2027 (decretos, juntas electorales, anuncios de gobernadores). Si una provincia fijó o cambió fecha, actualizar `fecha` (y `paso_prov` o `senal_paso` si corresponde) y `estado` en `datos/provincias.js`: `c` confirmada (decreto o junta electoral), `a` anunciada (sin decreto), `e` estimada. Actualizar también `fuente` (`texto` y `url` del decreto o la nota). Si una provincia pasa a votar el mismo día que la Nación, avisar a Franco antes de cambiar la lógica.
2. Resultados: si alguna provincia votó desde la última revisión, cargar `real` con el escrutinio (provisorio si todavía no hay definitivo; reemplazarlo en la semana del definitivo): `res` (of = gana LLA o aliado formal; amb = oficialismo provincial que negocia pero compite aparte; op = peronismo opositor), `ganador`, `pct`, `segundo`, `pct2`, `margen` (pct − pct2), `fecha`, `fuente`, `url`. Buenos Aires y la Ciudad usan `real` con `res` y `texto` (ver el comentario del archivo). Si la clasificación es dudosa, cargar lo seguro y avisar a Franco.
3. Correr `python scripts/verificar.py`. Si no hubo cambios, terminar sin commit. Si los hubo: commit "Provincias: <qué cambió>" y push a `main`, y avisar a Franco con un resumen de una o dos líneas.
