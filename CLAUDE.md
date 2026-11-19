# Instrucciones para Claude

Sitio estático "Elecciones 2027" de Franco Martín López. Responder en español, sin voseo.

## Revisión mensual (tarea programada)

1. Leer `datos/actual.json`. Si `mes` no cambió desde la última revisión (ver el último commit "Revisión:"), terminar sin cambios.
2. Los números marcados con `data-v`, `data-mes`, `data-ratios` y la "Lectura" se completan solos con JavaScript. Los valores de respaldo del HTML los actualiza `scripts/respaldo.py` (lo corre la acción); no tocarlos a mano.
3. Revisar los textos interpretativos que no se calculan solos y corregirlos si el nuevo mes los vuelve falsos:
   - `index.html`, desplegable "Lecturas": el punto "Contraste con la Tabla A" (compara el 39,0 % del escenario 2027 B con la general sin PASO del índice).
   - `index.html`, bloque proyectado: notas de trayectorias y años de referencia.
   - `index.html`, encabezado: la nota de diferencias entre los dos análisis.
   - El tercer bloque (composición de fuerzas, `#p2027comp`) toma la base de `datos/actual.json` sola; sus diferencias por escenario (`var COMP`, 44 de las Tablas A a L y 80 de la Tabla M) son fijas y solo cambian si se rehacen las tablas de escenarios.
   - Las tablas de escenarios (A a M) ya no están en la página: están en `datos/escenarios-2027.xlsx` (valores fijos, no se actualizan con el ICG). Si se rehacen los escenarios, regenerar el Excel.
4. `datos/economia.json` tiene el ajuste por proyección económica (pesimista, central y optimista, por región y mes). Lo recalcula solo la acción "Actualizar series económicas" (día 22 de cada mes): baja las series (`scripts/economia/fuentes.py`), lee el REM del BCRA (`scripts/economia/rem.py` → `datos/rem.json`) y corre `scripts/economia/calcular.py`. Al día siguiente la acción diaria lo aplica al sitio. Si `actualizado` en `datos/economia.json` tiene más de dos meses, la acción está fallando: avisar a Franco.
5. `datos/parametros.json` incluye el ajuste por continuidad del oficialismo (+1 PASO y general, +0,5 balotaje: Milei buscaría un segundo período seguido; base en `datos/base_gobernadores.csv`). No cambiar `datos/parametros.json` ni las tablas de escenarios salvo pedido expreso.
6. Commit "Revisión: ICG de <mes>" y push a `main`.

Si la acción de GitHub falló (no hay mes nuevo varios días después del fin de mes), avisar a Franco: desde la sesión de Claude no se puede descargar de utdt.edu.
