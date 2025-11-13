#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
import re
import sys
import ctypes
from datetime import datetime
import random

# ===== KIỂM TRA THƯ VIỆN (QUAN TRỌNG) =====
try:
    import psutil
    import customtkinter
except ImportError as e:
    missing_lib = "psutil"
    if "customtkinter" in str(e):
        missing_lib = "customtkinter"
        
    root_check = tk.Tk()
    root_check.withdraw()
    messagebox.showerror("Lỗi Thiếu Thư Viện", 
                         f"Không tìm thấy thư viện '{missing_lib}'.\n"
                         "Vui lòng mở 'cmd' với quyền Admin và chạy lệnh:\n\n"
                         f"pip install {missing_lib}\n\n"
                         "(Hoặc chạy: pip install customtkinter psutil)\n"
                         "Sau đó chạy lại ứng dụng.")
    root_check.destroy()
    sys.exit()

# ===== CÀI ĐẶT GIAO DIỆN HIỆN ĐẠI =====
customtkinter.set_appearance_mode("Dark")  # "Dark", "Light", hoặc "System"
customtkinter.set_default_color_theme("blue") # Theme màu

class AutoIPChangerWindows(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Auto IP Changer v3 - Modern UI (Admin Mode)")
        self.geometry("800x750") # Tăng chiều cao một chút cho thoáng
        self.resizable(True, True)

        self.is_auto_running = False
        self.auto_thread = None
        self.change_method = tk.StringVar(value="aggressive_renew") 
        
        self.setup_ui()
        self.network_interfaces = self.refresh_network_interfaces()
        self.update_interface_list() # Cập nhật combobox
        self.update_current_ip()

    def setup_ui(self):
        # Cấu hình grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Cho phép log frame mở rộng

        # === Frame Thông tin mạng ===
        info_frame = customtkinter.CTkFrame(self, corner_radius=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        info_frame.grid_columnconfigure(1, weight=1)

        info_title = customtkinter.CTkLabel(info_frame, text="📶 Thông tin mạng", font=("Segoe UI", 14, "bold"))
        info_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))

        customtkinter.CTkLabel(info_frame, text="Network Interface:").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.interface_var = tk.StringVar()
        self.interface_combo = customtkinter.CTkComboBox(info_frame, variable=self.interface_var, 
                                                         values=["Đang tải..."], state="readonly", width=300)
        self.interface_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        self.refresh_if_btn = customtkinter.CTkButton(info_frame, text="🔄 Làm mới Interface", 
                                                 command=self.refresh_interfaces_ui, width=150)
        self.refresh_if_btn.grid(row=1, column=2, padx=(5, 15), pady=5)
        
        customtkinter.CTkLabel(info_frame, text="IP hiện tại:").grid(row=2, column=0, sticky="w", padx=15, pady=(5, 15))
        self.current_ip_var = tk.StringVar(value="...")
        ip_label = customtkinter.CTkLabel(info_frame, textvariable=self.current_ip_var, 
                                         font=("Segoe UI", 11, "bold"), text_color="#3498db")
        ip_label.grid(row=2, column=1, sticky="w", pady=(5, 15), padx=5)
        
        self.refresh_ip_btn = customtkinter.CTkButton(info_frame, text="🔄 Làm mới IP", 
                                                 command=self.update_current_ip, width=150)
        self.refresh_ip_btn.grid(row=2, column=2, padx=(5, 15), pady=(5, 15))

        # === Frame Phương pháp ===
        method_frame = customtkinter.CTkFrame(self, corner_radius=10)
        method_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        method_title = customtkinter.CTkLabel(method_frame, text="🔧 Phương pháp thay đổi IP", font=("Segoe UI", 14, "bold"))
        method_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))

        methods = [
            ("DHCP Release/Renew (Cơ bản)", "dhcp_renew"),
            ("Khởi động lại Adapter (Mạnh)", "adapter_restart"),
            ("Cấp mới (Release + Restart) (Rất Mạnh)", "aggressive_renew"),
            ("Reconnect WiFi (Chỉ cho WiFi)", "wlan_reconnect"),
            ("Ngẫu nhiên (1 trong 4 trên)", "random")
        ]
        
        radio_frame = customtkinter.CTkFrame(method_frame, fg_color="transparent")
        radio_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 15))
        
        for i, (text, value) in enumerate(methods):
            customtkinter.CTkRadioButton(radio_frame, text=text, variable=self.change_method, 
                                        value=value).grid(row=i % 3, column=i // 3, sticky="w", pady=5, padx=10)

        # === Frame Điều khiển ===
        control_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="transparent")
        control_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        # Frame Thủ công
        manual_frame = customtkinter.CTkFrame(control_frame)
        manual_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        manual_frame.grid_columnconfigure(0, weight=1)

        manual_title = customtkinter.CTkLabel(manual_frame, text="🤚 Thay đổi thủ công", font=("Segoe UI", 14, "bold"))
        manual_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        manual_btn = customtkinter.CTkButton(manual_frame, text="🔄 THAY ĐỔI IP NGAY", 
                                             command=self.change_ip_manual,
                                             font=("Segoe UI", 12, "bold"),
                                             height=40)
        manual_btn.grid(row=1, column=0, sticky="ew", pady=(10, 15), padx=15)
        
        # Frame Tự động
        auto_frame = customtkinter.CTkFrame(control_frame)
        auto_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        auto_frame.grid_columnconfigure(1, weight=1)

        auto_title = customtkinter.CTkLabel(auto_frame, text="⏰ Tự động thay đổi", font=("Segoe UI", 14, "bold"))
        auto_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))

        customtkinter.CTkLabel(auto_frame, text="Khoảng (phút):").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.interval_var = tk.StringVar(value="10")
        interval_entry = customtkinter.CTkEntry(auto_frame, textvariable=self.interval_var,
                                                 width=100)
        interval_entry.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        self.auto_button = customtkinter.CTkButton(auto_frame, text="🚀 BẮT ĐẦU TỰ ĐỘNG", 
                                                    command=self.toggle_auto_mode,
                                                    font=("Segoe UI", 12, "bold"),
                                                    height=40)
        self.auto_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 5), padx=15)
        
        self.auto_status_var = tk.StringVar(value="Chế độ tự động: Chưa kích hoạt")
        self.auto_status_label = customtkinter.CTkLabel(auto_frame, textvariable=self.auto_status_var, 
                                                       text_color="#e02f2f", font=("Segoe UI", 9, "bold"))
        self.auto_status_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # === Frame Log ===
        log_frame = customtkinter.CTkFrame(self, corner_radius=10)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        log_title = customtkinter.CTkLabel(log_frame, text="📝 Nhật ký hoạt động", font=("Segoe UI", 14, "bold"))
        log_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))

        self.log_text = customtkinter.CTkTextbox(log_frame, font=("Consolas", 11), wrap=tk.WORD,
                                                 corner_radius=8, border_width=1)
        self.log_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 10))
        
        log_btn_frame = customtkinter.CTkFrame(log_frame, fg_color="transparent")
        log_btn_frame.grid(row=2, column=0, columnspan=2, sticky="e", padx=15, pady=(0, 10))
        
        customtkinter.CTkButton(log_btn_frame, text="🗑️ Xóa log", command=self.clear_log, width=100, fg_color="#555", hover_color="#333").grid(row=0, column=0, padx=5)
        customtkinter.CTkButton(log_btn_frame, text="💾 Lưu log", command=self.save_log, width=100).grid(row=0, column=1, padx=5)
        

    def refresh_interfaces_ui(self):
        self.log_message("🔄 Đang làm mới danh sách Network Interface...")
        self.network_interfaces = self.refresh_network_interfaces()
        self.update_interface_list()
        self.update_current_ip()
        
    def update_interface_list(self):
        interface_names = [display for _, display in self.network_interfaces]
        if not interface_names:
            interface_names = ["Không tìm thấy interface"]
            
        self.interface_combo.configure(values=interface_names)
        self.interface_combo.set(interface_names[0])
        self.log_message(f"👍 Đã tìm thấy {len(self.network_interfaces)} interface đang hoạt động.")

    # ===== Các hàm logic (Giữ nguyên) =====

    def refresh_network_interfaces(self):
        """Lấy danh sách các interface mạng đang 'Up' (hoạt động)"""
        interfaces = []
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            for interface_name in addrs:
                if interface_name in stats and stats[interface_name].isup:
                    ip_address = "Không có IP"
                    for addr in addrs[interface_name]:
                        if addr.family == 2: # AF_INET (IPv4)
                            ip_address = addr.address
                            break
                    
                    actual_ip = self.get_current_ip_windows(interface_name)
                    if re.match(r'\d+\.\d+\d+\.\d+', actual_ip):
                        ip_address = actual_ip
                    
                    display_name = f"{interface_name} ({ip_address})"
                    interfaces.append((interface_name, display_name))
        except Exception as e:
            self.log_message(f"Lỗi khi lấy interface: {e}")
            interfaces = [("Wi-Fi", "Wi-Fi"), ("Ethernet", "Ethernet")]
        
        return interfaces if interfaces else [("Wi-Fi", "Wi-Fi (Không tìm thấy)")]

    def get_current_ip_windows(self, interface_name):
        """Lấy IP hiện tại bằng cách phân tích 'ipconfig'"""
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            lines = result.stdout.split('\n')
            found = False
            for line in lines:
                if interface_name.lower() in line.lower() and 'adapter' in line.lower():
                    found = True
                    continue
                if found and ('ipv4' in line.lower() or 'ip address' in line.lower()):
                    parts = line.split(':')
                    if len(parts) > 1:
                        ip = parts[1].strip()
                        if re.match(r'\d+\.\d+\.\d+\.\d+', ip):
                            return ip
            return "Không có IP"
        except Exception as e:
            self.log_message(f"Lỗi get_current_ip: {e}")
            return "Không có IP"

    def check_internet_connection(self):
        """Kiểm tra kết nối Internet bằng cách ping Google DNS"""
        try:
            result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False

    def wait_for_internet(self, timeout=30):
        self.log_message("🌐 Đang chờ kết nối Internet...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_internet_connection():
                self.log_message("✅ Đã kết nối Internet")
                return True
            time.sleep(2)
        self.log_message("⚠️ Chưa thể kết nối Internet (Timeout)")
        return False

    def change_ip_dhcp_renew(self, interface_name):
        self.log_message("🔧 Phương pháp: DHCP Release/Renew (Cơ bản)")
        subprocess.run("ipconfig /release", shell=True, capture_output=True)
        time.sleep(3)
        subprocess.run("ipconfig /renew", shell=True, capture_output=True)
        time.sleep(5)
        return True

    def change_ip_wlan_reconnect(self, interface_name):
        self.log_message("🔧 Phương pháp: WiFi Reconnect")
        subprocess.run("netsh wlan disconnect", shell=True, capture_output=True)
        time.sleep(3)
        subprocess.run(f'netsh wlan connect name=(Tên profile WiFi của bạn)', shell=True, capture_output=True)
        self.log_message("Lưu ý: Cần thay (Tên profile WiFi) trong code để kết nối")
        time.sleep(8)
        return True

    def change_ip_adapter_restart(self, interface_name):
        self.log_message("🔧 Phương pháp: Khởi động lại Adapter (Mạnh)")
        command = f'powershell -Command "Restart-NetAdapter -Name \'{interface_name}\' -Confirm:$false"'
        subprocess.run(command, shell=True, capture_output=True)
        self.log_message("...Đã tắt/bật card mạng, đang chờ 10s...")
        time.sleep(10)
        subprocess.run("ipconfig /renew", shell=True, capture_output=True)
        time.sleep(5)
        return True

    def change_ip_aggressive_renew(self, interface_name):
        self.log_message("🔧 Phương pháp: Cấp mới (Release + Restart) (Rất Mạnh)")
        self.log_message("...Bước 1: ipconfig /release")
        subprocess.run("ipconfig /release", shell=True, capture_output=True)
        time.sleep(2)
        self.log_message("...Bước 2: Khởi động lại Adapter (PowerShell)")
        command = f'powershell -Command "Restart-NetAdapter -Name \'{interface_name}\' -Confirm:$false"'
        subprocess.run(command, shell=True, capture_output=True)
        self.log_message("...Đang chờ card mạng khởi động (10s)...")
        time.sleep(10)
        self.log_message("...Bước 3: ipconfig /renew")
        subprocess.run("ipconfig /renew", shell=True, capture_output=True)
        time.sleep(5)
        return True

    def change_ip_windows(self, interface_name):
        self.log_message(f"🔄 Bắt đầu thay đổi IP trên '{interface_name}'...")
        old_ip = self.get_current_ip_windows(interface_name)
        self.log_message(f"📝 IP hiện tại: {old_ip}")
        method = self.change_method.get()
        success = False

        methods_map = {
            "dhcp_renew": self.change_ip_dhcp_renew,
            "wlan_reconnect": self.change_ip_wlan_reconnect,
            "adapter_restart": self.change_ip_adapter_restart,
            "aggressive_renew": self.change_ip_aggressive_renew
        }
        
        chosen_method_func = None

        if method == "random":
            random_key = random.choice(list(methods_map.keys()))
            chosen_method_func = methods_map[random_key]
            self.log_message(f"🎲 Chọn phương pháp ngẫu nhiên: {random_key}")
        elif method in methods_map:
            chosen_method_func = methods_map[method]
        else:
            self.log_message(f"Lỗi: không rõ phương pháp '{method}'")
            return False

        try:
            success = chosen_method_func(interface_name)
        except Exception as e:
            self.log_message(f"❌ Lỗi khi thực thi phương pháp: {e}")
            success = False

        if success:
            self.wait_for_internet()
            time.sleep(5) # Chờ IP ổn định
            new_ip = self.get_current_ip_windows(interface_name)
            self.log_message(f"📝 IP mới: {new_ip}")
            if new_ip != old_ip and new_ip != "Không có IP" and re.match(r'\d+\.\d+\.\d+\.\d+', new_ip):
                self.log_message("✅ Thay đổi IP thành công!")
                return True
            elif new_ip == "Không có IP":
                self.log_message("❌ Lỗi: Không thể lấy IP mới (Mất kết nối?)")
                return False
            else:
                self.log_message("⚠️ IP không đổi (DHCP server cấp lại IP cũ)")
                return False
        else:
            self.log_message("❌ Phương pháp thay đổi IP thất bại")
            return False

    def log_message(self, message):
        def _log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            # CTkTextbox không có insert(tk.END...)
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
        
        # Đảm bảo log_text đã được tạo
        if hasattr(self, 'log_text'):
            self.after(0, _log)
        else:
            # Hàng đợi tin nhắn nếu UI chưa sẵn sàng (hiếm khi)
            self.after(500, lambda: self.log_message(message))


    def clear_log(self):
        self.log_text.delete(1.0, "end")

    def save_log(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ip_changer_log_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, "end"))
            self.log_message(f"💾 Đã lưu log vào: {filename}")
            messagebox.showinfo("Thành công", f"Đã lưu log vào:\n{filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu log: {e}")

    def update_current_ip(self):
        if not self.network_interfaces:
            self.current_ip_var.set("Không có interface")
            return
        
        selected_display = self.interface_var.get()
        interface_name = self.get_interface_name_from_display(selected_display)
        
        if not interface_name:
            self.current_ip_var.set("Lỗi chọn interface")
            return

        current_ip = self.get_current_ip_windows(interface_name)
        self.current_ip_var.set(current_ip)
        if not self.is_auto_running:
            self.log_message(f"📡 IP trên '{interface_name}': {current_ip}")
            
    def get_interface_name_from_display(self, display_name):
        for name, display in self.network_interfaces:
            if display == display_name:
                return name
        if display_name in [name for name, _ in self.network_interfaces]:
            return display_name
            
        self.log_message(f"Lỗi: Không tìm thấy tên interface từ '{display_name}'")
        # Trường hợp default "Đang tải..."
        if self.network_interfaces:
            return self.network_interfaces[0][0]
        return None

    def change_ip_manual(self):
        if not self.network_interfaces:
            messagebox.showerror("Lỗi", "Không có network interface nào!")
            return
            
        selected_display = self.interface_var.get()
        interface_name = self.get_interface_name_from_display(selected_display)

        if not interface_name:
            messagebox.showerror("Lỗi", f"Interface '{selected_display}' không hợp lệ. Hãy làm mới danh sách.")
            return

        thread = threading.Thread(target=self._change_ip_process, args=(interface_name, "thủ công"))
        thread.daemon = True
        thread.start()

    def _change_ip_process(self, interface_name, mode="thủ công"):
        try:
            self.log_message(f"🎯 Bắt đầu thay đổi IP {mode} trên '{interface_name}'...")
            success = self.change_ip_windows(interface_name)
            
            def update_ui_after_change():
                new_ip = self.get_current_ip_windows(interface_name)
                self.current_ip_var.set(new_ip)
                if success:
                    self.log_message(f"✅ Hoàn thành thay đổi IP {mode}!")
                else:
                    self.log_message(f"❌ Thay đổi IP {mode} thất bại!")
            
            self.after(0, update_ui_after_change)
            
        except Exception as e:
            self.log_message(f"❌ Lỗi không xác định: {e}")

    def toggle_auto_mode(self):
        if not self.is_auto_running:
            self.start_auto_mode()
        else:
            self.stop_auto_mode()

    def start_auto_mode(self):
        try:
            interval = int(self.interval_var.get())
            if interval < 1:
                messagebox.showerror("Lỗi", "Khoảng thời gian phải >= 1 phút!")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Khoảng thời gian phải là số!")
            return

        selected_display = self.interface_var.get()
        interface_name = self.get_interface_name_from_display(selected_display)
        
        if not interface_name:
            messagebox.showerror("Lỗi", f"Interface '{selected_display}' không hợp lệ. Hãy làm mới danh sách.")
            return

        self.is_auto_running = True
        # Lấy màu "stop"
        self.auto_button.configure(text="⏹️ DỪNG TỰ ĐỘNG", fg_color="#e02f2f", hover_color="#b02020")
        self.auto_status_label.configure(text_color="#107C10") # Green
        self.auto_status_var.set(f"Chế độ tự động: Đang chạy - Thay đổi mỗi {interval} phút")
        self.log_message(f"🚀 BẮT ĐẦU chế độ tự động")
        self.log_message(f"📡 Interface: {interface_name}")
        self.log_message(f"⏰ Interval: {interval} phút")
        self.log_message(f"🔧 Phương pháp: {self.change_method.get()}")
        
        self.auto_thread = threading.Thread(target=self._auto_mode_worker, args=(interface_name, interval))
        self.auto_thread.daemon = True
        self.auto_thread.start()

    def stop_auto_mode(self):
        self.is_auto_running = False
        # Lấy màu "start" (default)
        default_color = customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
        default_hover = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
        self.auto_button.configure(text="🚀 BẮT ĐẦU TỰ ĐỘNG", fg_color=default_color, hover_color=default_hover)
        self.auto_status_label.configure(text_color="#e02f2f") # Red
        self.auto_status_var.set("Chế độ tự động: Đã dừng")
        self.log_message("🛑 ĐÃ DỪNG chế độ tự động")

    def _auto_mode_worker(self, interface_name, interval_minutes):
        interval_seconds = interval_minutes * 60
        while self.is_auto_running:
            try:
                for i in range(interval_seconds):
                    if not self.is_auto_running:
                        return
                    
                    if i % 30 == 0:
                        remaining = interval_seconds - i
                        minutes = remaining // 60
                        seconds = remaining % 60
                        status = f"Chế độ tự động: Đang chạy - Còn {minutes}:{seconds:02d}"
                        self.after(0, lambda s=status: self.auto_status_var.set(s))
                    
                    time.sleep(1)
                
                if self.is_auto_running:
                    self.log_message(f"⏰ Tự động thay đổi IP (mỗi {interval_minutes} phút)")
                    self._change_ip_process(interface_name, "tự động")
            except Exception as e:
                self.log_message(f"❌ Lỗi trong chế độ tự động: {e}")
                time.sleep(10)

