import urllib.request, json, os, re

print("Descargando datos...")
url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read())

matches = [m for m in data['matches'] if m.get('group','').startswith('Group')]

NAME={'Mexico':'México','USA':'Estados Unidos','Canada':'Canadá','Brazil':'Brasil','Argentina':'Argentina','Spain':'España','France':'Francia','Germany':'Alemania','Japan':'Japón','Netherlands':'Países Bajos','Portugal':'Portugal','England':'Inglaterra','Croatia':'Croacia','Morocco':'Marruecos','Senegal':'Senegal','Ecuador':'Ecuador','Uruguay':'Uruguay','Colombia':'Colombia','Paraguay':'Paraguay','Switzerland':'Suiza','Belgium':'Bélgica','Denmark':'Dinamarca','Australia':'Australia','South Korea':'Corea del Sur','Iran':'Irán','Saudi Arabia':'Arabia Saudita','Tunisia':'Túnez','Ghana':'Ghana','Ivory Coast':'Costa de Marfil','Egypt':'Egipto','Algeria':'Argelia','Norway':'Noruega','Turkey':'Turquía','Scotland':'Escocia','Panama':'Panamá','Haiti':'Haití','South Africa':'Sudáfrica','Czech Republic':'Rep. Checa','Bosnia & Herzegovina':'Bosnia','Qatar':'Qatar','Haiti':'Haití','Curacao':'Curaçao','Sweden':'Suecia','New Zealand':'Nueva Zelanda','Cape Verde':'Cabo Verde','Iraq':'Irak','Jordan':'Jordania','DR Congo':'Congo DR','Uzbekistan':'Uzbekistán','Senegal':'Senegal','Austria':'Austria'}
MONTHS={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun','07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}

def es(n): return NAME.get(n,n)
def fD(s):
    if not s: return ''
    p=s.split('-'); return str(int(p[2])) + ' ' + MONTHS.get(p[1],p[1])
def fT(t):
    if not t: return ''
    try:
        parts=t.split(':'); h=(int(parts[0])+2)%24; return str(h).zfill(2)+':'+parts[1][:2]
    except: return t

out=[]
for i,m in enumerate(matches):
    sc=m.get('score',{}).get('ft')
    goals1=[]
    goals2=[]
    for g in m.get('goals1') or []:
        goals1.append({'name':g.get('name',''),'minute':str(g.get('minute',''))})
    for g in m.get('goals2') or []:
        goals2.append({'name':g.get('name',''),'minute':str(g.get('minute',''))})
    out.append({
        'id':i,
        'g':m['group'].replace('Group ',''),
        'a':es(m.get('team1','')),
        'b':es(m.get('team2','')),
        'date':fD(m.get('date','')),
        'dateRaw':m.get('date',''),
        'time':fT(m.get('time','')),
        'city':m.get('ground',''),
        'ga':sc[0] if sc else None,
        'gb':sc[1] if sc else None,
        'goals1':goals1,
        'goals2':goals2,
        'round':m.get('round','')
    })

jugados = sum(1 for m in out if m['ga'] is not None)
print(f"Partidos jugados: {jugados} de {len(out)}")

groups = {}
for m in out:
    g = m['g']
    if g not in groups: groups[g] = []
    if m['a'] not in groups[g]: groups[g].append(m['a'])
    if m['b'] not in groups[g]: groups[g].append(m['b'])

with open('template.html', encoding='utf-8') as f:
    tmpl = f.read()

DATA = 'const REAL_MATCHES = '+json.dumps(out, ensure_ascii=False)+';\nconst REAL_GROUPS = '+json.dumps(groups, ensure_ascii=False)+';'
result = re.sub(r'const REAL_MATCHES = \[.*?\];\nconst REAL_GROUPS = \{.*?\};', DATA, tmpl, flags=re.DOTALL)

# Inyectar jugados en splash
result = re.sub(r'(<div class="sp-kv" id="spJug"[^>]*>)\d+(</div>)', r'\g<1>'+str(jugados)+r'\2', result)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'✅ Listo — {jugados} partidos jugados inyectados en splash y dashboard')
