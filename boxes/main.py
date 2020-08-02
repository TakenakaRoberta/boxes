import os
import csv
import argparse

from PIL import Image

from utils.files import FileInfo


def get_files(path):
    print(path)
    if os.path.isfile(path):
        return [path]

    dirname = path
    files = []
    for path in os.listdir(dirname):
        fullpath = os.path.join(dirname, path)
        print(fullpath)
        if os.path.isfile(fullpath):
            files.append(fullpath)
        elif os.path.isdir(fullpath):
            files.extend(get_files(fullpath))
    return files


def classify_files(files):
    for file_path in files:
        fileinfo = FileInfo(file_path)
        try:
            Image(file_path)
        except TypeError:
            data = {"type": ""}
        else:
            data = {"type": "image"}
        data.update(fileinfo.data)
        yield data


def write(csv_file_path, files):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['type', 'hash', 'size', "birth_time", "name", "file_path", "dateiso", "time"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in files:
            print(data)
            writer.writerow(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", help="files source dir")
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    source_dir = args.source_dir
    print(source_dir)
    files = get_files(source_dir)
    classified = classify_files(files)
    write(args.csvfile, classified)


if __name__ == '__main__':
    main()
