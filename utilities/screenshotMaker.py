import os
from py_selenium_auto.browsers.browser_services import BrowserServices


class ScreenshootMaker:
    @staticmethod
    def make_page_screenshoot(page):
        directory_path = BrowserServices.Instance.browser.download_directory
        os.makedirs(directory_path, exist_ok=True)
        page.state.wait_for_displayed()
        with open(os.path.join(
                '..', directory_path, "screenshot.png"), "wb") as file:
            file.write(BrowserServices.Instance.browser.get_screenshot())
