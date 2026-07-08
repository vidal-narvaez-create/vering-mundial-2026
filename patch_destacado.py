"""
patch_destacado.py
Actualizado: prioridad correcta para fase eliminatoria
1) En vivo -> 2) Cuartos/Semis/Final del dia -> 3) Paraguay -> 4) Top team -> 5) Fallback
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

JS_DESTACADO = '''
// ============================================================
// PARTIDO DESTACADO DEL DIA (splash) - v3
// Prioridad: 1)En vivo 2)KO del dia 3)Paraguay hoy 4)Top team 5)Fallback
// ============================================================
const TOP_TEAMS_DESTACADO=['Brasil','Argentina','Francia','Alemania','España','Inglaterra','Portugal','Países Bajos','Marruecos','Noruega','Bélgica','Suiza'];
const KO_STAGES=['Dieciseisavos','Octavos','Cuartos','Semifinales','Tercer Puesto','Final'];

function pyTodayRaw(){
  var now=new Date();
  var utc=now.getTime()+(now.getTimezoneOffset()*60000);
  var py=new Date(utc-(4*3600000));
  var dd=py.getDate(), mm=py.getMonth()+1, yyyy=py.getFullYear();
  return yyyy+'-'+String(mm).padStart(2,'0')+'-'+String(dd).padStart(2,'0');
}

function isMatchLive(m){
  if(m.ga!==null) return false;
  if(!m.time||!m.dateRaw) return false;
  var todayRaw=pyTodayRaw();
  if(m.dateRaw!==todayRaw) return false;
  var now=new Date();
  var utc=now.getTime()+(now.getTimezoneOffset()*60000);
  var py=new Date(utc-(4*3600000));
  var nowMin=py.getHours()*60+py.getMinutes();
  var parts=m.time.split(':');
  var startMin=parseInt(parts[0])*60+parseInt(parts[1]);
  var diff=nowMin-startMin;
  return diff>=0 && diff<=150;
}

function getPartidoDestacado(){
  var todayRaw=pyTodayRaw();
  var todayMatches=REAL_MATCHES.filter(function(m){return m.dateRaw===todayRaw;});

  // 1) En vivo
  var live=REAL_MATCHES.find(function(m){return isMatchLive(m);});
  if(live) return {match:live,label:'🔴 EN VIVO',tag:'live'};

  // 2) Partido KO del dia (cuartos, semis, final) - prioritario sobre Paraguay
  var koToday=todayMatches.filter(function(m){return KO_STAGES.indexOf(m.stage||'')!==-1;});
  if(koToday.length>0){
    return {match:koToday[0],label:'PARTIDO DESTACADO DEL DÍA',tag:'ko'};
  }

  // 3) Paraguay juega hoy
  var pyHoy=todayMatches.find(function(m){return m.a==='Paraguay'||m.b==='Paraguay';});
  if(pyHoy) return {match:pyHoy,label:'PARTIDO DE PARAGUAY · HOY',tag:'paraguay'};

  // 4) Top team hoy
  if(todayMatches.length>0){
    var topM=todayMatches.find(function(m){
      return TOP_TEAMS_DESTACADO.indexOf(m.a)!==-1||TOP_TEAMS_DESTACADO.indexOf(m.b)!==-1;
    });
    var pick=topM||todayMatches[0];
    return {match:pick,label:'PARTIDO DESTACADO DEL DÍA',tag:'destacado'};
  }

  // 5) Proximo partido KO (dia de descanso sin partidos hoy: prioriza esto sobre resultados viejos)
  var koUpcoming=REAL_MATCHES.filter(function(m){return m.ga===null&&KO_STAGES.indexOf(m.stage||'')!==-1;})
    .sort(function(a,b){return (a.dateRaw||'').localeCompare(b.dateRaw||'');});
  if(koUpcoming.length>0){
    return {match:koUpcoming[0],label:'PRÓXIMO PARTIDO · '+(koUpcoming[0].stage||'ELIMINATORIA').toUpperCase(),tag:'next-ko'};
  }

  // 6) Ultimo resultado KO de Paraguay
  var pyKOPlayed=REAL_MATCHES.filter(function(m){
    return (m.a==='Paraguay'||m.b==='Paraguay')&&m.ga!==null&&KO_STAGES.indexOf(m.stage||'')!==-1;
  });
  if(pyKOPlayed.length>0){
    return {match:pyKOPlayed[pyKOPlayed.length-1],label:'ÚLTIMO RESULTADO · PARAGUAY',tag:'last-py'};
  }

  // 7) Ultimo resultado de Paraguay (cualquier fase)
  var pyPlayed=REAL_MATCHES.filter(function(m){return (m.a==='Paraguay'||m.b==='Paraguay')&&m.ga!==null;});
  if(pyPlayed.length>0){
    return {match:pyPlayed[pyPlayed.length-1],label:'ÚLTIMO RESULTADO · PARAGUAY',tag:'last-py'};
  }

  // 8) Fallback ultimo jugado
  var anyPlayed=REAL_MATCHES.filter(function(m){return m.ga!==null;});
  if(anyPlayed.length>0){
    return {match:anyPlayed[anyPlayed.length-1],label:'ÚLTIMO RESULTADO',tag:'last-any'};
  }
  return null;
}

function renderSplashDestacado(){
  var lblEl=document.getElementById('spMcLbl');
  var rowEl=document.getElementById('spMcRow');
  if(!lblEl||!rowEl) return;
  var res=getPartidoDestacado();
  if(!res){
    lblEl.textContent='PARTIDO DESTACADO';
    rowEl.innerHTML='<span style="color:rgba(255,255,255,.5)">Sin datos disponibles</span>';
    return;
  }
  var m=res.match;
  lblEl.textContent=res.label+(m.g?' · GRUPO '+m.g:'');

  var scoreHtml;
  if(res.tag==='live'){
    scoreHtml='<span class="sp-sc" style="background:rgba(229,57,53,.25);color:#fff">VS</span>';
  } else if(m.ga!==null){
    scoreHtml='<span class="sp-sc">'+m.ga+' - '+m.gb+'</span>';
  } else {
    scoreHtml='<span class="sp-sc" style="font-size:13px">'+(m.time||'--:--')+'</span>';
  }

  rowEl.innerHTML=
    '<span class="sp-mn">'+m.a+'</span>'
    +'<span class="sp-mvs">vs</span>'
    +scoreHtml
    +'<span class="sp-mvs">vs</span>'
    +'<span class="sp-mn" style="text-align:right">'+m.b+'</span>';
}
'''

if 'function getPartidoDestacado' in html:
    # Reemplazar funcion existente
    start = html.find('// ============================================================\n// PARTIDO DESTACADO')
    if start == -1:
        start = html.find('function pyTodayRaw')
    end = html.find('\nrenderSplashDestacado();\nsetInterval', start)
    if end == -1:
        end = html.find('\nfunction renderSplashDestacado', start)
        end2 = html.find('\n}\n', end) + 3
        html = html[:start] + JS_DESTACADO.strip() + '\n' + html[end2:]
    else:
        html = html[:start] + JS_DESTACADO.strip() + '\n' + html[end:]
    print("JS destacado ACTUALIZADO OK")
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + JS_DESTACADO + '\n' + html[last_script:]
        print("JS destacado INSERTADO OK")

if 'renderSplashDestacado();' not in html:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + "\nrenderSplashDestacado();\nsetInterval(renderSplashDestacado, 60000);\n" + html[last_script:]
        print("Llamada a renderSplashDestacado() agregada OK")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")

