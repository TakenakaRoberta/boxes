import csv


HEADER = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "birth_time",
                  "c_time",
                  "recent_access_time",
                  "modification_time",
                  "name", "file_path",
                  "labels", "new_filename", "new_dirname",
                  "main_label",
                  "duplicated",
                  ]


def read(source_csv):
    with open(source_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            yield data


def mark_duplicated(classified_files_csv_path, rows):
    with open(classified_files_csv_path, 'w', newline='') as csvf:
        classified_files_writer = csv.DictWriter(csvf, fieldnames=HEADER)
        classified_files_writer.writeheader()
        for row in rows:
            classified_files_writer.writerow(row)
