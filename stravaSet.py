import re
import itertools as it
import numpy as np

from functools import reduce
from threading import Thread
from datetime import timedelta
from copy import deepcopy
from matplotlib import pyplot as plt


class StravaSet():
    def __init__(self, activities):
        """
        Atributes:
        ----------
        activities : StravaActivity iterable
        """
        self.activities = list(activities)
        self.figs = 0
        self.n = 10

    def get_total_distance(self):
        """Total distance given in meters."""
        return reduce(lambda x, y: x+y, self.get_distance_iter())

    def get_distance_iter(self):
        return map(lambda x: x.distance/1000, self.activities)

    def get_moving_time_iter(self):
        return map(lambda x: x.moving_time/60, self.activities)

    def get_dates_iter(self):
        return map(lambda x: x.date.strftime("%d/%m/%Y"), self.activities)

    def get_paded_dates(self, n):
        result = []
        dates = list(self.get_dates_iter())
        for i in range(len(dates)):
            if i % n == 0:
                result.append(dates[i])
            else:
                result.append('')
        return result

    def print_total_km(self):
        buffer = re.sub(r"\B(?=\d{3})+", " ",
                        str(int(self.get_total_distance())))
        print('You have run {} km in total'.format(buffer))

    def filter_run(self):
        """Returns an iterable of the run activities."""
        return filter(lambda x: x.type == 'Run', self.activities)

    def filter_year(self, year):
        """Returns an iterable of the given year (int) activities."""
        return filter(lambda x: x.date.year == year, self.activities)

    def get_distance_list(self):
        return list(self.get_distance_iter())

    def plot_series(self, series, title='""', axis_labels=[]):
        self.figs += 1
        plt.figure(self.figs)
        plt.plot(series, color='r')
        plt.title(title)
        if axis_labels != []:
            plt.xticks(np.arange(len(axis_labels)), axis_labels, rotation=45)
        plt.tight_layout()
        plt.show()

    def scatter_series(self, series, title='""', axis_labels=[]):
        self.figs += 1
        plt.figure(self.figs)
        plt.plot(zero_to_nan(series), marker='o', linestyle='None', color='r')
        plt.title(title)
        if axis_labels != []:
            plt.xticks(np.arange(len(axis_labels)), axis_labels, rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_distance(self, title_added=''):
        self.plot_series(self.get_distance_list(),
                         title="Distance " + title_added, axis_labels=self.get_paded_dates(self.n))

    def scatter_distance(self, title_added=''):
        self.scatter_series(self.get_distance_list(),
                            title="Distance km" + title_added, axis_labels=self.get_paded_dates(self.n))

    def plot_accumulated_distance(self, title_added=''):
        da = list(it.accumulate(self.get_distance_iter()))
        self.plot_series(da,
                         title="Accumulated distance (km)" + title_added, axis_labels=self.get_paded_dates(self.n))

    def plot_accumulated_speed(self, title_added=''):
        da = it.accumulate(self.get_distance_iter())
        ta = it.accumulate(self.get_moving_time_iter())
        sa = list(map(lambda x, y: x/(y/60) if y != 0 else 0, da, ta))
        tstr = "Accumulated speed in (km/h)"
        self.plot_series(sa,
                         title=tstr + title_added, axis_labels=self.get_paded_dates(self.n))

    def fill_all_days(self):
        iterator = iter(self.activities)
        first_element = next(iterator)
        yield first_element
        current = deepcopy(first_element)
        current_day = current.date
        for e in iterator:
            while e.date.day != current_day.day:
                current_day += timedelta(days=1)
                to_yield = deepcopy(current)
                to_yield.date = current_day
                to_yield.empty()
                yield to_yield
            current = deepcopy(e)
            yield current

    def set_xticks_distance(self, n):
        self.n = n


def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    '''From: https://stackoverflow.com/questions/18697417/not-plotting-zero-in-matplotlib-or-change-zero-to-none-python'''
    return [float('nan') if x == 0 else x for x in values]
