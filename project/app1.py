from fastapi import FastAPI, Query
import requests
import json
from datetime import datetime
import os
from get_access_token import get_amadeus_access_token

CLIENT_ID = 'GeujpxISRCAGwtvRRwu67Scqot5VVSGx'
CLIENT_SECRET = 'mNVQG01ruRq7GptO'

access_token = get_amadeus_access_token(CLIENT_ID, CLIENT_SECRET)

app = FastAPI()


@app.get("/api/previous/flight_Prices")
async def get_pflight_prices(
    origin: str = Query(..., description="출발지 공항코드"),
    destination: str = Query(..., description="도착지 공항코드"),
    departureDate: str = Query(..., description="출국일 (YYYY-MM-DD)"),
    currency: str = Query("KRW", description="통화 (기본 KRW)")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}


    base_url = "https://test.api.amadeus.com/v1/analytics/itinerary-price-metrics"
    params = f"?originIataCode={origin}"
    params += f"&destinationIataCode={destination}"
    params += f"&departureDate={departureDate}"
    params += f"&currencyCode=KRW"
    params += f"&oneWay=true"




    full_url = base_url + params
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {"Result": True, "data": data}
    else:
        return {
            "Result": False,
            "message": f"API 호출 실패: {response.status_code}",
            "details": response.text
        }

@app.get("/api/flight_Prices")
async def get_flight_prices(
    origin: str = Query(..., description="출발지 공항코드"),
    destination: str = Query(..., description="도착지 공항코드"),
    departureDate: str = Query(..., description="출국일 (YYYY-MM-DD)"),
    currency: str = Query("KRW", description="통화 (기본 KRW)")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}


    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = f"?originLocationCode={origin}"
    params += f"&destinationLocationCode={destination}"
    params += f"&departureDate={departureDate}"
    params += f"&adults=1"
    params += f"&currencyCode={currency}"




    full_url = base_url + params
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {"Result": True, "data": data}
    else:
        return {
            "Result": False,
            "message": f"API 호출 실패: {response.status_code}",
            "details": response.text
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
