"""
patch_bracket.py
Ejecutar en la raiz del repo: python3 patch_bracket.py
Actualiza los resultados reales del cuadro eliminatorio Mundial 2026.
Actualizado: 07/07/2026
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

BRACKET_JS = '''
// ============================================================
// BRACKET REAL - RESULTADOS CONFIRMADOS MUNDIAL 2026
// Actualizado: 07/07/2026
// ============================================================
const BRACKET_REAL = {
  r32: [
    {m:73, a:'Sudáfrica',    ga:0, b:'Canadá',          gb:1,     date:'28/06'},
    {m:74, a:'Alemania',     ga:'1(4)', b:'Paraguay',    gb:'1(2)',date:'29/06', py:true},
    {m:75, a:'Países Bajos', ga:1, b:'Marruecos',       gb:2,     date:'29/06'},
    {m:76, a:'Noruega',      ga:3, b:'Costa de Marfil', gb:2,     date:'29/06'},
    {m:77, a:'Francia',      ga:3, b:'Suecia',           gb:0,    date:'30/06'},
    {m:78, a:'Bélgica',      ga:3, b:'Senegal',          gb:2,    date:'01/07'},
    {m:79, a:'Estados Unidos',ga:2,b:'Bosnia',           gb:0,    date:'01/07'},
    {m:80, a:'España',       ga:3, b:'Austria',          gb:0,    date:'02/07'},
    {m:81, a:'Portugal',     ga:2, b:'Croacia',          gb:1,    date:'02/07'},
    {m:82, a:'Suiza',        ga:2, b:'Argelia',          gb:0,    date:'03/07'},
    {m:83, a:'Australia',    ga:'1(2)',b:'Egipto',       gb:'1(4)',date:'03/07'},
    {m:84, a:'Argentina',    ga:3, b:'Cabo Verde',       gb:2,    date:'03/07'},
    {m:85, a:'Colombia',     ga:1, b:'Ghana',            gb:0,    date:'03/07'},
    {m:86, a:'México',       ga:2, b:'Ecuador',          gb:1,    date:'28/06'},
    {m:87, a:'Inglaterra',   ga:2, b:'RD Congo',         gb:1,    date:'03/07'},
    {m:88, a:'Brasil',       ga:1, b:'Japón',            gb:2,    date:'28/06'},
  ],
  r16: [
    {m:89, a:'Canadá',        ga:0, b:'Marruecos',      gb:3,    date:'04/07'},
    {m:90, a:'Paraguay',      ga:0, b:'Francia',         gb:1,    date:'04/07', py:true},
    {m:91, a:'Brasil',        ga:1, b:'Noruega',         gb:2,    date:'05/07'},
    {m:92, a:'México',        ga:2, b:'Inglaterra',      gb:3,    date:'05/07'},
    {m:93, a:'España',        ga:1, b:'Portugal',        gb:0,    date:'06/07'},
    {m:94, a:'Bélgica',       ga:4, b:'Estados Unidos',  gb:1,   date:'06/07'},
    {m:95, a:'Argentina',     ga:3, b:'Egipto',          gb:2,    date:'07/07'},
    {m:96, a:'Suiza',         ga:null, b:'Colombia',     gb:null, date:'07/07'},
  ],
  qf: [
    {m:97, a:'Marruecos',     ga:null, b:'Francia',      gb:null, date:'09/07'},
    {m:98, a:'España',        ga:null, b:'Bélgica',      gb:null, date:'10/07'},
    {m:99, a:'Noruega',       ga:null, b:'Inglaterra',   gb:null, date:'11/07'},
    {m:100,a:'Argentina',     ga:null, b:'Suiza/Colombia',gb:null,date:'11/07'},
  ],
  sf: [
    {m:101,a:'Por definir',   ga:null, b:'Por definir',  gb:null, date:'14/07'},
    {m:102,a:'Por definir',   ga:null, b:'Por definir',  gb:null, date:'15/07'},
  ],
  tp:    {m:103,a:'Por definir',ga:null,b:'Por definir',gb:null,date:'18/07'},
  final: {m:104,a:'Por definir',ga:null,b:'Por definir',gb:null,date:'19/07'}
};

function empScoreStr(ga, gb){
  if(ga===null||ga===undefined||gb===null||gb===undefined) return null;
  return String(ga) + ' - ' + String(gb);
}

function empRenderBracketReal(){
  var container = document.getElementById('empBracketContainer');
  var subtitle = document.getElementById('empSubtitle');
  if(!container) return;
  if(subtitle) subtitle.textContent = 'Resultados confirmados · Actualizado 07/07/2026';

  function renderMatch(match){
    var isPy = match.py;
    var score = empScoreStr(match.ga, match.gb);
    var winA = score && String(match.ga) > String(match.gb);
    var winB = score && String(match.gb) > String(match.ga);
    function flagHtml(name){
      if(typeof TF==='undefined'||typeof FH==='undefined'||!name||name==='Por definir') return '';
      var tf = TF[name];
      if(!tf) return '';
      return FH(tf.c, tf.d, 16, 11);
    }
    var border = isPy ? '1.5px solid #E53935' : (score?'1px solid #DCE0EC':'1px dashed #C7D2F0');
    var bg     = isPy ? '#FFF6F5' : (score?'#fff':'#F0F4FF');
    var nameA  = match.a || 'Por definir';
    var nameB  = match.b || 'Por definir';
    var colorA = score ? (winA?'#0a1f6e':'#999') : '#1a2b5c';
    var colorB = score ? (winB?'#0a1f6e':'#999') : '#1a2b5c';
    var fwA    = winA ? '900' : '600';
    var fwB    = winB ? '900' : '600';
    if(!score){colorA='#1a2b5c';colorB='#1a2b5c';fwA='700';fwB='700';}
    return '<div class="emp-match" style="background:'+bg+';border:'+border+';margin-bottom:6px">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;gap:4px;padding:2px 0">'
        +'<div style="display:flex;align-items:center;gap:4px;flex:1;overflow:hidden">'
          +flagHtml(nameA)
          +'<span style="font-size:12px;font-weight:'+fwA+';color:'+colorA+';white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+nameA+'</span>'
        +'</div>'
        +(score?'<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+match.ga+'</span>':'')
      +'</div>'
      +'<div style="display:flex;align-items:center;justify-content:space-between;gap:4px;padding:2px 0">'
        +'<div style="display:flex;align-items:center;gap:4px;flex:1;overflow:hidden">'
          +flagHtml(nameB)
          +'<span style="font-size:12px;font-weight:'+fwB+';color:'+colorB+';white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+nameB+'</span>'
        +'</div>'
        +(score?'<span style="font-size:11px;font-weight:900;color:#E53935;flex-shrink:0;padding:0 4px">'+match.gb+'</span>':'')
      +'</div>'
      +'<div style="font-size:9px;color:#A6ACC4;margin-top:3px">M'+match.m+(match.date?' · '+match.date:'')+'</div>'
      +'</div>';
  }

  var html = '<div class="emp-bracket-grid">';
  html += '<div><div class="emp-stage-label">DIECISEISAVOS</div>';
  BRACKET_REAL.r32.forEach(function(m){ html += renderMatch(m); });
  html += '</div>';
  html += '<div><div class="emp-stage-label">OCTAVOS</div>';
  BRACKET_REAL.r16.forEach(function(m){ html += renderMatch(m); });
  html += '</div>';
  html += '<div><div class="emp-stage-label">CUARTOS</div>';
  BRACKET_REAL.qf.forEach(function(m){ html += renderMatch(m); });
  html += '</div>';
  html += '<div><div class="emp-stage-label">SEMIFINALES</div>';
  BRACKET_REAL.sf.forEach(function(m){ html += renderMatch(m); });
  html += '<div style="margin-top:14px"><div class="emp-stage-label">TERCER PUESTO</div>';
  html += renderMatch(BRACKET_REAL.tp);
  html += '</div></div>';
  html += '<div><div class="emp-stage-label">FINAL</div>';
  html += '<div class="emp-final-box"><div class="lbl">19/07 · MetLife Stadium</div>';
  html += '<div class="team">'+BRACKET_REAL.final.a+'</div>';
  html += '<div class="team">'+BRACKET_REAL.final.b+'</div>';
  html += '</div></div>';
  html += '</div>';
  container.innerHTML = html;
}
'''

# Insertar o reemplazar el bloque JS
if 'BRACKET_REAL' in html:
    start = html.find('// ============================================================\n// BRACKET REAL')
    end   = html.find('\nfunction empRenderBracketReal', start)
    end2  = html.find('\n}\n', end) + 3
    if start > 0 and end > 0:
        html = html[:start] + BRACKET_JS.strip() + '\n' + html[end2:]
        print("JS BRACKET_REAL actualizado OK")
    else:
        print("WARNING: no se pudo reemplazar, insertando al final")
        last_script = html.rfind('</script>')
        html = html[:last_script] + '\n' + BRACKET_JS + '\n' + html[last_script:]
else:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + '\n' + BRACKET_JS + '\n' + html[last_script:]
        print("JS BRACKET_REAL insertado OK")

# Hook showPage
if "if(id==='emparejamiento')renderEmparejamiento();" in html:
    html = html.replace(
        "if(id==='emparejamiento')renderEmparejamiento();",
        "if(id==='emparejamiento')empRenderBracketReal();"
    )
    print("Hook showPage actualizado OK")
elif "if(id==='emparejamiento')empRenderBracketReal();" in html:
    print("Hook showPage ya OK")
else:
    print("WARNING: hook showPage no encontrado")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")
print("Ahora correr: python3 build.py")
