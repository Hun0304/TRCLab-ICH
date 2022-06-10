import os
import zipfile
from tqdm import tqdm
from trclab_ich.utils import TLogger

Logger = TLogger.get_logger()


def unzip(filepath: os.path, target: os.path):
    Logger.info(f"Unzip {filepath}.")
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting '):
            try:
                zip_ref.extract(member, target)
            except zipfile.error as e:
                pass
    Logger.info(f"Unzip Done.")
