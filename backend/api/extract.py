import fitz  # PyMuPDF
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import os
from utils.pdf_utils import save_image

UPLOAD_FOLDER = "extracted_images"

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
            image_filename = f"image_page{page_num+1}_{img_index}.png"
            image_path = os.path.join(pdf_folder, image_filename)
            save_image(image_bytes, image_path)
            images.append(os.path.join(os.path.basename(pdf_folder), image_filename))
    
    return JSONResponse(content={"text": text_content, "images": images})
