from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from databaseUtils.sqlBase import SQLBase


class Log(declarative_base(), SQLBase):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    is_exception = Column(Integer, nullable=False)
    test_id = Column(Integer, nullable=False)

    def __init__(self, content, is_exception, test_id):
        self.content = content
        self.is_exception = is_exception
        self.test_id = test_id
