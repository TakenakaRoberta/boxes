import os
import csv
import argparse
from datetime import datetime
from PIL import Image

from utils.files import FileInfo


def group_by_similarity(source_csv):
    fieldnames = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  ]
    
    items = {}
    with open(source_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            print(data.get("file_path"))
            k = "_".join((data.get("hash") or "", data.get("size") or "", data.get("first_time") or "", ))
            items[k] = items.get(k, [])
            items[k].append(data)
    return items


def classify(items, duplicated, unique):
    unique_fieldnames = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  ]
    duplicated_fieldnames = ['key', 'type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  ]
    with open(duplicated, 'w', newline='') as duplicated_csv:
        d_writer = csv.DictWriter(duplicated_csv, fieldnames=duplicated_fieldnames)
        d_writer.writeheader()
        with open(unique, 'w', newline='') as unique_csv:
            unique_writer = csv.DictWriter(unique_csv, fieldnames=unique_fieldnames)
            unique_writer.writeheader()
            for k, elements in items.items():
                for e in elements:
                    if len(elements) == 1:
                        unique_writer.writerow(e)
                    else:
                        e.update({'key': k})
                        d_writer.writerow(e)


def main():
    parser = argparse.ArgumentParser(
      'Lê o arquivo .csv que contém os dados dos arquivos classificados '
      '(gerado pelo classify.py). '
      'Identifica os arquivos iguais e os diferentes '
      'e os coloca respectivamente em *.duplicated.csv e *.unique.csv')
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    groups = group_by_similarity(args.csvfile)
    duplicated = args.csvfile.replace(".csv", ".duplicated.csv")
    unique = args.csvfile.replace(".csv", ".unique.csv")

    classify(groups, duplicated, unique)


if __name__ == '__main__':
    main()
