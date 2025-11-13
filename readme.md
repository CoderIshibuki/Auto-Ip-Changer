# 🌐 Auto IP Changer - Windows

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**Phần mềm tự động thay đổi IP trên Windows** - Công cụ hữu ích cho quản trị mạng, SEO, và những ai cần thay đổi địa chỉ IP thường xuyên.

## 📥 Tải về

**📦 Phiên bản mới nhất:** [AutoIPChanger_Setup.exe](https://github.com/your-repo/auto-ip-changer/releases/latest)

## ✨ Tính năng nổi bật

| Tính năng | Mô tả |
|-----------|--------|
| 🖱️ **Giao diện trực quan** | Dễ sử dụng, hoàn toàn bằng tiếng Việt |
| ⏰ **Thay đổi IP tự động** | Thiết lập thời gian tự động thay đổi IP |
| 🔄 **Thay đổi thủ công** | Thay đổi IP ngay lập tức với một cú click |
| 📊 **Theo dõi trạng thái** | Hiển thị IP hiện tại và nhật ký hoạt động |
| 🎯 **Đa giao diện mạng** | Hỗ trợ Ethernet, Wi-Fi, và các kết nối khác |
| 🔒 **An toàn** | Không thu thập dữ liệu người dùng |

## 🛠️ Yêu cầu hệ thống

- **🖥️ Hệ điều hành:** Windows 7/8/10/11 (64-bit)
- **💾 Bộ nhớ:** Tối thiểu 512MB RAM
- **⚡ Quyền:** Quyền Administrator để thay đổi cấu hình mạng
- **🌐 Kết nối:** Mạng internet hoạt động

## 🚀 Cài đặt

### **Phương pháp 1: Dùng Setup (Khuyến nghị)**
1. **📥 Tải file** `AutoIPChanger_Setup.exe`
2. **🖱️ Chạy file** với quyền **Administrator**
3. **📋 Làm theo hướng dẫn** trong trình cài đặt
4. **🚀 Khởi chạy** từ Desktop shortcut

### **Phương pháp 2: Chạy trực tiếp từ Python**
```bash
# Clone repository
git clone https://github.com/your-repo/auto-ip-changer.git
cd auto-ip-changer

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
python ip_changer_windows.py
```

## 📖 Hướng dẫn sử dụng

### **1. 🎯 Chọn Network Interface**
- Chọn giao diện mạng từ danh sách (Ethernet, Wi-Fi, ...)
- IP hiện tại sẽ tự động hiển thị

### **2. 🔧 Thay đổi IP thủ công**
- Nhấn **"THAY ĐỔI IP NGAY"** để thay đổi IP ngay lập tức
- Hệ thống sẽ release và renew IP

### **3. ⏰ Thiết lập tự động**
- Nhập khoảng thời gian (phút) giữa các lần thay đổi
- Nhấn **"BẮT ĐẦU TỰ ĐỘNG"** để kích hoạt
- Hệ thống sẽ đếm ngược và tự động thay đổi IP

### **4. 📝 Nhật ký hoạt động**
- Theo dõi tất cả hoạt động trong phần nhật ký
- Xem thời gian, trạng thái và kết quả thay đổi IP
- Có thể xóa nhật ký khi cần

## 🛠️ Xây dựng từ mã nguồn

### **Yêu cầu phát triển**
- **Python** 3.8+
- **Thư viện:** `tkinter`, `psutil`, `pyinstaller`

## 🔧 Xử lý sự cố

### **Lỗi thường gặp**

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| ❌ "Không thể thay đổi IP" | Không có quyền Admin | Chạy với quyền Administrator |
| ❌ "Interface không hoạt động" | Interface bị tắt | Bật network interface |
| ❌ "Không có IP" | Mất kết nối mạng | Kiểm tra kết nối internet |

### **💡 Mẹo sử dụng hiệu quả**
- 🕒 **Đặt thời gian tự động** 10-30 phút để tránh bị chặn IP
- 🔄 **Kiểm tra IP mới** sau mỗi lần thay đổi
- 📊 **Theo dõi nhật ký** để phát hiện vấn đề

## 📋 Lệnh Windows được sử dụng

Phần mềm sử dụng các lệnh Windows tiêu chuẩn:

```cmd
ipconfig /release    # Release IP hiện tại
ipconfig /renew      # Renew IP mới
```

## 🏗️ Kiến trúc ứng dụng

```
Auto IP Changer/
├── 📱 Giao diện người dùng (Tkinter)
├── 🔧 Core Engine
│   ├── IP Management
│   ├── Scheduler
│   └── Logger
├── 🌐 Network Interface
│   ├── Interface Detection
│   └── IP Configuration
└── 💾 Data Persistence
    └── Activity Logging
```

## 📄 Giấy phép

Dự án được phân phối theo **giấy phép MIT**.

## 🤝 Đóng góp

Đóng góp luôn được chào đón! Hãy:

1. **Fork** dự án
2. **Tạo branch mới** (`git checkout -b feature/AmazingFeature`)
3. **Commit thay đổi** (`git commit -m 'Add some AmazingFeature'`)
4. **Push đến branch** (`git push origin feature/AmazingFeature`)
5. **Tạo Pull Request**

## ⚠️ Lưu ý quan trọng

- 💡 **Chỉ hoạt động trên Windows**
- 🔒 **Cần quyền Administrator** để thay đổi cấu hình mạng
- 🌐 **IP thay đổi phụ thuộc vào cấu hình DHCP** của nhà cung cấp
- ⚠️ **Sử dụng có trách nhiệm**, không sử dụng cho mục đích bất hợp pháp

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề:

1. **Kiểm tra phần** [Xử lý sự cố](#-xử-lý-sự-cố)
2. **Tạo** [Issue](https://github.com/CoderIshibuki/auto-ip-changer/issues) mới
3. **Mô tả chi tiết** sự cố và cách tái tạo

## 🏆 Người đóng góp

Cảm ơn những người đóng góp đã giúp dự án này tốt hơn!

---

**Made with ❤️ for the Vietnamese developer community**

---
*Phiên bản 1.0.0 - Cập nhật tháng 12/2024*

---
