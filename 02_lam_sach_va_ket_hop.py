import pandas as pd

# 1. Đọc 2 file CSV thô vừa thu thập ở Bước 2
df_weather = pd.read_csv("weather_raw.csv")
df_air = pd.read_csv("air_raw.csv")

print("--- 1. KIỂM TRA DỮ LIỆU THÔ BAN ĐẦU ---")
print(f"Số bản ghi Thời tiết: {len(df_weather)}")
print(f"Số bản ghi AQI: {len(df_air)}")

# 2. Xóa các bản ghi trùng lặp (Deduplication) nếu có
df_weather = df_weather.drop_duplicates(subset=["City"])
df_air = df_air.drop_duplicates(subset=["City"])

# 3. Kiểm tra giá trị khuyết thiếu (Missing Values)
missing_w = df_weather.isnull().sum().sum()
missing_a = df_air.isnull().sum().sum()
print(f"Số giá trị thiếu (Weather): {missing_w}")
print(f"Số giá trị thiếu (AQI): {missing_a}")

# 4. Gộp 2 bảng dữ liệu (Merge INNER JOIN) theo cột "City"
df_merged = pd.merge(df_weather, df_air, on="City", how="inner")

# 5. Đổi tên cột chuẩn hóa để dễ làm biểu đồ
df_merged = df_merged.rename(columns={
    "PM2_5": "PM2.5 (µg/m³)",
    "PM10": "PM10 (µg/m³)"
})

print("\n--- 2. KẾT QUẢ SAU KHI GỘP DỮ LIỆU ---")
print(f"Kích thước bảng hợp nhất: {df_merged.shape[0]} dòng, {df_merged.shape[1]} cột")

# 6. Xuất ra file dữ liệu đã hợp nhất
df_merged.to_csv("vietnam_weather_air_merged.csv", index=False, encoding="utf-8-sig")
print("\n Đã xuất file thành công: vietnam_weather_air_merged.csv")