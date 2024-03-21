from datetime import datetime
from py_selenium_auto.browsers.browser_services import BrowserServices
from selenium.webdriver.common.by import By
from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.elements.label import Label
from test_data.constants import Constants


class ProjectPage(Form):
    _assert_test_name = ("//*[contains(text(), '{}')]", "test_name_locator")
    _table_rows = Label(Locator(By.XPATH, "//*[(@class='table')]//tr"), "table_rows")
    _test_screenshot = Label(Locator(By.XPATH, "//*[@class='thumbnail']"), "test_screenshot")
    _test_log = Label(Locator(By.XPATH, "(//*[@class='table']//td[1])[1]"), "test_log")
    _project_name_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[1]"), "project_name")
    _test_name_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[2]"), "test_name_info")
    _method_name_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[3]"), "method_name_info")
    _status_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[4]"), "status_info")
    _start_time_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[5]"), "start_time_info")
    _environment_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[8]"), "environment_info")
    _browser_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[9]"), "browser_info")
    _name_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[10]"), "name_info")
    _login_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[11]"), "login_info")
    _email_info = Label(Locator(By.XPATH, "(//*[@class='list-group-item-text'])[12]"), "email_info")
    _table_headers = Label(Locator(By.XPATH, "//*[(@class='table')]//tr[1]/th"), "table_headers")
    _test_name = ("(//*[(@class='table')]//tr[{}]//a)[1]", "test_name_locator")
    _test_method = ("//*[(@class='table')]//tr[{}]//td[2]", "test_method_locator")
    _test_result = ("//*[(@class='table')]//tr[{}]//*[contains(@class, 'label')]", "test_result_locator")
    _test_start = ("//*[(@class='table')]//tr[{}]/td[4]", "test_start_time")
    _test_end = ("//*[(@class='table')]//tr[{}]/td[5]", "test_end_time")

    def __init__(self):
        super().__init__(Locator(By.XPATH, "//*[@id='graph']"), "Project Page")

    def get_table_headers(self):
        return [i.text for i in BrowserServices.Instance.browser.driver.find_elements(
            By.XPATH, self._table_headers.locator.value)[:-2]]

    def get_tests(self, table_rows):
        tests_data = []
        for i in range(2, table_rows + 2):
            tests_data.append(self.get_test_data(i))
        return tests_data

    def get_test_data(self, row_index):
        test_name = Label(Locator(By.XPATH, self._test_name[0].format(row_index)), self._test_name[1]).text
        test_method = Label(Locator(By.XPATH, self._test_method[0].format(row_index)), self._test_method[1]).text
        test_result = Label(Locator(By.XPATH, self._test_result[0].format(row_index)), self._test_result[1]).text
        test_start = Label(Locator(By.XPATH, self._test_start[0].format(row_index)), self._test_start[1]).text
        test_end = Label(Locator(By.XPATH, self._test_end[0].format(row_index)), self._test_end[1]).text
        status_id = '1' if test_result == 'Passed' else ('2' if test_result == 'Failed' else None)
        test_start_time = datetime.strptime(test_start, Constants().strftime_regular + '.%f') if test_start else None
        test_end_time = datetime.strptime(test_end, Constants().strftime_regular + '.%f') if test_end else None
        return [test_name, test_method, status_id, test_start_time, test_end_time]

    def get_tests_number(self):
        return len(BrowserServices.Instance.browser.driver.find_elements(By.XPATH, self._table_rows.locator.value)[1::])

    def is_test_displayed(self, test_name):
        return Label(Locator(
            By.XPATH, self._assert_test_name[0].format(test_name)), self._test_name[1]).state.wait_for_displayed()

    def click_test_link(self, test_name):
        return Label(
            Locator(By.XPATH, self._assert_test_name[0].format(test_name)), self._test_name[1]).click()

    table_headers = property(get_table_headers)
    tests_number = property(get_tests_number)
