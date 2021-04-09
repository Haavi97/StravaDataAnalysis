import re
import itertools as it
from functools import reduce
from threading import Thread
from matplotlib import pyplot as plt


class StravaSet():
    def __init__(self, activities):
        """
        Atributes:
        ----------
        activities : StravaActivity iterable
        """
        self.activities = list(activities)

    def get_total_distance(self):
        """Total distance given in meters."""
        return reduce(lambda x, y: x+y, self.get_distance_iter())

    def get_distance_iter(self):
        return map(lambda x: x.distance, self.activities)

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

    def plot_series(self, series, title='""'):
        plt.plot(series)
        plt.title(title)
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
                                        title="Distance " + title_added)

    def plot_accumulated_distance(self, new_thread=True, title_added=''):
        da = list(it.accumulate(self.get_distance_iter()))
        if new_thread:
            self.plot_series_new_thread(da,
                                        title="Accumulated distance " + title_added)
        else:
            self.plot_series(self.get_distance_list(),
                                        title="Accumulated distance " + title_added)