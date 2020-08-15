import os
import csv
import argparse
import logging


def dest(data):
    d = data.get("first_date").split("-")
    file_path = os.path.normpath(data.get("file_path"))
    dirname = os.path.dirname(file_path)
    basename = os.path.basename(file_path)
    splitted_path = dirname.split("\\")
    new_dirname = "_".join(splitted_path[2:])
    if not new_dirname:
        new_dirname = 'folder'
    new_basename = "_".join([data.get("first_date"), new_dirname, basename])
    try:
        return os.path.join(new_dirname, new_basename)
    except Exception as e:
        logging.exception(
            "%s: %s (file_path), %s (dirname), %s (new_dirname), "
            "%s (new_basename)", e, data.get("file_path"), d, new_dirname, new_basename)
        return 'unknown'
        

def source_and_dest(source_csv):
    fieldnames = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  ]

    items = []
    with open(source_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for data in reader:
            try:
                items.append((os.path.normpath(data.get("file_path")), dest(data)))
            except Exception as e:
                logging.exception("%s %s", data.get("file_path"), e)
    return items
            

def write_source_and_dest(file_path, items):
    with open(file_path, 'w') as fp:
        fp.write("\n".join(["{}\t{}".format(s, d) for s, d in items]))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csvfile", help="csv file")
    args = parser.parse_args()

    items = source_and_dest(args.csvfile)
    txtfile = args.csvfile.replace('.csv', '.source_and_dest.txt')
    write_source_and_dest(txtfile, items)


if __name__ == '__main__':
    main()
