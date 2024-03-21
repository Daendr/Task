from datetime import datetime
from test_data.constants import Constants
from utilities.csvManager import CsvManager


class DataComparator:
    @staticmethod
    def prepare_comparison_data(csv_path, tests):
        comparison_data = {"expected_data": {}, "actual_data": {}}
        for row_index, row in enumerate(CsvManager.read_csv_data(csv_path)):
            test_name, test_method, test_result, test_start, test_end = row
            test_start_time = datetime.strptime(test_start, Constants().strftime_regular) if test_start else None
            test_end_time = datetime.strptime(test_end, Constants().strftime_regular) if test_end else None
            expected_data = {
                'Test name': test_name,
                'Test method': test_method,
                'Latest test result': int(test_result) if test_result else None,
                'Latest test start time': test_start_time.strftime(Constants().strftime_regular)
                if test_start_time else '',
                'Latest test end time': test_end_time.strftime(Constants().strftime_regular) if test_end_time else '',
            }
            actual_data = {
                'Test name': [test.name for test in tests][row_index],
                'Test method': [test.method_name for test in tests][row_index],
                'Latest test result': int([test.status_id for test in tests][row_index]) if test_result else None,
                'Latest test start time': [test.start_time.strftime(Constants().strftime_regular)
                                           if test.start_time else '' for test in tests][row_index],
                'Latest test end time': [test.end_time.strftime(Constants().strftime_regular)
                                         if test.end_time else '' for test in tests][row_index],
            }
            comparison_data["expected_data"][row_index] = expected_data
            comparison_data["actual_data"][row_index] = actual_data
        return comparison_data
