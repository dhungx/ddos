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

# Thông báo hệ điều hành và chọn gói cài đặt
echo -e "${GREEN_BOLD}Bạn đang sử dụng hệ điều hành nào?${RESET}"
echo "1) Kali Linux/Ubuntu/Debian (apt)"
echo "2) Arch Linux (pacman)"
echo "3) Alpine Linux (apk)"
echo "4) Termux (pkg)"
echo "5) macOS"
echo "6) Windows"
read -p "Lựa chọn của bạn (1/2/3/4/5/6): " os_choice

# Hàm kiểm tra cài đặt gói
check_and_install() {
    if ! command -v "$1" &>/dev/null; then
        echo -e "${GREEN_BOLD}Đang cài đặt $1...${RESET}"
        eval "$2"
    else
        echo -e "${GREEN_BOLD}$1 đã được cài đặt.${RESET}"
    fi
}

# Cài đặt các gói cần thiết cho các hệ điều hành khác nhau
install_packages() {
    case "$os_choice" in
        1)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng apt...${RESET}"
            sudo apt update && sudo apt upgrade -y
            check_and_install "python3" "sudo apt install -y python3"
            check_and_install "python3-pip" "sudo apt install -y python3-pip"
            check_and_install "nmap" "sudo apt install -y nmap"
            check_and_install "iptables" "sudo apt install -y iptables"
            ;;
        2)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng pacman...${RESET}"
            sudo pacman -Syu --noconfirm
            check_and_install "python" "sudo pacman -S --noconfirm python"
            check_and_install "python-pip" "sudo pacman -S --noconfirm python-pip"
            check_and_install "nmap" "sudo pacman -S --noconfirm nmap"
            check_and_install "iptables" "sudo pacman -S --noconfirm iptables"
            ;;
        3)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng apk...${RESET}"
            sudo apk update && sudo apk upgrade
            check_and_install "python3" "sudo apk add python3"
            check_and_install "py3-pip" "sudo apk add py3-pip"
            check_and_install "nmap" "sudo apk add nmap"
            check_and_install "iptables" "sudo apk add iptables"
            ;;
        4)
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng pkg...${RESET}"
            pkg update && pkg upgrade -y
            check_and_install "python" "pkg install -y python"
            check_and_install "nmap" "pkg install -y nmap"
            ;;
        5)
            # Kiểm tra và cài đặt Homebrew cho macOS nếu chưa có
            if ! command -v brew &>/dev/null; then
                echo -e "${GREEN_BOLD}Homebrew chưa được cài đặt. Đang cài đặt Homebrew...${RESET}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            echo -e "${GREEN_BOLD}Đang cập nhật và cài đặt các gói cần thiết bằng Homebrew...${RESET}"
            brew update && brew upgrade
            check_and_install "python" "brew install python"
            check_and_install "nmap" "brew install nmap"
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

# Cấu hình iptables
echo -e "${GREEN_BOLD}Đang cấu hình iptables...${RESET}"
# Chặn tất cả lưu lượng đầu vào trừ kết nối đã thiết lập
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# Chặn tất cả lưu lượng đến
sudo iptables -A INPUT -j DROP

# Kiểm tra sự tồn tại của vbs.py và chạy nếu có
if [[ -f "vbs.py" ]]; then
    echo -e "${GREEN_BOLD}Đang chạy file vbs.py...${RESET}"
    python3 vbs.py
else
    echo -e "${RED_BOLD}File vbs.py không tồn tại. Đảm bảo file vbs.py nằm trong cùng thư mục với script này.${RESET}"
fi
