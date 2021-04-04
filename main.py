import sys
import csv
import os
import traceback
import re
from matplotlib import pyplot as plt


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

def get_field_list(data, field):
    result = []
    for e in data:
        result.append(e[field])
    return result

def plot_float_list(data, factor=1.0):
    if factor >= 0.0:
        series = []
        for e in data:
            try:
                current = float(e)/factor
            except ValueError:
                pass
            series.append(current)
        plt.plot(series)
        plt.show()
    else:
        print('Invalid factor')

def filter_run(data):
    filtered = []
    for e in data:
        if e['Activity Type'] == 'Run':
            filtered.append(e)
    return filtered


if __name__ == "__main__":
    fields, data = reader(fn)
    print_total_km(data)
    run_data = filter_run(data)
    speed = get_field_list(run_data, 'Average Speed')
    plot_float_list(speed)
    dist = get_field_list(run_data, 'Distance')
    plot_float_list(dist, factor=1000)