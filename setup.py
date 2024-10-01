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
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        logging.error(f"Clear screen failed: {e}")

def check_python_version():
    if sys.version_info < (3, 6):
        print("Python 3.6 hoặc cao hơn là yêu cầu tối thiểu.")
        sys.exit(1)

def prompt_user():
    clear_screen()
    print(RED_BOLD + "Tấn công DDoS là hành vi phạm pháp và có thể bị trừng phạt theo pháp luật. Bạn có chắc chắn muốn chạy" + RESET)
    
    while True:
        response = input("[y/n]: ").strip().lower()
        if response in ['y', 'n']:
            break
        print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
    
    if response != 'y':
        print("Quá trình đã bị hủy bỏ.")
        logging.info("User canceled the operation.")
        sys.exit()

    while True:
        os_choice = input("Bạn đang sử dụng hệ điều hành/ứng dụng nào?\n"
                          "1) Linux\n"
                          "2) Windows\n"
                          "3) iSH\n"
                          "4) Termux\n"
                          "Lựa chọn của bạn (1/2/3/4): ").strip()
        if os_choice in ['1', '2', '3', '4']:
            break
        print("Lựa chọn không hợp lệ, vui lòng nhập lại.")

    logging.info(f"User confirmed to proceed. OS choice: {os_choice}")
    return os_choice

def install_libraries():
    print("Đang cài đặt thư viện cần thiết, vui lòng chờ…")
    logging.info("Installing required libraries...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", 
                        "requests",
                        "colorama",
                        "humanfriendly",
                        "PySocks",
                        "scapy",
                        "get_mac"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Đã xảy ra lỗi khi cài đặt thư viện: {e}")
        print("Đã xảy ra lỗi khi cài đặt thư viện. Vui lòng kiểm tra log.")
        sys.exit(1)

def run_ddos_script():
    if not os.path.isfile("vbs.py"):
        logging.error("File vbs.py không tồn tại.")
        print("File vbs.py không tồn tại.")
        sys.exit(1)
    
    print("Đang chạy file vbs.py...")
    logging.info("Running vbs.py script...")
    try:
        subprocess.run([sys.executable, "vbs.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Đã xảy ra lỗi khi chạy file vbs.py: {e}")
        print("Đã xảy ra lỗi khi chạy file vbs.py. Vui lòng kiểm tra log.")
        sys.exit(1)

if __name__ == "__main__":
    check_python_version()
    user_os = prompt_user()
    install_libraries()
    run_ddos_script()
