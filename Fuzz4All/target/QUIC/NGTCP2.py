import os
from typing import List, Tuple

from Fuzz4All.target.target import Target, FResult
from Fuzz4All.model import make_model


class NGTCP2Target(Target):
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

        # 添加提示词
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
        NGTCP2 验证占位逻辑：你可以集成 nghttp3/ngtcp2 服务后通过 quic 客户端测试。
        当前返回 True 以便调试。
        """
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return True, f"Loaded {len(data)} bytes of QUIC data"
        except Exception as e:
            return False, f"Failed to read file: {str(e)}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"# {prompt}"

    def parse_validation_message(self, success: bool, message: str, file_path: str):
        status = "VALID" if success else "INVALID"
        print(f"[{status}] {file_path}: {message}")

    def update(self, prev: List[Tuple[FResult, str]]):
        pass
