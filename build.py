import urllib.request, json, os

print("Descargando datos...")
url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read())

matches = [m for m in data['matches'] if m.get('group','').startswith('Group')]

NAME={'Mexico':'México','USA':'Estados Unidos','Canada':'Canadá','Brazil':'Brasil','Argentina':'Argentina','Spain':'España','France':'Francia','Germany':'Alemania','Japan':'Japón','Netherlands':'Países Bajos','Portugal':'Portugal','England':'Inglaterra','Croatia':'Croacia','Morocco':'Marruecos','Senegal':'Senegal','Ecuador':'Ecuador','Uruguay':'Uruguay','Colombia':'Colombia','Paraguay':'Paraguay','Chile':'Chile','Peru':'Perú','Bolivia':'Bolivia','Switzerland':'Suiza','Belgium':'Bélgica','Denmark':'Dinamarca','Serbia':'Serbia','Poland':'Polonia','Australia':'Australia','South Korea':'Corea del Sur','Iran':'Irán','Saudi Arabia':'Arabia Saudita','Tunisia':'Túnez','Cameroon':'Camerún','Ghana':'Ghana','Nigeria':'Nigeria','Ivory Coast':'Costa de Marfil','Egypt':'Egipto','Algeria':'Argelia','South Africa':'Sudáfrica','Norway':'Noruega','Turkey':'Turquía','Romania':'Rumanía','Ukraine':'Ucrania','Scotland':'Escocia','Panama':'Panamá','Haiti':'Haití','Jamaica':'Jamaica','Costa Rica':'Costa Rica','Honduras':'Honduras'}
MONTHS={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun','07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}

def es(n): return NAME.get(n,n)
def fD(s):
    if not s: return ''
    p=s.split('-'); return f"{int(p[2])} {MONTHS.get(p[1],p[1])}"
def fT(t):
    if not t: return ''
    try:
        parts=t.split(':'); h=(int(parts[0])+2)%24; return f"{h:02d}:{parts[1][:2]}"
    except: return t

out=[]
for i,m in enumerate(matches):
    sc=m.get('score',{}).get('ft')
    out.append({'id':i,'g':m['group'].replace('Group ',''),'a':es(m.get('team1','')),'b':es(m.get('team2','')),'date':fD(m.get('date','')),'time':fT(m.get('time','')),'city':m.get('ground',''),'ga':sc[0] if sc else None,'gb':sc[1] if sc else None})

os.makedirs('dist', exist_ok=True)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VERING · Fixture Mundial 2026</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial,sans-serif;background:#0a1628;color:#fff;min-height:100vh}}
.header{{background:#0d1f3c;padding:20px;text-align:center;border-bottom:2px solid #e63946}}
.header h1{{font-size:2.5em;letter-spacing:4px}}
.header p{{color:#aaa;margin-top:5px}}
.stats{{display:flex;flex-wrap:wrap;justify-content:center;gap:15px;padding:20px}}
.stat{{background:#1a2f4e;border-radius:10px;padding:20px 30px;text-align:center;min-width:120px}}
.stat .num{{font-size:2em;font-weight:bold;color:#e63946}}
.stat .label{{color:#aaa;font-size:0.85em;margin-top:5px}}
.matches{{max-width:800px;margin:0 auto;padding:20px}}
.match{{background:#1a2f4e;border-radius:10px;margin-bottom:15px;padding:20px}}
.match-row{{display:flex;align-items:center;justify-content:space-between;gap:10px}}
.team{{font-size:1.1em;font-weight:bold;flex:1}}
.team.right{{text-align:right}}
.score{{background:#0d1f3c;padding:10px 20px;border-radius:8px;font-size:1.3em;font-weight:bold;min-width:80px;text-align:center}}
.match-info{{color:#aaa;font-size:0.8em;text-align:center;margin-top:8px}}
.group-tag{{background:#e63946;color:#fff;padding:3px 8px;border-radius:4px;font-size:0.75em;margin-bottom:8px;display:inline-block}}
.finalizado{{border-left:3px solid #2ecc71}}
.proximo{{border-left:3px solid #555}}
h2{{text-align:center;padding:20px;color:#e63946;letter-spacing:2px}}
</style>
</head>
<body>
<div class="header"><h1>VERING</h1><p>FIXTURE · MUNDIAL 2026</p></div>
<div class="stats">
  <div class="stat"><div class="num">{len(out)}</div><div class="label">Partidos</div></div>
  <div class="stat"><div class="num">{sum(1 for m in out if m['ga'] is not None)}</div><div class="label">Jugados</div></div>
  <div class="stat"><div class="num">48</div><div class="label">Selecciones</div></div>
  <div class="stat"><div class="num">12</div><div class="label">Grupos A-L</div></div>
</div>
<h2>PARTIDOS</h2>
<div class="matches">
{''.join(f"""<div class="match {'finalizado' if m['ga'] is not None else 'proximo'}">
  <span class="group-tag">Grupo {m['g']}</span>
  <div class="match-row">
    <div class="team">{m['a']}</div>
    <div class="score">{f"{m['ga']} - {m['gb']}" if m['ga'] is not None else '- : -'}</div>
    <div class="team right">{m['b']}</div>
  </div>
  <div class="match-info">{m['date']} · {m['time']} · {m['city']}</div>
</div>""" for m in out)}
</div>
</body>
</html>"""

with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Listo: {len(out)} partidos, {sum(1 for m in out if m['ga'] is not None)} jugados")
