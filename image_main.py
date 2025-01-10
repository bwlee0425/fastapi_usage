from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image, ImageOps, ImageFilter
import io

app = FastAPI()

# 이미지 변환 작업을 위한 딕셔너리
transformations = {}

@app.post("/upload/", response_class=HTMLResponse)
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        # 이미지 파일 읽기
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # 변환 작업을 수행하여 딕셔너리에 저장
        transformations["Original"] = image

        # 이미지가 RGBA 모드인 경우 RGB로 변환
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # 다양한 변환 작업
        transformations["Grayscale"] = image.convert("L")
        transformations["Inverted"] = ImageOps.invert(image)
        transformations["Blur"] = image.filter(ImageFilter.BLUR)
        transformations["Edges"] = image.filter(ImageFilter.FIND_EDGES)
        transformations["Sharpen"] = image.filter(ImageFilter.SHARPEN)
        transformations["Contrast"] = ImageOps.autocontrast(image)
        transformations["Flipped"] = ImageOps.mirror(image)
        transformations["Rotated"] = image.rotate(45)

        # HTML 출력 준비
        html_content = "<html><body><h1>Transformed Images</h1>"
        for name, img in transformations.items():
            # 각 이미지를 BytesIO에 저장
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # 각 변환 이미지를 StreamingResponse로 반환
            html_content += f"<h3>{name}</h3>"
            html_content += f'<img src="/image/{name}" alt="{name}" style="max-width:500px;"/>'

        html_content += "</body></html>"

        return HTMLResponse(content=html_content)

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    # 변환된 이미지가 존재하면 StreamingResponse로 반환
    if image_name in transformations:
        img = transformations[image_name]
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/")
def read_root():
    return {"Hello": "World"}
