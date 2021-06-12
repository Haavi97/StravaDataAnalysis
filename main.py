import sys
import csv
import os
import traceback
import re
import multiprocessing
import itertools as it
from matplotlib import pyplot as plt
from datetime import datetime
from pyfiglet import Figlet

from stravaReader import reader
from stravaActivity import StravaActivity
from stravaSet import StravaSet

fd = os.path.sep  # folder delimiter
fn = 'activities.csv'

if __name__ == "__main__":
    # Getting fancy
    f = Figlet(font='big')
    print(f.renderText('Strava data'))

    # Reading input activities file
    fields, data = reader(fn)
    # Loading all data into StravaActivity objects
    activities = map(lambda x: StravaActivity(x), data)
    # Building up a StravaSet
    strava_set = StravaSet(activities)
