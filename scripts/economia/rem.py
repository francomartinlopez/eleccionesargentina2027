"""Actualiza datos/rem.json con la última publicación del REM del BCRA (medianas).

Uso: python scripts/economia/rem.py
Si no puede bajar o leer el archivo, deja datos/rem.json como estaba y termina con error.
"""
import io, json, re, sys
from pathlib import Path
import pandas as pd, requests

RAIZ = Path(__file__).resolve().parents[2]
PAGINA = 'https://www.bcra.gob.ar/PublicacionesEstadisticas/Relevamiento_Expectativas_de_Mercado.asp'
UA = {'User-Agent': 'Mozilla/5.0 (eleccionesargentina2027)'}
MESES = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}

def periodo(x):
    if isinstance(x, (pd.Timestamp,)) or hasattr(x, 'month'):
        try: return pd.Period(pd.Timestamp(x), 'M')
        except Exception: return None
    s = str(x).strip().lower()
    m = re.match(r'([a-z]{3})[a-z]*[-/ .]*(\d{2,4})$', s)
    if m and m.group(1) in MESES:
        y = int(m.group(2)); y = y + 2000 if y < 100 else y
        return pd.Period(f'{y}-{MESES[m.group(1)]:02d}', 'M')
    return None

def bloque(df, clave):
    """Filas mensuales (período, mediana) que siguen al título que contiene `clave`."""
    col0 = df.iloc[:, 0].astype(str).str.lower()
    ini = [i for i, v in enumerate(col0) if clave in v]
    if not ini: return {}
    i0 = ini[0]
    # columna de la mediana: buscar 'mediana' en las filas cercanas
    cm = None
    for i in range(max(0, i0 - 3), min(len(df), i0 + 4)):
        for j, v in enumerate(df.iloc[i]):
            if 'mediana' in str(v).lower(): cm = j; break
        if cm is not None: break
    if cm is None: return {}
    out = {}
    for i in range(i0 + 1, min(len(df), i0 + 40)):
        p = periodo(df.iloc[i, 0]) or periodo(df.iloc[i, 1])
        if p is None:
            if out: break
            continue
        try: out[str(p)] = round(float(df.iloc[i, cm]), 3)
        except Exception: pass
    return out

def main():
    html = requests.get(PAGINA, headers=UA, timeout=120).text
    links = re.findall(r'href="([^"]*tablas?-relevamiento-expectativas-mercado[^"]*\.xlsx)"', html, re.I)
    if not links: sys.exit('No se encontró el Excel del REM en ' + PAGINA)
    u = links[0]; u = u if u.startswith('http') else 'https://www.bcra.gob.ar/' + u.lstrip('/').replace('../', '')
    x = pd.ExcelFile(io.BytesIO(requests.get(u, headers=UA, timeout=180).content))
    df = pd.read_excel(x, sheet_name=0, header=None)
    infl = bloque(df, 'precios minoristas'); dol = bloque(df, 'tipo de cambio'); act = bloque(df, 'pib')
    if len(infl) < 3 or len(dol) < 2:
        print('No se pudo leer el REM. Primeras filas de la hoja', x.sheet_names[0], ':')
        print(df.head(80).to_string()); sys.exit(1)
    m = re.search(r'([a-z]{3})[a-z]*-(\d{4})\.xlsx', u.lower())
    rel = f'{m.group(2)}-{MESES[m.group(1)]:02d}' if m and m.group(1) in MESES else None
    dest = RAIZ / 'datos/rem.json'; prev = json.loads(dest.read_text())
    out = dict(prev); out.update({'relevamiento': rel, 'fuente': u, 'inflacion': infl, 'dolar': dol})
    if act: out['actividad_trimestral'] = act
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1)); print('REM', rel, 'inflación', infl, 'dólar', dol)

if __name__ == '__main__':
    main()
