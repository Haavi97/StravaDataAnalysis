import sys
import csv
import os
import traceback
import re
import itertools as it
from matplotlib import pyplot as plt
from datetime import datetime

from stravaReader import reader
from stravaActivity import StravaActivity
from stravaSet import StravaSet

fd = os.path.sep  # folder delimiter
fn = 'activities.csv'


def total_distance(data):
    """Total distance given in meters."""
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
    activities = map(lambda x: StravaActivity(x), data)
    strava_set = StravaSet(activities)
    run_set = StravaSet(strava_set.filter_run())
    run_20_21 = StravaSet(
        it.chain(run_set.filter_year(2020), run_set.filter_year(2021)))
    run_20_21.print_total_km()
    run_20_21.plot_distance(new_thread=False)
    run_20_21.plot_accumulated_distance(new_thread=False)
    run_20_21.plot_accumulated_speed(new_thread=False)

    run_20_21_2 = StravaSet(run_20_21.fill_all_days())
    run_20_21_2.set_xticks_distance(30)
    run_20_21_2.print_total_km()
    run_20_21_2.scatter_distance(new_thread=False)
    run_20_21_2.plot_accumulated_distance(new_thread=False)
    run_20_21_2.plot_accumulated_speed(new_thread=False)
