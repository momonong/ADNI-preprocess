import pandas as pd

df_ref = pd.read_excel("docs/fMRI_matched_20240624_afterchecked_final.xlsx", sheet_name="AD")
df_data = pd.read_excel("docs/AD_Phillips.xlsx")

mask = df_data["Group"].str.contains("Patient")
df_data = df_data[~mask]

sucjects = ""
subject_count = 0
exceptions = ["019_S_4477", "019_S_5019", "130_S_4589", "130_S_5231"]

for subj in df_data["Subject"]:
    if subj not in df_ref["Subject"].values or subj in exceptions:
        sucjects += f"{subj},"
        subject_count += 1
        print(f"{subj}: ✅")
    else:
        print(f"{subj}: ❌")
print("========================================")
print("lenth of the subjects:", subject_count)
print(sucjects[:-1])
