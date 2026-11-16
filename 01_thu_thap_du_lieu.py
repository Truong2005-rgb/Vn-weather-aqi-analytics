import os
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

# 1. Đọc API key từ biến môi trường hoặc file .env
load_dotenv(Path(__file__).resolve().parent / ".env")
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "").strip()
if not API_KEY or API_KEY == "your_openweathermap_api_key":
    raise SystemExit(
        "Chưa có API key. Sao chép .env.example thành .env, "
        "sau đó điền OPENWEATHERMAP_API_KEY."
    )

# 2. Danh sách 14 địa phương
CITIES = [
    # Miền Bắc
    {"city": "Hà Nội", "region": "Miền Bắc", "lat": 21.0285, "lon": 105.8542},
    {"city": "Hải Phòng", "region": "Miền Bắc", "lat": 20.8449, "lon": 106.6881},
    {"city": "Quảng Ninh", "region": "Miền Bắc", "lat": 20.9500, "lon": 107.0833},
    {"city": "Lào Cai", "region": "Miền Bắc", "lat": 22.4833, "lon": 103.9500},

    # Miền Trung
    {"city": "Đà Nẵng", "region": "Miền Trung", "lat": 16.0544, "lon": 108.2022},
    {"city": "Thừa Thiên Huế", "region": "Miền Trung", "lat": 16.4637, "lon": 107.5909},
    {"city": "Nha Trang", "region": "Miền Trung", "lat": 12.2388, "lon": 109.1967},
    {"city": "Hà Tĩnh", "region": "Miền Trung", "lat": 18.3430, "lon": 105.9058},

    # Miền Nam
    {"city": "TP Hồ Chí Minh", "region": "Miền Nam", "lat": 10.8231, "lon": 106.6297},
    {"city": "Cần Thơ", "region": "Miền Nam", "lat": 10.0452, "lon": 105.7469},
    {"city": "An Giang", "region": "Miền Nam", "lat": 10.5216, "lon": 105.1259},

    # Tây Nguyên
    {"city": "Đà Lạt", "region": "Tây Nguyên", "lat": 11.9404, "lon": 108.4583},
    {"city": "Buôn Ma Thuột", "region": "Tây Nguyên", "lat": 12.6667, "lon": 108.0500},
    {"city": "Pleiku", "region": "Tây Nguyên", "lat": 13.9833, "lon": 108.0000}
]

weather_data = []
air_data = []

print("Bắt đầu truy vấn OpenWeatherMap API...")

for item in CITIES:
    lat, lon, city, region = item["lat"], item["lon"], item["city"], item["region"]

    url_w = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=vi"
    url_a = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    res_w = requests.get(url_w, timeout=10)
    res_a = requests.get(url_a, timeout=10)

    if res_w.status_code == 200 and res_a.status_code == 200:
        dw = res_w.json()
        da = res_a.json()

        weather_data.append({
            "City": city,
            "Region": region,
            "Lat": lat,
            "Lon": lon,
            "Nhiệt độ (°C)": dw["main"]["temp"],
            "Độ ẩm (%)": dw["main"]["humidity"],
            "Áp suất (hPa)": dw["main"]["pressure"],
            "Tốc độ gió (m/s)": dw["wind"]["speed"],
            "Trạng thái": dw["weather"][0]["description"]
        })

        air_data.append({
            "City": city,
            "AQI_Level": da["list"][0]["main"]["aqi"],
            "CO": da["list"][0]["components"]["co"],
            "NO2": da["list"][0]["components"]["no2"],
            "O3": da["list"][0]["components"]["o3"],
            "SO2": da["list"][0]["components"]["so2"],
            "PM2_5": da["list"][0]["components"]["pm2_5"],
            "PM10": da["list"][0]["components"]["pm10"]
        })
    else:
        print(f"❌ Lỗi tại {city}: Mã Thời tiết {res_w.status_code}, Mã AQI {res_a.status_code}")

if len(weather_data) > 0:
    pd.DataFrame(weather_data).to_csv("weather_raw.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(air_data).to_csv("air_raw.csv", index=False, encoding="utf-8-sig")
    print(f"\n Đã lưu {len(weather_data)}/{len(CITIES)} địa phương vào weather_raw.csv và air_raw.csv")