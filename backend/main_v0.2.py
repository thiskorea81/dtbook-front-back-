import fitz  # PyMuPDF
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os
import io
from PIL import Image

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:5173",  # Vue.js 개발 서버의 주소
    "http://127.0.0.1:5173",  # 추가로 127.0.0.1 주소도 포함
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "extracted_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 정적 파일 제공 설정
app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    pdf_name = file.filename
    pdf_folder = os.path.join(UPLOAD_FOLDER, os.path.splitext(pdf_name)[0])
    os.makedirs(pdf_folder, exist_ok=True)
    
    file_location = os.path.join(pdf_folder, pdf_name)
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    pdf_document = fitz.open(file_location)
    
    text_content = []
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text_content.append(page.get_text("text"))

        image_list = page.get_images(full=True)
        print(f"Page {page_num+1} has {len(image_list)} images.")
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = "png"  # 모든 이미지를 png로 저장
                image_filename = f"image_page{page_num+1}_{img_index}.{image_ext}"
                image_path = os.path.join(pdf_folder, image_filename)
                
                # OpenCV를 사용하여 이미지를 PNG로 변환 및 저장
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                if image is not None:
                    if len(image.shape) == 2:  # 그레이스케일 이미지
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                    elif image.shape[2] == 4:  # 이미지가 RGBA인 경우
                        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                    else:  # 그 외의 경우는 RGB로 변환
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(image_path, image)
                    print(f"Saved image {image_filename} at {os.path.abspath(image_path)}")
                else:
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    print(f"Saved image {image_filename} at {os.path.abspath(image_path)} without conversion")
                
                images.append(os.path.join(os.path.basename(pdf_folder), image_filename))
            except Exception as e:
                print(f"Error processing image on page {page_num+1}, index {img_index}: {str(e)}")
    
    return JSONResponse(content={"text": text_content, "images": images})
