#!/bin/bash

# === Cấu hình màu sắc ===
RED_BOLD="\033[1;31m"
GREEN_BOLD="\033[1;32m"
YELLOW_BOLD="\033[1;33m"
RESET="\033[0m"

# === Ghi log vào file install.log ===
LOG_FILE="install.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "==== Bắt đầu cài đặt: $(date) ===="

# === Xóa màn hình terminal ===
clear_screen() {
    case "$OSTYPE" in
        "msys" | "cygwin" | "win32") cls ;;
        *) clear ;;
    esac
}
clear_screen

# === Kiểm tra quyền sudo ===
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED_BOLD}Vui lòng chạy script với quyền root (sudo).${RESET}"
    exit 1
fi

# === Kiểm tra kết nối Internet ===
echo -e "${GREEN_BOLD}🔍 Kiểm tra kết nối Internet...${RESET}"
if ! ping -c 1 8.8.8.8 &>/dev/null; then
    echo -e "${RED_BOLD}❌ Không có kết nối Internet! Hãy kiểm tra mạng.${RESET}"
    exit 1
fi

# === Kiểm tra dung lượng trống (tối thiểu 50MB) ===
FREE_SPACE=$(df / | tail -1 | awk '{print $4}')
if [[ $FREE_SPACE -lt 50000 ]]; then
    echo -e "${RED_BOLD}❌ Dung lượng ổ đĩa quá thấp! Cần ít nhất 50MB trống.${RESET}"
    exit 1
fi

# === Chọn hệ điều hành ===
echo -e "${GREEN_BOLD}🖥️ Chọn hệ điều hành của bạn:${RESET}"
echo "1) Kali Linux/Ubuntu/Debian (apt)"
echo "2) Arch Linux (pacman)"
echo "3) Alpine Linux (apk)"
echo "4) Termux (pkg)"
echo "5) macOS"
echo "6) Windows"
read -p "Lựa chọn (1/2/3/4/5/6): " os_choice

# === Hàm kiểm tra & cài đặt gói ===
check_and_install() {
    if ! command -v "$1" &>/dev/null; then
        echo -e "${YELLOW_BOLD}📦 Cài đặt $1...${RESET}"
        eval "$2"
    else
        echo -e "${GREEN_BOLD}✔ $1 đã có sẵn.${RESET}"
    fi
}

# === Cài đặt các gói cần thiết ===
install_packages() {
    case "$os_choice" in
        1)  install_cmd="sudo apt install -y" 
            packages=("python3" "python3-pip" "nmap" "iptables") ;;
        2)  install_cmd="sudo pacman -S --noconfirm" 
            packages=("python" "python-pip" "nmap" "iptables") ;;
        3)  install_cmd="sudo apk add" 
            packages=("python3" "py3-pip" "nmap" "iptables") ;;
        4)  install_cmd="pkg install -y" 
            packages=("python" "nmap") ;;
        5)  
            if ! command -v brew &>/dev/null; then
                echo -e "${GREEN_BOLD}🍺 Cài đặt Homebrew...${RESET}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            install_cmd="brew install" 
            packages=("python" "nmap") ;;
        6)  
            echo -e "${RED_BOLD}❌ Hãy cài đặt Python, pip và nmap thủ công trên Windows.${RESET}"
            exit 1 ;;
        *)  
            echo -e "${RED_BOLD}❌ Lựa chọn không hợp lệ! Thoát.${RESET}"
            exit 1 ;;
    esac

    echo -e "${GREEN_BOLD}🔄 Cập nhật hệ thống...${RESET}"
    case "$os_choice" in
        1) sudo apt update && sudo apt upgrade -y ;;
        2) sudo pacman -Syu --noconfirm ;;
        3) sudo apk update && sudo apk upgrade ;;
        4) pkg update && pkg upgrade -y ;;
        5) brew update && brew upgrade ;;
    esac

    for package in "${packages[@]}"; do
        check_and_install "$package" "$install_cmd $package"
    done
}

# === Cài đặt hệ thống ===
install_packages

# === Cài đặt pip nếu thiếu ===
if ! command -v pip3 &>/dev/null; then
    echo -e "${YELLOW_BOLD}📥 Cài đặt pip3...${RESET}"
    curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py && rm get-pip.py
fi

# === Cài đặt thư viện Python với tiến trình tải ===
PYTHON_LIBS=("requests" "colorama" "humanfriendly" "PySocks" "scapy" "get-mac")
TOTAL_LIBS=${#PYTHON_LIBS[@]}
CURRENT_LIB=0

echo -e "${GREEN_BOLD}🚀 Đang cài đặt thư viện Python...${RESET}"
for lib in "${PYTHON_LIBS[@]}"; do
    ((CURRENT_LIB++))
    PERCENT=$((CURRENT_LIB * 100 / TOTAL_LIBS))
    echo -ne "${YELLOW_BOLD}🔄 [$CURRENT_LIB/$TOTAL_LIBS] Cài đặt $lib... ($PERCENT%)${RESET}\r"
    pip3 install --quiet --timeout=60 -i https://pypi.tuna.tsinghua.edu.cn/simple $lib
done
echo -e "\n${GREEN_BOLD}✔ Tất cả thư viện đã được cài đặt thành công!${RESET}"

# === Cấu hình iptables ===
echo -e "${GREEN_BOLD}🛡️ Cấu hình iptables để bảo vệ hệ thống...${RESET}"
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -j DROP
echo -e "${GREEN_BOLD}✔ Cấu hình iptables hoàn tất! Kiểm tra bằng: sudo iptables -L -v${RESET}"

# === Hướng dẫn rollback iptables nếu mất mạng ===
echo -e "${RED_BOLD}⚠ Nếu mất mạng, chạy lệnh sau để khôi phục:${RESET}"
echo -e "${GREEN_BOLD}sudo iptables --flush${RESET}"

# === Kiểm tra & chạy vbs.py ===
if [[ -f "vbs.py" ]]; then
    echo -e "${GREEN_BOLD}🚀 Chạy vbs.py...${RESET}"
    if ! python3 vbs.py; then
        echo -e "${RED_BOLD}❌ Lỗi khi chạy vbs.py! Kiểm tra lại mã nguồn.${RESET}"
        exit 1
    fi
else
    echo -e "${RED_BOLD}❌ Không tìm thấy vbs.py! Kiểm tra lại thư mục.${RESET}"
fi