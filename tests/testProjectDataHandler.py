import os
import re
import time
from datetime import datetime
import pytest
from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto_core.logging.logger import Logger
from apiUtils.apiutils import ApiUtils
from databaseUtils.testDataManager import TestDataManager
from models.dataBase.project import Project
from models.dataBase.test import Test
from pages.homePage import HomePage
from pages.projectPage import ProjectPage
from pages.testPage import TestPage
from test_data.constants import Constants
from utilities.csvManager import CsvManager
from utilities.dataComparator import DataComparator
from utilities.dataManager import DataManager
from pytest_check import check
from utilities.directoryManager import DirectoryManager
from utilities.generateRandomText import GenerateRandomText
from utilities.screenshotMaker import ScreenshootMaker


class TestProjectDataHandler:
    _csv_path = os.path.join('..', "test_data", "file.csv")
    _log_path = os.path.join('..', "Log")
    _remote_img_path = os.path.join('..', 'test_data', 'remote.png')
    _project_name = GenerateRandomText.generate_random_text(4)

    @pytest.mark.test_project_actions
    def test_project_actions(self, setup_session, request):
        Logger.info("Шаг 1. Получить токен согласно номеру варианта")
        start_time = datetime.utcfromtimestamp(time.time()).strftime(Constants().strftime_regular)
        token = ApiUtils.post(
            DataManager.get_value("url_api"), DataManager.get_value("get_token").
            format(DataManager.get_value("variant",  Constants().test_data_file_name))).text
        assert (isinstance(token, str) and bool(token)), "Токен не найден"

        Logger.info("Шаг 2. С помощью cookie передать токен. Обновить страницу.")
        BrowserServices.Instance.browser.driver.add_cookie({"name": 'token', "value": token})
        home_page = HomePage()
        assert home_page.state.wait_for_displayed(), "Страница проектов не отображена"
        BrowserServices.Instance.browser.refresh()
        assert home_page.variant == DataManager.get_value(
            "variant", Constants().test_data_file_name), "Не соответствует номер варианта указанный в футере"

        Logger.info("Шаг 3. Запросом к БД получить список тестов проекта Nexage.")
        session = setup_session
        project_page = ProjectPage()
        home_page.click_project(DataManager.get_value("project_Nexage", Constants().test_data_file_name))
        table_rows = project_page.tests_number
        selected_tests = Test.select(session, DataManager.get_value(
            "selectMaxStartTimeTestsByProject", Constants().sql_query_file_name).format(
            Project.select(session, DataManager.get_value(
                "selectProjectByName", Constants().sql_query_file_name).format(
                DataManager.get_value("project_Nexage", Constants().test_data_file_name)))[0].id, table_rows))
        CsvManager.write_csv(self._csv_path, project_page.table_headers, project_page.get_tests(table_rows))
        prepare_data = DataComparator.prepare_comparison_data(self._csv_path, selected_tests)
        check.equal(prepare_data['expected_data'], prepare_data['actual_data'])

        Logger.info("Шаг 4. UI, добавить проект и сохранить его.")
        BrowserServices.Instance.browser.go_back()
        home_page.click_add_project()
        home_page.add_project(self._project_name)
        assert home_page.is_alert_right(self._project_name), "Алерт с сообщением об успешном сохранении не появился."
        BrowserServices.Instance.browser.driver.switch_to.default_content()
        BrowserServices.Instance.browser.driver.execute_script(DataManager.get_value("closePopUp_js_script"))
        assert home_page.is_frame_closed(), "Окно добавления проекта не закрылось"
        BrowserServices.Instance.browser.refresh()
        assert home_page.is_new_project_add(self._project_name), "Проект не появился в списке"

        Logger.info("Шаг 5. Добавить тест через БД в созданный ранее проект.")
        home_page.click_project(self._project_name)
        ScreenshootMaker.make_page_screenshoot(project_page)
        with open(DirectoryManager.get_latest_file(self._log_path), 'r', encoding='latin-1') as file:
            log_content = re.sub(r'\s+', ' ', file.read().strip())
        with open(DirectoryManager.get_latest_file(BrowserServices.Instance.browser.download_directory), 'rb') as file:
            file_content = file.read()
        TestDataManager.add_test(session, request.node.name, start_time, self._project_name, log_content, file_content)
        assert project_page.is_test_displayed(request.node.name), "Название теста не появилось на странице проекта"

        Logger.info("Шаг 6. Перейти на страницу созданного теста.")
        project_page.click_test_link(request.node.name)
        test_page = TestPage()
        expected_data = {
            'file_content': file_content,
            'log': log_content,
            'project_name': self._project_name,
            'test_name': request.node.name,
            'method_name': DataManager.get_value("method", Constants().test_data_file_name),
            'status': DataManager.get_value("status", Constants().test_data_file_name),
            'start_time': start_time,
            'environment': DataManager.get_value("env", Constants().test_data_file_name),
            'browser': DataManager.get_value("browser", Constants().test_data_file_name),
            'name': DataManager.get_value("name", Constants().test_data_file_name),
            'login': DataManager.get_value("login", Constants().test_data_file_name),
            'email': DataManager.get_value("email", Constants().test_data_file_name)
        }
        check.equal(expected_data, test_page.get_test_data(self._remote_img_path))
