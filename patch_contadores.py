"""
patch_contadores.py
Corrige los contadores de partidos jugados en Control y Clasificacion
para que usen REAL_JUGADOS (total real incluyendo eliminatorias).
"""
import re, sys, os

SRC = 'template.html'
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} no encontrado.")
    sys.exit(1)

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# Agregar calculo de REAL_JUGADOS en JS si no existe
JUGADOS_JS = '''
// REAL_JUGADOS - total de partidos jugados incluyendo eliminatorias
if(typeof REAL_JUGADOS === 'undefined'){
  var REAL_JUGADOS = REAL_MATCHES.filter(function(m){return m.ga!==null;}).length;
  var REAL_TOTAL = REAL_MATCHES.length;
}
'''

if 'REAL_JUGADOS' not in html:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + JUGADOS_JS + '\n' + html[last_script:]
        print("REAL_JUGADOS JS agregado OK")
else:
    print("REAL_JUGADOS ya existe OK")

# Buscar y corregir patrones de conteo en Control
# Patron 1: let jugados = REAL_MATCHES.filter(m=>m.stage==='group'&&m.ga!==null).length
patterns = [
    (r"(?:let|var|const)\s+jugados\s*=\s*REAL_MATCHES\.filter\([^)]*stage[^)]*group[^)]*\)\.length",
     "var jugados = REAL_JUGADOS"),
    (r"(?:let|var|const)\s+jugados\s*=\s*REAL_MATCHES\.filter\([^)]*\.g[^)]*null[^)]*\)\.length",
     "var jugados = REAL_JUGADOS"),
    (r"(?:let|var|const)\s+jugados\s*=\s*REAL_MATCHES\.filter\(function\([^)]*\)\s*\{[^}]*stage[^}]*group[^}]*\}\)\.length",
     "var jugados = REAL_JUGADOS"),
]

fixed = 0
for pat, rep in patterns:
    new_html = re.sub(pat, rep, html)
    if new_html != html:
        html = new_html
        fixed += 1
        print(f"Patron corregido OK")

# Buscar patrones de "de 72" o "de N · 100%" en JS y corregirlos
# Patron: 'de ' + totalPartidos + ' · 100%'
total_pattern = re.search(r"'de '\s*\+\s*(\w+)\s*\+\s*['\"] · ", html)
if total_pattern:
    old_var = total_pattern.group(1)
    if old_var not in ('REAL_TOTAL', 'REAL_JUGADOS'):
        html = html.replace("'de ' + " + old_var + " + ' · ", "'de ' + REAL_TOTAL + ' · ", 1)
        print(f"Variable total corregida: {old_var} → REAL_TOTAL")
        fixed += 1

if fixed == 0:
    print("No se encontraron patrones para corregir automaticamente")
    print("Los contadores se calculan dinamicamente en el JS del Control")
    print("Agregando override al final del script...")
    
    # Override directo: al cargar la pagina, sobreescribir el contador
    OVERRIDE_JS = '''
// Override contadores de partidos jugados
function fixContadores(){
  // Buscar elementos que muestran el contador de jugados
  var els = document.querySelectorAll('[id*="Jug"], [id*="jug"], [class*="jugados"]');
  els.forEach(function(el){
    if(el.textContent.match(/^[0-9]+$/) && parseInt(el.textContent) < REAL_JUGADOS){
      el.textContent = REAL_JUGADOS;
    }
  });
  // Buscar el elemento spJug especificamente
  var spJug = document.getElementById('spJug');
  if(spJug) spJug.textContent = REAL_JUGADOS;
}
// Ejecutar al cargar y periodicamente
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', fixContadores);
} else {
  fixContadores();
}
setTimeout(fixContadores, 500);
setTimeout(fixContadores, 1500);
'''
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + OVERRIDE_JS + '\n' + html[last_script:]
        print("Override de contadores agregado OK")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {html.count(chr(10))} lineas -> {SRC}")

