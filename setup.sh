#!/bin/bash

# Hàm cài đặt các gói Python bằng pip
install_packages() {
    echo "Cài đặt các gói Python cần thiết..."
    pip install --upgrade pip
    pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3
}

# Cài đặt các công cụ cần thiết cho Kali Linux
install_kali_tools() {
    echo "Cài đặt các công cụ cần thiết trên Kali Linux..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
}

# Cài đặt các công cụ cần thiết cho Termux
install_termux_tools() {
    echo "Cài đặt các công cụ cần thiết trên Termux..."
    pkg update
    pkg install -y python
    pip install --upgrade pip
}

# Cài đặt các công cụ cần thiết cho iSH
install_ish_tools() {
    echo "Cài đặt các công cụ cần thiết trên iSH..."
    apk update
    apk add python3 py3-pip
    pip3 install --upgrade pip
}

# Cài đặt các công cụ cần thiết cho Windows
install_windows_tools() {
    echo "Cài đặt các công cụ cần thiết trên Windows..."
    python -m pip install --upgrade pip
}

# Hỏi người dùng chọn hệ điều hành và thực hiện cài đặt tương ứng
ask_os_and_install() {
    echo "Vui lòng chọn hệ điều hành của bạn:"
    echo "1) Kali Linux"
    echo "2) Termux"
    echo "3) iSH"
    echo "4) Windows"
    echo "5) Khác"
    read -p "Nhập số tương ứng: " choice

    case "$choice" in
        1)
            install_kali_tools
            ;;
        2)
            install_termux_tools
            ;;
        3)
            install_ish_tools
            ;;
        4)
            install_windows_tools
            ;;
        5)
            echo "Cài đặt thủ công. Vui lòng cài đặt các gói Python cần thiết và công cụ bằng cách sử dụng lệnh sau:"
            echo "pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3"
            ;;
        *)
            echo "Lựa chọn không hợp lệ. Không thể cài đặt công cụ tự động."
            ;;
    esac
}

# Hỏi người dùng có muốn chạy ddos.py không
ask_to_run_ddos() {
    read -p "Bạn có muốn chạy tệp ddos.py không? [y/n]: " choice
    case "$choice" in
        y|Y)
            if [[ -f "ddos.py" ]]; then
                echo "Đang chạy ddos.py..."
                python3 ddos.py
            else
                echo "Tệp ddos.py không tồn tại trong thư mục hiện tại."
            fi
            ;;
        n|N)
            echo "Không chạy ddos.py. Kết thúc."
            ;;
        *)
            echo "Lựa chọn không hợp lệ. Vui lòng chọn 'y' hoặc 'n'."
            ;;
    esac
}

# Cài đặt các gói Python và hỏi hệ điều hành
install_packages
ask_os_and_install

# Hỏi người dùng có muốn chạy ddos.py không
ask_to_run_ddos