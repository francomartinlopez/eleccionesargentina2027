"""Descarga las series económicas a fuentes/eco/ (no se suben al repositorio).

Uso: python scripts/economia/fuentes.py
Las direcciones que cambian con cada publicación (OEDE, DNRPA, Índice Líder) se buscan en su página.
"""
import re, sys, json
from pathlib import Path
import requests

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / 'fuentes/eco'
UA = {'User-Agent': 'Mozilla/5.0 (eleccionesargentina2027)'}
SSPM = 'https://infra.datos.gob.ar/catalog/sspm/dataset/'
FIJAS = {
    'ripte.csv': SSPM + '158/distribution/158.1/download/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv',
    'jubmin.csv': SSPM + '58/distribution/58.1/download/haber-minimo-jubilatorio-pesos-corrientes-valores-mensuales-desde-1971.csv',
    'auh.csv': SSPM + '165/distribution/165.1/download/asignacion-universal-por-hijo-pesos-corrientes.csv',
    'ipc_hist.csv': SSPM + '178/distribution/178.1/download/ipc-historico.csv',
    'ipc_sl.csv': SSPM + '197/distribution/197.1/download/indice-precios-consumidor-san-luis-2003-100.csv',
    'ipc16.csv': SSPM + '145/distribution/145.3/download/indice-precios-al-consumidor-nivel-general-base-diciembre-2016-mensual.csv',
    'emae04.csv': SSPM + '143/distribution/143.3/download/emae-valores-anuales-indice-base-2004-mensual.csv',
    'tc.csv': SSPM + '175/distribution/175.1/download/tipos-de-cambio-historicos.csv',
    'sipa_prov.csv': SSPM + '154/distribution/154.2/download/asalariados-registrados-sector-privado-segun-provincia-datos-sin-estacionalidad.csv',
    'spn_07-14.csv': SSPM + '379/distribution/379.8/download/sector-publico-nacional-valores-mensuales-07-14.csv',
    'spn_17.csv': SSPM + '379/distribution/379.9/download/sector-publico-nacional-valores-mensuales-17.csv',
}
OEDE = 'https://www.argentina.gob.ar/trabajo/estadisticas/oede-estadisticas-provinciales'
IL = 'https://www.utdt.edu/ver_contenido.php?id_contenido=27169&id_item_menu=44671'
DNRPA = 'https://datos.jus.gob.ar/api/3/action/package_show?id=estadistica-de-tramites-de-automotores'

def bajar(url, nombre, minimo=2000):
    r = requests.get(url, headers=UA, timeout=300); r.raise_for_status()
    if len(r.content) < minimo: raise RuntimeError(f'{nombre}: archivo demasiado chico ({len(r.content)} bytes)')
    (DEST / nombre).write_bytes(r.content); print('ok', nombre, len(r.content))

def main():
    DEST.mkdir(parents=True, exist_ok=True); fallas = []
    for n, u in FIJAS.items():
        try: bajar(u, n)
        except Exception as e: fallas.append(f'{n}: {e}')
    try:
        html = requests.get(OEDE, headers=UA, timeout=120).text
        for pat, n in [(r'provinciales_serie_empleo_trimestral_2dig_\d+\.xlsx', 'oede_empleo.xlsx'),
                       (r'provinciales_serie_remuneraciones_mensual_2dig_\d+\.xlsx', 'oede_remuneraciones.xlsx')]:
            f = re.search(r'/sites/default/files/' + pat, html).group(0)
            bajar('https://www.argentina.gob.ar' + f, n, 100000)
    except Exception as e: fallas.append(f'OEDE: {e}')
    try:
        html = requests.get(IL, headers=UA, timeout=120).text
        u = re.search(r'https?://www\.utdt\.edu/download\.php\?fname=[^"]+\.xls', html).group(0)
        bajar(u, 'il.xls')
    except Exception as e: fallas.append(f'Índice Líder: {e}')
    try:
        res = requests.get(DNRPA, headers=UA, timeout=120).json()['result']['resources']
        u = [x['url'] for x in res if 'estadistica-inscripciones-iniciales-automotores' in x['url'] and x['url'].endswith('.csv')][0]
        bajar(u, 'autos.csv', 100000)
    except Exception as e: fallas.append(f'DNRPA: {e}')
    if fallas:
        print('FALLARON:', *fallas, sep='\n  ')
        sys.exit(1)

if __name__ == '__main__':
    main()
