import urllib.request, json, os, re

print("Descargando datos...")
url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read())

# Todos los partidos (grupos + eliminatorias)
all_matches = data['matches']

NAME={
    'Mexico':'México','USA':'Estados Unidos','Canada':'Canadá','Brazil':'Brasil',
    'Argentina':'Argentina','Spain':'España','France':'Francia','Germany':'Alemania',
    'Japan':'Japón','Netherlands':'Países Bajos','Portugal':'Portugal','England':'Inglaterra',
    'Croatia':'Croacia','Morocco':'Marruecos','Senegal':'Senegal','Ecuador':'Ecuador',
    'Uruguay':'Uruguay','Colombia':'Colombia','Paraguay':'Paraguay','Switzerland':'Suiza',
    'Belgium':'Bélgica','Denmark':'Dinamarca','Australia':'Australia',
    'South Korea':'Corea del Sur','Iran':'Irán','Saudi Arabia':'Arabia Saudita',
    'Tunisia':'Túnez','Ghana':'Ghana','Ivory Coast':'Costa de Marfil','Egypt':'Egipto',
    'Algeria':'Argelia','Norway':'Noruega','Turkey':'Turquía','Scotland':'Escocia',
    'Panama':'Panamá','Haiti':'Haití','South Africa':'Sudáfrica',
    'Czech Republic':'Rep. Checa','Bosnia & Herzegovina':'Bosnia','Qatar':'Qatar',
    'Curacao':'Curaçao','Sweden':'Suecia','New Zealand':'Nueva Zelanda',
    'Cape Verde':'Cabo Verde','Iraq':'Irak','Jordan':'Jordania','DR Congo':'Congo DR',
    'Uzbekistan':'Uzbekistán','Austria':'Austria','Ivory Coast':'Costa de Marfil',
    'Bosnia':'Bosnia','Cape Verde':'Cabo Verde','DR Congo':'Congo DR',
}

# Rondas eliminatorias en español
ROUND_ES = {
    'Round of 32': 'Dieciseisavos',
    'Round of 16': 'Octavos',
    'Quarter-Finals': 'Cuartos',
    'Semi-Finals': 'Semifinales',
    'Third-Place Match': 'Tercer Puesto',
    'Final': 'Final',
}

MONTHS={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun',
        '07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}

def es(n):
    return NAME.get(n, n) if n else ''

def fD(s):
    if not s: return ''
    p = s.split('-')
    return str(int(p[2])) + ' ' + MONTHS.get(p[1], p[1])

def fCity(ground):
    if not ground: return ''
    g = ground.lower()
    city_map = {
        'lumen field':             'Seattle',
        'sofi stadium':            'Los Angeles (Inglewood)',
        "levi's stadium":          'San Francisco Bay Area (Santa Clara)',
        'bc place':                'Vancouver',
        'at&t stadium':            'Dallas (Arlington)',
        'arrowhead stadium':       'Kansas City',
        'nrg stadium':             'Houston',
        'azteca stadium':          'Mexico City',
        'estadio akron':           'Guadalajara (Zapopan)',
        'estadio bbva':            'Monterrey (Guadalupe)',
        'mercedes-benz stadium':   'Atlanta',
        'hard rock stadium':       'Miami (Miami Gardens)',
        'gillette stadium':        'Boston (Foxborough)',
        'metlife stadium':         'New York/New Jersey (East Rutherford)',
        'lincoln financial field': 'Philadelphia',
        'bmo field':               'Toronto',
    }
    for key, city in city_map.items():
        if key in g:
            return city
    return ground

def fT_py(time_str):
    if not time_str: return ''
    try:
        # Extraer solo HH:MM ignorando timezone
        t = time_str.split(' ')[0]
        parts = t.split(':')
        local_h = int(parts[0])
        local_m = int(parts[1][:2]) if len(parts) > 1 else 0
        py_h = (local_h + 4) % 24
        return f"{py_h:02d}:{local_m:02d}"
    except Exception:
        return time_str

out = []
for i, m in enumerate(all_matches):
    sc = m.get('score', {}).get('ft') if m.get('score') else None
    goals1 = []
    goals2 = []
    for g in m.get('goals1') or []:
        goals1.append({'name': g.get('name', ''), 'minute': str(g.get('minute', ''))})
    for g in m.get('goals2') or []:
        goals2.append({'name': g.get('name', ''), 'minute': str(g.get('minute', ''))})

    ground  = m.get('ground', '')
    city    = fCity(ground)
    time_py = fT_py(m.get('time', ''))
    round_  = m.get('round', '')

    # Determinar grupo y tipo de partido
    is_group = m.get('group', '').startswith('Group')
    grupo    = m['group'].replace('Group ', '') if is_group else ''
    stage    = 'group' if is_group else ROUND_ES.get(round_, round_)

    # Nombres de equipos (pueden ser placeholders en eliminatorias ej: "W73", "2A")
    team1 = es(m.get('team1', '')) or m.get('team1', '')
    team2 = es(m.get('team2', '')) or m.get('team2', '')

    out.append({
        'id':      i,
        'num':     m.get('num'),          # numero de partido (73-104 en eliminatorias)
        'g':       grupo,                  # letra de grupo (solo fase de grupos)
        'stage':   stage,                  # fase del torneo
        'a':       team1,
        'b':       team2,
        'date':    fD(m.get('date', '')),
        'dateRaw': m.get('date', ''),
        'time':    time_py,
        'city':    city,
        'ga':      sc[0] if sc else None,
        'gb':      sc[1] if sc else None,
        'goals1':  goals1,
        'goals2':  goals2,
        'round':   round_,
    })

# Estadisticas
group_matches  = [m for m in out if m['stage'] == 'group']
ko_matches     = [m for m in out if m['stage'] != 'group']
jugados        = sum(1 for m in out if m['ga'] is not None)
jugados_grupos = sum(1 for m in group_matches if m['ga'] is not None)
jugados_ko     = sum(1 for m in ko_matches if m['ga'] is not None)

print(f"Total partidos: {len(out)} (grupos: {len(group_matches)}, eliminatorias: {len(ko_matches)})")
print(f"Jugados: {jugados} (grupos: {jugados_grupos}, eliminatorias: {jugados_ko})")

print("\nVerificacion horas (+4 PY):")
for m in out[:3]:
    print(f"  {m['a']} vs {m['b']} | {m['city']} | {m['time']} hs PY | {m['stage']}")

# Grupos (solo fase de grupos)
groups = {}
for m in group_matches:
    g = m['g']
    if g not in groups:
        groups[g] = []
    if m['a'] not in groups[g]:
        groups[g].append(m['a'])
    if m['b'] not in groups[g]:
        groups[g].append(m['b'])

with open('template.html', encoding='utf-8') as f:
    tmpl = f.read()

DATA = ('const REAL_MATCHES = ' + json.dumps(out, ensure_ascii=False)
        + ';\nconst REAL_GROUPS = ' + json.dumps(groups, ensure_ascii=False) + ';')

result = re.sub(
    r'const REAL_MATCHES = \[.*?\];\nconst REAL_GROUPS = \{.*?\};',
    DATA, tmpl, flags=re.DOTALL
)

result = re.sub(
    r'(<div class="sp-kv" id="spJug"[^>]*>)\d+(</div>)',
    r'\g<1>' + str(jugados) + r'\2',
    result
)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'\nListo! {jugados} jugados · hora PY (+4) · dist/index.html generado')

