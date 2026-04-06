import olefile
import zlib
import os


def extract_images_from_hwp(file_path, output_dir):
    """HWP 파일(OLE 구조)에서 이미지를 추출하여 저장합니다."""
    # 문서 확장자 제외 이름 추출
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
                # 이미지가 맞다면 연결
                stream = ole.openstream(d)
                # 이미지 데이터 통째로 읽어오기
                data = stream.read()

                # HWP zlib 압축 해제
                try:
                    decompressed_data = zlib.decompress(data, -15)
                except zlib.error:
                    try:
                        decompressed_data = zlib.decompress(data)
                    except zlib.error:
                        decompressed_data = data

                # 원본 이미지의 확장자 가져오기
                ext = os.path.splitext(stream_name)[1]
                # 새 파일 이름 만들기
                new_filename = f"{base_name}_{img_index}{ext}"
                # 저장할 폴더와 새 이름을 합쳐 최종 주소 만들기
                save_path = os.path.join(output_dir, new_filename)

                with open(save_path, "wb") as f:
                    f.write(decompressed_data)

                # 성공한 파일 주소 담기
                extracted_paths.append(save_path)
                img_index += 1

    ole.close()
    return extracted_paths
