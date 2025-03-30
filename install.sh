#!/bin/bash
# -*- coding: utf-8 -*-
# Script cải tiến cài đặt và cấu hình môi trường với logging và xử lý lỗi chuyên nghiệp.

# === Cấu hình màu sắc ===
RED_BOLD="\033[1;31m"
GREEN_BOLD="\033[1;32m"
YELLOW_BOLD="\033[1;33m"
RESET="\033[0m"

# === File log ===
LOG_FILE="install.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "==== Bắt đầu cài đặt: $(date) ===="

# === Hàm xóa màn hình terminal ===
clear_screen() {
    case "$OSTYPE" in
        msys*|cygwin*|win32*) cls ;;
        *) clear ;;
    esac
}
clear_screen

# === Kiểm tra quyền root ===
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

# === Kiểm tra dung lượng ổ đĩa (tối thiểu 50MB) ===
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
    local cmd=$1
    local pkg=$2
    if ! command -v "$pkg" &>/dev/null; then
        echo -e "${YELLOW_BOLD}📦 Đang cài đặt ${pkg}...${RESET}"
        eval "$cmd $pkg"
        if [[ $? -ne 0 ]]; then
            echo -e "${RED_BOLD}❌ Cài đặt ${pkg} thất bại.${RESET}"
            exit 1
        fi
    else
        echo -e "${GREEN_BOLD}✔ ${pkg} đã có sẵn.${RESET}"
    fi
}

# === Cài đặt các gói cần thiết ===
install_packages() {
    local install_cmd=""
    case "$os_choice" in
        1)
            install_cmd="sudo apt install -y"
            packages=("python3" "python3-pip" "nmap" "iptables")
            ;;
        2)
            install_cmd="sudo pacman -S --noconfirm"
            packages=("python" "python-pip" "nmap" "iptables")
            ;;
        3)
            install_cmd="sudo apk add"
            packages=("python3" "py3-pip" "nmap" "iptables")
            ;;
        4)
            install_cmd="pkg install -y"
            packages=("python" "nmap")
            ;;
        5)
            if ! command -v brew &>/dev/null; then
                echo -e "${GREEN_BOLD}🍺 Cài đặt Homebrew...${RESET}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            install_cmd="brew install"
            packages=("python" "nmap")
            ;;
        6)
            echo -e "${RED_BOLD}❌ Trên Windows, vui lòng cài đặt Python, pip và nmap thủ công.${RESET}"
            exit 1
            ;;
        *)
            echo -e "${RED_BOLD}❌ Lựa chọn không hợp lệ! Thoát.${RESET}"
            exit 1
            ;;
    esac

    echo -e "${GREEN_BOLD}🔄 Cập nhật hệ thống...${RESET}"
    case "$os_choice" in
        1) sudo apt update && sudo apt upgrade -y ;;
        2) sudo pacman -Syu --noconfirm ;;
        3) sudo apk update && sudo apk upgrade ;;
        4) pkg update && pkg upgrade -y ;;
        5) brew update && brew upgrade ;;
    esac

    for pkg in "${packages[@]}"; do
        check_and_install "$install_cmd" "$pkg"
    done
}

# === Cài đặt pip nếu chưa có ===
install_pip() {
    if ! command -v pip3 &>/dev/null; then
        echo -e "${YELLOW_BOLD}📥 Cài đặt pip3...${RESET}"
        curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py && rm get-pip.py
        if ! command -v pip3 &>/dev/null; then
            echo -e "${RED_BOLD}❌ Cài đặt pip3 thất bại.${RESET}"
            exit 1
        fi
    else
        echo -e "${GREEN_BOLD}✔ pip3 đã có sẵn.${RESET}"
    fi
}

# === Cài đặt thư viện Python ===
install_python_libs() {
    PYTHON_LIBS=("requests" "colorama" "humanfriendly" "PySocks" "scapy" "get-mac")
    TOTAL_LIBS=${#PYTHON_LIBS[@]}
    CURRENT_LIB=0

    echo -e "${GREEN_BOLD}🚀 Đang cài đặt thư viện Python...${RESET}"
    for lib in "${PYTHON_LIBS[@]}"; do
        ((CURRENT_LIB++))
        PERCENT=$((CURRENT_LIB * 100 / TOTAL_LIBS))
        echo -ne "${YELLOW_BOLD}🔄 [${CURRENT_LIB}/${TOTAL_LIBS}] Cài đặt ${lib}... (${PERCENT}%)${RESET}\r"
        pip3 install --quiet --timeout=60 -i https://pypi.tuna.tsinghua.edu.cn/simple "$lib"
        if [[ $? -ne 0 ]]; then
            echo -e "\n${RED_BOLD}❌ Cài đặt ${lib} thất bại.${RESET}"
            exit 1
        fi
    done
    echo -e "\n${GREEN_BOLD}✔ Tất cả thư viện đã được cài đặt thành công!${RESET}"
}

# === Cấu hình iptables ===
configure_iptables() {
    echo -e "${GREEN_BOLD}🛡️ Cấu hình iptables để bảo vệ hệ thống...${RESET}"
    sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    sudo iptables -A INPUT -j DROP
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN_BOLD}✔ Cấu hình iptables hoàn tất! Kiểm tra bằng: sudo iptables -L -v${RESET}"
    else
        echo -e "${RED_BOLD}❌ Cấu hình iptables gặp lỗi.${RESET}"
    fi
    echo -e "${RED_BOLD}⚠ Nếu mất mạng, chạy: sudo iptables --flush${RESET}"
}

# === Chạy file vbs.py nếu tồn tại ===
run_vbs() {
    if [[ -f "vbs.py" ]]; then
        echo -e "${GREEN_BOLD}🚀 Chạy vbs.py...${RESET}"
        if ! python3 vbs.py; then
            echo -e "${RED_BOLD}❌ Lỗi khi chạy vbs.py! Kiểm tra lại mã nguồn.${RESET}"
            exit 1
        fi
    else
        echo -e "${RED_BOLD}❌ Không tìm thấy vbs.py! Kiểm tra lại thư mục.${RESET}"
    fi
}

# === Main process ===
main() {
    install_packages
    install_pip
    install_python_libs
    configure_iptables
    run_vbs
}

main