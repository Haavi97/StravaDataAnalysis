import sys
import csv
import os


fd = os.path.sep  # folder delimiter
fn = 'activities.csv'

def reader(file_name):
    current_path = os.getcwd() + fd + str(file_name)
    with open(current_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        print(csv_reader.fieldnames)
        line_count = 0
        try:
            for row in csv_reader:
                print(row)
                line_count += 1
        except UnicodeDecodeError: # catching unicode error. Still don't know the problem
            pass
    print('Columns read: {}'.format(line_count))
    return csv_reader


if __name__ == "__main__":
    reader(fn)