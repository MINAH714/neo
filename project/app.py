from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests, json
import os
from datetime import datetime, timedelta
from get_access_token import get_amadeus_access_token
import math  # 지수함수를 위해 필요함
import random

CLIENT_ID = 'GeujpxISRCAGwtvRRwu67Scqot5VVSGx'
CLIENT_SECRET = 'mNVQG01ruRq7GptO'
access_token = get_amadeus_access_token(CLIENT_ID, CLIENT_SECRET)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
secret_file = os.path.join(BASE_DIR,"..", "secret.json")
country_file = os.path.join(BASE_DIR, "main_countries.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 주소 (자신의 주소)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
@app.get("/api/previous/flight_Prices")
async def get_pflight_prices(
    origin: str = Query(...),
    destination: str = Query(...),
    departureDate: str = Query(...),
    currency: str = Query("KRW")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    base_url = "https://test.api.amadeus.com/v1/analytics/itinerary-price-metrics"
    params = f"?originIataCode={origin}&destinationIataCode={destination}&departureDate={departureDate}&currencyCode={currency}&oneWay=true"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(base_url + params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        price_data = {}
        if "data" in data and len(data["data"]) > 0:
            metrics = data["data"][0].get("priceMetrics", [])
            for metric in metrics:
                ranking = metric.get("quartileRanking")
                amount = metric.get("amount")
                if ranking and amount:
                    price_data[ranking] = float(amount)
        return {"Result": True, "price": price_data}
    else:
        return {"Result": False, "message": f"API 호출 실패: {response.status_code}", "details": response.text}

@app.get("/api/flight_Prices")
async def get_flight_prices(
    origin: str = Query(...),
    destination: str = Query(...),
    departureDate: str = Query(...),
    currency: str = Query("KRW")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = f"?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departureDate}&adults=1&currencyCode={currency}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(base_url + params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            amount = float(data["data"][0]["price"]["total"])
            return {"Result": True, "amount": amount}
        else:
            return {"Result": False, "message": "항공권 데이터가 없습니다."}
    else:
        return {"Result": False, "message": f"API 호출 실패: {response.status_code}", "details": response.text}

@app.get("/api/total/flight_Prices")
async def get_total_price_analysis(
    origin: str = Query(...),
    destination: str = Query(...),
    departureDate: str = Query(...),
    currency: str = Query("KRW")
):
    try:
        target_date = datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    # 실시간 가격 요청
    real_response = await get_flight_prices(origin, destination, departureDate, currency)
    if not real_response["Result"]:
        return {"Result": False, "message": "실시간 항공권 데이터를 가져오지 못했습니다."}

    real_price = real_response.get("amount")

    # 과거 1, 2, 3년 데이터 요청
    past_years = [1, 2, 3]
    past_price_metrics = {}

    for y in past_years:
        past_date = (target_date - timedelta(days=365 * y)).strftime("%Y-%m-%d")
        past_response = await get_pflight_prices(origin, destination, past_date, currency)
        if past_response["Result"]:
            past_price_metrics[f"{y}년 전"] = past_response["price"]

    if not past_price_metrics:
        return {"Result": False, "message": "과거 가격 데이터를 가져오지 못했습니다."}

    return {
        "Result": True,
        "real_price": real_price,
        "comparison_reference": "가격 비교는 각 년도의 MEDIUM 기준과 비교 가능",
        "past_price_metrics": past_price_metrics
    }

@app.get("/api/total_final/flight_Prices")
async def get_total_final_price_analysis(
    origin: str = Query(...),
    destination: str = Query(...),
    departureDate: str = Query(...),
    currency: str = Query("KRW")
):
    try:
        target_date = datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    # 실시간 가격 요청
    real_response = await get_flight_prices(origin, destination, departureDate, currency)
    if not real_response["Result"]:
        return {"Result": False, "message": "실시간 항공권 데이터를 가져오지 못했습니다."}

    real_price = real_response.get("amount")

    # 과거 1, 2, 3년 데이터 요청
    past_years = [1, 2, 3]
    past_price_metrics = {}
    medium_values = []

    for y in past_years:
        past_date = (target_date - timedelta(days=365 * y)).strftime("%Y-%m-%d")
        past_response = await get_pflight_prices(origin, destination, past_date, currency)
        if past_response["Result"]:
            quartiles = past_response.get("price", {})
            past_price_metrics[f"{y}년 전"] = quartiles
            medium = quartiles.get("MEDIUM")
            if medium:
                medium_values.append(medium)

    if not past_price_metrics or not medium_values:
        return {"Result": False, "message": "과거 가격 데이터를 가져오지 못했습니다."}

    # 과거 MEDIUM 평균 계산
    avg_medium = sum(medium_values) / len(medium_values)

    # 분석 메시지
    if real_price < avg_medium:
        analysis = f"현재 항공권 가격({real_price:,.0f}원)은 최근 3년간 평균 중간값({avg_medium:,.0f}원)보다 저렴하므로, 지금은 비교적 싸게 구매할 수 있는 시점입니다."
    elif real_price > avg_medium:
        analysis = f"현재 항공권 가격({real_price:,.0f}원)은 최근 3년간 평균 중간값({avg_medium:,.0f}원)보다 비싸므로, 지금은 상대적으로 비싼 시점입니다."
    else:
        analysis = f"현재 항공권 가격은 최근 3년간 평균 중간값과 거의 동일합니다."

    return {
        "Result": True,
        "real_price": real_price,
        "comparison_reference": "가격 비교는 각 년도의 MEDIUM 기준과 비교 가능",
        "past_price_metrics": past_price_metrics,
        "analysis": analysis
    }


def noisy_exponential(x, a=100000, k=0.2, noise_level=0.1):
    base = a * math.exp(k * x)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

@app.get("/api/noise/flight_Prices")
async def get_noise_price_analysis(
    origin: str = Query(...),
    destination: str = Query(...),
    departureDate: str = Query(...),
    currency: str = Query("KRW")
):
    try:
        datetime.strptime(departureDate, "%Y-%m-%d")
    except ValueError:
        return {"Result": False, "message": "departureDate는 YYYY-MM-DD 형식이어야 합니다."}

    # 실시간 가격 요청
    real_response = await get_flight_prices(origin, destination, departureDate, currency)
    if not real_response["Result"]:
        return {"Result": False, "message": "실시간 항공권 데이터를 가져오지 못했습니다."}

    real_price = real_response.get("amount")

    # 노이즈 추가된 과거 시뮬레이션 가격 (1, 2, 3년 전)
    simulated_past_prices = {}
    sim_prices = []
    for year in [1, 2, 3]:
        sim_price = noisy_exponential(year)
        simulated_past_prices[f"{year}년 전"] = round(sim_price, 2)
        sim_prices.append(sim_price)

    # 평균 계산
    avg_sim = sum(sim_prices) / len(sim_prices)

    # 분석 메시지
    if real_price < avg_sim:
        analysis = f"현재 항공권 가격({real_price:,.0f}원)은 과거 평균({avg_sim:,.0f}원)보다 저렴합니다. 지금 구매하세요!."
    elif real_price > avg_sim:
        analysis = f"현재 항공권 가격({real_price:,.0f}원)은 과거 평균({avg_sim:,.0f}원)보다 비쌉니다. 기다려"
    else:
        analysis = f"현재 항공권 가격은 과거 평균이랑 비슷한듯?"

    return {
        "Result": True,
        "real_price": real_price,
        "simulated_past_prices": simulated_past_prices,
        "average_simulated_price": round(avg_sim, 2),
        "analysis": analysis
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)