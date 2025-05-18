# Funkcje pomocnicze (wczytywanie danych, liczenie)

import csv
from collections import Counter

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_csv(file_path):
    words = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            words.extend(' '.join(row).lower().split())
    return ' '.join(words)

import json

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Załóżmy, że data to lista słowników z kluczem "text"
    texts = [item.get('text', '') for item in data if isinstance(item, dict)]
    return ' '.join(texts)


def count_words(text):
    words = text.lower().split()
    return Counter(words)
