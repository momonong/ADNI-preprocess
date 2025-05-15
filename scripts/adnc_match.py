import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment

def match_with_hungarian(df_ad, df_cn):
    df_ad_unique = df_ad.drop_duplicates(subset="Subject").reset_index(drop=True)
    df_cn_unique = df_cn.drop_duplicates(subset="Subject").reset_index(drop=True)

    results = []

    for sex in df_ad_unique["Sex"].unique():
        ad_group = df_ad_unique[df_ad_unique["Sex"] == sex].reset_index(drop=True)
        cn_group = df_cn_unique[df_cn_unique["Sex"] == sex].reset_index(drop=True)

        if len(cn_group) == 0:
            print(f"⚠️ 沒有符合性別 {sex} 的 CN 資料，跳過")
            continue

        if len(cn_group) < len(ad_group):
            print(f"⚠️ CN 數量不足（性別 {sex}）：{len(cn_group)} 對 {len(ad_group)}，僅配對前 {len(cn_group)} 筆 AD")

        cost_matrix = np.abs(ad_group["Age"].values[:, None] - cn_group["Age"].values[None, :])
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        for i, j in zip(row_ind, col_ind):
            ad_row = ad_group.iloc[i]
            cn_row = cn_group.iloc[j]
            age_diff = abs(ad_row["Age"] - cn_row["Age"])

            print(f"✅ 匈牙利配對：AD {ad_row['Subject']} (Age={ad_row['Age']}, Sex={ad_row['Sex']}) "
                  f"<--> CN {cn_row['Subject']} (Age={cn_row['Age']}, Sex={cn_row['Sex']})")

            results.append({
                "AD_Subject": ad_row["Subject"],
                "AD_Age": ad_row["Age"],
                "AD_Sex": ad_row["Sex"],
                "CN_Subject": cn_row["Subject"],
                "CN_Age": cn_row["Age"],
                "CN_Sex": cn_row["Sex"],
                "Age_Diff": age_diff
            })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df_ad = pd.read_csv("meta/20250515_ge.csv")
    df_cn = pd.read_csv("meta/20250515_ge_cn.csv")

    matched_df = match_with_hungarian(df_ad, df_cn)
    matched_df.to_csv("docs/matched_ad_cn_pairs.csv", index=False)
    print("\n✅ 匈牙利配對結果已儲存為 `matched_ad_cn_pairs.csv`")

