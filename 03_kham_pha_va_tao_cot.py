import pandas as pd
import matplotlib.pyplot as plt


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 250)

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

# ❓ Câu hỏi 8: Đếm số địa phương theo vùng miền và mức AQI bằng groupby()
print("\n================= 3. SỐ ĐỊA PHƯƠNG THEO VÙNG VÀ MỨC AQI (GROUPBY) =================")
print("\n-> Số địa phương theo Vùng và Mức AQI:")
aqi_theo_vung = df.groupby(["Region", "Phân loại AQI"]).size().reset_index(name="So_dia_phuong")
print(aqi_theo_vung.to_string(index=False))

# Xuất file dữ liệu hoàn chỉnh
df.to_csv("vietnam_weather_air_final.csv", index=False, encoding="utf-8-sig")
print("\nThành công! Đã lưu file hoàn chỉnh: vietnam_weather_air_final.csv")

# ================= PHÂN TÍCH BỔ SUNG  =================
# 4. Thống kê theo vùng miền
print("\n================= 4. THỐNG KÊ THEO VÙNG MIỀN =================")
vung = df.groupby("Region").agg(
    So_dia_phuong=("City", "count"),
    PM25_TB=("PM2.5 (µg/m³)", "mean"),
    PM25_Max=("PM2.5 (µg/m³)", "max"),
    PM10_TB=("PM10 (µg/m³)", "mean"),
    Nhiet_do_TB=("Nhiệt độ (°C)", "mean"),
    Do_am_TB=("Độ ẩm (%)", "mean"),
    Gio_TB=("Tốc độ gió (m/s)", "mean"),
).round(2)
print(vung)

# 5. Xếp hạng PM2.5 từ cao xuống thấp
print("\n================= 5. XẾP HẠNG PM2.5 =================")
xep_hang = df.sort_values("PM2.5 (µg/m³)", ascending=False)[["City", "PM2.5 (µg/m³)", "Phân loại AQI"]]
print(xep_hang.to_string(index=False))

# 6. Hệ số tương quan Pearson
print("\n================= 6. HỆ SỐ TƯƠNG QUAN PEARSON =================")
cot = ["Nhiệt độ (°C)", "Độ ẩm (%)", "Tốc độ gió (m/s)", "PM2.5 (µg/m³)", "PM10 (µg/m³)"]
tuong_quan = df[cot].corr().round(2)
print(tuong_quan)

# 7. Biểu đồ: PM2.5 trung bình theo vùng
plt.figure(figsize=(6, 3.6))
vung["PM25_TB"].sort_values(ascending=False).plot(kind="bar", color="#1f77b4")
plt.ylabel("PM2.5 trung bình (µg/m³)")
plt.xlabel("Vùng miền")
plt.title("PM2.5 trung bình theo vùng miền")
plt.xticks(rotation=0)
plt.tight_layout()

# 8. Biểu đồ: ma trận tương quan
plt.figure(figsize=(6, 4.6))
plt.imshow(tuong_quan, cmap="RdBu_r", vmin=-1, vmax=1)
plt.colorbar(label="Hệ số tương quan r")
plt.xticks(range(len(cot)), cot, rotation=30, ha="right")
plt.yticks(range(len(cot)), cot)
for i in range(len(cot)):
    for j in range(len(cot)):
        r = tuong_quan.iloc[i, j]
        plt.text(j, i, f"{r:.2f}", ha="center", va="center",
                 color="white" if abs(r) > 0.6 else "black")
plt.title("Ma trận tương quan")
plt.tight_layout()

plt.show()
