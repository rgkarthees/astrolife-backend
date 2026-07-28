from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from typing import Dict, Tuple, Any
import urllib.request
import urllib.parse
import json
from backend.astro_calc import calculate_real_transits

app = FastAPI(title="AstroLife AI API")

# 🔓 Enable CORS for Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ZodiacSign(Enum):
    ARIES = (1, "Aries")
    TAURUS = (2, "Taurus")
    GEMINI = (3, "Gemini")
    CANCER = (4, "Cancer")
    LEO = (5, "Leo")
    VIRGO = (6, "Virgo")
    LIBRA = (7, "Libra")
    SCORPIO = (8, "Scorpio")
    SAGITTARIUS = (9, "Sagittarius")
    CAPRICORN = (10, "Capricorn")
    AQUARIUS = (11, "Aquarius")
    PISCES = (12, "Pisces")

    def __init__(self, number, fullname):
        self.number = number
        self.fullname = fullname

PLANET_DIGNITIES = {
    "Sun": (ZodiacSign.ARIES, ZodiacSign.LIBRA),
    "Moon": (ZodiacSign.TAURUS, ZodiacSign.SCORPIO),
    "Mars": (ZodiacSign.CAPRICORN, ZodiacSign.CANCER),
    "Mercury": (ZodiacSign.VIRGO, ZodiacSign.PISCES),
    "Jupiter": (ZodiacSign.CANCER, ZodiacSign.CAPRICORN),
    "Venus": (ZodiacSign.PISCES, ZodiacSign.VIRGO),
    "Saturn": (ZodiacSign.LIBRA, ZodiacSign.ARIES),
}

class UserInput(BaseModel):
    name: str
    dob: str
    tob: str
    city: str

def get_zodiac_sign(degree: float) -> ZodiacSign:
    adjusted_degree = float(degree) % 360
    sign_number = int((adjusted_degree / 30) + 1)
    for sign in ZodiacSign:
        if sign.number == sign_number:
            return sign
    return ZodiacSign.ARIES

def check_dignity(planet_name: str, sign: ZodiacSign) -> Tuple[bool, bool]:
    if planet_name in PLANET_DIGNITIES:
        ucha_sign, neecha_sign = PLANET_DIGNITIES[planet_name]
        return (sign == ucha_sign, sign == neecha_sign)
    return False, False

def geocode_city(city_name: str) -> Tuple[float, float]:
    """Helper to convert City Name -> Lat/Lng using built-in urllib (no extra requirements)"""
    try:
        encoded_city = urllib.parse.quote(city_name)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_city}&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "AstroLifeBackend/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data:
                    return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Geocoding error: {e}")
    # Default fallback: Chennai / South India coordinates
    return 13.0827, 80.2707

@app.get("/")
def home():
    return {"message": "AstroLife AI Server Running!"}

@app.post("/api/v1/daily-dashboard")
def get_daily_dashboard(user: UserInput):
    try:
        # Geocode using Python standard library
        lat, lon = geocode_city(user.city)
        
        raw_planets = calculate_real_transits()
        enriched_planets = {}
        ucham_list = []
        neecham_list = []

        if isinstance(raw_planets, dict):
            for planet, val in raw_planets.items():
                if isinstance(val, dict):
                    deg_val = float(val.get("degree", val.get("deg", val.get("position", 0.0))))
                else:
                    deg_val = float(val)

                sign = get_zodiac_sign(deg_val)
                is_ucham, is_neecham = check_dignity(planet, sign)
                
                status = f"{sign.fullname} ({deg_val:.2f}°)"
                if is_ucham:
                    status += " [UCHAM / Exalted 🌟]"
                    ucham_list.append(planet)
                elif is_neecham:
                    status += " [NEEHAM / Debilitated ⚠️]"
                    neecham_list.append(planet)
                    
                enriched_planets[planet] = status

        guidance = f"Planetary transit calculations completed for {user.name} ({user.city})."
        if ucham_list:
            guidance += f" Excellent strength from Ucham planets: {', '.join(ucham_list)}."
        if neecham_list:
            guidance += f" Proceed with patience regarding Neecham planets: {', '.join(neecham_list)}."

        return {
            "user_name": user.name,
            "date": "Today",
            "scores": {
                "focus": 85 if not neecham_list else 70,
                "wealth": 92 if "Jupiter" in ucham_list else 78,
                "health": 88
            },
            "guidance": guidance,
            "planetary_transits": enriched_planets
        }
    except Exception as e:
        return {
            "user_name": user.name,
            "date": "Today",
            "scores": {
                "focus": 75,
                "wealth": 70,
                "health": 80
            },
            "guidance": f"General transits (Calculation notice: {str(e)})",
            "planetary_transits": {"Status": "Active"}
        }