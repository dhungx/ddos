import os
import sys
import time
import random
from colorama import Fore as F, Style as S

def show_logo(animate: bool = False, delay: float = 0.05) -> None:
    """Displays the application logo with a warning message in a visually appealing layout with colors.
    
    Args:
        animate (bool, optional): Nếu True, in từng dòng với hiệu ứng animation. Mặc định là False.
        delay (float, optional): Khoảng thời gian delay giữa các dòng khi animate. Mặc định là 0.05 giây.
    
    Returns:
        None
    """
    width = 78
    logo = r"""
         __   _____ ___  ___  ___ ___   ___ _____ _   _ ___ ___ ___  
       \ \ / /_ _| _ )/ _ \/ __/ __| / __|_   _| | | |   \_ _/ _ \ 
        \ V / | || _ \ (_) \__ \__ \ \__ \ | | | |_| | |) | | (_) |
         \_/ |___|___/\___/|___/___/ |___/ |_|  \___/|___/___\___/ 

     HÃY CẨN THẬN TRƯỚC KHI SỬ DỤNG VÌ VIỆC BẠN SẮP LÀM CÓ THỂ LÀ ĐIỀU PHẠM PHÁP
     ĐỪNG TẤN CÔNG TRANG WEB CHÍNH PHỦ (NHÀ NƯỚC).

     PHẢI ĐẲNG CẤP THÌ MỚI TỒN TẠI ĐƯỢC!

                     AUTHOR: VIBOSS STUDIO
                     GITHUB: https://github.com/dhungx/
    """

    color_map = [F.RED, F.GREEN, F.YELLOW, F.BLUE, F.MAGENTA, F.CYAN, F.WHITE]

    def print_line(line: str, color: str = F.RESET) -> None:
        if animate:
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay / 10)
            sys.stdout.write("\n")
        else:
            print(line)

    # Divider
    divider = f"{F.MAGENTA}{'=' * width}{F.RESET}"
    print_line(divider)

    # In logo với màu ngẫu nhiên cho mỗi dòng
    for line in logo.splitlines():
        if line.strip():
            selected_color = random.choice(color_map)
            print_line(f"{selected_color}{line.center(width)}{F.RESET}")

    # Divider và tiêu đề phương thức
    print_line(divider)
    print_line(f"{F.CYAN}{'─' * width}{F.RESET}")
    print_line(f"{F.YELLOW}{'AVAILABLE DOS METHODS'.center(width)}{F.RESET}")
    print_line(f"{F.CYAN}{'─' * width}{F.RESET}")

    # In các section của từng layer
    print_line(f"{F.GREEN}{'LAYER 7:'.center(width)}{F.RESET}")
    print_line(f"{F.CYAN}{'• HTTP'.center(width - 2)}{F.RESET}")
    print_line(f"{F.CYAN}{'• HTTP-PROXY'.center(width - 2)}{F.RESET}")
    print_line(f"{F.CYAN}{'• SLOWLORIS'.center(width - 2)}{F.RESET}")
    print_line(f"{F.CYAN}{'• SLOWLORIS-PROXY'.center(width - 2)}{F.RESET}")

    if os.name != "nt":
        print_line(f"{F.GREEN}{'LAYER 4:'.center(width)}{F.RESET}")
        print_line(f"{F.CYAN}{'• SYN-FLOOD'.center(width - 2)}{F.RESET}")
        print_line(f"{F.GREEN}{'LAYER 2:'.center(width)}{F.RESET}")
        print_line(f"{F.CYAN}{'• ARP-SPOOF'.center(width - 2)}{F.RESET}")
        print_line(f"{F.CYAN}{'• DISCONNECT'.center(width - 2)}{F.RESET}")

    # Cảnh báo cuối cùng
    print_line(f"{F.MAGENTA}{'─' * width}{F.RESET}")
    print_line(f"{F.RED}{'HÃY CHẮC CHẮN RẰNG BẠN HIỂU NHỮNG GÌ BẠN ĐANG LÀM!'.center(width)}{F.RESET}")
    print_line(f"{F.MAGENTA}{'=' * width}{F.RESET}")

# Ví dụ gọi hàm show_logo với animation:
if __name__ == "__main__":
    show_logo(animate=True, delay=0.05)