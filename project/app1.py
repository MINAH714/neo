from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime

app = FastAPI()

@app.get("/api/flight_Prices")
async def get_flight_prices(
    origin: str = Query(..., description="출발지"),
    destination: str = Query(..., description="도착지"),
    departureDate: str = Query(..., description="출국일 (YYYY-MM-DD)"),
    currency: Optional[str] = Query("KRW", description="통화 (기본 KRW)")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    sample_data = {
        "Result": True,
        "country": {
            "name": destination,
            "averagePrice": 352000,
            "minPrice": 280000,
            "maxPrice": 450000,
            "currency": currency,
            "dataCount": 27
        }
    }

    return sample_data
