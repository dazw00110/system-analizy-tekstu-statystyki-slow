import os
from utils import read_txt, read_csv, read_json, count_words

def process_folder(folder_path, read_func):
    files = [f for f in os.listdir(folder_path) if f != '.gitkeep'] if os.path.exists(folder_path) else []
    if not files:
        return False
    for file in files:
        file_path = os.path.join(folder_path, file)
        print(f"\nAnaliza pliku: {file_path}")
        text = read_func(file_path)
        word_counts = count_words(text)
        for word, count in word_counts.most_common(10):  # pokaż top 10
            print(f"{word}: {count}")
    return True

def main():
    base_path = 'input_data'
    any_files_found = False

    if process_folder(os.path.join(base_path, 'csv'), read_csv):
        any_files_found = True
    if process_folder(os.path.join(base_path, 'json'), read_json):
        any_files_found = True
    if process_folder(os.path.join(base_path, 'txt'), read_txt):
        any_files_found = True

    if not any_files_found:
        print("Nie znaleziono plików do analizy.")

if __name__ == "__main__":
    main()
