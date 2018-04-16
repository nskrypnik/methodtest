"""The module contains TempTracker class for tracking temperature
"""
import time
from functools import reduce

def reindex_if_required(method):
    """Decorator for TempTrackert get_* methods to allow requesting
    reindexing of class data set
    """
    def wrap(self, reindex = False):
        if reindex:
            self.reindex(self)
        return method(self)
    return wrap


class TempRecord:
    """Class containing information temperature record
    """

    def __init__(self, temp):
        self.temp = temp
        self.timestamp = time.time()


class TempTracker:
    """Class describing temerature tracker

    Attributes:
        temp_rec_pool: Pool of temerature records
        max_temp: Maximum temperature record
        min_temp: Minimum temperature record
        records_count: Count of temperature records
        mean_temp: mean temperature
    """

    def __init__(self):
        """Init TempTracker with initial values
        """
        self.temp_rec_pool = []
        self.records_count = 0
        self.max_temp = None
        self.min_temp = None
        self.mean_temp = None

    @reindex_if_required
    def get_max(self):
        return self.max_temp.temp

    @reindex_if_required
    def get_min(self):
        return self.min_temp.temp

    @reindex_if_required
    def get_mean(self):
        return self.mean_temp

    def insert(self, temp):
        """Inserts a new temeperature value into the tracker

        Args:
            temp: integer value of measured temperature
        """
        self.records_count += 1 # increment count of recors
        new_temp_rec = TempRecord(temp) # create new temp record
        self.temp_rec_pool.append(new_temp_rec) # put it to the pool
        self.calculate_current_max(new_temp_rec) # calculate new max temperature
        self.calculate_current_min(new_temp_rec) # claculate new min temperature
        self.calculate_current_mean(new_temp_rec)

    def calculate_current_max(self, new_temp_rec):
        """Calculate current maximum temperature according to previous current

        Args:
            new_temp_rec: New temperature record
        """
        if self.max_temp is None:
            self.max_temp = new_temp_rec
        else:
            if new_temp_rec.temp > self.max_temp.temp:
                self.max_temp = new_temp_rec

    def calculate_current_min(self, new_temp_rec):
        """Calculate current minimum temperature according to previous current

        Args:
            new_temp_rec: New temperature record
        """
        if self.min_temp is None:
            self.min_temp = new_temp_rec
        else:
            if new_temp_rec.temp < self.min_temp.temp:
                self.min_temp = new_temp_rec

    def calculate_current_mean(self, new_temp_rec):
        """Calculate current mean temperature

        Args:
            new_temp_rec: New temperature record
        """
        if self.mean_temp is None:
            self.mean_temp = new_temp_rec.temp
        else:
            count = float(self.records_count) # trick to make result float
            self.mean_temp = (self.mean_temp * (count - 1) + new_temp_rec.temp) / count

    def reindex(self):
        """Recalculate all values according to presented dataset, e.g. when current min/max/measn
        values a thought to be corrupted by race condition or other reason
        """
        # sort temp records by timestamp
        self.temp_rec_pool = sorted(self.temp_rec_pool, key=lambda temp_rec: temp_rec.timestamp)
        # find min and max
        self.min_temp = self.temp_rec_pool[0]
        self.max_temp = self.temp_rec_pool[0]
        for temp_rec in self.temp_rec_pool:
            if self.min_temp.temp > temp_rec.temp:
                self.min_temp = temp_rec
            if self.max_temp.temp < temp_rec.temp:
                self.max_temp = temp_rec
        # claculate mean
        count = float(self.records_count)
        sum_of_temps = reduce(
            lambda product, temp_rec: product + temp_rec.temp,
            self.temp_rec_pool,
            0
        )
        self.mean_temp = sum_of_temps / count
