from typing import Optional

from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    negative_prompt: str = Field(default="bad quality, low resolution")
    num_inference_steps: int = Field(default=30, ge=1, le=80)
    guidance_scale: float = Field(default=5.5, ge=0.0, le=20.0)
    height: int = Field(default=576, ge=256, le=1280)
    width: int = Field(default=576, ge=256, le=1280)
    seed: Optional[int] = None
