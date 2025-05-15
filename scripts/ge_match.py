import pandas as pd

df_ref = pd.read_excel("docs/metadata_Siemens&GE_20250318.xlsx", sheet_name="編號_AD")
df_data = pd.read_csv("docs/IDA Search May 14 2025.csv")

ref_mask = df_ref["Machine"].str.contains("GE")
df_ref = df_ref[ref_mask]

subjects = ""
subject_count = 0

for subj in df_data["Subject"]:
    if subj not in df_ref["Subject"].values:
        subjects += f"{subj},"
        subject_count += 1

print(subjects[:-1])
print(subject_count)


ge_subjects = ""
ge_subject_count = 0

for subj in df_ref["Subject"]:
    ge_subjects += f"{subj},"
    ge_subject_count += 1

print(ge_subjects[:-1])
print(ge_subject_count)
