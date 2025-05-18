import os
import re
from collections import Counter
from utils import read_csv, read_json, read_txt
from report_utils import save_report_csv, save_report_docx, save_report_pdf, save_report_xlsx

import re
from collections import Counter

def analyze_text(filename, text):
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    avg_word_len = sum(len(w) for w in words) / total_words if total_words else 0

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences)
    avg_sentence_len = total_words / sentence_count if sentence_count else 0

    char_count = len(text)
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)

    filtered = [w for w in words if len(w) > 1 and w.isalpha()]
    if filtered:
        longest_word = max(filtered, key=len)
        shortest_word = min(filtered, key=len)
        longest_len = len(longest_word)
        shortest_len = len(shortest_word)
    else:
        longest_word = ''
        shortest_word = ''
        longest_len = 0
        shortest_len = 0

    return {
        'filename': filename,
        'total_words': total_words,
        'unique_words': unique_words,
        'avg_word_len': avg_word_len,
        'sentence_count': sentence_count,
        'avg_sentence_len': avg_sentence_len,
        'char_count': char_count,
        'longest_word': longest_word,
        'longest_len': longest_len,
        'shortest_word': shortest_word,
        'shortest_len': shortest_len,
        'top_words': top_words
    }



def main():
    base = 'input_data'
    paths = []
    for fmt in ('csv', 'json', 'txt'):
        folder = os.path.join(base, fmt)
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if f == '.gitkeep':
                    continue
                paths.append(os.path.join(folder, f))

    if not paths:
        print("Nie znaleziono plików do analizy.")
        return

    analysis_results = []
    for path in paths:
        print(f"Przetwarzam: {path}")
        if path.endswith('.csv'):
            text = read_csv(path)
        elif path.endswith('.json'):
            text = read_json(path)
        elif path.endswith('.txt'):
            text = read_txt(path)
        else:
            continue
        filename = os.path.basename(path)
        analysis_results.append(analyze_text(filename, text))

    # Tworzymy folder exports jeśli nie ma
    os.makedirs('exports', exist_ok=True)

    save_report_csv(os.path.join('exports', 'raport.csv'), analysis_results)
    save_report_docx(os.path.join('exports', 'raport.docx'), analysis_results)
    save_report_pdf(os.path.join('exports', 'raport.pdf'), analysis_results)
    save_report_xlsx(os.path.join('exports', 'raport.xlsx'), analysis_results)
    print("Raporty zapisane w folderze 'exports': raport.csv, raport.docx, raport.pdf, raport.xlsx")

if __name__ == "__main__":
    main()
