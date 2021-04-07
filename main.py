import sys
import csv
import os
import traceback
import re
import itertools as it
from matplotlib import pyplot as plt
from datetime import datetime


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


def plot_float_list(data, factor=1.0, title=""):
    if factor >= 0.0:
        series = []
        current = None
        for e in data:
            try:
                current = float(e)/factor
            except ValueError:
                pass
            series.append(current)
        plt.plot(series)
        plt.title(title)
        plt.show()
    else:
        print('Invalid factor')


def filter_run(data):
    return list(filter(lambda x: x['Activity Type'] == 'Run', data))


def time_str_to_datetime(date_str):
    return datetime.strptime(date_str, '%b %d, %Y, %I:%M:%S %p')


def filter_year(year, data):
    return list(filter(lambda x: time_str_to_datetime(x['Activity Date']).year == year, data))


def min_per_km(e):
    return (float(e['Moving Time'])/60)/(float(e['Distance'])/1000)


def get_min_per_km(data):
    return list(map(lambda x: min_per_km(x), data))


def avg(l):
    return sum(l) / len(l)


def list_3_avg(l):
    return [avg(l[i:(i+3)]) for i in range(0, len(l), 3)]


if __name__ == "__main__":
    fields, data = reader(fn)
    print_total_km(data)
    run_data = filter_run(data)
    speed = get_field_list(run_data, 'Average Speed')
    plot_float_list(speed, title='Average Speed')
    dist = get_field_list(run_data, 'Distance')
    plot_float_list(dist, factor=1000, title='Distance',)

    run_data_2020 = filter_year(2020, filter_run(data))
    print_total_km(run_data_2020)
    speed = get_min_per_km(run_data_2020)
    plot_float_list(speed, title='Speeds 2020')

    plot_float_list(list_3_avg(speed), title='Speeds 3 avg 2020')

    dist_acu = list(it.accumulate(map(lambda x: float(x),
                                      get_field_list(run_data_2020, 'Distance'))))
    plot_float_list(dist_acu, factor=1000, title='Distance accumulated 2020',)
