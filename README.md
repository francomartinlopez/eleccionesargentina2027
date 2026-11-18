# Elecciones 2027

Análisis electoral de la presidencial argentina 2027: el Índice de Confianza en el Gobierno (ICG) de la Universidad Torcuato Di Tella, corregido y leído por región, y 52 escenarios de coaliciones.

Sitio estático publicado en Netlify.

## Páginas

- `index.html`: portada con la serie del ICG y la lectura del último mes.
- `indice.html`: el ICG corregido, las proyecciones 2027 y el mapa por región.
- `escenarios.html`: las tablas de escenarios A a L.
- `metodologia.html`: cómo se calcula todo y las fuentes.

## Actualización mensual

1. La acción `.github/workflows/actualizar.yml` corre todos los días. Descarga los microdatos de la Di Tella (`scripts/descargar.py`) y recalcula (`scripts/actualizar.py`). Si hay un mes nuevo, sube `datos/actual.json` y `datos/icg_mensual.json`, y Netlify publica.
2. Las páginas leen `datos/actual.json` al cargar y completan los números, el mes y la lectura.
3. Una tarea programada de Claude revisa cada mes los textos interpretativos que no se actualizan solos (ver `CLAUDE.md`).

`datos/parametros.json` tiene los coeficientes calibrados. Solo cambian si se recalibra tras una elección.

## Fuente

Índice de Confianza en el Gobierno. Escuela de Gobierno. Universidad Torcuato Di Tella. https://www.utdt.edu/icg
