from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import easyocr
import asyncio

app = FastAPI()
reader = easyocr.Reader(['en','kr'])

async def extract_text_from_image(image_bytes):
    # 이미지를 PIL로 열기
    image = Image.open(io.BytesIO(image_bytes))
    
    # 이미지를 RGB로 변환 (EasyOCR은 RGB 형식을 요구함)
    image = image.convert('RGB')
    
    # 이미지를 바이트로 변환
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # EasyOCR로 텍스트 추출 (동기 함수를 비동기로 실행)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, reader.readtext, img_byte_arr)
    
    # 추출된 텍스트만 반환
    return [detection[1] for detection in result]

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    # 파일 읽기
    image_data = await file.read()
    
    # 텍스트 추출
    extracted_text = await extract_text_from_image(image_data)
    
    # 결과 반환
    return {"filename": file.filename, "extracted_text": extracted_text}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        # 이미지 파일 읽기
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # 이미지를 그레이스케일로 변환
        gray_image = image.convert('L')       

        # 변환된 이미지를 byte로 변환
        img_byte_arr = io.BytesIO()
        gray_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # StreamingResponse로 이미지 반환
        return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")
    else:
        raise HTTPException(status_code=400, detail="Invalid file format.")

@app.get("/")
def read_root():
    return {"Hello": "Lion"}