import os
import csv
import argparse
import logging
import shutil

"""
def organize(file_path, dest_path):
    dest_path = os.path.normpath(dest_path)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    with open(file_path, 'r') as fp:
        for item in fp.read().splitlines():
            if "\t" in item:
                src, dst = item.split("\t")
                dst_file_path = os.path.join(dest_path, dst)
                dirname = os.path.dirname(dst_file_path)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)
                shutil.copyfile(src, dst_file_path)
"""

def create_script_to_copy(file_path, dest_path):
    mkdir = []
    copy = []
    dest_path = os.path.normpath(dest_path)
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            src = data["source"]
            dst = data["destination"]
            dst_file_path = os.path.join(dest_path, dst)
            dirname = os.path.dirname(dst_file_path)
            if not os.path.isdir(dirname):
                mkdir.append('mkdir -p "{}"'.format(dirname))
            if not os.path.isfile(dst_file_path):
                copy.append('cp "{}" "{}"'.format(src, dst_file_path))
    script = os.path.join(os.path.dirname(file_path), "organize.sh")
    with open(script, "w") as fp:
        fp.write("\n".join(sorted(list(set(mkdir)))) + "\n" + "\n".join(sorted(copy)))


def main():
    parser = argparse.ArgumentParser(
        'Dada uma lista de fonte e destino, e uma pasta raíz do destino,'
        ' cria um script para '
        'fazer cópia em uma nova estrutura')
    parser.add_argument("txtfile", help="text file")
    parser.add_argument("destination", help="destination path")
    args = parser.parse_args()

    create_script_to_copy(args.txtfile, args.destination)
    

if __name__ == '__main__':
    main()
