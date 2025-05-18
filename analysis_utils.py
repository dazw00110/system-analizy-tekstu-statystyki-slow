import re
from collections import Counter

def analyze_text(filename, text):
    words = [w for w in re.findall(r"\b\w+\b", text.lower()) if w.isalpha()]
    total_words = len(words)
    unique_words = len(set(words))
    avg_word_len = sum(len(w) for w in words) / total_words if total_words else 0

    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)
    avg_sentence_len = total_words / sentence_count if sentence_count else 0

    char_count = len(text)
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)

    longest_word = max(words, key=len) if words else ""
    shortest_word = min(words, key=len) if words else ""

    return {
        "filename": filename,
        "total_words": total_words,
        "unique_words": unique_words,
        "avg_word_len": avg_word_len,
        "sentence_count": sentence_count,
        "avg_sentence_len": avg_sentence_len,
        "char_count": char_count,
        "top_words": top_words,
        "longest_word": longest_word,
        "longest_len": len(longest_word),
        "shortest_word": shortest_word,
        "shortest_len": len(shortest_word),
        "full_text": text,
    }
