import os
import random
from colorama import Fore as F, Style as S

def show_logo() -> None:
    """Displays the application logo with a warning message in a visually appealing layout with colors."""

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

    # Define a list of colors
    color_map = [F.RED, F.GREEN, F.YELLOW, F.BLUE, F.MAGENTA, F.CYAN, F.WHITE]

    # Print the logo with random colors for each line
    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")
    for line in logo.splitlines():
        if line.strip():
            selected_color = random.choice(color_map)
            print(f"{selected_color}{line.center(78)}{F.RESET}")

    # Divider and title for the methods section
    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")
    print(f"{F.CYAN}{'─' * 78}{F.RESET}")
    print(f"{F.YELLOW}{'AVAILABLE DOS METHODS'.center(78)}{F.RESET}")
    print(f"{F.CYAN}{'─' * 78}{F.RESET}")

    # Layer sections with improved color layout
    print(f"{F.GREEN}{'LAYER 7:'.center(78)}{F.RESET}")
    print(f"{F.CYAN} {'• HTTP'.center(76)}{F.RESET}")
    print(f"{F.CYAN} {'• HTTP-PROXY'.center(76)}{F.RESET}")
    print(f"{F.CYAN} {'• SLOWLORIS'.center(76)}{F.RESET}")
    print(f"{F.CYAN} {'• SLOWLORIS-PROXY'.center(76)}{F.RESET}")

    if os.name != "nt":
        print(f"{F.GREEN}{'LAYER 4:'.center(78)}{F.RESET}")
        print(f"{F.CYAN} {'• SYN-FLOOD'.center(76)}{F.RESET}")

        print(f"{F.GREEN}{'LAYER 2:'.center(78)}{F.RESET}")
        print(f"{F.CYAN} {'• ARP-SPOOF'.center(76)}{F.RESET}")
        print(f"{F.CYAN} {'• DISCONNECT'.center(76)}{F.RESET}")

    # Final caution line
    print(f"{F.MAGENTA}{'─' * 78}{F.RESET}")
    print(f"{F.RED}{'HÃY CHẮC CHẮN RẰNG BẠN HIỂU NHỮNG GÌ BẠN ĐANG LÀM!'.center(78)}{F.RESET}")
    print(f"{F.MAGENTA}{'=' * 78}{F.RESET}")
