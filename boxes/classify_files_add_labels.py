import os
import csv
import argparse
import logging
from datetime import datetime
import json

from utils.files import FileInfo
import classified_files_csv


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

INVALID = ("PHOTO", "FOTO", "ANDROID", "DCIM", "IMPORTANTE",
           "S8", "PHOTOS", "PICTURES", "PHONE", "FOTOS", "PESSOAL", "MAQUINA", 
           "DE", "CELULAR", "CAMERA", "ARTSCOW", "DBOOK", "UNIKO",
           "CRIANCAS", "FERIAS", "CALENDARIO", "PHOOTO", "UPLOAD", "DATA", "COM",
           "IMAGES", "UPLOADS", "PANA", "NA", "ORGANIZAR", "DROPBOX", "BKP",
           "FILES", "CASA", "E", "DA", "CÓPIA", "I", "B", "SEM", "NO", "DO", "DE",
           "EM", "IMG",

)
VALID = ("GUSTAVO", )


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
    return [w for w in words if w.isalnum() and not w.isdigit()]


def new_dirname(words):
    return "_".join(words)


def write(csv_file_path, file_info_items):
    fieldnames = classified_files_csv.HEADER

    total = len(file_info_items)
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        i = 0
        for file_info in file_info_items:
            i += 1
            file_info["main_label"] = file_info["labels"][0]
            file_info["labels"] = json.dumps(file_info["labels"])

            writer.writerow(file_info)
            if i % 100 == 0:
                logging.info("Created %i/%i items in CSV", i, total)
        logging.info("Created %i items in CSV", i)


def sorted_by_higher_score(names, scores):
    items = [
        (scores[name], name)
        for name in names
        if name not in INVALID
    ]
    labels = [item[1] for item in sorted(items, reverse=True)]
    if len(labels) == 0:
        labels = ["REORGANIZAR"]
    return labels


def file_labels(file_info_items):
    labels = {}
    labels_groups = {}
    total = len(file_info_items)
    i = 0
    for file_info in file_info_items:
        i += 1
        logging.info("Label %i/%i", i, total)
        file_path = file_info.get("file_path")
        dirname = os.path.dirname(file_path)
        dirname = convert_notalnum_to_under(dirname)
        words = get_words(dirname)[2:]

        file_info['labels'] = get_labels(words)
        file_info['new_dirname'] = new_dirname(words)
        file_info['new_filename'] = new_filename(
            file_path, file_info["first_date"], file_info['new_dirname'])
        if "casamento" in file_path:
            logging.info("CASAMENTO")
            logging.info(file_info["labels"])
            logging.info(file_info["new_dirname"])

        for label in file_info["labels"]:
            labels[label] = labels.get(label, 0)
            labels[label] += 1

    for file_info in file_info_items:
        logging.info("Main Label %i/%i", i, total)
        file_info["labels"] = sorted_by_higher_score(file_info["labels"], labels)
        if file_info["duplicated"] != "duplicated":
            labels_groups[file_info["new_dirname"]] = file_info["labels"][0]
    
    return labels, labels_groups


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
      'Lê o arquivo .csv que contém os dados dos arquivos classificados '
      '(gerado pelo classify_files.py). '
      'Com `file_path` identifica o arquivo com labels e '
      'gera uma nova planilha')
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    logging.info("-"*80)
    logging.info("Add labels info")
    source_csv = args.csvfile
    new_source_csv = source_csv.replace(".csv", ".labeled.csv")
    labels_csv = source_csv.replace(".csv", ".labels.csv")
    new_dirnames_csv = source_csv.replace(".csv", ".new_dirnames.csv")
    rows = classified_files_csv.read(source_csv)
    rows = list(rows)
    labels, new_dirnames = file_labels(rows)
    write(new_source_csv, rows)
    write_labels(labels_csv, labels)
    write_labels(new_dirnames_csv, new_dirnames)
    logging.info("-end-")


if __name__ == '__main__':
    main()
