import os
import csv
import argparse
from datetime import datetime
import logging

from PIL import Image

from utils.files import FileInfo
import classified_files_csv


logging.basicConfig(level=logging.INFO)


def group_by_content_similarity(rows):
    items = {}
    for data in rows:
        logging.info(data.get("file_path"))
        k = "_".join((data.get("hash") or "", data.get("size") or "", data.get("first_time") or "", ))
        items[k] = items.get(k, [])
        items[k].append(data)
    return items

def identify_first(group):
    colums = ("first_time", 
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  )
    _sorted = []
    for i, item in enumerate(group):
        item_data = [
            item.get(col)
            for col in colums
        ]
        _sorted.append((item_data, i))
    _sorted = sorted(_sorted)
    first = _sorted[0][1]
    for i, item in enumerate(group):
        group[i]['duplicated'] = 'duplicated' if i != first else 'original'
             

def mark_duplicated(groups):
    for k, items in groups.items():
        if len(items) == 1:
            items[0]['duplicated'] = 'unique'
            continue
        identify_first(groups[k])


def main():
    parser = argparse.ArgumentParser(
      'Lê o arquivo .csv que contém os dados dos arquivos classificados '
      '(gerado pelo classify.py). '
      'Identifica os arquivos iguais em uma nova coluna e '
      'gera uma nova planilha: *.duplicated.csv')
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()
    new_source_csv = source_csv.replace(".csv", ".duplicated.csv")
    rows = classified_files_csv.read(source_csv)
    groups = group_by_content_similarity(rows)
    
    mark_duplicated(groups)
    classified_files_csv.mark_duplicated(new_source_csv, rows)

if __name__ == '__main__':
    main()
