import os

def find_nifti_folders_with_json(root_dir):
    print(f"\n📁 檢查根目錄：{root_dir}")
    found, missing = [], []

    for subject in sorted(os.listdir(root_dir)):
        subj_path = os.path.join(root_dir, subject)
        if not os.path.isdir(subj_path):
            continue

        func_dir = os.path.join(subj_path, "func")
        if not os.path.isdir(func_dir):
            continue

        json_found = False
        for f in os.listdir(func_dir):
            if f.endswith(".json"):
                json_found = True
                break

        if json_found:
            found.append(subject)
        else:
            missing.append(subject)

    print(f"\n✅ 有 JSON 的 subject：{len(found)} 個")
    for subj in found:
        print(f"  ✔️ {subj}")

    print(f"\n⚠️ 沒有 JSON 的 subject：{len(missing)} 個")
    for subj in missing:
        print(f"  ❌ {subj}")

if __name__ == "__main__":
    nifti_root = "/Volumes/KIOXIA/data/0515_GE/ADNI/Nifti"  # 替換成你的 NIfTI 資料夾路徑
    find_nifti_folders_with_json(nifti_root)
