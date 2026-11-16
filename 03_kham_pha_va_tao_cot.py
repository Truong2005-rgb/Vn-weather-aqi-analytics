import pandas as pd

# 1. Đọc dữ liệu hợp nhất từ Bước 3
df = pd.read_csv("vietnam_weather_air_merged.csv")

print("==========================================================")
print("  MỤC 4. KHÁM PHÁ DỮ LIỆU (EDA - EXPLORATORY DATA ANALYSIS)")
print("==========================================================")

# ❓ Câu hỏi 1: Dữ liệu có bao nhiêu bản ghi?
print(f"\n1. Dữ liệu có bao nhiêu bản ghi?")
print(f"-> Tổng số bản ghi (dòng): {len(df)}")

# ❓ Câu hỏi 2, 3 & 4: Cấu trúc dữ liệu, các cột, loại dữ liệu và dữ liệu khuyết thiếu bằng df.info()
print(f"\n2. Cấu trúc dữ liệu và kiểu dữ liệu từng cột (df.info()):")
df.info()

# ❓ Câu hỏi 5: Kiểm tra dữ liệu trùng lặp
print(f"\n3. Kiểm tra dữ liệu trùng lặp:")
print(f"-> Số bản ghi bị trùng lặp (Duplicates): {df.duplicated(subset=['City']).sum()}")

# ❓ Câu hỏi 6: Giá trị lớn nhất, nhỏ nhất và Thống kê mô tả (df.describe())
print(f"\n================= 1. THỐNG KÊ MÔ TẢ (EDA) =================")
print(df.describe())

# ❓ Câu hỏi 7: Dữ liệu phân bố như thế nào? (Tạo cột phân loại)
def categorize_aqi(level):
    if level == 1:
        return "Tốt"
    elif level == 2:
        return "Trung bình"
    elif level == 3:
        return "Kém"
    elif level == 4:
        return "Xấu"
    else:
        return "Rất xấu"

df["Phân loại AQI"] = df["AQI_Level"].apply(categorize_aqi)

def categorize_temp(temp):
    if temp > 32:
        return "Nắng nóng"
    elif temp >= 20:
        return "Mát mẻ / Lý tưởng"
    else:
        return "Trời lạnh"

df["Cảnh báo Nhiệt độ"] = df["Nhiệt độ (°C)"].apply(categorize_temp)

# In danh sách dữ liệu có các cột phân loại mới
print("\n================= 2. DỮ LIỆU SAU KHI TẠO CỘT MỚI =================")
print(df[["City", "Region", "Nhiệt độ (°C)", "PM2.5 (µg/m³)", "Phân loại AQI", "Cảnh báo Nhiệt độ"]])

print("\n-> Phân bố Chất lượng không khí (AQI):")
print(df["Phân loại AQI"].value_counts())

print("\n-> Phân bố Trạng thái Nhiệt độ:")
print(df["Cảnh báo Nhiệt độ"].value_counts())

# Xuất file dữ liệu hoàn chỉnh
df.to_csv("vietnam_weather_air_final.csv", index=False, encoding="utf-8-sig")
print("\nThành công! Đã lưu file hoàn chỉnh: vietnam_weather_air_final.csv")