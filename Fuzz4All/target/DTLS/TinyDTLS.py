import os
import socket
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult
from Fuzz4All.model import make_model


class TinyDTLSTarget(Target):
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

        doc_path = target_config.get("path_documentation", "")
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                prompt += "\n# Documentation:\n" + f.read() + "\n"

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
        尝试向 tinydtls 服务器发送 DTLS 数据报。
        """
        try:
            with open(file_path, "rb") as f:
                payload = f.read()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(3)
            s.sendto(payload, ("127.0.0.1", 20220))  # tinydtls 默认 DTLS 端口
            data, _ = s.recvfrom(1024)
            if data:
                return True, f"Received response: {data[:50].hex()}"
            else:
                return False, "No response from TinyDTLS"
        except Exception as e:
            return False, f"DTLS error: {str(e)}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"# {prompt}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        status = "VALID" if success else "INVALID"
        print(f"[{status}] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        pass
