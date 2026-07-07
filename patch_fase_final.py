"""
patch_fase_final.py
Agrega la pestana Fase Final al template.html con bracket visual
automatico desde REAL_MATCHES (banderas, resultados, copa central).
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. CSS
# ============================================================
CSS = '''
/* FASE FINAL */
.ff-body{padding:16px;background:#F4F5F9;overflow-x:auto}
.ff-header{background:#0B369D;border-bottom:3px solid #E53935;border-radius:10px 10px 0 0;padding:12px 20px;display:flex;align-items:center;justify-content:space-between}
.ff-title{color:#fff;font-weight:900;font-size:13px;letter-spacing:.5px}
.ff-sub{color:#B9C6E8;font-size:10px}
.ff-badge{color:#fff;font-size:10px;background:rgba(255,255,255,.15);padding:3px 10px;border-radius:20px;display:flex;align-items:center;gap:5px}
.ff-titlebar{background:#fff;padding:10px 20px;border-bottom:1px solid #E5E7EE}
.ff-titlebar h2{color:#0a1f6e;font-size:16px;font-weight:900;margin:0 0 2px}
.ff-titlebar p{color:#6B7491;font-size:11px;margin:0}
.ff-grid{display:flex;gap:6px;align-items:flex-start;min-width:1050px}
.ff-col{flex-shrink:0}
.ff-col-label{font-size:9px;font-weight:900;color:#0B369D;letter-spacing:1px;text-align:center;margin-bottom:8px}
.ff-col-label.final{color:#E53935}
.ff-match{border-radius:6px;padding:6px 8px;margin-bottom:5px}
.ff-match.confirmed{background:#fff;border:1px solid #DCE0EC}
.ff-match.tbd{background:#F0F4FF;border:1px dashed #C7D2F0}
.ff-match.py{background:#FFF6F5;border:1.5px solid #E53935}
.ff-match.live{background:#FFF8E1;border:1.5px solid #FF9800}
.ff-team{display:flex;align-items:center;gap:5px;margin-bottom:3px}
.ff-name{font-size:11px;font-weight:600;color:#1a2b5c;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ff-name.win{font-weight:700;color:#0a1f6e}
.ff-name.lose{color:#999;font-weight:500}
.ff-name.tbd-t{color:#5E6FA8;font-size:10px}
.ff-score{font-size:11px;font-weight:700;color:#E53935;flex-shrink:0}
.ff-meta{font-size:9px;color:#A6ACC4;margin-top:2px}
.ff-live-tag{font-size:8px;background:#FF9800;color:#fff;padding:1px 4px;border-radius:2px;margin-left:4px}
.ff-flag{display:inline-flex;border-radius:2px;border:1px solid rgba(0,0,0,.12);overflow:hidden;flex-shrink:0}
.ff-flag span{display:block}
.ff-final-box{background:#0B369D;border-radius:10px;padding:14px 10px;text-align:center;width:100%}
.ff-final-box .trophy{font-size:24px;margin-bottom:6px}
.ff-final-box .lbl{color:#fff;font-size:9px;font-weight:900;letter-spacing:1px;margin-bottom:8px}
.ff-final-slot{background:rgba(255,255,255,.18);border-radius:5px;padding:5px 6px;margin-bottom:4px}
.ff-final-slot span{color:#fff;font-size:11px;font-weight:700}
.ff-vs{color:rgba(255,255,255,.4);font-size:9px;margin:3px 0;display:block;text-align:center}
.ff-date{color:#B9C6E8;font-size:8px;display:block;margin-top:4px}
.ff-3rd{background:#fff;border:1px dashed #C7D2F0;border-radius:6px;padding:7px 8px;text-align:center}
.ff-3rd-lbl{font-size:8px;color:#6B7491;font-weight:900;letter-spacing:1px;text-align:center;margin-bottom:5px}
.ff-legend{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:10px;flex-wrap:wrap;padding-bottom:4px}
.ff-legend-item{display:flex;align-items:center;gap:5px;font-size:10px;color:#6B7491}
.ff-legend-dot{width:10px;height:10px;border-radius:2px;display:inline-block}
@media(max-width:700px){.ff-body{padding:8px}}
'''

if '/* FASE FINAL */' not in html:
    html = html.replace('</style>', CSS + '</style>', 1)
    print("CSS Fase Final agregado OK")
else:
    print("CSS Fase Final ya existe OK")

# ============================================================
# 2. NAV TAB
# ============================================================
if "showPage('fasefinal'" not in html:
    m = re.search(r'<button[^>]*onclick=["\']showPage\(\'emparejamiento\'[^>]*>.*?</button>', html, re.DOTALL)
    if m:
        old = m.group(0)
        new = old + '\n      <button class="nav-tab" onclick="showPage(\'fasefinal\',this)">&#x1F3C6; Fase Final</button>'
        html = html.replace(old, new, 1)
        print("Nav tab Fase Final agregado OK")
    else:
        m2 = re.search(r'<button[^>]*onclick=["\']showPage\(\'miequipo\'[^>]*>.*?</button>', html, re.DOTALL)
        if m2:
            old = m2.group(0)
            new = '<button class="nav-tab" onclick="showPage(\'fasefinal\',this)">&#x1F3C6; Fase Final</button>\n      ' + old
            html = html.replace(old, new, 1)
            print("Nav tab Fase Final agregado OK (fallback Mi Equipo)")
        else:
            print("WARNING: no se encontro punto de insercion para nav tab Fase Final")
else:
    print("Nav tab Fase Final ya existe OK")

# ============================================================
# 3. PAGE HTML
# ============================================================
FF_PAGE = '''
  <!-- FASE FINAL -->
  <div id="page-fasefinal" class="page">
    <div>
      <div class="ff-header">
        <div>
          <div class="ff-title">VERING &middot; FASE FINAL</div>
          <div class="ff-sub">Mundial 2026 &middot; 16avos &rarr; Final</div>
        </div>
        <div class="ff-badge"><span style="width:6px;height:6px;border-radius:50%;background:#4ADE80;display:inline-block"></span>Auto-actualizado</div>
      </div>
      <div class="ff-titlebar">
        <h2>Fase final</h2>
        <p id="ffSubtitle">Cargando resultados...</p>
      </div>
      <div class="ff-body">
        <div class="ff-grid" id="ffBracketContainer"></div>
        <div class="ff-legend">
          <div class="ff-legend-item"><span class="ff-legend-dot" style="background:#fff;border:1px solid #DCE0EC"></span>Confirmado</div>
          <div class="ff-legend-item"><span class="ff-legend-dot" style="background:#F0F4FF;border:1px dashed #C7D2F0"></span>Por definir</div>
          <div class="ff-legend-item"><span class="ff-legend-dot" style="background:#FFF6F5;border:1px solid #E53935"></span>Paraguay</div>
          <div class="ff-legend-item"><span class="ff-legend-dot" style="background:#FFF8E1;border:1px solid #FF9800"></span>En vivo</div>
        </div>
      </div>
    </div>
  </div>

'''

if 'id="page-fasefinal"' not in html:
    for marker in ['<!-- ALERTAS -->', '<!-- CAMPEONES -->', '<!-- EMPAREJAMIENTO -->', '</body>']:
        if marker in html:
            html = html.replace(marker, FF_PAGE + marker, 1)
            print(f"Page Fase Final insertada OK (antes de {marker})")
            break
else:
    print("Page Fase Final ya existe OK")

# ============================================================
# 4. JS
# ============================================================
FF_JS = '''
// ============================================================
// FASE FINAL - Bracket visual automatico desde REAL_MATCHES
// ============================================================
const FF_FLAGS = {
  'Sudáfrica':     {c:['#007A4D','#FFB81C','#001489'],d:'h'},
  'Canadá':        {c:['#FF0000','#fff','#FF0000'],d:'h'},
  'Alemania':      {c:['#000','#DD0000','#FFCE00'],d:'h'},
  'Paraguay':      {c:['#D52B1E','#fff','#0038A8'],d:'h'},
  'Países Bajos':  {c:['#AE1C28','#fff','#21468B'],d:'h'},
  'Marruecos':     {c:['#C1272D','#006233','#C1272D'],d:'h'},
  'Noruega':       {c:['#EF2B2D','#fff','#002868'],d:'v'},
  'Costa de Marfil':{c:['#FF8200','#fff','#009E60'],d:'v'},
  'Francia':       {c:['#002395','#fff','#ED2939'],d:'v'},
  'Suecia':        {c:['#006AA7','#FECC00','#006AA7'],d:'h'},
  'Bélgica':       {c:['#000','#FAE042','#ED2939'],d:'v'},
  'Senegal':       {c:['#00853F','#FDEF42','#E31B23'],d:'v'},
  'Estados Unidos':{c:['#B22234','#fff','#3C3B6E'],d:'h'},
  'Bosnia':        {c:['#002395','#FFD700','#fff'],d:'h'},
  'España':        {c:['#AA151B','#F1BF00','#AA151B'],d:'h'},
  'Austria':       {c:['#ED2939','#fff','#ED2939'],d:'h'},
  'Brasil':        {c:['#009C3B','#FDEF42','#009C3B'],d:'h'},
  'Japón':         {c:['#fff','#BC002D','#fff'],d:'h'},
  'Portugal':      {c:['#006600','#FF0000','#FF0000'],d:'v'},
  'Croacia':       {c:['#FF0000','#fff','#171796'],d:'h'},
  'Suiza':         {c:['#FF0000','#fff','#FF0000'],d:'h'},
  'Argelia':       {c:['#006233','#fff','#D21034'],d:'v'},
  'Australia':     {c:['#00008B','#CC0000','#00008B'],d:'h'},
  'Egipto':        {c:['#CE1126','#fff','#000'],d:'h'},
  'Argentina':     {c:['#74ACDF','#fff','#74ACDF'],d:'h'},
  'Cabo Verde':    {c:['#003893','#CF2027','#003893'],d:'h'},
  'Colombia':      {c:['#FCD116','#003087','#CE1126'],d:'h'},
  'Ghana':         {c:['#006B3F','#FCD116','#CE1126'],d:'v'},
  'México':        {c:['#006847','#fff','#CE1126'],d:'v'},
  'Ecuador':       {c:['#FFD100','#003DA5','#CE1126'],d:'h'},
  'Inglaterra':    {c:['#CF142B','#fff','#CF142B'],d:'h'},
  'RD Congo':      {c:['#007FFF','#CE1126','#F7D618'],d:'h'},
  'Corea del Sur': {c:['#fff','#CD2E3A','#fff'],d:'h'},
  'Uruguay':       {c:['#fff','#5bcfed','#0038A8'],d:'h'},
};

function ffFlag(name, w, h){
  var f = FF_FLAGS[name];
  if(!f) return '<span class="ff-flag" style="width:'+w+'px;height:'+h+'px;background:#ddd"></span>';
  var dir = f.d==='v'?'row':'column';
  var parts = f.c.map(function(c){return '<span style="flex:1;background:'+c+'"></span>';}).join('');
  return '<span class="ff-flag" style="width:'+w+'px;height:'+h+'px;flex-direction:'+dir+'">'+parts+'</span>';
}

function ffIsLive(m){
  if(m.ga!==null||!m.dateRaw||!m.time) return false;
  var now=new Date(), utc=now.getTime()+(now.getTimezoneOffset()*60000);
  var py=new Date(utc-(4*3600000));
  var today=py.getFullYear()+'-'+String(py.getMonth()+1).padStart(2,'0')+'-'+String(py.getDate()).padStart(2,'0');
  if(m.dateRaw!==today) return false;
  var parts=m.time.split(':');
  var start=parseInt(parts[0])*60+parseInt(parts[1]);
  var now2=py.getHours()*60+py.getMinutes();
  return now2-start>=0 && now2-start<=150;
}

function ffMatchBox(m){
  if(!m) return '<div class="ff-match tbd"><div class="ff-name tbd-t">Por definir</div></div>';
  var isPy=(m.a==='Paraguay'||m.b==='Paraguay');
  var isLive=ffIsLive(m);
  var hasScore=m.ga!==null&&m.gb!==null;
  var isTbd=!m.a||!m.b||/^[W2][0-9]/.test(m.a||'')||/^[W2][0-9]/.test(m.b||'');
  var cls='ff-match '+(isPy?'py':isLive?'live':isTbd?'tbd':'confirmed');
  var nameA=(m.a||'Por definir').replace(/^W([0-9]+)$/,'Gan. M$1').replace(/^L([0-9]+)$/,'Per. M$1');
  var nameB=(m.b||'Por definir').replace(/^W([0-9]+)$/,'Gan. M$1').replace(/^L([0-9]+)$/,'Per. M$1');
  var winA=hasScore&&m.ga>m.gb, winB=hasScore&&m.gb>m.ga;
  var clsA=isTbd?'tbd-t':hasScore?(winA?'win':'lose'):'';
  var clsB=isTbd?'tbd-t':hasScore?(winB?'win':'lose'):'';
  var sA=hasScore?'<span class="ff-score">'+m.ga+'</span>':'';
  var sB=hasScore?'<span class="ff-score">'+m.gb+'</span>':'';
  var liveTag=isLive?'<span class="ff-live-tag">EN VIVO</span>':'';
  return '<div class="'+cls+'">'
    +'<div class="ff-team">'+ffFlag(nameA,18,12)+'<span class="ff-name '+clsA+'">'+nameA+'</span>'+liveTag+sA+'</div>'
    +'<div class="ff-team">'+ffFlag(nameB,18,12)+'<span class="ff-name '+clsB+'">'+nameB+'</span>'+sB+'</div>'
    +'<div class="ff-meta">'+(m.num?'M'+m.num:'')+(m.date?' · '+m.date:'')+'</div>'
    +'</div>';
}

function ffTbd(meta){
  return '<div class="ff-match tbd"><div class="ff-name tbd-t">Por definir</div><div class="ff-name tbd-t">Por definir</div><div class="ff-meta">'+meta+'</div></div>';
}

function renderFaseFinal(){
  var container=document.getElementById('ffBracketContainer');
  var subtitle=document.getElementById('ffSubtitle');
  if(!container) return;

  var stages={r32:[],r16:[],qf:[],sf:[],tp:null,final:null};
  REAL_MATCHES.forEach(function(m){
    var s=m.stage||'';
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

  var jugados=stages.r32.filter(function(m){return m.ga!==null;}).length
    +stages.r16.filter(function(m){return m.ga!==null;}).length
    +stages.qf.filter(function(m){return m.ga!==null;}).length
    +stages.sf.filter(function(m){return m.ga!==null;}).length;

  if(subtitle) subtitle.textContent=jugados>0?'Resultados en tiempo real · '+jugados+' partidos eliminatorios jugados':'Cargando resultados...';

  var LEFT32=stages.r32.slice(0,8);
  var RIGHT32=stages.r32.slice(8,16);
  var LEFT16=stages.r16.slice(0,4);
  var RIGHT16=stages.r16.slice(4,8);
  var LEFTQF=stages.qf.slice(0,2);
  var RIGHTQF=stages.qf.slice(2,4);
  var LEFTSF=stages.sf[0]||null;
  var RIGHTSF=stages.sf[1]||null;

  function col32(matches){
    var h='<div class="ff-col" style="width:168px">';
    h+='<div class="ff-col-label">16AVOS</div>';
    for(var i=0;i<8;i++) h+=ffMatchBox(matches[i]||null);
    h+='</div>';
    return h;
  }

  function col16(matches, spacers){
    var h='<div class="ff-col" style="width:132px">';
    h+='<div class="ff-col-label">OCTAVOS</div>';
    h+='<div style="height:28px"></div>';
    for(var i=0;i<4;i++){
      h+=ffMatchBox(matches[i]||null);
      if(i<3) h+='<div style="height:58px"></div>';
    }
    h+='</div>';
    return h;
  }

  function colQF(matches){
    var h='<div class="ff-col" style="width:112px">';
    h+='<div class="ff-col-label">CUARTOS</div>';
    h+='<div style="height:78px"></div>';
    h+=ffMatchBox(matches[0]||null);
    h+='<div style="height:148px"></div>';
    h+=ffMatchBox(matches[1]||null);
    h+='</div>';
    return h;
  }

  function colSF(match, meta){
    var h='<div class="ff-col" style="width:82px">';
    h+='<div class="ff-col-label">SEMIS</div>';
    h+='<div style="height:175px"></div>';
    h+=match?ffMatchBox(match):ffTbd(meta);
    h+='</div>';
    return h;
  }

  // Final central
  var finalA=stages.final?stages.final.a:'Por definir';
  var finalB=stages.final?stages.final.b:'Por definir';
  var finalGa=stages.final&&stages.final.ga!==null?stages.final.ga:'';
  var finalGb=stages.final&&stages.final.gb!==null?stages.final.gb:'';
  var tp3A=stages.tp?stages.tp.a:'Por definir';
  var tp3B=stages.tp?stages.tp.b:'Por definir';
  var hasFinal=stages.final&&stages.final.ga!==null;

  var finalSlotA=hasFinal
    ?'<div class="ff-final-slot">'+ffFlag(finalA,16,11)+'<span style="margin-left:5px">'+finalA+'</span><span style="margin-left:auto;font-size:12px;font-weight:900">'+finalGa+'</span></div>'
    :'<div class="ff-final-slot"><span>'+finalA+'</span></div>';
  var finalSlotB=hasFinal
    ?'<div class="ff-final-slot">'+ffFlag(finalB,16,11)+'<span style="margin-left:5px">'+finalB+'</span><span style="margin-left:auto;font-size:12px;font-weight:900">'+finalGb+'</span></div>'
    :'<div class="ff-final-slot"><span>'+finalB+'</span></div>';

  var centerCol='<div class="ff-col" style="width:112px;display:flex;flex-direction:column;align-items:center">'
    +'<div class="ff-col-label final">FINAL</div>'
    +'<div style="height:148px"></div>'
    +'<div class="ff-final-box">'
      +'<div class="trophy">&#x1F3C6;</div>'
      +'<div class="lbl">FINAL MUNDIAL</div>'
      +finalSlotA
      +'<span class="ff-vs">vs</span>'
      +finalSlotB
      +'<span class="ff-date">19/07 &middot; MetLife Stadium</span>'
    +'</div>'
    +'<div style="height:10px"></div>'
    +'<div class="ff-3rd-lbl">3er PUESTO</div>'
    +'<div class="ff-3rd">'
      +'<div style="font-size:10px;color:#5E6FA8">'+tp3A+'</div>'
      +'<div style="font-size:10px;color:#5E6FA8">'+tp3B+'</div>'
      +'<div style="font-size:9px;color:#A6ACC4;margin-top:2px">18 Jul &middot; Miami</div>'
    +'</div>'
    +'</div>';

  container.innerHTML=
    col32(LEFT32)+
    col16(LEFT16)+
    colQF(LEFTQF)+
    colSF(LEFTSF,'14 Jul')+
    centerCol+
    colSF(RIGHTSF,'15 Jul')+
    colQF(RIGHTQF)+
    col16(RIGHT16)+
    col32(RIGHT32);

  setTimeout(renderFaseFinal, 60000);
}
'''

if 'function renderFaseFinal' in html:
    print("JS renderFaseFinal ya existe, reemplazando...")
    start = html.find('function renderFaseFinal')
    depth = 0
    i = html.find('{', start)
    while i < len(html):
        if html[i] == '{': depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    html = html[:start] + FF_JS.strip() + '\n' + html[end:]
    print("JS renderFaseFinal reemplazado OK")
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + '\n' + FF_JS + '\n' + html[last_script:]
        print("JS renderFaseFinal insertado OK")

# ============================================================
# 5. Hook showPage
# ============================================================
if "if(id==='fasefinal')renderFaseFinal();" not in html:
    for old in ["if(id==='emparejamiento')renderEmparejamiento();",
                "if(id==='campeones')renderCampeones();",
                "if(id==='miequipo')renderMyTeam();"]:
        if old in html:
            html = html.replace(old, old + "\n  if(id==='fasefinal')renderFaseFinal();", 1)
            print("Hook showPage Fase Final agregado OK")
            break

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
print("Ahora correr: python3 build.py")
