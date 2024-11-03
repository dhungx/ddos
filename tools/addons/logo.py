import os
import random
from colorama import Fore as F, Style as S

def show_logo() -> None:
    """In logo ứng dụng với thông điệp cảnh báo với bố cục đẹp và màu sắc sinh động.

    Trả về:
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

    # In logo với màu sắc ngẫu nhiên cho từng dòng
    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")  # Đường ngang trên cùng
    for line in logo.splitlines():
        if line.strip():  # Kiểm tra nếu dòng không rỗng
            selected_color = random.choice(color_map)
            print(f"{selected_color}{line.center(78)}{F.RESET}")  # Căn giữa dòng

    # In các thông tin khác với bố cục đẹp hơn
    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")  # Đường ngang dưới logo
    print(f"{random.choice(color_map)}│{' ' * 26}DOS TOOL{' ' * 25}│{F.RESET}")
    print(f"{random.choice(color_map)}│{' ' * 24}AVAILABLE METHODS{' ' * 23}│{F.RESET}")
    print(f"{random.choice(color_map)}│{' ' * 28}LAYER 7: HTTP{' ' * 28}│{F.RESET}")
    print(f"{random.choice(color_map)}│{' ' * 25}HTTP-PROXY{' ' * 26}│{F.RESET}")
    print(f"{random.choice(color_map)}│{' ' * 26}SLOWLORIS{' ' * 26}│{F.RESET}")
    print(f"{random.choice(color_map)}│{' ' * 22}SLOWLORIS-PROXY{' ' * 21}│{F.RESET}")

    if os.name != "nt":
        print(f"{random.choice(color_map)}│{' ' * 25}LAYER 4: SYN-FLOOD{' ' * 23}│{F.RESET}")
        print(f"{random.choice(color_map)}│{' ' * 24}LAYER 2: ARP-SPOOF{' ' * 23}│{F.RESET}")
        print(f"{random.choice(color_map)}│{' ' * 26}DISCONNECT{' ' * 27}│{F.RESET}")

    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")  
