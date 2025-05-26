import os
import requests
import datetime
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import openai
from openai import OpenAI


EOF_STRINGS = ["<|endoftext|>", "###"]

# === OpenAI GPT ===
class OpenAICoder:
    def __init__(self, model_name: str, device: str, eos: List[str], max_length: int):
        from openai import OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name
        self.eos = eos
        self.max_length = max_length
        self.token_log_path = "tokens_used.txt"
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def _strip_output(self, text: str) -> str:
        for eos in self.eos:
            idx = text.find(eos)
            if idx != -1:
                return text[:idx]
        return text

    def generate(self, prompt: str, batch_size=1, temperature=1.0, max_length=512) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            n=batch_size,
            stop=self.eos if self.eos else None,
            max_tokens=min(max_length, self.max_length),
        )

        # === Token usage tracking ===
        usage = response.usage
        self.total_prompt_tokens += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens

        # Save token info
        self._log_token_usage(usage.prompt_tokens, usage.completion_tokens)

        return [choice.message.content for choice in response.choices]

    def _log_token_usage(self, prompt_toks, completion_toks):
        with open(self.token_log_path, "a") as f:
            f.write(f"[{datetime.datetime.now()}] prompt: {prompt_toks}, completion: {completion_toks}\n")


# === DeepSeek ===
class DeepSeekCoder:
    def __init__(self, model_name: str, device: str, eos: List[str], max_length: int):
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Please set DEEPSEEK_API_KEY environment variable.")
        self.model_name = model_name
        self.eos = EOF_STRINGS + eos
        self.max_length = max_length
        self.prefix_token = "<fim_prefix>"
        self.suffix_token = "<fim_suffix><fim_middle>"

    def _build_prompt(self, prompt: str) -> str:
        return self.prefix_token + prompt + self.suffix_token

    def _strip_output(self, text: str) -> str:
        for eos in self.eos:
            idx = text.find(eos)
            if idx != -1:
                return text[:idx]
        return text

    def generate(self, prompt: str, batch_size=1, temperature=1.0, max_length=512) -> List[str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": self._build_prompt(prompt)}],
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


# === HuggingFace StarCoder (local) ===
class StarCoder:
    def __init__(self, model_name: str, device: str, eos: List[str], max_length: int):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        self.eos = EOF_STRINGS + eos
        self.device = device
        self.max_length = max_length

    def _strip_output(self, text: str) -> str:
        for eos in self.eos:
            idx = text.find(eos)
            if idx != -1:
                return text[:idx]
        return text

    def generate(self, prompt: str, batch_size=1, temperature=1.0, max_length=512) -> List[str]:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=min(max_length, self.max_length),
            do_sample=True,
            temperature=temperature,
            num_return_sequences=batch_size
        )
        return [self._strip_output(self.tokenizer.decode(output, skip_special_tokens=True)) for output in outputs]


# === Unified Model Interface ===
def make_model(eos: List[str], model_name: str, device: str, max_length: int):
    kwargs_for_model = {
        "model_name": model_name,
        "eos": eos,
        "device": device,
        "max_length": max_length,
    }

    print("[DEBUG] Selecting model backend based on model_name")
    print("=== Model Config ===")
    for k, v in kwargs_for_model.items():
        print(f"{k}: {v}")

    if "gpt" in model_name.lower():
        model_obj = OpenAICoder(**kwargs_for_model)
    elif "deepseek" in model_name.lower():
        model_obj = DeepSeekCoder(**kwargs_for_model)
    else:
        model_obj = StarCoder(**kwargs_for_model)

    print(f"model_obj (class name): {model_obj.__class__.__name__}")
    print("====================")

    return model_obj
