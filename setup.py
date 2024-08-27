# setup_script.py

import os
import subprocess
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_user():
    clear_screen()
    print("Tấn công DDoS là hành vi phạm pháp và có thể bị trừng phạt theo pháp luật. Bạn có chắc chắn muốn chạy")
    response = input("[y/n]: ").strip().lower()
    
    if response != 'y':
        print("Quá trình đã bị hủy bỏ.")
        sys.exit()

    os_choice = input("Bạn đang sử dụng hệ điều hành/ứng dụng nào?\n"
                      "1) Linux\n"
                      "2) Window\n"
                      "3) Ish\n"
                      "4) Termux\n"
                      "Lựa chọn của bạn (1/2/3/4): ").strip()

    return os_choice

def install_libraries():
    print("Đang cài đặt thư viện cần thiết, vui lòng chờ…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                           "requests>=2.28.1",
                           "colorama>=0.4.5",
                           "humanfriendly>=10.0",
                           "PySocks>=1.7.1",
                           "scapy>=2.4.5",
                           "get_mac>=0.8.3"])

def run_ddos_script():
    print("Đang chạy file ddos.py...")
    subprocess.check_call([sys.executable, "ddos.py"])

if __name__ == "__main__":
    user_os = prompt_user()
    install_libraries()
    run_ddos_script()