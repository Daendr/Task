class Constants:
    _test_data_file_name = "test_data.json"
    _sql_query_file_name = "sqlquery.json"
    _config_file_name = "config.json"
    _strftime_regular = "%Y-%m-%d %H:%M:%S"

    def get_strftime_regular(self):
        return self._strftime_regular

    def get_test_data_file_name(self):
        return self._test_data_file_name

    def set_test_data_file_name(self, value):
        self._test_data_file_name = value

    def get_sql_query_file_name(self):
        return self._sql_query_file_name

    def set_sql_query_file_name(self, value):
        self._sql_query_file_name = value

    def get_config_file_name(self):
        return self._config_file_name

    def set_config_file_name(self, value):
        self._config_file_name = value

    test_data_file_name = property(get_test_data_file_name, set_test_data_file_name)
    sql_query_file_name = property(get_sql_query_file_name, set_sql_query_file_name)
    config_file_name = property(get_config_file_name, set_config_file_name)
    strftime_regular = property(get_strftime_regular)
