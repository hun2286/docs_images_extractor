import zipfile
import os


def extract_images_from_hwpx(file_path, output_dir):
    """HWPX 파일(ZIP 구조)에서 이미지를 추출하여 저장합니다."""
    # 문서 확장자 제외 이름 추출
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    extracted_paths = []

    with zipfile.ZipFile(file_path, "r") as zf:
        img_index = 1
        # 압축 파일 내부 모든 파일 이름 확인
        for item in zf.namelist():
            if item.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                # 이미지 파일이면 압축 파일 내부에서 이미지만 읽어오기
                img_data = zf.read(item)
                # 원본 이미지 확장자 가져오기
                ext = os.path.splitext(item)[1]
                new_filename = f"{base_name}_{img_index}{ext}"
                save_path = os.path.join(output_dir, new_filename)

                # 지정한 주소에 새 파일 생성
                with open(save_path, "wb") as f:
                    # 이미지 데이터 새 파일에 넣기
                    f.write(img_data)

                extracted_paths.append(save_path)
                img_index += 1

    return extracted_paths
