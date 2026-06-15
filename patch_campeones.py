"""
patch_campeones.py
Ejecutar en la raiz del repo: python3 patch_campeones.py
Lee template.html, agrega la pestana Campeones y guarda.
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado. Ejecuta desde la raiz del repo.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────
# 1. CSS: insertar antes del cierre </style>
# ─────────────────────────────────────────────
CSS = """
/* CAMPEONES */
.champ-body{padding:20px;max-width:900px;margin:0 auto}
.champ-hero{background:#0B369D;border-radius:16px;padding:20px 24px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;position:relative;overflow:hidden}
.champ-hero::before{content:'\\1F3C6';position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:80px;opacity:.1}
.champ-hero h2{color:#fff;font-size:20px;font-weight:900;margin-bottom:3px}
.champ-hero p{color:rgba(255,255,255,.6);font-size:12px}
.champ-stats{display:flex;gap:8px}
.champ-stat{background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px;text-align:center;min-width:56px}
.champ-stat span{display:block;font-size:20px;font-weight:900;color:#fff}
.champ-stat small{font-size:8px;color:rgba(255,255,255,.6);font-weight:700;letter-spacing:1px}
.champ-subtabs{display:flex;background:#fff;border-radius:12px;border:1px solid var(--vg2);overflow:hidden;margin-bottom:16px}
.champ-stab{flex:1;padding:10px 6px;text-align:center;font-size:12px;font-weight:800;color:var(--vm);cursor:pointer;border:none;background:none;font-family:'Poppins',sans-serif;border-right:1px solid var(--vg2);transition:all .15s}
.champ-stab:last-child{border-right:none}
.champ-stab.active{background:#0B369D;color:#fff}
.champ-stab:hover:not(.active){background:var(--vg)}
.champ-filters{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.champ-fbtn{padding:5px 12px;border-radius:16px;border:1.5px solid var(--vg3);background:#fff;color:var(--vm);font-size:11px;font-weight:800;cursor:pointer}
.champ-fbtn.active{background:#0B369D;color:#fff;border-color:#0B369D}
.champ-row{background:#fff;border-radius:10px;border:1px solid var(--vg2);padding:11px 14px;display:flex;align-items:center;gap:10px;margin-bottom:7px}
.champ-year{font-size:12px;font-weight:900;color:#0B369D;min-width:36px}
.champ-flag{display:inline-flex;border-radius:3px;overflow:hidden;border:1px solid rgba(0,0,0,.12);flex-shrink:0}
.champ-flag span{display:block}
.champ-name{font-size:13px;font-weight:800;color:#0a1f6e;flex:1}
.champ-host{font-size:11px;color:var(--vm);flex:1;text-align:center}
.champ-final{font-size:11px;font-weight:700;color:#0B369D;background:#f0f4ff;padding:3px 8px;border-radius:6px;white-space:nowrap}
.rank-bar-w{width:70px;height:4px;background:var(--vg2);border-radius:2px;overflow:hidden}
.rank-bar-f{height:100%;background:linear-gradient(90deg,#0B369D,#E53935);border-radius:2px}
.rec-card{background:#fff;border-radius:10px;border:1px solid var(--vg2);padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;gap:12px}
.rec-icon{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.rec-title{font-size:12px;font-weight:800;color:#0a1f6e;margin-bottom:3px}
.rec-desc{font-size:11px;font-weight:700}
.goal-hist-row{background:#fff;border-radius:10px;border:1px solid var(--vg2);padding:11px 14px;display:flex;align-items:center;gap:10px;margin-bottom:7px}
.goal-hist-pos{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:900;flex-shrink:0}
.goal-hist-avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;font-weight:900;flex-shrink:0}
.goal-hist-info{flex:1}
.goal-hist-name{font-size:13px;font-weight:800;color:#0a1f6e}
.goal-hist-sub{font-size:11px;color:var(--vm);margin-top:2px;display:flex;align-items:center;gap:4px}
.goal-hist-num{font-size:22px;font-weight:900;color:#0B369D;line-height:1}
.goal-hist-lbl{font-size:9px;color:var(--vm);font-weight:700}
.era-badge{font-size:9px;font-weight:800;padding:2px 7px;border-radius:6px;margin-left:4px}
@media(max-width:700px){.champ-body{padding:12px}}
"""

if '/* CAMPEONES */' in html:
    print("CSS ya existe, saltando.")
else:
    html = html.replace('</style>', CSS + '</style>', 1)
    print("CSS agregado OK")

# ─────────────────────────────────────────────
# 2. NAV TAB: agregar antes de Alertas
# ─────────────────────────────────────────────
OLD_NAV = "onclick=\"showPage('alertas',this)\">&#x1F514; Alertas</button>"
NEW_NAV  = "onclick=\"showPage('campeones',this)\">&#x1F3C5; Campeones</button>\n      <button class=\"nav-tab\" onclick=\"showPage('alertas',this)\">&#x1F514; Alertas</button>"

# Try multiple variants since emoji rendering varies
nav_variants = [
    ("onclick=\"showPage('alertas',this)\">🔔 Alertas</button>",
     "onclick=\"showPage('campeones',this)\">🏅 Campeones</button>\n      <button class=\"nav-tab\" onclick=\"showPage('alertas',this)\">🔔 Alertas</button>"),
]

nav_patched = False
for old, new in nav_variants:
    if old in html:
        html = html.replace(old, new, 1)
        nav_patched = True
        print("Nav tab agregado OK (emoji variant)")
        break

if not nav_patched:
    # Try with regex
    m = re.search(r"onclick=\"showPage\('alertas',this\)\">.*?Alertas</button>", html)
    if m:
        old_text = m.group(0)
        new_text = "onclick=\"showPage('campeones',this)\">&#x1F3C5; Campeones</button>\n      <button class=\"nav-tab\" " + old_text
        html = html.replace(old_text, new_text, 1)
        nav_patched = True
        print("Nav tab agregado OK (regex)")
    else:
        print("WARNING: Nav tab no encontrado - revisar manualmente")

# ─────────────────────────────────────────────
# 3. PAGE HTML: insertar antes de page-alertas
# ─────────────────────────────────────────────
CHAMP_PAGE = """
  <!-- CAMPEONES -->
  <div id="page-campeones" class="page">
    <div class="champ-body">
      <div class="champ-hero">
        <div><h2>Historia del Mundial</h2><p>Campeones &middot; Goleadores &middot; R&eacute;cords &middot; 1930&ndash;2022</p></div>
        <div class="champ-stats">
          <div class="champ-stat"><span>22</span><small>MUNDIALES</small></div>
          <div class="champ-stat"><span>2548</span><small>GOLES</small></div>
        </div>
      </div>
      <div class="champ-subtabs">
        <button class="champ-stab active" onclick="showChampTab('campeones',this)">&#x1F3C6; Campeones</button>
        <button class="champ-stab" onclick="showChampTab('goleadores',this)">&#x26BD; Goleadores</button>
        <button class="champ-stab" onclick="showChampTab('ranking',this)">&#x1F4CA; Ranking</button>
        <button class="champ-stab" onclick="showChampTab('records',this)">&#x2B50; R&eacute;cords</button>
      </div>
      <div id="champ-tab-campeones">
        <div class="champ-filters" id="champFilters">
          <button class="champ-fbtn active" onclick="filterChamp('todos',this)">Todos</button>
          <button class="champ-fbtn" onclick="filterChamp('Brasil',this)">Brasil</button>
          <button class="champ-fbtn" onclick="filterChamp('Alemania',this)">Alemania</button>
          <button class="champ-fbtn" onclick="filterChamp('Italia',this)">Italia</button>
          <button class="champ-fbtn" onclick="filterChamp('Argentina',this)">Argentina</button>
        </div>
        <div id="champList"></div>
      </div>
      <div id="champ-tab-goleadores" style="display:none">
        <div class="champ-filters" id="goalFilters">
          <button class="champ-fbtn active" onclick="filterGoalHist('todos',this)">Todos</button>
          <button class="champ-fbtn" onclick="filterGoalHist('moderno',this)">2000+</button>
          <button class="champ-fbtn" onclick="filterGoalHist('clasico',this)">1990s</button>
          <button class="champ-fbtn" onclick="filterGoalHist('historico',this)">Cl&aacute;sicos</button>
        </div>
        <div id="goalHistList"></div>
      </div>
      <div id="champ-tab-ranking" style="display:none">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">
          <div class="scard"><div class="slbl">M&aacute;s t&iacute;tulos</div><div class="sval">5</div><div class="ssub">Brasil</div></div>
          <div class="scard"><div class="slbl">Pa&iacute;ses campeones</div><div class="sval">8</div><div class="ssub">distintos</div></div>
          <div class="scard"><div class="slbl">Primer campe&oacute;n</div><div class="sval">1930</div><div class="ssub">Uruguay</div></div>
          <div class="scard"><div class="slbl">&Uacute;ltimo campe&oacute;n</div><div class="sval">2022</div><div class="ssub">Argentina</div></div>
        </div>
        <div style="font-size:10px;font-weight:800;color:var(--vm);letter-spacing:1px;margin-bottom:8px">RANKING POR T&Iacute;TULOS</div>
        <div class="stat-list" id="champRankList"></div>
      </div>
      <div id="champ-tab-records" style="display:none">
        <div id="recList"></div>
      </div>
    </div>
  </div>

"""

if 'id="page-campeones"' in html:
    print("Page campeones ya existe, saltando.")
else:
    # Find page-alertas and insert before it
    m = re.search(r'(\s*<!-- ALERTAS -->)', html)
    if m:
        html = html[:m.start()] + CHAMP_PAGE + html[m.start():]
        print("Page campeones agregado OK")
    else:
        print("WARNING: <!-- ALERTAS --> no encontrado - revisar manualmente")

# ─────────────────────────────────────────────
# 4. JS DATA + FUNCTIONS: insertar antes de </script> final
# ─────────────────────────────────────────────
CHAMP_JS = """
// ============================================================
// CAMPEONES HISTORICOS
// ============================================================
const HIST_CHAMPS=[
  {y:2022,c:'Argentina',f:['#74ACDF','#fff','#74ACDF'],d:'h',h:'Qatar',fin:'Argentina 3-3 Francia (pen)'},
  {y:2018,c:'Francia',f:['#002395','#fff','#ED2939'],d:'v',h:'Rusia',fin:'Francia 4-2 Croacia'},
  {y:2014,c:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',h:'Brasil',fin:'Alemania 1-0 Argentina'},
  {y:2010,c:'España',f:['#AA151B','#F1BF00','#AA151B'],d:'h',h:'Sudáfrica',fin:'España 1-0 Países Bajos'},
  {y:2006,c:'Italia',f:['#009246','#fff','#CE2B37'],d:'v',h:'Alemania',fin:'Italia 1-1 Francia (pen)'},
  {y:2002,c:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',h:'Japón/Corea',fin:'Brasil 2-0 Alemania'},
  {y:1998,c:'Francia',f:['#002395','#fff','#ED2939'],d:'v',h:'Francia',fin:'Francia 3-0 Brasil'},
  {y:1994,c:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',h:'EE.UU.',fin:'Brasil 0-0 Italia (pen)'},
  {y:1990,c:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',h:'Italia',fin:'Alemania 1-0 Argentina'},
  {y:1986,c:'Argentina',f:['#74ACDF','#fff','#74ACDF'],d:'h',h:'México',fin:'Argentina 3-2 Alemania'},
  {y:1982,c:'Italia',f:['#009246','#fff','#CE2B37'],d:'v',h:'España',fin:'Italia 3-1 Alemania'},
  {y:1978,c:'Argentina',f:['#74ACDF','#fff','#74ACDF'],d:'h',h:'Argentina',fin:'Argentina 3-1 Países Bajos'},
  {y:1974,c:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',h:'Alemania',fin:'Alemania 2-1 Países Bajos'},
  {y:1970,c:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',h:'México',fin:'Brasil 4-1 Italia'},
  {y:1966,c:'Inglaterra',f:['#CF142B','#fff','#CF142B'],d:'h',h:'Inglaterra',fin:'Inglaterra 4-2 Alemania'},
  {y:1962,c:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',h:'Chile',fin:'Brasil 3-1 Checoslovaquia'},
  {y:1958,c:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',h:'Suecia',fin:'Brasil 5-2 Suecia'},
  {y:1954,c:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',h:'Suiza',fin:'Alemania 3-2 Hungría'},
  {y:1950,c:'Uruguay',f:['#fff','#5bcfed','#0038A8'],d:'h',h:'Brasil',fin:'Uruguay 2-1 Brasil'},
  {y:1938,c:'Italia',f:['#009246','#fff','#CE2B37'],d:'v',h:'Francia',fin:'Italia 4-2 Hungría'},
  {y:1934,c:'Italia',f:['#009246','#fff','#CE2B37'],d:'v',h:'Italia',fin:'Italia 2-1 Checoslovaquia'},
  {y:1930,c:'Uruguay',f:['#fff','#5bcfed','#0038A8'],d:'h',h:'Uruguay',fin:'Uruguay 4-2 Argentina'},
];

const HIST_GOALS=[
  {name:'Miroslav Klose',team:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',goles:16,años:'2002-2014',era:'moderno',av:'#0B369D'},
  {name:'Ronaldo',team:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',goles:15,años:'1998-2006',era:'moderno',av:'#009C3B'},
  {name:'Gerd Müller',team:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',goles:14,años:'1970-1974',era:'historico',av:'#c8922a'},
  {name:'Lionel Messi',team:'Argentina',f:['#74ACDF','#fff','#74ACDF'],d:'h',goles:13,años:'2006-2022',era:'moderno',av:'#74ACDF'},
  {name:'Just Fontaine',team:'Francia',f:['#002395','#fff','#ED2939'],d:'v',goles:13,años:'1958',era:'historico',av:'#E53935'},
  {name:'Pelé',team:'Brasil',f:['#009C3B','#FDEF42','#009C3B'],d:'h',goles:12,años:'1958-1970',era:'historico',av:'#009C3B'},
  {name:'Sándor Kocsis',team:'Hungría',f:['#CE2939','#fff','#477050'],d:'h',goles:11,años:'1954',era:'historico',av:'#888'},
  {name:'Jürgen Klinsmann',team:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',goles:11,años:'1990-1998',era:'clasico',av:'#333'},
  {name:'Thomas Müller',team:'Alemania',f:['#000','#DD0000','#FFCE00'],d:'h',goles:10,años:'2010-2022',era:'moderno',av:'#444'},
  {name:'Gary Lineker',team:'Inglaterra',f:['#CF142B','#fff','#CF142B'],d:'h',goles:10,años:'1986-1990',era:'clasico',av:'#CF142B'},
  {name:'Gabriel Batistuta',team:'Argentina',f:['#74ACDF','#fff','#74ACDF'],d:'h',goles:10,años:'1994-2002',era:'clasico',av:'#74ACDF'},
  {name:'Teófilo Cubillas',team:'Perú',f:['#D91023','#fff','#D91023'],d:'v',goles:10,años:'1970-1978',era:'historico',av:'#D91023'},
  {name:'Grzegorz Lato',team:'Polonia',f:['#fff','#DC143C','#fff'],d:'h',goles:10,años:'1974-1982',era:'historico',av:'#DC143C'},
  {name:'Cristiano Ronaldo',team:'Portugal',f:['#006600','#FF0000','#FF0000'],d:'v',goles:8,años:'2006-2022',era:'moderno',av:'#E53935'},
];

const HIST_RECORDS=[
  {icon:'⚽',title:'Más goles en un Mundial',desc:'Just Fontaine — 13 goles · Francia 1958',color:'#e8f5e9',tc:'#2e7d32'},
  {icon:'🏆',title:'Más títulos como jugador',desc:'Pelé — 3 copas (1958, 1962, 1970)',color:'#fff8e1',tc:'#c8922a'},
  {icon:'👑',title:'Más mundiales jugados',desc:'Lothar Matthäus — 5 torneos (1982-1998)',color:'#e3f2fd',tc:'#1565c0'},
  {icon:'⚡',title:'Gol más rápido',desc:'Hakan Sükür — 11 seg · Turquía vs Corea 2002',color:'#fce4ec',tc:'#c62828'},
  {icon:'📊',title:'Más partidos ganados (país)',desc:'Brasil — 76 victorias en Mundiales',color:'#e8f5e9',tc:'#2e7d32'},
  {icon:'🌟',title:'Máximo goleador un partido',desc:'Oleg Salenko — 5 goles · Rusia vs Camerún 1994',color:'#fff3e0',tc:'#e65100'},
  {icon:'🌍',title:'Mundial con más goles',desc:'Francia 1998 — 171 goles en 64 partidos',color:'#e0f7fa',tc:'#00695c'},
  {icon:'🇧🇷',title:'Único campeón en 5 ocasiones',desc:'Brasil — 1958, 1962, 1970, 1994, 2002',color:'#f3e5f5',tc:'#6a1b9a'},
];

function FH(f,d,w,h){
  var dir=d==='v'?'row':'column';
  return '<span class="champ-flag" style="width:'+w+'px;height:'+h+'px;flex-direction:'+dir+'">'+f.map(function(c){return'<span style="flex:1;background:'+c+'"></span>';}).join('')+'</span>';
}

function renderChampList(filter){
  var items=filter==='todos'?HIST_CHAMPS:HIST_CHAMPS.filter(function(d){return d.c===filter;});
  document.getElementById('champList').innerHTML=items.map(function(d,i){
    var bl=i===0?'3px solid #c8922a':i===1?'3px solid #888':i===2?'3px solid #cd7f32':'1px solid var(--vg2)';
    return '<div class="champ-row" style="border-left:'+bl+'">'
      +'<span class="champ-year">'+d.y+'</span>'
      +FH(d.f,d.d,26,17)
      +'<span class="champ-name">'+d.c+'</span>'
      +'<span class="champ-host">'+d.h+'</span>'
      +'<span class="champ-final">'+d.fin+'</span>'
      +'</div>';
  }).join('');
}

function renderGoalHistList(filter){
  var sorted=HIST_GOALS.slice().sort(function(a,b){return b.goles-a.goles;});
  var items=filter==='todos'?sorted:sorted.filter(function(d){return d.era===filter;});
  var max=items.length>0?items[0].goles:1;
  var avatarColors=['#0B369D','#E53935','#2e7d32','#c8922a','#6b7aaa'];
  document.getElementById('goalHistList').innerHTML=items.map(function(g,i){
    var cls=i===0?'rp1':i===1?'rp2':i===2?'rp3':'rpx';
    var era=g.era==='moderno'?{bg:'#e3f2fd',c:'#1565c0',t:'2000+'}:g.era==='clasico'?{bg:'#e8f5e9',c:'#2e7d32',t:'1990s'}:{bg:'#fff8e1',c:'#c8922a',t:'Clasico'};
    var initials=g.name.split(' ').map(function(w){return w[0];}).slice(0,2).join('');
    var pct=Math.round(g.goles/max*100);
    return '<div class="goal-hist-row">'
      +'<div class="goal-hist-pos '+cls+'">'+(i+1)+'</div>'
      +'<div class="goal-hist-avatar" style="background:'+(g.av||avatarColors[i%5])+'">'+initials+'</div>'
      +'<div class="goal-hist-info">'
        +'<div class="goal-hist-name">'+g.name+' <span class="era-badge" style="background:'+era.bg+';color:'+era.c+'">'+era.t+'</span></div>'
        +'<div class="goal-hist-sub">'+FH(g.f,g.d,16,11)+' '+g.team+' &middot; '+g.años+'</div>'
        +'<div style="margin-top:4px;width:100px;height:3px;background:var(--vg2);border-radius:2px;overflow:hidden"><div style="width:'+pct+'%;height:100%;background:linear-gradient(90deg,#0B369D,#E53935);border-radius:2px"></div></div>'
      +'</div>'
      +'<div style="text-align:right;flex-shrink:0">'
        +'<div class="goal-hist-num">'+g.goles+'</div>'
        +'<div class="goal-hist-lbl">GOLES</div>'
      +'</div>'
      +'</div>';
  }).join('');
}

function renderChampRanking(){
  var counts={};
  HIST_CHAMPS.forEach(function(d){counts[d.c]=(counts[d.c]||0)+1;});
  var sorted=Object.entries(counts).sort(function(a,b){return b[1]-a[1];});
  var max=sorted[0][1];
  document.getElementById('champRankList').innerHTML=sorted.map(function(arr,i){
    var c=arr[0], n=arr[1];
    var pct=Math.round(n/max*100);
    var cls=i===0?'rp1':i===1?'rp2':i===2?'rp3':'rpx';
    var entry=HIST_CHAMPS.find(function(d){return d.c===c;});
    return '<div class="rk-row">'
      +'<div class="rk-pos '+cls+'">'+(i+1)+'</div>'
      +FH(entry.f,entry.d,22,15)
      +'<span style="flex:1;font-size:12px;font-weight:700;color:var(--vt);margin-left:6px">'+c+'</span>'
      +'<div class="rank-bar-w"><div class="rank-bar-f" style="width:'+pct+'%"></div></div>'
      +'<span style="font-size:14px;font-weight:900;color:#0B369D;min-width:36px;text-align:right">'+n+' 🏆</span>'
      +'</div>';
  }).join('');
}

function renderRecords(){
  document.getElementById('recList').innerHTML=HIST_RECORDS.map(function(r){
    return '<div class="rec-card">'
      +'<div class="rec-icon" style="background:'+r.color+'">'+r.icon+'</div>'
      +'<div><div class="rec-title">'+r.title+'</div><div class="rec-desc" style="color:'+r.tc+'">'+r.desc+'</div></div>'
      +'</div>';
  }).join('');
}

function filterChamp(f,btn){
  document.querySelectorAll('#champFilters .champ-fbtn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  renderChampList(f);
}

function filterGoalHist(f,btn){
  document.querySelectorAll('#goalFilters .champ-fbtn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  renderGoalHistList(f);
}

function showChampTab(tab,btn){
  document.querySelectorAll('.champ-stab').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  ['campeones','goleadores','ranking','records'].forEach(function(t){
    var el=document.getElementById('champ-tab-'+t);
    if(el) el.style.display=t===tab?'block':'none';
  });
}

function renderCampeones(){
  renderChampList('todos');
  renderGoalHistList('todos');
  renderChampRanking();
  renderRecords();
}
"""

if 'renderCampeones' in html:
    print("JS campeones ya existe, saltando.")
else:
    # Insert before the last </script>
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + CHAMP_JS + '\n' + html[last_script:]
        print("JS campeones agregado OK")
    else:
        print("WARNING: </script> no encontrado")

# ─────────────────────────────────────────────
# 5. showPage(): agregar llamada a renderCampeones
# ─────────────────────────────────────────────
OLD_SHOW = "if(id==='miequipo')renderMyTeam();"
NEW_SHOW = "if(id==='miequipo')renderMyTeam();\n  if(id==='campeones')renderCampeones();"

if "if(id==='campeones')" in html:
    print("showPage campeones ya existe, saltando.")
elif OLD_SHOW in html:
    html = html.replace(OLD_SHOW, NEW_SHOW, 1)
    print("showPage campeones agregado OK")
else:
    print("WARNING: showPage hook no encontrado - revisar manualmente")

# ─────────────────────────────────────────────
# Guardar
# ─────────────────────────────────────────────
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.count('\n')
size  = len(html)
print(f"\nDone! {lines} lineas, {size} bytes -> {SRC}")
print("Ahora correr: python3 build.py")
