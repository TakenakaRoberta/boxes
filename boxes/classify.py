import os
import csv
import argparse
from datetime import datetime
from PIL import Image

from utils.files import FileInfo


def get_files(path):
    if os.path.isfile(path):
        return [path]

    dirname = path
    files = []
    for path in os.listdir(dirname):
        fullpath = os.path.join(dirname, path)
        if os.path.isfile(fullpath):
            files.append(fullpath)
        elif os.path.isdir(fullpath):
            files.extend(get_files(fullpath))
    return files


def classify_files(files):
    for file_path in files:
        fileinfo = FileInfo(file_path)
        data = {"type": ""}
        try:
            Image.open(file_path)
        except Exception as e:
            ign, ext = os.path.splitext(file_path)
            if ext.startswith(".mp"):
                data = {"type": "video"}
        else:
            data = {"type": "image"}
        
        data.update(get_data(fileinfo))
        yield data


def isoformat(time):
    return datetime.fromtimestamp(time).isoformat()[:10]


def get_data(fileinfo):
    return {
        "file_path": fileinfo.file_path,
        "size": fileinfo.size,
        "first_time": fileinfo.first_time,
        "first_date": isoformat(fileinfo.first_time),
        "birth_date": isoformat(fileinfo.birth_time),
        "c_date": isoformat(fileinfo.c_time),
        "recent_access_date": isoformat(fileinfo.recent_access_time),
        "modification_date": isoformat(fileinfo.modification_time),
        "hash": fileinfo.hash,
        "name": fileinfo.basename,
    }


def write(csv_file_path, file_info_items):
    fieldnames = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  ]
    path = os.path.dirname(csv_file_path)
    if not os.path.isdir(path):
        os.makedirs(path)
    img_csv_file_path = csv_file_path.replace(".csv", ".img.csv")
    vid_csv_file_path = csv_file_path.replace(".csv", ".vid.csv")
    oth_csv_file_path = csv_file_path.replace(".csv", ".other.csv")

    with open(oth_csv_file_path, 'w', newline='') as oth_csvfile:
        with open(vid_csv_file_path, 'w', newline='') as vid_csvfile:
            with open(img_csv_file_path, 'w', newline='') as img_csvfile:
                vid_writer = csv.DictWriter(vid_csvfile, fieldnames=fieldnames)
                img_writer = csv.DictWriter(img_csvfile, fieldnames=fieldnames)
                oth_writer = csv.DictWriter(oth_csvfile, fieldnames=fieldnames)
                vid_writer.writeheader()
                img_writer.writeheader()
                oth_writer.writeheader()
                for file_info in file_info_items:
                    if file_info.get("type") == "image":
                        img_writer.writerow(file_info)
                    elif file_info.get("type") == "video":
                        vid_writer.writerow(file_info)
                    else:
                        oth_writer.writerow(file_info)


def main():
    parser = argparse.ArgumentParser(
        'Classifica arquivos de uma dada pasta em imagens, vídeo e outros, '
        'e gera um arquivo csv para cada tipo de arquivo com os dados de seus arquivos')
    parser.add_argument("source_dir", help="files source dir")
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    source_dir = args.source_dir
    csvfile = args.csvfile

    if not os.path.isdir(source_dir):
        raise IOError("Pasta não encontrada: %s", source_dir)

    files = get_files(source_dir)
    classified = classify_files(files)
    write(csvfile, classified)


if __name__ == '__main__':
    main()
