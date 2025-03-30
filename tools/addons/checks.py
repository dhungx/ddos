import os
import sys
import logging
from typing import Any

import requests
from colorama import Fore as F
from requests.exceptions import ConnectionError, InvalidURL, ReadTimeout

from tools.addons.ip_tools import __get_local_host_ips, set_target_http

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def prompt_input(prompt: str) -> str:
    """In prompt với định dạng màu sắc và trả về giá trị người dùng nhập."""
    return input(f"{F.RED}│   ├─── {prompt}: {F.RESET}")

def check_method_input() -> str:
    """Kiểm tra xem tên phương thức có hợp lệ hay không.

    Returns:
        str: Tên phương thức hợp lệ
    """
    valid_methods = [
        "http",
        "http-proxy",
        "slowloris",
        "slowloris-proxy",
        "syn-flood",
        "arp-spoof",
        "disconnect",
    ]
    
    while True:
        method = prompt_input("METHOD").lower()
        if method not in valid_methods:
            if method in ["syn-flood", "arp-spoof", "disconnect"] and os.name == "nt":
                print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Type a valid method!{F.RESET}")
                print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}These methods require Super User privileges on Windows!{F.RESET}")
            else:
                print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Type a valid method!{F.RESET}")
        else:
            # Kiểm tra quyền root trên hệ thống (nếu có thuộc tính getuid)
            try:
                uid = os.getuid()
            except AttributeError:
                uid = 0  # Trên Windows, giả sử quyền admin được xác nhận qua phương thức khác
            if method in ["syn-flood", "arp-spoof", "disconnect"] and uid != 0:
                print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}This attack needs Super User privileges!")
                python_path = os.popen('which python').read().strip()
                print(f"{F.RED}│   └───{F.MAGENTA} [!] {F.BLUE}Run: {F.GREEN}sudo {python_path} vbs.py{F.RESET}\n")
                sys.exit(1)
            return method

def check_number_input(field_name: str) -> int:
    """Kiểm tra xem đầu vào có phải là số nguyên lớn hơn 0 hay không.

    Args:
        field_name (str): Tên của trường đầu vào

    Returns:
        int: Giá trị hợp lệ được nhập
    """
    while True:
        user_input = prompt_input(field_name.upper())
        try:
            value = int(user_input)
            if value <= 0:
                raise ValueError("Giá trị phải lớn hơn 0.")
        except ValueError as ve:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}This value must be an integer greater than zero! ({ve}){F.RESET}")
        else:
            return value

def check_http_target_input() -> str:
    """Kiểm tra xem mục tiêu có đang lắng nghe trên cổng HTTP (80) hay không.

    Returns:
        str: Mục tiêu hợp lệ
    """
    while True:
        target = prompt_input("URL")
        try:
            # Kiểm tra kết nối internet
            requests.get("https://google.com", timeout=4)
            # Kiểm tra kết nối đến mục tiêu sau khi chỉnh sửa URL nếu cần
            requests.get(set_target_http(target), timeout=4)
        except ConnectionError:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Device is not connected to the internet!{F.RESET}")
            continue
        except (ReadTimeout, InvalidURL) as exc:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Invalid URL or timeout! ({exc}){F.RESET}")
            continue
        else:
            return target

def check_local_target_input() -> str:
    """Kiểm tra xem mục tiêu có trong mạng cục bộ hay không.

    Returns:
        str: Mục tiêu hợp lệ
    """
    hosts = __get_local_host_ips()
    while True:
        target = prompt_input("IP")
        if target not in hosts:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Cannot connect to {F.CYAN}{target}{F.BLUE} on the local network!{F.RESET}")
        else:
            return target

# Nếu module được chạy trực tiếp, ta có thể thêm một số ví dụ kiểm tra
if __name__ == "__main__":
    method = check_method_input()
    print(f"Method chọn: {method}")
    number = check_number_input("threads")
    print(f"Threads: {number}")
    target_http = check_http_target_input()
    print(f"HTTP Target: {target_http}")
    target_local = check_local_target_input()
    print(f"Local Target: {target_local}")