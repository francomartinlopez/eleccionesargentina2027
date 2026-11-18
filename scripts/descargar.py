"""Descarga los microdatos del ICG desde la página de descargas de la Di Tella.

El nombre del archivo cambia con cada publicación, así que se busca el enlace en la página.
Uso: python scripts/descargar.py fuentes/icg.dta
"""
import re, sys
from pathlib import Path
import requests

PAGINA = 'https://www.utdt.edu/listado_contenidos.php?id_item_menu=28756'
UA = {'User-Agent': 'Mozilla/5.0 (eleccionesargentina2027)'}

def main(destino):
    html = requests.get(PAGINA, headers=UA, timeout=60).text
    m = re.search(r'href="([^"]*download\.php\?fname=[^"]+\.dta)"', html, re.I)
    if not m:
        sys.exit('No se encontró el enlace a los microdatos (.dta) en ' + PAGINA)
    url = m.group(1)
    if url.startswith('/'):
        url = 'https://www.utdt.edu' + url
    elif not url.startswith('http'):
        url = 'https://www.utdt.edu/' + url
    r = requests.get(url, headers=UA, timeout=300)
    r.raise_for_status()
    if len(r.content) < 1_000_000:
        sys.exit(f'El archivo descargado es demasiado chico ({len(r.content)} bytes): {url}')
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    Path(destino).write_bytes(r.content)
    print('Descargado', url, len(r.content), 'bytes')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'fuentes/icg.dta')
