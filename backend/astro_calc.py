import swisseph as swe
import datetime

# Planet IDs in Swiss Ephemeris
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE
}

RASIS = [
    "Aries (Mesham)", "Taurus (Rishabham)", "Gemini (Mithunam)",
    "Cancer (Katakam)", "Leo (Simmam)", "Virgo (Kanni)",
    "Libra (Thulaam)", "Scorpio (Viruchigam)", "Sagittarius (Dhanusu)",
    "Capricorn (Makaram)", "Aquarius (Kumbham)", "Pisces (Meenam)"
]

def calculate_real_transits():
    now = datetime.datetime.now()
    
    # 1. Calculate Julian Day for current UTC time
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)
    
    # Sidereal flag for Lahiri Ayanamsa (Vedic)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0.0, 0.0)
    flag = swe.FLG_SIDEREAL | swe.FLG_SPEED
    
    positions = {}
    for planet_name, planet_id in PLANETS.items():
        res, _ = swe.calc_ut(jd, planet_id, flag)
        longitude = res[0] % 360
        rasi_index = int(longitude // 30)
        degree_in_rasi = longitude % 30
        
        positions[planet_name] = {
            "longitude": round(longitude, 2),
            "rasi": RASIS[rasi_index],
            "degree": round(degree_in_rasi, 2)
        }
        
    return positions