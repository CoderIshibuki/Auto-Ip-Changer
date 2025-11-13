# 🚀 Auto IP Changer v3 - Modern UI (Windows)

## 📝 Giới thiệu

Auto IP Changer v3 là một công cụ tiện ích mạnh mẽ được thiết kế để tự động thay đổi địa chỉ IPv4 của máy tính Windows (thường được cấp bởi DHCP Server của Router) một cách định kỳ hoặc thủ công.

Ứng dụng này sử dụng các lệnh PowerShell và Netsh ở chế độ quản trị (Administrator) để buộc Network Adapter phải xin cấp phát một IP mới, giúp người dùng dễ dàng đổi IP khi cần thiết.

**Lưu ý quan trọng:** Ứng dụng này yêu cầu quyền Administrator để thực hiện các thao tác thay đổi cấu hình mạng.

## ✨ Tính năng nổi bật

- **Giao diện hiện đại (Modern UI):** Xây dựng bằng CustomTkinter với chế độ Tối/Sáng.
- **Chạy ở chế độ Administrator:** Tự động kiểm tra và yêu cầu quyền Admin để đảm bảo thao tác mạng thành công.
- **Nhiều phương pháp đổi IP:**
  - **DHCP Release/Renew (Cơ bản):** Phương pháp truyền thống.
  - **Khởi động lại Adapter (Mạnh):** Tắt/bật Network Adapter bằng PowerShell.
  - **Cấp mới (Release + Restart) (Rất Mạnh):** Kết hợp Release, Restart Adapter, và Renew để tối đa hóa khả năng đổi IP.
  - **Reconnect WiFi:** Tùy chọn dành riêng cho các kết nối WiFi.
  - **Ngẫu nhiên (Random):** Tự động chọn một phương pháp bất kỳ sau mỗi lần chạy.
- **Chế độ Tự động:** Tự động thay đổi IP sau một khoảng thời gian (phút) được thiết lập.
- **Nhật ký hoạt động (Log):** Ghi lại chi tiết quá trình thay đổi IP và các lỗi phát sinh.
- **Tương thích:** Chỉ dành cho hệ điều hành Windows.

## 🛠️ Yêu cầu hệ thống

- **Hệ điều hành:** Windows 10/11
- **Python 3.x** (Chỉ cần nếu chạy file .py trực tiếp)
- **Thư viện Python:** customtkinter và psutil.

## 📦 Cài đặt và sử dụng

Bạn có 2 lựa chọn để sử dụng ứng dụng: Cài đặt bằng file Setup (khuyến nghị) hoặc chạy trực tiếp từ mã nguồn Python.

### Tùy chọn 1: Cài đặt bằng File Setup (Khuyến nghị)

Nếu bạn đã đóng gói thành công file setup.exe theo hướng dẫn, hãy làm theo các bước sau:

1. Tải file `setup-auto-ip-changer-v3.exe`.
2. Chạy file `setup-auto-ip-changer-v3.exe`. Trình cài đặt sẽ tự động yêu cầu quyền Admin.
3. Làm theo hướng dẫn trên màn hình. Chương trình sẽ được cài đặt vào thư mục Program Files.
4. Sau khi cài đặt, bạn có thể chạy ứng dụng từ Desktop hoặc Start Menu.

### Tùy chọn 2: Chạy từ Mã nguồn Python

1. **Clone Repository** (Nếu có) hoặc tải file:
```bash
git clone [LINK_REPO_CỦA_BẠN]
cd [TÊN_THƯ_MỤC]
```

2. **Cài đặt các thư viện cần thiết:**
```bash
pip install customtkinter psutil
```

3. **Chạy ứng dụng (QUAN TRỌNG):**
   Bạn **BẮT BUỘC** phải chạy file với quyền Administrator.
   - Nhấn chuột phải vào file `auto_ip_changer_v2.py`.
   - Chọn **"Run as Administrator"** (Chạy với quyền Quản trị viên).

## 🖥️ Hướng dẫn sử dụng cơ bản

1. **Chọn Network Interface:**
   - Sử dụng nút "🔄 Làm mới Interface" để quét các card mạng đang hoạt động.
   - Chọn đúng card mạng mà bạn muốn thay đổi IP (ví dụ: Wi-Fi, Ethernet).

2. **Chọn Phương pháp:**
   - Chọn một trong các Radio Button để xác định cơ chế thay đổi IP. Phương pháp "Cấp mới (Release + Restart) (Rất Mạnh)" thường hiệu quả nhất.

3. **Thay đổi thủ công:**
   - Nhấn nút "🔄 THAY ĐỔI IP NGAY" để thực hiện thay đổi IP một lần duy nhất.

4. **Chế độ Tự động:**
   - Nhập khoảng thời gian mong muốn (phút) vào ô "Khoảng (phút)".
   - Nhấn nút "🚀 BẮT ĐẦU TỰ ĐỘNG". Ứng dụng sẽ thay đổi IP định kỳ theo thời gian bạn đã đặt. Nhấn lại nút để "⏹️ DỪNG TỰ ĐỘNG".

## 📄 Thông tin cấp phép

Dự án này được cấp phép theo Giấy phép MIT. Xem tệp LICENSE để biết thêm chi tiết.