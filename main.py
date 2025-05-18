import os
from collections import Counter
from utils import read_txt, read_csv, read_json, count_words

def analyze_text(text):
    word_counts = count_words(text)
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    avg_word_len = sum(len(word) * count for word, count in word_counts.items()) / total_words if total_words else 0

    print(f"Liczba wszystkich słów: {total_words}")
    print(f"Liczba unikalnych słów: {unique_words}")
    print(f"Średnia długość słowa: {avg_word_len:.2f}")

    print("\nTop 10 najczęstszych słów:")
    for word, count in word_counts.most_common(10):
        print(f"{word}: {count}")

def process_folder(folder_path, read_func):
    files = [f for f in os.listdir(folder_path) if f != '.gitkeep'] if os.path.exists(folder_path) else []
    if not files:
        return False
    for file in files:
        file_path = os.path.join(folder_path, file)
        print(f"\nAnaliza pliku: {file_path}")
        text = read_func(file_path)
        analyze_text(text)
    return True

def main():
    base_path = 'input_data'

    csv_processed = process_folder(os.path.join(base_path, 'csv'), read_csv)
    json_processed = process_folder(os.path.join(base_path, 'json'), read_json)
    txt_processed = process_folder(os.path.join(base_path, 'txt'), read_txt)

    if not (csv_processed or json_processed or txt_processed):
        print("Nie znaleziono plików do analizy.")

if __name__ == "__main__":
    main()
