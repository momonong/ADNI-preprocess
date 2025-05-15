import pandas as pd

df = pd.read_csv("meta/20250515_ge_cn.csv")

count = len(df["Subject"].unique())

print(count)



