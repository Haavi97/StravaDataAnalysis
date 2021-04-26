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

    def get_total_distance(self):
        """Total distance given in meters."""
        return reduce(lambda x, y: x+y, self.get_distance_iter())

    def get_distance_iter(self):
        return map(lambda x: x.distance, self.activities)

    def get_moving_time_iter(self):
        return map(lambda x: x.moving_time, self.activities)

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
                        str(int(self.get_total_distance()/1000)))
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
        plt.plot(series)
        plt.title(title)
        if axis_labels != []:
            plt.xticks(np.arange(len(axis_labels)), axis_labels, rotation=45)
        plt.tight_layout()
        plt.show()

    def scatter_series(self, series, title='""', axis_labels=[]):
        self.figs += 1
        plt.figure(self.figs)
        plt.plot(series, marker='o', linestyle='None')
        plt.title(title)
        if axis_labels != []:
            plt.xticks(np.arange(len(axis_labels)), axis_labels, rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_series_new_thread(self, series, title=''):
        t = Thread(target=self.plot_series, args=[series, title])
        t.start()

    def plot_distance(self, new_thread=True, title_added=''):
        if new_thread:
            self.plot_series_new_thread(self.get_distance_list(),
                                        title="Distance " + title_added)
        else:
            self.plot_series(self.get_distance_list(),
                             title="Distance " + title_added, axis_labels=self.get_paded_dates(10))

    def scatter_distance(self, new_thread=True, title_added=''):
        self.scatter_series(self.get_distance_list(),
                            title="Distance " + title_added, axis_labels=self.get_paded_dates(10))

    def plot_accumulated_distance(self, new_thread=True, title_added=''):
        da = list(it.accumulate(self.get_distance_iter()))
        if new_thread:
            self.plot_series_new_thread(da,
                                        title="Accumulated distance " + title_added)
        else:
            self.plot_series(da,
                             title="Accumulated distance " + title_added, axis_labels=self.get_paded_dates(10))

    def plot_accumulated_speed(self, new_thread=True, title_added=''):
        da = it.accumulate(self.get_distance_iter())
        ta = it.accumulate(self.get_moving_time_iter())
        sa = list(map(lambda x, y: x/y if y!=0 else 0, da, ta))
        tstr = "Accumulated speed in (m/s)"
        if new_thread:
            self.plot_series_new_thread(sa,
                                        title=tstr + title_added)
        else:
            self.plot_series(sa,
                             title=tstr + title_added, axis_labels=self.get_paded_dates(10))

    def fill_all_days(self):
        iterator = iter(self.activities)
        current = deepcopy(next(iterator))
        yield current
        current_day = current.date
        for e in iterator:
            while e.date.day != current_day.day:
                current_day += timedelta(days=1)
                current.date = current_day
                current.empty()
                yield current
            current = deepcopy(e)
            yield current
