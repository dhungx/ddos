import os
import random
from colorama import Fore as F

def show_logo() -> None:
    """In logo ứng dụng với thông điệp cảnh báo.

    Trả về:
        None
    """
    logo = r"""
__     __   _____ ___  ___  ___ ___   ___ _____ _   _ ___ ___
 \ \ / /_ _| _ )/ _ \/ __/ __| / __|_   _| | | |   \_ _/ _ \ 
  \ V / | || _ \ (_) \__ \__ \ \__ \ | | | |_| | |) | | (_) |
   \_/ |___|___/\___/|___/___/ |___/ |_|  \___/|___/___\___/ 
                                                             
     HÃY CẨN THẬN TRƯỚC KHI SỬ DỤNG VÌ VIỆC BẠN SẮP LÀM CÓ THỂ LÀ ĐIỀU PHẠM PHÁP
  ĐỪNG TẤN CÔNG TRANG WEB CHÍNH PHỦ (NHÀ NƯỚC).

  PHẢI ĐẲNG CẤP THÌ MỚI TỒN TẠI ĐƯỢC!

                  AuThor: ViBoss Studio
                  Github: https://github.com/dhungx/
  """

    # Định nghĩa danh sách màu
    color_map = [
        F.RED,
        F.GREEN,
        F.YELLOW,
        F.BLUE,
        F.MAGENTA,
        F.CYAN,
        F.WHITE,
    ]

    selected_color = random.choice(color_map)  # Chọn màu ngẫu nhiên từ danh sách

    print(f"{selected_color}{logo}{F.RESET}")  # In logo với màu đã chọn

    print("┌───────────────────────────────────┐")
    print("│              DOS TOOL             │")
    print("├───────────────────────────────────┤")
    print("│          AVAILABLE METHODS         │")
    print("├───────────────────────────────────┤")
    print("│ Layer 7: HTTP                     │")
    print("│          HTTP-PROXY               │")
    print("│          SLOWLORIS                │")
    print("│          SLOWLORIS-PROXY          │")
    
    if os.name != "nt":
        print("│ Layer 4: SYN-FLOOD                │")
        print("│ Layer 2: ARP-SPOOF                │")
        print("│          DISCONNECT                │")
    
    print("└───────────────────────────────────┘")
