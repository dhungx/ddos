#!/bin/bash

# Xóa màn hình terminal
clear_cmd="clear"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  clear_cmd="cls"
fi
$clear_cmd


# Cấu hình màu sắc cho thông báo
RED_BOLD="\033[1;31m"
GREEN_BOLD="\033[1;32m"
RESET="\033[0m"

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED_BOLD}Yêu cầu quyền root để chạy script này. Hãy chạy lại với 'sudo'.${RESET}"
  exit
fi

# Thông báo hệ điều hành và chọn gói cài đặt
echo -e "${GREEN_BOLD}Bạn đang sử dụng hệ điều hành nào?${RESET}"
echo "1) Kali Linux/Ubuntu/Debian (apt)"
echo "2) Arch Linux (pacman)"
echo "3) Alpine Linux (apk)"
echo "4) Termux (pkg)"
echo "5) macOS"
echo "6) Windows"
read -p "Lựa chọn của bạn (1/2/3/4/5/6): " os_choice

# Hàm cập nhật và cài đặt các gói cần thiết cho các hệ điều hành khác nhau
install_packages() {
    case "$os_choice" in
        1)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng apt...${RESET}"
            sudo apt update && sudo apt upgrade -y
            sudo apt install -y python3 python3-pip nmap
            ;;
        2)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng pacman...${RESET}"
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm python python-pip nmap
            ;;
        3)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng apk...${RESET}"
            sudo apk update && sudo apk upgrade
            sudo apk add python3 py3-pip nmap
            ;;
        4)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng pkg...${RESET}"
            pkg update && pkg upgrade -y
            pkg install -y python nmap
            ;;
        5)
            # Kiểm tra và cài đặt Homebrew cho macOS nếu chưa có
            if ! command -v brew &>/dev/null; then
                echo -e "${GREEN_BOLD}Homebrew chưa được cài đặt. Đang cài đặt Homebrew...${RESET}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng Homebrew...${RESET}"
            brew update && brew upgrade
            brew install python nmap
            ;;
        6)
            echo -e "${RED_BOLD}Hãy cài đặt thủ công Python, pip, và nmap cho Windows.${RESET}"
            exit
            ;;
        *)
            echo -e "${RED_BOLD}Lựa chọn không hợp lệ. Thoát.${RESET}"
            exit
            ;;
    esac
}

# Cài đặt các gói cần thiết
install_packages

# Kiểm tra và cài đặt pip nếu thiếu
if ! command -v pip3 &>/dev/null; then
    echo -e "${GREEN_BOLD}pip3 chưa được cài đặt. Đang cài đặt pip3...${RESET}"
    curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Cài đặt các thư viện Python cần thiết
echo -e "${GREEN_BOLD}Đang cài đặt các thư viện Python cần thiết...${RESET}"
pip3 install requests colorama humanfriendly PySocks scapy get-mac --quiet

# Kiểm tra sự tồn tại của vbs.py và chạy nếu có
if [[ -f "vbs.py" ]]; then
    echo -e "${GREEN_BOLD}Đang chạy file vbs.py...${RESET}"
    python3 vbs.py
else
    echo -e "${RED_BOLD}File vbs.py không tồn tại. Đảm bảo file vbs.py nằm trong cùng thư mục với script này.${RESET}"
fi
