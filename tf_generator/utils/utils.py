import os
import zipfile
import tarfile
from typing import Tuple, List


def extract_folder(file_name: str, target: str):
    if os.path.exists(file_name):
        if file_name.endswith("tar.gz"):
            extract_tar_folder(file_name, "r:gz", target)
        elif file_name.endswith("tar"):
            extract_tar_folder(file_name, "r:", target)
        elif file_name.endswith("zip"):
            extract_zip_folder(file_name, target)
        else:
            raise Exception("Not in preferred valid format list!!!")
    else:
        raise Exception("File not found!!!")


def extract_zip_folder(path_to_zip_file: str, target: str):
    if os.path.exists(path_to_zip_file):
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target)
    else:
        raise Exception("File not found!!!")

def extract_tar_folder(file_name: str, file_type: str, target: str):
    tar = tarfile.open(file_name, file_type)
    tar.extractall(target)
    tar.close()

def get_files_and_folders_recursively(directory: str) -> Tuple[List[str], List[str]]:
    subfolders, files = [], []

    for folders_or_files in os.scandir(directory):
        if folders_or_files.is_dir():
            subfolders.append(folders_or_files.path)
        if folders_or_files.is_file():
            files.append(folders_or_files.path)


    for dir in list(subfolders):
        sf, folders_or_files = get_files_and_folders_recursively(dir)
        subfolders.extend(sf)
        files.extend(folders_or_files)
    return subfolders, files

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))

def zip_folder(file_name: str, target_path: str):
    print("Zip the folder", target_path)
    with zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        zipdir(target_path, zip_f)
    print("Completed zipping successfully.")
