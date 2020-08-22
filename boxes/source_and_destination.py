import os
import csv
import argparse
from datetime import datetime
import logging


import classified_files_csv


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def new_path(root_dir, row, _format):
    if _format == "DIRNAME": 
        return os.path.join(root_dir, row['new_dirname'], row['new_filename'])

    if _format == "LABEL": 
        return os.path.join(root_dir, row['main_label'], row['new_filename'])

    if _format == "LABEL/DIRNAME": 
        return os.path.join(root_dir, row['main_label'], row['new_dirname'], row['new_filename'])

    if _format == "RETRO/DIRNAME": 
        return os.path.join(root_dir, "RETRO", row['new_dirname'], row['new_filename'])

    if _format == "DBOOK/LABEL/DIRNAME": 
        return os.path.join(root_dir, "DBOOK", row['main_label'], row['new_dirname'], row['new_filename'])

    subdir = row['first_date'].split("-")
    if _format == "YEAR/MONTH": 
        return os.path.join(
            root_dir,
            subdir[0], subdir[1],
            row['new_filename'])
    if _format == "YEAR/MONTH/LABEL_DIRNAME": 
        return os.path.join(
            root_dir,
            subdir[0], subdir[1],
            row['main_label'] + "_" + row['new_dirname'],
            row['new_filename'])
    if _format == "YEAR/MONTH/LABEL/DIRNAME": 
        return os.path.join(
            root_dir,
            subdir[0], subdir[1],
            row['main_label'],
            row['new_dirname'],
            row['new_filename'])
    if _format == "YEAR/MONTH/DIRNAME": 
        return os.path.join(
            root_dir,
            subdir[0], subdir[1],
            row['new_dirname'],
            row['new_filename'])
    if _format == "YEAR/MONTH/LABEL": 
        return os.path.join(
            root_dir,
            subdir[0], subdir[1],
            row['main_label'],
            row['new_filename'])
    if _format == "YEAR/MONTH/REORGANIZAR":
        return os.path.join(root_dir, subdir[0], subdir[1], "REORGANIZAR", row["new_filename"])


def get_path_data(row):
    if row['duplicated'] == 'duplicated':
        return 'DUPLICATED', "YEAR/MONTH/DIRNAME"
    if "PINTURA" in row["new_dirname"] and "MADEIRA" in row["new_dirname"]:
        return "ORGANIZED", "LABEL"

    for name in ("DIDA", "ANTIGAS", "FACEBOOK", "INSTAGRAM", "ENJOEI", "WHAT",
                 "TELEGRAM", "MESSENGER", "KINDLE", "THUMB", "COLLAGE"):
        if name in row["new_dirname"]:
            return "ORGANIZED", "LABEL" 
    if "DBOOK" in row["new_dirname"]:
        return "ORGANIZED", "DBOOK/LABEL/DIRNAME" 

    if "RETRO" in row["new_dirname"]:
        return "ORGANIZED", "RETRO/DIRNAME" 

    if "PYPROJETOS" in row["new_dirname"]:
        return "IGNORE", "DIRNAME"

    if row['main_label'] in ["REORGANIZAR", "CAMERAUPLOADS", "CACHE", "IMG"]:
        return "ORGANIZED", "YEAR/MONTH/REORGANIZAR"

    if row['main_label'] in ["ARTESANATO"]:
        return "ORGANIZED", "LABEL"

    return "ORGANIZED", "YEAR/MONTH/LABEL"


def analyze(row):
    root_dir, _format = get_path_data(row)
    return new_path(root_dir, row, _format)


def create(csv_file_path, result_file_path):
    fieldnames = ['source', 'destination']
    rows = list(classified_files_csv.read(csv_file_path))
    total = len(rows)
    with open(result_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        i = 0
        for row in rows:
            i += 1
            destination = analyze(row)
            data = {'source': row['file_path'], 'destination': destination}
            if i % 100 == 0:
                logging.info("Created %i/%i items in CSV", i, total)
            writer.writerow(data)


def main():
    parser = argparse.ArgumentParser(
      'Lê o arquivo .csv que contém os dados dos arquivos classificados '
      '(gerado pelo classify_files.py). '
      'Cria para cada linha, um par fonte e destino de cópia ou '
      'movimentação para reorganizar os arquivos')
    parser.add_argument("csv_file_path", help="csv file")
    args = parser.parse_args()
    csv_file_path = args.csv_file_path
    result = csv_file_path.replace(".csv", ".src_dst.csv")
    create(csv_file_path, result)
    logging.info("-end-")


if __name__ == '__main__':
    main()
