"""
patch_destacado.py
Ejecutar en la raiz del repo: python3 patch_destacado.py
Lee template.html, reemplaza la logica del "Partido Destacado" del splash
(antes: fijo en ultimo resultado de Paraguay) por logica dinamica:
  1) Partido en vivo ahora
  2) Partido de Paraguay hoy
  3) Partido con equipo top hoy (o primero del dia)
  4) Fallback: ultimo resultado jugado de Paraguay
  5) Fallback final: ultimo resultado jugado de cualquier equipo
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado. Ejecuta desde la raiz del repo.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

JS_DESTACADO = """
// ============================================================
// PARTIDO DESTACADO DEL DIA (splash)
// Prioridad: 1) En vivo  2) Paraguay hoy  3) Top/primero del dia  4) Fallback Paraguay  5) Fallback general
// ============================================================
const TOP_TEAMS_DESTACADO=['Brasil','Argentina','Francia','Alemania','España','Inglaterra','Portugal','Países Bajos'];

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

  var live=REAL_MATCHES.find(function(m){return isMatchLive(m);});
  if(live) return {match:live,label:'🔴 EN VIVO',tag:'live'};

  var pyHoy=todayMatches.find(function(m){return m.a==='Paraguay'||m.b==='Paraguay';});
  if(pyHoy) return {match:pyHoy,label:'PARTIDO DE PARAGUAY · HOY',tag:'paraguay'};

  if(todayMatches.length>0){
    var topM=todayMatches.find(function(m){
      return TOP_TEAMS_DESTACADO.indexOf(m.a)!==-1||TOP_TEAMS_DESTACADO.indexOf(m.b)!==-1;
    });
    var pick=topM||todayMatches[0];
    return {match:pick,label:'PARTIDO DESTACADO DEL DÍA',tag:'destacado'};
  }

  var pyPlayed=REAL_MATCHES.filter(function(m){return (m.a==='Paraguay'||m.b==='Paraguay')&&m.ga!==null;});
  if(pyPlayed.length>0){
    return {match:pyPlayed[pyPlayed.length-1],label:'ÚLTIMO RESULTADO · PARAGUAY',tag:'last-py'};
  }

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
"""

if 'function getPartidoDestacado' in html:
    print("JS destacado ya existe, saltando insercion de funciones.")
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + JS_DESTACADO + '\n' + html[last_script:]
        print("JS destacado agregado OK")
    else:
        print("WARNING: no se encontro </script> para insertar JS destacado")

OLD_CALL_PATTERNS = [
    r"document\.getElementById\('spMcRow'\)\.innerHTML\s*=\s*[^;]+;",
]
for pat in OLD_CALL_PATTERNS:
    if re.search(pat, html):
        html = re.sub(pat, "renderSplashDestacado();", html, count=1)
        print("Llamada anterior a spMcRow reemplazada por renderSplashDestacado()")

if 'renderSplashDestacado();' not in html:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + "\nrenderSplashDestacado();\nsetInterval(renderSplashDestacado, 60000);\n" + html[last_script:]
        print("Llamada inicial a renderSplashDestacado() agregada OK")
else:
    print("Llamada a renderSplashDestacado() ya presente")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
print("Ahora correr: python3 build.py")
