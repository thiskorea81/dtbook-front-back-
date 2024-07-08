from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os

from api.extract import extract_pdf
from api.chat import chat_with_student
from api.generate import router as generate_router

app = FastAPI()

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

BOOKS_FOLDER = "generated_books"
os.makedirs(BOOKS_FOLDER, exist_ok=True)

# 정적 파일 제공 설정
app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")
app.mount("/books", StaticFiles(directory=BOOKS_FOLDER), name="books")

app.post("/extract")(extract_pdf)
app.post("/chat")(chat_with_student)
app.include_router(generate_router, prefix="/api")
