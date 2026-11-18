# Instrucciones para Claude

Sitio estático "Elecciones 2027" de Franco Martín López. Responder en español, sin voseo.

## Revisión mensual (tarea programada)

1. Leer `datos/actual.json`. Si `mes` no cambió desde la última revisión (ver el último commit "Revisión:"), terminar sin cambios.
2. Los números marcados con `data-v`, `data-mes`, `data-ratios` y la "Lectura" se completan solos con JavaScript. No tocarlos a mano, pero sí actualizar el valor de respaldo escrito en el HTML para que coincida con `actual.json`.
3. Revisar los textos interpretativos que no se calculan solos y corregirlos si el nuevo mes los vuelve falsos:
   - `index.html`, desplegable "Lecturas": el punto "Contraste con la Tabla A" (compara el 38,0 % del escenario 2027 B con la general sin PASO del índice).
   - `index.html`, bloque proyectado: notas de trayectorias y años de referencia.
   - `index.html`, encabezado: la nota de diferencias entre los dos análisis.
4. No cambiar `datos/parametros.json` ni las tablas de escenarios salvo pedido expreso.
5. Commit "Revisión: ICG de <mes>" y push a `main`.

Si la acción de GitHub falló (no hay mes nuevo varios días después del fin de mes), avisar a Franco: desde la sesión de Claude no se puede descargar de utdt.edu.
