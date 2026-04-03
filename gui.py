import customtkinter as ctk
from tkinter import filedialog
import os
import glob
import sys
from core.hwp_parser import extract_images_from_hwp
from core.hwpx_parser import extract_images_from_hwpx


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HWP 이미지 추출기 v1.0")
        self.geometry("600x600")

        # 1. 제목 라벨
        self.label = ctk.CTkLabel(self, text="한글 문서 이미지 추출기", font=("나눔고딕", 22, "bold"))
        self.label.pack(pady=20)

        # 2. 버튼 영역 (파일, 폴더, 초기화)
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10, padx=20, fill="x")

        self.btn_files = ctk.CTkButton(self.btn_frame, text="📄 파일 선택", command=self.select_files)
        self.btn_files.pack(side="left", expand=True, padx=5, pady=10)

        self.btn_folder = ctk.CTkButton(self.btn_frame, text="📁 폴더 선택", command=self.select_folder)
        self.btn_folder.pack(side="left", expand=True, padx=5, pady=10)

        self.btn_reset = ctk.CTkButton(
            self.btn_frame, text="🔄 초기화", fg_color="#e74c3c", hover_color="#c0392b", command=self.reset_all
        )
        self.btn_reset.pack(side="left", expand=True, padx=5, pady=10)

        # 3. 저장 위치 옵션 스위치
        self.opt_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.opt_frame.pack(pady=10, padx=20, fill="x")

        self.save_at_exe = ctk.BooleanVar(value=False)
        self.switch_save = ctk.CTkSwitch(
            self.opt_frame, text="실행기(.exe) 위치에 결과 저장하기", variable=self.save_at_exe, font=("나눔고딕", 13)
        )
        self.switch_save.pack(side="left", padx=10)

        # 4. 선택된 경로 표시창
        self.path_display = ctk.CTkTextbox(self, height=80, font=("나눔고딕", 12))
        self.path_display.pack(pady=10, padx=20, fill="x")
        self.path_display.insert("0.0", "선택된 파일이나 폴더가 없습니다.")

        # 5. 실행 버튼
        self.btn_run = ctk.CTkButton(
            self,
            text="🚀 이미지 추출 시작",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("나눔고딕", 16, "bold"),
            command=self.run_extraction,
        )
        self.btn_run.pack(pady=20)

        # 6. 상태 로그창
        self.log_box = ctk.CTkTextbox(self, height=180, font=("나눔고딕", 12), fg_color="#2c3e50", text_color="white")
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)

        self.selected_items = []
        self.mode = ""  # "file" 또는 "folder"

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("한글 문서", "*.hwp *.hwpx")])
        if files:
            self.selected_items = list(files)
            self.mode = "file"
            self.update_display()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_items = [folder]
            self.mode = "folder"
            self.update_display()

    def update_display(self):
        self.path_display.delete("1.0", "end")
        text = "\n".join(self.selected_items)
        self.path_display.insert("0.0", text)

    def write_log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.update()

    def reset_all(self):
        self.selected_items = []
        self.mode = ""
        self.path_display.delete("1.0", "end")
        self.path_display.insert("0.0", "선택된 파일이나 폴더가 없습니다.")
        self.log_box.delete("1.0", "end")
        self.write_log("🧹 모든 설정이 초기화되었습니다.")

    def run_extraction(self):
        if not self.selected_items:
            self.write_log("⚠️ 먼저 파일이나 폴더를 선택해주세요!")
            return

        self.log_box.delete("1.0", "end")
        self.write_log("📂 작업을 시작합니다...")

        try:
            first_item = os.path.abspath(self.selected_items[0])

            # 저장 기준 위치 결정
            if self.save_at_exe.get():
                if getattr(sys, "frozen", False):
                    base_path = os.path.dirname(sys.executable)
                else:
                    base_path = os.path.dirname(os.path.abspath(__file__))
            else:
                base_path = os.path.dirname(first_item)

            if self.mode == "folder":
                # 폴더 선택 시: [폴더명]_이미지
                folder_name = os.path.basename(first_item)
                main_output_dir = os.path.join(base_path, f"{folder_name}_이미지")
                self.write_log(f"📍 저장 위치: {main_output_dir}")
                self.process_custom_folder(first_item, main_output_dir)

            else:
                if len(self.selected_items) == 1:
                    # 파일 1개 선택 시: [파일명]_이미지 (이중 폴더 방지)
                    name_only = os.path.splitext(os.path.basename(first_item))[0]
                    main_output_dir = os.path.join(base_path, f"{name_only}_이미지")
                    os.makedirs(main_output_dir, exist_ok=True)
                    self.write_log(f"📍 저장 위치: {main_output_dir}")
                    self.extract_to_fixed_dir(first_item, main_output_dir)
                else:
                    # 파일 여러 개 선택 시: 선택파일_이미지
                    main_output_dir = os.path.join(base_path, "선택파일_이미지")
                    self.write_log(f"📍 저장 위치: {main_output_dir}")
                    for file_path in self.selected_items:
                        self.extract_single_file(file_path, main_output_dir)

            self.write_log("\n✨ 모든 작업이 완료되었습니다!")
        except Exception as e:
            self.write_log(f"❌ 에러 발생: {e}")

    def extract_to_fixed_dir(self, file_path, target_dir):
        """지정된 폴더에 직접 이미지 추출 (이중 폴더 방지용)"""
        file_name = os.path.basename(file_path)
        ext = file_name.split(".")[-1].lower()
        self.write_log(f"📄 [{file_name}] 추출 중...")

        if ext == "hwp":
            res = extract_images_from_hwp(file_path, target_dir)
        else:
            res = extract_images_from_hwpx(file_path, target_dir)
        self.write_log(f"   ㄴ 완료! ({len(res)}개 저장)")

    def extract_single_file(self, file_path, parent_output_dir):
        """상위 폴더 내에 파일명 폴더를 만들고 추출"""
        file_name = os.path.basename(file_path)
        name_only = os.path.splitext(file_name)[0]
        target_dir = os.path.join(parent_output_dir, name_only)
        os.makedirs(target_dir, exist_ok=True)
        self.extract_to_fixed_dir(file_path, target_dir)

    def process_custom_folder(self, input_dir, output_dir):
        """폴더 내 한글 파일들 스캔 및 추출"""
        files = glob.glob(os.path.join(input_dir, "*.hwp")) + glob.glob(os.path.join(input_dir, "*.hwpx"))

        if not files:
            self.write_log("❓ 폴더 내에 한글 파일이 없습니다.")
            return

        for file_path in files:
            self.extract_single_file(file_path, output_dir)


if __name__ == "__main__":
    app = App()
    app.mainloop()
