from datetime import datetime


class StravaActivity():
    def __init__(self, activity):
        """Initialized from a dictionary with the data.

        The dictionary is given by the csv reader.

        Atributes
        ---------
        date : datetime object
        distance: float
                    distance of the activity in meters
        """
        self.id = activity['Activity ID']
        self.date = datetime.strptime(
            activity['Activity Date'], '%b %d, %Y, %I:%M:%S %p')
        self.distance = float(activity['Distance'])
        self.moving_time = float(activity['Moving Time'])
        self.type = activity['Activity Type']

    def get_km(self):
        return self.distance/1000

    def get_minutes(self):
        """Get moving time of the activity in minutes"""
        return self.moving_time/60

    def get_min_per_km(self):
        return self.get_km()
