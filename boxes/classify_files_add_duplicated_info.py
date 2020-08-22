import os
import csv
import argparse
from datetime import datetime
import logging

from utils.files import FileInfo
import classified_files_csv


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


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
                  "birth_time",
                  "c_time",
                  "recent_access_time",
                  "modification_time",
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
    total = len(groups)
    i = 0
    for k, items in groups.items():
        i += 1
        if i % 100 == 0:
          logging.info("Marked %i/%i", i, total)
        if len(items) == 1:
            items[0]['duplicated'] = 'unique'
            continue
        identify_first(groups[k])


def main():
    parser = argparse.ArgumentParser(
      'Lê o arquivo .csv que contém os dados dos arquivos classificados '
      '(gerado pelo classify_files.py). '
      'Identifica os arquivos iguais em uma nova coluna e '
      'gera uma nova planilha: *.duplicated.csv')
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    logging.info("-"*80)
    logging.info("Add duplicated info")

    source_csv = args.csvfile
    new_source_csv = source_csv.replace(".csv", ".duplicated.csv")
    rows = list(classified_files_csv.read(source_csv))
    groups = group_by_content_similarity(rows)
    
    mark_duplicated(groups)
    classified_files_csv.mark_duplicated(new_source_csv, rows)
    logging.info("-end-")


if __name__ == '__main__':
    main()
