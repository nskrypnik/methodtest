from tests import pytest, unittest
from methodtest.temp_tracker import TempTracker, TempRecord


class TempTrackerTest(unittest.TestCase):

    def setUp(self):
        tt = TempTracker()
        for t in [67, 55, 76, 71, 59, 53, 69, 70, 74]:
            tt.insert(t)
        self.temp_tracker = tt

    def test_get_min(self):
        self.assertEqual(self.temp_tracker.get_min(), 53)

    def test_get_max(self):
        self.assertEqual(self.temp_tracker.get_max(), 76)

    def test_get_mean(self):
        mean = self.temp_tracker.get_mean()
        self.assertEqual(mean, 66.0)
        self.assertEqual(type(mean), float)

    def test_insert(self):
        tt = self.temp_tracker
        count = tt.records_count
        tt.insert(79)
        self.assertEqual(tt.records_count, count + 1)
        self.assertEqual(tt.get_max(), 79)
        self.assertEqual(tt.get_min(), 53)

        tt.insert(49)
        self.assertEqual(tt.records_count, count + 2)
        self.assertEqual(tt.get_max(), 79)
        self.assertEqual(tt.get_min(), 49)

    def test_calculate_current_max(self):
        self.temp_tracker.calculate_current_max(TempRecord(80))
        self.assertEqual(self.temp_tracker.get_max(), 80)

    def test_calculate_current_max(self):
        self.temp_tracker.calculate_current_min(TempRecord(30))
        self.assertEqual(self.temp_tracker.get_min(), 30)

    def test_calculate_current_mean(self):
        self.temp_tracker.records_count += 1
        self.temp_tracker.calculate_current_mean(TempRecord(80))
        self.assertEqual(self.temp_tracker.get_mean(), 67.4)

    def test_reindex_is_called(self):

        def spy(func):
            def wrap(self):
                spy.call_count += 1
                return func()
            return wrap
        spy.call_count = 0

        self.temp_tracker.reindex = spy(self.temp_tracker.reindex)
        self.assertEqual(self.temp_tracker.get_min(True), 53)
        self.assertEqual(spy.call_count, 1)
        self.assertEqual(self.temp_tracker.get_max(True), 76)
        self.assertEqual(spy.call_count, 2)
        mean = self.temp_tracker.get_mean(True)
        self.assertEqual(mean, 66.0)
        self.assertEqual(spy.call_count, 3)
