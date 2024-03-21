from datetime import datetime
from urllib import request
from selenium.webdriver.common.by import By
from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.elements.label import Label
from test_data.constants import Constants
from utilities.fileUtils import FileUtil


class TestPage(Form):
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

    def __init__(self):
        super().__init__(Locator(By.XPATH, "//*[contains(text(), 'image/png')]"), "Test Page")

    def get_test_data(self, img_path):
        request.urlretrieve(self._test_screenshot.get_attribute("src"), img_path)
        return {
            'file_content': FileUtil.read_file_content(img_path),
            'log': self._test_log.text,
            'project_name': self._project_name_info.text,
            'test_name': self._test_name_info.text,
            'method_name': self._method_name_info.text,
            'status': '1' if self._status_info.text == 'Passed' else (
                '2' if self._status_info.text == 'Failed' else None),
            'start_time': datetime.strptime(self._start_time_info.text.split(': ')[1], Constants().
                                            strftime_regular + '.%f').strftime(Constants().strftime_regular),
            'environment': self._environment_info.text,
            'browser': self._browser_info.text,
            'name': self._name_info.text.split(': ')[1],
            'login': self._login_info.text.split(': ')[1],
            'email': self._email_info.text.split(': ')[1]
        }
