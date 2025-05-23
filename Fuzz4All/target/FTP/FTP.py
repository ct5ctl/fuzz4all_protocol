import os
import socket
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult


class FTPTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_dict = kwargs.get("config_dict", {})
        self.model = make_model(
            eos=[],  # 或 ["\n", "<eom>"] 视你的协议结束标志而定
            model_name=kwargs["model_name"],
            device=kwargs["device"],
            max_length=kwargs["max_length"],
        )

    def initialize(self):
        # 构造生成提示词
        self.prompt = self.build_prompt()
        self.generated_count = 0

    def build_prompt(self) -> str:
        """
        构建发送给 LLM 的 prompt，根据 trigger、hint、文档等拼接而成。
        """
        config = self.config_dict
        target_config = config["target"]
        fuzz_config = config["fuzzing"]

        prompt = ""

        # 包裹触发提示
        if "trigger_to_generate_input" in target_config:
            trigger = self.wrap_in_comment(target_config["trigger_to_generate_input"])
            prompt += trigger + "\n"

        # 添加输入 hint
        if "input_hint" in target_config:
            prompt += target_config["input_hint"] + "\n"

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
            print(f"[VALID ✅] {file_path}: {message}")
        else:
            print(f"[INVALID ❌] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        # 可以记录哪些输入是无效的，当前不做处理
        pass
