# -*- coding: utf-8 -*-
"""
Main script to start GUI DoS attack application.
"""

import os
import sys
from colorama import Fore

# Thay đổi thư mục làm việc đến vị trí của file script
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("cls" if os.name == "nt" else "clear")

# Kiểm tra các thư viện cần thiết
try:
    from tools.addons.checks import (
        check_http_target_input,
        check_local_target_input,
        check_method_input,
        check_number_input
    )
    from tools.addons.ip_tools import show_local_host_ips
    from tools.addons.logo import show_logo
    from tools.method import AttackMethod
except ImportError as err:
    print(f"\n{Fore.RED}Failed to import required modules: {err}{Fore.RESET}")
    sys.exit(1)


def configure_attack():
    """Cấu hình các thông số cho cuộc tấn công."""
    method = check_method_input()
    if method in ["arp-spoof", "disconnect"]:
        show_local_host_ips()

    target = (
        check_http_target_input()
        if method not in ["arp-spoof", "disconnect"]
        else check_local_target_input()
    )
    threads = (
        check_number_input("threads")
        if method not in ["arp-spoof", "disconnect"]
        else 1
    )
    duration = check_number_input("time")
    sleep_time = check_number_input("sleep time") if "slowloris" in method else 0

    return method, target, threads, duration, sleep_time


def start_attack(method, target, threads, duration, sleep_time):
    """Khởi động cuộc tấn công với các tham số đã cấu hình."""
    with AttackMethod(
        duration=duration,
        method_name=method,
        threads=threads,
        target=target,
        sleep_time=sleep_time,
    ) as attack:
        attack.start()


def main():
    """Run main application."""
    show_logo()
    try:
        method, target, threads, duration, sleep_time = configure_attack()
        start_attack(method, target, threads, duration, sleep_time)
    except KeyboardInterrupt:
        print(
            f"\n\n{Fore.RED}[!] {Fore.MAGENTA}Ctrl+C detected. Program closed.\n\n{Fore.RESET}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Fore.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
