from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from databaseUtils.sqlBase import SQLBase
from models.dataBase.attachment import Attachment
from models.dataBase.author import Author
from models.dataBase.log import Log
from models.dataBase.project import Project
from models.dataBase.session import Session
from models.dataBase.status import Status


class Test(declarative_base(), SQLBase):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status_id = Column(Integer, ForeignKey(Status.id), nullable=False)
    method_name = Column(String)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    session_id = Column(Integer, ForeignKey(Session.id), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    env = Column(String)
    browser = Column(String)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=True)

    def __init__(self, name, status_id, method_name, project_id, session_id, start_time, end_time, env, browser, author_id):
        self.name = name
        self.status_id = status_id
        self.method_name = method_name
        self.project_id = project_id
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.env = env
        self.browser = browser
        self.author_id = author_id
