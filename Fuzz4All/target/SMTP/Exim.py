import os
import socket
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult
from Fuzz4All.model import make_model


class EximTarget(Target):
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
        self.prompt = self.build_prompt()
        self.generated_count = 0

    def build_prompt(self) -> str:
        config = self.config_dict
        target_config = config["target"]
        prompt = ""

        if "trigger_to_generate_input" in target_config:
            prompt += self.wrap_in_comment(target_config["trigger_to_generate_input"]) + "\n"
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
        尝试连接本地 Exim SMTP 服务并发送生成的 SMTP 命令，判断是否回应 250。
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = f.read()
        except Exception as e:
            return False, f"File read error: {e}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(("127.0.0.1", 25))  # Exim 默认 SMTP 端口
            banner = s.recv(1024).decode(errors="ignore")

            for line in payload.strip().splitlines():
                if not line.endswith("\r\n"):
                    line += "\r\n"
                s.sendall(line.encode("utf-8"))
                resp = s.recv(1024).decode(errors="ignore")
                if not resp.startswith("2"):  # 非 250/220 开头说明错误
                    return False, f"SMTP error: {resp.strip()}"

            s.close()
            return True, "SMTP interaction successful"
        except Exception as e:
            return False, f"SMTP socket error: {e}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"# {prompt}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        status = "VALID" if success else "INVALID"
        print(f"[{status}] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        pass
