import logging
import os
import pytest
from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from utilities.dataManager import DataManager


@pytest.fixture(scope="session")
def setup_session(request, database_session):
    work_dir = RootPathHelper.current_root_path(__file__)
    os.chdir(work_dir)
    for log_name in [
        "selenium.webdriver.remote.remote_connection",
        "selenium.webdriver.common.selenium_manager",
        "urllib3.connectionpool",
    ]:
        logger = logging.getLogger(log_name)
        logger.disabled = True
    session = database_session
    BrowserServices.Instance.browser.go_to(DataManager.get_value("url_auth").format(
        DataManager.get_value("login"), DataManager.get_value("password")))
    BrowserServices.Instance.browser.maximize()
    yield session
    if BrowserServices.Instance.is_browser_started:
        BrowserServices.Instance.browser.quit()
    session.close()


@pytest.fixture(scope="session")
def database_session():
    Base = declarative_base()
    engine = create_engine(DataManager.get_value("database").
                           format(DataManager.get_value("login"), DataManager.get_value("password")))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
