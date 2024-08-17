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
    pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3
}

# Xử lý hệ điều hành không được hỗ trợ
handle_unsupported_os() {
    echo "Hệ điều hành của bạn không được hỗ trợ cho việc cài đặt tự động gói Python."
    echo "Vui lòng cài đặt các gói Python theo cách thủ công với lệnh sau:"
    echo "pip install requests>=2.28.1 colorama>=0.4.5 humanfriendly>=10.0 PySocks>=1.7.1 scapy>=2.4.5 get_mac>=0.8.3"
}

# Gọi hàm để kiểm tra hệ điều hành và cài đặt gói
detect_os
if [[ $? -eq 0 ]]; then
    install_packages
else
    handle_unsupported_os
fi