import os
import glob
import argparse
import warnings
import dicom2nifti
from tqdm import tqdm

def convert_dicom_to_nifti(data_root):
    dicom_root = os.path.join(data_root, "dicom")
    anat_root = os.path.join(dicom_root, "anat")
    func_root = os.path.join(dicom_root, "func")
    nifti_root = os.path.join(data_root, "Nifti")

    subjects = sorted([
        d for d in os.listdir(anat_root)
        if os.path.isdir(os.path.join(anat_root, d))
    ])

    print(f"Found {len(subjects)} subjects.")

    # Ensure nifti_root exists
    os.makedirs(nifti_root, exist_ok=True)

    for subject in tqdm(subjects, desc="Processing subjects"):
        subject_anat_dicom = os.path.join(anat_root, subject)
        subject_func_dicom = os.path.join(func_root, subject)

        subject_nifti_anat = os.path.join(nifti_root, subject, "anat")
        subject_nifti_func = os.path.join(nifti_root, subject, "func")

        os.makedirs(subject_nifti_anat, exist_ok=True)
        os.makedirs(subject_nifti_func, exist_ok=True)

        # Convert anatomical DICOM to NIfTI
        try:
            dicom2nifti.convert_directory(subject_anat_dicom, subject_nifti_anat, compression=True, reorient=True)
            anat_nii = glob.glob(os.path.join(subject_nifti_anat, '*.nii.gz'))[0]
            new_anat_name = os.path.join(subject_nifti_anat, f"sub-{subject}_ses-001_T1w.nii.gz")
            os.rename(anat_nii, new_anat_name)
            print(f"Anatomical conversion done for {subject}: {new_anat_name}")
        except Exception as e:
            print(f"Anatomical conversion failed for {subject}: {e}")

        # Convert functional DICOM to NIfTI
        try:
            dicom2nifti.convert_directory(subject_func_dicom, subject_nifti_func, compression=True, reorient=True)
            func_nii = glob.glob(os.path.join(subject_nifti_func, '*.nii.gz'))[0]
            new_func_name = os.path.join(subject_nifti_func, f"sub-{subject}_ses-001_task-rest_bold.nii.gz")
            os.rename(func_nii, new_func_name)
            print(f"Functional conversion done for {subject}: {new_func_name}")
        except Exception as e:
            print(f"Functional conversion failed for {subject}: {e}")

def main(args):
    # Suppress all pydicom warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="pydicom")
    convert_dicom_to_nifti(args.data_root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DICOM to NIfTI Conversion Pipeline")
    parser.add_argument("--data_root", type=str, required=True, help="Root path containing dicom/anat/ and dicom/func/ folders")
    args = parser.parse_args()

    main(args)

