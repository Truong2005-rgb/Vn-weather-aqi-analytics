import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CẤU HÌNH TRANG WEB STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Báo cáo Thời tiết & Chất lượng Không khí VN",
    page_icon="🌤️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. ĐỌC DỮ LIỆU ĐÃ XỬ LÝ
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("vietnam_weather_air_final.csv")

df = load_data()

# -----------------------------------------------------------------------------
# 3. THANH BỘ LỌC BÊN TRÁI (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 Bộ Lọc Dữ Liệu")

# Lọc theo Vùng miền
regions = ["Tất cả"] + list(df["Region"].unique())
selected_region = st.sidebar.selectbox("Chọn Vùng Miền:", regions)

# Áp dụng bộ lọc
if selected_region != "Tất cả":
    df_filtered = df[df["Region"] == selected_region]
else:
    df_filtered = df.copy()

# -----------------------------------------------------------------------------
# 4. TIÊU ĐỀ CHÍNH & CÁC CHỈ SỐ TỔNG QUAN (METRICS)
# -----------------------------------------------------------------------------
st.title("🌤️ DASHBOARD THỜI TIẾT & CHẤT LƯỢNG KHÔNG KHÍ VIỆT NAM")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng số tỉnh/thành", len(df_filtered))
col2.metric("Nhiệt độ trung bình", f"{df_filtered['Nhiệt độ (°C)'].mean():.1f} °C")
col3.metric("Bụi PM2.5 trung bình", f"{df_filtered['PM2.5 (µg/m³)'].mean():.1f} µg/m³")
col4.metric("Số tỉnh AQI Tốt", len(df_filtered[df_filtered["Phân loại AQI"] == "Tốt"]))

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. HÀNG 1: BIỂU ĐỒ CỘT BỤI PM2.5 & BIỂU ĐỒ TRÒN PHÂN BỐ AQI
# -----------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📊 Nồng độ Bụi PM2.5 theo Thành phố")
    fig_pm25 = px.bar(
        df_filtered,
        x="City",
        y="PM2.5 (µg/m³)",
        color="Phân loại AQI",
        text_auto=".1f",
        labels={"City": "Thành phố", "PM2.5 (µg/m³)": "PM2.5 (µg/m³)"},
        title="Mức độ ô nhiễm PM2.5 tại từng Tỉnh/Thành"
    )
    st.plotly_chart(fig_pm25, use_container_width=True)

with row1_col2:
    st.subheader("🍕 Tỷ lệ Phân bố Chất lượng Không khí (AQI)")
    fig_pie = px.pie(
        df_filtered,
        names="Phân loại AQI",
        title="Tỷ lệ % các mức độ chất lượng không khí",
        hole=0.4, # Tạo dạng Donut chart hiện đại
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. HÀNG 2: BẢN ĐỒ TỌA ĐỘ VỊ TRÍ & BIỂU ĐỒ SCATTER NHIỆT ĐỘ - ĐỘ ẨM
# -----------------------------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🗺️ Bản đồ Phân bố Mức độ Ô nhiễm (Tọa độ)")
    fig_map = px.scatter_geo(
        df_filtered,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        size="PM2.5 (µg/m³)",
        color="Phân loại AQI",
        projection="natural earth",
        title="Vị trí Địa lý & Mức độ Ô nhiễm PM2.5",
        fitbounds="locations" # Tự động zoom vừa khít các tỉnh Việt Nam
    )
    fig_map.update_geos(
        showland=True, landcolor="lightgray",
        showcountries=True, countrycolor="white",
        showocean=True, oceancolor="azure"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with row2_col2:
    st.subheader("🌡️ Mối liên hệ Nhiệt độ & Độ ẩm")
    fig_temp = px.scatter(
        df_filtered,
        x="Nhiệt độ (°C)",
        y="Độ ẩm (%)",
        color="Cảnh báo Nhiệt độ",
        size="Tốc độ gió (m/s)",
        hover_name="City",
        title="Tương quan giữa Nhiệt độ, Độ ẩm và Tốc độ gió"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. BẢNG DỮ LIỆU CHI TIẾT
# -----------------------------------------------------------------------------
st.subheader("📋 Bảng Dữ Liệu Chi Tiết")
st.dataframe(df_filtered, use_container_width=True)