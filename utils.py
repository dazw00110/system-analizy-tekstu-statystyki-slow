import csv
import json
import re
from collections import Counter

def read_csv(filepath):
    texts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(' '.join(row.values()))
    return ' '.join(texts)

def read_json(filepath):
    texts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                texts.append(' '.join(str(v) for v in entry.values()))
            else:
                texts.append(str(entry))
    elif isinstance(data, dict):
        texts.append(' '.join(str(v) for v in data.values()))
    else:
        texts.append(str(data))
    return ' '.join(texts)

def read_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)
