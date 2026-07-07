"""
patch_emparejamiento_v2.py
Reemplaza patch_emparejamiento.py con version que lee REAL_MATCHES directamente.
El bracket se actualiza automaticamente cuando openfootball carga nuevos resultados.
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# CSS (solo agregar si no existe)
CSS = '''
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
.emp-match.live{background:#FFF8E1;border:1.5px solid #FF9800}
.emp-team-row{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:700;color:#1a2b5c;padding:2px 0}
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
'''

if '/* EMPAREJAMIENTO */' not in html:
    html = html.replace('</style>', CSS + '</style>', 1)
    print("CSS emparejamiento agregado OK")
else:
    print("CSS emparejamiento ya existe OK")

# JS principal - lee REAL_MATCHES automaticamente
EMP_JS_V2 = '''
// ============================================================
// EMPAREJAMIENTO V2 - AUTOMATICO desde REAL_MATCHES
// Lee los 104 partidos directamente, sin datos hardcodeados
// ============================================================

function empGetKOMatches(){
  // Filtrar partidos eliminatorios de REAL_MATCHES
  var stages = {
    r32: [], r16: [], qf: [], sf: [], tp: null, final: null
  };
  REAL_MATCHES.forEach(function(m){
    var s = m.stage || '';
    if(s === 'Dieciseisavos') stages.r32.push(m);
    else if(s === 'Octavos') stages.r16.push(m);
    else if(s === 'Cuartos') stages.qf.push(m);
    else if(s === 'Semifinales') stages.sf.push(m);
    else if(s === 'Tercer Puesto') stages.tp = m;
    else if(s === 'Final') stages.final = m;
  });
  // Ordenar por num de partido
  function byNum(a,b){ return (a.num||0)-(b.num||0); }
  stages.r32.sort(byNum);
  stages.r16.sort(byNum);
  stages.qf.sort(byNum);
  stages.sf.sort(byNum);
  return stages;
}

function empIsLive(m){
  if(m.ga !== null || !m.dateRaw || !m.time) return false;
  var now = new Date();
  var utc = now.getTime() + (now.getTimezoneOffset()*60000);
  var py = new Date(utc - (4*3600000));
  var todayRaw = py.getFullYear()+'-'+String(py.getMonth()+1).padStart(2,'0')+'-'+String(py.getDate()).padStart(2,'0');
  if(m.dateRaw !== todayRaw) return false;
  var parts = m.time.split(':');
  var startMin = parseInt(parts[0])*60 + parseInt(parts[1]);
  var nowMin = py.getHours()*60 + py.getMinutes();
  var diff = nowMin - startMin;
  return diff >= 0 && diff <= 150;
}

function empRenderMatchAuto(m, stageLabel){
  if(!m) return '<div class="emp-match tbd"><div style="font-size:10px;color:#5E6FA8;padding:4px">Por definir</div></div>';
  var isPy = (m.a === 'Paraguay' || m.b === 'Paraguay');
  var isLive = empIsLive(m);
  var hasResult = m.ga !== null && m.gb !== null;
  var isTbd = !m.a || !m.b || m.a.match(/^[W2]\d+/) || m.b.match(/^[W2][0-9]+/);
  var cls = 'emp-match' + (isPy?' py':(isLive?' live':(isTbd?' tbd':'')));
  var nameA = m.a || 'Por definir';
  var nameB = m.b || 'Por definir';
  // Traducir placeholders
  nameA = nameA.replace(/^W([0-9]+)$/, 'Gan. M$1').replace(/^L([0-9]+)$/, 'Per. M$1');
  nameB = nameB.replace(/^W(\d+)$/, 'Gan. M$1').replace(/^L(\d+)$/, 'Per. M$1');
  function flag(name){
    if(typeof TF==='undefined'||typeof FH==='undefined') return '';
    var tf = TF[name]; if(!tf) return '';
    return FH(tf.c, tf.d, 16, 11);
  }
  var winA = hasResult && m.ga > m.gb;
  var winB = hasResult && m.gb > m.ga;
  var colorA = hasResult?(winA?'#0a1f6e':'#999'):'#1a2b5c';
  var colorB = hasResult?(winB?'#0a1f6e':'#999'):'#1a2b5c';
  var fwA = winA?'900':'600'; var fwB = winB?'900':'600';
  if(!hasResult){colorA='#1a2b5c';colorB='#1a2b5c';fwA='700';fwB='700';}
  var scoreA = hasResult ? '<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+m.ga+'</span>' : '';
  var scoreB = hasResult ? '<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+m.gb+'</span>' : '';
  var liveTag = isLive ? '<span style="font-size:8px;background:#FF9800;color:#fff;padding:1px 4px;border-radius:3px;margin-left:4px">EN VIVO</span>' : '';
  return '<div class="'+cls+'">'
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
    +'<div class="emp-match-meta">'+(m.num?'M'+m.num:'')+(m.date?' · '+m.date:'')+'</div>'
    +'</div>';
}

function renderEmparejamiento(){
  var container = document.getElementById('empBracketContainer');
  var subtitle = document.getElementById('empSubtitle');
  if(!container) return;

  var stages = empGetKOMatches();
  var jugados = stages.r32.filter(function(m){return m.ga!==null;}).length
              + stages.r16.filter(function(m){return m.ga!==null;}).length
              + stages.qf.filter(function(m){return m.ga!==null;}).length
              + stages.sf.filter(function(m){return m.ga!==null;}).length;

  if(subtitle){
    if(jugados > 0){
      subtitle.textContent = 'Resultados en tiempo real · ' + jugados + ' partidos eliminatorios jugados';
    } else {
      subtitle.textContent = 'Se completa automaticamente segun resultados oficiales';
    }
  }

  var html = '<div class="emp-bracket-grid">';

  // DIECISEISAVOS
  html += '<div><div class="emp-stage-label">DIECISEISAVOS</div>';
  if(stages.r32.length > 0){
    stages.r32.forEach(function(m){ html += empRenderMatchAuto(m); });
  } else {
    for(var i=0;i<16;i++) html += empRenderMatchAuto(null);
  }
  html += '</div>';

  // OCTAVOS
  html += '<div><div class="emp-stage-label">OCTAVOS</div>';
  if(stages.r16.length > 0){
    stages.r16.forEach(function(m){ html += empRenderMatchAuto(m); });
  } else {
    for(var i=0;i<8;i++) html += empRenderMatchAuto(null);
  }
  html += '</div>';

  // CUARTOS
  html += '<div><div class="emp-stage-label">CUARTOS</div>';
  if(stages.qf.length > 0){
    stages.qf.forEach(function(m){ html += empRenderMatchAuto(m); });
  } else {
    for(var i=0;i<4;i++) html += empRenderMatchAuto(null);
  }
  html += '</div>';

  // SEMIS + TERCER PUESTO
  html += '<div><div class="emp-stage-label">SEMIFINALES</div>';
  if(stages.sf.length > 0){
    stages.sf.forEach(function(m){ html += empRenderMatchAuto(m); });
  } else {
    html += empRenderMatchAuto(null);
    html += empRenderMatchAuto(null);
  }
  html += '<div style="margin-top:14px"><div class="emp-stage-label">TERCER PUESTO</div>';
  html += empRenderMatchAuto(stages.tp);
  html += '</div></div>';

  // FINAL
  html += '<div><div class="emp-stage-label">FINAL</div>';
  if(stages.final){
    html += empRenderMatchAuto(stages.final);
  } else {
    html += '<div class="emp-final-box"><div class="lbl">19/07 · MetLife Stadium</div><div class="team">Por definir</div><div class="team">Por definir</div></div>';
  }
  html += '</div>';

  html += '</div>';
  container.innerHTML = html;
  // Refrescar cada 60 segundos
  setTimeout(renderEmparejamiento, 60000);
}
'''

# Insertar o reemplazar JS
if 'function renderEmparejamiento' in html:
    # Reemplazar funcion existente
    start = html.find('\nfunction renderEmparejamiento()')
    if start == -1:
        start = html.find('function renderEmparejamiento()')
    end = html.find('\n}\n', start) + 3
    if start > 0 and end > 3:
        html = html[:start] + '\n' + EMP_JS_V2.strip() + '\n' + html[end:]
        print("JS renderEmparejamiento REEMPLAZADO OK")
    else:
        last_script = html.rfind('</script>')
        html = html[:last_script] + '\n' + EMP_JS_V2 + '\n' + html[last_script:]
        print("JS renderEmparejamiento insertado OK (fallback)")
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + '\n' + EMP_JS_V2 + '\n' + html[last_script:]
        print("JS renderEmparejamiento insertado OK")

# Asegurar hook showPage
if "if(id==='emparejamiento')renderEmparejamiento();" not in html:
    for old in [
        "if(id==='emparejamiento')empRenderBracketReal();",
        "if(id==='miequipo')renderMyTeam();"
    ]:
        if old in html:
            html = html.replace(old, old + "\n  if(id==='emparejamiento')renderEmparejamiento();", 1)
            print("Hook showPage agregado OK")
            break

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
print("Ahora correr: python3 build.py")
