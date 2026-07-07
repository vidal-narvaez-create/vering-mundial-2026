"""
patch_emparejamiento_v2.py
Versión robusta - inserta nav tab Emparejamiento y reemplaza función JS
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. NAV TAB - buscar con regex flexible
# ============================================================
nav_patched = False

if "showPage('emparejamiento'" in html:
    print("Nav tab emparejamiento ya existe OK")
    nav_patched = True
else:
    # Buscar el boton de Mi Equipo con regex flexible
    pattern = r"(<button[^>]*onclick=['\"]showPage\('miequipo'[^>]*>)[^<]*(Mi\s*Equipo[^<]*</button>)"
    m = re.search(pattern, html, re.IGNORECASE)
    if m:
        old_text = m.group(0)
        new_text = '<button class="nav-tab" onclick="showPage(\'emparejamiento\',this)">&#x1F5FA; Emparejamiento</button>\n      ' + old_text
        html = html.replace(old_text, new_text, 1)
        nav_patched = True
        print("Nav tab emparejamiento agregado OK (regex)")
    else:
        # Buscar con patron mas simple
        patterns_to_try = [
            ">'Mi Equipo'",
            ">Mi Equipo<",
            "miequipo",
        ]
        for pat in patterns_to_try:
            idx = html.find(pat)
            if idx > 0:
                # Encontrar el boton completo alrededor de ese indice
                start = html.rfind('<button', 0, idx)
                end = html.find('</button>', idx) + 9
                if start > 0 and end > 9:
                    old_btn = html[start:end]
                    new_btn = '<button class="nav-tab" onclick="showPage(\'emparejamiento\',this)">&#x1F5FA; Emparejamiento</button>\n      ' + old_btn
                    html = html[:start] + new_btn + html[end:]
                    nav_patched = True
                    print(f"Nav tab emparejamiento agregado OK (patron: {pat})")
                    break

    if not nav_patched:
        print("WARNING: no se pudo insertar nav tab - buscando en JS...")
        # Buscar en la funcion showPage como fallback
        if "showPage('miequipo'" in html:
            idx = html.find("showPage('miequipo'")
            start = html.rfind('<button', 0, idx)
            end = html.find('</button>', idx) + 9
            if start > 0:
                old_btn = html[start:end]
                new_btn = '<button class="nav-tab" onclick="showPage(\'emparejamiento\',this)">&#x1F5FA; Emparejamiento</button>\n      ' + old_btn
                html = html[:start] + new_btn + html[end:]
                nav_patched = True
                print("Nav tab emparejamiento agregado OK (fallback JS)")

# ============================================================
# 2. PAGE HTML - insertar si no existe
# ============================================================
if 'id="page-emparejamiento"' not in html:
    EMP_PAGE = '''
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
        <p id="empSubtitle">Se completa automaticamente segun resultados oficiales</p>
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
'''
    # Insertar antes de alertas o campeones
    for marker in ['<!-- ALERTAS -->', '<!-- CAMPEONES -->', '</body>']:
        if marker in html:
            html = html.replace(marker, EMP_PAGE + marker, 1)
            print(f"Page emparejamiento insertada OK (antes de {marker})")
            break
else:
    print("Page emparejamiento ya existe OK")

# ============================================================
# 3. JS - reemplazar función renderEmparejamiento
# ============================================================
EMP_JS_V2 = '''
// ============================================================
// EMPAREJAMIENTO V2 - AUTOMATICO desde REAL_MATCHES
// ============================================================
function empGetKOMatches(){
  var stages = {r32:[],r16:[],qf:[],sf:[],tp:null,final:null};
  REAL_MATCHES.forEach(function(m){
    var s = m.stage||'';
    if(s==='Dieciseisavos') stages.r32.push(m);
    else if(s==='Octavos') stages.r16.push(m);
    else if(s==='Cuartos') stages.qf.push(m);
    else if(s==='Semifinales') stages.sf.push(m);
    else if(s==='Tercer Puesto') stages.tp=m;
    else if(s==='Final') stages.final=m;
  });
  function byNum(a,b){return (a.num||0)-(b.num||0);}
  stages.r32.sort(byNum); stages.r16.sort(byNum);
  stages.qf.sort(byNum); stages.sf.sort(byNum);
  return stages;
}

function empIsLiveM(m){
  if(m.ga!==null||!m.dateRaw||!m.time) return false;
  var now=new Date(), utc=now.getTime()+(now.getTimezoneOffset()*60000);
  var py=new Date(utc-(4*3600000));
  var todayRaw=py.getFullYear()+'-'+String(py.getMonth()+1).padStart(2,'0')+'-'+String(py.getDate()).padStart(2,'0');
  if(m.dateRaw!==todayRaw) return false;
  var parts=m.time.split(':');
  var startMin=parseInt(parts[0])*60+parseInt(parts[1]);
  var nowMin=py.getHours()*60+py.getMinutes();
  var diff=nowMin-startMin;
  return diff>=0&&diff<=150;
}

function empRenderMatchAuto(m){
  if(!m) return '<div class="emp-match tbd"><div style="font-size:10px;color:#5E6FA8;padding:4px">Por definir</div></div>';
  var isPy=(m.a==='Paraguay'||m.b==='Paraguay');
  var isLive=empIsLiveM(m);
  var hasResult=m.ga!==null&&m.gb!==null;
  var nameA=m.a||'Por definir'; var nameB=m.b||'Por definir';
  nameA=nameA.replace(/^W([0-9]+)$/,'Gan. M$1').replace(/^L([0-9]+)$/,'Per. M$1');
  nameB=nameB.replace(/^W([0-9]+)$/,'Gan. M$1').replace(/^L([0-9]+)$/,'Per. M$1');
  function flag(name){
    if(typeof TF==='undefined'||typeof FH==='undefined') return '';
    var tf=TF[name]; if(!tf) return ''; return FH(tf.c,tf.d,16,11);
  }
  var winA=hasResult&&m.ga>m.gb; var winB=hasResult&&m.gb>m.ga;
  var colorA=hasResult?(winA?'#0a1f6e':'#999'):'#1a2b5c';
  var colorB=hasResult?(winB?'#0a1f6e':'#999'):'#1a2b5c';
  var fwA=winA?'900':'600'; var fwB=winB?'900':'600';
  if(!hasResult){colorA='#1a2b5c';colorB='#1a2b5c';fwA='700';fwB='700';}
  var border=isPy?'1.5px solid #E53935':(isLive?'1.5px solid #FF9800':(hasResult?'1px solid #DCE0EC':'1px dashed #C7D2F0'));
  var bg=isPy?'#FFF6F5':(isLive?'#FFF8E1':(hasResult?'#fff':'#F0F4FF'));
  var liveTag=isLive?'<span style="font-size:8px;background:#FF9800;color:#fff;padding:1px 4px;border-radius:3px;margin-left:4px">EN VIVO</span>':'';
  var scoreA=hasResult?'<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+m.ga+'</span>':'';
  var scoreB=hasResult?'<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+m.gb+'</span>':'';
  return '<div class="emp-match" style="background:'+bg+';border:'+border+';margin-bottom:6px">'
    +'<div style="display:flex;align-items:center;justify-content:space-between;gap:4px;padding:2px 0">'
      +'<div style="display:flex;align-items:center;gap:4px;flex:1;overflow:hidden">'+flag(nameA)
        +'<span style="font-size:12px;font-weight:'+fwA+';color:'+colorA+';white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+nameA+'</span>'+liveTag
      +'</div>'+scoreA
    +'</div>'
    +'<div style="display:flex;align-items:center;justify-content:space-between;gap:4px;padding:2px 0">'
      +'<div style="display:flex;align-items:center;gap:4px;flex:1;overflow:hidden">'+flag(nameB)
        +'<span style="font-size:12px;font-weight:'+fwB+';color:'+colorB+';white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+nameB+'</span>'
      +'</div>'+scoreB
    +'</div>'
    +'<div style="font-size:9px;color:#A6ACC4;margin-top:3px">'+(m.num?'M'+m.num:'')+(m.date?' · '+m.date:'')+'</div>'
    +'</div>';
}

function renderEmparejamiento(){
  var container=document.getElementById('empBracketContainer');
  var subtitle=document.getElementById('empSubtitle');
  if(!container) return;
  var stages=empGetKOMatches();
  var jugados=stages.r32.filter(function(m){return m.ga!==null;}).length
    +stages.r16.filter(function(m){return m.ga!==null;}).length
    +stages.qf.filter(function(m){return m.ga!==null;}).length
    +stages.sf.filter(function(m){return m.ga!==null;}).length;
  if(subtitle){
    subtitle.textContent=jugados>0?'Resultados en tiempo real · '+jugados+' partidos eliminatorios jugados':'Se completa automaticamente segun resultados oficiales';
  }
  var html='<div class="emp-bracket-grid">';
  html+='<div><div class="emp-stage-label">DIECISEISAVOS</div>';
  (stages.r32.length>0?stages.r32:Array(16).fill(null)).forEach(function(m){html+=empRenderMatchAuto(m);});
  html+='</div>';
  html+='<div><div class="emp-stage-label">OCTAVOS</div>';
  (stages.r16.length>0?stages.r16:Array(8).fill(null)).forEach(function(m){html+=empRenderMatchAuto(m);});
  html+='</div>';
  html+='<div><div class="emp-stage-label">CUARTOS</div>';
  (stages.qf.length>0?stages.qf:Array(4).fill(null)).forEach(function(m){html+=empRenderMatchAuto(m);});
  html+='</div>';
  html+='<div><div class="emp-stage-label">SEMIFINALES</div>';
  (stages.sf.length>0?stages.sf:Array(2).fill(null)).forEach(function(m){html+=empRenderMatchAuto(m);});
  html+='<div style="margin-top:14px"><div class="emp-stage-label">TERCER PUESTO</div>';
  html+=empRenderMatchAuto(stages.tp);
  html+='</div></div>';
  html+='<div><div class="emp-stage-label">FINAL</div>';
  if(stages.final){html+=empRenderMatchAuto(stages.final);}
  else{html+='<div class="emp-final-box"><div class="lbl">19/07 · MetLife Stadium</div><div class="team">Por definir</div><div class="team">Por definir</div></div>';}
  html+='</div></div>';
  container.innerHTML=html;
  setTimeout(renderEmparejamiento,60000);
}
'''

# Reemplazar o insertar función
if 'function renderEmparejamiento' in html:
    # Buscar y reemplazar la función completa
    start = html.find('function renderEmparejamiento')
    # Encontrar el cierre de la función (buscar la llave de cierre)
    depth = 0
    i = html.find('{', start)
    while i < len(html):
        if html[i] == '{':
            depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    # Incluir el \n previo si existe
    prev_newline = html.rfind('\n', 0, start)
    if prev_newline > 0 and html[prev_newline:start].strip() == '':
        start = prev_newline
    html = html[:start] + '\n' + EMP_JS_V2.strip() + '\n' + html[end:]
    print("JS renderEmparejamiento REEMPLAZADO OK")
else:
    last_script = html.rfind('</script>')
    html = html[:last_script] + '\n' + EMP_JS_V2 + '\n' + html[last_script:]
    print("JS renderEmparejamiento INSERTADO OK")

# ============================================================
# 4. Hook showPage
# ============================================================
if "if(id==='emparejamiento')renderEmparejamiento();" in html:
    print("Hook showPage emparejamiento ya existe OK")
else:
    for old in ["if(id==='campeones')renderCampeones();",
                "if(id==='miequipo')renderMyTeam();"]:
        if old in html:
            html = html.replace(old, old + "\n  if(id==='emparejamiento')renderEmparejamiento();", 1)
            print("Hook showPage emparejamiento agregado OK")
            break

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
