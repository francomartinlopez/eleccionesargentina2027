/* Elecciones provinciales 2027: datos del efecto sobre LLA. Ver js/provincias.js. Esperado: of (oficial), amb (ambiguo), op (opositor). Efecto: [PASO, general, balotaje] en fracción del máximo. Estado de la fecha: c confirmada, a anunciada, e estimada. Cuando una provincia vota se agrega "real": {"res": "of|amb|op", "ganador": "Nombre (fuerza)", "pct": 45.2, "segundo": "Nombre (fuerza)", "pct2": 30.1, "margen": 15.1, "fecha": "AAAA-MM-DD", "fuente": "escrutinio provisorio|definitivo", "url": "..."}. Buenos Aires: "real": {"res": "pc|pa|sa|sc", "texto": "..."}; Ciudad: "real": {"res": "of|amb|op", "texto": "..."}. */
window.PROV_DATA = {
 "actualizado": "2026-11-19",
 "nacionales": {
  "paso": "2027-08-08",
  "general": "2027-10-24",
  "balotaje": "2027-11-21"
 },
 "padron_total": 36477204,
 "fuente_padron": "CNE, padrón definitivo de las elecciones del 26-10-2025",
 "reglas": {
  "max_con": {
   "P": 1,
   "G": 0.7,
   "B": 0.5
  },
  "max_sin": {
   "G": 1.2,
   "B": 0.5
  },
  "tope_con": {
   "P": 3,
   "G": 2,
   "B": 1.5
  },
  "tope_sin": {
   "G": 2.5,
   "B": 1.5
  },
  "dias_mitad": 92,
  "vuelco": 0.6,
  "racha": 1.5,
  "margen_alto": 10,
  "margen_bajo": 3,
  "f_alto": 1.25,
  "f_bajo": 0.75,
  "icg_posterior": 0.5
 },
 "ba": {
  "esperado": "pa",
  "padron": 13353974,
  "opciones": {
   "pc": {
    "P": -0.6,
    "G": -1.1,
    "B": -0.7
   },
   "pa": {
    "P": -0.3,
    "G": -0.55,
    "B": -0.35
   },
   "sa": {
    "P": 0.3,
    "G": 0.55,
    "B": 0.35
   },
   "sc": {
    "P": 0.6,
    "G": 1.1,
    "B": 0.7
   }
  }
 },
 "caba": {
  "esperado": "amb",
  "padron": 2520249,
  "efecto": {
   "of": 0.2,
   "amb": 0,
   "op": -0.2
  }
 },
 "mismo_dia": [
  "Buenos Aires",
  "Ciudad de Buenos Aires",
  "Catamarca",
  "La Rioja"
 ],
 "no_eligen": [
  "Corrientes",
  "Santiago del Estero"
 ],
 "provincias": [
  {
   "n": "Neuquén",
   "fecha": "2027-02-14",
   "estado": "c",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 609951
  },
  {
   "n": "Río Negro",
   "fecha": "2027-03-21",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 617054
  },
  {
   "n": "La Pampa",
   "fecha": "2027-05-16",
   "estado": "e",
   "esperado": "op",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 304693,
   "paso_prov": "2027-03-14"
  },
  {
   "n": "Misiones",
   "fecha": "2027-05-02",
   "estado": "a",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 994317
  },
  {
   "n": "Tucumán",
   "fecha": "2027-05-09",
   "estado": "c",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 1341563
  },
  {
   "n": "Salta",
   "fecha": "2027-05-16",
   "estado": "a",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 1111029
  },
  {
   "n": "Jujuy",
   "fecha": "2027-05-23",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 602380
  },
  {
   "n": "Tierra del Fuego",
   "fecha": "2027-05-30",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 162527
  },
  {
   "n": "San Juan",
   "fecha": "2027-05-30",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 606278
  },
  {
   "n": "Córdoba",
   "fecha": "2027-06-06",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -1,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 3084000
  },
  {
   "n": "Santa Fe",
   "fecha": "2027-06-13",
   "estado": "a",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0.5
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 2815453,
   "paso_prov": "2027-04-18"
  },
  {
   "n": "Entre Ríos",
   "fecha": "2027-06-13",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1053652,
   "paso_prov": "2027-04-11"
  },
  {
   "n": "San Luis",
   "fecha": "2027-06-13",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 399321
  },
  {
   "n": "Formosa",
   "fecha": "2027-06-27",
   "estado": "e",
   "esperado": "op",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 491565
  },
  {
   "n": "Chubut",
   "fecha": "2027-07-25",
   "estado": "a",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 453021
  },
  {
   "n": "Santa Cruz",
   "fecha": "2027-08-08",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 288732
  },
  {
   "n": "Chaco",
   "fecha": "2027-09-19",
   "estado": "a",
   "esperado": "of",
   "efecto": {
    "of": [
     0.5,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -1,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1015693,
   "paso_prov": "2027-06-27",
   "senal_paso": "2027-06-27"
  },
  {
   "n": "Mendoza",
   "fecha": "2027-09-26",
   "estado": "a",
   "esperado": "of",
   "efecto": {
    "of": [
     0.5,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -1,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1525824,
   "paso_prov": "2027-07-04",
   "senal_paso": "2027-07-04"
  }
 ]
};
