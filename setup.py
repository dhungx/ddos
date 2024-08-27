import os
import sys
import subprocess

# Mã escape ANSI để đổi màu đỏ và in đậm
RED_BOLD = '\033[91m\033[1m'
RESET = '\033[0m'

def install_packages(packages):
    try:
        print(RED_BOLD + "Đang cài đặt thư viện cần thiết, vui lòng đợi..." + RESET)
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi cài đặt các gói: {e}")
        sys.exit(1)

def check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("pip không được cài đặt và không thể tự động cài đặt. Vui lòng cài đặt pip thủ công.")
        sys.exit(1)

def clear_screen():
    # Xóa màn hình tùy theo hệ điều hành
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear_screen()  # Xóa màn hình

    # Cảnh báo tấn công DDoS với màu đỏ và in đậm
    print(RED_BOLD + "Tấn công DDoS là hành vi phạm pháp và sẽ bị xử lý theo quy định của pháp luật." + RESET)
    print(RED_BOLD + "Bạn có chắc chắn muốn chạy ko? [y/n]" + RESET)
    
    choice = input().strip().lower()
    if choice != 'y':
        print("Quá trình bị hủy.")
        sys.exit()

    # Hỏi người dùng về hệ điều hành/ứng dụng
    print("Bạn đang sử dụng hệ điều hành/ứng dụng nào?")
    print("1. Termux")
    print("2. iSH")
    print("3. Linux")
    print("4. Windows")
    
    user_env_choice = input().strip()
    
    if user_env_choice == '1':
        user_env = 'termux'
    elif user_env_choice == '2':
        user_env = 'ish'
    elif user_env_choice == '3':
        user_env = 'linux'
    elif user_env_choice == '4':
        user_env = 'windows'
    elif user_env_choice == '5':
        user_env = 'unknown'
    else:
        print("Lựa chọn không hợp lệ. Mặc định là 'khác'.")
        user_env = 'unknown'

    print(f"Đang kiểm tra môi trường: {user_env}")

    # Kiểm tra và cài đặt pip nếu cần thiết
    check_pip()

    # Các gói cần cài đặt
    packages = [
        "requests>=2.28.1",
        "colorama>=0.4.5",
        "humanfriendly>=10.0",
        "PySocks>=1.7.1",
        "scapy>=2.4.5",
        "get_mac>=0.8.3"
    ]

    # Cài đặt các thư viện
    install_packages(packages)

    # Chạy file ddos.py
    try:
        print("Đang chạy ddos.py...")
        subprocess.run([sys.executable, "ddos.py"])
        print("Hoàn tất.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi chạy ddos.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()