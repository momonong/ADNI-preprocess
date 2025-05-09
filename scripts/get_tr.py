import nibabel as nib

path_to_func_file = "/Volumes/KIOXIA/data/0509_philips/ADNI/Nifti/sub-01/func/sub-01_ses-001_task-rest_bold.nii.gz"  # 替換為你的功能性影像檔案路徑

img = nib.load(path_to_func_file)
tr = img.header.get_zooms()[3]  # 第四維是時間間隔，即 TR
print(f"TR = {tr} 秒")
