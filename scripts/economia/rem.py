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

def celdas(fila):
    return [v for v in list(fila)[:3] if not (isinstance(v, float) and pd.isna(v)) and str(v).strip() not in ('', 'nan', 'NaT')]

def bloque(df, clave, extra_ref=False, trimestral=False):
    """Medianas del bloque cuyo título contiene `clave`: {período: valor}."""
    ini = [i for i in range(len(df)) if any(clave in str(v).lower() for v in celdas(df.iloc[i]))]
    if not ini: return {}
    i0 = ini[0]; cm = None
    for i in range(i0, min(len(df), i0 + 4)):
        for j, v in enumerate(df.iloc[i]):
            if str(v).strip().lower() == 'mediana': cm = j; hdr = i; break
        if cm is not None: break
    if cm is None: return {}
    out = {}
    for i in range(hdr + 1, min(len(df), hdr + 30)):
        c = celdas(df.iloc[i])
        if not c: break
        p = periodo(c[0]); ref = str(c[1]) if len(c) > 1 else ''
        if trimestral:
            m = re.match(r'trim\.\s*(i{1,3}|iv)-(\d{2})', str(c[0]).strip().lower())
            if m:
                q = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4}[m.group(1)]; y = 2000 + int(m.group(2))
                for k in range(3): out[str(pd.Period(f'{y}-{3*q-2+k:02d}', 'M'))] = round(float(df.iloc[i, cm]) / 3, 3)
            continue
        if p is None and extra_ref:
            m = re.search(r';\s*([a-z]{3})-(\d{2})', ref.lower())
            if m and m.group(1) in MESES: p = pd.Period(f'{2000+int(m.group(2))}-{MESES[m.group(1)]:02d}', 'M')
        if p is None: continue
        if 'i.a.' in ref: continue
        try: out[str(p)] = round(float(df.iloc[i, cm]), 3)
        except Exception: pass
    return dict(sorted(out.items()))

def main():
    html = requests.get(PAGINA, headers=UA, timeout=120).text
    links = [l for l in re.findall(r'href=["\']([^"\']+\.xlsx?)["\']', html, re.I) if re.search(r'relevamiento|expectativas|rem', l, re.I)]
    if not links:
        print('Enlaces de la página:', *re.findall(r'href=["\']([^"\']+)["\']', html)[:200], sep='\n  ')
        sys.exit('No se encontró el Excel del REM en ' + PAGINA)
    print('Excel del REM:', links[:5])
    u = [l for l in links if 'tablas' in l.lower()][0] if any('tablas' in l.lower() for l in links) else links[0]; u = u if u.startswith('http') else 'https://www.bcra.gob.ar/' + u.lstrip('/').replace('../', '')
    import os
    x = pd.ExcelFile(io.BytesIO(requests.get(u, headers=UA, timeout=180).content))
    df = pd.read_excel(x, sheet_name=0, header=None)
    if os.environ.get('REM_DEBUG'):
        print('Hojas:', x.sheet_names)
        with pd.option_context('display.width', 250, 'display.max_columns', 12): print(df.head(120).to_string(max_colwidth=40))
    infl = bloque(df, 'precios minoristas (ipc nivel general'); dol = bloque(df, 'tipo de cambio nominal', extra_ref=True); act = bloque(df, 'pib a precios constantes', trimestral=True)
    if len(infl) < 3 or len(dol) < 2:
        print('No se pudo leer el REM. Primeras filas de la hoja', x.sheet_names[0], ':')
        print(df.head(80).to_string()); sys.exit(1)
    m = re.search(r'(\d{4})-(\d{2})\.xlsx', u)
    rel = f'{m.group(1)}-{m.group(2)}' if m else None
    dest = RAIZ / 'datos/rem.json'; prev = json.loads(dest.read_text())
    out = dict(prev); out.update({'relevamiento': rel, 'fuente': u, 'inflacion': infl, 'dolar': dol})
    if act: out['actividad'] = act
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1)); print('REM', rel, 'inflación', infl, 'dólar', dol)

if __name__ == '__main__':
    main()
