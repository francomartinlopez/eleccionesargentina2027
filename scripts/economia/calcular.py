"""Recalcula datos/economia.json (ajuste del ICG por proyección económica) con las series de fuentes/eco/ y los supuestos del REM en datos/rem.json.

Uso: python scripts/economia/fuentes.py && python scripts/economia/calcular.py
"""
import json, statistics, unicodedata, warnings
from datetime import date
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
def norm(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper().replace('_',' ').strip()
REG={'AMBA':['GRAN BUENOS AIRES','PARTIDOS DE GBA','CAPITAL FEDERAL','CABA'],
 'Pampeana':['BUENOS AIRES','RESTO DE BUENOS AIRES','CORDOBA','SANTA FE','ENTRE RIOS','LA PAMPA'],
 'Cuyo':['MENDOZA','SAN JUAN','SAN LUIS'],'NOA':['JUJUY','SALTA','TUCUMAN','SANTIAGO DEL ESTERO','CATAMARCA','LA RIOJA'],
 'NEA':['MISIONES','CORRIENTES','CHACO','FORMOSA'],'Patagonia':['NEUQUEN','RIO NEGRO','CHUBUT','SANTA CRUZ','TIERRA DEL FUEGO']}
p2r={p:r for r,ps in REG.items() for p in ps}
def armar(R, ICGJ):
    def ser(f,col):
        d=pd.read_csv(R/f,parse_dates=['indice_tiempo']).set_index('indice_tiempo')[col].dropna()
        d.index=d.index.to_period('M'); return d.groupby(level=0).mean()
    gba=ser('ipc_hist.csv','nivel_general'); sl=ser('ipc_sl.csv','nivel_general'); nac=ser('ipc16.csv','ipc_ng_nacional')
    def splice(a,b,at):
        k=a[at-1]/b[at-1]; return pd.concat([a[a.index<at],b[b.index>=at]*k])
    ipc=splice(gba,sl,pd.Period('2007-01','M')); ipc=splice(ipc,nac,pd.Period('2017-01','M'))
    M=pd.DataFrame({'ipc':ipc})
    M['ripte_real']=ser('ripte.csv','ripte')/M.ipc
    M['jub_min_real']=ser('jubmin.csv','mensual_pesos_corrientes')/M.ipc
    M['auh_real']=ser('auh.csv','auh')/M.ipc
    M['emae']=ser('emae04.csv','emae_desestacionalizada')
    tc=ser('tc.csv','dolar_referencia_com_3500').combine_first(ser('tc.csv','dolar_oficial_venta'))
    M['dolar_real']=tc/M.ipc; M['tc']=tc
    M['expect_infl']=np.nan
    M=M[M.index>=pd.Period('2003-01','M')]
    gob=[('Duhalde','2002-01'),('Kirchner','2003-06'),('CFK 1','2007-12'),('CFK 2','2011-12'),('Macri','2015-12'),('Fernández','2019-12'),('Milei','2023-12')]
    g=pd.Series(index=M.index,dtype=object)
    for n,d in gob: g[M.index>=pd.Period(d,'M')]=n
    M['gob']=g
    return M
def panel(R, ICGJ, M):
    # --- empleo OEDE trimestral por provincia (total) ---
    x=pd.ExcelFile(R/'oede_empleo.xlsx')
    emp={}
    for sh in x.sheet_names[2:-1]:
        e=pd.read_excel(x,sheet_name=sh,header=None)
        hdr=e.iloc[3,2:].tolist(); row=e[e.iloc[:,1].astype(str).str.upper().str.contains('TOTAL')].iloc[0,2:]
        q=[]
        for h in hdr:
            h=str(h); n=int(h[0]); y=int(h[-4:]); q.append(pd.Period(f'{y}-{3*n-1:02d}','M'))
        emp[norm(sh)]=pd.Series(pd.to_numeric(row.values,errors='coerce'),index=q)
    E=pd.DataFrame(emp); E=E.T.groupby(lambda p:p2r[p]).sum(min_count=1).T
    E=E.resample('M').interpolate() if False else E.reindex(pd.period_range(E.index.min(),E.index.max(),freq='M')).interpolate(limit_area='inside')
    # --- salarios OEDE mensual por provincia ---
    s=pd.read_excel(R/'oede_remuneraciones.xlsx',sheet_name='Total',header=None)
    dates=[pd.Period(pd.Timestamp(d),'M') for d in s.iloc[4,1:]]
    W={}
    for i in range(5,30):
        n=norm(s.iloc[i,0])
        if n in p2r: W[n]=pd.Series(pd.to_numeric(s.iloc[i,1:].values,errors='coerce'),index=dates)
    W=pd.DataFrame(W)
    # empleo por provincia para ponderar (trimestral interpolado)
    Ep={}
    for sh in x.sheet_names[2:-1]:
        e=pd.read_excel(x,sheet_name=sh,header=None); hdr=e.iloc[3,2:].tolist(); row=e[e.iloc[:,1].astype(str).str.upper().str.contains('TOTAL')].iloc[0,2:]
        q=[pd.Period(f'{int(str(h)[-4:])}-{3*int(str(h)[0])-1:02d}','M') for h in hdr]
        Ep[norm(sh)]=pd.Series(pd.to_numeric(row.values,errors='coerce'),index=q)
    Ep=pd.DataFrame(Ep).rename(columns={'PARTIDOS DE GBA':'GRAN BUENOS AIRES','CABA':'CAPITAL FEDERAL','RESTO DE BUENOS AIRES':'BUENOS AIRES'})
    Ep=Ep.reindex(pd.period_range(Ep.index.min(),W.index.max(),freq='M')).interpolate(limit_direction='forward')
    Wr={}
    for r,ps in REG.items():
        cols=[p for p in ps if p in W.columns]; ww=Ep.reindex(W.index)[cols]
        Wr[r]=(W[cols]*ww).sum(axis=1,min_count=1)/ww.where(W[cols].notna()).sum(axis=1)
    Wr=pd.DataFrame(Wr)
    # --- IPC regional (desde 2017; antes nacional) ---
    ip=pd.read_csv(R/'ipc16.csv',parse_dates=['indice_tiempo']).set_index('indice_tiempo'); ip.index=ip.index.to_period('M')
    ipr=pd.DataFrame({'AMBA':ip.ipc_ng_gba,'Pampeana':ip.ipc_ng_pampeana,'NEA':ip.ipc_ng_nea,'NOA':ip.ipc_ng_noa,'Cuyo':ip.ipc_ng_cuyo,'Patagonia':ip.ipc_ng_patagonia})
    P=pd.DataFrame({r:M.ipc for r in REG})
    for r in REG:
        k=P.loc[pd.Period('2016-12','M'),r]/ipr.loc[pd.Period('2016-12','M'),r]
        P.loc[P.index>=pd.Period('2017-01','M'),r]=ipr.loc[ipr.index>=pd.Period('2017-01','M'),r].reindex(P.index[P.index>=pd.Period('2017-01','M')]).values*k
    # --- patentamientos ---
    a=pd.read_csv(R/'autos.csv'); a['r']=a.provincia_inscripcion_inicial.map(lambda s:p2r.get(norm(s),'AMBA' if 'BS.AS' in norm(s) else None))
    a.loc[a.provincia_inscripcion_inicial=='Buenos Aires','r']='AMBA'
    a['p']=pd.PeriodIndex.from_fields(year=a.anio_inscripcion_inicial,month=a.mes_inscripcion_inicial,freq='M')
    pat=a.groupby(['p','r']).cantidad_inscripciones_iniciales.sum().unstack().rolling(12).sum()
    # --- ICG regional ---
    I=json.load(open(ICGJ))
    ICG=(pd.DataFrame({pd.Period(k,'M'):{r:v[r][0] for r in REG if r in v} for k,v in I.items()}).T*20).rolling(3).mean()
    rows=[]
    for r in REG:
        d=pd.DataFrame(index=M.index)
        d['icg']=ICG[r]; d['region']=r; d['gob']=M.gob
        d['salario_reg_real']=np.log(Wr[r]/P[r]).diff(12)*100
        d['jub_min_real']=np.log(M.jub_min_real*M.ipc/P[r]).diff(12)*100
        d['auh_real']=np.log(M.auh_real*M.ipc/P[r]).diff(12)*100
        d['ripte_real']=np.log(M.ripte_real).diff(12)*100
        d['expect_infl']=np.log1p(M.expect_infl/100)*100
        d['infl_rel']=(np.log(P[r]/P[r].shift(3))-np.log(M.ipc/M.ipc.shift(3)))*400
        d['dolar_real']=np.log(M.dolar_real).diff(12)*100
        d['patentam']=np.log(pat[r]).diff(12)*100 if r in pat else np.nan
        d['emae']=np.log(M.emae).diff(12)*100
        d['L_ripte_real']=np.log(M.ripte_real); d['L_salario_reg_real']=np.log(Wr[r]/P[r]); d['L_jub_min_real']=np.log(M.jub_min_real*M.ipc/P[r])
        d['L_auh_real']=np.log(M.auh_real*M.ipc/P[r]); d['L_expect_infl']=np.log1p(M.expect_infl/100); d['L_dolar_real']=np.log(M.dolar_real)
        d['L_patentam']=np.log(pat[r]) if r in pat else np.nan; d['L_emae']=np.log(M.emae); d['L_empleo_reg']=np.log(E[r])
        d['L_infl_rel']=np.log(P[r]/P[r].shift(3))-np.log(M.ipc/M.ipc.shift(3))
        d['empleo_reg']=np.log(E[r]).diff(12)*100
        rows.append(d)
    D=pd.concat(rows); D.index.name='mes'; D=D.reset_index()
    D=D[D.mes>=pd.Period('2003-01','M')]
    return D
def proyectar(R, D, M, HOY, REM):
    REGS=['AMBA','Pampeana','Cuyo','NOA','NEA','Patagonia']
    V=['ripte_real','salario_reg_real','jub_min_real','auh_real','infl3','dolar_real','patentam','empleo_reg','il','gasto_real']
    signo={'ripte_real':1,'salario_reg_real':1,'jub_min_real':1,'auh_real':1,'expect_infl':-1,'dolar_real':-1,'patentam':1,'emae':1,'empleo_reg':1,'infl_rel':-1,'infl3':-1,'il':1,'gasto_real':1}
    FIN=pd.Period('2027-10','M'); hist=pd.period_range('2003-01',HOY,freq='M'); todo=pd.period_range('2003-01',FIN,freq='M')
    # --- SIPA mensual por provincia para completar empleo regional (feb-26 -> ago-26) ---
    sp=pd.read_csv(R/'sipa_prov.csv',parse_dates=['indice_tiempo']).set_index('indice_tiempo'); sp.index=sp.index.to_period('M')
    sp.columns=[norm(c.replace('asalariados_priv_sin_estac_','')) for c in sp.columns]
    RP={'AMBA':['BUENOS AIRES','CABA'],'Pampeana':['BUENOS AIRES','CORDOBA','SANTA FE','ENTRE RIOS','LA PAMPA'],'Cuyo':['MENDOZA','SAN JUAN','SAN LUIS'],
     'NOA':['JUJUY','SALTA','TUCUMAN','SANTIAGO ESTERO','CATAMARCA','LA RIOJA'],'NEA':['MISIONES','CORRIENTES','CHACO','FORMOSA'],'Patagonia':['NEUQUEN','RIO NEGRO','CHUBUT','SANTA CRUZ','TIERRA FUEGO']}
    spr={r:np.log(sp[[c for c in ps if c in sp.columns]].sum(axis=1)) for r,ps in RP.items()}
    ip_=pd.read_csv(R/'ipc16.csv',parse_dates=['indice_tiempo']).set_index('indice_tiempo'); ip_.index=ip_.index.to_period('M')
    IPR={'AMBA':ip_.ipc_ng_gba,'Pampeana':ip_.ipc_ng_pampeana,'NEA':ip_.ipc_ng_nea,'NOA':ip_.ipc_ng_noa,'Cuyo':ip_.ipc_ng_cuyo,'Patagonia':ip_.ipc_ng_patagonia}
    il_=pd.read_excel(R/'il.xls',header=0); il_.index=pd.to_datetime(il_.iloc[:,0]).dt.to_period('M'); IL=np.log(il_.iloc[:,1].astype(float))
    g1=pd.read_csv(R/'spn_07-14.csv',parse_dates=['indice_tiempo']).set_index('indice_tiempo')['gtos_primarios_antes_figurativos_2007_2014']
    g2=pd.read_csv(R/'spn_17.csv',parse_dates=['indice_tiempo']).set_index('indice_tiempo')['gtos_primario_antes_figurativos_2017']
    gg=pd.concat([g1,g2]); gg.index=gg.index.to_period('M'); gg=gg.groupby(level=0).last()
    GAS=np.log(gg.rolling(12).sum()/M.ipc.rolling(12).mean())
    H={}
    for r in REGS:
        a=D[D.region==r].set_index('mes').reindex(hist)
        L=pd.DataFrame({c:a['L_'+c] for c in V if c not in('infl3','il','gasto_real')})
        L['il']=IL.reindex(hist); L['gasto_real']=GAS.reindex(hist)
        L['emae']=a['L_emae']
        L['salario_reg_real']=L['salario_reg_real'].rolling(12,min_periods=12).mean()   # sin aguinaldo
        # completar huecos hasta oct-26 (se reasigna cada serie: pandas trabaja con copias)
        s=L['ripte_real'].copy(); s[s.index>s.last_valid_index()]=s[s.last_valid_index()]; L['ripte_real']=s
        s=L['salario_reg_real'].copy(); last=s.last_valid_index()
        for p in pd.period_range(last+1,HOY,freq='M'): s[p]=s[p-1]+(L['ripte_real'][p]-L['ripte_real'][p-1])
        L['salario_reg_real']=s
        for c in ('il','gasto_real'):
            s=L[c].copy(); last=s.last_valid_index(); pend=(s[last]-s[last-24])/24*0.5
            for p in pd.period_range(last+1,HOY,freq='M'): s[p]=s[last]+pend*(p-last).n
            L[c]=s
        s=L['emae'].copy(); last=s.last_valid_index()
        for p in pd.period_range(last+1,HOY,freq='M'): s[p]=s[p-1]-0.003
        L['emae']=s
        s=L['empleo_reg'].copy(); last=s.last_valid_index()
        for p in pd.period_range(last+1,HOY,freq='M'):
            ok=p in spr[r].index and (p-1) in spr[r].index and not np.isnan(spr[r][p]) and not np.isnan(spr[r][p-1])
            s[p]=s[p-1]+(spr[r][p]-spr[r][p-1] if ok else 0)
        L['empleo_reg']=s
        for c in ('jub_min_real','auh_real','dolar_real','patentam'):
            s=L[c].copy(); last=s.last_valid_index()
            if last<HOY: s[s.index>last]=s[last]
            L[c]=s
        pr=M.ipc.reindex(hist).copy(); kk=pr[pd.Period('2016-12','M')]/IPR[r][pd.Period('2016-12','M')]
        f=pr.index>=pd.Period('2017-01','M'); pr[f]=IPR[r].reindex(pr.index[f]).values*kk
        L['infl3']=np.log(pr/pr.shift(3))*4; L['_ipc']=np.log(pr)
        H[r]=L
    # ---------- reglas de proyección ----------
    ipc=M.ipc.reindex(todo)
    fut_all=pd.period_range(HOY+1,FIN,freq='M')
    INFL=pd.Series({p:REM['inflacion'].get(str(p)) for p in fut_all},dtype=float)
    ultimo=[float(v) for k,v in sorted(REM['inflacion'].items())][-1]
    INFL=INFL.ffill().fillna(ultimo)
    for p in INFL.index: ipc[p]=ipc[p-1]*np.exp(INFL[p]/100)
    tci=pd.Series(np.nan,index=pd.period_range(HOY,FIN,freq='M'))
    tci[HOY]=float(M.tc.reindex([HOY]).ffill().iloc[0]) if not np.isnan(M.tc.reindex([HOY]).iloc[0]) else float(M.tc.dropna().iloc[-1])
    for k,v in REM['dolar'].items():
        if pd.Period(k,'M') in tci.index: tci[pd.Period(k,'M')]=float(v)
    last=tci.last_valid_index()
    for p in pd.period_range(last+1,FIN,freq='M'): tci[p]=tci[p-1]*np.exp(INFL[p]/100)
    tci=np.exp(np.log(tci.astype(float)).interpolate())
    act=[float(v) for k,v in sorted(REM['actividad'].items())]
    EMAE_REM={p:float(REM['actividad'].get(str(p),act[-1])) for p in fut_all}
    def reglas(L,t0,t1,usar_rem):
        """proyecta L desde t0 hasta t1 con las reglas de años electorales. usar_rem=True solo para 2027."""
        X=L.copy().reindex(pd.period_range(L.index.min(),t1,freq='M'))
        fut=pd.period_range(t0+1,t1,freq='M')
        for c in ['ripte_real','salario_reg_real']: X.loc[fut,c]=X.loc[t0,c]
        for c in ('il','gasto_real'):
            a0=X.loc[t0-24,c] if (t0-24) in X.index else np.nan
            pend=0.0 if pd.isna(a0) or pd.isna(X.loc[t0,c]) else (X.loc[t0,c]-a0)/24*0.5
            X.loc[fut,c]=[X.loc[t0,c]+pend*(p-t0).n for p in fut]
        for c,k in [('patentam',6),('empleo_reg',12)]:
            pend=(X.loc[t0,c]-X.loc[t0-k,c])/k
            X.loc[fut,c]=[X.loc[t0,c]+pend*(p-t0).n for p in fut]
        if usar_rem:
            # jubilación y AUH: suben con la inflación de 2 meses antes
            for c in ['jub_min_real','auh_real']:
                for p in fut: X.loc[p,c]=X.loc[p-1,c]+np.log(ipc[p-2]/ipc[p-3])-np.log(ipc[p]/ipc[p-1])
            tcn=float(np.exp(X.loc[t0,'dolar_real']))*float(ipc[t0])
            X.loc[fut,'dolar_real']=[np.log(tci[p]/ipc[p]) for p in fut]
            for p in fut: X.loc[p,'emae']=X.loc[p-1,'emae']+EMAE_REM[p]/100
            for p in fut: X.loc[p,'_ipc']=X.loc[p-1,'_ipc']+INFL[p]/100
            X['infl3']=(X['_ipc']-X['_ipc'].shift(3))*4
        else:
            for c in ['jub_min_real','auh_real','dolar_real']: X.loc[fut,c]=X.loc[t0,c]
            X.loc[fut,'emae']=X.loc[t0,'emae']
            X.loc[fut,'infl3']=X.loc[t0,'infl3']
        return X
    def momento(L): return L-L.shift(1).rolling(12).mean()
    # estandarización y coeficiente con la historia
    Zh={r:momento(H[r]) for r in REGS}; allz=pd.concat(Zh.values()); mu=allz.mean(); sd=allz.std()
    def comp(Z): return pd.DataFrame({c:signo[c]*(Z[c]-mu[c])/sd[c] for c in V}).mean(axis=1)
    ini={'Duhalde':'2002-01','Kirchner':'2003-06','CFK 1':'2007-12','CFK 2':'2011-12','Macri':'2015-12','Fernández':'2019-12','Milei':'2023-12'}
    P=D.copy(); P['z']=np.nan
    for r in REGS: P.loc[P.region==r,'z']=P.loc[P.region==r,'mes'].map(comp(Zh[r])).values
    P['lm']=[np.log1p((m-pd.Period(ini[g],'M')).n) for m,g in zip(P.mes,P.gob)]; P['rg']=P.region+'|'+P.gob
    C=pd.get_dummies(P.rg,dtype=float); C=pd.concat([C,C.mul(P.lm,axis=0).add_suffix('_t')],axis=1)
    m=P.icg.notna()&P.z.notna()
    k=np.linalg.lstsq(np.column_stack([C[m].values,P.z[m].values]),P.icg[m].values,rcond=None)[0][-1]
    print(f'coeficiente {k:.2f} puntos de ICG (0-100) por unidad del índice')
    # errores de las reglas en años electorales (trayectoria completa de 12 meses)
    ANIOS=[2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025]
    errores={}
    for y in ANIOS:
        t0=pd.Period(f'{y-1}-10','M'); t1=t0+12; ok=True; E={}
        for r in REGS:
            if t1>HOY: ok=False; break
            pr=reglas(H[r].loc[:t0],t0,t1,False); real=H[r].loc[t0+1:t1]
            E[r]=(real-pr.loc[t0+1:t1]).reset_index(drop=True)   # error por mes 1..12
        if ok: errores[y]=E
    # proyección 2027 por reglas + cada error histórico
    base={r:reglas(H[r],HOY,FIN,True) for r in REGS}
    MESES={'jul':pd.Period('2027-07','M'),'sep':pd.Period('2027-09','M'),'oct':pd.Period('2027-10','M')}
    def dz(rutas):
        return {r:{m:float(comp(momento(rutas[r]))[p]-comp(momento(rutas[r]))[HOY]) for m,p in MESES.items()} for r in REGS}
    dz_base=dz(base)
    dz_hist={}
    for y,E in errores.items():
        rutas={}
        for r in REGS:
            X=base[r].copy(); fut=pd.period_range(HOY+1,FIN,freq='M')
            e=E[r].fillna(0.0); e.index=fut; X.loc[fut,V]=X.loc[fut,V]+e[V]
            rutas[r]=X
        dz_hist[y]=dz(rutas)
    # cambio típico en años de referencia (historia real)
    zn=pd.concat([comp(Zh[r]) for r in REGS],axis=1).mean(axis=1)
    REF={'todos':[2007,2011,2015,2019,2023],'continuidad':[2007,2011,2019]}
    dref={(ref,mm):np.mean([zn[pd.Period(f'{y}-{p.strftime("%m")}','M')]-zn[pd.Period(f'{y-1}-10','M')] for y in ys]) for ref,ys in REF.items() for mm,p in MESES.items()}
    # percentiles entre años: promedio de regiones para ordenar
    orden=sorted(dz_hist,key=lambda y:np.mean([dz_hist[y][r]['sep'] for r in REGS]))
    print('cambio del índice a sep-27 (prom. regiones) según reglas:',round(np.mean([dz_base[r]['sep'] for r in REGS]),2))
    print('con el error de cada año electoral:',{y:round(np.mean([dz_hist[y][r]['sep'] for r in REGS]),2) for y in orden})
    def pct(q):
        return {r:{mm:float(np.percentile([dz_hist[y][r][mm] for y in dz_hist],q)) for mm in MESES} for r in REGS}
    ESC={'pesimista':pct(10),'central':pct(50),'optimista':pct(90),'reglas':dz_base}
    return float(k),{f'{a}|{b}':float(v) for (a,b),v in dref.items()},ESC,orden
    print('dref',{f'{a}|{b}':round(v,2) for (a,b),v in dref.items()})

def main():
    RAIZ=Path(__file__).resolve().parents[2]; R=RAIZ/'fuentes/eco'; ICGJ=RAIZ/'datos/icg_mensual.json'
    REM=json.loads((RAIZ/'datos/rem.json').read_text())
    HOY=pd.Period(list(json.loads(ICGJ.read_text()))[-1],'M')
    M=armar(R,ICGJ); D=panel(R,ICGJ,M)
    k,dref,ESC,orden=proyectar(R,D,M,HOY,REM)
    aj={esc:{r:{m:round(k*(ESC[esc][r][m]-dref['todos|'+m])/20,4) for m in ('jul','sep','oct')} for r in ESC[esc]} for esc in ('pesimista','central','optimista')}
    dest=RAIZ/'datos/economia.json'; prev=json.loads(dest.read_text()) if dest.exists() else {}
    out={'actualizado':date.today().isoformat(),'coeficiente_icg_0_100':round(k,2),'nota':prev.get('nota','Ajuste del ICG regional (escala 0-5) por proyección económica, medido contra el cambio económico típico de los años de referencia.'),
         'datos_hasta':str(HOY),'rem':REM.get('relevamiento'),'ajuste':{f'{e}_todos':v for e,v in aj.items()}}
    if {k_:v for k_,v in prev.items() if k_!='actualizado'}=={k_:v for k_,v in out.items() if k_!='actualizado'}:
        print('Sin cambios en el ajuste económico.'); return
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=1)); print('economia.json actualizado', {e:round(np.mean([aj[e][r]['sep'] for r in aj[e]]),4) for e in aj})

if __name__=='__main__':
    main()
