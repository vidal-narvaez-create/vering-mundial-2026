"""
patch_emparejamiento.py
Ejecutar en la raiz del repo: python3 patch_emparejamiento.py
Lee template.html, agrega la pestana Emparejamiento (cuadro eliminatorio
Mundial 2026, dieciseisavos a la final) y guarda.

Logica oficial FIFA: 16 reglas fijas para los partidos 73-88 del Round of 32,
mas tabla Annex C con las 495 combinaciones posibles de los 8 grupos que
aportan el mejor tercer puesto. Una vez termina la fase de grupos, el sistema
identifica que 8 grupos clasificaron en 3er lugar y arma el cruce real.
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado. Ejecuta desde la raiz del repo.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# CSS
CSS = """
/* EMPAREJAMIENTO */
.emp-body{padding:20px;max-width:1300px;margin:0 auto;background:#F4F5F9}
.emp-header{background:#0B369D;border-bottom:3px solid #E53935;border-radius:10px 10px 0 0;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.emp-header-title{color:#fff;font-weight:900;font-size:14px;letter-spacing:0.5px}
.emp-header-sub{color:#B9C6E8;font-size:10px}
.emp-badge-live{color:#fff;font-size:11px;background:rgba(255,255,255,.15);padding:4px 10px;border-radius:20px;display:flex;align-items:center;gap:5px}
.emp-titlebar{background:#fff;padding:14px 18px;border-bottom:1px solid #E5E7EE}
.emp-titlebar h2{color:#0a1f6e;font-size:17px;font-weight:900;margin-bottom:2px}
.emp-titlebar p{color:#6B7491;font-size:12px}
.emp-canvas{background:#F4F5F9;border-radius:0 0 10px 10px;padding:18px;overflow-x:auto}
.emp-match{background:#fff;border:1px solid #DCE0EC;border-radius:6px;padding:8px 10px;margin-bottom:7px;min-width:148px}
.emp-match.tbd{background:#F0F4FF;border:1px dashed #C7D2F0}
.emp-match.py{background:#FFF6F5;border:1.5px solid #E53935}
.emp-team-row{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:700;color:#1a2b5c;padding:2px 0}
.emp-team-row.tbd-text{color:#5E6FA8;font-weight:700;font-size:10px}
.emp-match-meta{font-size:9px;color:#A6ACC4;margin-top:3px}
.emp-stage-label{font-size:10px;font-weight:900;color:#0B369D;letter-spacing:1px;margin-bottom:8px}
.emp-legend{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:14px;flex-wrap:wrap}
.emp-legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:#6B7491}
.emp-legend-dot{width:10px;height:10px;border-radius:2px;display:inline-block}
.emp-final-box{background:#0B369D;border-radius:8px;padding:14px;color:#fff;text-align:center}
.emp-final-box .lbl{font-size:11px;font-weight:900;letter-spacing:1px;margin-bottom:6px}
.emp-final-box .team{font-size:13px;font-weight:700;margin:2px 0}
.emp-bracket-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;min-width:1100px}
@media(max-width:700px){.emp-body{padding:10px}.emp-canvas{padding:10px}}
"""

if '/* EMPAREJAMIENTO */' in html:
    print("CSS emparejamiento ya existe, saltando.")
else:
    html = html.replace('</style>', CSS + '</style>', 1)
    print("CSS emparejamiento agregado OK")

# NAV TAB - insertar entre Predicciones y Mi Equipo
nav_patched = False
nav_variants = [
    ("onclick=\"showPage('miequipo',this)\">⭐ Mi Equipo</button>",
     "onclick=\"showPage('emparejamiento',this)\">🗺 Emparejamiento</button>\n      <button class=\"nav-tab\" onclick=\"showPage('miequipo',this)\">⭐ Mi Equipo</button>"),
]
for old, new in nav_variants:
    if old in html:
        html = html.replace(old, new, 1)
        nav_patched = True
        print("Nav tab Emparejamiento agregado OK")
        break

if not nav_patched:
    m = re.search(r"onclick=\"showPage\('miequipo',this\)\">.*?Mi Equipo</button>", html)
    if m:
        old_text = m.group(0)
        new_text = "onclick=\"showPage('emparejamiento',this)\">&#x1F5FA; Emparejamiento</button>\n      <button class=\"nav-tab\" " + old_text
        html = html.replace(old_text, new_text, 1)
        nav_patched = True
        print("Nav tab Emparejamiento agregado OK (regex)")
    else:
        print("WARNING: Nav tab Mi Equipo no encontrado, no se pudo insertar Emparejamiento")

# PAGE HTML
EMP_PAGE = """
  <!-- EMPAREJAMIENTO -->
  <div id="page-emparejamiento" class="page">
    <div class="emp-body">
      <div class="emp-header">
        <div>
          <div class="emp-header-title">VERING &middot; CUADRO ELIMINATORIO</div>
          <div class="emp-header-sub">Mundial 2026 &middot; Dieciseisavos a la Final</div>
        </div>
        <div class="emp-badge-live">&#x1F7E2; Auto-actualizado</div>
      </div>
      <div class="emp-titlebar">
        <h2>Cuadro eliminatorio</h2>
        <p id="empSubtitle">Se completa solo segun resultados de la fase de grupos</p>
      </div>
      <div class="emp-canvas">
        <div id="empBracketContainer"></div>
        <div class="emp-legend">
          <div class="emp-legend-item"><span class="emp-legend-dot" style="background:#fff;border:1px solid #DCE0EC"></span>Confirmado</div>
          <div class="emp-legend-item"><span class="emp-legend-dot" style="background:#F0F4FF;border:1px dashed #C7D2F0"></span>Por definir</div>
          <div class="emp-legend-item"><span class="emp-legend-dot" style="background:#FFF6F5;border:1px solid #E53935"></span>Paraguay</div>
        </div>
      </div>
    </div>
  </div>

"""

if 'id="page-emparejamiento"' in html:
    print("Page emparejamiento ya existe, saltando.")
else:
    m = re.search(r'(\s*<!-- ALERTAS -->)', html)
    if m:
        html = html[:m.start()] + EMP_PAGE + html[m.start():]
        print("Page emparejamiento agregado OK")
    else:
        m2 = re.search(r'(\s*<!-- CAMPEONES -->)', html)
        if m2:
            html = html[:m2.start()] + EMP_PAGE + html[m2.start():]
            print("Page emparejamiento agregado OK (antes de Campeones)")
        else:
            print("WARNING: punto de insercion no encontrado para Emparejamiento")

# JS - logica completa del bracket FIFA 2026
EMP_JS = """
// ============================================================
// EMPAREJAMIENTO - CUADRO ELIMINATORIO MUNDIAL 2026
// Logica oficial FIFA: Round of 32 (partidos 73-88) + Annex C (495 combos)
// ============================================================

// Las 16 reglas fijas del Round of 32 (partidos 73 a 88)
const R32_FIXED_RULES = [
  {m:73, a:{type:'RU',g:'A'}, b:{type:'RU',g:'B'}, date:'28/06'},
  {m:74, a:{type:'W',g:'E'},  b:{type:'3RD',slot:74}, date:'29/06'},
  {m:75, a:{type:'W',g:'F'},  b:{type:'RU',g:'C'}, date:'29/06'},
  {m:76, a:{type:'W',g:'C'},  b:{type:'RU',g:'F'}, date:'29/06'},
  {m:77, a:{type:'W',g:'I'},  b:{type:'3RD',slot:77}, date:'30/06'},
  {m:78, a:{type:'RU',g:'E'}, b:{type:'RU',g:'I'}, date:'30/06'},
  {m:79, a:{type:'W',g:'A'},  b:{type:'3RD',slot:79}, date:'30/06'},
  {m:80, a:{type:'W',g:'L'},  b:{type:'3RD',slot:80}, date:'01/07'},
  {m:81, a:{type:'W',g:'D'},  b:{type:'3RD',slot:81}, date:'01/07'},
  {m:82, a:{type:'W',g:'G'},  b:{type:'3RD',slot:82}, date:'01/07'},
  {m:83, a:{type:'RU',g:'K'}, b:{type:'RU',g:'L'}, date:'01/07'},
  {m:84, a:{type:'W',g:'H'},  b:{type:'RU',g:'J'}, date:'02/07'},
  {m:85, a:{type:'W',g:'B'},  b:{type:'3RD',slot:85}, date:'02/07'},
  {m:86, a:{type:'W',g:'J'},  b:{type:'RU',g:'H'}, date:'02/07'},
  {m:87, a:{type:'W',g:'K'},  b:{type:'3RD',slot:87}, date:'03/07'},
  {m:88, a:{type:'RU',g:'D'}, b:{type:'RU',g:'G'}, date:'03/07'}
];

// Estructura fija de octavos a la final (numero de partido, de que match sale cada lado)
const R16_RULES = [
  {m:89, srcA:74, srcB:77, date:'04/07'},
  {m:90, srcA:73, srcB:75, date:'04/07'},
  {m:91, srcA:76, srcB:78, date:'05/07'},
  {m:92, srcA:79, srcB:80, date:'05/07'},
  {m:93, srcA:83, srcB:84, date:'06/07'},
  {m:94, srcA:81, srcB:82, date:'06/07'},
  {m:95, srcA:86, srcB:88, date:'07/07'},
  {m:96, srcA:85, srcB:87, date:'07/07'}
];
const QF_RULES = [
  {m:97, srcA:89, srcB:90, date:'09/07'},
  {m:98, srcA:93, srcB:94, date:'10/07'},
  {m:99, srcA:91, srcB:92, date:'10/07'},
  {m:100,srcA:95, srcB:96, date:'11/07'}
];
const SF_RULES = [
  {m:101, srcA:97, srcB:98, date:'14/07'},
  {m:102, srcA:99, srcB:100, date:'15/07'}
];
const THIRD_PLACE_RULE = {m:103, loserA:101, loserB:102, date:'18/07'};
const FINAL_RULE = {m:104, srcA:101, srcB:102, date:'19/07'};

// Las 495 combinaciones oficiales (Annex C). Formato: [numero, "8 letras de grupo", "partidoGrupo,..."]
const THIRD_PLACE_COMBOS = [
[1,"EFGHIJKL","79E,85J,81I,74F,82H,77G,87L,80K"],
[2,"DFGHIJKL","79H,85G,81I,74D,82J,77F,87L,80K"],
[3,"DEGHIJKL","79E,85J,81I,74D,82H,77G,87L,80K"],
[4,"DEFHIJKL","79E,85J,81I,74D,82H,77F,87L,80K"],
[5,"DEFGIJKL","79E,85G,81I,74D,82J,77F,87L,80K"],
[6,"DEFGHJKL","79E,85G,81J,74D,82H,77F,87L,80K"],
[7,"DEFGHIKL","79E,85G,81I,74D,82H,77F,87L,80K"],
[8,"DEFGHIJL","79E,85G,81J,74D,82H,77F,87L,80I"],
[9,"DEFGHIJK","79E,85G,81J,74D,82H,77F,87I,80K"],
[10,"CFGHIJKL","79H,85G,81I,74C,82J,77F,87L,80K"],
[11,"CEGHIJKL","79E,85J,81I,74C,82H,77G,87L,80K"],
[12,"CEFHIJKL","79E,85J,81I,74C,82H,77F,87L,80K"],
[13,"CEFGIJKL","79E,85G,81I,74C,82J,77F,87L,80K"],
[14,"CEFGHJKL","79E,85G,81J,74C,82H,77F,87L,80K"],
[15,"CEFGHIKL","79E,85G,81I,74C,82H,77F,87L,80K"],
[16,"CEFGHIJL","79E,85G,81J,74C,82H,77F,87L,80I"],
[17,"CEFGHIJK","79E,85G,81J,74C,82H,77F,87I,80K"],
[18,"CDGHIJKL","79H,85G,81I,74C,82J,77D,87L,80K"],
[19,"CDFHIJKL","79C,85J,81I,74D,82H,77F,87L,80K"],
[20,"CDFGIJKL","79C,85G,81I,74D,82J,77F,87L,80K"],
[21,"CDFGHJKL","79C,85G,81J,74D,82H,77F,87L,80K"],
[22,"CDFGHIKL","79C,85G,81I,74D,82H,77F,87L,80K"],
[23,"CDFGHIJL","79C,85G,81J,74D,82H,77F,87L,80I"],
[24,"CDFGHIJK","79C,85G,81J,74D,82H,77F,87I,80K"],
[25,"CDEHIJKL","79E,85J,81I,74C,82H,77D,87L,80K"],
[26,"CDEGIJKL","79E,85G,81I,74C,82J,77D,87L,80K"],
[27,"CDEGHJKL","79E,85G,81J,74C,82H,77D,87L,80K"],
[28,"CDEGHIKL","79E,85G,81I,74C,82H,77D,87L,80K"],
[29,"CDEGHIJL","79E,85G,81J,74C,82H,77D,87L,80I"],
[30,"CDEGHIJK","79E,85G,81J,74C,82H,77D,87I,80K"],
[31,"CDEFIJKL","79C,85J,81E,74D,82I,77F,87L,80K"],
[32,"CDEFHJKL","79C,85J,81E,74D,82H,77F,87L,80K"],
[33,"CDEFHIKL","79C,85E,81I,74D,82H,77F,87L,80K"],
[34,"CDEFHIJL","79C,85J,81E,74D,82H,77F,87L,80I"],
[35,"CDEFHIJK","79C,85J,81E,74D,82H,77F,87I,80K"],
[36,"CDEFGJKL","79C,85G,81E,74D,82J,77F,87L,80K"],
[37,"CDEFGIKL","79C,85G,81E,74D,82I,77F,87L,80K"],
[38,"CDEFGIJL","79C,85G,81E,74D,82J,77F,87L,80I"],
[39,"CDEFGIJK","79C,85G,81E,74D,82J,77F,87I,80K"],
[40,"CDEFGHKL","79C,85G,81E,74D,82H,77F,87L,80K"],
[41,"CDEFGHJL","79C,85G,81J,74D,82H,77F,87L,80E"],
[42,"CDEFGHJK","79C,85G,81J,74D,82H,77F,87E,80K"],
[43,"CDEFGHIL","79C,85G,81E,74D,82H,77F,87L,80I"],
[44,"CDEFGHIK","79C,85G,81E,74D,82H,77F,87I,80K"],
[45,"CDEFGHIJ","79C,85G,81J,74D,82H,77F,87E,80I"],
[46,"BFGHIJKL","79H,85J,81B,74F,82I,77G,87L,80K"],
[47,"BEGHIJKL","79E,85J,81I,74B,82H,77G,87L,80K"],
[48,"BEFHIJKL","79E,85J,81B,74F,82I,77H,87L,80K"],
[49,"BEFGIJKL","79E,85J,81B,74F,82I,77G,87L,80K"],
[50,"BEFGHJKL","79E,85J,81B,74F,82H,77G,87L,80K"],
[51,"BEFGHIKL","79E,85G,81B,74F,82I,77H,87L,80K"],
[52,"BEFGHIJL","79E,85J,81B,74F,82H,77G,87L,80I"],
[53,"BEFGHIJK","79E,85J,81B,74F,82H,77G,87I,80K"],
[54,"BDGHIJKL","79H,85J,81B,74D,82I,77G,87L,80K"],
[55,"BDFHIJKL","79H,85J,81B,74D,82I,77F,87L,80K"],
[56,"BDFGIJKL","79I,85G,81B,74D,82J,77F,87L,80K"],
[57,"BDFGHJKL","79H,85G,81B,74D,82J,77F,87L,80K"],
[58,"BDFGHIKL","79H,85G,81B,74D,82I,77F,87L,80K"],
[59,"BDFGHIJL","79H,85G,81B,74D,82J,77F,87L,80I"],
[60,"BDFGHIJK","79H,85G,81B,74D,82J,77F,87I,80K"],
[61,"BDEHIJKL","79E,85J,81B,74D,82I,77H,87L,80K"],
[62,"BDEGIJKL","79E,85J,81B,74D,82I,77G,87L,80K"],
[63,"BDEGHJKL","79E,85J,81B,74D,82H,77G,87L,80K"],
[64,"BDEGHIKL","79E,85G,81B,74D,82I,77H,87L,80K"],
[65,"BDEGHIJL","79E,85J,81B,74D,82H,77G,87L,80I"],
[66,"BDEGHIJK","79E,85J,81B,74D,82H,77G,87I,80K"],
[67,"BDEFIJKL","79E,85J,81B,74D,82I,77F,87L,80K"],
[68,"BDEFHJKL","79E,85J,81B,74D,82H,77F,87L,80K"],
[69,"BDEFHIKL","79E,85I,81B,74D,82H,77F,87L,80K"],
[70,"BDEFHIJL","79E,85J,81B,74D,82H,77F,87L,80I"],
[71,"BDEFHIJK","79E,85J,81B,74D,82H,77F,87I,80K"],
[72,"BDEFGJKL","79E,85G,81B,74D,82J,77F,87L,80K"],
[73,"BDEFGIKL","79E,85G,81B,74D,82I,77F,87L,80K"],
[74,"BDEFGIJL","79E,85G,81B,74D,82J,77F,87L,80I"],
[75,"BDEFGIJK","79E,85G,81B,74D,82J,77F,87I,80K"],
[76,"BDEFGHKL","79E,85G,81B,74D,82H,77F,87L,80K"],
[77,"BDEFGHJL","79H,85G,81B,74D,82J,77F,87L,80E"],
[78,"BDEFGHJK","79H,85G,81B,74D,82J,77F,87E,80K"],
[79,"BDEFGHIL","79E,85G,81B,74D,82H,77F,87L,80I"],
[80,"BDEFGHIK","79E,85G,81B,74D,82H,77F,87I,80K"],
[81,"BDEFGHIJ","79H,85G,81B,74D,82J,77F,87E,80I"],
[82,"BCGHIJKL","79H,85J,81B,74C,82I,77G,87L,80K"],
[83,"BCFHIJKL","79H,85J,81B,74C,82I,77F,87L,80K"],
[84,"BCFGIJKL","79I,85G,81B,74C,82J,77F,87L,80K"],
[85,"BCFGHJKL","79H,85G,81B,74C,82J,77F,87L,80K"],
[86,"BCFGHIKL","79H,85G,81B,74C,82I,77F,87L,80K"],
[87,"BCFGHIJL","79H,85G,81B,74C,82J,77F,87L,80I"],
[88,"BCFGHIJK","79H,85G,81B,74C,82J,77F,87I,80K"],
[89,"BCEHIJKL","79E,85J,81B,74C,82I,77H,87L,80K"],
[90,"BCEGIJKL","79E,85J,81B,74C,82I,77G,87L,80K"],
[91,"BCEGHJKL","79E,85J,81B,74C,82H,77G,87L,80K"],
[92,"BCEGHIKL","79E,85G,81B,74C,82I,77H,87L,80K"],
[93,"BCEGHIJL","79E,85J,81B,74C,82H,77G,87L,80I"],
[94,"BCEGHIJK","79E,85J,81B,74C,82H,77G,87I,80K"],
[95,"BCEFIJKL","79E,85J,81B,74C,82I,77F,87L,80K"],
[96,"BCEFHJKL","79E,85J,81B,74C,82H,77F,87L,80K"],
[97,"BCEFHIKL","79E,85I,81B,74C,82H,77F,87L,80K"],
[98,"BCEFHIJL","79E,85J,81B,74C,82H,77F,87L,80I"],
[99,"BCEFHIJK","79E,85J,81B,74C,82H,77F,87I,80K"],
[100,"BCEFGJKL","79E,85G,81B,74C,82J,77F,87L,80K"],
[101,"BCEFGIKL","79E,85G,81B,74C,82I,77F,87L,80K"],
[102,"BCEFGIJL","79E,85G,81B,74C,82J,77F,87L,80I"],
[103,"BCEFGIJK","79E,85G,81B,74C,82J,77F,87I,80K"],
[104,"BCEFGHKL","79E,85G,81B,74C,82H,77F,87L,80K"],
[105,"BCEFGHJL","79H,85G,81B,74C,82J,77F,87L,80E"],
[106,"BCEFGHJK","79H,85G,81B,74C,82J,77F,87E,80K"],
[107,"BCEFGHIL","79E,85G,81B,74C,82H,77F,87L,80I"],
[108,"BCEFGHIK","79E,85G,81B,74C,82H,77F,87I,80K"],
[109,"BCEFGHIJ","79H,85G,81B,74C,82J,77F,87E,80I"],
[110,"BCDHIJKL","79H,85J,81B,74C,82I,77D,87L,80K"],
[111,"BCDGIJKL","79I,85G,81B,74C,82J,77D,87L,80K"],
[112,"BCDGHJKL","79H,85G,81B,74C,82J,77D,87L,80K"],
[113,"BCDGHIKL","79H,85G,81B,74C,82I,77D,87L,80K"],
[114,"BCDGHIJL","79H,85G,81B,74C,82J,77D,87L,80I"],
[115,"BCDGHIJK","79H,85G,81B,74C,82J,77D,87I,80K"],
[116,"BCDFIJKL","79C,85J,81B,74D,82I,77F,87L,80K"],
[117,"BCDFHJKL","79C,85J,81B,74D,82H,77F,87L,80K"],
[118,"BCDFHIKL","79C,85I,81B,74D,82H,77F,87L,80K"],
[119,"BCDFHIJL","79C,85J,81B,74D,82H,77F,87L,80I"],
[120,"BCDFHIJK","79C,85J,81B,74D,82H,77F,87I,80K"],
[121,"BCDFGJKL","79C,85G,81B,74D,82J,77F,87L,80K"],
[122,"BCDFGIKL","79C,85G,81B,74D,82I,77F,87L,80K"],
[123,"BCDFGIJL","79C,85G,81B,74D,82J,77F,87L,80I"],
[124,"BCDFGIJK","79C,85G,81B,74D,82J,77F,87I,80K"],
[125,"BCDFGHKL","79C,85G,81B,74D,82H,77F,87L,80K"],
[126,"BCDFGHJL","79C,85G,81B,74D,82H,77F,87L,80J"],
[127,"BCDFGHJK","79H,85G,81B,74C,82J,77F,87D,80K"],
[128,"BCDFGHIL","79C,85G,81B,74D,82H,77F,87L,80I"],
[129,"BCDFGHIK","79C,85G,81B,74D,82H,77F,87I,80K"],
[130,"BCDFGHIJ","79H,85G,81B,74C,82J,77F,87D,80I"],
[131,"BCDEIJKL","79E,85J,81B,74C,82I,77D,87L,80K"],
[132,"BCDEHJKL","79E,85J,81B,74C,82H,77D,87L,80K"],
[133,"BCDEHIKL","79E,85I,81B,74C,82H,77D,87L,80K"],
[134,"BCDEHIJL","79E,85J,81B,74C,82H,77D,87L,80I"],
[135,"BCDEHIJK","79E,85J,81B,74C,82H,77D,87I,80K"],
[136,"BCDEGJKL","79E,85G,81B,74C,82J,77D,87L,80K"],
[137,"BCDEGIKL","79E,85G,81B,74C,82I,77D,87L,80K"],
[138,"BCDEGIJL","79E,85G,81B,74C,82J,77D,87L,80I"],
[139,"BCDEGIJK","79E,85G,81B,74C,82J,77D,87I,80K"],
[140,"BCDEGHKL","79E,85G,81B,74C,82H,77D,87L,80K"],
[141,"BCDEGHJL","79H,85G,81B,74C,82J,77D,87L,80E"],
[142,"BCDEGHJK","79H,85G,81B,74C,82J,77D,87E,80K"],
[143,"BCDEGHIL","79E,85G,81B,74C,82H,77D,87L,80I"],
[144,"BCDEGHIK","79E,85G,81B,74C,82H,77D,87I,80K"],
[145,"BCDEGHIJ","79H,85G,81B,74C,82J,77D,87E,80I"],
[146,"BCDEFJKL","79C,85J,81B,74D,82E,77F,87L,80K"],
[147,"BCDEFIKL","79C,85E,81B,74D,82I,77F,87L,80K"],
[148,"BCDEFIJL","79C,85J,81B,74D,82E,77F,87L,80I"],
[149,"BCDEFIJK","79C,85J,81B,74D,82E,77F,87I,80K"],
[150,"BCDEFHKL","79C,85E,81B,74D,82H,77F,87L,80K"],
[151,"BCDEFHJL","79C,85J,81B,74D,82H,77F,87L,80E"],
[152,"BCDEFHJK","79C,85J,81B,74D,82H,77F,87E,80K"],
[153,"BCDEFHIL","79C,85E,81B,74D,82H,77F,87L,80I"],
[154,"BCDEFHIK","79C,85E,81B,74D,82H,77F,87I,80K"],
[155,"BCDEFHIJ","79C,85J,81B,74D,82H,77F,87E,80I"],
[156,"BCDEFGKL","79C,85G,81B,74D,82E,77F,87L,80K"],
[157,"BCDEFGJL","79C,85G,81B,74D,82J,77F,87L,80E"],
[158,"BCDEFGJK","79C,85G,81B,74D,82J,77F,87E,80K"],
[159,"BCDEFGIL","79C,85G,81B,74D,82E,77F,87L,80I"],
[160,"BCDEFGIK","79C,85G,81B,74D,82E,77F,87I,80K"],
[161,"BCDEFGIJ","79C,85G,81B,74D,82J,77F,87E,80I"],
[162,"BCDEFGHL","79C,85G,81B,74D,82H,77F,87L,80E"],
[163,"BCDEFGHK","79C,85G,81B,74D,82H,77F,87E,80K"],
[164,"BCDEFGHJ","79H,85G,81B,74C,82J,77F,87D,80E"],
[165,"BCDEFGHI","79C,85G,81B,74D,82H,77F,87E,80I"],
[166,"AFGHIJKL","79H,85J,81I,74F,82A,77G,87L,80K"],
[167,"AEGHIJKL","79E,85J,81I,74A,82H,77G,87L,80K"],
[168,"AEFHIJKL","79E,85J,81I,74F,82A,77H,87L,80K"],
[169,"AEFGIJKL","79E,85J,81I,74F,82A,77G,87L,80K"],
[170,"AEFGHJKL","79E,85G,81J,74F,82A,77H,87L,80K"],
[171,"AEFGHIKL","79E,85G,81I,74F,82A,77H,87L,80K"],
[172,"AEFGHIJL","79E,85G,81J,74F,82A,77H,87L,80I"],
[173,"AEFGHIJK","79E,85G,81J,74F,82A,77H,87I,80K"],
[174,"ADGHIJKL","79H,85J,81I,74D,82A,77G,87L,80K"],
[175,"ADFHIJKL","79H,85J,81I,74D,82A,77F,87L,80K"],
[176,"ADFGIJKL","79I,85G,81J,74D,82A,77F,87L,80K"],
[177,"ADFGHJKL","79H,85G,81J,74D,82A,77F,87L,80K"],
[178,"ADFGHIKL","79H,85G,81I,74D,82A,77F,87L,80K"],
[179,"ADFGHIJL","79H,85G,81J,74D,82A,77F,87L,80I"],
[180,"ADFGHIJK","79H,85G,81J,74D,82A,77F,87I,80K"],
[181,"ADEHIJKL","79E,85J,81I,74D,82A,77H,87L,80K"],
[182,"ADEGIJKL","79E,85J,81I,74D,82A,77G,87L,80K"],
[183,"ADEGHJKL","79E,85G,81J,74D,82A,77H,87L,80K"],
[184,"ADEGHIKL","79E,85G,81I,74D,82A,77H,87L,80K"],
[185,"ADEGHIJL","79E,85G,81J,74D,82A,77H,87L,80I"],
[186,"ADEGHIJK","79E,85G,81J,74D,82A,77H,87I,80K"],
[187,"ADEFIJKL","79E,85J,81I,74D,82A,77F,87L,80K"],
[188,"ADEFHJKL","79H,85J,81E,74D,82A,77F,87L,80K"],
[189,"ADEFHIKL","79H,85E,81I,74D,82A,77F,87L,80K"],
[190,"ADEFHIJL","79H,85J,81E,74D,82A,77F,87L,80I"],
[191,"ADEFHIJK","79H,85J,81E,74D,82A,77F,87I,80K"],
[192,"ADEFGJKL","79E,85G,81J,74D,82A,77F,87L,80K"],
[193,"ADEFGIKL","79E,85G,81I,74D,82A,77F,87L,80K"],
[194,"ADEFGIJL","79E,85G,81J,74D,82A,77F,87L,80I"],
[195,"ADEFGIJK","79E,85G,81J,74D,82A,77F,87I,80K"],
[196,"ADEFGHKL","79H,85G,81E,74D,82A,77F,87L,80K"],
[197,"ADEFGHJL","79H,85G,81J,74D,82A,77F,87L,80E"],
[198,"ADEFGHJK","79H,85G,81J,74D,82A,77F,87E,80K"],
[199,"ADEFGHIL","79H,85G,81E,74D,82A,77F,87L,80I"],
[200,"ADEFGHIK","79H,85G,81E,74D,82A,77F,87I,80K"],
[201,"ADEFGHIJ","79H,85G,81J,74D,82A,77F,87E,80I"],
[202,"ACGHIJKL","79H,85J,81I,74C,82A,77G,87L,80K"],
[203,"ACFHIJKL","79H,85J,81I,74C,82A,77F,87L,80K"],
[204,"ACFGIJKL","79I,85G,81J,74C,82A,77F,87L,80K"],
[205,"ACFGHJKL","79H,85G,81J,74C,82A,77F,87L,80K"],
[206,"ACFGHIKL","79H,85G,81I,74C,82A,77F,87L,80K"],
[207,"ACFGHIJL","79H,85G,81J,74C,82A,77F,87L,80I"],
[208,"ACFGHIJK","79H,85G,81J,74C,82A,77F,87I,80K"],
[209,"ACEHIJKL","79E,85J,81I,74C,82A,77H,87L,80K"],
[210,"ACEGIJKL","79E,85J,81I,74C,82A,77G,87L,80K"],
[211,"ACEGHJKL","79E,85G,81J,74C,82A,77H,87L,80K"],
[212,"ACEGHIKL","79E,85G,81I,74C,82A,77H,87L,80K"],
[213,"ACEGHIJL","79E,85G,81J,74C,82A,77H,87L,80I"],
[214,"ACEGHIJK","79E,85G,81J,74C,82A,77H,87I,80K"],
[215,"ACEFIJKL","79E,85J,81I,74C,82A,77F,87L,80K"],
[216,"ACEFHJKL","79H,85J,81E,74C,82A,77F,87L,80K"],
[217,"ACEFHIKL","79H,85E,81I,74C,82A,77F,87L,80K"],
[218,"ACEFHIJL","79H,85J,81E,74C,82A,77F,87L,80I"],
[219,"ACEFHIJK","79H,85J,81E,74C,82A,77F,87I,80K"],
[220,"ACEFGJKL","79E,85G,81J,74C,82A,77F,87L,80K"],
[221,"ACEFGIKL","79E,85G,81I,74C,82A,77F,87L,80K"],
[222,"ACEFGIJL","79E,85G,81J,74C,82A,77F,87L,80I"],
[223,"ACEFGIJK","79E,85G,81J,74C,82A,77F,87I,80K"],
[224,"ACEFGHKL","79H,85G,81E,74C,82A,77F,87L,80K"],
[225,"ACEFGHJL","79H,85G,81J,74C,82A,77F,87L,80E"],
[226,"ACEFGHJK","79H,85G,81J,74C,82A,77F,87E,80K"],
[227,"ACEFGHIL","79H,85G,81E,74C,82A,77F,87L,80I"],
[228,"ACEFGHIK","79H,85G,81E,74C,82A,77F,87I,80K"],
[229,"ACEFGHIJ","79H,85G,81J,74C,82A,77F,87E,80I"],
[230,"ACDHIJKL","79H,85J,81I,74C,82A,77D,87L,80K"],
[231,"ACDGIJKL","79I,85G,81J,74C,82A,77D,87L,80K"],
[232,"ACDGHJKL","79H,85G,81J,74C,82A,77D,87L,80K"],
[233,"ACDGHIKL","79H,85G,81I,74C,82A,77D,87L,80K"],
[234,"ACDGHIJL","79H,85G,81J,74C,82A,77D,87L,80I"],
[235,"ACDGHIJK","79H,85G,81J,74C,82A,77D,87I,80K"],
[236,"ACDFIJKL","79C,85J,81I,74D,82A,77F,87L,80K"],
[237,"ACDFHJKL","79H,85J,81F,74C,82A,77D,87L,80K"],
[238,"ACDFHIKL","79H,85F,81I,74C,82A,77D,87L,80K"],
[239,"ACDFHIJL","79H,85J,81F,74C,82A,77D,87L,80I"],
[240,"ACDFHIJK","79H,85J,81F,74C,82A,77D,87I,80K"],
[241,"ACDFGJKL","79C,85G,81J,74D,82A,77F,87L,80K"],
[242,"ACDFGIKL","79C,85G,81I,74D,82A,77F,87L,80K"],
[243,"ACDFGIJL","79C,85G,81J,74D,82A,77F,87L,80I"],
[244,"ACDFGIJK","79C,85G,81J,74D,82A,77F,87I,80K"],
[245,"ACDFGHKL","79H,85G,81F,74C,82A,77D,87L,80K"],
[246,"ACDFGHJL","79C,85G,81J,74D,82A,77F,87L,80H"],
[247,"ACDFGHJK","79H,85G,81J,74C,82A,77F,87D,80K"],
[248,"ACDFGHIL","79H,85G,81F,74C,82A,77D,87L,80I"],
[249,"ACDFGHIK","79H,85G,81F,74C,82A,77D,87I,80K"],
[250,"ACDFGHIJ","79H,85G,81J,74C,82A,77F,87D,80I"],
[251,"ACDEIJKL","79E,85J,81I,74C,82A,77D,87L,80K"],
[252,"ACDEHJKL","79H,85J,81E,74C,82A,77D,87L,80K"],
[253,"ACDEHIKL","79H,85E,81I,74C,82A,77D,87L,80K"],
[254,"ACDEHIJL","79H,85J,81E,74C,82A,77D,87L,80I"],
[255,"ACDEHIJK","79H,85J,81E,74C,82A,77D,87I,80K"],
[256,"ACDEGJKL","79E,85G,81J,74C,82A,77D,87L,80K"],
[257,"ACDEGIKL","79E,85G,81I,74C,82A,77D,87L,80K"],
[258,"ACDEGIJL","79E,85G,81J,74C,82A,77D,87L,80I"],
[259,"ACDEGIJK","79E,85G,81J,74C,82A,77D,87I,80K"],
[260,"ACDEGHKL","79H,85G,81E,74C,82A,77D,87L,80K"],
[261,"ACDEGHJL","79H,85G,81J,74C,82A,77D,87L,80E"],
[262,"ACDEGHJK","79H,85G,81J,74C,82A,77D,87E,80K"],
[263,"ACDEGHIL","79H,85G,81E,74C,82A,77D,87L,80I"],
[264,"ACDEGHIK","79H,85G,81E,74C,82A,77D,87I,80K"],
[265,"ACDEGHIJ","79H,85G,81J,74C,82A,77D,87E,80I"],
[266,"ACDEFJKL","79C,85J,81E,74D,82A,77F,87L,80K"],
[267,"ACDEFIKL","79C,85E,81I,74D,82A,77F,87L,80K"],
[268,"ACDEFIJL","79C,85J,81E,74D,82A,77F,87L,80I"],
[269,"ACDEFIJK","79C,85J,81E,74D,82A,77F,87I,80K"],
[270,"ACDEFHKL","79H,85E,81F,74C,82A,77D,87L,80K"],
[271,"ACDEFHJL","79H,85J,81F,74C,82A,77D,87L,80E"],
[272,"ACDEFHJK","79H,85J,81E,74C,82A,77F,87D,80K"],
[273,"ACDEFHIL","79H,85E,81F,74C,82A,77D,87L,80I"],
[274,"ACDEFHIK","79H,85E,81F,74C,82A,77D,87I,80K"],
[275,"ACDEFHIJ","79H,85J,81E,74C,82A,77F,87D,80I"],
[276,"ACDEFGKL","79C,85G,81E,74D,82A,77F,87L,80K"],
[277,"ACDEFGJL","79C,85G,81J,74D,82A,77F,87L,80E"],
[278,"ACDEFGJK","79C,85G,81J,74D,82A,77F,87E,80K"],
[279,"ACDEFGIL","79C,85G,81E,74D,82A,77F,87L,80I"],
[280,"ACDEFGIK","79C,85G,81E,74D,82A,77F,87I,80K"],
[281,"ACDEFGIJ","79C,85G,81J,74D,82A,77F,87E,80I"],
[282,"ACDEFGHL","79H,85G,81F,74C,82A,77D,87L,80E"],
[283,"ACDEFGHK","79H,85G,81E,74C,82A,77F,87D,80K"],
[284,"ACDEFGHJ","79H,85G,81J,74C,82A,77F,87D,80E"],
[285,"ACDEFGHI","79H,85G,81E,74C,82A,77F,87D,80I"],
[286,"ABGHIJKL","79H,85J,81B,74A,82I,77G,87L,80K"],
[287,"ABFHIJKL","79H,85J,81B,74A,82I,77F,87L,80K"],
[288,"ABFGIJKL","79I,85J,81B,74F,82A,77G,87L,80K"],
[289,"ABFGHJKL","79H,85J,81B,74F,82A,77G,87L,80K"],
[290,"ABFGHIKL","79H,85G,81B,74A,82I,77F,87L,80K"],
[291,"ABFGHIJL","79H,85J,81B,74F,82A,77G,87L,80I"],
[292,"ABFGHIJK","79H,85J,81B,74F,82A,77G,87I,80K"],
[293,"ABEHIJKL","79E,85J,81B,74A,82I,77H,87L,80K"],
[294,"ABEGIJKL","79E,85J,81B,74A,82I,77G,87L,80K"],
[295,"ABEGHJKL","79E,85J,81B,74A,82H,77G,87L,80K"],
[296,"ABEGHIKL","79E,85G,81B,74A,82I,77H,87L,80K"],
[297,"ABEGHIJL","79E,85J,81B,74A,82H,77G,87L,80I"],
[298,"ABEGHIJK","79E,85J,81B,74A,82H,77G,87I,80K"],
[299,"ABEFIJKL","79E,85J,81B,74A,82I,77F,87L,80K"],
[300,"ABEFHJKL","79E,85J,81B,74F,82A,77H,87L,80K"],
[301,"ABEFHIKL","79E,85I,81B,74F,82A,77H,87L,80K"],
[302,"ABEFHIJL","79E,85J,81B,74F,82A,77H,87L,80I"],
[303,"ABEFHIJK","79E,85J,81B,74F,82A,77H,87I,80K"],
[304,"ABEFGJKL","79E,85J,81B,74F,82A,77G,87L,80K"],
[305,"ABEFGIKL","79E,85G,81B,74A,82I,77F,87L,80K"],
[306,"ABEFGIJL","79E,85J,81B,74F,82A,77G,87L,80I"],
[307,"ABEFGIJK","79E,85J,81B,74F,82A,77G,87I,80K"],
[308,"ABEFGHKL","79E,85G,81B,74F,82A,77H,87L,80K"],
[309,"ABEFGHJL","79H,85J,81B,74F,82A,77G,87L,80E"],
[310,"ABEFGHJK","79H,85J,81B,74F,82A,77G,87E,80K"],
[311,"ABEFGHIL","79E,85G,81B,74F,82A,77H,87L,80I"],
[312,"ABEFGHIK","79E,85G,81B,74F,82A,77H,87I,80K"],
[313,"ABEFGHIJ","79H,85J,81B,74F,82A,77G,87E,80I"],
[314,"ABDHIJKL","79I,85J,81B,74D,82A,77H,87L,80K"],
[315,"ABDGIJKL","79I,85J,81B,74D,82A,77G,87L,80K"],
[316,"ABDGHJKL","79H,85J,81B,74D,82A,77G,87L,80K"],
[317,"ABDGHIKL","79I,85G,81B,74D,82A,77H,87L,80K"],
[318,"ABDGHIJL","79H,85J,81B,74D,82A,77G,87L,80I"],
[319,"ABDGHIJK","79H,85J,81B,74D,82A,77G,87I,80K"],
[320,"ABDFIJKL","79I,85J,81B,74D,82A,77F,87L,80K"],
[321,"ABDFHJKL","79H,85J,81B,74D,82A,77F,87L,80K"],
[322,"ABDFHIKL","79H,85I,81B,74D,82A,77F,87L,80K"],
[323,"ABDFHIJL","79H,85J,81B,74D,82A,77F,87L,80I"],
[324,"ABDFHIJK","79H,85J,81B,74D,82A,77F,87I,80K"],
[325,"ABDFGJKL","79F,85J,81B,74D,82A,77G,87L,80K"],
[326,"ABDFGIKL","79I,85G,81B,74D,82A,77F,87L,80K"],
[327,"ABDFGIJL","79F,85J,81B,74D,82A,77G,87L,80I"],
[328,"ABDFGIJK","79F,85J,81B,74D,82A,77G,87I,80K"],
[329,"ABDFGHKL","79H,85G,81B,74D,82A,77F,87L,80K"],
[330,"ABDFGHJL","79H,85G,81B,74D,82A,77F,87L,80J"],
[331,"ABDFGHJK","79H,85G,81B,74D,82A,77F,87J,80K"],
[332,"ABDFGHIL","79H,85G,81B,74D,82A,77F,87L,80I"],
[333,"ABDFGHIK","79H,85G,81B,74D,82A,77F,87I,80K"],
[334,"ABDFGHIJ","79H,85G,81B,74D,82A,77F,87I,80J"],
[335,"ABDEIJKL","79E,85J,81B,74A,82I,77D,87L,80K"],
[336,"ABDEHJKL","79E,85J,81B,74D,82A,77H,87L,80K"],
[337,"ABDEHIKL","79E,85I,81B,74D,82A,77H,87L,80K"],
[338,"ABDEHIJL","79E,85J,81B,74D,82A,77H,87L,80I"],
[339,"ABDEHIJK","79E,85J,81B,74D,82A,77H,87I,80K"],
[340,"ABDEGJKL","79E,85J,81B,74D,82A,77G,87L,80K"],
[341,"ABDEGIKL","79E,85G,81B,74A,82I,77D,87L,80K"],
[342,"ABDEGIJL","79E,85J,81B,74D,82A,77G,87L,80I"],
[343,"ABDEGIJK","79E,85J,81B,74D,82A,77G,87I,80K"],
[344,"ABDEGHKL","79E,85G,81B,74D,82A,77H,87L,80K"],
[345,"ABDEGHJL","79H,85J,81B,74D,82A,77G,87L,80E"],
[346,"ABDEGHJK","79H,85J,81B,74D,82A,77G,87E,80K"],
[347,"ABDEGHIL","79E,85G,81B,74D,82A,77H,87L,80I"],
[348,"ABDEGHIK","79E,85G,81B,74D,82A,77H,87I,80K"],
[349,"ABDEGHIJ","79H,85J,81B,74D,82A,77G,87E,80I"],
[350,"ABDEFJKL","79E,85J,81B,74D,82A,77F,87L,80K"],
[351,"ABDEFIKL","79E,85I,81B,74D,82A,77F,87L,80K"],
[352,"ABDEFIJL","79E,85J,81B,74D,82A,77F,87L,80I"],
[353,"ABDEFIJK","79E,85J,81B,74D,82A,77F,87I,80K"],
[354,"ABDEFHKL","79H,85E,81B,74D,82A,77F,87L,80K"],
[355,"ABDEFHJL","79H,85J,81B,74D,82A,77F,87L,80E"],
[356,"ABDEFHJK","79H,85J,81B,74D,82A,77F,87E,80K"],
[357,"ABDEFHIL","79H,85E,81B,74D,82A,77F,87L,80I"],
[358,"ABDEFHIK","79H,85E,81B,74D,82A,77F,87I,80K"],
[359,"ABDEFHIJ","79H,85J,81B,74D,82A,77F,87E,80I"],
[360,"ABDEFGKL","79E,85G,81B,74D,82A,77F,87L,80K"],
[361,"ABDEFGJL","79E,85G,81B,74D,82A,77F,87L,80J"],
[362,"ABDEFGJK","79E,85G,81B,74D,82A,77F,87J,80K"],
[363,"ABDEFGIL","79E,85G,81B,74D,82A,77F,87L,80I"],
[364,"ABDEFGIK","79E,85G,81B,74D,82A,77F,87I,80K"],
[365,"ABDEFGIJ","79E,85G,81B,74D,82A,77F,87I,80J"],
[366,"ABDEFGHL","79H,85G,81B,74D,82A,77F,87L,80E"],
[367,"ABDEFGHK","79H,85G,81B,74D,82A,77F,87E,80K"],
[368,"ABDEFGHJ","79H,85G,81B,74D,82A,77F,87E,80J"],
[369,"ABDEFGHI","79H,85G,81B,74D,82A,77F,87E,80I"],
[370,"ABCHIJKL","79I,85J,81B,74C,82A,77H,87L,80K"],
[371,"ABCGIJKL","79I,85J,81B,74C,82A,77G,87L,80K"],
[372,"ABCGHJKL","79H,85J,81B,74C,82A,77G,87L,80K"],
[373,"ABCGHIKL","79I,85G,81B,74C,82A,77H,87L,80K"],
[374,"ABCGHIJL","79H,85J,81B,74C,82A,77G,87L,80I"],
[375,"ABCGHIJK","79H,85J,81B,74C,82A,77G,87I,80K"],
[376,"ABCFIJKL","79I,85J,81B,74C,82A,77F,87L,80K"],
[377,"ABCFHJKL","79H,85J,81B,74C,82A,77F,87L,80K"],
[378,"ABCFHIKL","79H,85I,81B,74C,82A,77F,87L,80K"],
[379,"ABCFHIJL","79H,85J,81B,74C,82A,77F,87L,80I"],
[380,"ABCFHIJK","79H,85J,81B,74C,82A,77F,87I,80K"],
[381,"ABCFGJKL","79C,85J,81B,74F,82A,77G,87L,80K"],
[382,"ABCFGIKL","79I,85G,81B,74C,82A,77F,87L,80K"],
[383,"ABCFGIJL","79C,85J,81B,74F,82A,77G,87L,80I"],
[384,"ABCFGIJK","79C,85J,81B,74F,82A,77G,87I,80K"],
[385,"ABCFGHKL","79H,85G,81B,74C,82A,77F,87L,80K"],
[386,"ABCFGHJL","79H,85G,81B,74C,82A,77F,87L,80J"],
[387,"ABCFGHJK","79H,85G,81B,74C,82A,77F,87J,80K"],
[388,"ABCFGHIL","79H,85G,81B,74C,82A,77F,87L,80I"],
[389,"ABCFGHIK","79H,85G,81B,74C,82A,77F,87I,80K"],
[390,"ABCFGHIJ","79H,85G,81B,74C,82A,77F,87I,80J"],
[391,"ABCEIJKL","79E,85J,81B,74A,82I,77C,87L,80K"],
[392,"ABCEHJKL","79E,85J,81B,74C,82A,77H,87L,80K"],
[393,"ABCEHIKL","79E,85I,81B,74C,82A,77H,87L,80K"],
[394,"ABCEHIJL","79E,85J,81B,74C,82A,77H,87L,80I"],
[395,"ABCEHIJK","79E,85J,81B,74C,82A,77H,87I,80K"],
[396,"ABCEGJKL","79E,85J,81B,74C,82A,77G,87L,80K"],
[397,"ABCEGIKL","79E,85G,81B,74A,82I,77C,87L,80K"],
[398,"ABCEGIJL","79E,85J,81B,74C,82A,77G,87L,80I"],
[399,"ABCEGIJK","79E,85J,81B,74C,82A,77G,87I,80K"],
[400,"ABCEGHKL","79E,85G,81B,74C,82A,77H,87L,80K"],
[401,"ABCEGHJL","79H,85J,81B,74C,82A,77G,87L,80E"],
[402,"ABCEGHJK","79H,85J,81B,74C,82A,77G,87E,80K"],
[403,"ABCEGHIL","79E,85G,81B,74C,82A,77H,87L,80I"],
[404,"ABCEGHIK","79E,85G,81B,74C,82A,77H,87I,80K"],
[405,"ABCEGHIJ","79H,85J,81B,74C,82A,77G,87E,80I"],
[406,"ABCEFJKL","79E,85J,81B,74C,82A,77F,87L,80K"],
[407,"ABCEFIKL","79E,85I,81B,74C,82A,77F,87L,80K"],
[408,"ABCEFIJL","79E,85J,81B,74C,82A,77F,87L,80I"],
[409,"ABCEFIJK","79E,85J,81B,74C,82A,77F,87I,80K"],
[410,"ABCEFHKL","79H,85E,81B,74C,82A,77F,87L,80K"],
[411,"ABCEFHJL","79H,85J,81B,74C,82A,77F,87L,80E"],
[412,"ABCEFHJK","79H,85J,81B,74C,82A,77F,87E,80K"],
[413,"ABCEFHIL","79H,85E,81B,74C,82A,77F,87L,80I"],
[414,"ABCEFHIK","79H,85E,81B,74C,82A,77F,87I,80K"],
[415,"ABCEFHIJ","79H,85J,81B,74C,82A,77F,87E,80I"],
[416,"ABCEFGKL","79E,85G,81B,74C,82A,77F,87L,80K"],
[417,"ABCEFGJL","79E,85G,81B,74C,82A,77F,87L,80J"],
[418,"ABCEFGJK","79E,85G,81B,74C,82A,77F,87J,80K"],
[419,"ABCEFGIL","79E,85G,81B,74C,82A,77F,87L,80I"],
[420,"ABCEFGIK","79E,85G,81B,74C,82A,77F,87I,80K"],
[421,"ABCEFGIJ","79E,85G,81B,74C,82A,77F,87I,80J"],
[422,"ABCEFGHL","79H,85G,81B,74C,82A,77F,87L,80E"],
[423,"ABCEFGHK","79H,85G,81B,74C,82A,77F,87E,80K"],
[424,"ABCEFGHJ","79H,85G,81B,74C,82A,77F,87E,80J"],
[425,"ABCEFGHI","79H,85G,81B,74C,82A,77F,87E,80I"],
[426,"ABCDIJKL","79I,85J,81B,74C,82A,77D,87L,80K"],
[427,"ABCDHJKL","79H,85J,81B,74C,82A,77D,87L,80K"],
[428,"ABCDHIKL","79H,85I,81B,74C,82A,77D,87L,80K"],
[429,"ABCDHIJL","79H,85J,81B,74C,82A,77D,87L,80I"],
[430,"ABCDHIJK","79H,85J,81B,74C,82A,77D,87I,80K"],
[431,"ABCDGJKL","79C,85J,81B,74D,82A,77G,87L,80K"],
[432,"ABCDGIKL","79I,85G,81B,74C,82A,77D,87L,80K"],
[433,"ABCDGIJL","79C,85J,81B,74D,82A,77G,87L,80I"],
[434,"ABCDGIJK","79C,85J,81B,74D,82A,77G,87I,80K"],
[435,"ABCDGHKL","79H,85G,81B,74C,82A,77D,87L,80K"],
[436,"ABCDGHJL","79H,85G,81B,74C,82A,77D,87L,80J"],
[437,"ABCDGHJK","79H,85G,81B,74C,82A,77D,87J,80K"],
[438,"ABCDGHIL","79H,85G,81B,74C,82A,77D,87L,80I"],
[439,"ABCDGHIK","79H,85G,81B,74C,82A,77D,87I,80K"],
[440,"ABCDGHIJ","79H,85G,81B,74C,82A,77D,87I,80J"],
[441,"ABCDFJKL","79C,85J,81B,74D,82A,77F,87L,80K"],
[442,"ABCDFIKL","79C,85I,81B,74D,82A,77F,87L,80K"],
[443,"ABCDFIJL","79C,85J,81B,74D,82A,77F,87L,80I"],
[444,"ABCDFIJK","79C,85J,81B,74D,82A,77F,87I,80K"],
[445,"ABCDFHKL","79H,85F,81B,74C,82A,77D,87L,80K"],
[446,"ABCDFHJL","79C,85J,81B,74D,82A,77F,87L,80H"],
[447,"ABCDFHJK","79H,85J,81B,74C,82A,77F,87D,80K"],
[448,"ABCDFHIL","79H,85F,81B,74C,82A,77D,87L,80I"],
[449,"ABCDFHIK","79H,85F,81B,74C,82A,77D,87I,80K"],
[450,"ABCDFHIJ","79H,85J,81B,74C,82A,77F,87D,80I"],
[451,"ABCDFGKL","79C,85G,81B,74D,82A,77F,87L,80K"],
[452,"ABCDFGJL","79C,85G,81B,74D,82A,77F,87L,80J"],
[453,"ABCDFGJK","79C,85G,81B,74D,82A,77F,87J,80K"],
[454,"ABCDFGIL","79C,85G,81B,74D,82A,77F,87L,80I"],
[455,"ABCDFGIK","79C,85G,81B,74D,82A,77F,87I,80K"],
[456,"ABCDFGIJ","79C,85G,81B,74D,82A,77F,87I,80J"],
[457,"ABCDFGHL","79C,85G,81B,74D,82A,77F,87L,80H"],
[458,"ABCDFGHK","79H,85G,81B,74C,82A,77F,87D,80K"],
[459,"ABCDFGHJ","79H,85G,81B,74C,82A,77F,87D,80J"],
[460,"ABCDFGHI","79H,85G,81B,74C,82A,77F,87D,80I"],
[461,"ABCDEJKL","79E,85J,81B,74C,82A,77D,87L,80K"],
[462,"ABCDEIKL","79E,85I,81B,74C,82A,77D,87L,80K"],
[463,"ABCDEIJL","79E,85J,81B,74C,82A,77D,87L,80I"],
[464,"ABCDEIJK","79E,85J,81B,74C,82A,77D,87I,80K"],
[465,"ABCDEHKL","79H,85E,81B,74C,82A,77D,87L,80K"],
[466,"ABCDEHJL","79H,85J,81B,74C,82A,77D,87L,80E"],
[467,"ABCDEHJK","79H,85J,81B,74C,82A,77D,87E,80K"],
[468,"ABCDEHIL","79H,85E,81B,74C,82A,77D,87L,80I"],
[469,"ABCDEHIK","79H,85E,81B,74C,82A,77D,87I,80K"],
[470,"ABCDEHIJ","79H,85J,81B,74C,82A,77D,87E,80I"],
[471,"ABCDEGKL","79E,85G,81B,74C,82A,77D,87L,80K"],
[472,"ABCDEGJL","79E,85G,81B,74C,82A,77D,87L,80J"],
[473,"ABCDEGJK","79E,85G,81B,74C,82A,77D,87J,80K"],
[474,"ABCDEGIL","79E,85G,81B,74C,82A,77D,87L,80I"],
[475,"ABCDEGIK","79E,85G,81B,74C,82A,77D,87I,80K"],
[476,"ABCDEGIJ","79E,85G,81B,74C,82A,77D,87I,80J"],
[477,"ABCDEGHL","79H,85G,81B,74C,82A,77D,87L,80E"],
[478,"ABCDEGHK","79H,85G,81B,74C,82A,77D,87E,80K"],
[479,"ABCDEGHJ","79H,85G,81B,74C,82A,77D,87E,80J"],
[480,"ABCDEGHI","79H,85G,81B,74C,82A,77D,87E,80I"],
[481,"ABCDEFKL","79C,85E,81B,74D,82A,77F,87L,80K"],
[482,"ABCDEFJL","79C,85J,81B,74D,82A,77F,87L,80E"],
[483,"ABCDEFJK","79C,85J,81B,74D,82A,77F,87E,80K"],
[484,"ABCDEFIL","79C,85E,81B,74D,82A,77F,87L,80I"],
[485,"ABCDEFIK","79C,85E,81B,74D,82A,77F,87I,80K"],
[486,"ABCDEFIJ","79C,85J,81B,74D,82A,77F,87E,80I"],
[487,"ABCDEFHL","79H,85F,81B,74C,82A,77D,87L,80E"],
[488,"ABCDEFHK","79H,85E,81B,74C,82A,77F,87D,80K"],
[489,"ABCDEFHJ","79H,85J,81B,74C,82A,77F,87D,80E"],
[490,"ABCDEFHI","79H,85E,81B,74C,82A,77F,87D,80I"],
[491,"ABCDEFGL","79C,85G,81B,74D,82A,77F,87L,80E"],
[492,"ABCDEFGK","79C,85G,81B,74D,82A,77F,87E,80K"],
[493,"ABCDEFGJ","79C,85G,81B,74D,82A,77F,87E,80J"],
[494,"ABCDEFGI","79C,85G,81B,74D,82A,77F,87E,80I"],
[495,"ABCDEFGH","79H,85G,81B,74C,82A,77F,87D,80E"]
];

function empGetGroupStandings(){
  // Calcula 1ro, 2do, 3ro de cada grupo usando REAL_MATCHES + lista de grupos A-L
  var groups = {};
  'ABCDEFGHIJKL'.split('').forEach(function(g){ groups[g] = {}; });

  REAL_MATCHES.forEach(function(m){
    if(!m.g) return;
    if(!groups[m.g][m.a]) groups[m.g][m.a] = {team:m.a, pts:0, gf:0, gc:0, pj:0};
    if(!groups[m.g][m.b]) groups[m.g][m.b] = {team:m.b, pts:0, gf:0, gc:0, pj:0};
    if(m.ga===null || m.gb===null) return;
    var ta = groups[m.g][m.a], tb = groups[m.g][m.b];
    ta.pj++; tb.pj++;
    ta.gf += m.ga; ta.gc += m.gb;
    tb.gf += m.gb; tb.gc += m.ga;
    if(m.ga > m.gb){ ta.pts += 3; }
    else if(m.ga < m.gb){ tb.pts += 3; }
    else { ta.pts += 1; tb.pts += 1; }
  });

  var standings = {};
  Object.keys(groups).forEach(function(g){
    var teams = Object.values(groups[g]).sort(function(a,b){
      if(b.pts !== a.pts) return b.pts - a.pts;
      var gdA = a.gf - a.gc, gdB = b.gf - b.gc;
      if(gdB !== gdA) return gdB - gdA;
      return b.gf - a.gf;
    });
    standings[g] = teams;
  });
  return standings;
}

function empGetThirdPlaceRanking(standings){
  var thirds = [];
  Object.keys(standings).forEach(function(g){
    var teams = standings[g];
    if(teams.length >= 3){
      var t = teams[2];
      thirds.push(Object.assign({}, t, {group:g}));
    }
  });
  thirds.sort(function(a,b){
    if(b.pts !== a.pts) return b.pts - a.pts;
    var gdA = a.gf-a.gc, gdB = b.gf-b.gc;
    if(gdB !== gdA) return gdB - gdA;
    return b.gf - a.gf;
  });
  return thirds;
}

function empFindCombo(qualifiedGroupsSet){
  // qualifiedGroupsSet: array de 8 letras de grupo que clasificaron en 3er puesto
  var sorted = qualifiedGroupsSet.slice().sort().join('');
  for(var i=0;i<THIRD_PLACE_COMBOS.length;i++){
    var row = THIRD_PLACE_COMBOS[i];
    var rowSorted = row[1].split('').sort().join('');
    if(rowSorted === sorted) return row;
  }
  return null;
}

function empResolveTeam(ref, standings, comboAssign){
  if(!ref) return null;
  if(ref.type === 'W'){
    var t = standings[ref.g] && standings[ref.g][0];
    return t ? {name:t.team, label:'1&deg; Grupo '+ref.g} : null;
  }
  if(ref.type === 'RU'){
    var t2 = standings[ref.g] && standings[ref.g][1];
    return t2 ? {name:t2.team, label:'2&deg; Grupo '+ref.g} : null;
  }
  if(ref.type === '3RD'){
    if(!comboAssign) return null;
    var g = comboAssign[ref.slot];
    if(!g) return null;
    var t3 = standings[g] && standings[g][2];
    return t3 ? {name:t3.team, label:'3&deg; Grupo '+g} : null;
  }
  return null;
}

function empBuildBracket(){
  var standings = empGetGroupStandings();
  var thirdsRanked = empGetThirdPlaceRanking(standings);
  var groupsComplete = Object.keys(standings).every(function(g){
    return standings[g].length===4 && standings[g].every(function(t){return t.pj===3;});
  });

  var comboAssign = null;
  if(groupsComplete && thirdsRanked.length >= 8){
    var qualifiedGroups = thirdsRanked.slice(0,8).map(function(t){return t.group;});
    var combo = empFindCombo(qualifiedGroups);
    if(combo){
      comboAssign = {};
      combo[2].split(',').forEach(function(pair){
        var matchNo = parseInt(pair.slice(0,2));
        var grp = pair.slice(2);
        comboAssign[matchNo] = grp;
      });
    }
  }

  var matchResults = {};
  R32_FIXED_RULES.forEach(function(rule){
    var teamA = empResolveTeam(rule.a, standings, comboAssign);
    var teamB = empResolveTeam(rule.b, standings, comboAssign);
    matchResults[rule.m] = {teamA:teamA, teamB:teamB, date:rule.date, winner:null};
  });

  return {standings:standings, thirdsRanked:thirdsRanked, comboAssign:comboAssign, matches:matchResults, groupsComplete:groupsComplete};
}

function empFlag(teamName){
  var tf = TF[teamName];
  if(!tf) return '<span class=\\"champ-flag\\" style=\\"width:18px;height:13px;background:#ddd\\"></span>';
  return FH(tf.c, tf.d, 18, 13);
}

function empRenderMatchBox(matchNo, data, extraClass){
  var isPy = (data.teamA && data.teamA.name==='Paraguay') || (data.teamB && data.teamB.name==='Paraguay');
  var cls = 'emp-match' + (isPy ? ' py' : (!data.teamA || !data.teamB ? ' tbd' : ''));
  var rowA, rowB;
  if(data.teamA){
    rowA = '<div class=\\"emp-team-row\\">' + empFlag(data.teamA.name) + '<span>'+data.teamA.name+'</span></div>';
  } else {
    rowA = '<div class=\\"emp-team-row tbd-text\\">' + (R32_FIXED_RULES.find(function(r){return r.m===matchNo;}) ? 'Por definir' : 'Ganador M'+matchNo) + '</div>';
  }
  if(data.teamB){
    rowB = '<div class=\\"emp-team-row\\">' + empFlag(data.teamB.name) + '<span>'+data.teamB.name+'</span></div>';
  } else {
    rowB = '<div class=\\"emp-team-row tbd-text\\">Por definir</div>';
  }
  return '<div class=\\"'+cls+'\\">'+rowA+rowB+'<div class=\\"emp-match-meta\\">M'+matchNo+(data.date?' &middot; '+data.date:'')+'</div></div>';
}

function renderEmparejamiento(){
  var container = document.getElementById('empBracketContainer');
  var subtitle = document.getElementById('empSubtitle');
  if(!container) return;

  var bracket = empBuildBracket();

  if(subtitle){
    if(bracket.groupsComplete && bracket.comboAssign){
      subtitle.textContent = 'Cuadro confirmado segun resultados oficiales de la fase de grupos';
    } else {
      subtitle.textContent = 'Se completa solo segun resultados de la fase de grupos (' + bracket.thirdsRanked.length + ' de 12 terceros definidos)';
    }
  }

  var html = '<div class=\\"emp-bracket-grid\\">';

  html += '<div><div class=\\"emp-stage-label\\">DIECISEISAVOS</div>';
  R32_FIXED_RULES.forEach(function(rule){
    html += empRenderMatchBox(rule.m, bracket.matches[rule.m]);
  });
  html += '</div>';

  html += '<div><div class=\\"emp-stage-label\\">OCTAVOS</div>';
  R16_RULES.forEach(function(rule){
    html += empRenderMatchBox(rule.m, {teamA:null, teamB:null, date:rule.date});
  });
  html += '</div>';

  html += '<div><div class=\\"emp-stage-label\\">CUARTOS</div>';
  QF_RULES.forEach(function(rule){
    html += empRenderMatchBox(rule.m, {teamA:null, teamB:null, date:rule.date});
  });
  html += '</div>';

  html += '<div><div class=\\"emp-stage-label\\">SEMIFINALES</div>';
  SF_RULES.forEach(function(rule){
    html += empRenderMatchBox(rule.m, {teamA:null, teamB:null, date:rule.date});
  });
  html += '<div style=\\"margin-top:14px\\"><div class=\\"emp-stage-label\\">TERCER PUESTO</div>';
  html += empRenderMatchBox(THIRD_PLACE_RULE.m, {teamA:null, teamB:null, date:THIRD_PLACE_RULE.date});
  html += '</div></div>';

  html += '<div><div class=\\"emp-stage-label\\">FINAL</div>';
  html += '<div class=\\"emp-final-box\\"><div class=\\"lbl\\">19/07 &middot; MetLife Stadium</div><div class=\\"team\\">Por definir</div><div class=\\"team\\">Por definir</div></div>';
  html += '</div>';

  html += '</div>';
  container.innerHTML = html;
}
"""

# Insertar JS si no existe
if 'renderEmparejamiento' in html:
    print("JS emparejamiento ya existe, saltando insercion.")
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + EMP_JS + '\n' + html[last_script:]
        print("JS emparejamiento agregado OK")
    else:
        print("WARNING: no se encontro </script> para insertar JS emparejamiento")

# showPage hook
OLD_SHOW = "if(id==='campeones')renderCampeones();"
NEW_SHOW = "if(id==='campeones')renderCampeones();\n  if(id==='emparejamiento')renderEmparejamiento();"

if "if(id==='emparejamiento')" in html:
    print("showPage emparejamiento ya existe OK")
elif OLD_SHOW in html:
    html = html.replace(OLD_SHOW, NEW_SHOW, 1)
    print("showPage emparejamiento agregado OK")
else:
    # fallback: insertar despues del hook de miequipo
    OLD_SHOW2 = "if(id==='miequipo')renderMyTeam();"
    if "if(id==='emparejamiento')" not in html and OLD_SHOW2 in html:
        html = html.replace(OLD_SHOW2, OLD_SHOW2 + "\n  if(id==='emparejamiento')renderEmparejamiento();", 1)
        print("showPage emparejamiento agregado OK (fallback)")
    else:
        print("WARNING: showPage hook no encontrado para emparejamiento")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
print("Ahora correr: python3 build.py")
