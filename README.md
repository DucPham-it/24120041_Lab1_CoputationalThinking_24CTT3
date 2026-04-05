# Lab 1 - FastAPI Hugging Face API

## Thong tin sinh vien

- MSSV: `24120041`
- Ho va ten: `Phạm Võ Đức`
- Mon hoc: `Tu duy tinh toan`

## Mo hinh su dung

- Ten mo hinh: `AiArtLab/sdxs-1b`
- Link Hugging Face: https://huggingface.co/AiArtLab/sdxs-1b
- Loai mo hinh: `Text-to-Image`

## Mo ta he thong

Du an nay xay dung mot Web API bang FastAPI de khai thac mo hinh `AiArtLab/sdxs-1b` tren Hugging Face. Nguoi dung gui prompt mo ta anh, he thong se sinh anh bang mo hinh va tra ket qua duoi dang JSON. Anh duoc ma hoa base64 de de dang gui qua API.

API cung cap 3 endpoint chinh:

- `GET /`: Tra ve thong tin gioi thieu ngan gon ve he thong.
- `GET /health`: Kiem tra trang thai hoat dong cua API.
- `POST /predict`: Nhan prompt va cac tham so sinh anh, goi mo hinh Hugging Face, sau do tra ket qua JSON.

## Cau truc source code

```text
.
|-- app/
|   |-- main.py
|   |-- model.py
|   |-- schemas.py
|   `-- utils.py
|-- test_api.py
|-- requirements.txt
`-- README.md
```

## Cai dat thu vien

Nen tao moi truong ao truoc khi cai dat:

```bash
python -m venv .venv
source .venv/bin/activate
```

Cai dat cac thu vien can thiet:

```bash
pip install -r requirements.txt
```

## Huong dan chay chuong trinh

Khoi dong FastAPI server:

```bash
uvicorn app.main:app --reload
```

Sau khi server chay, co the mo Swagger UI tai:

```text
http://127.0.0.1:8000/docs
```

Kiem tra nhanh hai endpoint co ban:

```text
GET http://127.0.0.1:8000/
GET http://127.0.0.1:8000/health
```

## Huong dan goi API

### 1. Goi bang file Python co san

Chay file test:

```bash
python test_api.py
```

Neu thanh cong, chuong trinh se tao file `generated_image.png`.

### 2. Goi bang cURL

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "anime girl, smiling, red eyes, green hair, white shirt",
    "negative_prompt": "bad quality, low resolution, blurry",
    "num_inference_steps": 30,
    "guidance_scale": 5.5,
    "height": 576,
    "width": 576,
    "seed": 42
  }'
```

## Vi du request/response

### Request JSON

```json
{
  "prompt": "anime girl, smiling, red eyes, green hair, white shirt",
  "negative_prompt": "bad quality, low resolution, blurry",
  "num_inference_steps": 30,
  "guidance_scale": 5.5,
  "height": 576,
  "width": 576,
  "seed": 42
}
```

### Response JSON

```json
{
  "success": true,
  "data": {
    "model_id": "AiArtLab/sdxs-1b",
    "device": "cuda",
    "images": [
      {
        "index": 0,
        "format": "PNG",
        "base64": "iVBORw0KGgoAAAANSUhEUgAA..."
      }
    ]
  }
}
```

## Kiem tra du lieu dau vao va xu ly loi

He thong co kiem tra du lieu dau vao o muc co ban:

- `prompt` khong duoc rong.
- `prompt` toi da `1000` ky tu.
- `height` va `width` phai la boi so cua `64`.
- API tra ve loi `400` neu input khong hop le.
- API tra ve loi `500` neu co loi khi load model hoac suy luan.

## Luu y khi chay

- Lan dau tien chay, model se duoc tai tu Hugging Face nen co the mat kha nhieu thoi gian.
- Mo hinh co kich thuoc lon, neu chay bang CPU thi toc do se cham hon dang ke so voi GPU.
- Can co ket noi Internet de tai model neu may chua co cache san.

## Video demo
[▶ Watch Demo](https://youtu.be/hD8vQYVGnXU)
