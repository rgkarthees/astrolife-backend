from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from backend.astro_calc import calculate_real_transits

app = FastAPI(title="AstroLife AI API")

class UserDetails(BaseModel):
    name: str
    dob: str
    tob: str
    latitude: float
    longitude: float

@app.get("/")
def home():
    return {"message": "AstroLife AI Server Running!"}

@app.post("/api/v1/daily-dashboard")
def get_daily_dashboard(user: UserDetails):
    today = datetime.datetime.now()
    
    # Fetch real-time planetary positions
    real_transits = calculate_real_transits()
    
    return {
        "user_name": user.name,
        "date": today.strftime("%Y-%m-%d"),
        "scores": {
            "focus": 85,
            "wealth": 90,
            "health": 65
        },
        "live_transits": real_transits,
        "guidance": "Sun Dasha + 11th House Rahu provides networking gains.",
        "dos_and_donts": {
            "do": "Leverage business contacts & planning.",
            "dont": "Avoid hasty investments."
        }
    }