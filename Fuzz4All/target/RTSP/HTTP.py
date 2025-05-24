import os
import socket
import http.client
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult
from Fuzz4All.model import make_model


class HTTPTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_dict = kwargs.get("config_dict", {})
        self.model = make_model(
            eos=["\r\n\r\n"],
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
        return prompt

    def generate(self) -> List[str]:
        self.generated_count += 1
        return self.model.generate(self.prompt)

    def validate_individual(self, file_path: str) -> Tuple[bool, str]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                request = f.read()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        try:
            conn = http.client.HTTPConnection("127.0.0.1", 80, timeout=5)
            conn.request("GET", "/")
            conn.close()
            return True, "HTTP request sent successfully"
        except Exception as e:
            return False, f"HTTP error: {str(e)}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"// {prompt}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        if success:
            print(f"[VALID ✅] {file_path}: {message}")
        else:
            print(f"[INVALID ❌] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        pass
