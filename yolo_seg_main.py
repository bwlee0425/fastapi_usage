from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import asyncio
from ultralytics import YOLO

app = FastAPI()

# Load a model
model = YOLO("yolo11n-seg.pt")

async def extract_yolo_image(image_bytes):
    # 이미지를 PIL로 열기
    image = Image.open(io.BytesIO(image_bytes))
    
    # 이미지를 RGB로 변환 (EasyOCR은 RGB 형식을 요구함)
    image = image.convert('RGB')
    results = model(image)
    results[0].save("output.png")

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    # 파일 읽기
    image_data = await file.read()
    
    # 텍스트 추출
    extracted_text = await extract_yolo_image(image_data)
    return {"status":"done"}


