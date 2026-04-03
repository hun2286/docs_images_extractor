import os
from core.processor import process_all_files


def main():
    input_path = os.path.join(os.getcwd(), "input_docs")
    process_all_files(input_path)


if __name__ == "__main__":
    main()
