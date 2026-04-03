import zipfile
import os


def extract_images_from_hwpx(file_path, output_dir):
    """HWPX 파일(ZIP 구조)에서 이미지를 추출하여 저장합니다."""
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    extracted_paths = []

    with zipfile.ZipFile(file_path, "r") as zf:
        img_index = 1
        for item in zf.namelist():
            if item.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                img_data = zf.read(item)
                ext = os.path.splitext(item)[1]
                new_filename = f"{base_name}_{img_index}{ext}"
                save_path = os.path.join(output_dir, new_filename)

                with open(save_path, "wb") as f:
                    f.write(img_data)

                extracted_paths.append(save_path)
                img_index += 1

    return extracted_paths
