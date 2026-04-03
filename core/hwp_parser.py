import olefile
import zlib
import os


def extract_images_from_hwp(file_path, output_dir):
    """HWP 파일(OLE 구조)에서 이미지를 추출하여 저장합니다."""
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    extracted_paths = []

    if not olefile.isOleFile(file_path):
        return []

    ole = olefile.OleFileIO(file_path)
    img_index = 1

    # HWP 내부 리스트를 순회하며 폴더 탐색
    for d in ole.listdir():
        if d[0] == "BinData":
            stream_name = d[1]
            # 이미지 확장자 필터링
            if stream_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                stream = ole.openstream(d)
                data = stream.read()

                # HWP 특유의 zlib 압축 해제 시도
                try:
                    decompressed_data = zlib.decompress(data, -15)
                except zlib.error:
                    try:
                        decompressed_data = zlib.decompress(data)
                    except zlib.error:
                        decompressed_data = data

                ext = os.path.splitext(stream_name)[1]
                new_filename = f"{base_name}_{img_index}{ext}"
                save_path = os.path.join(output_dir, new_filename)

                with open(save_path, "wb") as f:
                    f.write(decompressed_data)

                extracted_paths.append(save_path)
                img_index += 1

    ole.close()
    return extracted_paths
