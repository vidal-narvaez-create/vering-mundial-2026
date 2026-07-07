"""
patch_bracket.py
Ejecutar en la raiz del repo: python3 patch_bracket.py
Actualiza los resultados reales del cuadro eliminatorio Mundial 2026.
Actualizado: 07/07/2026 - Suiza vs Colombia pendiente
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

BRACKET_JS = """
// ============================================================
// BRACKET REAL - RESULTADOS CONFIRMADOS MUNDIAL 2026
// Actualizado: 07/07/2026
// ============================================================
const BRACKET_REAL = {
  r32: [
    {m:73, a:'Sudáfrica',    ga:0, b:'Canadá',        gb:1,    date:'28/06'},
    {m:74, a:'Alemania',     ga:'1(4)', b:'Paraguay',  gb:'1(2)',date:'29/06', py:true},
    {m:75, a:'Países Bajos', ga:1, b:'Marruecos',     gb:2,    date:'29/06'},
    {m:76, a:'Noruega',      ga:3, b:'Costa de Marfil',gb:2,   date:'29/06'},
    {m:77, a:'Francia',      ga:3, b:'Suecia',         gb:0,   date:'30/06'},
    {m:78, a:'Bélgica',      ga:3, b:'Senegal',        gb:2,   date:'01/07'},
    {m:79, a:'Estados Unidos',ga:2,b:'Bosnia',         gb:0,   date:'01/07'},
    {m:80, a:'España',       ga:3, b:'Austria',        gb:0,   date:'02/07'},
    {m:81, a:'Portugal',     ga:2, b:'Croacia',        gb:1,   date:'02/07'},
    {m:82, a:'Suiza',        ga:2, b:'Argelia',        gb:0,   date:'03/07'},
    {m:83, a:'Australia',    ga:'1(2)',b:'Egipto',     gb:'1(4)',date:'03/07'},
    {m:84, a:'Argentina',    ga:3, b:'Cabo Verde',     gb:2,   date:'03/07'},
    {m:85, a:'Colombia',     ga:1, b:'Ghana',          gb:0,   date:'03/07'},
    {m:86, a:'México',       ga:2, b:'Ecuador',        gb:1,   date:'28/06'},
    {m:87, a:'Inglaterra',   ga:2, b:'RD Congo',       gb:1,   date:'03/07'},
    {m:88, a:'Brasil',       ga:1, b:'Japón',          gb:2,   date:'28/06'},
  ],
  r16: [
    {m:89, a:'Canadá',       ga:0, b:'Marruecos',     gb:3,   date:'04/07'},
    {m:90, a:'Paraguay',     ga:0, b:'Francia',        gb:1,   date:'04/07', py:true},
    {m:91, a:'Brasil',       ga:1, b:'Noruega',        gb:2,   date:'05/07'},
    {m:92, a:'México',       ga:2, b:'Inglaterra',     gb:3,   date:'05/07'},
    {m:93, a:'España',       ga:1, b:'Portugal',       gb:0,   date:'06/07'},
    {m:94, a:'Bélgica',      ga:4, b:'Estados Unidos', gb:1,  date:'06/07'},
    {m:95, a:'Argentina',    ga:3, b:'Egipto',         gb:2,   date:'07/07'},
    {m:96, a:'Suiza',        ga:null, b:'Colombia',    gb:null,date:'07/07'},
  ],
  qf: [
    {m:97, a:'Marruecos',    ga:null, b:'Francia',     gb:null,date:'09/07'},
    {m:98, a:'España',       ga:null, b:'Bélgica',     gb:null,date:'10/07'},
    {m:99, a:'Noruega',      ga:null, b:'Inglaterra',  gb:null,date:'11/07'},
    {m:100,a:'Argentina',    ga:null, b:'Suiza/Colombia',gb:null,date:'11/07'},
  ],
  sf: [
    {m:101,a:'Por definir',  ga:null, b:'Por definir', gb:null,date:'14/07'},
    {m:102,a:'Por definir',  ga:null, b:'Por definir', gb:null,date:'15/07'},
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
    var score =
