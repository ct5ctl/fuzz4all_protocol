import os
import socket
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult


class FTPTarget(Target):
    def initialize(self):
        # 构造生成提示词
        self.prompt = self.build_prompt()
        self.generated_count = 0

    def generate(self) -> List[str]:
        self.generated_count += 1
        return self.model.generate(self.prompt)

    def validate_individual(self, file_path: str) -> Tuple[bool, str]:
        """
        发送 FTP 报文到服务器并返回响应，用于 On-the-Fly 验证。
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = f.read()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        try:
            # 创建连接
            s = socket.socket()
            s.settimeout(5)
            s.connect(("127.0.0.1", 21))  # 默认 FTP 服务地址
            banner = s.recv(1024).decode(errors="ignore")

            # 发送每行命令
            for line in payload.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                if not line.endswith("\r\n"):
                    line += "\r\n"
                s.sendall(line.encode("utf-8"))
                s.recv(1024)  # 接收响应，但不深度分析

            s.close()
            return True, "FTP command executed successfully"
        except Exception as e:
            return False, f"FTP error: {str(e)}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        if success:
            print(f"[VALID ✅] {file_path}: {message}")
        else:
            print(f"[INVALID ❌] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        # 可以记录哪些输入是无效的，当前不做处理
        pass
