import os
import subprocess
import sys
import logging

# Cấu hình ghi log
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mã ANSI để in đậm và màu đỏ
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_python_version():
    if sys.version_info < (3, 6):
        print("Python 3.6 hoặc cao hơn là yêu cầu tối thiểu.")
        sys.exit(1)

def prompt_user():
    clear_screen()
    print(RED_BOLD + "Tấn công DDoS là hành vi phạm pháp và có thể bị trừng phạt theo pháp luật. Bạn có chắc chắn muốn chạy" + RESET)
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
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                               "requests>=2.28.1",
                               "colorama>=0.4.5",
                               "humanfriendly>=10.0",
                               "PySocks>=1.7.1",
                               "scapy>=2.4.5",
                               "get_mac>=0.8.3"])
    except subprocess.CalledProcessError as e:
        logging.error(f"Đã xảy ra lỗi khi cài đặt thư viện: {e}")
        print("Đã xảy ra lỗi khi cài đặt thư viện. Vui lòng kiểm tra log.")
        sys.exit(1)

def run_ddos_script():
    if not os.path.isfile("ddos.py"):
        logging.error("File ddos.py không tồn tại.")
        print("File ddos.py không tồn tại.")
        sys.exit(1)
    
    print("Đang chạy file ddos.py...")
    try:
        subprocess.check_call([sys.executable, "ddos.py"])
    except subprocess.CalledProcessError as e:
        logging.error(f"Đã xảy ra lỗi khi chạy file ddos.py: {e}")
        print("Đã xảy ra lỗi khi chạy file ddos.py. Vui lòng kiểm tra log.")
        sys.exit(1)

if __name__ == "__main__":
    check_python_version()
    user_os = prompt_user()
    install_libraries()
    run_ddos_script()