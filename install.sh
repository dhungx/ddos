#!/bin/bash

# Cấu hình màu sắc cho thông báo
RED_BOLD="\033[1;31m"
RESET="\033[0m"

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED_BOLD}Yêu cầu quyền root để chạy script này. Hãy chạy lại với 'sudo'.${RESET}"
  exit
fi

# Thông báo hệ điều hành và chọn gói cài đặt
echo "Bạn đang sử dụng hệ điều hành nào?"
echo "1) Kali Linux/Ubuntu/Debian (apt)"
echo "2) Arch Linux (pacman)"
echo "3) Alpine Linux (apk)"
echo "4) Termux (pkg)"
echo "5) macOS"
echo "6) Windows"
read -p "Lựa chọn của bạn (1/2/3/4/5/6): " os_choice

# Hàm cập nhật và cài đặt các gói cần thiết cho các hệ điều hành khác nhau
install_packages() {
    if [[ "$os_choice" == "1" ]]; then
        sudo apt update && apt upgrade -y
        sudo apt install -y python3 python3-pip nmap
    elif [[ "$os_choice" == "2" ]]; then
        pacman -Syu --noconfirm
        sudo pacman -S --noconfirm python python-pip nmap
    elif [[ "$os_choice" == "3" ]]; then
        apk update && apk upgrade
        sudo apk add python3 py3-pip nmap
    elif [[ "$os_choice" == "4" ]]; then
        pkg update && pkg upgrade -y
        pkg install -y python nmap
    elif [[ "$os_choice" == "5" ]]; then
        # Kiểm tra và cài đặt Homebrew cho macOS nếu chưa có
        if ! command -v brew &>/dev/null; then
            echo "Homebrew chưa được cài đặt. Đang cài đặt Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew update && brew upgrade
        brew install python nmap
    elif [[ "$os_choice" == "6" ]]; then
        echo -e "${RED_BOLD}Hãy cài đặt thủ công Python, pip, và nmap cho Windows.${RESET}"
        exit
    else
        echo -e "${RED_BOLD}Lựa chọn không hợp lệ. Thoát.${RESET}"
        exit
    fi
}

# Cài đặt các gói cần thiết
install_packages

# Kiểm tra và cài đặt pip nếu thiếu
if ! command -v pip3 &>/dev/null; then
    echo "pip3 chưa được cài đặt. Đang cài đặt pip3..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Cài đặt các thư viện Python cần thiết
echo "Đang cài đặt các thư viện Python cần thiết..."
pip3 install requests colorama humanfriendly PySocks scapy get-mac --quiet

# Kiểm tra sự tồn tại của vbs.py và chạy nếu có
if [[ -f "vbs.py" ]]; then
    echo "Đang chạy file vbs.py..."
    python3 vbs.py
else
    echo -e "${RED_BOLD}File vbs.py không tồn tại. Đảm bảo file vbs.py nằm trong cùng thư mục với script này.${RESET}"
fi
