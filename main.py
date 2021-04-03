import sys
import csv
import os
import traceback
import re


fd = os.path.sep  # folder delimiter
fn = 'activities.csv'


def reader(file_name):
    current_path = os.getcwd() + fd + str(file_name)
    result = []
    try:
        with open(current_path, encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            field_names = csv_reader.fieldnames
            line_count = 0
            try:
                for row in csv_reader:
                    result.append(row)
                    line_count += 1
            except Exception:  # catching unicode error. Still don't know the problem
                traceback.print_exc()
                pass
        print('Columns read: {}'.format(line_count))
        return field_names, result
    except FileNotFoundError:
        print(('Please check that you have your file {}' +
               ' in the same folder as this script').format(file_name))


def total_distance(data):
    """Total distance given in meters"""
    total_distance = 0
    for e in data:
        total_distance += float(e['Distance'])
    return total_distance


def print_total_km(subset):
    buffer = re.sub(r"\B(?=\d{3})+", " ",
                    str(int(total_distance(subset)/1000)))
    print('You have run {} km in total'.format(buffer))


if __name__ == "__main__":
    fields, data = reader(fn)
    print_total_km(data)
