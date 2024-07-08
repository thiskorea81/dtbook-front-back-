import fitz  # PyMuPDF
from openai import OpenAI
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import numpy as np
import cv2

app = FastAPI()
client = OpenAI() #


# CORS 설정 추가
origins = [
    "http://localhost:5173",  # Vue.js 개발 서버의 주소
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

def convert_text_with_openai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Rewrite the following text in a more elegant and professional style:\n\n{text}"},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in processing text with OpenAI: {e}"

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
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"image_page{page_num+1}_{img_index}.{image_ext}"
            image_path = os.path.join(pdf_folder, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            images.append(os.path.join(os.path.basename(pdf_folder), image_filename))
    
    return JSONResponse(content={"text": text_content, "images": images})

@app.post("/chat")
async def chat_with_student(prompt: dict):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "학생과 책과 관련된 모르는 부분에 대한 질문에 답하는 역할"},
                {"role": "user", "content": prompt["prompt"]}
            ]
        )
        return JSONResponse(content={"response": response.choices[0].message.content})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
