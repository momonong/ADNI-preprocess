import pandas as pd

df = pd.read_csv("docs/matched_ad_cn_pairs.csv")

subjects = ""
count = 0

for subj in df["CN_Subject"]:
    subjects += f"{subj},"
    count += 1

print(subjects[:-1])
print(count)

