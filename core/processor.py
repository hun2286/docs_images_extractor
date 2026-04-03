import os
import glob
from core.hwp_parser import extract_images_from_hwp
from core.hwpx_parser import extract_images_from_hwpx


def process_all_files(input_dir):
    """폴더를 스캔하여 파일별로 이미지를 추출하고 분류함"""

    # input_docs 폴더 체크 및 생성
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"'{input_dir}' 폴더가 없어 새로 생성했습니다. 문서를 넣어주세요.")
        return

    # 대상 파일 스캔
    files = glob.glob(os.path.join(input_dir, "*.hwp")) + glob.glob(os.path.join(input_dir, "*.hwpx"))

    if not files:
        print(f"'{input_dir}' 폴더에 처리할 한글 파일이 없습니다.")
        return

    print(f"총 {len(files)}개의 파일을 발견했습니다.\n")

    for file_path in files:
        file_name = os.path.basename(file_path)
        name_only = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_name)[1].lower()

        # 결과 저장 폴더: output_images/[파일명]
        target_dir = os.path.join(os.getcwd(), "output_images", name_only)
        os.makedirs(target_dir, exist_ok=True)

        print(f"[{file_name}] 추출 시작...", end=" ", flush=True)

        try:
            if ext == ".hwp":
                res = extract_images_from_hwp(file_path, target_dir)
            else:
                res = extract_images_from_hwpx(file_path, target_dir)

            if res:
                print(f"완료! ({len(res)}개 저장)")
            else:
                print("이미지 없음")
        except Exception as e:
            print(f"실패 (사유: {e})")

    print("\n모든 작업이 완료되었습니다.")
