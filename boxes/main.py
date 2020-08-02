import os
import csv
import argparse

from boxes.utils.files import FileInfo
from boxes.utils import images


def get_files(dirname):
    files = []
    for path in os.listdir(dirname):
        if os.path.isfile(path):
            files.append(os.path.join(dirname, path))
        elif os.path.isdir(path):
            files.extend(get_files(path))
    return files


def classify_files(files):
    for file_path in files:
        fileinfo = FileInfo(file_path)
        try:
            images.image(file_path)
        except TypeError:
            data = {"type": ""}
        else:
            data = {"type": "image"}
        data.update(fileinfo.data)
        yield data


def write(csv_file_path, files):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['type', 'hash', 'size', "birth_time", "name", "file_path"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in files:
            writer.writerow(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", help="files source dir")
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    source_dir = args.source_dir
    files = get_files(source_dir)
    classified = classify_files(files)
    write(args.csvfile, classified)


