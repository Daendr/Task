from py_selenium_auto.browsers.browser_services import BrowserServices
from selenium.webdriver.common.by import By
from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.text_box import TextBox
from py_selenium_auto.elements.button import Button
from utilities.dataManager import DataManager
from utilities.regexUtils import RegexUtils


class HomePage(Form):
    _footer_variant = Label(Locator(By.XPATH, "//*[contains(@class, 'footer-text')]/*"), "footer_variant")
    _add_project = Label(Locator(By.XPATH, "//*[contains(text(), '+Add')]"), "add_project")
    _project_nexage = Label(Locator(By.XPATH, "//*[contains(text(), 'Nexage')]"), "project_nexage")
    _input_project_name = TextBox(Locator(By.ID, "projectName"), "input_project_name")
    _submit = Button(Locator(By.XPATH, "//*[contains(@class, 'btn-primary') and (@type='submit')]"), "submit")
    _success_alert = Label(Locator(By.XPATH, "//*[contains(@class, 'alert-success')]"), "success_alert")
    _iframe_add_project = Label(Locator(By.ID, "addProjectFrame"), "iframe_add_project")
    _test_project = ("//*[contains(text(), '{}')]", "test_project")
    _alert_success_word = "Project {} saved"

    def __init__(self):
        super().__init__(Locator(By.XPATH, "//*[contains(text(), 'Available projects')]"), "Home Page")

    def get_variant(self):
        return RegexUtils.extract_digits(self._footer_variant.text)

    def click_add_project(self):
        self._add_project.click()

    def click_project_nexage(self):
        self._project_nexage.click()

    def add_project(self, project_name):
        BrowserServices.Instance.browser.driver.switch_to.frame(self._iframe_add_project.locator.value)
        BrowserServices.Instance.browser.driver.execute_script(
            DataManager.get_value("send_key_js_script"),
            BrowserServices.Instance.browser.driver.find_element(By.ID, self._input_project_name.locator.value),
            project_name
        )
        BrowserServices.Instance.browser.driver.execute_script(
            DataManager.get_value("click_js_script"),
            BrowserServices.Instance.browser.driver.find_element(By.XPATH, self._submit.locator.value)
        )

    def is_alert_right(self, project_name):
        return self._alert_success_word.format(project_name) in self._success_alert.text

    def is_frame_closed(self):
        return self._iframe_add_project.state.wait_for_not_displayed()

    def is_new_project_add(self, project):
        return Label(Locator(By.XPATH, self._test_project[0].format(project)),
                     self._test_project[1]).state.wait_for_displayed()

    def click_project(self, project):
        return Label(Locator(By.XPATH, self._test_project[0].format(project)), self._test_project[1]).click()

    variant = property(get_variant)
