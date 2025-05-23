import os
import requests
from typing import List, Dict, Optional


EOF_STRINGS = ["<|endoftext|>", "###"]


class DeepSeekCoder:
    def __init__(self, model_name: str, device: str, eos: List[str], max_length: int):
        """
        Initialize the DeepSeek model wrapper.

        Args:
            model_name: Model name used by DeepSeek (e.g., "deepseek-chat").
            device: Placeholder for compatibility.
            eos: Custom end-of-sequence strings.
            max_length: Maximum number of tokens to generate.
        """
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Please set the environment variable DEEPSEEK_API_KEY with your API key.")
        self.model_name = model_name
        self.eos = EOF_STRINGS + eos
        self.max_length = max_length
        self.prefix_token = "<fim_prefix>"
        self.suffix_token = "<fim_suffix><fim_middle>"

    def _build_prompt(self, prompt: str) -> str:
        return self.prefix_token + prompt + self.suffix_token

    def _strip_output(self, text: str) -> str:
        """
        Strips generated text at the first occurrence of any EOS string.
        """
        min_index = len(text)
        for eos in self.eos:
            if eos in text:
                min_index = min(min_index, text.index(eos))
        return text[:min_index]

    def generate(self, prompt: str, batch_size=1, temperature=1.0, max_length=512) -> List[str]:
        """
        Generates text using DeepSeek API.

        Args:
            prompt: Input prompt string.
            batch_size: Number of completions to return.
            temperature: Sampling temperature.
            max_length: Maximum token length.

        Returns:
            A list of decoded strings.
        """
        full_prompt = self._build_prompt(prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": max(temperature, 1e-2),
            "n": batch_size,
            "stop": self.eos,
            "max_tokens": min(max_length, self.max_length)
        }

        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"DeepSeek API Error {response.status_code}: {response.text}")

        results = response.json()
        return [
            self._strip_output(choice["message"]["content"])
            for choice in results.get("choices", [])
        ]


def make_model(eos: List[str], model_name: str, device: str, max_length: int):
    """
    Factory function to create a model interface.

    Args:
        eos: List of custom end-of-sequence tokens.
        model_name: Model name (e.g., 'deepseek-chat').
        device: Placeholder for compatibility.
        max_length: Max token length for generation.

    Returns:
        A model object with a `generate()` method.
    """
    kwargs_for_model = {
        "model_name": model_name,
        "eos": eos,
        "device": device,
        "max_length": max_length,
    }
    print("[DEBUG] Using DeepSeekCoder backend")
    print("=== Model Config ===")
    for k, v in kwargs_for_model.items():
        print(f"{k}: {v}")

    if "deepseek" in model_name.lower():
        model_obj = DeepSeekCoder(**kwargs_for_model)
    else:
        raise ValueError(f"Unknown model backend for: {model_name}")

    print(f"model_obj (class name): {model_obj.__class__.__name__}")
    print("====================")

    return model_obj
