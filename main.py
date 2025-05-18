import os
from utils import read_csv, read_json, read_txt
from analysis_utils import analyze_text

from report_utils import (
    save_report_csv,
    save_report_docx,
    save_report_pdf,
    save_report_xlsx
)
from viz_utils import (
    create_summary_table,
    plot_comparison_metrics,
    plot_comparison_top3
)



def main():
    # zbieramy ścieżki
    base = "input_data"
    paths = []
    for fmt in ("csv","json","txt"):
        folder = os.path.join(base, fmt)
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if not f.startswith("."):
                    paths.append(os.path.join(folder, f))
    if not paths:
        print("Brak plików do analizy.")
        return

    # analiza wszystkich plików
    analysis = []
    for p in paths:
        print("Przetwarzam:", p)
        if p.endswith(".csv"):
            txt = read_csv(p)
        elif p.endswith(".json"):
            txt = read_json(p)
        else:
            txt = read_txt(p)
        fname = os.path.basename(p)
        res = analyze_text(fname, txt)
        analysis.append(res)

    # raporty w exports/raports
    raports_dir = os.path.join("exports", "raports")
    os.makedirs(raports_dir, exist_ok=True)
    save_report_csv(os.path.join(raports_dir, "raport.csv"), analysis)
    save_report_docx(os.path.join(raports_dir, "raport.docx"), analysis)
    save_report_pdf(os.path.join(raports_dir, "raport.pdf"), analysis)
    save_report_xlsx(os.path.join(raports_dir, "raport.xlsx"), analysis)
    print("Raporty w exports/raports gotowe.")

    # pojedyncze analizy PNG w exports/single_file_analysis
    single = os.path.join("exports", "single_file_analysis")
    os.makedirs(single, exist_ok=True)
    for r in analysis:
        name, ext = os.path.splitext(r["filename"])
        ext = ext.lstrip(".")
        folder = os.path.join(single, f"{name}_{ext}")
        os.makedirs(folder, exist_ok=True)
        # teraz pasuje do wiz_utils signature:
        create_summary_table(r, folder)
    print("Pojedyńcza analiza plików gototwa w exports/single_file_analysis.")

    # porównawcze wykresy w exports/plots/comparison
    comp_dir = os.path.join("exports", "plots", "comparison")
    os.makedirs(comp_dir, exist_ok=True)
    plot_comparison_metrics(analysis, comp_dir)
    plot_comparison_top3(analysis, comp_dir)
    print("Wykresy porównawcze gotowe w exports/plots/comparison.")

    print("Analiza zakończona.")

if __name__ == "__main__":
    main()
