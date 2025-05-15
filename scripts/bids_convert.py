import os
import glob
import argparse
import warnings
import subprocess
from tqdm import tqdm

def is_functional_modality(path):
    name = os.path.basename(path).lower()
    return any(key in name for key in ["rsfmri", "rest", "bold", "task", "eyes_open", "fcfmri"])

def is_anatomical_modality(path):
    name = os.path.basename(path).lower()
    return any(key in name for key in ["mprage", "t1", "anat", "fspgr", "sag", "mp-rage"])

def find_deepest_dicom_dirs(subject_path):
    anat_dir, func_dir = None, None
    for subfolder in os.listdir(subject_path):
        full_path = os.path.join(subject_path, subfolder)
        if not os.path.isdir(full_path):
            continue

        if is_anatomical_modality(subfolder):
            anat_dir = full_path
        elif is_functional_modality(subfolder):
            func_dir = full_path

    return anat_dir, func_dir

def run_dcm2niix(dicom_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        ["dcm2niix", "-z", "y", "-i", "y", "-m", "n", "-o", output_dir, dicom_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)

def convert_dicom_to_nifti(data_root):
    print(f"\n📁 資料根目錄：{data_root}")
    nifti_root = os.path.join(data_root, "Nifti")
    os.makedirs(nifti_root, exist_ok=True)

    subject_dirs = sorted([
        d for d in os.listdir(data_root)
        if os.path.isdir(os.path.join(data_root, d)) and d.lower() != "nifti"
    ])
    print(f"🔎 找到 {len(subject_dirs)} 個 subject 資料夾：{subject_dirs}\n")

    for subject in tqdm(subject_dirs, desc="🚀 開始轉換 DICOM → NIfTI"):
        subject_id = subject
        subject_path = os.path.join(data_root, subject)
        print(f"\n=== 處理 subject {subject}（轉成 sub-{subject_id}） ===")

        anat_dir, func_dir = find_deepest_dicom_dirs(subject_path)

        subject_nifti_anat = os.path.join(nifti_root, f"sub-{subject_id}", "anat")
        subject_nifti_func = os.path.join(nifti_root, f"sub-{subject_id}", "func")
        os.makedirs(subject_nifti_anat, exist_ok=True)
        os.makedirs(subject_nifti_func, exist_ok=True)

        if anat_dir:
            print(f"🧠 Anatomical DICOM 來源：{anat_dir}")
            try:
                run_dcm2niix(anat_dir, subject_nifti_anat)
                anat_file = glob.glob(os.path.join(subject_nifti_anat, "*.nii.gz"))[0]
                new_anat_name = os.path.join(subject_nifti_anat, f"sub-{subject_id}_T1w.nii.gz")
                os.rename(anat_file, new_anat_name)
                print(f"✅ Anatomical 轉換完成：{new_anat_name}")
            except Exception as e:
                print(f"❌ Anatomical 轉換失敗：{e}")
        else:
            print("⚠️ 沒有找到 anatomical DICOM")

        if func_dir:
            print(f"🧠 Functional DICOM 來源：{func_dir}")
            try:
                run_dcm2niix(func_dir, subject_nifti_func)
                func_file = glob.glob(os.path.join(subject_nifti_func, "*.nii.gz"))[0]
                new_func_name = os.path.join(subject_nifti_func, f"sub-{subject_id}_task-rest_bold.nii.gz")
                os.rename(func_file, new_func_name)
                print(f"✅ Functional 轉換完成：{new_func_name}")
            except Exception as e:
                print(f"❌ Functional 轉換失敗：{e}")
        else:
            print("⚠️ 沒有找到 functional DICOM")

def main():
    parser = argparse.ArgumentParser(description="🧪 BIDS DICOM → NIfTI converter（dcm2niix 版）")
    parser.add_argument("--data_root", type=str, required=True, help="資料根目錄（應直接包含 subject 資料夾）")
    args = parser.parse_args()
    warnings.filterwarnings("ignore", category=UserWarning)
    convert_dicom_to_nifti(args.data_root)

if __name__ == "__main__":
    main()

