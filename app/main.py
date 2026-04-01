from fastapi import FastAPI, HTTPException
from app.schemas import PredictRequest
from app.model import predict
from app.utils import image_to_base64, validate_image_options, validate_prompt

app = FastAPI(title="Lab1 API")

@app.get("/")
def root():
    return {
        "message": "This is a HuggingFace text-to-image API using FastAPI"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict_api(req: PredictRequest):
    try:
        validate_prompt(req.prompt)
        validate_image_options(req.height, req.width)
        result = predict(
            prompt=req.prompt,
            negative_prompt=req.negative_prompt,
            num_inference_steps=req.num_inference_steps,
            guidance_scale=req.guidance_scale,
            height=req.height,
            width=req.width,
            seed=req.seed,
        )
        return {
            "success": True,
            "data": {
                "model_id": result["model_id"],
                "device": result["device"],
                "images": [
                    {
                        "index": index,
                        "format": "PNG",
                        "base64": image_to_base64(image),
                    }
                    for index, image in enumerate(result["images"])
                ],
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
