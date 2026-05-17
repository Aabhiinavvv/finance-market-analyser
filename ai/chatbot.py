import os
from typing import Any

import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"


def _get_hf_token() -> str:
    # Support common env var names used by HF tooling.
    return (
        os.getenv("HF_TOKEN")
        or os.getenv("hf_token")
        or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        or os.getenv("huggingfacehub_api_token")
        or os.getenv("HUGGING_FACE_HUB_TOKEN")
        or os.getenv("hugging_face_hub_token")
        or ""
    )


def _build_headers() -> dict[str, str]:
    token = _get_hf_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _extract_content(data: Any) -> str | None:
    if isinstance(data, dict) and data.get("choices"):
        message = data["choices"][0].get("message", {})
        content = message.get("content")
        if isinstance(content, str) and content.strip():
            return content
    return None


def _candidate_models() -> list[str]:
    requested = os.getenv("HF_MODEL", "").strip()

    # HF router provider suffixes (like :fastest) can fail depending on account/provider setup.
    # Try both with and without suffix, then known safe defaults.
    candidates: list[str] = []
    if requested:
        candidates.append(requested)
        if ":" in requested:
            candidates.append(requested.split(":", 1)[0])

    if not requested:
        tinyllama_default = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        candidates.extend([tinyllama_default, DEFAULT_MODEL])
    else:
        candidates.append(DEFAULT_MODEL)

    # Keep order, remove duplicates.
    unique: list[str] = []
    for model in candidates:
        if model and model not in unique:
            unique.append(model)
    return unique


def ask_finance(prompt: str) -> str:
    if not _get_hf_token():
        return (
            "Missing Hugging Face token. Set HF_TOKEN (or HUGGINGFACEHUB_API_TOKEN) "
            "in your environment and retry."
        )

    last_error = ""

    for model_id in _candidate_models():
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400,
            "temperature": 0.6,
            "stream": False,
        }

        try:
            response = requests.post(API_URL, headers=_build_headers(), json=payload, timeout=60)

            if response.status_code != 200:
                text = response.text

                # Common bug from screenshot: model_not_supported. Try next candidate model.
                if response.status_code == 400 and "model_not_supported" in text:
                    last_error = f"{model_id}: {text}"
                    continue

                if response.status_code == 404:
                    return (
                        f"HF model endpoint not found for '{model_id}'. "
                        "Set HF_MODEL to a valid model id and retry."
                    )
                return f"HF API Error {response.status_code}: {text}"

            data = response.json()

            if isinstance(data, dict) and "error" in data:
                err = str(data["error"])
                if "model_not_supported" in err:
                    last_error = f"{model_id}: {err}"
                    continue
                return f"HF Error: {err}"

            content = _extract_content(data)
            if content:
                return content

            return f"Unexpected HF response format: {data}"

        except requests.RequestException as e:
            last_error = str(e)

    model_list = ", ".join(_candidate_models())
    return (
        "No compatible HF model was available for your account/providers. "
        f"Tried: {model_list}. "
        "Set HF_MODEL to a model enabled on your HF router account. "
        f"Last error: {last_error}"

    )