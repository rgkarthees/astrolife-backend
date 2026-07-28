from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.astro_calc import calculate_real_transits

app = FastAPI(title="AstroLife AI API")

# 🔓 Enable CORS for all web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any frontend origin (like localhost)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

class UserInput(BaseModel):
    name: str
    dob: str
    tob: str
    latitude: float
    longitude: float

@app.get("/")
def home():
    return {"message": "AstroLife AI Server Running!"}

@app.post("/api/v1/daily-dashboard")
def get_daily_dashboard(user: UserInput):
    # Calculate real planetary transits via Swiss Ephemeris
    planets = calculate_real_transits()
    
    return {
        "user_name": user.name,
        "date": "Today",
        "scores": {
            "focus": 85,
            "wealth": 72,
            "health": 90
        },
        "guidance": "Sun and Mercury alignment boosts mental clarity today. Excellent day for strategic decision-making.",
        "planetary_transits": planets
    }