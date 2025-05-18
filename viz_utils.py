import os
import matplotlib.pyplot as plt
import pandas as pd

# Stała paleta kolorów (tab10 ma 10 różnych)
COLORS = plt.cm.get_cmap("tab10", 10)

def create_summary_table(res, out_dir):
    """
    Rysuje i zapisuje PNG z tabelką zawierającą:
    - nagłówek z nazwą pliku
    - podstawowe statystyki
    - Top 10 słów
    """
    # 1) Nagłówek
    header = [(f"Plik: {res['filename']}", "")]

    # 2) Podstawowe metryki
    metrics = [
        ("Liczba wszystkich słów", res["total_words"]),
        ("Liczba unikalnych słów", res["unique_words"]),
        ("Średnia długość słowa", f"{res['avg_word_len']:.2f}"),
        ("Liczba zdań", res["sentence_count"]),
        ("Średnia długość zdania", f"{res['avg_sentence_len']:.2f}"),
        ("Liczba znaków", res["char_count"]),
        ("Najdłuższe słowo", res["longest_word"]),
        ("Długość najdłuższego", res["longest_len"]),
        ("Najkrótsze słowo", res["shortest_word"]),
        ("Długość najkrótszego", res["shortest_len"]),
    ]

    # 3) Top 10 słów
    top = [("Top 10 słów", "Liczba")]
    for w, c in res["top_words"]:
        top.append((w, c))

    # Scal wszystkie wiersze w kolejności
    rows = header + [("", "")] + metrics + [("", "")] + top

    # Rysowanie tabeli
    fig, ax = plt.subplots(figsize=(8, len(rows) * 0.35 + 1))
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=["Opis", "Wartość"],
        cellLoc="left",
        loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    plt.tight_layout()

    # Zapis
    fname = os.path.splitext(res["filename"])[0]
    out_path = os.path.join(out_dir, f"{fname}_summary.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_comparison_metrics(results, out_dir):
    """
    Dla każdej z poniższych metryk tworzy wykres słupkowy,
    gdzie każdy plik jest oznaczony innym kolorem z palety COLORS.
    """
    numeric = {
        "total_words":      "Wszystkie słowa",
        "unique_words":     "Unikalne słowa",
        "char_count":       "Znaki",
        "sentence_count":   "Ilość zdań",
        "avg_word_len":     "Śr. dł. słowa",
        "avg_sentence_len": "Śr. dł. zdania",
        "longest_len":      "Długość najdłuższego",
        "shortest_len":     "Długość najkrótszego"
    }

    df = pd.DataFrame([
        {k: r[k] for k in numeric.keys()} | {"plik": r["filename"]}
        for r in results
    ]).set_index("plik")

    for i, (key, label) in enumerate(numeric.items()):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = [COLORS(j % COLORS.N) for j in range(len(df))]
        bars = ax.bar(df.index, df[key], color=colors)
        ax.set_title(f"Porównanie – {label}")
        ax.set_xlabel("Plik")
        ax.set_ylabel(label)
        ax.bar_label(bars, labels=[f"{v}" for v in df[key]], padding=3)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        fig.savefig(os.path.join(out_dir, f"comparison_{key}.png"), dpi=150)
        plt.close(fig)

    # Dodatkowo jeden zbiorczy wykres wszystkich metryk razem
    fig, ax = plt.subplots(figsize=(12, 7))
    df.plot(kind="bar", ax=ax, color=[COLORS(j % COLORS.N) for j in range(len(df))])
    ax.set_title("Porównanie – wszystkie metryki")
    ax.set_xlabel("Plik")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "comparison_all_metrics.png"), dpi=150)
    plt.close(fig)


def plot_comparison_top3(results, out_dir):
    """
    Tworzy obraz z tabelką porównującą top-3 słowa dla każdego pliku.
    """
    rows = []
    for r in results:
        top3 = r["top_words"][:3]
        while len(top3) < 3:
            top3.append(("", 0))
        rows.append([r["filename"], *[item for pair in top3 for item in pair]])

    cols = ["Plik", "Word1", "Count1", "Word2", "Count2", "Word3", "Count3"]
    fig, ax = plt.subplots(figsize=(8, len(rows) * 0.6 + 1))
    ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=cols, loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "comparison_top3_words.png"), dpi=150)
    plt.close(fig)
