import os
import sys
from typing import Union

import requests
from colorama import Fore as F
from requests.exceptions import ConnectionError, InvalidURL, ReadTimeout

from tools.addons.ip_tools import __get_local_host_ips, set_target_http

def check_method_input() -> str:
    """Kiểm tra xem tên phương thức có hợp lệ hay không.

    Trả về:
        - method - Tên phương thức hợp lệ
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
    
    while (method := input(f"{F.RED}│   ├─── METHOD: {F.RESET}").lower()) not in valid_methods:
        if method in ["syn-flood", "arp-spoof", "disconnect"] and os.name == "nt":
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Type a valid method!{F.RESET}")
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}These methods require Super User privileges on Windows!{F.RESET}")
        else:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Type a valid method!{F.RESET}")

    if method in ["syn-flood", "arp-spoof", "disconnect"] and os.getuid() != 0:
        print(
            f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}This attack needs Super User privileges!"
        )
        print(
            f"{F.RED}│   └───{F.MAGENTA} [!] {F.BLUE}Run: {F.GREEN}sudo {os.popen('which python').read().strip()} vbs.py\n{F.RESET}"
        )
        sys.exit(1)

    return method


def check_number_input(x: str) -> int:
    """Kiểm tra xem đầu vào có phải là số nguyên lớn hơn 0 hay không.

    Tham số:
        - x - Tên của trường đầu vào

    Trả về:
        - y - Giá trị hợp lệ
    """
    while True:
        y = input(f"{F.RED}│   ├─── {x.upper()}: {F.RESET}")
        try:
            y = int(y)
            if y <= 0:
                raise ValueError("Giá trị phải lớn hơn 0.")
        except ValueError as ve:
            print(
                f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}This value must be an integer number greater than zero! ({ve}){F.RESET}"
            )
        else:
            return y


def check_http_target_input() -> str:
    """Kiểm tra xem mục tiêu có đang lắng nghe trên cổng HTTP (80) hay không.

    Trả về:
        - target - Mục tiêu hợp lệ
    """
    while True:
        target = input(f"{F.RED}│   ├─── URL: {F.RESET}")
        try:
            requests.get("https://google.com", timeout=4)
            requests.get(set_target_http(target), timeout=4)
        except ConnectionError:
            print(
                f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Device is not connected to the internet!{F.RESET}"
            )
            continue
        except (ReadTimeout, InvalidURL) as exc:
            print(f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Invalid URL or timeout! ({exc}){F.RESET}")
            continue
        else:
            return target


def check_local_target_input() -> str:
    """Kiểm tra xem mục tiêu có trong mạng cục bộ hay không.

    Trả về:
        - target - Mục tiêu hợp lệ
    """
    hosts = __get_local_host_ips()
    while True:
        target = input(f"{F.RED}│   ├─── IP: {F.RESET}")
        if target not in hosts:
            print(
                f"{F.RED}│   ├───{F.MAGENTA} [!] {F.BLUE}Cannot connect to {F.CYAN}{target}{F.BLUE} on the local network!{F.RESET}"
            )
        else:
            return target
