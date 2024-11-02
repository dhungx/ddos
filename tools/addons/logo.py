"""This module provides a function that prints the logo's application."""

import os

from colorama import Fore as F


def show_logo() -> None:
    """Print the application logo.

    Args:
        None

    Returns:
        None
    """
    logo = r"""
     __   _____ ___  ___  ___ ___   ___ _____ _   _ ___ ___ ___  
 \ \ / /_ _| _ )/ _ \/ __/ __| / __|_   _| | | |   \_ _/ _ \ 
  \ V / | || _ \ (_) \__ \__ \ \__ \ | | | |_| | |) | | (_) |
   \_/ |___|___/\___/|___/___/ |___/ |_|  \___/|___/___\___/ 
                                                             
HÃY CẨN THẬN TRƯỚC KHI SỬ DỤNG VÌ VIỆC BẠN SẮP LÀM CÓ THỂ LÀ ĐIỀU PHẠM PHÁP
ĐỪNG TẤN CÔNG TRANG WEB CHÍNH PHỦ (NHÀ NƯỚC).

PHẢI ĐẲNG CẤP THÌ MỚI TỒN TẠI ĐƯỢC!

AuThor: ViBoss Studio
Github: https://github.com/dhungx/
  """

    print(f"{F.RED}{logo}")
    print("├─── DOS TOOL")
    print("├─── AVAILABLE METHODS")
    print("├─── LAYER 7: HTTP | HTTP-PROXY | SLOWLORIS | SLOWLORIS-PROXY")
    if os.name != "nt":
        print("├─── LAYER 4: SYN-FLOOD")
        print("├─── LAYER 2: ARP-SPOOF | DISCONNECT")
    print("├───┐")
