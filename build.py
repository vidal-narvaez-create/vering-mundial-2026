import urllib.request, json, re, os

url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read())

matches = [m for m in data['matches'] if m.get('group','').startswith('Group')]
NAME={'Mexico':'México','South Africa':'Sudáfrica','South Korea':'Corea del Sur','Czech Republic':'Rep. Checa','Canada':'Canadá','Bosnia & Herzegovina':'Bosnia','Qatar':'Qatar','Switzerland':'Suiza','Brazil':'Brasil','Haiti':'Haití','Morocco':'Marruecos','Scotland':'Escocia','USA':'Estados Unidos','Paraguay':'Paraguay','Australia':'Australia','Turkey':'Turquía','Curaçao':'Curaçao','Ecuador':'Ecuador','Germany':'Alemania','Ivory Coast':'Costa de Marfil','Japan':'Japón','Netherlands':'Países Bajos','Sweden':'Suecia','Tunisia':'Túnez','Belgium':'Bélgica','Egypt':'Egipto','Iran':'Irán','New Zealand':'Nueva Zelanda','Cape Verde':'Cabo Verde','Saudi Arabia':'Arabia Saudita','Spain':'España','Uruguay':'Uruguay','France':'Francia','Iraq':'Irak','Norway':'Noruega','Senegal':'Senegal','Algeria':'Argelia','Argentina':'Argentina','Austria':'Austria','Jordan':'Jordania','Colombia':'Colombia','DR Congo':'Congo DR','Portugal':'Portugal','Uzbekistan':'Uzbekistán','Croatia':'Croacia','England':'Inglaterra','Ghana':'Ghana','Panama':'Panamá'}
MONTHS={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun','07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}
def es(n): return NAME.get(n,n)
def fD(s):
    if not s: return ''
    p=s.split('-'); return f"{int(p[2])} {MONTHS.get(p[1],p[1])}"
def fT(t):
    if not t: return ''
    try:
        parts=t.split(' ')[0].split(':'); h=(int(parts[0])+2)%24; return f"{h:02d}:{parts[1]}"
    except: return t

out=[]
for i,m in enumerate(matches):
    sc=m.get('score',{}).get('ft')
    out.append({'id':i,'g':m['group'].replace('Group ',''),'a':es(m['team1']),'b':es(m['team2']),'date':fD(m['date']),'dateRaw':m['date'],'time':fT(m.get('time','')),'city':m.get('ground',''),'ga':sc[0] if sc else None,'gb':sc[1] if sc else None,'goals1':[{'name':g['name'],'minute':g['minute']} for g in m.get('goals1',[])],'goals2':[{'name':g['name'],'minute':g['minute']} for g in m.get('goals2',[])],'round':m.get('round','')})

groups={}
for m in out:
    g=m['g']
    if g not in groups: groups[g]=[]
    if m['a'] not in groups[g]: groups[g].append(m['a'])
    if m['b'] not in groups[g]: groups[g].append(m['b'])

NEW_DATA = f"const REAL_MATCHES = {json.dumps(out, ensure_ascii=False)};\nconst REAL_GROUPS = {json.dumps(groups, ensure_ascii=False)};"
with open('template.html') as f:
    html = f.read()
html = re.sub(r'const REAL_MATCHES = \[.*?\];\nconst REAL_GROUPS = \{.*?\};', NEW_DATA, html, flags=re.DOTALL)
os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w') as f:
    f.write(html)
print(f"Done: {len(out)} matches, {sum(1 for m in out if m['ga'] is not None)} scored")
