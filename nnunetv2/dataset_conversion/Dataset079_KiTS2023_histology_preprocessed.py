from batchgenerators.utilities.file_and_folder_operations import *
import shutil
from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw


def convert_kits2023(kits_base_dir: str, nnunet_dataset_id: int = 220):
    task_name = "KiTS2023_histology_preprocessed"

    foldername = "Dataset%03.0d_%s" % (nnunet_dataset_id, task_name)


    # setting up nnU-Net folders
    out_base = join(nnUNet_raw, foldername)
    imagestr = join(out_base, "imagesTr")
    labelstr = join(out_base, "labelsTr")
    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(labelstr)

    cases = subdirs(kits_base_dir, prefix='case_', join=False)
    for tr in cases:
        shutil.copy(join(kits_base_dir, tr, 'imaging.nii.gz'), join(imagestr, f'{tr}_0000.nii.gz'))
        shutil.copy(join(kits_base_dir, tr, 'segmentation.nii.gz'), join(labelstr, f'{tr}.nii.gz'))

    print(f"Generating dataset {task_name} with {len(cases)} training cases...")

    generate_dataset_json(out_base, {0: "CT"},
                          labels={
                            "background": 0,
                            "kidney": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
                            "masses": (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17),
                            "tumor": (2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17),
                            "angiomyolipoma": 4,
                            "chromophobe": 5,
                            "clear_cell_papillary_rcc": 6,
                            "clear_cell_rcc": 7,
                            "collecting_duct_undefined": 8,
                            "mest": 9,
                            "multilocular_cystic_rcc": 10,
                            "oncocytoma": 11,
                            "other": 12,
                            "papillary": 13,
                            "rcc_unclassified": 14,
                            "spindle_cell_neoplasm": 15,
                            "urothelial": 16,
                            "wilms": 17
                          },
                          regions_class_order=(1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
                          num_training_cases=len(cases), file_ending='.nii.gz',
                          dataset_name=task_name, reference='none',
                          release='0.1.3',
                          overwrite_image_reader_writer='NibabelIOWithReorient',
                          description="KiTS2023")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str,
                        help="The downloaded and extracted KiTS2023 dataset (must have case_XXXXX subfolders)")
    parser.add_argument('-d', required=False, type=int, default=79, help='nnU-Net with histology preprocessed dataset ID, default: 079')
    args = parser.parse_args()
    amos_base = args.input_folder
    convert_kits2023(amos_base, args.d)

    # dataset/

