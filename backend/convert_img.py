import cv2
import os
import glob
import shutil
import numpy as np

def correct_image_colors(image):
    if image is None:
        return None
    
    # Convert image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image to different channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))
    
    # Convert image from LAB color space back to BGR color space
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return final

def process_images(input_folder):
    output_folder = os.path.join(input_folder, 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # JPEG 및 JPG 파일 검색
    jpeg_files = glob.glob(os.path.join(input_folder, '*.[jJ][pP][gG]')) + \
                 glob.glob(os.path.join(input_folder, '*.[jJ][pP][eE][gG]'))
    
    # PNG 파일 검색
    png_files = glob.glob(os.path.join(input_folder, '*.[pP][nN][gG]'))
    
    for file in jpeg_files:
        try:
            if not os.path.isfile(file):
                print(f"File does not exist: {file}")
                continue
            
            # 이미지 읽기
            image = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                print(f"Failed to read image: {file}")
                continue
            
            # 색상 조정
            corrected_image = correct_image_colors(image)
            
            # 출력 파일 경로 생성 (PNG 파일로 저장)
            base_name = os.path.basename(file)
            name, ext = os.path.splitext(base_name)
            output_file = os.path.join(output_folder, f"{name}.png")
            
            # 수정된 이미지 저장
            cv2.imwrite(output_file, corrected_image)
            print(f"Processed and saved: {output_file}")
        
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    
    for file in png_files:
        try:
            if not os.path.isfile(file):
                print(f"File does not exist: {file}")
                continue
            
            # 출력 파일 경로 생성
            base_name = os.path.basename(file)
            output_file = os.path.join(output_folder, base_name)
            
            # PNG 파일 복사
            shutil.copy(file, output_file)
            print(f"Copied: {output_file}")
        
        except Exception as e:
            print(f"Error copying file {file}: {e}")

# 사용 예시
input_folder = r'D:\myGit\dtbook-front-back-\backend\extracted_images\sample_images'  # 입력 폴더 경로

process_images(input_folder)
