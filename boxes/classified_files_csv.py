import csv


HEADER = ['type', 'hash', 'size', "first_time", 
                  "first_date",
                  "birth_date",
                  "c_date",
                  "recent_access_date",
                  "modification_date",
                  "name", "file_path",
                  "labels", "new_filename", "new_dirname",
                  "main_label",
                  ]


def read(source_csv):
    items = {}
    with open(source_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            yield data


def mark_duplicated(classified_files_csv_path, rows):
    classified_files_csv.HEADER.append("duplicated")

    with open(classified_files_csv_path, 'w', newline='') as csv:
        classified_files_writer = csv.DictWriter(csv, fieldnames=classified_files_csv.HEADER)
        classified_files_writer.writeheader()
        for row in rows:
            classified_files_writer.writerow(e)
