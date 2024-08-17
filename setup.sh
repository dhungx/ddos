#!/bin/bash

# Hàm kiểm tra hệ điều hành
detect_os() {
    echo "Xác định hệ điều hành..."

    if [[ "$(uname -s)" == "Linux" ]]; then
        if [[ -f /etc/os-release ]]; then
            . /etc/os-release
            if [[ "$ID" == "kali" ]]; then
                echo "Phát hiện Kali Linux"
                return 0
            elif [[ "$ID" == "termux" ]]; then
                echo "Phát hiện Termux"
                return 0
            elif [[ "$ID" == "ish" ]]; then
                echo "Phát hiện iSH"
                return 0
            else
                echo "Phát hiện hệ điều hành Linux khác"
                return 1
            fi
        else
            echo "Không thể xác định hệ điều hành Linux từ /etc/os-release"
            return 1
        fi
    elif [[ "$(uname -s)" == "Darwin" ]]; then
        echo "Phát hiện macOS"
        return 1
    elif [[ "$(uname -s)" == "MINGW64_NT"* || "$(uname -s)" == "MINGW32_NT"* || "$(uname -s)" == "MSYS_NT"* ]]; then
        echo "Phát hiện Windows"
        return 0
    else
        echo "Hệ điều hành không xác định hoặc không hỗ trợ"
        return 1
    fi
}

# Cài đặt các gói Python bằng pip
install_packages() {
    echo "Cài đặt các gói Python cần thiết..."
    pip install --upgrade pip
    pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3
}

# Cài đặt các công cụ cần thiết trên Kali Linux
install_kali_tools() {
    echo "Cài đặt các công cụ cần thiết trên Kali Linux..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
}

# Cài đặt các công cụ cần thiết trên Termux
install_termux_tools() {
    echo "Cài đặt các công cụ cần thiết trên Termux..."
    pkg update
    pkg install -y python
    pip install --upgrade pip
}

# Cài đặt các công cụ cần thiết trên iSH
install_ish_tools() {
    echo "Cài đặt các công cụ cần thiết trên iSH..."
    apk update
    apk add python3 py3-pip
    pip3 install --upgrade pip
}

# Cài đặt các công cụ cần thiết trên Windows
install_windows_tools() {
    echo "Cài đặt các công cụ cần thiết trên Windows..."
    python -m pip install --upgrade pip
}

# Xử lý hệ điều hành không được hỗ trợ
handle_unsupported_os() {
    echo "Hệ điều hành của bạn không được hỗ trợ cho việc cài đặt tự động gói Python."
    echo "Vui lòng cài đặt các gói Python theo cách thủ công với lệnh sau:"
    echo "pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3"
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

# Gọi hàm để kiểm tra hệ điều hành và cài đặt gói
detect_os
if [[ $? -eq 0 ]]; then
    install_packages
    case "$(uname -s)" in
        Linux)
            if grep -q "ID=kali" /etc/os-release; then
                install_kali_tools
            elif grep -q "ID=termux" /etc/os-release; then
                install_termux_tools
            elif grep -q "ID=ish" /etc/os-release; then
                install_ish_tools
            fi
            ;;
        Darwin)
            # macOS đã được xác định
            ;;
        MINGW64_NT*|MINGW32_NT*|MSYS_NT*)
            install_windows_tools
            ;;
        *)
            handle_unsupported_os
            ;;
    esac

    # Hỏi người dùng có muốn chạy ddos.py không
    ask_to_run_ddos
else
    handle_unsupported_os
fi