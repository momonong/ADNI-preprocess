import os
import pandas as pd
from collections import Counter

# === 參數設定 ===
FILE_DATE = "20250507"

# === 路徑設定 ===
csv_subjects_path = os.path.join("meta", f"{FILE_DATE}.csv")
xlsx_reference_path = os.path.join("docs", "matching_data.xlsx")

# === 讀取資料 ===
df_csv = pd.read_csv(csv_subjects_path)
df_xlsx = pd.read_excel(xlsx_reference_path)

csv_subjects = df_csv["Subject"].dropna().astype(str).tolist()
xlsx_subjects = set(df_xlsx["Subject"].dropna().astype(str).tolist())

# === 統計比對 ===
found_in_xlsx = []
not_found_in_xlsx = []

for subj in csv_subjects:
    if subj in xlsx_subjects:
        found_in_xlsx.append(subj)
    else:
        not_found_in_xlsx.append(subj)

# === 整理重複計數 ===
def summarize_counts(lst):
    counter = Counter(lst)
    return sorted(counter.items())

def print_summary(label, items):
    print(f"{label} ({len(items)} unique, {sum(count for _, count in items)} total):")
    print("Summary:")
    for subj, count in items:
        print(f"  {subj}: {count}")
    print("CSV:")
    print(",".join([s for s, _ in items]))
    print("\n")

print_summary("✅ Found in Excel", summarize_counts(found_in_xlsx))
print_summary("❌ Not in Excel", summarize_counts(not_found_in_xlsx))
