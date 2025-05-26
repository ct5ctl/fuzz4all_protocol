import os
import socket
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult
from Fuzz4All.model import make_model


class FTPTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_dict = kwargs.get("config_dict", {})
        self.model = make_model(
            eos=[],
            model_name=kwargs["model_name"],
            device=kwargs["device"],
            max_length=kwargs["max_length"],
        )

    def initialize(self):
        # 构造生成提示词
        self.prompt = self.build_prompt()
        self.generated_count = 0

    def build_prompt(self) -> str:

        config = self.config_dict
        target_config = config["target"]
        prompt = ""

        # 触发提示词
        if "trigger_to_generate_input" in target_config:
            prompt += self.wrap_in_comment(target_config["trigger_to_generate_input"]) + "\n"

        # 输入提示
        if "input_hint" in target_config:
            prompt += target_config["input_hint"] + "\n"

        # 添加文档内容
        doc_path = target_config.get("path_documentation", "")
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                prompt += "\n# Documentation:\n" + f.read() + "\n"

        # 添加示例代码内容
        code_path = target_config.get("path_example_code", "")
        if os.path.exists(code_path):
            if os.path.isdir(code_path):
                for root, _, files in os.walk(code_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            prompt += f"\n# Code File: {file}\n" + f.read() + "\n"
            else:
                with open(code_path, "r", encoding="utf-8", errors="ignore") as f:
                    prompt += "\n# Example Code:\n" + f.read() + "\n"

        return prompt

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
    
    def wrap_in_comment(self, prompt: str) -> str:
        # FTP 请求没有真正的注释语法，用 # 表示注释对模型即可
        return f"# {prompt}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        if success:
            print(f"[VALID] {file_path}: {message}")
        else:
            print(f"[INVALID] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        # 可以记录哪些输入是无效的，当前不做处理
        pass
