from models.dataBase.attachment import Attachment
from models.dataBase.author import Author
from models.dataBase.log import Log
from models.dataBase.project import Project
from models.dataBase.test import Test
from test_data.constants import Constants
from utilities.dataManager import DataManager


class TestDataManager:
    @staticmethod
    def add_test(session, test_name, start_time, project, log, screenshot):
        author = TestDataManager.get_author(session)
        project_id = TestDataManager.get_project_id(session, project)
        test_data = {
            'name': test_name,
            'status_id': int(DataManager.get_value("status", Constants().test_data_file_name)),
            'method_name': DataManager.get_value("method", Constants().test_data_file_name),
            'project_id': project_id,
            'session_id': int(DataManager.get_value("session_id", Constants().test_data_file_name)),
            'start_time': start_time,
            'end_time': None,
            'env': DataManager.get_value("env", Constants().test_data_file_name),
            'browser': DataManager.get_value("browser", Constants().test_data_file_name),
            'author_id': author.id
        }
        test_instance = Test.create(session, **test_data)
        TestDataManager.create_log(session, log, test_instance.id)
        TestDataManager.create_attachment(session, screenshot, test_instance.id)

    @staticmethod
    def get_author(session):
        author_data = {
            "name": DataManager.get_value("name", Constants().test_data_file_name),
            "login": DataManager.get_value("login", Constants().test_data_file_name),
            "email": DataManager.get_value("email", Constants().test_data_file_name)
        }
        author = Author.select(session, column_name='login', column_value=DataManager.get_value(
            "login", Constants().test_data_file_name))
        if author:
            return author
        else:
            return Author.create(session=session, **author_data)

    @staticmethod
    def get_project_id(session, project_name):
        return Project.select(session, column_name='name', column_value=project_name).id

    @staticmethod
    def create_log(session, log_content, test_id):
        log_data = {
            'content': log_content,
            'is_exception': int(DataManager.get_value("is_exception", Constants().test_data_file_name)),
            'test_id': test_id
        }
        Log.create(session, **log_data)

    @staticmethod
    def create_attachment(session, content, test_id):
        attachment_data = {
            'content': content,
            'content_type': 'image/png',
            'test_id': test_id
        }
        Attachment.create(session, **attachment_data)
