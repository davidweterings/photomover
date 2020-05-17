import argparse
import logging
import os
import sys
import shutil
from glob import iglob
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_target_directory(directory: str) -> str:
    """
    Format should be: Artikelnummer-inkoopordernummer-batchnummer-datum/tijd
    So the second entry is always the purchase order number
    """
    return directory.split("-")[1]


def is_valid_directory(directory: str) -> bool:
    return "-" in directory


def find_directory(target_directory: str, start_directory: str) -> Optional[str]:
    logging.info("Looking for target directory: %s", target_directory)
    for root, dirs, files in os.walk(start_directory):
        if target_directory in dirs:
            logging.info("Found directory %s in %s", target_directory, root)
            return f"{root}/{target_directory}"

    return None


def move_photos(source_dir: str, search_dir: str):
    dirs_to_copy = [d for d in iglob(f"{source_dir}/*") if os.path.isdir(d)]

    logging.info("Found dirs: %s", dirs_to_copy)

    for directory in dirs_to_copy:
        if not is_valid_directory(directory):
            logging.info("Skipping directory %s", directory)
            continue

        target_directory = find_directory(get_target_directory(directory), search_dir)

        if target_directory:
            full_target_path = os.path.join(target_directory, "Warehouse", os.path.basename(directory))
            Path(full_target_path).mkdir(parents=True, exist_ok=True)
            shutil.move(directory, full_target_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_dir",
        type=dir_path,
        help="Directory to find photos/files in",
    )
    parser.add_argument(
        "search_dir",
        type=dir_path,
        help="Directory to search in recursively",
    )
    args = parser.parse_args()
    move_photos(args.source_dir, args.search_dir)
