import json
import logging
import os
import glob2
import shutil
import hashlib
import argparse
from collections import defaultdict

from trclab_ich.utils import Tzip
from trclab_ich.utils import TLogger

RESOURCES_DIR = os.path.abspath(os.path.join(__file__, os.pardir))

DATASET_INFO_MAP = {
    "name": {
        "#Non-progression case": "Non-progression",
        "Probably Non-progression- 46 cases": "Probably_Non-progression",
        "Probably progression-37 cases": "Probably_progression",
        "Progression case": "Progression",
        "Validation DICOM-44 cases": "Validation_DICOM",
        "Validation Mask-44 cases": "Validation_Mask",
    },
    "kind": {
        "Baseline CT": "baseline",
        "Follow-up CT": "followup",
    },
    "type": {
        "#Non-progression case": "type1",
        "Progression case": "type1",
        "Probably Non-progression- 46 cases": "type2",
        "Probably progression-37 cases": "type2",
        "Validation DICOM-44 cases": "type3",
        "Validation Mask-44 cases": "type3",
    }
}

V2_DATASET_EXCEPTION = {
    "Case 246-1271.tif": "Case 246-127-1.tif"
}


def check_dataset_exception(exception_map: dict, basename: str) -> bool:
    if basename in exception_map.keys():
        Logger.warning(f"Find Dataset Exception. '{basename}'")
        return True
    return False


def ich_dataset_type_1(folder_path, indent=None):
    image_kind = ["Baseline CT", "Follow-up CT"]
    for kind in image_kind:
        Logger.info(f"Start process {kind}")
        json_data = defaultdict(dict)
        json_data["name"] = DATASET_INFO_MAP["name"][os.path.basename(folder_path)]
        images = glob2.glob(os.path.join(folder_path, f"{kind}/**/*.tif"))
        kind_name = DATASET_INFO_MAP["kind"][kind]
        for image in images:
            basename = os.path.basename(image)
            if check_dataset_exception(V2_DATASET_EXCEPTION, basename):
                Logger.info(f"Fix Dataset Exception. '{basename}' => {V2_DATASET_EXCEPTION[basename]}")
                basename = new_filename = V2_DATASET_EXCEPTION[basename]
                new_filepath = os.path.abspath(os.path.join(image, os.pardir, new_filename))
                os.rename(image, new_filepath)
                image = new_filepath

            tags = basename[5:-4].split("-")
            case_id = tags[0]
            segment_id = tags[1]
            is_ivh = "V" in tags[2] or "v" in tags[2]

            if case_id not in json_data[kind_name].keys():
                json_data[kind_name][case_id] = {}
            if segment_id not in json_data[kind_name][case_id].keys():
                json_data[kind_name][case_id][segment_id] = []

            json_data[kind_name][case_id][segment_id] += [{"is_ivh": is_ivh, "filepath": image.replace("\\", "/")}]

        sha1 = hashlib.sha1()
        sha1.update(json.dumps(json_data[kind_name]).encode('utf-8'))
        # noinspection PyTypeChecker
        json_data["sha1"] = str(sha1.hexdigest())

        output_filename = f"{DATASET_INFO_MAP['name'][os.path.basename(folder_path)]}-{kind_name}.json"
        with open(os.path.join(folder_path, output_filename), "w") as json_file:
            json.dump(json_data, json_file, indent=indent)
            Logger.info(f"Json '{output_filename}' generated.")


def ich_dataset_v2(dataset_folder):
    folders = [os.path.join(dataset_folder, folder)
               for folder in os.listdir(dataset_folder)
               if os.path.isdir(os.path.join(dataset_folder, folder))]
    for folder in folders:
        Logger.info(
            f"Generate '{folder}' json file with '{DATASET_INFO_MAP['type'][os.path.basename(folder)]}' parser!")
        if DATASET_INFO_MAP["type"][os.path.basename(folder)] == "type1":
            ich_dataset_type_1(folder, indent=2)


def is_folder_exists(folder_path: os.path, ignore_exists: bool = False) -> bool:
    Logger.info(f"Check if folder '{folder_path}' exists.")
    if os.path.exists(folder_path) and not ignore_exists:
        Logger.info(f"Folder '{folder_path}' does exists.")
        return True

    Logger.info(f"Folder '{folder_path}' doesn't exists!")
    return False


def parser() -> argparse:
    _parser = argparse.ArgumentParser(prog="ICH_Dataset.py", description="ICH Dataset Processor")
    _parser.add_argument("--version", "-v",
                         type=str,
                         choices=["v2"],
                         required=True,
                         help="ICH Dataset Version")

    _parser.add_argument("filename",
                         type=str,
                         help="ICH Dataset Zip Path")

    return _parser


def main():
    args = parser().parse_args()
    ich_parser_version = args.version
    dataset_folder = f"ICH-Dataset-{ich_parser_version}"
    zip_filepath = os.path.join(RESOURCES_DIR, args.filename)
    dataset_path = os.path.join(RESOURCES_DIR, dataset_folder)

    if not is_folder_exists(dataset_folder):
        shutil.rmtree(zip_filepath, ignore_errors=True)
        Tzip.unzip(zip_filepath, dataset_folder)

    if ich_parser_version == "v2":
        Logger.info(f"Start ICH Dataset Parser v2")
        ich_dataset_v2(dataset_path)


if __name__ == '__main__':
    Logger = TLogger.get_logger()
    main()
