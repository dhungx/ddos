import os
import sys
import subprocess

def install_packages(packages):
    try:
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

def main():
    print("Tấn công DDoS là hành vi phạm pháp và sẽ bị xử lý theo quy định của pháp luật. Bạn có chắc chắn muốn chạy ko? [y/n]")
    choice = input().strip().lower()
    if choice != 'y':
        print("Quá trình bị hủy.")
        sys.exit()

    # Kiểm tra và cài đặt pip nếu cần thiết
    check_pip()

    # Kiểm tra môi trường người dùng
    if 'termux' in os.environ.get('PATH', '').lower():
        user_env = 'termux'
    elif os.name == 'posix':
        if os.environ.get('SHELL', '').endswith('ish'):
            user_env = 'ish'
        else:
            user_env = 'linux'
    elif os.name == 'nt':
        user_env = 'windows'
    else:
        user_env = 'unknown'

    print(f"Đang kiểm tra môi trường: {user_env}")

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
