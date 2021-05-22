import sys
import csv
import os
import traceback
import re
import multiprocessing
import itertools as it
from matplotlib import pyplot as plt
from datetime import datetime

from stravaReader import reader
from stravaActivity import StravaActivity
from stravaSet import StravaSet

fd = os.path.sep  # folder delimiter
fn = 'activities.csv'

if __name__ == "__main__":
    # Reading input activities file
    fields, data = reader(fn)
    # Loading all data into StravaActivity objects
    activities = map(lambda x: StravaActivity(x), data)
    # Building up a StravaSet
    strava_set = StravaSet(activities)

    run_set = StravaSet(strava_set.filter_run())
    run_20_21 = StravaSet(
        it.chain(run_set.filter_year(2020), run_set.filter_year(2021)))
    run_20_21.print_total_km()
    multiprocessing.Process(target=run_20_21.plot_distance).start()
    multiprocessing.Process(target=run_20_21.plot_accumulated_distance).start()
    multiprocessing.Process(target=run_20_21.plot_accumulated_speed).start()

    run_20_21_2 = StravaSet(run_20_21.fill_all_days())
    run_20_21_2.set_xticks_distance(30)
    run_20_21_2.print_total_km()

    multiprocessing.Process(target=run_20_21_2.scatter_distance).start()
    multiprocessing.Process(target=run_20_21_2.plot_accumulated_distance).start()
    multiprocessing.Process(target=run_20_21_2.plot_accumulated_speed).start()
