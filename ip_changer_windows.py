#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import time
import re
import psutil
from datetime import datetime
import sys
import os

class AutoIPChangerWindows:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto IP Changer - Windows")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Biến toàn cục
        self.is_auto_running = False
        self.auto_thread = None
        
        # Danh sách interface mạng
        self.network_interfaces = self.get_network_interfaces()
        
        self.setup_ui()
        self.update_current_ip()
    
    def get_network_interfaces(self):
        """Lấy danh sách các interface mạng có sẵn trên Windows"""
        interfaces = []
        try:
            addrs = psutil.net_if_addrs()
            for interface_name in addrs:
                for addr in addrs[interface_name]:
                    if addr.family == 2:  # IPv4
                        interfaces.append(interface_name)
                        break
        except Exception as e:
            print(f"Lỗi khi lấy interface: {e}")
            interfaces = ["Ethernet", "Wi-Fi", "Local Area Connection"]
        
        return list(set(interfaces))
    
    def get_current_ip_windows(self, interface):
        """Lấy IP hiện tại trên Windows"""
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, check=True, shell=True)
            
            lines = result.stdout.split('\n')
            found_interface = False
            for line in lines:
                if interface in line and 'adapter' in line.lower():
                    found_interface = True
                    continue
                if found_interface and 'IPv4 Address' in line:
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        return ip_match.group(1)
                if found_interface and line.strip() == '':
                    break
            
            return "Không có IP"
                
        except subprocess.CalledProcessError as e:
            return f"Lỗi: {e}"
        except Exception as e:
            return f"Lỗi: {e}"
    
    def change_ip_windows(self, interface):
        """Thay đổi IP trên Windows sử dụng netsh"""
        try:
            self.log_message(f"Đang release IP trên {interface}...")
            subprocess.run(['ipconfig', '/release'], capture_output=True, text=True, check=True, shell=True)
            time.sleep(3)
            
            self.log_message(f"Đang renew IP trên {interface}...")
            subprocess.run(['ipconfig', '/renew'], capture_output=True, text=True, check=True, shell=True)
            
            return True
        except subprocess.CalledProcessError as e:
            self.log_message(f"Lỗi lệnh: {e}")
            return False
        except Exception as e:
            self.log_message(f"Lỗi không xác định: {e}")
            return False
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # ===== PHẦN 1: Thông tin mạng =====
        info_frame = ttk.LabelFrame(main_frame, text="📶 Thông tin mạng", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Network Interface:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(info_frame, textvariable=self.interface_var, 
                                           values=self.network_interfaces, state="readonly")
        self.interface_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        if self.network_interfaces:
            self.interface_combo.set(self.network_interfaces[0])
        
        ttk.Label(info_frame, text="IP hiện tại:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.current_ip_var = tk.StringVar(value="Đang tải...")
        ip_label = ttk.Label(info_frame, textvariable=self.current_ip_var, 
                           foreground="blue", font=("Arial", 10, "bold"))
        ip_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(info_frame, text="🔄 Làm mới IP", 
                  command=self.update_current_ip).grid(row=1, column=2, padx=10)
        
        # ===== PHẦN 2: Thay đổi IP thủ công =====
        manual_frame = ttk.LabelFrame(main_frame, text="🔧 Thay đổi IP thủ công", padding="10")
        manual_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        manual_btn = ttk.Button(manual_frame, text="🔄 THAY ĐỔI IP NGAY", 
                               command=self.change_ip_manual,
                               style="Accent.TButton")
        manual_btn.grid(row=0, column=0, pady=15)
        
        # ===== PHẦN 3: Tự động thay đổi IP =====
        auto_frame = ttk.LabelFrame(main_frame, text="⏰ Tự động thay đổi IP", padding="10")
        auto_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        auto_frame.columnconfigure(1, weight=1)
        
        ttk.Label(auto_frame, text="Khoảng thời gian (phút):", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value="10")
        ttk.Spinbox(auto_frame, from_=1, to=1440, textvariable=self.interval_var,
                   width=8, font=("Arial", 9)).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        self.auto_button = ttk.Button(auto_frame, text="🚀 BẮT ĐẦU TỰ ĐỘNG", 
                                     command=self.toggle_auto_mode)
        self.auto_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.auto_status_var = tk.StringVar(value="Chế độ tự động: Chưa kích hoạt")
        status_label = ttk.Label(auto_frame, textvariable=self.auto_status_var, 
                               foreground="red", font=("Arial", 9, "bold"))
        status_label.grid(row=2, column=0, columnspan=2)
        
        # ===== PHẦN 4: Log =====
        log_frame = ttk.LabelFrame(main_frame, text="📝 Nhật ký hoạt động", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Nút xóa log
        ttk.Button(log_frame, text="🗑️ Xóa log", 
                  command=self.clear_log).grid(row=1, column=0, pady=5, sticky=tk.E)
    
    def log_message(self, message):
        """Thêm message vào log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Xóa nội dung log"""
        self.log_text.delete(1.0, tk.END)
    
    def update_current_ip(self):
        """Cập nhật hiển thị IP hiện tại"""
        interface = self.interface_var.get()
        if not interface:
            self.current_ip_var.set("Chưa chọn interface")
            return
        
        current_ip = self.get_current_ip_windows(interface)
        self.current_ip_var.set(current_ip)
        self.log_message(f"Cập nhật IP trên {interface}: {current_ip}")
    
    def change_ip_manual(self):
        """Thay đổi IP thủ công"""
        interface = self.interface_var.get()
        if not interface:
            messagebox.showerror("Lỗi", "Vui lòng chọn network interface!")
            return
        
        thread = threading.Thread(target=self._change_ip_process, args=(interface, "thủ công"))
        thread.daemon = True
        thread.start()
    
    def _change_ip_process(self, interface, mode="thủ công"):
        """Tiến trình thay đổi IP (chạy trong thread)"""
        try:
            self.log_message(f"🎯 Bắt đầu thay đổi IP {mode} trên {interface}...")
            
            success = self.change_ip_windows(interface)
            
            if success:
                time.sleep(5)
                new_ip = self.get_current_ip_windows(interface)
                self.log_message(f"✅ Thay đổi IP thành công! IP mới: {new_ip}")
                self.root.after(0, lambda: self.current_ip_var.set(new_ip))
                self.root.after(0, lambda: messagebox.showinfo("Thành công", f"Đã thay đổi IP thành công!\nIP mới: {new_ip}"))
            else:
                self.log_message("❌ Thay đổi IP thất bại!")
                self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không thể thay đổi IP. Vui lòng thử lại."))
                
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.log_message(f"❌ {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Lỗi", error_msg))
    
    def toggle_auto_mode(self):
        """Bật/tắt chế độ tự động"""
        if not self.is_auto_running:
            self.start_auto_mode()
        else:
            self.stop_auto_mode()
    
    def start_auto_mode(self):
        """Bắt đầu chế độ tự động"""
        interface = self.interface_var.get()
        if not interface:
            messagebox.showerror("Lỗi", "Vui lòng chọn network interface!")
            return
        
        try:
            interval = int(self.interval_var.get())
            if interval < 1:
                messagebox.showerror("Lỗi", "Khoảng thời gian phải >= 1 phút!")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Khoảng thời gian phải là số!")
            return
        
        self.is_auto_running = True
        self.auto_button.config(text="⏹️ DỪNG TỰ ĐỘNG")
        self.auto_status_var.set(f"Chế độ tự động: Đang chạy - Thay đổi mỗi {interval} phút")
        
        self.log_message(f"🚀 BẮT ĐẦU chế độ tự động - Interface: {interface}, Interval: {interval} phút")
        
        self.auto_thread = threading.Thread(target=self._auto_mode_worker, 
                                          args=(interface, interval))
        self.auto_thread.daemon = True
        self.auto_thread.start()
    
    def stop_auto_mode(self):
        """Dừng chế độ tự động"""
        self.is_auto_running = False
        self.auto_button.config(text="🚀 BẮT ĐẦU TỰ ĐỘNG")
        self.auto_status_var.set("Chế độ tự động: Đã dừng")
        self.log_message("🛑 ĐÃ DỪNG chế độ tự động")
    
    def _auto_mode_worker(self, interface, interval_minutes):
        """Worker thread cho chế độ tự động"""
        interval_seconds = interval_minutes * 60
        countdown = interval_seconds
        
        while self.is_auto_running:
            try:
                # Hiển thị countdown
                for i in range(interval_seconds):
                    if not self.is_auto_running:
                        return
                    countdown = interval_seconds - i
                    if countdown % 60 == 0:  # Hiển thị mỗi phút
                        self.root.after(0, lambda: self.auto_status_var.set(
                            f"Chế độ tự động: Đang chạy - Còn {countdown//60} phút"))
                    time.sleep(1)
                
                if self.is_auto_running:
                    self.log_message(f"⏰ Tự động thay đổi IP (mỗi {interval_minutes} phút)")
                    self._change_ip_process(interface, "tự động")
                    
            except Exception as e:
                self.log_message(f"❌ Lỗi trong chế độ tự động: {e}")
                time.sleep(5)

def main():
    # Tạo style cho giao diện
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="white", background="#0078D7", font=("Arial", 10, "bold"))
    
    app = AutoIPChangerWindows(root)
    
    # Hiển thị hướng dẫn ban đầu
    app.log_message("=" * 50)
    app.log_message("🚀 AUTO IP CHANGER - WINDOWS")
    app.log_message("=" * 50)
    app.log_message("1. Chọn network interface")
    app.log_message("2. Nhấn 'THAY ĐỔI IP NGAY' để thay đổi thủ công")
    app.log_message("3. Hoặc thiết lập tự động với khoảng thời gian")
    app.log_message("=" * 50)
    
    # Center window
    root.update()
    root.eval('tk::PlaceWindow . center')
    
    root.mainloop()

if __name__ == "__main__":
    main()
