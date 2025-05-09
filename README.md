# 🏠 Dự án Crawler Nhà Đất Đà Nẵng - alonhadat.com.vn

Script Python tự động thu thập dữ liệu các bài đăng **bán căn hộ chung cư tại Đà Nẵng** từ trang web [alonhadat.com.vn](https://alonhadat.com.vn). Dữ liệu sẽ được lưu vào file Excel để phân tích hoặc lưu trữ.

## 📌 Tính năng nổi bật

- Duyệt tự động qua nhiều trang kết quả để thu thập thông tin.
- Trích xuất các thông tin quan trọng: Tiêu đề, Mô tả, Địa chỉ, Diện tích, Giá.
- Xử lý CAPTCHA nếu phát hiện.
- Nếu không lấy được giá/diện tích từ giao diện chính, script sẽ trích xuất thông tin từ phần mô tả bài viết.
- Lưu dữ liệu thành file Excel `nha_dat_da_nang.xlsx`.
- Tự động chạy hàng ngày vào lúc **06:00 sáng**.

---

## 🛠️ Cài đặt và chạy dự án

Làm theo các bước dưới đây để thiết lập môi trường và chạy chương trình:

### 1. Clone repository từ GitHub

Mở terminal và chạy:

```bash
git clone https://github.com/NguyenHong04/bai_tap_lon.git
cd bai_tap_lon
2. Tạo môi trường ảo (virtual environment)
Khuyến khích bạn sử dụng môi trường ảo để tránh xung đột thư viện.
Trên Windows:
python -m venv venv
.\venv\Scripts\activate
3. Cài đặt các thư viện cần thiết
Cài đặt các thư viện yêu cầu từ file requirements.txt:

pip install -r requirements.txt
4. Chạy chương trình
Sau khi cài đặt xong, bạn có thể chạy chương trình bằng lệnh:

python btl.py

🕓 Lưu ý: Bạn có thể thay đổi thời gian chạy trong btl.py bằng cách chỉnh sửa dòng sau:

schedule.every().day.at("06:00").do(crawl_data)
📁 Cấu trúc thư mục
bai_tap_lon/
├── btl.py             # Script chính thực hiện crawl dữ liệu
├── requirements.txt    # Danh sách thư viện cần cài đặt
└── README.md           # Tài liệu hướng dẫn sử dụng dự án
🧰 Các thư viện sử dụng
selenium: Điều khiển trình duyệt tự động để thu thập dữ liệu từ trang web.

re: Thư viện Python để xử lý các biểu thức chính quy, sử dụng để trích xuất giá và diện tích.

pandas: Dùng để xử lý dữ liệu và lưu vào file Excel.

schedule: Lên lịch tự động cho việc chạy chương trình vào 6 giờ sáng hàng ngày.

openpyxl: Để ghi dữ liệu vào file Excel.