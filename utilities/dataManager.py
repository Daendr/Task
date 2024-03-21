import json
import os
from test_data.constants import Constants


class DataManager:
    @staticmethod
    def get_value(key, filename=Constants().config_file_name):
        with open(os.path.join('..', 'test_data', filename)) as file:
            return json.load(file).get(key)
