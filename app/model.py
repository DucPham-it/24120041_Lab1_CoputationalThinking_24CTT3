import os
from functools import lru_cache
from typing import Any

MODEL_ID = os.getenv("SDXS_MODEL_ID", "AiArtLab/sdxs-1b")


def _get_runtime_modules():
    try:
        import torch
        from diffusers import DiffusionPipeline

        return torch, DiffusionPipeline
    except Exception as exc:
        raise RuntimeError(
            "Missing dependencies for image generation. "
            "Please install torch, diffusers, transformers, accelerate, safetensors and pillow."
        ) from exc


def _get_runtime_config() -> tuple[str, Any]:
    torch, _ = _get_runtime_modules()

    if torch.cuda.is_available():
        return "cuda", torch.float16

    return "cpu", torch.float32


@lru_cache(maxsize=1)
def get_pipeline():
    _, DiffusionPipeline = _get_runtime_modules()
    device, dtype = _get_runtime_config()

    try:
        pipe = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            trust_remote_code=True,
        )
        pipe = pipe.to(device)

        if device == "cuda":
            pipe.enable_attention_slicing()

        return pipe
    except Exception as exc:
        raise RuntimeError(
            "Cannot load model 'AiArtLab/sdxs-1b'. "
            "Please make sure torch, diffusers, transformers, accelerate, safetensors "
            "are installed and the model can be downloaded from Hugging Face."
        ) from exc


def predict(
    prompt: str,
    negative_prompt: str,
    num_inference_steps: int,
    guidance_scale: float,
    height: int,
    width: int,
    seed: int | None = None,
) -> dict[str, Any]:
    torch, _ = _get_runtime_modules()
    pipe = get_pipeline()
    device, _ = _get_runtime_config()
    generator = None

    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)

    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width,
        generator=generator,
    )

    return {
        "model_id": MODEL_ID,
        "device": device,
        "images": result.images,
    }
