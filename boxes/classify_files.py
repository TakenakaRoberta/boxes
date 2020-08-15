import os
import csv
import argparse
import logging
from datetime import datetime
import json

from PIL import Image

from utils.files import FileInfo


logging.basicConfig(level=logging.INFO)


def new_filename(file_path, first_date, new_dirname):
    basename = os.path.basename(file_path)
    return "--".join([first_date, new_dirname, basename])
    

def convert_notalnum_to_under(word):
    normalized = []
    for c in word:
        if c.isalnum():
            normalized.append(c.upper())
            continue
        normalized.append("_")
    return "".join(normalized)


def get_words(normalized_word):
    return [w for w in normalized_word.split("_") if w]


def get_labels(words):
    return [w for w in words if w.isalpha()]


def new_dirname(words):
    return "_".join(words)


def get_files(path):
    if os.path.isfile(path):
        path = os.path.normpath(path)
        logging.info(path)
        return [path]

    files = []
    for _path in os.listdir(path):
        files.extend(get_files(os.path.join(path, _path)))
    return files


def classify_files(files):
    classified = []
    total = len(files)
    for i, file_path in enumerate(files):
        logging.info("Classifying: %i/%i: %s", i, total, file_path)
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
        normalized_file_path = convert_notalnum_to_under(file_path)
        words = get_words(normalized_file_path)
        data['labels'] = get_labels(words)
        data['new_dirname'] = new_dirname(words)
        data['new_filename'] = new_filename(file_path, data.get("first_date"), data['new_dirname'])

        classified.append(data)
    return classified

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
                  "labels", "new_filename", "new_dirname",
                  "main_label",
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
                i = 0
                for file_info in file_info_items:
                    i += 1
                    file_info["main_label"] = file_info["labels"][0]
                    file_info["labels"] = json.dumps(file_info["labels"])

                    if file_info.get("type") == "image":
                        img_writer.writerow(file_info)
                    elif file_info.get("type") == "video":
                        vid_writer.writerow(file_info)
                    else:
                        oth_writer.writerow(file_info)
                    if i % 100 == 0:
                        logging.info("Created %i items in CSV", i)
                logging.info("Created %i items in CSV", i)
    return labels


def sorted_by_higher_score(names, scores):
    items = [
        (scores[name], name)
        for name in names
    ]
    labels = [item[1] for item in sorted(items, reverse=True)]
    if len(labels) > 1:
        labels.remove("PHOTO")
    return labels


def file_labels(file_info_items):
    labels = {}
    for file_info in file_info_items:
        for label in file_info.get("labels"):
            labels[label] = labels.get(label, 0)
            labels[label] += 1

    for file_info in file_info_items:
        file_info["labels"] = sorted_by_higher_score(file_info["labels"])
    return labels


def write_labels(file_path, labels):
    sorted_labels = sorted([(n, k) for k, n in labels.items()], reverse=True)
    with open(file_path, "w") as fp:
        fp.write(
            "\n".join([
                    "{},{}".format(k, n)
                    for n, k in sorted_labels
                ]))
    logging.info("Created %s", file_path)
                

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

    path = os.path.dirname(csvfile)
    if not os.path.isdir(path):
        os.makedirs(path)

    files = get_files(source_dir)
    classified = classify_files(files)
    labels = file_labels(classified)
    write_labels(os.path.join(path, "labels.csv"), labels)
    write(csvfile, classified)


if __name__ == '__main__':
    main()
