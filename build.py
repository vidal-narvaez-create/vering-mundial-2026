import urllib.request, json, os, re

print("Descargando datos...")
url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
with urllib.request.urlopen(url, timeout=15) as r:
    data = json.loads(r.read())

matches = [m for m in data['matches'] if m.get('group','').startswith('Group')]

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
    'Uzbekistan':'Uzbekistán','Austria':'Austria'
}

MONTHS={'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun',
        '07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}

# Offset UTC con horario de VERANO (DST) - junio 2026
PY_OFFSET = -3  # Paraguay UTC-3 (junio 2026)
# EDT (Eastern Daylight) = UTC-4
# CDT (Central Daylight)  = UTC-5
# MDT (Mountain Daylight) = UTC-6
# PDT (Pacific Daylight)  = UTC-7
# Mexico (CDT)            = UTC-5
CITY_UTC_OFFSET = {
    # Pacific Daylight Time (UTC-7)
    'lumen field':            -7,
    'sofi stadium':           -7,
    "levi's stadium":         -7,
    'bc place':               -7,
    # Central Daylight Time (UTC-5) - Mexico y ciudades del centro USA
    'at&t stadium':           -5,
    'arrowhead stadium':      -5,
    'nrg stadium':            -5,
    'azteca stadium':         -5,
    'estadio akron':          -5,
    'estadio bbva':           -5,
    # Eastern Daylight Time (UTC-4) - igual que Paraguay
    'mercedes-benz stadium':  -4,
    'hard rock stadium':      -4,
    'gillette stadium':       -4,
    'metlife stadium':        -4,
    'lincoln financial field':-4,
    'bmo field':              -4,
}

# Mapeo ciudad display -> offset UTC (DST junio 2026)
CITY_DISPLAY_OFFSET = {
    'Seattle':                              -7,
    'Los Angeles (Inglewood)':              -7,
    'San Francisco Bay Area (Santa Clara)': -7,
    'Vancouver':                            -7,
    'Dallas (Arlington)':                   -5,
    'Kansas City':                          -5,
    'Houston':                              -5,
    'Mexico City':                          -5,
    'Guadalajara (Zapopan)':                -5,
    'Monterrey (Guadalupe)':                -5,
    'Atlanta':                              -4,
    'Miami (Miami Gardens)':                -4,
    'Boston (Foxborough)':                  -4,
    'New York/New Jersey (East Rutherford)':-4,
    'Philadelphia':                         -4,
    'Toronto':                              -4,
}

PY_OFFSET = -4  # Paraguay UTC-4

def es(n):
    return NAME.get(n, n)

def fD(s):
    if not s:
        return ''
    p = s.split('-')
    return str(int(p[2])) + ' ' + MONTHS.get(p[1], p[1])

def fT_py(time_str, ground):
    """Convierte hora local del estadio a hora Paraguay (UTC-4)"""
    if not time_str:
        return ''
    try:
        parts = time_str.split(':')
        local_h = int(parts[0])
        local_m = int(parts[1][:2]) if len(parts) > 1 else 0

        # Buscar offset de la ciudad
        city_offset = None
        ground_lower = (ground or '').lower()
        for key, off in CITY_UTC_OFFSET.items():
            if key in ground_lower:
                city_offset = off
                break

        if city_offset is None:
            # Fallback: asumir Central Time (UTC-6) para sedes mexicanas
            city_offset = -6

        # Convertir: local -> UTC -> Paraguay
        utc_h = local_h - city_offset   # hora_local - offset_negativo = UTC
        py_h  = utc_h + PY_OFFSET       # UTC - 4 = PY

        # Ajustar si pasa medianoche
        if py_h >= 24:
            py_h -= 24
        elif py_h < 0:
            py_h += 24

        return f"{py_h:02d}:{local_m:02d}"
    except Exception:
        return time_str

def fCity(ground):
    """Convierte nombre de estadio a ciudad display"""
    if not ground:
        return ''
    g = ground.lower()
    city_map = {
        'lumen field':              'Seattle',
        'sofi stadium':             'Los Angeles (Inglewood)',
        "levi's stadium":           'San Francisco Bay Area (Santa Clara)',
        'bc place':                 'Vancouver',
        'at&t stadium':             'Dallas (Arlington)',
        'arrowhead stadium':        'Kansas City',
        'nrg stadium':              'Houston',
        'azteca stadium':           'Mexico City',
        'estadio akron':            'Guadalajara (Zapopan)',
        'estadio bbva':             'Monterrey (Guadalupe)',
        'mercedes-benz stadium':    'Atlanta',
        'hard rock stadium':        'Miami (Miami Gardens)',
        'gillette stadium':         'Boston (Foxborough)',
        'metlife stadium':          'New York/New Jersey (East Rutherford)',
        'lincoln financial field':  'Philadelphia',
        'bmo field':                'Toronto',
    }
    for key, city in city_map.items():
        if key in g:
            return city
    return ground  # fallback: nombre del estadio

def fT_py_from_city(time_str, city_display):
    """Convierte hora local del estadio a hora PY usando ciudad display"""
    if not time_str:
        return ''
    try:
        parts = time_str.split(':')
        local_h = int(parts[0])
        local_m = int(parts[1][:2]) if len(parts) > 1 else 0

        city_offset = CITY_DISPLAY_OFFSET.get(city_display, -6)

        utc_h = local_h - city_offset
        py_h  = utc_h + PY_OFFSET

        if py_h >= 24:
            py_h -= 24
        elif py_h < 0:
            py_h += 24

        return f"{py_h:02d}:{local_m:02d}"
    except Exception:
        return time_str

out = []
for i, m in enumerate(matches):
    sc = m.get('score', {}).get('ft')
    goals1 = []
    goals2 = []
    for g in m.get('goals1') or []:
        goals1.append({'name': g.get('name', ''), 'minute': str(g.get('minute', ''))})
    for g in m.get('goals2') or []:
        goals2.append({'name': g.get('name', ''), 'minute': str(g.get('minute', ''))})

    ground   = m.get('ground', '')
    city     = fCity(ground)
    time_raw = m.get('time', '')
    time_py  = fT_py_from_city(time_raw, city)

    out.append({
        'id':       i,
        'g':        m['group'].replace('Group ', ''),
        'a':        es(m.get('team1', '')),
        'b':        es(m.get('team2', '')),
        'date':     fD(m.get('date', '')),
        'dateRaw':  m.get('date', ''),
        'time':     time_py,
        'city':     city,
        'ga':       sc[0] if sc else None,
        'gb':       sc[1] if sc else None,
        'goals1':   goals1,
        'goals2':   goals2,
        'round':    m.get('round', '')
    })

jugados = sum(1 for m in out if m['ga'] is not None)
print(f"Partidos jugados: {jugados} de {len(out)}")

# Verificacion de algunas horas
print("\nVerificacion de horas (deben ser hora PY):")
for m in out[:5]:
    print(f"  {m['a']} vs {m['b']} | {m['city']} | {m['time']} hs PY")

groups = {}
for m in out:
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

# Inyectar numero de jugados en splash
result = re.sub(
    r'(<div class="sp-kv" id="spJug"[^>]*>)\d+(</div>)',
    r'\g<1>' + str(jugados) + r'\2',
    result
)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'\nListo! {jugados} jugados · horas en formato PY (UTC-4) · dist/index.html generado')

