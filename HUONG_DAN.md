# Hướng dẫn chạy và đăng dự án lên GitHub

## 1. Bộ file này gồm những gì?

- 4 file Python và 4 file CSV từ dự án bạn đã cung cấp.
- `README.md` bằng tiếng Anh để giới thiệu dự án với người tuyển dụng.
- `requirements.txt`: các thư viện cần cài.
- `.env.example`: mẫu cấu hình API key, không chứa khóa thật.
- `.gitignore`: loại trừ `.env`, môi trường ảo và file tạm khi dùng Git.
- `docs/`: ảnh dashboard trích từ báo cáo gốc.

Ảnh báo cáo và CSV thuộc hai lần thu thập khác nhau nên các số đo có thể khác nhau. README đã giải thích điều này; không dùng ảnh để khẳng định số đo của bản CSV hiện tại.

## 2. Đăng bằng giao diện GitHub

1. Giải nén file ZIP trên máy. Mở thư mục `vn-weather-aqi-analytics` bên trong.
2. Đăng nhập tài khoản `Truong2005-rgb`, mở https://github.com/new.
3. Đặt tên repository: `vn-weather-aqi-analytics`.
4. Mô tả có thể dùng: `Python data collection, analysis and interactive visualization of weather and air quality across 14 locations in Vietnam.`
5. Chọn **Public** nếu muốn người tuyển dụng mở xem mà không cần cấp quyền. Không chọn tạo sẵn README, .gitignore hoặc license, vì bộ file đã có README và .gitignore.
6. Bấm **Create repository**.
7. Tại trang hướng dẫn repository mới, bấm **uploading an existing file**. Nếu repository đã có file, chọn **Add file → Upload files**.
8. Kéo toàn bộ nội dung BÊN TRONG thư mục đã giải nén vào vùng tải lên, gồm thư mục `docs`. Không chỉ tải file ZIP; không kéo thêm một thư mục cha bao ngoài.
9. Kiểm tra có `README.md`, `requirements.txt`, 4 file `.py`, 4 file `.csv`, `.env.example`, `.gitignore`, `HUONG_DAN.md` và ảnh trong `docs`.
10. Nhập nội dung commit: `Add weather and air quality analytics project`. Bấm **Commit changes**.
11. Kiểm tra README hiển thị ở trang đầu và hai ảnh mở được.

Lưu ý: GitHub không tự chạy dashboard khi bạn tải file lên. Đây là nơi xem mã nguồn và hướng dẫn chạy. Đường dẫn repo dự kiến là:

https://github.com/Truong2005-rgb/vn-weather-aqi-analytics

Link này chỉ có nội dung sau khi bạn thực sự tạo repository và tải file lên.

## 3. Xem dashboard bằng CSV mẫu

Mở terminal trong thư mục dự án. Thực hiện các lệnh tạo/kích hoạt môi trường theo README, sau đó chạy:

```text
python -m pip install -r requirements.txt
python -m streamlit run 04_dashboard_app.py
```

Không cần API key nếu chỉ dùng dữ liệu mẫu đã có. Mở địa chỉ localhost Streamlit in ra.

## 4. Lấy dữ liệu mới

- Sao chép `.env.example` thành `.env` và điền API key OpenWeatherMap của bạn.
- Chạy file 01 → 02 → 03 rồi khởi động lại dashboard; dữ liệu CSV cũ sẽ được thay bằng lần thu thập mới.
- Không đăng `.env` hoặc khóa thật lên GitHub. Khi tải thủ công bằng trình duyệt, bạn vẫn phải tự kiểm tra các file đã chọn: `.gitignore` không ngăn việc tải file qua giao diện web.
- Khóa từng được ghi trực tiếp trong bộ code gốc. Nếu khóa đó từng bị công khai, hãy thu hồi/thay khóa trong tài khoản OpenWeatherMap.

## 5. Những gì đã được kiểm tra khi đóng gói

- Cú pháp 4 file Python.
- Tái chạy xử lý 02 và 03 với CSV mẫu, đối chiếu bảng đầu ra.
- Bộ dữ liệu cuối 14 dòng, 18 cột, không thiếu dữ liệu hoặc trùng địa phương.
- File ZIP không có API key gốc hoặc file `.env` chứa khóa thật.

Chưa chạy lại API bằng khóa thật, chưa kiểm tra giao diện Streamlit trực tiếp trong lần đóng gói này và chưa đăng bất kỳ file nào lên tài khoản GitHub.
