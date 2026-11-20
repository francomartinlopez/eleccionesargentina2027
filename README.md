# Elecciones 2027

Análisis electoral de la presidencial argentina 2027, de Franco Martín López: el Índice de Confianza en el Gobierno (ICG) de la Universidad Torcuato Di Tella, corregido y leído por región, escenarios de coaliciones (170 casos de alianzas con Kicillof, Massa y Bullrich, y Cristina Kirchner como sensibilidad) y el efecto de las elecciones provinciales de 2027.

Sitio estático publicado en Netlify: https://eleccionesargentina2027.netlify.app/

## Página

Todo está en `index.html`, en una sola página con menú: el índice (bloques 2027, gráfico, mapa por región), los escenarios (recuento de 170 casos y cuadro interactivo) y la metodología. Las tablas de escenarios (A a M) y todas las combinaciones están en `datos/escenarios-2027.xlsx`.

- `css/estilo.css` y `css/tipografias/`: estilos y fuentes (IBM Plex Sans y Source Serif 4, alojadas en el sitio).
- `js/datos.js`: completa los números con `datos/actual.json`.
- `js/provincias.js` y `datos/provincias.js`: efecto de las elecciones provinciales 2027 (fechas, probabilidades, fuentes y resultados reales).
- `datos/comp.js`: las 1.542 composiciones del cuadro de escenarios.
- `js/chart.umd.js`: Chart.js 4.4.1 (licencia MIT), para el gráfico de barras.
- `js/sitio.js`: enlaces a desplegables, impresión y botón para volver arriba.

## Actualización

1. La acción `.github/workflows/actualizar.yml` corre del 20 a fin de cada mes (la Di Tella publica entre el 24 y el 28; también se puede lanzar a mano). Descarga los microdatos de la Di Tella (`scripts/descargar.py`), recalcula (`scripts/actualizar.py`), actualiza los valores de respaldo de la página (`scripts/respaldo.py`) y corre los controles (`scripts/verificar.py`). Si hay un mes nuevo, sube los cambios y Netlify publica.
2. La acción `.github/workflows/economia.yml` (día 22 de cada mes) recalcula el ajuste por proyección económica (`scripts/economia/`).
3. La acción `.github/workflows/verificar.yml` corre los controles en cada cambio de `main`.
4. Dos tareas programadas de Claude revisan cada mes los textos interpretativos y cada lunes las fechas y resultados provinciales (ver `CLAUDE.md`).

`datos/parametros.json` tiene los coeficientes calibrados. Solo cambian si se recalibra tras una elección.

## Escenarios

Las composiciones se generan en orden con `scripts/kicillof_massa.py`, `cristina.py`, `bullrich.py`, `recuento.py` y `excel_km.py`. Después, `scripts/verificar.py` comprueba que las cifras citadas en la página coincidan con los datos.

## Fuente

Índice de Confianza en el Gobierno. Escuela de Gobierno. Universidad Torcuato Di Tella. https://www.utdt.edu/icg