def main():
    root_check = tk.Tk()
    root_check.withdraw()

    try:
        is_admin = (ctypes.windll.shell32.IsUserAnAdmin() == 1)
    except:
        is_admin = False

    if not is_admin:
        messagebox.showerror("Lỗi Quyền Hạn (Administrator)", 
                             "Không thể chạy ứng dụng.\n\n"
                             "Vui lòng chạy file này bằng cách:\n"
                             "1. Nhấn chuột phải vào file .py\n"
                             "2. Chọn 'Run as Administrator'")
        root_check.destroy()
        sys.exit()

    root_check.destroy()
    
    # Khởi chạy app CTk
    app = AutoIPChangerWindows()
    
    # Ghi log chào mừng (cần app.after để đảm bảo log_text tồn tại)
    def welcome_logs():
        app.log_message("=" * 60)
        app.log_message("🚀 AUTO IP CHANGER v3 - MODERN UI (ADMIN)")
        app.log_message("=" * 60)
        app.log_message("✅ Đã chạy với quyền Administrator.")
        app.log_message("✅ Đã tìm thấy thư viện 'psutil' và 'customtkinter'.")
        app.log_message(f"🎨 Giao diện: {customtkinter.get_appearance_mode()} Mode")
        app.log_message("=" * 60)
        app.log_message("Vui lòng chọn đúng Network Interface của bạn!")
    
    app.after(100, welcome_logs) # Chờ 100ms để UI render
    app.mainloop()


if __name__ == "__main__":
    main()
